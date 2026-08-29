# Decision Tree Analysis
## Purpose
Map sequential decisions and chance events into a valued tree to identify the optimal contingent path. The method makes visible which decision should wait for information and which branch has the highest expected value under stated probabilities.
## Use
- A decision unfolds as sequential choices under uncertainty with estimable probabilities and payoffs
- You must compare contingent strategies, not a single static alternative
- Expected value, risk exposure, or optimal path at each node must be explicit
## Avoid
- Uncertainty is continuous and needs full distribution simulation—use monte-carlo-simulation
- You need qualitative future narratives without quantified branches—use scenario-planning
- The asset has irreversible timing options better valued as options—use real-options-analysis
## Inputs
**Must-have:** Decision nodes, chance nodes, and terminal outcomes fully specified; Probabilities on chance branches and payoffs or costs on terminals; Discount rate or value metric for comparing paths; Risk attitude or decision rule (e.g., maximize EMV); Sensitivity ranges on key probabilities and payoffs.

**Nice-to-have:** Research costs, decision deadlines, risk limits, and triggers that make later choices observable.

**When data is thin:** Use probability ranges and value-of-information calculations to decide whether another observation is worth buying; do not conceal judgment behind decimal precision.
## Procedure
1. **Frame the decision chronology.** State the first choice, later choices, information revealed between them, terminal horizon, and value metric. Prune events that do not alter a choice or payoff.
2. **Draw decision and chance nodes.** Use squares for controllable choices and circles for uncertainties. Ensure chance branches are mutually exclusive and exhaustive at each node.
3. **Assign branch values.** Put discounted cash flows, costs, or another common payoff at terminals. Attach probabilities to chance branches, documenting the evidence and the time at which costs occur.
4. **Roll back the tree.** Multiply terminal values by probabilities at chance nodes; sum to expected value. At decision nodes, select the permitted branch that meets the stated decision rule and retain the contingent actions.
5. **Stress the pivotal branches.** Vary probabilities, payoffs, timing, and information costs. Identify the break-even probability or value at which the recommended first move changes.
## Output Contract
A labeled tree with decision timing, chance branches, probabilities, terminal values, rollback calculations, preferred initial action, and contingent actions by observed outcome. It includes sensitivity thresholds and any risk-rule exception to the expected-value choice. The decision record must be reproducible from the displayed node assumptions.
## Evidence
Probabilities from frequency data, contract terms, and known costs are evidence; expert probabilities and unpriced externalities are assumptions. State whether probabilities are conditional on prior branches. Do not add outcomes merely to make a tree look comprehensive, and do not assign a zero probability to an inconvenient but plausible loss without justification.
## Checks
- Every chance-node probability totals 100% after rounding.
- Payoffs use the same currency, date basis, and treatment of sunk costs.
- Rollback calculations match the displayed branches.
- The tree includes only decisions management can actually take at that time.
- Sensitivity identifies the assumption capable of reversing the first choice.
## Failure Modes
- Putting a management action after a chance event even though it must be committed beforehand.
- Double-counting a cost at an intermediate node and terminal payoff.
- Treating mutually overlapping market outcomes as separate probability branches.
- Choosing the largest terminal payoff instead of the best expected contingent strategy.
