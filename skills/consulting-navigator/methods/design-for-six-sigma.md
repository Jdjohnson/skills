# Design for Six Sigma
## Purpose
Design products and processes so customer CTQs and Six Sigma capability are built in before production, not fixed after launch. It converts measurable customer needs into a robust design that tolerates ordinary manufacturing and use variation.
## Use
- Designing or redesigning products/processes so they meet Six Sigma capability from day one
- Translating customer CTQs into robust design parameters before launch
- Preventing chronic field failures that continuous improvement cannot fix cheaply
## Avoid
- An existing stable process needs defect reduction—use six-sigma (DMAIC)
- You need early customer desirability exploration, not statistical design rigor—use design-thinking or design-sprints
- The issue is production control of an already capable design—use statistical-process-control
## Inputs
**Must-have:** Voice of customer or CTQ requirements with measurable targets; Concept or baseline design and process options under consideration; Historical failure, capability, or warranty data if redesigning; Tolerance, cost, and timeline constraints for the design.

**Nice-to-have:** usage-environment data, supplier capability studies, and physical or digital prototypes.

**When data is thin:** state provisional CTQ limits and run a small experiment on the parameter most likely to change the concept choice.
## Procedure
1. **Define:** turn customer language into measurable CTQs, set design scope, and make a requirements flow-down. Specify the defect definition and target capability before choosing a solution.
2. **Measure:** collect benchmark, warranty, and prototype data; translate CTQs into engineering responses and quantify the current noise factors. Establish measurement-system adequacy for any test metric.
3. **Analyze:** generate concepts, identify critical parameters, and use tolerance analysis, failure analysis, or simulation to locate combinations that miss CTQs. Select a concept against capability, cost, and manufacturability.
4. **Design:** optimize parameter settings and tolerances with designed experiments or robust-design techniques. Build control features and mistake-proofing into the product and its production process.
5. **Verify:** pilot the design under representative conditions, calculate predicted versus observed capability, and close requirements traceability. Release only with a control and handoff plan.
## Output Contract
A design package containing a CTQ-to-specification trace, selected concept, critical-parameter settings, tolerance stack-up, predicted capability, residual risks, and verification results. It must identify which customer requirements are protected against which noise factors, plus the owner and acceptance criterion for each remaining design verification.
## Evidence
Mark customer research, test readings, and field returns as observed. Treat translated engineering targets and model predictions as inferred; record the equation, model version, and validation range. Label assumed distributions for material, user behavior, or process variation. An untested operating condition remains unknown, even if simulation is favorable; it requires a verification test or an explicit release limitation.
## Checks
- Every critical requirement has a measurable limit, unit, and verification method.
- The selected concept beats alternatives on the CTQs rather than merely on cost.
- Capability calculations use a stated variation source and an adequate measurement system.
- Tolerances are feasible for named suppliers and processes.
- The verification plan exercises worst-case noise, not only nominal prototypes.
## Failure Modes
- Freezing dimensions before the CTQ hierarchy is agreed, then discovering that reliability was never designed for.
- Optimizing a nominal prototype while temperature, wear, or supplier variation drives field defects.
- Treating a QFD matrix as proof that parameter capability has been demonstrated.
