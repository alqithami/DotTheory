#!/usr/bin/env python3
"""
Minimal Dot-Trace Theory simulator.

This is a compact, dependency-free reference implementation of the core
Dot-Trace loop:
interaction -> dot creation -> retrieval -> action -> transmission/mutation
-> correction -> lifecycle update -> social-edge update -> logging.

It is intended as a transparent starter simulator, not a final empirical model.
Run:
    python dot_trace_minimal_simulator_v01.py --agents 8 --steps 30 --seed 7 --out dtt_run
"""

from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple


def sigmoid(x: float) -> float:
    # Stable enough for small simulator ranges.
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def clip(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def clip_signed(x: float) -> float:
    return max(-1.0, min(1.0, x))


@dataclass
class Config:
    agents: int = 8
    steps: int = 30
    interactions_per_step: int = 8
    top_k: int = 5
    seed: int = 7
    initial_trust: float = 0.50
    trust_noise: float = 0.10
    lambda_memory: float = 0.96
    eta_edge: float = 0.12
    p_transmit: float = 0.08
    p_institutional: float = 0.05
    p_counter: float = 0.00
    beta_z: float = 1.25
    beta_w: float = 1.00
    actor_bias: float = -0.15
    alpha_0: float = 0.0
    alpha_z: float = 1.50
    mutation_enabled: bool = False
    mutation_epsilon: float = 0.08
    correction_enabled: bool = False
    correction_strength: float = 0.35
    retrieval_relevance_weight: float = 1.00
    retrieval_memory_weight: float = 1.00
    retrieval_credibility_weight: float = 0.75
    retrieval_recency_weight: float = 0.20
    retrieval_social_weight: float = 0.50
    reinforce_retrieved: float = 0.04
    reinforce_anchor: float = 0.02
    edge_threshold: float = 0.50


@dataclass
class Agent:
    id: int
    group: int = 0
    bias: float = 0.0


@dataclass
class Dot:
    id: int
    origin: int
    target: int
    dot_type: str
    content: str
    x: float
    valence: float
    credibility: float
    created_at: int
    parents: List[int] = field(default_factory=list)
    status: str = "active"
    anchored: bool = False


@dataclass
class Event:
    time: int
    event_type: str
    actors: List[int]
    dots: List[int] = field(default_factory=list)
    parents: List[int] = field(default_factory=list)
    details: Dict[str, object] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)


