# FMEA
## Purpose
Identify failure modes for a product or process, score severity-occurrence-detection, and prioritize preventive and detection controls. The worksheet makes prospective risk visible before a release, design change, or process handoff exposes customers to it.
## Use
- Systematically identifying how a product or process can fail and ranking residual risk.
- Prioritizing design, process, and detection controls before release or change.
- Supporting DFSS, launch readiness, or change control with a living risk worksheet.
## Avoid
- A failure already occurred and you need causal explanation—use root-cause-analysis.
- You need enterprise risk portfolios or board-level ERM—use enterprise-risk-management or coso-erm-framework.
- The need is continuous defect reduction on a running process without design focus—use six-sigma or statistical-process-control.
## Inputs
**Must-have:** Defined product function or process steps in scope; cross-functional knowledge of design/process failure history; severity, occurrence, and detection rating scales agreed in advance; current prevention and detection controls for each step or function.

**Useful additions:** warranty data, customer complaints, test plans, drawings, control plans, and supplier process information.

**Boundary:** name the revision, intended user, operating conditions, and interfaces. A worksheet for an unspecified design cannot be approved.
## Procedure
1. Form a cross-functional team and freeze the analysis boundary. For a process FMEA, walk the actual sequence; for a design FMEA, list the functions and interfaces the design must perform.
2. For each function or step, write a specific failure mode, its local and end-user effects, and credible causes. Keep “operator error” as a prompt to find a mechanism, not as a cause.
3. Rate severity from the worst reasonably foreseeable effect, independent of whether current controls catch it. Use the team’s agreed scale and record rationale for high scores.
4. List current prevention controls and detection controls separately. Estimate occurrence from cause frequency and detection from the likelihood that the control finds the mode before release or customer use.
5. Calculate the agreed priority measure, such as RPN = severity × occurrence × detection, or apply the organization’s action-priority table. Rank modes, while escalating any high-severity item even if its calculated score is modest.
6. Assign a preventive design or process action and, where needed, a detection action, owner, due date, and verification test. After evidence of implementation, re-rate the relevant scores and retain the before-and-after record.
## Output Contract
Produce a controlled FMEA table with function or step, failure mode, effects, causes, current controls, S/O/D ratings with rationale, priority, actions, owners, dates, and post-action ratings. It must distinguish prevention from detection and show whether the residual condition is acceptable. The artifact guides control-plan and design decisions; it is not a generic risk list.
## Evidence
Use field data, test evidence, process capability, and supplier records as observed evidence. Team estimates of frequency or detectability are inferred judgments and need rationale. Rating-scale definitions and assumed operating misuse are assumptions. Unknown failure mechanisms remain explicit open risks; do not assign a low occurrence score merely because the team has no history.
## Checks
- Each row ties to a real function, interface, or process step.
- Effects are written at the customer, safety, regulatory, or downstream level.
- Severity is unchanged by adding an inspection; only occurrence or detection may change.
- Actions remove or control a cause, rather than restating “train operators.”
- Re-ranking occurs only after completion is verified by test, audit, or data.
## Failure Modes
- Letting a single engineer score a cross-functional interface without manufacturing or service input.
- Reducing severity after installing a sensor, which confuses harm with discoverability.
- Closing an action because a procedure exists without proving the procedure prevents the cause.
- Using equal scores for every row, leaving the team with a false priority order.
