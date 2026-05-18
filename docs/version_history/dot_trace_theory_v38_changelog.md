# Dot-Trace Theory v0.38 Changelog

## Focus of this revision

Version 0.38 performs a reader-flow and length-management pass after the late-section expansion and diagram repair work in v0.37. The goal was to make the long-form manuscript easier to navigate without moving material into appendices yet.

## Main changes

1. **Expanded article-structure guidance.**
   - Rewrote the article-structure subsection as a four-layer reading architecture: conceptual/formal vocabulary, process model, theorem spine, and operational/application layer.
   - Added explicit reading paths for theory readers, applied readers, computational readers, and validation-oriented readers.

2. **Added a reading-path table.**
   - New Table: `Reading paths through the long-form manuscript`.
   - The table clarifies what different readers should focus on and what each path establishes.

3. **Added a new synthesis section after the main theoretical results.**
   - New section: `Interpretive Synthesis of the Theoretical Spine`.
   - This section explains how representational insufficiency, Markov restoration, consensus/fragmentation, temporal sequencing, mixed dynamics, and recursive feedback stability fit together as one cumulative argument.

4. **Added a theorem-to-operation synthesis table.**
   - New table: `Interpretive summary of the theorem spine`.
   - It links theoretical layers to their operational burdens, making the transition from proofs to implementation and validation smoother.

5. **Rewrote Boundary Conditions and Extensions.**
   - Removed duplicated external-validation prose.
   - Reorganized the section into polished subsections on:
     - when dot fields are unnecessary,
     - measurement limits,
     - inactive or dominated mechanisms,
     - computational and design boundaries,
     - normative and governance boundaries,
     - extensions.

6. **Rewrote the conclusion.**
   - Strengthened the conclusion as a final synthesis of representational, dynamic, operational, and governance contributions.
   - Removed redundant wording and improved academic flow.

7. **Citation and draft-language checks.**
   - Confirmed no missing citation keys relative to the v0.38 bibliography.
   - Scanned for obvious development-stage markers such as TODO, TBD, placeholder, next step, minimum publishable, publication strategy, working paper, and formal article.

8. **Compile and visual verification.**
   - Compiled with pdfLaTeX and BibTeX8.
   - Rendered representative pages including the new reading-path table, synthesis section, boundary section, conclusion, glossary, and references.

## Output

- Compiled PDF length: 242 pages.
- Bibliography: `dot_trace_theory_references_v38.bib`.