class DotTraceState:
    def __init__(self, config: Config, rng: random.Random):
        self.config = config
        self.rng = rng
        self.agents: List[Agent] = [Agent(i, group=i % 2, bias=config.actor_bias) for i in range(config.agents)]
        self.dots: Dict[int, Dot] = {}
        self.next_dot_id = 1
        # Directed social/trust weights W[i][j].
        self.W: List[List[float]] = [[0.0 for _ in self.agents] for _ in self.agents]
        for i in range(config.agents):
            for j in range(config.agents):
                if i == j:
                    self.W[i][j] = 0.0
                else:
                    self.W[i][j] = clip(config.initial_trust + rng.uniform(-config.trust_noise, config.trust_noise))
        # Agent-dot access and agent-specific memory weights.
        self.access: Dict[int, Set[int]] = {a.id: set() for a in self.agents}
        self.memory: Dict[Tuple[int, int], float] = {}
        # Dot-dot relation edges as (source, relation, target).
        self.relations: List[Tuple[int, str, int]] = []
        self.events: List[Event] = []
        self.cooperation_count = 0
        self.action_count = 0

    def log(self, event: Event) -> None:
        self.events.append(event)

    def create_dot(
        self,
        *,
        time: int,
        origin: int,
        target: int,
        dot_type: str,
        content: str,
        x: float,
        valence: float,
        credibility: float,
        parents: Optional[List[int]] = None,
        anchored: bool = False,
        grant_to: Optional[Iterable[int]] = None,
    ) -> Dot:
        dot = Dot(
            id=self.next_dot_id,
            origin=origin,
            target=target,
            dot_type=dot_type,
            content=content,
            x=x,
            valence=clip_signed(valence),
            credibility=clip(credibility),
            created_at=time,
            parents=list(parents or []),
            anchored=anchored,
        )
        self.next_dot_id += 1
        self.dots[dot.id] = dot
        for parent in dot.parents:
            self.relations.append((parent, "parent_of", dot.id))
        if grant_to is None:
            grant_to = [origin]
        for aid in grant_to:
            self.grant_access(aid, dot.id, initial_weight=0.75)
        self.log(Event(time, "dot_created", [origin, target], [dot.id], dot.parents, {
            "type": dot_type,
            "valence": dot.valence,
            "credibility": dot.credibility,
            "anchored": dot.anchored,
        }))
        return dot

    def grant_access(self, agent_id: int, dot_id: int, initial_weight: float = 0.50) -> None:
        self.access[agent_id].add(dot_id)
        self.memory[(agent_id, dot_id)] = max(self.memory.get((agent_id, dot_id), 0.0), clip(initial_weight))

    def memory_weight(self, agent_id: int, dot_id: int) -> float:
        return self.memory.get((agent_id, dot_id), 0.0)

    def retrieve(self, agent_id: int, target: int, time: int, top_k: Optional[int] = None) -> List[Tuple[float, Dot]]:
        cfg = self.config
        top_k = cfg.top_k if top_k is None else top_k
        scored: List[Tuple[float, Dot]] = []
        for dot_id in self.access[agent_id]:
            dot = self.dots.get(dot_id)
            if not dot or dot.status != "active":
                continue
            relevance = 1.0 if dot.target == target else 0.15
            mem = self.memory_weight(agent_id, dot_id)
            recency = 1.0 / (1.0 + max(0, time - dot.created_at))
            social = self.W[agent_id][dot.origin] if agent_id != dot.origin else 1.0
            score = (
                cfg.retrieval_relevance_weight * relevance
                + cfg.retrieval_memory_weight * mem
                + cfg.retrieval_credibility_weight * dot.credibility
                + cfg.retrieval_recency_weight * recency
                + cfg.retrieval_social_weight * social
            )
            scored.append((score, dot))
        scored.sort(key=lambda item: item[0], reverse=True)
        selected = scored[:top_k]
        self.log(Event(time, "dots_retrieved", [agent_id, target], [d.id for _, d in selected], details={
            "scores": [(d.id, round(s, 4)) for s, d in selected]
        }))
        return selected

    def pressure(self, agent_id: int, target: int, retrieved: Sequence[Tuple[float, Dot]]) -> float:
        z = 0.0
        for _, dot in retrieved:
            if dot.target == target:
                z += self.memory_weight(agent_id, dot.id) * dot.credibility * dot.valence
        return z


