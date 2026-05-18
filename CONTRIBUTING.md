# Contributing

This repository is currently prepared as a foundation package for Dot-Trace Theory. Contributions should preserve the distinction between:

1. formal claims,
2. measurement claims,
3. implementation claims,
4. validation claims,
5. governance claims.

## Suggested contribution workflow

1. Create a branch with a descriptive name.
2. Keep manuscript changes in `paper/main.tex` and bibliography changes in `paper/references.bib`.
3. Run `make check` before opening a pull request.
4. For theorem changes, state which assumptions change and whether the result is a theorem, proposition, lemma, or corollary.
5. For simulator changes, include a smoke test and document any changed output schema.
6. For new references, verify author order, title, year, venue, DOI/arXiv identifier, and URL.

## Manuscript style

Avoid development-log language in the paper body. Keep uncertainty in scope conditions, assumptions, limitations, and open problems rather than in conversational statements.
