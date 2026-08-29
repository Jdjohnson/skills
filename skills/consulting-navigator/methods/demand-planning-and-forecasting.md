# Demand Planning & Forecasting
## Purpose
Produce a governed, accuracy-managed demand forecast that operations and commercial teams can plan against. It creates one unconstrained demand signal by blending statistical history with controlled commercial judgment and learning from error.
## Use
- Building or resetting unconstrained demand forecasts for planning horizons
- Feeding a single demand signal into S&OP, capacity, or inventory decisions
- Improving forecast process, metrics, and consensus between sales and supply
## Avoid
- You need full financial and strategic reconciliation across functions—use integrated-business-planning
- The core issue is order amplification across echelons—use bullwhip-effect-analysis first
- You only need stock-level math with demand already trusted—use inventory-optimization
## Inputs
**Must-have:** Historical shipments, orders, and sell-out or POS where available; Known demand drivers (price, promo, seasonality, pipeline, events); Product hierarchy and planning time buckets; Forecast accuracy history and current process roles.

**Nice-to-have:** Lost-sales estimates, competitor activity, customer inventory, causal-model features, new-product analogs, and supply constraints kept separate from demand.

**When data is thin:** Forecast at the highest stable hierarchy level, use a documented analog for new products, and expose a confidence range rather than forcing SKU-month detail.
## Procedure
1. **Define the planning grain and demand truth.** Set SKU, location, customer, and week or month levels; specify whether history is orders, shipments, or consumption. Remove supply-constrained shipments from the demand baseline where possible.
2. **Clean and segment history.** Correct one-off events, stockouts, product substitutions, returns, and hierarchy changes. Identify stable, seasonal, intermittent, and new items because they require different baseline methods.
3. **Generate a statistical baseline.** Select and back-test appropriate time-series or causal models at each segment. Produce an unconstrained baseline before sales overrides are considered.
4. **Apply controlled demand sensing.** Require commercial owners to enter promotion, price, customer, or event adjustments with a rationale, volume delta, date range, and confidence. Reconcile disputed changes in a documented consensus meeting.
5. **Publish and learn.** Freeze the approved forecast for the planning cycle, pass it to S&OP or inventory users, and track bias, WAPE or comparable error, override accuracy, and forecast-value-add by horizon and segment.
## Output Contract
A versioned unconstrained demand plan containing historical-data treatment, forecast grain, baseline method, commercial overrides, consensus decisions, final volumes, confidence range, owner, freeze date, and error measures. It shows the difference between baseline and judgment so users can distinguish a demand signal from a supply-constrained production plan.
## Evidence
Mark POS, orders, and confirmed promotions as observed; classify inferred lost demand and event uplift as assumptions. Keep a change log for every manual override and never overwrite the original baseline. When product history is short, state the analog basis and when it will be replaced by actual performance.
## Checks
- Forecast units, calendar, hierarchy, and actuals definition match the consuming plan.
- Stockouts and exceptional orders are treated consistently in the history.
- Baselines are back-tested against a holdout period before overrides are praised.
- Overrides carry owners and are evaluated separately for bias and accuracy.
- Error is segmented by forecast horizon and volatility, not hidden in one enterprise average.
## Failure Modes
- Treating constrained shipments as unconstrained customer demand.
- Allowing sales overrides with no date, rationale, or later accuracy review.
- Averaging seasonal and intermittent items into a single forecasting method.
- Declaring accuracy improved when favorable product mix masks persistent bias.
