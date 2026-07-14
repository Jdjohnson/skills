---
name: plan
description: Co-create a day, week, or month plan through lightweight approval phases. Use when the user wants to plan a period, reconcile tasks and calendar constraints, update an existing plan, or decide what belongs now versus later.
---

# Plan

Act as a planning partner, not a form. Read available context first, name the shape of the period, and move through one phase at a time. Do not dump a complete plan before the user has had a chance to correct it.

## Modes

Use `day`, `week`, or `month`. If the user does not name a mode, infer the most likely one from their request and current date; ask one concise question only when the choice materially changes the result.

## Context and destination

Before proposing work, inspect the sources the user has made available: current and prior plans, project or meeting notes, calendar events, task systems, and workspace instructions. Treat workspace-specific planning preferences as configuration, not universal rules.

Determine the output destination in this order:

1. A path the user explicitly names.
2. A planning route defined by workspace instructions.
3. An existing current-period plan.
4. A proposed filename that the user can approve before it is created.

Do not invent a private directory convention. Preserve existing structure when updating a plan.

## Approval phases

Show only the current phase. At each major step, ask for corrections, additions, or approval and wait before continuing.

1. **Shape** — Summarize the character of the day, week, or month in a few source-backed sentences.
2. **Constraints and capacity** — Name fixed commitments, deadlines, available time, dependencies, and real limits.
3. **Top outcomes** — Propose up to three outcomes that deserve focus.
4. **One thing** — Recommend the single outcome whose progress would matter most.
5. **Tasks, meetings, deadlines, and prep** — Reconcile the actual work from notes, calendar, and task sources.
6. **Parking lot** — Show only known items that clearly should not be active in this period.

Write or update the final plan only after the phases have been approved or clearly revised.

## Work table

Use a compact, editable table unless the workspace already has a clearer convention:

| Item | Type | Source | Owner | Time / Due | Priority | Status | Next action |
|---|---|---|---|---|---|---|---|

Include only real tasks, meetings, deadlines, or decision items. A scheduled meeting is already work; do not create a separate prep task unless a concrete deliverable is required beforehand. Preserve completed rows when updating an existing plan.

## Task and calendar reconciliation

- Keep connector searches bounded to the current period and relevant workstreams.
- Include subtasks when the task source exposes them.
- Deduplicate by stable task ID or URL first, then normalized title plus project or context.
- Compare source tasks with the current and proposed plan before adding rows.
- Surface overdue, due-soon, undated, or unassigned items only when they are relevant to the active planning scope.
- If a connector is unavailable, say which reconciliation could not be completed and continue from the available context.
- Approval of the plan is not approval to create, complete, assign, comment on, reschedule, or otherwise mutate an external task or calendar event. Get explicit approval for each mutation.

## Parking-lot rules

An item belongs in the parking lot only when the user explicitly defers it, a future date makes it inactive now, or it is blocked on a named dependency. Do not park work merely because it is lower priority, unclear, inconvenient, or potentially distracting. Ask when uncertain.

## Integrity rules

- Do not invent tasks, owners, commitments, dates, meetings, or constraints.
- Do not turn background activity or completed work into new plan rows.
- Keep raw user wording distinct from synthesis when both are saved.
- Do not send messages or mutate external systems without explicit approval.
- Keep planning distinct from reflection, inbox triage, meeting closeout, and general task cleanup.
