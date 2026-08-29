# Real Options Analysis
## Purpose
Value managerial flexibility in real investments by treating staged expand, defer, abandon, or switch rights as options. It prevents capital decisions from hiding learning and reversible commitments.
## Use
- Valuing investments whose main value is flexibility to expand, defer, abandon, or switch under uncertainty
- Comparing staged commitments versus all-or-nothing CAPEX when information will improve
- Supplementing DCF when irreversibility and learning are material
## Avoid
- Cash flows are stable and flexibility is trivial—use discounted-cash-flow-valuation or npv-and-irr-analysis
- You need qualitative futures without valuation mechanics—use scenario-planning first
- The decision is pure portfolio share/growth positioning, not project flexibility—use bcg-matrix
## Inputs
**Must-have:**
- Base project cash-flow model and uncertainty drivers (volatility, decision points)
- Clearly defined options (expand, defer, abandon, switch) and exercise conditions
- Cost of keeping the option alive and estimated value if exercised
- Decision timeline and information that will resolve before exercise

**Nice-to-have:** market comparables, scenario probabilities, and contract terms governing exclusivity or exit.

**When data is thin:** use ranges for volatility and show the option value across them; do not report a precise premium unsupported by the underlying market.
## Procedure
1. Build the conventional base-case cash-flow valuation so the project’s static value is visible separately from flexibility.
2. Identify the decision right: defer an investment, stage a pilot, expand capacity, abandon a site, or switch an input. Specify who can exercise it, its expiry date, cost, and constraint.
3. Map the uncertainty that changes the underlying asset value and the information arriving before exercise. Translate business events into upside, downside, volatility, and decision dates.
4. Select a transparent pricing approach, such as a binomial lattice for staged decisions or a simulation-based method for complex paths. Keep the option logic consistent with the asset, exercise cost, and time horizon.
5. Calculate static NPV, option-adjusted value, and the incremental flexibility value. Stress-test volatility, delay, exercise cost, and the ability to act when the signal appears.
6. Convert the result into an exercise policy: thresholds, review dates, accountable decision maker, and conditions under which management must abandon rather than continue.
## Output Contract
Produce an option-adjusted business case containing the base DCF, each right being valued, its exercise price and expiry, uncertainty inputs, valuation method, sensitivity ranges, and explicit continue/defer/expand/abandon triggers. Show the value of flexibility separately from operating cash flow. The decision memo must state which future observation activates a right and who has authority to act, rather than merely attaching a higher discount rate to an uncertain project.
## Evidence
Use contractual rights, market prices, and dated cash-flow estimates as observed evidence. Treat volatility estimates, correlations, and exercise feasibility as assumptions with ranges. Clearly mark where management’s ability to expand or exit is inferred from history rather than legally secured. A scenario without a feasible decision right has uncertainty, not an option, and must not receive option value.
## Checks
- The underlying project value can be reconciled to the base cash-flow model.
- Each option has a holder, trigger, expiry, and exercise cost.
- The model distinguishes an option to wait from a vague hope that conditions improve.
- Sensitivities show whether the recommendation reverses at credible volatility or delay values.
- Governance can execute the stated exercise policy in time.
## Failure Modes
- Pricing “flexibility” when a contract or regulator prevents the choice from being exercised.
- Double-counting upside in both the base case and an expansion option.
- Treating a pilot as valuable while ignoring its carrying cost and expiry.
- Using a financial-option formula with inputs unrelated to the project’s uncertainty.
- Approving a staged investment without reserving the future capital required to expand.
