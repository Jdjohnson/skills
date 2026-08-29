# Poka-Yoke
## Purpose
Design process, fixture, or sequence mechanisms that prevent human errors from becoming defects—or detect them at the source before they escape. It redesigns a known error opportunity, rather than documenting the preferred work method or merely ranking potential failures.
## Use
- Defects are driven by predictable human error and you can redesign the process or device to make the error impossible or immediately obvious
- Inspection and training alone have not reduced recurring mistakes
- You want prevention or detection at the source rather than downstream scrap/rework
## Avoid
- Root cause is still unknown process physics or multi-factor variation—use root-cause-analysis or fmea first
- You need statistical process control of continuous variables rather than discrete error prevention—use statistical-process-control
- The real issue is an unclear or unstable standard—use standard-work before error-proofing gadgets
## Inputs
**Must-have:** Defined defect mode and the exact human action that enables it; process step map and current standard work at the failure point; constraints on cost, cycle time, and tool/fixture changes; severity and frequency of the defect (to size prevention vs warning devices); operator feedback on practicality of candidate devices or sequence changes.

**Nice-to-have:** defect photographs, task video, maintenance history, capability data, and supplier design constraints.

**When data is thin:** observe several shifts first; do not build a device around an assumed error sequence or an anecdote from quality inspection.
## Procedure
1. **Describe the error chain.** Define the defect, the exact action or omission that creates it, when it occurs, and how it currently escapes. Output: error-point map.
2. **Verify the failure condition.** Observe the task at normal and stressed pace; test whether part geometry, information, sequence, or attention creates the opportunity. Output: confirmed error mechanism.
3. **Generate prevention and detection concepts.** Consider contact, count, orientation, interlock, scan, and alarm mechanisms. Prefer constraints over warnings that depend on attention. Output: candidate designs.
4. **Select against operating constraints.** Compare effectiveness, cycle time, maintainability, bypass risk, ergonomic impact, and cost with operators and engineering. Output: selected design specification.
5. **Trial and validate at the source.** Run normal variation and deliberate error challenges; document response when the mechanism triggers. Output: validation record and revised work instruction.
6. **Control and maintain.** Assign ownership for checking device condition, alarms, overrides, and recurrence metrics. Output: control plan.
## Output Contract
An error-proofed step design with the targeted defect, causal action, selected prevention or detection mechanism, interface or fixture specification, validation test, operator instructions, maintenance checks, and override policy. It must identify where the error is stopped and what happens when the device cannot make a decision.
## Evidence
Treat direct observations, defect counts, and challenge-test results as observed. Label predicted error reduction, ergonomic effects, and rare-event frequency as estimates. State assumptions about operators, product variants, lighting, wear, and software connectivity. A passed bench test is not evidence of production robustness; record conditions and failed tests. If bypassing is possible, measure it explicitly rather than assuming compliance.
## Checks
- The mechanism targets one specified error action and occurs before downstream escape.
- A wrong orientation, count, or sequence is tested deliberately, not only inferred.
- Operators can perform the task safely at required takt time.
- Bypass, sensor failure, and maintenance response are designed and owned.
- The new control is reflected in standard work and defect monitoring.
## Failure Modes
- Adding a warning light when a fixture could physically prevent misassembly.
- Error-proofing the symptom after the defect has already been shipped internally.
- Designing a sensor for ideal parts that false-alarms on normal variation.
- Creating a cumbersome device operators learn to bypass during peak volume.
- Assuming retraining is the corrective action for a recurring design-induced mistake.
