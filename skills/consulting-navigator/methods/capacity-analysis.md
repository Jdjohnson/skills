# Capacity Analysis
## Purpose
Measure and forecast resource load versus available capacity to expose gaps, excess, and utilization risk. It translates demand and work content into required hours at each constrained resource, rather than assuming that nominal staffing equals usable output.
## Use
- Quantifying available capacity versus required load by resource or line
- Deciding whether to hire, add shifts, outsource, or defer demand
- Supporting S&OP, capital, or make-vs-buy choices with utilization facts
## Avoid
- You need the single flow constraint and protection policy—use bottleneck-analysis then theory-of-constraints
- Demand itself is the uncertain variable without a forecast process—use demand-planning-and-forecasting first
- The problem is process waste and long lead time, not resource hours—use value-stream-mapping
## Inputs
**Must-have:**

- Resource list with available hours (shifts, OEE, downtime assumptions)
- Demand or load by product/service over the planning horizon
- Routing or work content (standard times) by resource
- Current utilization, overtime, and backlog data

**Nice-to-have:** skill matrices, maintenance schedules, yield assumptions, outsourcing lead times, and planned new equipment.

**When data is thin:** calculate a conservative range using observed output and clearly separate demonstrated capacity from nameplate capacity.
## Procedure
1. **Choose the planning grain.** Set the horizon and buckets, then identify resources at the level where capacity can actually be changed: machine, crew, skill, room, or supplier lane. Output: resource and calendar model.
2. **Calculate available effective capacity.** Start with scheduled hours, then remove planned downtime, breaks, maintenance, absenteeism, changeovers, and realistic efficiency losses. Distinguish design capacity from attainable capacity. Output: effective hours by resource and period.
3. **Convert demand to load.** Multiply the demand mix by routing time or service effort at every resource, adjusting for yield, scrap, rework, and product mix. Output: required hours by resource and period.
4. **Compare load, capacity, and buffers.** Calculate utilization, gap or excess hours, backlog trajectory, and overtime requirement. Highlight where an annual average conceals a weekly overload. Output: load-versus-capacity heat map.
5. **Evaluate response actions.** Quantify the effect and lead time of overtime, cross-training, shift changes, maintenance improvement, outsourcing, demand shaping, or capital. Output: capacity action plan tied to the constrained periods.
## Output Contract
Provide a resource-by-period load-versus-effective-capacity table, utilization and backlog view, stated operating assumptions, and a ranked set of remedies. It must identify when and where the gap occurs, the hours involved, and the operational action needed; an enterprise-wide percent utilization alone is insufficient.
## Evidence
Use time-clock records, production logs, routings, maintenance history, and actual output as observed data. Mark forecast demand, standard-time adjustments, and future efficiency gains as assumptions. Do not treat 100 percent utilization as sustainable capacity: queues and variability require operating headroom. When routings are uncertain, test high-volume products first and show the resulting error band.
## Checks
- Resource calendars account for planned losses and skill constraints.
- Demand mix is loaded through every relevant routing step.
- Units, yields, and standard times reconcile to the chosen period.
- Peak-period gaps are shown separately from average utilization.
- Each recommendation states hours released or added and its availability date.
## Failure Modes
- Calling three scheduled shifts available when maintenance consumes one shift each week.
- Averaging a December overload with spare capacity in January.
- Loading only final assembly and missing the skilled-test constraint.
- Counting overtime twice: once as capacity and again as a cost-saving action.
- Funding equipment without confirming operators, floor space, or upstream material capacity.
