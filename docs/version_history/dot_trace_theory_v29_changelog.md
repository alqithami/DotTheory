# Dot-Trace Theory v0.29 Changelog

## Revision focus

Version 0.29 is a theorem-priority and proof-polish pass. It does not add another mechanism family. Instead, it clarifies the proof architecture so the manuscript reads as a coherent formal theory rather than a long list of independent results.

## Main changes

1. Added a new subsection: **Primary theorem spine and supporting results**.

2. Added **Table: Primary theorem spine of Dot-Trace Theory**, organizing the central proof path into six spine results:
   - S1: Representational insufficiency.
   - S2: Dot-field Markov restoration.
   - S3: Dot consensus and fragmented dot memory.
   - S4: Temporal sequencing and non-commutativity.
   - S5: Well-defined mixed dot-field dynamics.
   - S6: Recursive topology-feedback stability.

3. Added a new **Primary theorem spine figure**, showing the cumulative proof path and how mechanism, measurement, implementation, and validation results support the spine.

4. Added a **Proof-priority convention** distinguishing the role of theorems, propositions, corollaries, and lemmas.

5. Added missing labels to major theorem environments, including:
   - well-defined mixed dot-field dynamics,
   - recursive feedback contraction,
   - local recursive feedback stability,
   - representational insufficiency,
   - dot-field Markov restoration,
   - simulator faithfulness.

6. Revised the **Theoretical Results** introduction so the section is presented as a hierarchy rather than a flat list of claims.

7. Updated the **Article Structure** paragraph so the theorem-consolidation and theorem-spine sections are part of the reader-facing flow.

8. Removed remaining development-stage wording from the main text, including phrases such as "later versions" and "next step".

9. Normalized one remaining retrieval notation instance from `R_i(q,t)` to `\mathcal V_i(q,t)` in the topology-feedback loop.

10. Compiled successfully under pdfLaTeX and rendered representative pages for inspection.

## Result

The paper now has a more defensible formal architecture: a small primary theorem spine carries the central argument, while the broader theorem family is explicitly framed as supporting mechanism, measurement, implementation, and validation structure.
