# Marketing Mix Modeling
## Purpose
Quantify incremental sales and ROI of marketing investments by statistically decomposing channel, price, promo, and base demand effects.
## Use
- You have multi-period spend and sales data across channels and need incremental contribution estimates
- Budget reallocation decisions require statistically defensible channel ROI
- You must separate base demand, seasonality, pricing, and competitive effects from paid media impact
## Avoid
- You lack sufficient history or channel-level spend variation—use a-b-testing or pilot-and-scale-methodology first
- You need causal proof for one creative or landing page change—use a-b-testing
- You are pricing a single SKU for launch—use price-elasticity-analysis or price-sensitivity-meter
## Inputs
**Must-have:**
- Multi-period sales or demand series at consistent grain
- Channel-level marketing spend and activity history
- Price, promotion, distribution, and seasonality controls
- Competitor activity or macro indicators when material

**Nice-to-have:** impressions or reach, creative flight dates, geographic variation, stockout records, brand tracking, margin, experiment results, and media-plan constraints.

**When data is thin:** reduce the channel detail, extend the history, or run controlled tests. A coefficient estimated from spend that barely moves cannot support a reallocation decision.
## Procedure
1. **Define the outcome and grain.** Select sales, orders, or margin; choose weekly or monthly geography-product units that align with media and controls. Output: modeling specification.
2. **Prepare the time series.** Reconcile sales, spend, price, promotions, distribution, holidays, stockouts, and external shocks; treat missing or changed measurement periods explicitly. Output: modeling dataset.
3. **Encode media response.** Transform each channel for carryover and saturation, using plausible lag and diminishing-return structures rather than assuming each dollar acts immediately. Output: response variables.
4. **Estimate and validate models.** Fit candidate models, assess signs, stability, residual patterns, holdout accuracy, and business plausibility; compare alternatives rather than accepting one convenient fit. Output: validated model set.
5. **Turn response into decisions.** Estimate incremental contribution, marginal ROI, and response curves under feasible budget constraints; propose an allocation and its expected range. Output: budget scenario plan.
## Output Contract
Provide a model pack containing the outcome definition, time coverage, data quality notes, channel transformations, control variables, validation results, base-versus-incremental decomposition, contribution and ROI by channel, response curves, and constrained budget scenarios. The recommendation must state the spending level at which each channel approaches saturation and the uncertainty around reallocating funds.
## Evidence
Treat reconciled sales, recorded media, price, and promotion data as observed after documenting corrections. Treat lag length, saturation shape, missing competitor activity, and attribution of correlated channels as assumptions or limitations. Preserve known supply constraints so lost sales are not assigned to media. Use holdout periods, geography, or experiments to challenge coefficients where possible. Do not describe correlation as conclusive causation when variation is weak.
## Checks
- Sales and media series share a documented calendar, geography, and product scope.
- Important price, promotion, distribution, and seasonality effects are modeled or explicitly excluded.
- Channel response has plausible lag and diminishing returns where the business expects them.
- Results are checked on withheld time periods, not just in-sample fit.
- Allocation scenarios respect minimum commitments, capacity, and channel availability.
## Failure Modes
- Crediting television with seasonal demand because both rise in the same quarter.
- Combining brand and performance media into one variable that cannot inform a budget choice.
- Ignoring promotion pull-forward and calling temporary volume incremental demand.
- Reporting average ROI while reallocating at the margin where response is different.
- Treating an unstable coefficient as a precise instruction to cut a channel.
