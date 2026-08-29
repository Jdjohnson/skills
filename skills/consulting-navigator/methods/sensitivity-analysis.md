# Sensitivity Analysis
## Purpose
Systematically vary model inputs to show which assumptions move results most and where decision thresholds break.
## Use
- A quantitative model exists and you must test how outputs move when inputs change.
- You need to rank assumptions by impact for base, upside, and downside cases.
- Break-even or threshold values are required for a go or no-go decision.
## Avoid
- You need full probabilistic outcomes across joint uncertainty—use monte-carlo-simulation.
- No model yet exists and the problem is still qualitative framing—use issue-tree or hypothesis-driven-problem-solving first.
- You need narrative alternative worlds rather than parameter flexes—use scenario-planning.
## Inputs
**Must-have:** Working quantitative model with defined output metrics; base-case inputs and plausible ranges or step changes for each key driver; rules for one-at-a-time versus selected multi-variable cases; decision thresholds (e.g., NPV > 0, payback, margin floor).

**Nice-to-have:** Historical forecast error, management-approved cases, and an owner for each assumption.

**When data is thin:** Use clearly labeled low/base/high bounds from accountable owners. Test broad bounds first and defer an irreversible decision when the threshold is crossed inside an unverified range.
## Procedure
1. Freeze the formula, calculation period, and output measure before changing any driver. Reconcile the base case to the approved model so later deltas have a common reference.
2. Inventory candidate inputs, their units, base values, plausible lower and upper values, and why each range is credible. Separate controllable levers, such as price, from external assumptions, such as demand.
3. Select the perturbation rule. Flex one factor while holding the rest at base for a ranking; define a limited two-way table only where drivers can jointly create a decision risk.
4. Recalculate the output for every step and record absolute and percentage movement from base. Rank drivers by the output span, not by whichever input has the largest percentage range.
5. Solve for the break-even value of consequential inputs: the price at NPV zero, volume at a margin floor, or cost at a payback limit. Mark ranges that contain a threshold.
6. Present a tornado chart or ranked table, the two-way cases, and the decision triggers. Name the owner who must monitor each trigger after approval.
## Output Contract
Deliver a sensitivity pack with the fixed model version, base output, a driver-and-range register, one-way results ranked by impact, selected interaction tables, and break-even values against stated thresholds. It must distinguish a lever worth managing from a number merely worth measuring. Include a short decision statement such as “approve only if unit price remains above $X”; it is not a probability distribution or a narrative scenario set.
## Evidence
Treat model formulas and actual performance as observed. Label forecast ranges as estimated, and identify whether an interval came from history, a contract, or expert judgment. Do not alter two inputs in a “one-way” run. Correlated drivers may appear together only in an explicit joint case; otherwise readers can mistake an illustrative combination for a likely outcome. If a model omits a material mechanism, state that omission rather than widening an unrelated range.
## Checks
- Base-case output matches the governed workbook before flexing begins.
- Units, sign conventions, and time periods remain constant across runs.
- Every ranked driver has a visible range and range rationale.
- Break-even calculations use the same threshold stated in the decision brief.
- Tornado bars compare equal low-to-high tests rather than mixed increments.
## Failure Modes
- Ranking revenue growth above price because its range was made much wider without justification.
- Calling a correlated price-and-volume downside a one-factor result.
- Hiding a threshold inside a chart whose axis starts far from zero.
- Treating a break-even point as a forecast rather than an operating trigger.
