# Publication Metadata to Complete

This repository is structurally prepared for use as a manuscript companion. The items below require author or venue decisions before formal submission, preprint release, DOI archival, or public reuse.

## Author metadata

- [ ] Full author name or author list
- [ ] Affiliation(s)
- [ ] Corresponding author email
- [ ] ORCID identifier(s), if available
- [ ] Contributor roles, if desired
- [ ] Final author order, if more than one author

Files to update:

```text
paper/main.tex
AUTHORS.md
CITATION.cff
pyproject.toml
```

## Manuscript metadata

- [ ] Final title confirmation
- [ ] Abstract approval
- [ ] Keywords
- [ ] Short title, if needed
- [ ] Target venue or preprint server
- [ ] Preferred citation format
- [ ] Repository citation statement
- [ ] Code availability statement

Suggested repository sentence:

> Code, LaTeX source, reference simulator prototypes, synthetic validation scripts, and reproducibility documentation are available at `https://github.com/alqithami/DotTheory`.

## Required statements

- [ ] Acknowledgements
- [ ] Funding statement
- [ ] Competing interests statement
- [ ] Data availability statement
- [ ] Code availability statement
- [ ] Ethics statement
- [ ] AI assistance statement, if required by the selected venue

Draft wording for the code statement is available in:

```text
docs/code_availability_statement.md
```

## Licensing

Current repository license status: pending.

Decide whether to use:

- CC BY 4.0 for manuscript, documentation, and diagrams;
- MIT or Apache-2.0 for code;
- another license structure;
- or a private/all-rights-reserved release.

Files to update after the license decision:

```text
LICENSE.md
CITATION.cff
README.md
pyproject.toml
```

## Repository publication

- [x] Replace placeholder GitHub URL in `CITATION.cff`.
- [x] Add repository reproducibility statement.
- [x] Add code availability statement.
- [x] Add repository submission checklist.
- [x] Add Experiment 1 runner and configuration.
- [x] Add GitHub Actions workflow files.
- [ ] Replace provisional author metadata in `CITATION.cff`, `AUTHORS.md`, and `pyproject.toml`.
- [ ] Update `LICENSE.md` after license decision.
- [ ] Add maintainer contact or preferred private-reporting route in `SECURITY.md`.
- [ ] Create a tagged release.
- [ ] Archive the release with a DOI if the target venue expects durable code citation.

## Repository checks before submission

Run:

```bash
make check
make paper
make experiment-01-quick
```

For a full synthetic experiment run:

```bash
make experiment-01
```

If these pass locally, the repository is ready to be cited as a reproducible companion, subject to the author and license decisions above.
