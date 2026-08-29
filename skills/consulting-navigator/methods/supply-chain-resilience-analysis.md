# Supply Chain Resilience Analysis
## Purpose
Diagnose the supply network's ability to absorb shocks and recover service, then prioritize resilience gaps and interventions. It tests disruption pathways through the network instead of maintaining a generic risk list.
## Use
- Diagnosing how quickly the supply network can absorb and recover from shocks.
- Identifying critical nodes, single points of failure, and recovery bottlenecks.
- Prioritizing resilience investments such as dual sourcing, buffers, or network redesign.
## Avoid
- You need ongoing supplier risk scoring and mitigation governance without network recovery focus—use supply-chain-risk-management.
- The need is enterprise process continuity plans rather than supply-network diagnosis—use business-continuity-planning.
- The problem is purely inventory policy optimization under normal demand—use inventory-optimization.
## Inputs
**Must-have:** End-to-end supply network map (suppliers, plants, DCs, lanes, critical SKUs); lead times, capacities, inventory positions, and alternate sources; historical disruption events and recovery timelines; service-level and revenue-at-risk priorities for key products and customers.

**Useful additions:** tier-two supplier visibility, port and border dependencies, qualification lead times, contractual rights, and disruption probability estimates.
## Procedure
1. Build a bill-of-network for priority products from upstream sources through plants, distribution centers, lanes, and customers. Link nodes to capacities, inventory, and product dependencies rather than mapping legal entities alone.
2. Define disruption scenarios that are plausible and decision-relevant, such as a supplier outage, plant fire, lane closure, cyber interruption, or demand spike. State duration and affected nodes for each scenario.
3. Stress the network scenario by scenario. Calculate time to survive from accessible inventory and time to recover from alternate supply, rerouting, qualification, capacity expansion, or restart. Follow consequences to affected customers and revenue.
4. Locate single points of failure and recovery bottlenecks. Test whether apparent alternates share a hidden common dependency, lack qualified tooling, or cannot meet required volume.
5. Compare interventions by service protected, recovery-time reduction, cost, implementation lead time, and residual exposure. Options may include dual source qualification, strategic buffer relocation, flexible capacity, alternative lanes, or product redesign.
6. Prioritize a funded resilience portfolio and assign trigger conditions, owner, and review cadence. Retest the network after a material supplier, product, or footprint change.
## Output Contract
Deliver a disruption-tested network map, scenario workbook, critical-node register, time-to-survive and time-to-recover measures, and ranked intervention portfolio. Each intervention specifies affected flow, scenario coverage, expected service protection, cost, lead time, owner, and remaining exposure. The assessment must make recovery mechanics visible, not merely assign a risk score to each supplier.
## Evidence
Use inventory, capacity, lead-time, and shipment data at the product-location level where possible. Separate verified alternate capacity from a supplier’s untested assurance. State assumptions about demand prioritization, usable inventory, regulatory qualification, and concurrent disruptions. Historical recovery time informs scenarios but does not prove future performance under a larger event. Show unknown tier dependencies rather than treating them as zero risk.
## Checks
- Network paths connect critical SKUs to customers through every material node and lane.
- Scenarios specify duration, scope, and recovery actions, not only a hazard label.
- Time-to-survive and time-to-recover use consistent service assumptions.
- Alternate sources are checked for common-mode dependencies and qualification time.
- Priorities compare resilience benefit with cost and implementation feasibility.
## Failure Modes
- Calling a second supplier resilient when both buy the same constrained subcomponent.
- Counting inventory in a distant DC as usable despite customs, allocation rules, or incompatible packaging.
- Measuring only time to recover production while ignoring the lane or customer allocation that delays service restoration.
- Funding buffers everywhere instead of protecting the few nodes that determine network survival.
