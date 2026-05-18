# Dot-Trace Theory Core Article Blueprint v0.42

## Proposed title

**Dot-Trace Theory: Persistent Social Memory-Traces in Multi-Agent Systems**

Alternative subtitle:

**A Formal Representation for the Co-Evolution of Memory, Action, and Social Topology**

## Target length

35-50 pages before appendices.

## Core article thesis

A memory-sensitive social multi-agent system cannot always be adequately represented by agents, edges, and ordinary state variables alone. When persistent, socially accessible traces of prior events affect action, trust, retrieval, and topology, the state must include a dot field: dots, dot-dot relations, agent-dot access, memory weights, effective retrieval strengths, and lineage or institutional anchors where relevant.

## Proposed structure

### 1. Introduction

Purpose: motivate the representational problem.

Must include:

- examples: promise, accusation, audit log, correction, institutional record;
- reduced state \(Z_t=(A,E_t,X_t,\bar S_t)\);
- dot-field state as representational extension;
- conditional novelty claim;
- contribution summary.

Recommended length: 4-6 pages.

### 2. Related Work and Representational Gap

Purpose: show what existing literatures capture and what they leave unformalized.

Include only high-yield comparisons:

- dynamic graph learning;
- agent memory and generative agents;
- graph-based memory;
- collective memory and social networks;
- social capital;
- institutional memory.

Recommended length: 5-7 pages.

### 3. Ontology: Dots and the Dot Field

Purpose: define the primitive objects.

Include:

- dot definition;
- dot versus event, memory, edge;
- agent set \(A\);
- social graph \(G_t^A\);
- dot graph \(G_t^D\);
- access graph \(G_t^B\);
- core and augmented dot fields;
- dot lifecycle figure.

Recommended length: 6-8 pages.

### 4. State Hierarchy and Formal Dynamics

Purpose: define the model and compare state levels.

Include:

\[
Z_t=(A,E_t,X_t,\bar S_t),
\]

\[
\Omega_t^{core}=(A,E_t,X_t,\bar S_t,D_t,R_t^D,B_t),
\]

\[
\Omega_t^{aug}=(\Omega_t^{core},\mathbf M_t,Q_t,L_t,I_t,C_t).
\]

Then include reduced transition:

\[
\Omega_{t+1}^{aug}=\mathscr F_t(\Omega_t^{aug},X_{t+1},\varepsilon_{t+1}).
\]

Recommended length: 5-6 pages.

### 5. Main Theoretical Results

Purpose: present the theorem spine.

Core results only:

1. Representational insufficiency.
2. Dot-field Markov restoration.
3. Dot consensus and fragmentation.
4. Temporal sequencing/non-commutativity.
5. Mixed-mechanism well-definedness.
6. Recursive topology-feedback stability.

Mechanism-specific theorems should be summarized but moved to the technical companion.

Recommended length: 10-14 pages.

### 6. Measurement and Validation Implications

Purpose: show how the theory can be tested without overclaiming.

Include:

- minimum dot test;
- access, attention, retrieval distinction;
- observability ladder;
- prediction-lift claim;
- negative controls;
- identifiability warning.

Recommended length: 5-7 pages.

### 7. Worked Examples

Purpose: make the theory concrete.

Use 2 or 3 examples only:

- two-agent trust repair after betrayal;
- organizational incident memory;
- public accusation and correction.

Recommended length: 4-5 pages.

### 8. Applications, Boundaries, and Governance

Purpose: show relevance and limits.

Include:

- AI multi-agent systems;
- organizational memory;
- misinformation/correction;
- institutional records;
- privacy, contestability, auditability;
- when dot fields are unnecessary.

Recommended length: 4-6 pages.

### 9. Conclusion

Purpose: restate the core representational contribution.

Recommended length: 1-2 pages.

## Main figures for the core article

1. Conceptual overview.
2. State hierarchy.
3. Dot lifecycle.
4. Mixed-mechanism transition.
5. Recursive topology-memory feedback.
6. Theorem spine.

## Main tables for the core article

1. Dot ontology summary.
2. State hierarchy summary.
3. Theorem spine table.
4. Measurement observability ladder.
5. Boundary conditions.

## Material to move to technical companion

- full metric list;
- all simulation programs;
- trainable prediction runner details;
- calibration protocol;
- implementation store/index details;
- full measurement codebook;
- all mechanism-specific proofs;
- exhaustive hypotheses;
- extended governance framework;
- full glossary.

## Drafting principle

The core article should not try to prove every mechanism. It should prove that the dot-field representation is necessary under memory-sensitive trace conditions, then show that the representation supports a coherent family of dynamics. The companion can carry the full mechanism suite.
