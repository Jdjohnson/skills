# Scalability Assessment
## Purpose
Diagnose whether the operating model can absorb planned volume growth without breaking quality, cost, or delivery. It tests the full growth path across people, process, systems, suppliers, and economics rather than measuring headroom in one process alone.
## Use
- Testing whether people, process, systems, and unit economics can support planned volume
- Identifying constraints that would break before a funding or expansion push
- Building a readiness roadmap from current capacity to target scale
## Avoid
- You need a pure throughput bottleneck fix without growth strategy—use bottleneck-analysis or theory-of-constraints
- The question is market size, not internal capacity—use market-sizing
- You only want peer performance gaps without scale scenarios—use operational-benchmarking
## Inputs
**Must-have:** Target volume, revenue, or customer growth path and timeline; current capacity, utilization, and constraint map for critical processes; unit economics at current and stressed volume levels; systems, org design, and supplier limits that bind under load; service-level and risk tolerances that must hold at scale.

**Nice-to-have:** hiring lead times, technology load-test results, facility options, financing limits, and credible demand scenarios.

**When data is thin:** use bounded growth scenarios and clearly separate measured capacity from management estimates; prioritize tests for constraints that could stop service.
## Procedure
1. **Specify growth cases.** Translate the plan into monthly demand, transaction, customer, and staffing loads for base, expected, and stretch cases. Define the service, quality, cash, and risk thresholds that cannot be breached.
2. **Map the scaling chain.** Trace each case through demand intake, fulfillment, support, systems, suppliers, management layers, and cash conversion. Identify dependencies that scale in steps rather than smoothly.
3. **Stress each constraint.** Calculate utilization, queueing or response effects, hiring ramp, system limits, vendor lead times, and unit-cost behavior at each growth point. Test failure propagation: a delayed hire may also reduce training quality and service.
4. **Locate breakpoints and options.** Mark the volume or date where each capability crosses its tolerance. Compare capacity adds, automation, standardization, outsourcing, policy change, and demand throttling by cost, lead time, reversibility, and new risk.
5. **Build the readiness roadmap.** Sequence actions ahead of their breakpoint, assign early-warning measures, funding decisions, and contingency triggers. Distinguish no-regret preparation from investments conditional on demand.
## Output Contract
Issue a growth-readiness assessment with scenarios, capability-by-capability breakpoints, severity-ranked constraints, economics at each scale point, and a timed constraint-removal roadmap. It must make clear what volume can be absorbed now, what investment unlocks the next threshold, and what trigger pauses expansion.
## Evidence
Use observed throughput, defect, latency, turnover, supplier, and cost data where possible. Model future demand, learning curves, utilization targets, and automation yield as assumptions with ranges. Do not extrapolate a linear cost or service curve through a step-change such as a new shift, warehouse, manager layer, or platform limit. Highlight unknown dependency capacity before calling a plan scalable.
## Checks
- Every scenario uses the same volume and time basis across functions.
- Breakpoints cite an explicit tolerance, not an undefined sense of strain.
- The assessment covers demand, operations, technology, people, and economics.
- Roadmap actions occur before their dependency lead time expires.
- Contingencies identify both an owner and a measurable trigger.
## Failure Modes
- Declaring spare production hours sufficient while support and onboarding queues fail first.
- Applying today's unit cost to a volume that requires a new facility or management layer.
- Assuming a cloud service scales automatically without testing downstream integrations.
- Treating a vendor's nominal capacity as committed capacity during peak demand.
- Funding every possible upgrade instead of tying investments to demand gates.
