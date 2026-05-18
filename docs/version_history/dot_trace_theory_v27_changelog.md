# Dot-Trace Theory Working Paper v0.27 Changelog

Version 0.27 is an appendix-architecture, figure-improvement, and simulator-calibration pass. It builds on v0.26 by making the long foundation paper easier to navigate and by introducing calibration discipline for the simulator and validation layers.

## Major additions

1. Added visual anchors using TikZ diagrams:
   - canonical state hierarchy and projection loss;
   - integrated mixed-mechanism dot-field transition;
   - recursive topology-access-memory feedback loop;
   - simulator calibration workflow.

2. Added a new section: **Simulator Calibration and Parameter Governance**.
   - Defines calibration objective and loss.
   - Distinguishes calibration tiers C0-C3.
   - Adds a parameter governance table.
   - Adds calibration diagnostics for access density, retrieval depth, mutation rate, institutionalization rate, and stability margin.
   - Adds a simulator calibration non-identifiability proposition.
   - Adds a calibration-report schema.

3. Added a new section: **Manuscript Architecture, Figures, and Appendix Plan**.
   - Defines main-text versus appendix placement rules.
   - Proposes an appendix architecture for a later technical report.
   - States a figure plan for the foundation manuscript.
   - Adds a navigation principle for future revisions.

4. Added **Technical Appendix Architecture** to the appendix.
   - Records the intended migration rule: core claim in main text, technical burden in appendix.

5. Updated the Metrics section with simulator calibration metrics:
   - calibration loss;
   - parameter sensitivity index;
   - calibration overfit gap;
   - calibration tier.

6. Added hypotheses H52-H54:
   - calibration tier constrains claim strength;
   - calibration overfit gap predicts poor external validation;
   - appendix navigation improves theorem usability.

7. Added Simulation 20:
   - simulator calibration and appendix-ready reporting.

8. Updated the Research Roadmap.
   - Marks figure plan, appendix architecture, and simulator calibration protocol as in place.
   - Sets the next foundation task as proof polishing and appendix migration.

## Compilation and QA

- Compiled successfully under pdfLaTeX.
- Rendered representative pages including the title page, table of contents, new figures, simulator calibration section, manuscript architecture section, appendix architecture, and version note.
- Final compiled PDF length: 246 pages.
