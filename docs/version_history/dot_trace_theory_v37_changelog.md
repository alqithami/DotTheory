# Dot-Trace Theory v0.37 Changelog

## Focus
This revision addresses late-stage coherence, glossary/reference layout, diagram legibility, and underdeveloped later sections.

## Main changes

1. **Glossary/reference ordering fixed**
   - Moved all glossary terminology before the bibliography.
   - Removed the previous issue where several glossary entries appeared after the references.
   - Expanded the glossary into a more complete appendix with definitions for access graph, accessible dot set, archival social capital, compressed dot, dot-centroid, dot-field projection, effective retrievable strength, institutional dot, lineage, memory barycenter, semantic brokerage capital, and trace-mediated path dependence.

2. **Diagram repair and enrichment**
   - Rebuilt the major TikZ diagrams to reduce text overlap and improve visual clarity.
   - Reworked figures for conceptual overview, literature positioning, state hierarchy, dot lifecycle, integrated dynamics, recursive feedback, theorem spine, implementation architecture, simulator loop, calibration governance, calibration workflow, dot-extraction workflow, validation stack, metrics dashboard, benchmark suite, application map, differentiation, and governance.
   - Removed crossing arrows from the implementation architecture figure and replaced them with a clearer conceptual feedback note.

3. **Later-section maturation**
   - Expanded short or outline-like subsections in the implementation, simulator, calibration, measurement, validation, applications, governance, and boundary-condition sections.
   - Added fuller prose to sections on stores and indexes, validation-to-theorem mapping, parameter governance, calibration reports, measurement stance, unit of observation, attribute schema, dot relations, observability ladder, baseline hierarchy, minimal evidence standard, validation decision rules, applications, semantic governance, proportionality, scalability, and external validation.

4. **Reference update**
   - Added recent 2026 references on LLM-agent memory evolution and limitations of AI-agent-based social simulation.
   - Updated the related-work discussion so those references support the paper's claims about memory mechanisms, calibration, scheduling, and boundary-aware simulation.

5. **Proofreading and consistency**
   - Scanned for draft-stage phrases such as TODO, TBD, placeholder, next step, minimum publishable, publication strategy, working paper, and formal article. No such development-stage markers remain in the LaTeX source.
   - Recompiled with pdfLaTeX and BibTeX8.

## Output
- Source: `dot_trace_theory_overleaf_v37.tex`
- Bibliography: `dot_trace_theory_references_v37.bib`
- PDF: `dot_trace_theory_overleaf_v37.pdf`
- Rendered key-page contact sheet: `dtt_v37_key_contact_sheet.png`

## Current assessment
The manuscript is now more coherent as a long-form theory manuscript. The remaining high-value work is a reader-flow and length-management pass: deciding whether the 239-page foundation document should remain as one technical manuscript or eventually be split into a shorter core article plus a technical companion.