class DotTraceSimulator:
    def __init__(self, config: Config):
        self.config = config
        self.rng = random.Random(config.seed)
        self.state = DotTraceState(config, self.rng)

    def sample_pairs(self) -> List[Tuple[int, int]]:
        n = self.config.agents
        pairs: List[Tuple[int, int]] = []
        for _ in range(self.config.interactions_per_step):
            i = self.rng.randrange(n)
            j = self.rng.randrange(n - 1)
            if j >= i:
                j += 1
            pairs.append((i, j))
        return pairs

    def sample_action(self, i: int, j: int, z_ij: float) -> Tuple[str, float]:
        cfg = self.config
        p = sigmoid(self.state.agents[i].bias + cfg.beta_w * self.state.W[i][j] + cfg.beta_z * z_ij)
        action = "cooperate" if self.rng.random() < p else "defect"
        return action, p

    def create_action_dot(self, time: int, actor: int, recipient: int, action: str) -> Dot:
        cfg = self.config
        positive = action == "cooperate"
        valence = 1.0 if positive else -1.0
        content = f"agent {actor} {action}ed toward agent {recipient} at t={time}"
        anchored = self.rng.random() < cfg.p_institutional
        # The recipient observes and originates the evaluative dot about the actor.
        return self.state.create_dot(
            time=time,
            origin=recipient,
            target=actor,
            dot_type="evaluation",
            content=content,
            x=valence,
            valence=valence,
            credibility=0.85,
            anchored=anchored,
            grant_to=[recipient],
        )

    def transmit(self, time: int) -> None:
        cfg = self.config
        st = self.state
        for i in range(cfg.agents):
            if not st.access[i]:
                continue
            # Limit transmission attempts for inspectability.
            candidate_ids = list(st.access[i])
            self.rng.shuffle(candidate_ids)
            for j in range(cfg.agents):
                if i == j:
                    continue
                for dot_id in candidate_ids[: min(5, len(candidate_ids))]:
                    dot = st.dots[dot_id]
                    p = cfg.p_transmit * st.W[i][j] * dot.credibility
                    if self.rng.random() >= p:
                        continue
                    if cfg.mutation_enabled:
                        noise = self.rng.uniform(-cfg.mutation_epsilon, cfg.mutation_epsilon)
                        new_valence = clip_signed(dot.valence + noise)
                        child = st.create_dot(
                            time=time,
                            origin=i,
                            target=dot.target,
                            dot_type="mutated_" + dot.dot_type,
                            content=dot.content + f" | retold by {i} to {j}",
                            x=dot.x + noise,
                            valence=new_valence,
                            credibility=clip(dot.credibility * 0.95),
                            parents=[dot.id],
                            anchored=dot.anchored,
                            grant_to=[j],
                        )
                        st.log(Event(time, "dot_mutated", [i, j], [child.id], [dot.id], {"noise": noise}))
                    else:
                        st.grant_access(j, dot.id, initial_weight=0.45)
                        st.log(Event(time, "dot_transmitted", [i, j], [dot.id], details={"probability": p}))

    def maybe_correct(self, time: int) -> None:
        cfg = self.config
        if not cfg.correction_enabled:
            return
        st = self.state
        for dot in list(st.dots.values()):
            if dot.status != "active" or dot.valence >= 0:
                continue
            if self.rng.random() >= cfg.p_counter:
                continue
            c = st.create_dot(
                time=time,
                origin=dot.target,
                target=dot.target,
                dot_type="counter_dot",
                content=f"counter-dot challenging dot {dot.id}",
                x=-dot.x,
                valence=abs(dot.valence),
                credibility=0.90,
                parents=[dot.id],
                grant_to=[dot.target],
            )
            st.relations.append((c.id, "contradicts", dot.id))
            # Reduce active memory of the target dot for agents who can access the counter-dot.
            for aid in list(st.access.keys()):
                if c.id in st.access[aid] and dot.id in st.access[aid]:
                    old = st.memory_weight(aid, dot.id)
                    st.memory[(aid, dot.id)] = clip(old - cfg.correction_strength)
            st.log(Event(time, "counter_dot_generated", [dot.target], [c.id], [dot.id], {}))

    def update_memory(self, time: int) -> None:
        cfg = self.config
        st = self.state
        for (aid, dot_id), old in list(st.memory.items()):
            dot = st.dots.get(dot_id)
            if dot is None:
                continue
            new = cfg.lambda_memory * old
            if dot.anchored:
                new += cfg.reinforce_anchor
            st.memory[(aid, dot_id)] = clip(new)

    def reinforce_retrieved(self, agent_id: int, retrieved: Sequence[Tuple[float, Dot]]) -> None:
        cfg = self.config
        st = self.state
        for _, dot in retrieved:
            key = (agent_id, dot.id)
            st.memory[key] = clip(st.memory.get(key, 0.0) + cfg.reinforce_retrieved)

    def update_edges(self, time: int) -> None:
        cfg = self.config
        st = self.state
        for i in range(cfg.agents):
            for j in range(cfg.agents):
                if i == j:
                    continue
                retrieved = st.retrieve(i, j, time, top_k=cfg.top_k)
                z = st.pressure(i, j, retrieved)
                target_w = sigmoid(cfg.alpha_0 + cfg.alpha_z * z)
                old = st.W[i][j]
                st.W[i][j] = clip((1.0 - cfg.eta_edge) * old + cfg.eta_edge * target_w)
                st.log(Event(time, "social_edge_updated", [i, j], [d.id for _, d in retrieved], details={
                    "old": round(old, 4),
                    "new": round(st.W[i][j], 4),
                    "pressure": round(z, 4),
                }))

    def step(self, time: int) -> None:
        st = self.state
        # Decision and dot creation.
        for i, j in self.sample_pairs():
            retrieved = st.retrieve(i, j, time)
            z = st.pressure(i, j, retrieved)
            self.reinforce_retrieved(i, retrieved)
            action, p = self.sample_action(i, j, z)
            st.action_count += 1
            if action == "cooperate":
                st.cooperation_count += 1
            st.log(Event(time, "action_sampled", [i, j], [d.id for _, d in retrieved], details={
                "action": action,
                "probability": round(p, 4),
                "pressure": round(z, 4),
                "trust": round(st.W[i][j], 4),
            }))
            self.create_action_dot(time, i, j, action)
        # Transmission, correction, lifecycle, topology.
        self.transmit(time)
        self.maybe_correct(time)
        self.update_memory(time)
        self.update_edges(time)
        st.log(Event(time, "metrics", [], details=self.metrics()))

    def run(self) -> DotTraceState:
        for t in range(self.config.steps):
            self.step(t)
        return self.state

    def metrics(self) -> Dict[str, float]:
        st = self.state
        n = self.config.agents
        edge_values = [st.W[i][j] for i in range(n) for j in range(n) if i != j]
        active_dots = sum(1 for d in st.dots.values() if d.status == "active")
        access_count = sum(len(v) for v in st.access.values())
        cooperation_rate = st.cooperation_count / st.action_count if st.action_count else 0.0
        # Simple two-group fragmentation: distance between mean dot valence by group over accessible dots.
        group_vals: Dict[int, List[float]] = {0: [], 1: []}
        for agent in st.agents:
            for dot_id in st.access[agent.id]:
                dot = st.dots[dot_id]
                group_vals[agent.group].append(dot.valence * st.memory_weight(agent.id, dot_id))
        g0 = sum(group_vals[0]) / len(group_vals[0]) if group_vals[0] else 0.0
        g1 = sum(group_vals[1]) / len(group_vals[1]) if group_vals[1] else 0.0
        return {
            "cooperation_rate": round(cooperation_rate, 6),
            "mean_trust": round(sum(edge_values) / len(edge_values), 6) if edge_values else 0.0,
            "active_dots": float(active_dots),
            "access_count": float(access_count),
            "anchored_dots": float(sum(1 for d in st.dots.values() if d.anchored)),
            "fragmentation_proxy": round(abs(g0 - g1), 6),
        }

    def summary(self) -> Dict[str, object]:
        st = self.state
        return {
            "config": asdict(self.config),
            "metrics": self.metrics(),
            "dot_count": len(st.dots),
            "event_count": len(st.events),
            "final_social_matrix": [[round(x, 4) for x in row] for row in st.W],
            "threshold_edges": [
                [i, j] for i in range(self.config.agents) for j in range(self.config.agents)
                if i != j and st.W[i][j] > self.config.edge_threshold
            ],
        }


