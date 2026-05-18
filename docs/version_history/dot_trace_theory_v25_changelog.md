# Dot-Trace Theory Working Paper v0.25 Changelog

## Revision focus

Version 0.25 adds a substantive foundation module on **recursive topology-feedback stability**. The goal of this revision is to strengthen the dynamic theory after v0.24's integrated mixed-mechanism transition. The new material analyzes the loop in which social edges shape dot access, access shapes retrieval, retrieval creates edge pressure, and edge pressure changes social edges.

## Main additions

1. **New section: Recursive Topology-Feedback Stability**
   - Defines the feedback subsystem using edge vectors, soft access vectors, retrieval features, and edge-pressure vectors.
   - Introduces the reduced recursive edge map
     \[
     e_{t+1}=\Theta(e_t).
     \]
   - Clarifies that the fixed-background assumption is a phase assumption, not a claim that dots never change.

2. **Global contraction theorem**
   - Proves a sufficient contraction condition for the recursive edge-access-retrieval-pressure loop:
     \[
     L_E^e+L_E^zL_ZL_RL_B<1.
     \]
   - Shows that under a convex edge update, stability requires the full dot-mediated feedback product to remain below the amplification threshold.

3. **Local Jacobian stability theorem**
   - Defines the local feedback Jacobian
     \[
     J_\Theta=E_e+E_zZ_rR_bB_e.
     \]
   - States local stability when
     \[
     \rho(J_\Theta)<1.
     \]
   - Distinguishes direct edge inertia from the recursive dot-mediated feedback channel.

4. **Feedback sign regimes**
   - Adds reinforcing, balancing, and broken-feedback regimes.
   - Connects these regimes to bonding capital, bridging capital, correction, lock-in, alliance formation, and exclusion.

5. **Threshold access closure**
   - Proves that if an edge falls below an access threshold and the counter-dot is inaccessible, the relation can remain closed and converge below the threshold.
   - Formalizes a self-sealing distrust/exclusion mechanism.

6. **Finite-time bridge recovery**
   - Proves that if bridge, mediator, archive, or institutional correction raises the target above the access threshold, the edge crosses the threshold in finite time.
   - Connects bridge recovery to correction reach and topology-mediated social capital.

7. **New recursive stability diagnostics**
   - Adds recursive stability margin:
     \[
     SM(t)=1-\rho(J_\Theta(t)).
     \]
   - Adds access-closure risk:
     \[
     ACR_{ij}(t).
     \]
   - Adds bridge recovery margin:
     \[
     BRM_{ij}(t).
     \]
   - Adds shock amplification ratio:
     \[
     SAR(k).
     \]

8. **Theorem register update**
   - Adds recursive topology-feedback stability as a mechanism theorem with state scope in \(\Omega_t^{aug}\).
   - Adds A14 to the assumption register for recursive topology feedback.

9. **New hypotheses H48-H51**
   - H48: Recursive feedback stability follows the Jacobian margin.
   - H49: Threshold access closure predicts durable distrust and exclusion.
   - H50: Bridge recovery margin predicts repair speed.
   - H51: Recursive feedback diagnostics improve mechanism ablation.

10. **New Simulation 19**
   - Adds a recursive topology-feedback stability simulation design.
   - Tests spectral stability, threshold closure, bridge recovery, dominant-channel ablation, and shock amplification.

11. **Roadmap update**
   - Marks topology-feedback stability as substantially satisfied at the foundation level.
   - Updates the next foundation task to worked examples, simulator calibration, literature consolidation, and appendix organization.

## Compilation and QA

- Compiled successfully under pdfLaTeX.
- Output PDF length: 228 pages.
- Rendered representative pages including the title page, the new stability section, theorem register, metrics, hypotheses, simulation, roadmap, and version note for visual inspection.
