# Dot-Trace Theory Working Paper v0.22 Changelog

## Focus of this revision

Version 0.22 adds a substantive measurement and dot-extraction protocol. The purpose is to make Dot-Trace Theory operational before empirical launch: what counts as a dot, how dots are coded, how access/provenance/credibility are measured, how uncertainty is represented, and when a dot-field claim is too strong for the available data.

## Main manuscript additions

1. Added a new section: **Measurement and Dot-Extraction Protocol**.
2. Distinguished observed dots, inferred dots, and latent dots.
3. Defined the unit of observation and the extraction function from trace-bearing units to candidate dots.
4. Added a formal **minimum dot test** requiring content, persistence, provenance, access, and action relevance.
5. Added exclusion and boundary rules for transient stimuli, pure social edges, outcome-only pseudo-dots, unassigned aggregate attributes, duplicate surface forms, and inaccessible artifacts.
6. Added a staged coding workflow: segmentation, dot testing, type assignment, content/target extraction, provenance coding, access coding, relation coding, strength estimation, audit/adjudication, and rule freezing.
7. Added task-relative dot identity and canonicalization rules for token identity, lineage identity, and semantic identity.
8. Added a recommended dot attribute schema with fields for content, type, time, provenance, target, context, access, salience, credibility, valence, normative force, lifecycle state, relations, lineage, institutional anchoring, and uncertainty.
9. Separated access, attention, and retrieval as distinct measured quantities.
10. Added provenance and credibility coding guidance.
11. Added a typed dot-relation inventory covering support, contradiction, citation, summarization, mutation, targeting, institutionalization, and repair.
12. Added target, valence, and normative-force coding rules.
13. Added empirical guidance for estimating memory weight and effective retrievable strength.
14. Added reliability and auditability requirements, including dot-detection F1, relation-extraction F1, mean absolute disagreement for continuous labels, and an audit tuple.
15. Added an observability ladder from O0 to O5, ranging from action-only data to randomized exposure or instrumented agent memory.
16. Added a definition of measurement-admissible dot datasets.
17. Added a proposition showing prediction stability under bounded extraction error.
18. Added a measurement-threats taxonomy and a protocol-deliverables checklist before empirical launch.

## Metrics, hypotheses, and simulation additions

Added extraction/coding quality metrics:

- Dot detection F1 (`F1_D`)
- Relation extraction F1 (`F1_R`)
- Attribute completeness score (`ACS`)
- Access uncertainty mass (`AUM`)
- Outcome-blind coding rate (`OBR`)
- Observability grade (`O`)

Added hypotheses:

- H41: Extraction reliability moderates dot-field prediction lift.
- H42: Access observability separates trace existence from trace influence.
- H43: Outcome-blind extraction reduces overfitting.
- H44: Semantic identity thresholds affect fragmentation and correction estimates.

Added **Simulation 17: Measurement-error and extraction-quality stress test**, which evaluates how dot deletion, false extraction, access noise, provenance loss, relation loss, semantic over-merging, semantic over-splitting, and outcome-aware extraction affect prediction lift and mechanism recovery.

## Roadmap updates

The roadmap now treats measurement as a completed foundation section rather than only a future task. The next foundation task is theorem consolidation against the canonical state hierarchy and measurement protocol: each theorem should state its state level, observability requirements, measurement grade, validation signature, and failure condition.

## Compilation and verification

The v0.22 LaTeX source compiles successfully under pdfLaTeX. Key pages were rendered and visually inspected, including the new measurement protocol, measurement metrics, Simulation 17, roadmap, and final reference page.
