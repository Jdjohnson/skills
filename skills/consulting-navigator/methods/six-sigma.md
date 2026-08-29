# Six Sigma
## Purpose
Diagnose and reduce process variation and defects through a data-driven DMAIC project cycle with statistical proof of causes and gains.
## Use
- Reducing defects, variation, or cost of poor quality with data and hypothesis tests.
- Running structured DMAIC projects on stable-enough processes with measurable Y outcomes.
- Proving root causes and solution impact before scaling process changes.
## Avoid
- The main need is rapid waste and flow improvement without statistical rigor—use lean-manufacturing or value-stream-mapping.
- The product is still being designed and prevention beats after-the-fact control—use design-for-six-sigma.
- The process is undefined or chaotic with no baseline metrics—use sipoc-analysis and process-mapping first.
## Inputs
**Must-have:** Critical-to-quality outcomes and defect or variation definition; baseline process performance data with enough samples for analysis; process map or SIPOC of the in-scope process; access to subject-matter experts and operators for cause hypotheses; business case thresholds for improvement (cost, quality, cycle time).

**Nice-to-have:** Measurement-system studies, stratifiers such as shift and product, historical process limits, and a process owner able to sustain controls.

**When data is thin:** Confirm the measurement system and collect a planned baseline before testing causes. Do not substitute workshop votes for variation data.
## Procedure
1. **Define.** Charter a narrow defect problem, customer impact, financial goal, process boundary, sponsor, and team. Operationally define the Y so two inspectors count the same defect the same way.
2. **Measure.** Map the current process, build a data-collection plan, and check gauge repeatability and reproducibility where measurements are involved. Establish baseline yield, defect rate, cycle variation, DPMO, or capability as appropriate.
3. **Analyze.** Stratify Y by time, product, machine, operator, and other suspected X factors. Use plots, sampling logic, and suitable hypothesis tests or regression to distinguish a signal from random variation.
4. **Improve.** Generate changes directed at verified Xs, pilot them under controlled conditions, and compare results with the baseline. Include practical safeguards against moving the defect to another step.
5. **Control.** Document the new method, monitoring measure, control limits or response rule, ownership, and escalation trigger. Close only after the owner accepts the control plan and post-pilot result.
## Output Contract
Deliver a DMAIC project record with the CTQ and defect definition, scope, measurement plan and capability, baseline, verified causal factors, test results, improvement design, quantified benefit, and control plan. Statistical claims must state the population, sample period, and test or chart used. The record must establish why an intervention changed the critical outcome; it is not a generic improvement idea list or a one-time root-cause diagram.
## Evidence
Preserve raw data, exclusions, and operational definitions. Treat process-owner hypotheses as candidates, not causes. Report sample sizes and confidence or practical-effect measures where tests support a claim. If a factor cannot be randomized, explain the confounding risk. Never declare a capability change from a shifted specification, altered defect definition, or a short pilot run without noting it.
## Checks
- The Y links to a customer or business CTQ and has an unambiguous defect opportunity.
- Data collection agrees with the process map and measurement-system findings.
- Causal conclusions are supported by stratification, tests, or designed experimentation.
- Pilot results are compared with a comparable baseline.
- Control ownership, sampling cadence, and reaction plan are operationally specified.
## Failure Modes
- Calculating sigma level from an opportunity count that changes by shift.
- Testing a suspected X after pooling machines with fundamentally different settings.
- Improving the mean while the tail defect rate remains unacceptable.
- Installing a control chart without an operator response rule when a point signals.
