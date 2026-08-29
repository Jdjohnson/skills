# Statistical Process Control
## Purpose
Monitor process stability and capability over time with control charts so teams act on special-cause signals and leave common-cause systems alone. It establishes a continuing reaction system rather than a one-off improvement project.
## Use
- Monitoring process stability and capability with control charts and reaction plans.
- Distinguishing common-cause variation from special-cause signals that need investigation.
- Sustaining gains after improvement projects with ongoing statistical guardrails.
## Avoid
- There is no standard method or measurement system yet—use standard-work and measurement system checks first.
- You need a full project to find and permanently remove chronic defect drivers—use six-sigma.
- The issue is a one-time incident investigation, not ongoing process monitoring—use root-cause-analysis.
## Inputs
**Must-have:** Defined critical process or product characteristic to chart; reliable measurement method and sampling/subgroup plan; historical or baseline data sufficient to set provisional control limits; documented reaction plan for out-of-control signals; process owners and operators who will update and act on the charts.

**Useful additions:** specification limits, changeover records, operator and material identifiers, and a data-capture system that preserves timestamp order.
## Procedure
1. Select the characteristic and chart family that fit its data: an individuals chart for single continuous readings, X-bar and R for rational subgroups, p or np for defective units, and c or u for counts of defects.
2. Verify that readings represent the same operational definition and that subgrouping captures short-term process conditions rather than conveniently sized batches.
3. Freeze a baseline period with no known exceptional events. Calculate the center line and statistical control limits from that baseline; keep specification limits visually and analytically separate.
4. Plot readings in time order and apply stated signal rules, such as a point outside a limit, a sustained run on one side of center, or a persistent trend.
5. When a signal occurs, contain affected output if necessary, record the assignable condition, investigate before adjustment, and document the disposition. When no signal occurs, do not tamper with settings because of ordinary noise.
6. After a deliberate process change is proven, establish a new baseline and assess capability against customer specifications separately from stability.
## Output Contract
Provide a live chart set with characteristic definition, chart type, subgroup rule, baseline dates, center line, limits, current signals, and an operator reaction plan. Include a capability view only where the process is stable and specification limits are defensible. The package must tell a shift what to do at a signal, not merely display historical variation.
## Evidence
Use timestamped measurements and calibration records as observed evidence. Flag backfilled readings, mixed product families, and changed inspection methods. Treat a provisional baseline as conditional when a known change or small sample may distort limits. Never label a point defective solely because it breaches a control limit, nor label a stable process capable without comparing it to specifications. Keep causes separate from signals until an investigation establishes the link.
## Checks
- Chart choice matches the data type, sample structure, and opportunity count.
- Subgroups are rational and consistently collected.
- Limits come from process variation, not customer tolerances.
- Reaction ownership and hold/release authority are explicit for every signal.
- Capability indices are not reported for an unstable process.
## Failure Modes
- Recalculating limits after every alarming point, thereby normalizing a real shift.
- Mixing two machines or product variants on one chart and mistaking the mixture for instability.
- Adjusting a stable filling line after each low reading and increasing its variation through tampering.
- Treating a red point as a root cause rather than a prompt to investigate a specific time window.
