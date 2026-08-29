# Customer Profitability Analysis
## Purpose
Attribute revenues and fully loaded costs-to-serve to customers or segments so management can see who creates profit, who erodes it, and where service and pricing policies should change. The ranking exposes profit concentration and leaks to drive service-level, pricing, retention, and go-to-market decisions—on current-period economics, not lifetime value.
## Use
- Leadership suspects the largest accounts may be among the least profitable.
- Service, logistics, support, or customization costs explode for a few accounts without tracking.
- Sales chase volume while finance believes the firm is buying unprofitable revenue.
- The firm treats all customers the same on price and service despite different economics.
- Portfolio or go-to-market choices need true cost-to-serve, not revenue alone.
## Avoid
- You only need a period revenue/margin bridge, not customer attribution—use price-volume-mix-analysis.
- You lack any workable way to allocate service and overhead costs—start with activity-based-costing.
- The question is lifetime value under retention scenarios rather than current-period P&L—use customer-lifetime-value-analysis.
- Customer hierarchy and time window are undefined; fix those first.
## Inputs
**Must-have:** Revenue by customer or segment for the analysis period; direct product or service costs attributable to those customers; cost-to-serve drivers (orders, support tickets, deliveries, returns, customization) or ABC/TDABC allocations; a clear customer/segment hierarchy and time window.

**Nice-to-have:** Contract terms, service-level agreements, channel path, payment terms, and win/loss or churn flags.

**When data is thin:** Pilot one segment with explicit allocation rules; label views fully loaded vs contribution-only—never claim full cost from product cost alone.
## Procedure
1. **Define the customer hierarchy and window** — Choose account vs site vs segment grain and the period. Output: hierarchy and scope statement.
2. **Assemble revenue and direct product costs** — Map invoices and COGS (or equivalent) to each customer. Output: gross contribution by customer before cost-to-serve.
3. **Measure cost-to-serve** — Assign sales, marketing, distribution, support, and administrative costs to customers using activity-based drivers of customer behavior. Output: cost-to-serve by customer.
4. **Compute customer profit** — Product contribution less cost-to-serve per customer, with further layers if needed. Output: customer P&L table.
5. **Rank and visualize concentration** — Sort customers by profit into a cumulative whale curve showing how much profit the top tier creates and how much loss sits in the tail. Output: ranked list and concentration chart.
6. **Set actions by segment** — Group customers into manage-for-growth, reprice/restructure, reduce-service, or exit candidates with concrete levers. Output: prioritized action list by segment.
## Output Contract
A customer-level (or segment-level) profitability view that includes: (1) scope and hierarchy, (2) revenue, product cost, cost-to-serve, and profit by customer, (3) ranking and profit concentration, (4) transparent allocation rules, and (5) prioritized actions for pricing, service, and retention. The artifact must answer who funds the business and who drains it—not a period bridge or a multi-year lifetime-value model.
## Evidence
- **Observed:** invoices, shipments, tickets, and direct costs.
- **Inferred:** allocated cost-to-serve from drivers and rates.
- **Assumptions:** allocation keys and which costs are customer-caused—document them.
- **Unknowns:** where drivers are missing, show contribution-only and flag the gap; never present allocated profit as more precise than the costing system allows.
## Checks
- Revenue and direct costs reconcilable to the books for the period.
- Cost-to-serve uses causal drivers, not arbitrary equal splits, for material costs.
- Rankings hold up under allocation sensitivity tests.
- Actions differ by economics (not one-size-fits-all “improve service”).
- Large “unallocated” buckets are disclosed, not hidden.
## Failure Modes
- Ranking by revenue and calling it profitability.
- Ignoring cost-to-serve so high-touch accounts look healthy.
- Over-allocating fixed costs until every small customer looks unprofitable.
- Building a costing system with no decision use (framework theater).
- Confusing current-period profitability with lifetime value.
