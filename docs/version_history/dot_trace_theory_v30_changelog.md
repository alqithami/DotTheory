# Dot-Trace Theory v0.30 Changelog

## Focus

Version 0.30 performs a proof-compression and theorem-polish pass. The goal is to make the formal section easier to read without weakening the theorem spine or removing the supporting mechanism results.

## Main changes

1. Renamed the theorem section from **Theoretical Results** to **Main Theoretical Results** to clarify its role in the article.

2. Added a concise proof-spine reading guide before the first theorem subsection. The guide frames the six primary spine results as the formal backbone of the theory:
   - S1: representational insufficiency,
   - S2: dot-field Markov restoration,
   - S3: consensus and fragmentation,
   - S4: temporal sequencing,
   - S5: mixed-mechanism dynamics,
   - S6: recursive topology-feedback stability.

3. Updated the proof-priority convention so direct corollaries are not re-proved when they follow immediately by specialization, projection, monotonicity, or a direct application of the preceding result.

4. Removed repetitive proof blocks for direct corollaries in the main theorem section. The proof material is now concentrated around core theorems, technical lemmas, and propositions requiring explicit verification.

5. Preserved the proof of the **Dot-sufficient compression** corollary because it remains close to the core representation claim.

6. Fixed a notation issue in the Markov-restoration section: the prior draft reused \(C_t\) as both an encoding map and correction state. The full state encoding map is now written as \(\Xi_t\), while \(C_t\) remains reserved for correction state.

7. Compressed the proof of the screening-off lemma so that it states the kernel-composition argument directly rather than repeating each transition component in prose.

8. Updated the opening paragraph of the main theorem section to explain that direct corollaries are recorded as consequences rather than separately re-proved.

## Compilation

The document was compiled successfully with pdfLaTeX. The compiled PDF has 225 pages.
