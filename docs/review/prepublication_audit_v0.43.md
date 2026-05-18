# Dot-Trace Theory: Pre-Publication Proofreading and Readiness Audit

**Manuscript audited:** `dot_trace_theory_overleaf_v43.tex`  
**Compiled PDF:** `dot_trace_theory_overleaf_v43.pdf`  
**Audit date:** 14 May 2026

## Executive verdict

The manuscript is now strong enough to circulate as a **comprehensive foundation manuscript / technical discussion draft**. It is not yet ready for direct journal submission without a small set of publication-facing decisions and metadata additions.

The main manuscript no longer reads like an internal development log. The theory is coherent, the theorem spine is visible, the operational sections are substantially filled in, the diagrams are materially improved, and the document compiles cleanly. The remaining blockers are not conceptual; they are publication-packaging, bibliographic precision, length strategy, author metadata, and independent review.

## Corrections made in v0.43

This audit found several bibliography metadata issues in recent arXiv/publisher entries. I corrected the BibTeX file and recompiled the manuscript.

Corrected entries include:

- `mou2024socialsimulation`: author names corrected to match the arXiv record.
- `piao2025agentsociety`: author names and primary class corrected to match the arXiv record.
- `gao2024llmabm`: author list corrected to match the journal record.
- `xu2025amem`: author names and primary class corrected to match the arXiv record.
- `li2026notpanacea`: title corrected to the current arXiv title.
- `zhang2025socioverse`: author spelling and primary class corrected.

## Technical checks completed

| Check | Result |
|---|---|
| PDF compilation | Passed |
| BibTeX processing | Passed |
| Missing citation keys | None found |
| Unused bibliography keys | None found |
| Unresolved cross-references | None found in final compile pass |
| Obvious draft markers | None found |
| PDF preflight | Openable, not encrypted, not scanned |
| Page count | 246 pages |

Searched draft/development markers included: `TODO`, `TBD`, `placeholder`, `to come`, `next step`, `working paper`, `publication strategy`, `minimum publishable`, `future version`, `this version`, and `draft`. None appeared in the v0.43 source.

## Remaining publication blockers

### 1. Author metadata is missing

The source currently has an empty author field:

```latex
\author{}
```

Before publication, the manuscript needs:

- author name(s),
- institutional affiliation(s),
- email or corresponding-author line,
- ORCID if available,
- contribution statement if multiple authors.

This is the clearest hard blocker.

### 2. Publication target is not selected

The manuscript is 246 pages. That is appropriate for a technical monograph, arXiv foundation paper, or long-form technical report, but it is too long for most journal articles.

A publication path must be chosen:

1. **Comprehensive preprint / technical report**: publish the full foundation manuscript, likely on arXiv/SSRN/OSF.
2. **Journal article**: extract a 25-40 page core article and move technical material into appendices or a companion report.
3. **Book-length monograph / extended white paper**: retain full length but adjust tone and formatting accordingly.

The current document is closest to option 1.

### 3. The paper needs a final title-page package

Depending on venue, add:

- short title,
- author affiliations,
- correspondence line,
- acknowledgements,
- funding statement,
- competing interests statement,
- data availability statement,
- code availability statement,
- ethics statement,
- AI assistance statement if desired or required.

### 4. The claims should remain explicitly theoretical

The current manuscript is strongest as a formal theory. It should not imply empirical validation beyond the included simulation and validation framework.

The safest publication framing is:

> This article introduces and formalizes Dot-Trace Theory. It provides theoretical results, operational definitions, simulator specifications, and validation protocols. External empirical validation remains a separate research stage.

### 5. Proofs need independent mathematical review

The theorem spine is coherent, but before formal publication the proofs should be checked by at least one mathematically trained reader. The highest-priority proof checks are:

- representational insufficiency,
- dot-field Markov restoration,
- consensus/fragmentation,
- temporal non-commutativity,
- mixed-mechanism dynamics,
- recursive feedback stability.

### 6. Figures are acceptable but should be reviewed in final output format

The diagrams now compile and are much clearer than earlier versions. Because the manuscript is figure-heavy, final review should still inspect all figures in the exact format that will be submitted. The remaining concern is not correctness but visual density: some figures are information-rich and may be easier to read if split in a shorter article version.

### 7. Bibliography should receive one last strict verification pass

The most visible recent bibliography issues have been corrected in v0.43. However, before publication, all references should be verified for:

- exact title,
- exact author order,
- venue status,
- DOI/arXiv number,
- publication year,
- preprint versus peer-reviewed status.

This is especially important for 2025-2026 arXiv papers and rapidly evolving LLM-agent literature.

### 8. Code and reproducibility package should be stabilized

The paper references simulator and validation logic. Before publication, decide whether to publish:

- simulator source code,
- validation runners,
- example output logs,
- reproduction instructions,
- environment requirements,
- a repository DOI or archive link.

If the code is not published, the manuscript should say that code is available upon request or that implementation details are provided as specification rather than executable artifact.

## Missing items before publication

The manuscript should not be submitted externally until the following are resolved:

1. author/affiliation metadata,
2. target publication route,
3. final front-matter statements,
4. final bibliography verification,
5. independent proof review,
6. code/data availability decision,
7. final PDF figure inspection,
8. final copy-edit for venue style.

## Recommended path forward

### For immediate circulation

The manuscript can be circulated privately to trusted readers as a comprehensive theory manuscript after adding author metadata.

### For public preprint

Add author metadata, acknowledgements, data/code availability, and a short note clarifying that the work is a theory paper with simulation specifications rather than external empirical validation. Then publish the full manuscript as a technical preprint.

### For journal submission

Extract a shorter core article. Suggested core:

1. Introduction and related work.
2. Ontology and dot field.
3. State hierarchy and reduced-state insufficiency.
4. Markov restoration.
5. Consensus/fragmentation or topology-feedback stability.
6. Measurement and validation sketch.
7. Discussion and limitations.

Keep the current full manuscript as the technical companion.

## Readiness conclusion

The current v0.43 manuscript is **content-substantive and internally coherent**, but it is **not yet publication-complete** because author metadata, target venue, final front-matter statements, final bibliography verification, and independent proof review are still missing.

The strongest next action is to add publication metadata and create a concise publication package: manuscript PDF, LaTeX source, bibliography, code artifacts, and a one-page cover note summarizing the contribution and theoretical status.
