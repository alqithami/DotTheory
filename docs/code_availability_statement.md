# Code Availability Statement

The code accompanying **Dot-Trace Theory: A Formal Theory of Agentic Social Memory** is available in this repository:

```text
https://github.com/alqithami/DotTheory
```

The repository contains:

- the LaTeX manuscript source;
- the BibTeX bibliography;
- reference simulator prototypes;
- validation and prediction-lift runners;
- Experiment 1 configuration and orchestration script;
- documentation for reproducibility, interpretation, and reporting.

## Suggested manuscript wording

A publication-facing code availability statement may use the following wording after author metadata and license decisions are finalized:

> Code and LaTeX source for the foundation manuscript and synthetic computational demonstrations are available at `https://github.com/alqithami/DotTheory`. The repository includes reference simulators, validation runners, Experiment 1 configuration files, and reproducibility documentation. The computational experiment is synthetic and is intended as a mechanism check rather than external empirical validation.

If the repository is archived with a DOI, replace or supplement the GitHub URL with the DOI.

## Generated outputs

Generated experiment outputs are not tracked by default. To reproduce them, run:

```bash
make experiment-01
```

or, for a quick smoke run:

```bash
make experiment-01-quick
```

The outputs will be written under:

```text
results/experiment_01/
```

## License status

The repository license is currently marked as pending. Before formal publication or public reuse, the author should finalize the license for:

1. manuscript and documentation;
2. diagrams and figures;
3. software scripts;
4. generated outputs, if shared.
