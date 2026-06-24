# Release Notes: v0.44.0 Repository Release Candidate

Date: 2026-06-24

This release candidate prepares the Dot-Trace Theory repository to be cited as a manuscript companion and reproducibility package.

## Added

- Reproducible Experiment 1 orchestration script:

```text
scripts/run_experiment_01_prediction_lift.py
```

- Experiment 1 configuration:

```text
configs/experiment_01_prediction_lift.json
```

- Experiment 1 documentation:

```text
docs/experiments/experiment_01_prediction_lift.md
```

- Repository reproducibility statement:

```text
docs/reproducibility_statement.md
```

- Code availability statement:

```text
docs/code_availability_statement.md
```

- Repository submission checklist:

```text
docs/repository_submission_checklist.md
```

- Author metadata file:

```text
AUTHORS.md
```

- Contribution guidelines:

```text
CONTRIBUTING.md
```

- Lightweight repository smoke test:

```text
tests/test_repository_smoke.py
```

- GitHub Actions workflow files for Python checks and LaTeX build.

## Updated

- README with Experiment 1 commands and publication-facing documentation links.
- Makefile with `experiment-01`, `experiment-01-quick`, `experiment-01-dry-run`, and `test` targets.
- `.gitignore` with generated output and LaTeX build artifacts.
- `CITATION.cff` with the correct repository URL.
- `pyproject.toml` with repository URLs and v0.44.0 version metadata.
- `SECURITY.md` with misuse and security reporting guidance.
- Publication metadata checklist.

## Remaining author decisions before formal submission

- Confirm final author name(s), affiliation(s), email, and ORCID(s).
- Replace provisional metadata in `CITATION.cff`, `AUTHORS.md`, `pyproject.toml`, and `paper/main.tex`.
- Choose and activate a repository license.
- Decide whether to tag and archive a DOI-bearing release.
- Add the final repository or DOI citation to the paper.

## Interpretation boundary

Experiment 1 is synthetic. It is a mechanism and reproducibility check, not external empirical validation of Dot-Trace Theory in real social systems.
