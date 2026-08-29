# Critical Path Method
## Purpose
Compute the longest dependency path through a project network so schedule control focuses on the activities that set finish date. The method reveals which logic links and durations determine the promised date before resource constraints are imposed.
## Use
- Building or stress-testing a deterministic project schedule from task dependencies and durations
- Identifying which activities must finish on time to protect the end date
- Explaining schedule risk to sponsors with float and path logic, not gut feel
## Avoid
- Activity durations are highly uncertain and probabilistic—use monte-carlo-simulation or scenario-planning on the network
- You need resource-constrained dates before a pure logic path—use resource-leveling-and-smoothing after CPM
- Work is continuous flow without a finite activity network—use kanban-system
## Inputs
**Must-have:**
- Work breakdown with discrete activities
- Predecessor/successor dependency logic
- Duration estimates per activity
- Defined project start and any hard constraints or milestones

**Nice-to-have:** calendars, logic-review workshops, historical actual durations, contractual milestones, and a coded schedule status date.

**When data is thin:** use explicit planning estimates and identify the links needing validation; never invent predecessors merely to make a network display neatly.
## Procedure
1. **Define activities and completion rules.** Break scope into finishable tasks with one accountable owner, duration, and unambiguous start and finish condition. Output: activity list.
2. **Connect the network.** Record finish-to-start, start-to-start, finish-to-finish, leads, lags, external dependencies, and milestones. Remove open ends and circular logic. Output: logic network.
3. **Run the forward pass.** Calculate each activity’s early start and early finish by carrying the controlling predecessor’s finish through the network. Output: earliest-date schedule.
4. **Run the backward pass.** Start from the required or calculated finish and calculate late start and late finish for every activity. Output: latest-date schedule.
5. **Calculate float and inspect the longest path.** Total float equals late start minus early start; trace zero or near-zero-float chains and validate their logic with task owners. Output: critical-path report and schedule-control actions.
## Output Contract
A logic-driven schedule containing activities, durations, dependencies, early and late dates, total float, milestones, the critical or longest path, and the specific activities requiring control. It must disclose fixed constraints and calendars that affect dates. A Gantt chart without traceable network logic is not a critical-path result.
## Evidence
Base durations on completed-work history, supplier commitments, or named estimator judgment and mark their source. Treat dependencies as claims that must be validated by the people doing the work. Separate imposed milestone dates from calculated dates. Record lags and constraints explicitly because they can hide schedule risk and distort float.
## Checks
- Every nonterminal activity has a successor and every nonstarting activity has a predecessor.
- No circular logic, unexplained hard constraint, or negative float is hidden.
- Critical activities form a continuous path to the finish milestone.
- Durations and dependencies are reviewed with accountable owners.
- Near-critical paths are reported when small slippage could change the finish date.
## Failure Modes
- Calling the longest row of a Gantt chart a critical path without a network calculation.
- Adding arbitrary lags to force a preferred milestone date.
- Ignoring near-critical paths that overtake the current path after one delay.
- Using CPM alone to claim a feasible schedule when scarce resources are double-booked.