def write_outputs(sim: DotTraceSimulator, out_prefix: str) -> Tuple[Path, Path]:
    prefix = Path(out_prefix)
    log_path = prefix.with_name(prefix.name + "_log.jsonl")
    summary_path = prefix.with_name(prefix.name + "_summary.json")
    log_path.write_text("\n".join(event.to_json() for event in sim.state.events) + "\n", encoding="utf-8")
    summary_path.write_text(json.dumps(sim.summary(), indent=2, sort_keys=True), encoding="utf-8")
    return log_path, summary_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minimal Dot-Trace Theory simulator")
    parser.add_argument("--agents", type=int, default=8)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--interactions-per-step", type=int, default=8)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--mutation", action="store_true")
    parser.add_argument("--correction", action="store_true")
    parser.add_argument("--p-counter", type=float, default=0.05)
    parser.add_argument("--p-transmit", type=float, default=0.08)
    parser.add_argument("--p-institutional", type=float, default=0.05)
    parser.add_argument("--out", type=str, default="dtt_minimal_run")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = Config(
        agents=args.agents,
        steps=args.steps,
        interactions_per_step=args.interactions_per_step,
        seed=args.seed,
        top_k=args.top_k,
        mutation_enabled=args.mutation,
        correction_enabled=args.correction,
        p_counter=args.p_counter,
        p_transmit=args.p_transmit,
        p_institutional=args.p_institutional,
    )
    sim = DotTraceSimulator(cfg)
    sim.run()
    log_path, summary_path = write_outputs(sim, args.out)
    print(json.dumps({"summary": summary_path.as_posix(), "log": log_path.as_posix(), **sim.metrics()}, indent=2))


if __name__ == "__main__":
    main()
