# Resource Leveling & Smoothing
## Purpose
Make a project schedule resource-feasible by leveling overallocation and smoothing peaks against real people and capacity limits. It turns logic-only dates into a delivery plan that recognizes calendars, skills, and finite assignment capacity.
## Use
- Resolving overallocation by delaying or splitting work within or beyond float
- Smoothing demand to fit fixed capacity without unnecessary peaks
- Producing a resource-feasible schedule after logic-driven CPM dates
## Avoid
- You do not yet have a dependency network and durations—use critical-path-method first
- The constraint is process throughput, not named resource calendars—use theory-of-constraints or bottleneck-analysis
- Portfolio capacity strategy is the issue, not a project schedule—use workforce-planning or capacity-analysis at portfolio level
## Inputs
**Must-have:**
- Activity network with dates or float from a schedule model
- Resource pool with calendars, skills, and max units
- Activity resource requirements
- Leveling rules (priority, split allowed, deadline constraints)

**Nice-to-have:** approved overtime policies, contractor lead times, resource substitution rules, and milestone penalties.

**When data is thin:** assume conservative availability, identify the activities affected, and obtain calendar confirmation before baselining dates.
## Procedure
1. Validate the activity network, durations, dependencies, and calendars. Separate schedule logic errors from resource conflicts before moving any work.
2. Assign named or role-based resources with units and skills to each activity. Calculate demand by day or week and display the initial load histogram.
3. Identify overallocation periods, the tasks competing for the scarce skill, available float, and constraints such as fixed milestones or non-splittable work.
4. Apply leveling rules in order: move noncritical work within float, split permitted activities, reassign qualified capacity, add approved capacity, or delay the finish if no feasible alternative remains.
5. Recalculate the critical path and load histogram after each material change. For smoothing, preserve the finish date where possible; for leveling, make any deadline consequence explicit.
6. Compare the selected schedule with the logic-only baseline and publish changed dates, resource assignments, remaining overloads, and decisions needed from sponsors.
## Output Contract
Deliver a resource-feasible schedule with the dated network, assigned resources and units, before/after load histograms, leveling rules, changed activities, critical-path impact, and unresolved capacity decisions. State whether the plan used smoothing within available float or leveling that moved a deadline. Include a list of scarce roles, overload periods, and the accountable owner for each capacity response. A clean Gantt without finite resource evidence is not sufficient.
## Evidence
Use approved calendars, commitments, skill certifications, and task estimates as observed planning evidence. Mark assumed availability, productivity, and interchangeability of people or vendors. Do not replace a named specialist with a generic full-time equivalent unless competency and onboarding time support it. Keep an uncertainty note where scope or durations are likely to change the resource profile.
## Checks
- Every activity with work has a resource demand and calendar basis.
- No chosen period exceeds the stated maximum units without an approved exception.
- Delayed work respects precedence relationships and nonworking days.
- Resource substitutions meet the skill requirement and transition time.
- Milestone movement and residual overloads are visible to the sponsor.
## Failure Modes
- Calling a schedule “level” after averaging demand across a month that contains a weekly overload.
- Moving critical tasks without recalculating downstream logic.
- Assuming one expert can contribute 100% to several concurrent activities.
- Treating contractors as instantly productive capacity.
- Smoothing work inside float that was already consumed by an undisclosed risk.
