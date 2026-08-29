# Churn Analysis
## Purpose
Diagnose why customers leave by linking behavioral, operational, and stated-exit evidence into prioritized retention drivers. It separates the event of leaving from the causes that a retention team can actually prevent.
## Use
- Identifying why customers cancel, lapse, or fail to renew
- Segmenting leavers by reason, value, and preventability
- Prioritizing retention interventions before scaling acquisition spend
## Avoid
- You need long-run value of remaining customers rather than leave drivers—use customer-lifetime-value-analysis
- The issue is acquisition conversion, not retention—use sales-funnel-optimization or funnel-analysis
- You lack any usage, support, or exit data—instrument first
## Inputs
**Must-have:** Customer status history (active, cancelled, lapsed) with dates; usage, engagement, or purchase frequency signals before exit; exit reasons, support tickets, and NPS/CSAT where available; customer attributes (segment, plan, tenure, acquisition channel).

**Nice-to-have:** renewal offers, payment failures, product releases, competitor mentions, and account-manager notes.

**When data is thin:** define the churn event and denominator first, then use coded interviews as directional evidence instead of pretending every cancellation reason is known.
## Procedure
1. **Define the churn event and exposure base.** Decide whether cancellation, non-renewal, inactivity, or involuntary payment lapse counts as churn. Freeze the observation window and distinguish customers eligible to churn from new customers.
2. **Build the customer timeline.** Join status changes to usage, orders, support contacts, price changes, and survey signals. Align each signal by days before exit so a last-week ticket is not confused with a ticket from a year earlier.
3. **Measure patterns across cohorts.** Calculate churn rate by tenure, plan, acquisition source, value band, and product behavior. Compare leavers with retained customers who had the same opportunity to leave.
4. **Code and test drivers.** Group exit reasons and operational events into candidate drivers, then test timing, concentration, and counterexamples. Separate voluntary dissatisfaction, product-fit loss, competitor switching, and involuntary churn.
5. **Prioritize save levers.** Estimate affected accounts, preventability, expected value, and intervention owner. Recommend product, service, billing, or offer changes, with a holdout or phased test where feasible.
## Output Contract
Provide a retention diagnosis with a documented churn definition, rate and denominator, cohort cuts, pre-exit signals, ranked drivers, confidence, preventability, and intervention backlog. Each driver must show the population affected and the evidence path; the deliverable is not just a retention curve or a customer-value forecast.
## Evidence
Treat dated status, transaction, product, and support records as observed. Mark reason codes, causal links, and missed-save estimates as inferred unless directly confirmed. State how missing cancellations, merged accounts, and involuntary payment failures are handled. Preserve an “unknown reason” category. A correlation such as falling usage should prompt a test, not be represented as proof that usage caused departure.
## Checks
- The churn numerator and at-risk denominator are explicit and stable across cuts.
- Timelines use evidence from before the exit event.
- Retained comparison customers are included for major drivers.
- Voluntary, involuntary, and contractual exits are not mixed blindly.
- Every proposed save action has a measurable success metric and owner.
## Failure Modes
- Counting customers who never reached renewal eligibility as churned.
- Treating a cancellation click as the root cause when support failures began 30 days earlier.
- Offering discounts to payment-failure accounts that need billing remediation.
- Ranking reasons by frequency while ignoring high-value accounts or preventability.
