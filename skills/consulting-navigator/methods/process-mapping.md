# Process Mapping
## Purpose
Make a business process explicit as a step-by-step flow of activities, actors, inputs, and handoffs. A shared current-state map replaces conflicting recollections with a testable view of how work actually moves.
## Use
- Documenting current-state steps, actors, inputs, and outputs for a business process
- Locating handoff failures, loops, and non-value steps before improvement
- Creating a shared baseline before reengineering, automation, or controls design
## Avoid
- You need time and inventory waste quantified across a value stream—use value-stream-mapping
- You only need suppliers-inputs-process-outputs-customers at a high level—use sipoc-analysis first
- The problem is industry structure or market power, not workflow—use five-forces or value-chain-analysis
## Inputs
**Must-have:** Defined process start and end points and scope; access to people who perform or own each major step; sample artifacts, systems, and decision points along the flow; agreement on whether mapping as-is, to-be, or both.

**Nice-to-have:** timestamps, volume and error data, policy documents, screen captures, queue reports, and representative exception cases.

**When data is thin:** map the normal path from direct observation, use a different line style for unverified steps, and schedule validation with the people doing the work.
## Procedure
1. **Set the boundary.** Name the triggering event, end condition, customer or recipient, and level of detail. Decide whether the map follows one case type or separates materially different variants.
2. **Walk the work.** Interview or observe performers in sequence, collecting the form, system, decision rule, and output at each action. Ask what happens next, not what the policy says should happen.
3. **Draw the primary flow.** Use consistent symbols for activity, decision, document, system, and wait. Place steps in swimlanes by accountable role so ownership changes are visible.
4. **Add handoffs and branches.** Connect the actual transfer of information or work, label decision criteria, and capture rework loops, escalations, and external dependencies. Do not force exceptions into a fictional straight line.
5. **Validate the map.** Replay a recent case with cross-functional participants. Reconcile disagreements against artifacts or system history, then mark uncertain links for follow-up.
6. **Annotate improvement observations.** Call out duplicate entry, unclear decision rights, queue points, missing outputs, and control gaps. Keep observations separate from the as-is map so the baseline remains credible.
## Output Contract
A legible current-state or future-state flow with stated boundaries, swimlanes, activity and decision symbols, inputs and outputs, handoffs, branch conditions, exception loops, and validation status. It must let a new participant trace one case from trigger to completion and identify where an item can stall or return.
## Evidence
Observed evidence includes screen flows, sampled cases, forms, and direct observation. Interview statements are reported as participant accounts until corroborated. Mark a proposed future step as design, not present fact. Do not infer sequence from the organization chart; a manager’s reporting line is not proof of a work handoff.
## Checks
- The first and last events are explicit and within agreed scope.
- Every activity has a performer or system and a discernible output.
- Decisions name the criterion that selects each outbound path.
- Handoffs cross lanes where responsibility actually changes.
- At least one normal case and one meaningful exception have been replayed.
## Failure Modes
- Mapping departmental responsibilities instead of the order an individual case travels.
- Omitting email, spreadsheet, or chat steps because they are not official systems.
- Drawing only the happy path and missing the rework that consumes most effort.
- Mixing proposed automation into an as-is map until nobody can tell what is real.
- Using boxes so broad that a decision, an action, and three handoffs disappear inside one label.
