---
description: |
  Review a stalled or in-progress project, make adjustments, and re-emit the
  runner command to continue execution.
---

## Resume & Adjust

Load shared controls:
- [[../_shared/nodes/interaction-gates.md]]
- [[../_shared/nodes/output-discipline.md]]
- [[safety.md]]

Reference: [[blueprint-schema.md]]

---

## Inputs

- Optional: path to `blueprint.json` (same locate logic as [[status.md]])

Assume the user may not know how `run` packages work yet. Briefly explain what is blocked and what changing the blueprint will do before making edits.

## Execution

1. **Run the shared status surface first**:
   - One-shot summary:
     ```bash
     run-workflow --status <path-to-blueprint.json>
     ```
   - Live follow, when the user wants to stay attached until terminal state:
     ```bash
     run-workflow --follow <path-to-blueprint.json>
     ```
   Use the shared surface as the source of truth instead of reconstructing status from `progress.md` by hand.
   If the run already terminated, also check `completion-summary.txt` in the run directory for the durable terminal report.

2. **Review blockers**:
   - Start with the rendered `Blocker:` and `Inspect next:` lines from `--status` or `--follow`.
   - If `blockers.jsonl` exists, review the latest unresolved lifecycle entries there first.
   - Fall back to `blockers.md` for older runs that do not have structured blocker history.
   - Present each unresolved blocker.
   - Ask: "Resolve, skip, or adjust the step?"
   - If resolve: ask for the resolution, then update step detail or status as needed.
   - If skip: set step status to `skipped`.
   - If adjust: modify the step title, detail, done condition, tool, or dependencies.

3. **Offer adjustments**:
   - After blocker review, ask whether any other changes are needed.
   - Supported changes: add steps, remove steps, skip steps, change tools, reword steps, or adjust dependencies.

4. **Apply changes**:
   - Write all modifications to `blueprint.json`.
   - Reset any `blocked` steps to `pending` if their blocker was resolved.

5. **Re-emit the launch package**:
   ```bash
   # Validate the updated package before launch
   run-workflow --validate <path>/blueprint.json

   # Standard: run the approved plan and stop on failure or blocker
   run-workflow --launch-mode standard <path>/blueprint.json

   # Adaptive: fixed scope, bounded blocker removal, restart on disruption or timeout
   run-workflow --launch-mode adaptive <path>/blueprint.json

   # Expansion: adaptive behavior plus bounded step creation during execution
   run-workflow --launch-mode expansion <path>/blueprint.json

   # Legacy supervised compatibility
   run-workflow --supervised <path>/blueprint.json

   # Watch mode
   run-workflow --watch <path>/blueprint.json
   ```

   Use the launch-mode ladder as the preferred handoff. Treat `--supervised` as legacy compatibility.
   If the run stopped in `Incomplete / Blocked`, describe the blocker in the same terms the shared status surface uses before proposing a resume path.
   Recommend the next command in plain English instead of only pasting the command block.

6. **Log to `progress.md`**:
   ```text
   ## Resume - <timestamp>
   Changes: <summary of what was adjusted>
   ```

7. **Re-attach to the shared supervision surface if needed**:
   ```bash
   run-workflow --follow <path-to-blueprint.json>
   ```

---

## Output Contract

- Updated `blueprint.json`
- Resume entry appended to `progress.md`
- Launch package presented with `--validate` plus `standard`, `adaptive`, and `expansion` commands
