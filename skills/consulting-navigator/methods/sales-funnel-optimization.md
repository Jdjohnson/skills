# Sales Funnel Optimization
## Purpose
Improve end-to-end sales and marketing conversion by diagnosing stage drop-offs and redesigning process, offer, and handoffs that raise throughput. The work turns measured leakage into tested changes, not just a report of funnel percentages.
## Use
- Stage conversion rates are the constraint and you need evidence-based process and offer fixes
- Marketing and sales handoffs leak value and require shared funnel diagnostics
- You want continuous improvement of conversion with measurement and experiments
## Avoid
- Root issue is rep capacity, skills, or territory design—use sales-force-effectiveness
- You lack any stage definitions or CRM hygiene—fix funnel-analysis and data first
- The offer itself lacks product-market fit—use product-market-fit-analysis before optimizing the funnel
## Inputs
**Must-have:** Defined funnel stages and conversion definitions; volume and conversion metrics by stage, segment, and channel; drop-off reasons from CRM notes, win/loss, or user analytics; ability to change process, messaging, or routing and measure impact.

**Nice-to-have:** response-time logs, recording or session evidence, campaign costs, pricing exceptions, and experiment traffic allocation.

**When data is thin:** establish stage entry and exit rules first, then run a short baseline period instead of inferring conversion from inconsistent labels.
## Procedure
1. **Instrument the funnel.** Define mutually exclusive stages, start and exit events, time windows, ownership, and treatment of duplicates. Rebuild the baseline by channel and segment so marketing and sales use the same denominator.
2. **Locate the constraint.** Calculate volume, conversion, velocity, and abandonment at each transition. Follow cohorts rather than comparing different monthly populations; isolate the transition with the greatest lost economic value.
3. **Diagnose the leak.** Inspect rejected leads, call recordings, form behavior, emails, and CRM reasons. Distinguish qualification error, delayed follow-up, weak proposition, offer friction, routing failure, and sales objection.
4. **Design targeted interventions.** Write a hypothesis for the selected transition, such as a faster routing rule, revised qualification question, proof point, or offer. Specify audience, expected mechanism, guardrail, owner, and measurement window.
5. **Test, learn, and scale.** Run controlled tests where traffic permits; otherwise use a dated pilot with a matched baseline. Promote only changes that improve the target transition without harming downstream win rate, deal value, or acquisition cost.
## Output Contract
Provide an implementation plan containing the funnel definition, segmented baseline, prioritized leakage diagnosis, experiment backlog, change owners, target metrics, and rollout rules. Each intervention must name its affected transition and the evidence that would cause it to be stopped or expanded.
## Evidence
Use timestamped system events for observed movement. CRM loss reasons and qualitative comments are coded evidence with an explicit sample size, not universal truth. Do not add conversion rates across stages or compare channels with different qualification rules. Mark attribution, seasonality, and traffic-mix effects as assumptions; retain raw counts alongside percentages.
## Checks
- Stage populations form a traceable cohort and conversion denominator.
- The chosen fix addresses a documented drop-off cause, not a generic best practice.
- Test success includes a downstream guardrail such as opportunity quality or close rate.
- Routing and response-time changes have accountable operational owners.
- A weekly review can detect a metric shift before declaring causality.
## Failure Modes
- Improving lead-form completion while flooding sellers with poor-fit inquiries.
- Celebrating a higher meeting rate when no-show or close rate collapses.
- Diagnosing a mid-funnel leak with aggregate data that hides a single channel's failure.
- Changing message, audience, and routing simultaneously, leaving no learnable result.
- Treating a CRM stage change as customer progress without behavioral evidence.
