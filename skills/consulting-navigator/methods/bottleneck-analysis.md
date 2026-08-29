# Bottleneck Analysis
## Purpose
Identify and quantify the process step that limits end-to-end throughput so improvement effort targets the true constraint. It follows flow and queues to identify the resource that sets the pace, not the station with the loudest local problem.
## Use
- Diagnosing the single constraint that limits system throughput.
- Prioritizing improvement spend where it will raise overall flow.
- Explaining persistent queues, WIP buildup, or missed delivery despite spare capacity elsewhere.
## Avoid
- You need full system redesign of policies, buffers, and subordination rules—use theory-of-constraints.
- The issue is demand uncertainty or S&OP planning, not a process constraint—use sales-and-operations-planning or demand-planning-and-forecasting.
- You only need nameplate load-versus-hours math without flow diagnosis—use capacity-analysis.
## Inputs
**Must-have:** Process map or value stream with sequential steps; throughput, cycle time, or queue data by step over a representative period; WIP and utilization observations at each major station; demand rate or takt the system must meet.

**Nice-to-have:** downtime reasons, rework paths, shift schedules, changeover history, and customer-priority rules.

**When data is thin:** time a representative sample at the worksite and distinguish observed queues from assumptions; do not infer a bottleneck from utilization alone.
## Procedure
1. **Set the flow boundary.** Choose one product or service family, start/end points, and demand window; separate it from unrelated routing.
2. **Measure effective capacity.** For each step calculate available time less changeover, downtime, and quality loss, then compare capacity with required rate.
3. **Trace WIP and starvation.** Observe where work accumulates before a step and where downstream steps wait; note rework that secretly consumes capacity.
4. **Identify the binding constraint.** Select the step whose effective capacity or instability actually caps completed units over the representative period.
5. **Quantify the leverage.** Estimate incremental system throughput from one additional constraint hour or from removing its dominant loss; avoid crediting improvements elsewhere.
6. **Recommend focused actions.** Protect the constraint from avoidable downtime, move nonessential work away, improve quality before it, and reassess after the flow changes.
## Output Contract
A bottleneck diagnosis containing the scoped flow, step-level demand and effective-capacity table, queue/WIP evidence, constraint location, loss breakdown, throughput impact estimate, and a ranked intervention list. It must state what evidence would show that the constraint has moved.
## Evidence
Use timestamp, machine, staffing, and queue observations as observed evidence. Mark missing downtime categories, product-mix estimates, and demand forecasts as assumptions. Measure a full enough period to include shifts and normal variability. A high-utilization station without upstream WIP may be busy but not system-constraining.
## Checks
- Capacity is based on effective available time, not nameplate speed.
- The selected constraint explains both the output cap and the observed queue pattern.
- Rework and changeovers are assigned to the station that consumes them.
- Improvement impact is calculated on finished throughput, not local pieces processed.
- A re-measurement date is set because the bottleneck can migrate.
## Failure Modes
- Buying equipment for the visibly slowest step while work actually waits elsewhere.
- Raising upstream output and enlarging WIP ahead of an unchanged constraint.
- Treating average cycle time as capacity despite frequent breakdowns or setups.
- Improving a downstream station that is mostly starved by the true constraint.
- Declaring victory after local utilization falls without checking customer throughput.
