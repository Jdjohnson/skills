---
name: run
version: 1.0.0
description: |
  Plan and run larger projects through a guided session, a structured
  blueprint, and a portable runner. Use when the work is too large or fuzzy
  for a single prompt and needs clear steps, tool routing, status checks, and
  resume support.
argument-hint: "[session | status | resume]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# /run - Plan, Launch, and Supervise Bigger Work

`run` is for work that should be treated like a small project, not a one-off prompt.

`run` is a portable workflow runner for AI tools, distributed as a skill for Codex and Claude Code.

Use it when you want to:

- turn a rough goal into an executable plan
- break the work into steps with dependencies
- assign the right tool to each step
- launch the work in a controlled way
- inspect progress and recover from blockers

The `run` planner handles the planning layer. The `run-workflow` CLI handles execution and supervision. `run-skill` remains available as a legacy compatibility alias.

---

## Mode Routing

| Mode | Trigger | When | Node |
|------|---------|------|------|
| `session` | `/run` or `/run session` | Shape a high-trust, launch-ready run package | [[nodes/session.md]] |
| `status` | `/run status` | Check progress on a running project | [[nodes/status.md]] |
| `resume` | `/run resume` | Adjust and continue a stalled project | [[nodes/resume.md]] |

Default mode: `session`.

---

## What To Expect

When you start with `/run` or `$run`, the planner will usually:

1. clarify the goal, scope, and success criteria
2. propose a run folder, usually under `./runs/<project-slug>/`
3. write a human-readable planning record in `session.md`
4. lock the structured execution contract into `blueprint.json`
5. initialize `progress.md`
6. hand you the exact commands to validate and launch the run

The planner does not auto-launch the work. It stops at a launch-ready package unless you choose to run it separately.

---

## Core Rules

1. Load shared controls first:
   - [[_shared/nodes/interaction-gates.md]]
   - [[_shared/nodes/output-discipline.md]]
   - [[nodes/safety.md]]
2. Determine mode from the command argument. No argument means `session`.
3. Use [[nodes/blueprint-schema.md]] as the source of truth for `blueprint.json`.
4. Keep the output user-facing and practical. Assume the person using this workflow is seeing it for the first time unless the conversation says otherwise.

---

## Runner Commands

After `session` or `resume` writes or updates `blueprint.json`, present these commands:

**Validate the package**
```bash
run-workflow --validate <path-to-blueprint.json>
```

**See a one-shot status summary**
```bash
run-workflow --status <path-to-blueprint.json>
```

**Follow the run live**
```bash
run-workflow --follow <path-to-blueprint.json>
```

`--follow` polls every 2 seconds by default. Override with `RUN_STATUS_POLL_SECONDS=<seconds>` when needed.

**Standard launch mode**
```bash
run-workflow --launch-mode standard <path-to-blueprint.json>
```

**Adaptive launch mode**
```bash
run-workflow --launch-mode adaptive <path-to-blueprint.json>
```

**Expansion launch mode**
```bash
run-workflow --launch-mode expansion <path-to-blueprint.json>
```

**Legacy supervised compatibility**
```bash
run-workflow --supervised <path-to-blueprint.json>
```

**Resume last blueprint path**
```bash
run-workflow --resume-last
```

**Watch mode**
```bash
run-workflow --watch <path-to-blueprint.json>
```

**Dry run**
```bash
run-workflow --dry-run <path-to-blueprint.json>
```

**Autonomy profile override**
```bash
run-workflow --autonomy-profile max <path-to-blueprint.json>
```

**Codex service-tier override**
```bash
run-workflow --codex-service-tier fast <path-to-blueprint.json>
```

The shared operator contract for both Codex and Claude Code is `run-workflow --status` and `run-workflow --follow`. They read `run-state.json`, `events.jsonl`, `blockers.jsonl`, and step attempt logs first, then fall back to `progress.md` and `blockers.md` for older run directories.

When a run reaches terminal state, the runner writes both `completion-summary.txt` and `completion-recap.md` in the run directory. `completion-summary.txt` is the durable terminal snapshot. `completion-recap.md` is the operator-facing recap artifact to read first before briefing someone on the outcome.

Model defaults:
- Claude Code: `claude-opus-4-5`
- Codex: `gpt-5.4` with `xhigh` reasoning effort

Override those in `blueprint.json` with `defaults.models.*` or step-level fields.

---

## Mental Model

Think of the system in four pieces:

- `session.md`: the human planning record
- `blueprint.json`: the execution contract
- `progress.md`: the running log
- `run-workflow`: the operator that executes and supervises the plan

If the user is new, explain the workflow in those terms instead of assuming prior knowledge.

---

## Node Map

- [[nodes/blueprint-schema.md]]
- [[nodes/safety.md]]
- [[nodes/session.md]]
- [[nodes/status.md]]
- [[nodes/resume.md]]

## Shared Dependencies

- [[_shared/nodes/interaction-gates.md]]
- [[_shared/nodes/output-discipline.md]]
