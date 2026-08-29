# Treasury Management Framework
## Purpose
Design and govern group liquidity, funding, and market-risk policies so cash is visible, mobile, and protected. It establishes the standing accountabilities and controls that allow a group to manage funding and exposures every day.
## Use
- Designing group cash concentration, liquidity buffers, and funding policy.
- Setting governance for FX, interest-rate, counterparty, and refinancing risk.
- Professionalizing banking structure, treasury controls, and cash visibility.
## Avoid
- The bottleneck is operating cycle length in AR/AP/inventory—use working-capital-management first.
- You need a multi-year enterprise value model—use discounted-cash-flow-valuation.
- The issue is full ERM taxonomy beyond treasury market risk—use enterprise-risk-management.
## Inputs
**Must-have:** Cash positions by entity, currency, and bank account; debt schedule, covenants, and planned funding events; FX and interest exposure map and hedge inventory; treasury policies, authorities, and banking agreements; short-term cash forecast and liquidity buffer targets.

**Nice-to-have:** bank fee analysis, counterparty credit limits, forecast accuracy history, and tax or regulatory constraints on cash movement.

**When data is thin:** start with material entities and accounts, impose a daily position cutoff, and place uncertain balances outside the usable-liquidity total until confirmed.
## Procedure
1. **Map cash, banks, and authority.** Inventory accounts, signatories, balances, currencies, sweeps, pooling structures, banking partners, and access rights. Identify dormant accounts, trapped cash, duplicated authorities, and concentration points.
2. **Set the liquidity operating model.** Define daily cash positioning, forecast horizon, minimum buffers, funding hierarchy, cash concentration mechanics, and escalation triggers for forecast shortfall or covenant headroom.
3. **Measure financial exposures.** Build a schedule of debt maturities, rate basis, FX exposures, hedge instruments, counterparty limits, and policy breaches. Distinguish transaction exposure from translation exposure.
4. **Design policy and controls.** Specify dealing authorities, segregation of duties, confirmations, bank-account lifecycle control, approved instruments, hedge documentation, limit monitoring, and board reporting.
5. **Sequence implementation.** Prioritize quick account rationalization and visibility fixes, then concentration, risk systems, and refinancing actions. Assign an owner and test each control through a live operating cycle.
## Output Contract
The framework provides a treasury target operating model, bank-account map, liquidity policy, forecast cadence, funding and maturity plan, exposure and hedge policy, authorities matrix, control catalogue, KPI dashboard, and implementation roadmap. It shows who can move cash, approve debt or hedges, and escalate breaches. It does not replace the underlying receipts-and-payments forecast.
## Evidence
Bank statements, debt agreements, executed hedges, and authorized signatory lists are observed. Use a dated cash snapshot; do not combine balances from incompatible cutoff times. Label repatriation ability, covenant headroom, credit availability, and forecasted flows as assumptions or estimates where legal or operational confirmation is absent. Keep notional exposure distinct from actual cash at risk. Reconcile each hedge to a documented exposure and policy limit.
## Checks
- Bank accounts, balances, and signatories reconcile to independent records.
- Usable liquidity excludes restricted or inaccessible cash.
- The forecast’s timing convention matches debt and payroll obligations.
- Every hedge has an exposure, authority, limit, and effectiveness review.
- Controls separate deal initiation, approval, confirmation, and settlement.
## Failure Modes
- Calling overseas cash available without checking controls, tax, or local restrictions.
- Netting currencies before measuring the settlement risk.
- Leaving departed executives as account signatories.
- Using a monthly balance report to manage a weekly covenant trigger.
- Buying a hedge after exposure has already settled.
