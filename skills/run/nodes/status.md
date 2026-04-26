---
description: |
  Status and live-follow surface for a running or completed project. Uses the
  runner's artifact-backed shell entrypoint instead of building a separate
  dashboard in the node.
---

## Status & Follow

Load shared controls:
- [[../_shared/nodes/interaction-gates.md]]
- [[../_shared/nodes/output-discipline.md]]

Reference: [[blueprint-schema.md]]

---

## Inputs

- Optional: path to `blueprint.json` or a run directory containing it
- Optional intent: one-shot status summary or live follow

Assume the user may be seeing these artifacts for the first time. Explain the current state in plain language before leaning on internal file names.

## Execution

1. **Locate the run**:
   - If the user supplied a path, use it.
   - If not, search `./runs/**/blueprint.json`.
   - If multiple blueprints are plausible, list them and ask the user to choose.
   - If one blueprint is found, use it.

2. **Use the shared runner surface**:
   - One-shot summary:
     ```bash
     run-workflow --status <path-to-blueprint.json>
     ```
   - Live follow until terminal state:
     ```bash
     run-workflow --follow <path-to-blueprint.json>
     ```
   - In Codex, use `--follow` from an attached shell session when you are actively supervising the run.
   - In Claude Code, use the same shell surface even if the UI also shows background activity.

3. **Interpret the output from runner artifacts**:
   - The shared surface reads `run-state.json`, `events.jsonl`, `blockers.jsonl`, and step attempt logs first.
   - For older run directories, it degrades gracefully to `progress.md` and `blockers.md`.
   - Treat the artifact-backed fields as canonical. Do not rebuild a separate status model from `progress.md` if the structured artifacts exist.
   - Expect the rendered surface to call out the active attempt budget, recovery state, latest blocker, and `Inspect next` artifact when those signals exist.
   - `Recovering` means the runner is still trying to self-heal inside the configured bounded recovery path.
   - `Incomplete / Blocked` or exhausted attempt/recovery language means the run has stopped and needs a human decision before continuing.
   - `Completed Cleanly` and `Completed With Skips` are the terminal outcome labels to repeat back.
   - The live follow mode stops cleanly when the run reaches a terminal state instead of tailing forever.
   - Terminal runs also persist the same outcome summary to `completion-summary.txt` and a recap-ready artifact to `completion-recap.md` in the run directory.
   - When the recap artifact exists, the shared surface should point `Inspect next` at `completion-recap.md`; use that as the first read when someone needs a finished-run recap.

4. **Stay read-only**:
   - Do not edit the blueprint or run artifacts from `status`.
   - If the user asks what to do next, answer from the rendered state rather than inventing a second status model.
   - If technical file names appear in the output, translate them into user-facing meaning.

---

## Output Contract

- The runner's shared status or follow output, relayed in user-facing language
- No file modifications
