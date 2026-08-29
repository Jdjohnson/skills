# Agile Product Management
## Purpose
Plan and run iterative product delivery by continuously refining a prioritized backlog against capacity and live user feedback. The backlog is an executable learning plan, not a static list of stakeholder requests.
## Use
- Running continuous product discovery and delivery in short cycles
- Replacing big-bang release planning with backlog-driven iteration
- Aligning product, design, and engineering on prioritized outcomes each sprint
## Avoid
- Scope, budget, and requirements are contractually fixed with no iteration room—use waterfall-methodology or pmbok-framework
- You only need a one-time feature ranking without an operating cadence—use feature-prioritization
- The organization lacks cross-functional ownership and needs structure first—use product-roadmap-development then return
## Inputs
**Must-have:** Product vision and near-term outcome goals; prioritized backlog or candidate work items with acceptance criteria; team capacity and sprint/cadence constraints; feedback channels from users, support, or analytics after each release.

**Nice-to-have:** Product analytics baseline, discovery research, technical-debt inventory, release constraints, and a definition of done.

**When data is thin:** Treat uncertain items as discovery work with a learning objective, cap their effort, and avoid promising an outcome before users have been observed.
## Procedure
1. **Set the product outcome and horizon.** Define the user or business result for the next release window and the guardrails on quality, reliability, and spend.
2. **Shape backlog items.** Break opportunities into slices that can produce usable evidence. Add a user, intended outcome, acceptance criteria, dependencies, and a clear reason the item belongs now.
3. **Order by value, risk, and learning.** Compare items against the outcome, cost of delay, technical exposure, and dependency. Place discovery or enabling work explicitly rather than allowing it to disappear below visible features.
4. **Refine with the delivery team.** Estimate enough to make a capacity decision, challenge oversized slices, and clarify acceptance criteria before commitment. Product ownership decides order; the team decides feasible scope.
5. **Commit a sprint or release increment.** Pull the highest ordered ready items that fit capacity, record the sprint goal, and protect it from unexamined urgent additions.
6. **Review evidence and re-order.** Demonstrate the increment, inspect user feedback and telemetry, hold a retrospective, then update the backlog and roadmap implications.
## Output Contract
Deliver a living backlog and cadence plan containing an outcome statement, ordered work items, acceptance criteria, size or capacity view, dependencies, sprint goal, release hypotheses, and measures to inspect after release. It must identify what is ready to build now and what evidence will change the next order, rather than presenting a multi-year feature wish list.
## Evidence
Usage data, support contacts, and experiment results are observed. Forecast benefit and stakeholder demand are hypotheses until tested. State the source and date of every priority signal, since a past customer request may no longer be relevant. Mark estimates as ranges and record technical uncertainty separately from market uncertainty.
## Checks
- Every committed item contributes to the sprint goal or an explicit enabling constraint.
- Acceptance criteria make “done” testable by product and engineering.
- Capacity includes maintenance, defects, and discovery rather than assuming 100% feature delivery.
- Mid-sprint work enters only through a visible trade-off.
- Release review produces a measurable decision to continue, revise, or stop.
## Failure Modes
- Allowing the backlog to become an unranked intake queue.
- Treating story-point totals as customer value.
- Filling a sprint before clarifying acceptance criteria and discovering the real work halfway through.
- Measuring feature shipment while ignoring activation, retention, or task success.
