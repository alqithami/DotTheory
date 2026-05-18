# Dot-Trace Theory v0.21 - Editorial Coherence and Flow Pass

## Purpose
Version 0.21 is a full editorial consolidation pass focused on academic coherence, flow, terminology consistency, and professional presentation. It does not begin the empirical study. It keeps the project in foundation-stabilization mode.

## Major editorial changes

1. Rewrote the abstract into a tighter journal-style abstract with clearer problem, object, state representation, formal results, scope limits, and contribution.
2. Rewrote the introduction for smoother academic flow: adjacent literatures, motivating trace examples, dot definition, central intuition, novelty boundary, and article structure.
3. Standardized language across the draft, including consistent use of US English forms such as `modeling` and `research program`.
4. Cleaned all multi-line section and subsection titles so the table of contents reads professionally.
5. Added a new `Notation and State Hierarchy` section to clarify the relationship between:
   - the reduced agent-edge state,
   - the core dot field,
   - the augmented dot field,
   - the executable implementation state.
6. Added projection and information-loss notation to clarify when dot-field variables add transition-relevant information.
7. Separated dot-dot relation notation from retrieval notation:
   - dot-dot relations: `R_t^D`,
   - retrieved dot sets/sequences: `\mathcal V_i(q,t)`.
8. Rewrote the dot-centroid and social-capital section to clarify that a dot is not a centroid by definition, but may become centroid-like in the lifted heterogeneous graph.
9. Strengthened the dot-mediated social-capital treatment with a cleaner decomposition and a more coherent proof statement.
10. Added smoother transition paragraphs to major sections, including the dot concept, ontology, dot field, axioms, formal dynamics, theoretical results, algorithmic implementation, and validation protocol.
11. Updated the roadmap so it no longer says the next task is the notation/state hierarchy audit; that work is now marked as substantially satisfied in v0.21.
12. Updated the immediate next action to focus on the measurement and extraction protocol, with theorem-notation harmonization as a parallel task.
13. Updated the minimal formal package to align with the canonical notation introduced in v0.21.
14. Rewrote the conclusion for a more professional final synthesis.
15. Added an editorial consolidation note in the appendix.

## Build and verification

- Compiled successfully with `latexmk -pdf`.
- Rendered representative pages from the generated PDF for layout inspection.
- Verified that the PDF has 189 pages and no encryption or form restrictions.
- Confirmed that legacy `v0.19` references and British spelling variants targeted for standardization were removed.
