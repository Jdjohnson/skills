---
name: jj-log
description: Summarize and log an active work thread only to the explicit Dot Today file, the explicit ad hoc Codex memory-note folder, and an explicit Asana task URL or gid when present. Use only when the user explicitly invokes `$jj-log`, says `use jj-log`, or gives an unambiguous close-out/sweep command for the current thread; never trigger automatically or infer intent from ordinary status updates.
---

# JJ Log

Close out the active work thread by recording only the useful outcomes, decisions,
deadlines, dependencies, and next actions in the explicit surfaces named below.

## Invocation Gate

- Run only after an explicit user command such as `$jj-log`, `use jj-log`, or `close out this thread`.
- Never run automatically, in the background, or because a thread merely appears finished.
- If the command is ambiguous, stop and ask whether the user wants a thread closeout.
- Treat invocation as permission to touch only the allowed surfaces below for the current thread. It is not permission to send email, publish, search for tasks, complete tasks, or mutate anything unnamed here.

## Allowed Surfaces

Read these local Dot files before writing:

- `/Users/jaradjohnson/Dot/AGENTS.md`
- `/Users/jaradjohnson/Dot/ASSISTANT.md`
- `/Users/jaradjohnson/Dot/MEMORY.md`
- `/Users/jaradjohnson/Dot/ROUTES.md`

Write only these targets:

- Today file: the exact relative path on the `**Today**:` line in `/Users/jaradjohnson/Dot/MEMORY.md`, resolved under `/Users/jaradjohnson/Dot/`.
- Ad hoc memory note: one new file under `/Users/jaradjohnson/.codex/memories/extensions/ad_hoc/notes/`, only when current system instructions explicitly allow memory updates and the fact is useful beyond today.
- Asana: one task explicitly named in the current thread by Asana URL or Asana gid.

If a target is not listed in this section, skip it and report that it was not an allowed surface.

## Setup

1. Load the four local Dot files listed in Allowed Surfaces.
2. Check onboarding state as normal Dot work requires.
3. Use only the `**Today**:` line in `/Users/jaradjohnson/Dot/MEMORY.md` to identify the Today file. If that line is missing or ambiguous, ask before writing.
4. Do not discover alternate write paths.
5. Do not discover, search, or infer Asana tasks. Use Asana only when the current thread contains an explicit Asana URL or gid.

## Thread Review

Extract a concise, source-backed closeout set:

- Achievements and shipped artifacts.
- Decisions made or confirmed.
- New deadlines, date changes, timeline shifts, or dependencies.
- Open follow-ups and next actions, with owners when known.
- Blockers, skipped items, approvals still needed, or systems intentionally not touched.

Use exact dates for relative deadlines. Do not invent owners, dates, commitments, task IDs, or external actions.

## Update Targets

### Daily File

- Add a short status bullet under `## Progress log` when that section exists in the explicit Today file; create `## Progress log` only in that same file if it has no suitable progress area.
- Update an existing task row when the thread clearly changes the status, due date, owner, or next action.
- Preserve the existing day structure and surrounding notes. Do not rewrite raw journal/source material.
- Include links or paths only when they help future re-entry.

### Ad Hoc Memory Note

- Create at most one short note under `/Users/jaradjohnson/.codex/memories/extensions/ad_hoc/notes/`.
- Use this only when current system instructions explicitly allow memory updates and the fact will help future continuity.
- Do not edit `/Users/jaradjohnson/Dot/MEMORY.md`, `/Users/jaradjohnson/.codex/memories/MEMORY.md`, rollout summaries, or memory sweep files.
- If the exact ad hoc note folder is unavailable or not writable, skip it and report the skip.

### Asana

- Use Asana only when the current thread includes a specific Asana task URL or gid.
- Add a progress comment only to that explicit task when the comment would help the task owner understand the closeout.
- Update that explicit task's due date only when the thread explicitly created or changed a deadline.
- Add subtasks only to that explicit task and only for new, concrete follow-ups that are clearly connected to it.
- Do not create, complete, reassign, delete, or reorganize Asana tasks unless the user explicitly asks.
- If the target task, wording, owner, or deadline is unclear, ask before mutating Asana.
- Do not search Asana to infer a task.

## Off-Limits

- Do not update project, sales, meeting, resource, `source/`, `human/`, `HUMAN.md`, `dot-runtime/`, `.dot-core/`, `.dot-addons/`, Google Drive, Gmail, Superhuman, Slack, Calendar, Figma, GitHub, Harvest, or any unnamed connector.
- Do not edit generated Dot Core files, installed add-ons, or product-managed skill surfaces.
- Do not rewrite raw source material or human-owned material.
- Do not run a full memory sweep, deterministic memory refresh, or automation closeout unless the user explicitly requested that exact sweep.
- Do not broaden the closeout to adjacent threads or stale tasks just because they are visible.

## Completion Report

End with a brief receipt:

- Today file path written, or `skipped` with the reason.
- Ad hoc memory note path created, or `skipped` with the reason.
- Asana task URL or gid updated, or `skipped` with the reason.
- Remaining follow-ups, blockers, or clarifications.

Keep the report short. The closeout should make future re-entry easier, not create a long artifact to read.
