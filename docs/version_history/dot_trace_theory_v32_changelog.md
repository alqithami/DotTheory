# Dot-Trace Theory v0.32 Changelog

## Revision focus
Reference-format and citation-style pass.

## Main changes

1. Converted the manual reference list into a BibTeX-based bibliography.
2. Added a standalone `dot_trace_theory_references.bib` file for Overleaf use.
3. Added `natbib` author-year citation support.
4. Replaced manually typed in-text citations in the Related Work and Positioning section with citation commands such as `\citet{...}` and `\citep{...}`.
5. Replaced the hand-written References section with:

   ```latex
   \bibliographystyle{plainnat}
   \bibliography{dot_trace_theory_references}
   ```

6. Normalized reference entries into a consistent BibTeX format across books, articles, conference papers, arXiv preprints, and web sources.
7. Corrected the LLM social simulation boundary citation year to 2025 to match arXiv:2506.19806.
8. Preserved the existing manuscript structure, theorem spine, figures, algorithms, and core formal content.
9. Compiled the manuscript with pdfLaTeX + BibTeX and verified that there were no unresolved citations or missing references.

## Files

- `dot_trace_theory_overleaf_v32.tex`
- `dot_trace_theory_references.bib`
- `dot_trace_theory_overleaf_v32.pdf`
- `dot_trace_theory_v32_changelog.md`
- `dot_trace_theory_overleaf_v32_bundle.zip`
