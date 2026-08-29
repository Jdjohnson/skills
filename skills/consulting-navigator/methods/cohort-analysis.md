# Cohort Analysis
## Purpose
Diagnose how groups that share a start event behave across subsequent time windows relative to one another. It separates a real product or channel change from shifts in the mix or maturity of customers, rather than treating one monthly aggregate as the answer.
## Use
- You need to separate time, lifecycle, and acquisition effects on customer behavior.
- Retention, engagement, or revenue must be compared across groups defined by a shared start event.
- You are diagnosing whether performance shifts are product, mix, or vintage driven.
## Avoid
- You only need a single-period snapshot of conversion drop-offs—use funnel-analysis.
- The question is why individuals leave at a moment in time without vintage structure—use churn-analysis.
- You lack event timestamps or a clear cohort-defining event—instrument first.
## Inputs
**Must-have:** User/account identifiers with a defining start event and timestamp; longitudinal outcome events (activity, revenue, churn, renewal); cohort definition rules (signup month, channel, plan, experiment cell); consistent time buckets for follow-up windows; enough history to compare mature and immature cohorts fairly.

**Nice-to-have:** acquisition spend, release dates, plan changes, and account-level attributes that explain a divergence.

**When data is thin:** publish only windows completed by every compared cohort; do not fill missing future periods with zeroes.
## Procedure
1. Choose the origin event, such as first paid invoice, and freeze the inclusion rule so an account enters once.
2. Build a person- or account-level event table, deduplicate events, and assign each record an origin week or month plus lifecycle age.
3. Define the outcome precisely: retained can mean any active day, renewal, or repeat purchase. Calculate each cohort's eligible population before measuring it.
4. Pivot cohort rows against age columns. For retention, divide active members at age *n* by the original cohort; for revenue, show revenue per original member and, separately, per active member.
5. Read diagonals and like-for-like columns. Compare cohorts at the same age, then annotate releases, channel changes, and sample sizes that may explain a break.
6. Segment only after the base table establishes a pattern, for example by acquisition channel within the affected signup months. Turn the finding into an experiment or investigation.
## Output Contract
Deliver a triangular cohort table with cohort size, lifecycle-age columns, metric definition, and a maturity cutoff. Include a chart of comparable-age retention or revenue, annotations for material events, and a finding that distinguishes mix change from within-cohort change. A funnel conversion snapshot or individual churn score does not satisfy this contract.
## Evidence
Treat timestamped starts and outcomes as observed. Label timezone conversions, identity stitching, reactivation treatment, and the definition of “active” as assumptions. Flag small cohorts and censored recent cohorts as uncertain. Never compare a twelve-month-old row with a two-month-old row as if both had twelve observed periods.
## Checks
- Each member belongs to one origin cohort for the selected analysis.
- Denominators remain the original eligible cohort unless the table explicitly says otherwise.
- Calendar period and lifecycle age are both available, avoiding a misleading aggregate trend.
- Outcome events reconcile to a raw-event count or revenue ledger.
- Conclusions use equal-age comparisons and report cohort sizes.
## Failure Modes
- Calling an acquisition-mix shift a retention improvement because the monthly total rose.
- Counting a trial account twice after conversion creates artificial later-period retention.
- Letting recent, incomplete cohorts depress an age column.
- Using “active” inconsistently across product versions.
- Splitting into so many channel and plan cells that sampling noise becomes a product diagnosis.
