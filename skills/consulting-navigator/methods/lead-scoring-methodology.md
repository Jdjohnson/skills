# Lead Scoring Methodology
## Purpose
Prioritize sales and marketing effort by scoring prospects on fit and intent so the best opportunities get first attention. It converts a mixed inbound queue into transparent follow-up tiers, rather than attempting to repair every funnel stage.
## Use
- Ranking inbound or outbound prospects by fit and intent for sales attention
- Aligning marketing and sales on MQL/SQL definitions with a transparent score
- Improving conversion efficiency when lead volume exceeds selling capacity
## Avoid
- Funnel stages and process are undefined—use sales-funnel-optimization first
- You need account strategy for existing customers, not prospect ranking—use crm-strategy or customer-lifetime-value-analysis
- Sample of closed-won/lost outcomes is too thin to validate scores—use simple ICP rules until data matures
## Inputs
**Must-have:** Historical lead-to-opportunity and win/loss outcomes; firmographic/demographic fit attributes (ICP); behavioral intent signals (web, content, email, product usage); sales capacity and SLA for follow-up by score tier.

**Nice-to-have:** opportunity value, sales notes explaining disqualification, marketing-consent status, and account-level duplicate matching.

**When data is thin:** implement a small rule-based fit score, keep the cutoff conservative, and schedule a review after enough disposition outcomes accumulate.
## Procedure
1. **Define the conversion event and population.** Choose the outcome to predict, such as qualified opportunity within 30 days, and exclude records that sales could never work because of consent, geography, or duplication.
2. **Build candidate signals.** Separate fit attributes such as industry and company size from behavior such as pricing-page visits, webinar attendance, and trial activity. Check when each signal became available to avoid using future information.
3. **Estimate and challenge weights.** Compare conversion rates by signal and test a simple points model or validated predictive model on held-out outcomes. Penalize traits that create volume but not qualified opportunities.
4. **Set score tiers and routing.** Choose thresholds from sales capacity and expected quality. Define response SLA, owner, required next action, recycle rule, and disqualification codes for each tier.
5. **Monitor and recalibrate.** Track score distribution, contact rate, opportunity rate, win rate, and fairness across segments. Review mismatched scores with sales and adjust only after evidence, not anecdote.
## Output Contract
Provide a scored-lead specification with population rules, feature definitions, weights or model version, tier cutoffs, routing logic, service levels, and a dashboard of validation metrics. A rep must be able to see why a record entered a tier and what action follows. The artifact must preserve a path for low-score prospects to be nurtured or corrected when data is incomplete.
## Evidence
Use dated CRM and marketing-automation events; exclude values entered after the conversion event. Record missing attributes rather than quietly treating them as poor fit. Call out survivorship bias when only worked leads have dispositions. Do not score protected traits or use proxies that have not been reviewed for unfair treatment and business relevance.
## Checks
- The outcome window matches the actual sales handoff decision.
- Score components are available when the lead is routed.
- Thresholds fit daily rep capacity and the promised follow-up SLA.
- Validation compares conversion by tier on data not used to choose weights.
## Failure Modes
- Giving ten points for a whitepaper download that was required to access basic documentation.
- Training on closed leads while ignoring thousands never contacted.
- Setting an MQL threshold so low that response time degrades for high-intent prospects.
- Hiding score reasons, causing sales to discard valid leads as arbitrary.
