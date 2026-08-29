# Funnel Analysis
## Purpose
Diagnose conversion leakage by quantifying drop-off at each ordered step toward a defined goal. It turns an instrumented path into an ordered loss account, showing where people stop progressing and which segments deserve investigation first.
## Use
- A goal path can be expressed as ordered stages with measurable progression.
- You need to locate the largest drop-offs before redesigning steps.
- Conversion performance must be compared across segments, channels, or periods.
## Avoid
- The problem is long-horizon retention by signup vintage—use cohort-analysis.
- You need root causes inside a single process step's operations—use process-mapping or root-cause-analysis.
- You are designing the commercial sales motion end-to-end—use sales-funnel-optimization after diagnosis.
## Inputs
**Must-have:** Defined ordered stages from entry event to goal conversion; event instrumentation that attributes users/sessions to each stage; time window and segmentation dimensions (channel, device, segment); volume and conversion rates at each step, including absolute drop-offs; business definition of success and any multi-path caveats.

**Useful additions:** experiment history, error logs, page speed, qualitative replay evidence, and campaign spend.

**Identity rule:** specify whether the denominator is users, sessions, accounts, or opportunities. Never mix them within one path.
## Procedure
1. State the conversion goal and choose a path that preserves event order. Define entry, each qualifying stage, conversion, time-to-convert window, and treatment of re-entry or alternate routes.
2. Audit event names, timestamps, user identity, and joins. Compare a sample of raw events with the product or CRM record to locate missing or duplicated instrumentation before calculating rates.
3. Count the eligible population at each stage. Compute both conditional conversion from the preceding step and cumulative conversion from entry, then calculate absolute people lost between steps.
4. Segment the path by channel, device, geography, product, customer type, or experiment cohort. Require enough volume before ranking a small segment’s apparent leak.
5. Rank leaks by lost conversions and business value, not percentage decline alone. A 10-point decline near the top can outweigh an 80% decline among a handful of users.
6. Form specific explanations using error logs, recordings, support contacts, or interviews. Select a redesign or experiment for the highest-value confirmed hypothesis and keep the baseline for later comparison.
## Output Contract
Deliver a funnel specification, instrumentation audit, table of stage counts and conditional/cumulative rates, segment cuts, ranked leaks, diagnostic hypotheses, and a prioritized test backlog. Include the denominator, period, inclusion rules, and data exclusions. The result says where conversion is lost; it does not assert why without additional evidence.
## Evidence
Captured events and transaction records are observed, subject to the instrumentation audit. Derived rates and segment differences are inferred from those events. Stage definitions, attribution windows, bot filtering, and value per conversion are assumptions documented beside the chart. If client-side events are blocked or identity stitching is incomplete, report a bounded or directional result rather than a precise rate.
## Checks
- A person cannot appear in a later stage without an explained route through the funnel.
- The date window allows the intended conversion lag before calling recent entrants drop-offs.
- Counts reconcile to the underlying event population after stated exclusions.
- Segment comparisons use the same stage definitions and time window.
- The first proposed test addresses a measured leak rather than the most visually dramatic chart color.
## Failure Modes
- Calculating checkout conversion from page views when many sessions never saw a purchasable item.
- Treating a consent-banner tracking loss as customer abandonment.
- Ranking a 90% decline among ten users above a leak affecting 8,000 qualified users.
- Combining mobile and desktop paths even though their required steps differ.
