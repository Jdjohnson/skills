# Runner Handoff

After `session`, `harden`, or `resume` writes or updates `blueprint.json`, hand back the smallest useful command set:

```bash
run-workflow --validate <path-to-blueprint.json>
run-workflow --status <path-to-blueprint.json>
run-workflow --follow <path-to-blueprint.json>
run-workflow --launch-mode <recommended-mode> <path-to-blueprint.json>
```

Default to exactly one recommended launch command. Mention alternate launch modes only when the recommendation is genuinely close or the user asks.

## Launch Modes

- `standard`: run the approved plan and stop on failure or blocker
- `adaptive`: fixed scope, bounded blocker removal, restart on disruption or timeout
- `expansion`: adaptive behavior plus bounded step creation during execution

Keep `--supervised`, `--watch`, `--dry-run`, `--resume-last`, `--autonomy-profile`, and `--codex-service-tier` as compatibility or advanced options, not the default handoff.

## Shared Operator Contract

- `--status` and `--follow` read `run-state.json`, `events.jsonl`, `blockers.jsonl`, and step attempt logs first.
- For older run directories, they fall back to `progress.md` and `blockers.md`.
- Terminal runs write `completion-summary.txt` and `completion-recap.md`.
- When `completion-recap.md` exists, read it first before briefing someone on the finished run.
- `Completed Cleanly`, `Completed With Friction`, `Completed With Skips`, and `Incomplete / Blocked` are the terminal outcome labels to repeat back.
- `Completed With Friction` means the run finished successfully after retries, recovery, rerouting, or another bounded intervention; include the `Completion notes:` line when present.
