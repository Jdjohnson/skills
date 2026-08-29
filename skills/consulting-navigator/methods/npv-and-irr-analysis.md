# NPV and IRR Analysis
## Purpose
Rank capital investments by converting incremental cash flows into NPV and IRR against a hurdle rate. The analysis makes timing, cost of capital, and mutually exclusive choices explicit instead of comparing attractive-looking accounting returns.
## Use
- Ranking mutually exclusive or capital-constrained investment alternatives
- Screening projects against a cost-of-capital hurdle using NPV and IRR
- Comparing cash-timing profiles of growth, replacement, or cost-save initiatives
## Avoid
- Flexibility value and staged abandon/expand options dominate—use real-options-analysis
- You still lack a defensible discount rate—compute weighted-average-cost-of-capital first
- The choice is buy-vs-build strategic design rather than pure cash ranking—use buy-vs-build-analysis after NPV inputs exist
## Inputs
**Must-have:** Incremental free-cash-flow forecast by period for each option; discount rate or WACC and reinvestment assumptions; initial outlay, terminal value or salvage, and tax/depreciation treatment; capital constraint or mutual exclusivity rules if ranking a portfolio.

**Nice-to-have:** working-capital profile, downside case, funding schedule, inflation convention, and treatment of shared costs and cannibalization.

**When data is thin:** build a range for the few cash-flow drivers that matter most, state the unknowns, and defer an irreversible decision rather than hiding gaps in a single base case.
## Procedure
1. **Set the investment boundary.** Define the decision, do-nothing alternative, analysis period, currency, and nominal or real convention. Include only cash flows caused by choosing the option; exclude sunk costs.
2. **Build incremental cash flows.** Lay out initial investment, operating inflows and outflows, tax effects, working-capital changes, replacement spend, and terminal proceeds by period. Reconcile each major line to an operational assumption.
3. **Calculate NPV.** Discount each period’s incremental free cash flow at the appropriate hurdle rate and sum it with the initial outlay. For mutually exclusive projects, use NPV as the primary value measure because it expresses absolute value created.
4. **Calculate and interpret IRR.** Find the discount rate that makes NPV equal zero, then compare it with the hurdle. Identify multiple or nonexistent IRRs when cash flows change sign more than once; use modified IRR or NPV in those cases.
5. **Stress-test and recommend.** Vary material drivers, report break-even assumptions, apply capital constraints, and explain the decision rule. Keep strategic prerequisites and nonfinancial risks visible beside the cash ranking.
## Output Contract
An investment case with cash-flow schedule, calculation convention, discount rate rationale, NPV, IRR where meaningful, hurdle comparison, sensitivity table, break-even drivers, capital constraint treatment, and recommendation. It must let a reviewer trace each number to a period and an operating assumption, not just show a return percentage.
## Evidence
Use signed contracts, cost estimates, tax rates, and observed volumes as evidence. Label forecasts of adoption, savings realization, terminal value, and timing as assumptions. Do not include allocated corporate overhead unless the decision changes that cash outflow. Keep nominal cash flows with a nominal discount rate and real cash flows with a real rate. If a benefit is strategically important but unquantified, present it separately rather than silently converting it into NPV.
## Checks
- Cash flows are incremental relative to a documented baseline.
- Sign convention, period timing, and inflation convention are consistent.
- Discount rate matches the cash-flow risk and currency.
- NPV and IRR calculations reconcile to the displayed schedule.
- Multiple-sign cash-flow patterns receive an IRR warning.
- Sensitivities identify the driver that can reverse the recommendation.
## Failure Modes
- Comparing projects by IRR alone when a lower-IRR project creates more value.
- Counting a sunk feasibility study as a future cash cost.
- Discounting nominal revenue with a real hurdle rate.
- Calling accounting depreciation a cash outflow while omitting its tax shield.
- Accepting a spreadsheet IRR despite two different rates satisfying irregular cash flows.
