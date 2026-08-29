# Activity-Based Costing
## Purpose
Trace resource costs through activities to products, customers, or channels so true cost-to-serve is visible. It replaces broad volume allocations with rates based on the work that each cost object actually consumes.
## Use
- Traditional volume-based overhead allocations distort product or customer profitability
- You need defensible unit costs for pricing, mix, or make-vs-buy decisions
- Shared resources support heterogeneous products, channels, or customers
## Avoid
- You already have credible activity costs and need to manage them operationally—use activity-based-management
- The goal is enterprise cost-cut design rather than cost measurement—use cost-optimization-framework or zero-based-budgeting
- Simple direct-cost products with negligible overhead make ABC overkill—use financial-ratio-analysis or price-volume-mix-analysis
## Inputs
**Must-have:** General ledger costs and cost-center structure; list of major activities and resource drivers; activity volumes and product/customer consumption measures; defined cost objects (products, services, customers, or channels).

**Nice-to-have:** Time-study observations, process maps, capacity data, and a prior-period allocation for reconciliation.

**When data is thin:** Build rates for the few pools that explain most indirect cost, retain a separately reported residual pool, and label estimates as provisional.
## Procedure
1. **Set the cost-object boundary.** Decide whether a SKU, order, customer, or channel is being costed, specify the period, and exclude costs outside the decision. This prevents a product analysis from silently becoming a customer P&L.
2. **Trace resources into activity pools.** Reclassify indirect ledger accounts into work such as setups, purchasing, testing, packing, engineering changes, and order handling. Reconcile the pool total to the selected ledger cost before proceeding.
3. **Choose a causal driver for every pool.** Use setup count for setup labor, test hours for quality work, purchase orders for buying, and picks for warehouse handling. Reject a driver chosen only because it is easily available.
4. **Calculate pool rates.** Divide each pool’s practical-period cost by its driver volume. Separate unused capacity when possible; charging it to a low-volume product obscures the operating decision.
5. **Apply consumption to cost objects.** Multiply each object’s measured driver use by each pool rate, add direct material and labor, then calculate unit or account cost. Trace exceptions such as special engineering requests explicitly.
6. **Reconcile and explain variance.** Tie assigned plus unassigned cost to the ledger, compare the resulting costs with the legacy method, and identify the drivers causing material movement.
## Output Contract
Deliver a cost map showing scope, activity mapping, drivers, pool rates, consumption, direct cost, indirect cost, and fully loaded unit cost. Include a ledger reconciliation and explanation of material shifts. The output supports a pricing, mix, or service decision; it is not an operational savings plan.
## Evidence
Treat ledger balances, payroll records, and transaction counts as observed. Treat resource splits and driver relationships as inferences supported by interviews or time studies. Record the numerator, denominator, period, and owner for every rate. If an activity has no reliable volume measure, keep its allocation visible as an assumption rather than spreading it evenly across all objects.
## Checks
- Activity-pool cost plus separately reported residual cost reconciles to the in-scope ledger total.
- Each material pool has one stated causal driver and a nonzero denominator.
- Direct costs are not also embedded in an overhead pool.
- Rates use a consistent period and units.
- The conclusion changes only where the consumption evidence supports it.
## Failure Modes
- Treating revenue, headcount, or unit volume as a universal driver for work caused by orders or complexity.
- Hiding idle capacity inside product rates and then blaming low-volume products for a plant utilization problem.
- Creating dozens of tiny pools whose measurement cost exceeds the decision value.
- Assigning a customer’s expedite work to all customers because request-level records are missing.
