# Repository Submission Checklist

This checklist should be completed before the repository is cited in a submitted manuscript, preprint, or public release.

## Required before manuscript submission

- [ ] Confirm final author name(s) in `paper/main.tex`.
- [ ] Confirm author metadata in `AUTHORS.md`.
- [ ] Confirm author metadata in `CITATION.cff`.
- [ ] Replace provisional author fields in `pyproject.toml`.
- [ ] Choose and activate a repository license.
- [ ] Update `LICENSE.md` after license decision.
- [ ] Add corresponding author or issue-reporting route in `SECURITY.md`.
- [ ] Decide whether to archive a release with DOI.
- [ ] If DOI is created, add it to `CITATION.cff`, README, and the manuscript.

## Required checks

Run:

```bash
make check
```

Expected behavior:

- Python files compile;
- placeholder scan passes;
- citation check passes;
- smoke tests complete.

If the paper source is included in the submitted artifact, run:

```bash
make paper
```

Expected behavior:

- `paper/main.pdf` builds successfully;
- BibTeX processing succeeds;
- no missing citation keys;
- no unresolved cross-references after final compile.

## Experiment 1 reproducibility

For a quick sanity check:

```bash
make experiment-01-quick
```

For the full configured synthetic experiment:

```bash
make experiment-01
```

Confirm that the following files are generated:

```text
results/experiment_01/experiment_01_summary.json
results/experiment_01/paper_results_table.csv
results/experiment_01/figures/prediction_lift_full.svg
results/experiment_01/figures/negative_control_degradation.svg
results/experiment_01/figures/ablation_lift_by_condition.svg
```

## Manuscript reference to repository

A cautious repository-reference sentence for the manuscript is:

> The accompanying repository contains the LaTeX source, reference simulator prototypes, synthetic validation scripts, and reproducibility instructions for the computational demonstration: `https://github.com/alqithami/DotTheory`.

If a DOI is created, use:

> The accompanying repository is archived at [DOI] and mirrored at `https://github.com/alqithami/DotTheory`.

## Claim boundaries

When citing this repository in the manuscript, preserve the following distinction:

- The paper's formal theorems are theoretical results under stated assumptions.
- Experiment 1 is a synthetic mechanism check.
- The repository scripts are reference implementations.
- None of the repository outputs constitute external empirical validation of real social systems.

## Recommended release process

1. Complete metadata and license fields.
2. Run `make check` and `make paper`.
3. Run `make experiment-01-quick`.
4. Optionally run `make experiment-01`.
5. Create a Git tag, for example:

```bash
git tag -a v0.44.0 -m "Dot-Trace Theory repository release candidate"
git push origin v0.44.0
```

6. Archive the release if a DOI is needed.
7. Update the manuscript repository citation with the tagged release or DOI.
