# Game Theory
## Purpose
Model interdependent decisions among strategic actors to forecast equilibrium outcomes and best-response strategies. The method asks what each player will do after considering the incentives and anticipated moves of the others, not merely which internal option appears attractive in isolation.
## Use
- Forecasting outcomes when a few rational players interact strategically.
- Structuring pricing, entry, capacity, or bidding moves with explicit payoffs.
- Identifying dominant strategies, equilibria, and credible threats or commitments.
## Avoid
- Many uncertain external futures matter more than rival moves—use scenario-planning.
- The decision is mostly internal optimization with weak strategic interaction—use decision-tree-analysis or monte-carlo-simulation.
- You lack even rough payoffs and player definitions—gather structure first via competitive-benchmarking or five-forces.
## Inputs
**Must-have:** Defined players, actions, and information assumptions; payoff estimates (profit, share, or utility) for action combinations; timing rules (simultaneous vs sequential) and commitment ability; beliefs about rival objectives and constraints.

**Useful additions:** historic responses, capacity constraints, contract terms, competitor financials, and alternative payoff estimates.

**Modeling boundary:** state which actors are strategic players and which conditions are fixed background assumptions; a game that silently omits the regulator or dominant distributor may be misleading.
## Procedure
1. Specify the decision question, players, and objective each player is assumed to optimize. Separate named firms, customers, regulators, and partners only when their actions materially alter outcomes.
2. List the feasible actions for each player, including “do nothing,” and eliminate choices that are physically, legally, or financially unavailable. Set the timing: simultaneous move, observed sequence, repeated interaction, or private information.
3. Estimate payoffs for every material action combination in a common unit. Build them from contribution margin, share, capacity utilization, utility, or another relevant measure, and make contested inputs ranges.
4. Represent a simultaneous setting as a payoff matrix; represent sequential moves as a decision tree with player nodes rather than chance nodes. Mark commitments, retaliation capability, and information each player has when choosing.
5. Solve for best responses and equilibria. For a sequential setting, use backward induction: determine the follower’s rational response at each later node before evaluating the leader’s opening move.
6. Stress-test the conclusion by changing uncertain payoffs, information, and rationality assumptions. Convert robust outcomes into a recommended move, contingency response, and early indicators that a rival’s behavior differs from the model.
## Output Contract
Provide a game definition, action set, payoff matrix or tree, assumptions register, identified equilibrium or equilibria, sensitivity cases, and recommended strategy with contingent replies. Show the payoff logic, not only the final label. The deliverable must distinguish an equilibrium prediction from a recommendation the client prefers but cannot sustain against a rival response.
## Evidence
Contracts, capacity data, public prices, and observed prior moves are evidence. Payoff estimates and beliefs about a rival’s goals are modeled inferences. Rationality, information availability, and credible commitment are assumptions that receive explicit sensitivity tests. Unknown retaliation cost or private information should generate alternative games, not be buried in a single payoff cell.
## Checks
- Each player has at least two feasible actions and a defined objective.
- Payoff order is consistent across cells: first player, second player, then any others.
- Best-response markings are recalculated after every scenario change.
- Sequential games do not use a simultaneous equilibrium as if timing were irrelevant.
- The recommendation remains sensible in the downside payoff range or identifies a trigger to switch.
## Failure Modes
- Calling a threat credible when the threatened player would lose money by carrying it out.
- Assigning a competitor the client’s objectives rather than its own incentives.
- Omitting a capacity limit that makes an apparent price war response impossible.
- Selecting one equilibrium without explaining how expectations coordinate on it.
