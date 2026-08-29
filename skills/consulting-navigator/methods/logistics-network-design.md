# Logistics Network Design
## Purpose
Design the optimal number, location, and capacity of facilities and flows to meet service targets at minimum total landed cost.
## Use
- Redesigning plant, DC, or cross-dock footprint for cost and service
- Evaluating greenfield entry or major demand shift impacts on the network
- Comparing multi-echelon facility and flow options before capex commitment
## Avoid
- The issue is day-to-day warehouse execution software—use wms-strategy
- You only need carrier or last-mile routing, not facility location—use last-mile-delivery-optimization
- Demand and capacity baselines are unknown; run demand-planning-and-forecasting and capacity-analysis first
## Inputs
**Must-have:**
- Demand by SKU/region/time bucket and service-level targets
- Current facilities with capacity, fixed cost, and handling cost
- Lane costs, lead times, and transport mode constraints
- Inventory policy assumptions and product flow rules
- Candidate locations or expansion/closure constraints

**Nice-to-have:** tax and incentive data, labor availability, disruption history, lease break costs, carbon limits, and a clean customer-to-zip-code demand map.

**When data is thin:** aggregate demand into defensible regions and test alternate allocations. State when a candidate site is a proxy rather than pretending the model has address-level precision.
## Procedure
1. **Define service and cost rules.** Set promised delivery windows, capacity constraints, product compatibility, sourcing rules, and the landed-cost components to optimize. Output: model design brief.
2. **Create the baseline network.** Map current demand to shipping nodes and lanes, reconcile volume and cost totals, and calculate service attainment, utilization, and inventory by echelon. Output: calibrated current-state model.
3. **Generate feasible footprints.** Create alternatives that open, close, expand, consolidate, or repurpose facilities; include allowed flows and capacity limits for each. Output: scenario set.
4. **Optimize flows and inventory.** Allocate demand through the feasible nodes while minimizing fixed, handling, transport, and inventory carrying cost subject to service constraints. Output: cost-service results by scenario.
5. **Select and phase the design.** Compare resilience, transition cost, labor, customer disruption, and implementation lead time; sequence leases, inventory moves, carrier changes, and cutovers. Output: chosen network map and migration plan.
## Output Contract
Deliver a target network map with facilities, capacities, customer service regions, lane flows, and inventory positions. For every alternative, show total landed cost, service attainment, capital or exit costs, key constraints, and sensitivity to demand or fuel changes. The recommendation must make explicit which nodes close, open, or change role and the timing needed to move safely.
## Evidence
Reconcile shipment history, facility cost, and demand totals before optimization. Classify quoted lane rates and leases as observed; classify future demand, labor availability, and candidate-site cost as assumptions. Preserve exclusions such as hazardous-product rules and customer-specific service commitments. Test a demand shift, a facility outage, and transport-rate inflation when they could reverse the preferred footprint.
## Checks
- Baseline volumes and costs reconcile to finance and operations records.
- Every capacity is stated in the same operational unit and time period.
- The model honors delivery promises instead of purchasing savings through missed service.
- Fixed exit, start-up, and inventory-transfer costs appear in the business case.
- A logistics operator can trace a region’s flow from source to destination.
## Failure Modes
- Optimizing transportation cost alone and creating excessive safety stock or missed delivery windows.
- Using annual averages that hide seasonal capacity peaks.
- Treating an existing warehouse as free because its lease cost is sunk for only part of the horizon.
- Allowing infeasible product mixing, dock capacity, or customs flows in the solver.
- Recommending a perfect end state with no credible inventory or customer cutover path.
