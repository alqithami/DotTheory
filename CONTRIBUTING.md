# Contributing

Thank you for considering a contribution to Dot-Trace Theory.

This repository contains a theory manuscript, mathematical notation, diagrams, reference simulators, and synthetic validation tools. Contributions should preserve the distinction between formal theory, synthetic demonstration, and external empirical validation.

## Contribution areas

Useful contributions include:

- corrections to notation, definitions, proofs, or theorem statements;
- improvements to diagrams and figure captions;
- BibTeX metadata corrections;
- reproducibility improvements for the simulator and experiment scripts;
- additional negative controls or ablation settings;
- documentation improvements;
- issue reports identifying unclear claims, overclaims, or missing assumptions.

## Claim discipline

When contributing, please maintain the following claim boundaries.

1. **Formal claims** may follow from definitions and assumptions.
2. **Synthetic experiment claims** apply only to the configured simulator.
3. **Empirical claims** require external data, measurement validation, and appropriate causal or predictive design.
4. **Governance claims** require domain-specific ethical and legal analysis.

Do not convert a synthetic result into a real-world empirical claim.

## Development workflow

1. Open an issue describing the proposed change.
2. Use a branch for non-trivial edits.
3. Keep changes focused: paper edits, code edits, or documentation edits should be separable where possible.
4. Run repository checks before submitting a pull request:

```bash
make check
```

5. If editing the paper, also run:

```bash
make paper
```

6. If editing Experiment 1, run at least:

```bash
make experiment-01-quick
```

## Paper edits

For changes to `paper/main.tex`:

- preserve notation conventions for `R_t^D`, `\mathcal M_i(t)`, and `\mathcal V_i(q,t)`;
- avoid draft-language markers such as `TODO`, `TBD`, and `placeholder`;
- keep figure captions self-contained;
- ensure citations are represented in `paper/references.bib`;
- avoid adding unsupported publication or empirical claims.

## Code edits

The reference scripts are intentionally dependency-free unless a dependency is explicitly justified. If adding a dependency, update `pyproject.toml`, the README, and any relevant workflow files.

## Security and misuse

Do not contribute functionality designed for surveillance, reputational scoring of real people, covert influence, or consequential social decisions. See `SECURITY.md` for misuse-reporting guidance.
