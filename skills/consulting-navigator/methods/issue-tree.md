# Issue Tree
## Purpose
Break a complex governing question into a hierarchical tree of mutually testable sub-issues that drive analysis workstreams. The tree makes the logic of what must be true or false visible before the team collects a mountain of data.
## Use
- A complex, multi-factor problem must be broken into testable branches before analysis
- You need a shared visual map of how the governing question decomposes
- Workstreams must be partitioned without gaps or double-coverage
## Avoid
- The governing question is already crisp and single-branch—start with hypothesis-driven-problem-solving or root-cause-analysis
- You only need a communication narrative, not a problem structure—use scqa or pyramid-principle
- The issue is a known linear process flow rather than a decision problem—use process-mapping or sipoc-analysis
## Inputs
**Must-have:** A clear governing question or problem statement; Boundary of what is in and out of scope; Initial hypotheses or known drivers from experts or prior work; Criteria for what 'solved' would mean at the top of the tree.

**Nice-to-have:** Baseline metrics, prior analyses, decision constraints, and named owners for each possible branch.

**When data is thin:** Build the first tree from expert challenge sessions, label untested splits, and use it to prioritize the next evidence request rather than asserting causes.
## Procedure
1. **Write one answerable governing question.** Include the metric, population, time period, and decision where possible. A vague question such as “fix profitability” cannot anchor a useful tree.
2. **Select the decomposition logic.** Choose a driver tree, a process tree, a profit equation, or a decision tree based on the question. Do not mix causes, outcomes, solutions, and stakeholder opinions on the same level.
3. **Split the first level cleanly.** Make branches collectively cover the parent question and avoid overlap. State the test each branch will answer, so “pricing” becomes “is realized price below target by segment?”
4. **Decompose to analysis-ready leaves.** Continue only until each leaf can be assigned to one workstream with a feasible fact base, hypothesis, and expected conclusion. Stop before the diagram becomes a catalogue of trivia.
5. **Test completeness and exclusivity.** Walk upward from each leaf to confirm it contributes to the parent; look for double counting and missing residual categories. Challenge the tree with a counterexample.
6. **Turn leaves into a workplan.** Prioritize branches by likely decision impact, uncertainty, and speed of evidence. Assign owners, data needs, and a synthesis cadence.
## Output Contract
A one-page issue hierarchy with the governing question at the root; labeled branches and analysis-ready leaves; the logic used for each split; priority, owner, hypothesis, and evidence requirement for each leaf; and an explicit out-of-scope boundary. It must organize investigation, not claim a root cause before testing.
## Evidence
Treat the tree’s structure as a hypothesis, not evidence. Cite observed baselines at leaves, distinguish expert-suggested drivers from verified ones, and mark branches with no available test. Keep mutually exclusive categories numerically reconcilable where the tree partitions a total; otherwise state that the split is conceptual.
## Checks
- Every child answers a portion of its parent, using one level of abstraction.
- Branches neither overlap nor leave an unexplained remainder.
- Every terminal leaf has a testable question and a plausible evidence source.
- The root preserves the decision and boundary from the original brief.
- Workstream scope follows leaves, preventing duplicate data requests.
## Failure Modes
- Starting with favorite solutions, then disguising them as diagnostic branches.
- Mixing “why profit fell” with “how to fix it” in adjacent branches.
- Stopping at labels such as people, process, and technology that no analyst can test.
- Treating MECE as decorative jargon while double-counting the same driver.
