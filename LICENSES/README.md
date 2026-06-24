# License Templates and Decision Notes

The repository license is currently pending. This directory records the recommended licensing structure before a formal license is activated.

## Recommended structure

For an open scholarly release, a common split is:

| Material | Recommended license option |
|---|---|
| Manuscript, documentation, diagrams, and educational materials | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| Source code and simulator scripts | MIT License or Apache License 2.0 |
| Generated synthetic outputs | Same as documentation or a data-specific license, depending on release strategy |

## Before activating a license

Confirm:

1. author approval;
2. institutional or funder requirements;
3. target venue requirements;
4. whether code and manuscript should use separate licenses;
5. whether generated outputs should be archived and licensed.

## Activation procedure

After a license decision:

1. replace the pending language in `LICENSE.md`;
2. update `CITATION.cff`;
3. update `pyproject.toml`;
4. update the README license section;
5. tag a release if the repository will be cited.

Do not assume a license is granted while `LICENSE.md` states that licensing is pending.
