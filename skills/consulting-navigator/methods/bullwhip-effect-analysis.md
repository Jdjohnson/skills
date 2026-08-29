# Bullwhip Effect Analysis
## Purpose
Diagnose how order variability amplifies upstream and prescribe levers to dampen the bullwhip. It distinguishes a real change in consumption from volatility created by replenishment rules, promotions, and information delays.
## Use
- Demand variability grows as you move upstream from customer to supplier
- Inventory and capacity oscillate despite relatively stable end demand
- You need root causes of order amplification before changing forecast or inventory policy
## Avoid
- You only need a baseline statistical forecast with no amplification diagnosis—use demand-planning-and-forecasting
- The problem is purely local warehouse safety-stock sizing—use inventory-optimization
- You need enterprise plan governance across functions—use sales-and-operations-planning or integrated-business-planning
## Inputs
**Must-have:**

- Time series of end demand, orders, and shipments by echelon
- Lead times, lot sizes, and ordering policies at each tier
- Promotion, allocation, and shortage-gaming history
- Information-sharing and visibility practices across partners

**Nice-to-have:** inventory positions, fill rates, forecast revisions, order cut-off calendars, and customer stockout records.

**When data is thin:** align the few comparable weekly series available, identify the missing echelons, and treat any causal conclusion as a hypothesis to test with transaction extracts.
## Procedure
1. **Set the chain and clock.** Choose a product family, the nodes from sell-through to supplier release, and a common weekly or daily interval. Exclude exceptional launches unless they are the case under investigation. Output: a chain map and reconciled analysis window.
2. **Align demand with replenishment signals.** Build parallel series for customer consumption, each node's outbound shipment, and each node's order to its supplier. Correct unit-of-measure changes and mark stockout-censored demand. Output: a tiered signal table.
3. **Calculate amplification.** For every upstream link, compare order variance with the variance of downstream demand over the same horizon; inspect order-to-demand ratios, batch sizes, and lagged correlations. Output: an amplification profile by echelon.
4. **Trace the mechanism.** Review the weeks driving peaks against price promotions, minimum-order multiples, forecast updates, allocation announcements, and lead-time changes. Test whether a spike was consumption-led or policy-led. Output: a cause-and-effect timeline.
5. **Design dampening experiments.** Match each proven driver to a lever: smaller order increments, shorter review cycles, stable pricing, allocation based on sell-through, or shared point-of-sale data. Specify the owner and a measurable reduction target. Output: prioritized stabilization actions.
## Output Contract
A diagnosis contains the echelon map, aligned demand and order series, variance ratios at each link, a timeline of the events explaining material spikes, and a ranked list of damping actions. It states which level is the first amplifier and separates a demand forecast issue from a replenishment-policy issue.
## Evidence
Use shipped or point-of-sale quantities as observed consumption only after noting lost sales and returns. Treat orders as intent, not demand. Record assumed lead times, aggregation rules, and any imputed weeks. Do not compare variance across different time buckets, product substitutions, or unadjusted seasonal periods. If partner data are withheld, show the break in the chain rather than inventing the upstream ratio.
## Checks
- Every ratio compares like units, dates, and product scope.
- The first volatile tier is identified before recommending a remedy.
- Event evidence supports each named mechanism, not merely a correlation.
- Stockouts and allocation periods are visibly flagged in the series.
- Proposed levers change ordering behavior, not just the forecast presentation.
## Failure Modes
- Calling a seasonal demand peak bullwhip without comparing consumer sales.
- Using monthly demand against weekly orders and manufacturing volatility by aggregation.
- Blaming suppliers when retailer batch rules created the initial pulse.
- Averaging away the few promotion weeks that actually explain the variance.
- Recommending lower safety stock before removing the order signal distortion.
