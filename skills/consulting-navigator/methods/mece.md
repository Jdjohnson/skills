# MECE
## Purpose
Test and reshape any breakdown so its parts neither overlap nor leave gaps relative to a defined universe. It is a structural test for a list, segmentation, or one level of a tree, not the logic for choosing the question or prioritizing the answers.
## Use
- Checking that a breakdown of issues, options, segments, or causes has no overlap and no missing pieces
- Building or stress-testing an issue tree, option set, or segmentation scheme
- Forcing teams to name what is excluded so coverage claims are honest
## Avoid
- You need the hierarchical problem map itself—use issue-tree and apply MECE at each level
- The task is causal diagnosis of a known failure mode—use root-cause-analysis or five-whys-style depth, not category hygiene
- Creative divergence is the goal and premature partitioning would kill ideas—use structured-brainstorming first, then MECE to clean the list
## Inputs
**Must-have:** A candidate list, tree level, or set of categories to test; a defined universe or scope the set must cover; a decision rule for what counts as the same versus different items.

**Nice-to-have:** source data that can be reconciled to the universe, edge cases, and a named owner for category definitions.

**When data is thin:** write boundary definitions and test with representative cases. A clear “unclassified” bucket is safer than pretending coverage.
## Procedure
1. **State the universe.** Define the population, time period, unit of analysis, and inclusion rule. “Reasons customers leave” is not enough; specify voluntary churn among annual-contract customers in the last quarter.
2. **Name the classification axis.** Decide whether parts are grouped by cause, customer type, process step, or decision option. Do not mix axes at the same level.
3. **Test exclusivity with edge cases.** For each pair, ask whether one real item could fit both. Split a category, tighten its definition, or impose a deterministic assignment rule when it can.
4. **Test collective coverage.** Compare the set against the declared universe, source totals, and known exceptions. Add an omitted branch only when it belongs on the selected axis; otherwise flag a scope change.
5. **Reconcile and label.** Count or map every item where practical, retain a visible residual, and publish definitions that let another analyst classify the next item the same way.
## Output Contract
A cleaned breakdown showing the universe, chosen axis, category definitions, assignment rules for edge cases, uncovered items, and a reconciliation or coverage test. The artifact must say which categories changed and why; it is not a generic list of neat-looking headings.
## Evidence
Treat item-level records and reconciled totals as observed. Mark category definitions as design choices and expert judgments as assumptions. If categories cannot be reconciled numerically, document the coverage test used instead. Never remove difficult cases just to make the structure look exhaustive; retain an exceptions log until the owner decides whether the taxonomy must change.
## Checks
- Every category uses the same classification axis.
- Pairwise overlaps have a written assignment rule or have been eliminated.
- The universe has a start and end boundary.
- A sample of real items can be assigned by a second reviewer consistently.
- Residual or excluded items are visible and explained.
## Failure Modes
- Combining “pricing,” “enterprise customers,” and “sales execution” in one level.
- Calling categories exclusive while allowing the same complaint into two queues.
- Declaring exhaustive coverage without defining the population being covered.
- Hiding exceptions in an “other” bucket that becomes the largest category.
- Using MECE to make an issue tree visually tidy before its causal logic is tested.
