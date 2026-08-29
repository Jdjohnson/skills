# Customer Lifetime Value Analysis
## Purpose
Forecast the economic value of a customer relationship over its expected life to guide acquisition, retention, and service investment. It converts retention, margin, and time assumptions into a comparable forward value rather than treating first-purchase revenue as value.
## Use
- Estimating discounted future profit or revenue per customer or cohort
- Setting acquisition ceilings, retention investment, and service tiers by value
- Comparing channels, products, or segments on long-run economics
## Avoid
- You need why customers leave, not what they are worth—use churn-analysis
- You need transaction-level cost-to-serve profitability now—use customer-profitability-analysis
- Data is only one-period revenue with no retention or margin structure—build those inputs first
## Inputs
**Must-have:** Customer-level or cohort revenue and gross margin history; Retention/churn rates and expected tenure assumptions; Acquisition cost by channel or segment; Discount rate and time horizon for the forecast.

**Nice-to-have:** Expansion revenue, servicing costs, return rates, survival curves, and channel attribution rules.

**When data is thin:** Use cohort-level value with a short horizon and a sensitivity range; do not manufacture individual-level precision from sparse history.
## Procedure
1. **Define the economic unit.** Choose customer, account, household, or acquisition cohort; set the clock origin, value metric, horizon, and whether value is gross margin or contribution after service cost.
2. **Construct retention curves.** Calculate period survival by cohort and segment, correcting for immature cohorts. Identify contractual renewal versus behavioral repeat-purchase patterns rather than applying one global churn rate.
3. **Estimate margin streams.** Project expected revenue, gross margin, expansion, and material variable service costs conditional on survival for each period.
4. **Discount and aggregate.** Calculate expected present value as the sum of period margin multiplied by survival probability and discounted to acquisition. Keep acquisition cost separate until comparing unit economics.
5. **Tier and stress-test.** Compare value, CAC, payback, and confidence by segment or channel. Recalculate under retention, margin, and discount-rate sensitivities; recommend only actions that survive plausible downside cases.
## Output Contract
A documented value model with unit definition, cohort or segment retention curves, projected margin streams, discount convention, CAC treatment, value tiers, payback view, and sensitivity table. The output states whether it represents revenue, gross margin, or contribution and identifies segments where investment economics are negative. It is a forward model, not a current customer P&L.
## Evidence
Treat booked revenue, margin, and observed retention as facts for their closed periods. Mark forecasts of renewal, expansion, future costs, and discount rates as assumptions. Exclude incomplete cohorts from mature-rate claims or adjust explicitly. If data cannot separate acquisition channels, disclose the attribution limitation instead of assigning value to the last click.
## Checks
- Cohorts use a consistent acquisition date and retention denominator.
- Margin and acquisition cost definitions align with the decision being made.
- Discounting begins at the correct period and is not applied twice.
- Base, downside, and upside cases change the drivers that are genuinely uncertain.
- Tier boundaries lead to a different acquisition, retention, or service action.
## Failure Modes
- Multiplying average order value by a guessed lifetime without a retention curve.
- Calling revenue CLV while using the result to set a profit-based CAC cap.
- Comparing a mature organic cohort with an immature paid cohort as if horizons match.
- Hiding high service costs inside a supposedly margin-based value figure.
