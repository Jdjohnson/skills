# Gather Context

Gather silently and narrowly before speaking.

## Always

1. Read the workspace's current re-entry index and period pointers when present.
2. Read configured planning preferences and routes before any write.
3. Read the relevant current and prior period files, including raw journal sources before assistant synthesis.
4. Open project, sales, meeting, or other canonical records only for lanes named in the plan, journal, or request.
5. Read the personal profile only when relationships, health, goals, or collaboration style genuinely matter.

Use configured read-only calendar, task, time, weather, or device adapters only when they materially improve the selected mode. Dedupe by stable ID, then normalized title plus context. A failed adapter creates a bounded reconciliation gap, not an empty result. Never broaden accounts, collections, dates, or permissions to compensate, and never mutate an external system during gather.

## Mode sources

- `full` / `light`: today, yesterday's close, current week/month, today's calendar, near-term tasks, named decisions.
- `close`: complete day record, raw journal, log, planned priorities, current artifacts, and useful read-only task/calendar evidence.
- `week` / `review`: current and prior week plans, daily records, full-period calendar, relevant tasks, named active lanes.
- `month`: current/prior month, recent weekly recaps, known deadlines, and relevant recurring patterns.
- `orient`: only the requested day, week, or named project and its linked records.
- `track`: current priorities, work table, log, remaining calendar, and read-only task state.
- `reflect`: raw journals first; older or migrated sources are supporting history, not current truth.

Do not reproduce source audits or connector dumps in the plan. Promote only facts that earn a place in the approved narrative, priorities, work table, parking lot, or log.
