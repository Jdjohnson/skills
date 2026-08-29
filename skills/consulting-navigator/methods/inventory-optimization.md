# Inventory Optimization
## Purpose
Set differentiated inventory policies that balance service levels against holding, ordering, and shortage costs. It turns demand uncertainty, replenishment time, and economics into SKU or segment rules instead of one buffer for every item.
## Use
- Setting reorder points, safety stocks, and order quantities to hit service at minimum cost
- Reducing excess and obsolete inventory without wrecking fill rate
- Differentiating inventory policy by segment (volume, variability, criticality)
## Avoid
- Demand signal quality is the root problem—fix demand-planning-and-forecasting first
- You need multi-echelon amplification diagnosis—use bullwhip-effect-analysis
- The fix is pure flow and waste removal on the warehouse floor—use lean-logistics or just-in-time
## Inputs
**Must-have:** SKU-level demand history, variability, and service targets; Lead times, costs (holding, ordering, stockout), and constraints; Current inventory positions, policies, and ABC or similar segmentation; Network nodes where inventory is held.

**Nice-to-have:** Supplier reliability, minimum-order quantities, shelf life, substitution rules, and planned promotions.

**When data is thin:** Use a conservative service band and a visible proxy for variability; test it on a limited item set before changing replenishment parameters broadly.
## Procedure
1. **Clean and segment the item population.** Remove discontinued items, stockouts that censor demand, and exceptional orders. Segment by value, demand pattern, criticality, and supply risk because a spare part and a fast-moving consumer SKU need different policies.
2. **Measure replenishment exposure.** Calculate average demand and variability over the lead-time window, then inspect actual lead-time variation rather than relying on contract lead time alone.
3. **Choose the service measure.** Set cycle-service probability or fill-rate target by segment, with explicit cost of a miss. Do not assign an identical 99% target to every item.
4. **Calculate policy parameters.** Derive safety stock from lead-time demand uncertainty; set reorder point as expected lead-time demand plus safety stock. For suitable stable items, compare economic order quantity with minimum-order and capacity constraints.
5. **Simulate and challenge.** Replay recent demand or stress the policy with promotion and lead-time shocks. Compare proposed stock, fill rate, stockouts, and carrying cost against the current rule.
6. **Deploy and govern.** Load approved parameters, define override rights, and review exceptions such as new items, end-of-life stock, and supplier disruption monthly.
## Output Contract
A segmented inventory policy table that states each item group’s service target, safety-stock logic, reorder point, order quantity or review cadence, owner, and exception rule. Include the expected service and working-capital change, plus a list of parameters that require master-data correction.
## Evidence
Demand history and on-hand records are observed, but promotional uplift and lost sales are often inferred. State the demand window, outlier treatment, and service definition. Keep supplier lead-time promises separate from measured receipt performance. For intermittent demand, avoid applying normal-distribution formulas without checking the pattern; use an appropriate discrete or review policy instead.
## Checks
- Parameter units match the replenishment unit and review frequency.
- Lead time includes release, transit, receiving, and usable-stock delay.
- Proposed buffers are tested against item-specific variability, not average portfolio variability.
- Policy changes show both service and carrying-cost effects.
- Obsolete or end-of-life items are excluded from automatic replenishment.
## Failure Modes
- Reducing all safety stock by the same percentage to meet a cash target.
- Calling an ABC label a policy without changing service or replenishment rules.
- Using average demand for highly erratic or intermittent items.
- Ignoring minimum order quantities that make a calculated order quantity impossible.
