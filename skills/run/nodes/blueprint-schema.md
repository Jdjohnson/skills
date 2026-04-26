---
description: |
  Single source of truth for blueprint.json structure. Referenced by all nodes
  and the runner script. Any schema changes happen here first.
---

## Blueprint Schema

Every `run` project is written to its own run directory. The core file in that directory is `blueprint.json`.

Typical home:
- `./runs/<project>/`

If you are new to the system, think of `blueprint.json` as the machine-readable version of the plan. The `/run` planner helps generate it. The workflow runner reads it to execute the work.

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Short project name (slug-friendly) |
| `goal` | string | yes | One-sentence outcome statement |
| `created` | string | yes | ISO 8601 timestamp |
| `context` | string | yes | Rich project briefing - background, constraints, relevant files, and anything the runner needs to understand the project |
| `defaults` | object | yes | Project-level defaults |
| `steps` | array | yes | Ordered list of execution steps |

### `defaults` Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tool` | string | yes | Fallback tool when a step does not specify one |
| `skill_runner` | string | no | CLI runner for `skill:*` steps (default: `"claude-code"`) |
| `timeout` | integer | no | Per-step timeout in seconds (default: `1200`). `0` means no timeout. |
| `max_retries` | integer | no | Max retries on timeout or failure (default: `2`). `0` means no retry. |
| `autonomy_profile` | string | no | Execution envelope: `safe`, `balanced`, or `max` |
| `auto_resolve_attempts` | integer | no | Auto-recovery attempts before hard block (default: `2`) |
| `enable_dynamic_steps` | bool | no | Allow step output to append follow-up steps via patch markers (default: `true`; launch mode may override) |
| `network_domains` | array | no | Optional domains for network preflight DNS checks |
| `gate_profile` | string | no | Built-in quality gate profile: `lint`, `tests`, or `review-ready` |
| `gate_strict` | boolean | no | Default gate behavior. `true` blocks the step on gate failure, `false` warns and continues |
| `gate_retry_max` | integer | no | Number of remediation reruns allowed after a strict gate failure |
| `gate_commands.*` | object | no | Optional command overrides for built-in gates |
| `models.claude_code` | string | no | Default Claude model for `claude-code` runs |
| `models.codex` | string | no | Default Codex model for `codex` runs |
| `models.codex_reasoning_effort` | string | no | Default Codex reasoning effort (`none|minimal|low|medium|high|xhigh`) |
| `models.codex_service_tier` | string | no | Default Codex service tier (`fast`) |
| `claude_model` | string | no | Legacy shorthand for `models.claude_code` |
| `codex_model` | string | no | Legacy shorthand for `models.codex` |
| `codex_reasoning_effort` | string | no | Legacy shorthand for `models.codex_reasoning_effort` |
| `codex_service_tier` | string | no | Legacy shorthand for `models.codex_service_tier` |

### `steps[]` Array Items

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique step identifier (for example `step-01`) |
| `title` | string | yes | Short action title |
| `detail` | string | yes | Full instructions for the AI tool - what to do, where, and acceptance criteria |
| `done_when` | string | yes | How the runner knows this step succeeded |
| `tool` | string | no | Override tool for this step (falls back to `defaults.tool`) |
| `depends` | array | no | List of step `id`s that must be `done` before this step can start |
| `status` | string | yes | One of: `pending`, `in_progress`, `done`, `blocked`, `skipped` |
| `timeout` | integer | no | Per-step timeout override in seconds |
| `max_retries` | integer | no | Per-step retry override |
| `fallback_tool` | string | no | Tool used by auto-recovery when primary execution fails |
| `on_blocked` | string | no | Block handling policy: `auto_repair`, `block`, or `skip` |
| `capabilities` | array | no | Optional capability hints for preflight or routing (for example `network`, `external_fs`, `git_push`, `browser`) |
| `network_domains` | array | no | Optional per-step domains for DNS preflight checks |
| `external_paths` | array | no | Optional external paths requiring write access |
| `acceptance.files_required` | array | no | File paths that must exist before the step can be marked done |
| `acceptance.commands` | array | no | Commands that must exit `0` before the step can be marked done |
| `acceptance.execution_root` | string | no | Directory root for `acceptance.commands`: `"project"`, `"repo"`, an absolute path, or a relative path resolved from the project directory |
| `gate_profile` | string | no | Per-step built-in gate profile override |
| `gate_strict` | boolean | no | Per-step strict or warn override for quality gates |
| `gate_retry_max` | integer | no | Per-step gate remediation retry override |
| `model` | string | no | Step-level model override |
| `claude_model` | string | no | Step-level model override for `claude-code` |
| `codex_model` | string | no | Step-level model override for `codex` |
| `reasoning_effort` | string | no | Step-level Codex reasoning effort override |
| `codex_reasoning_effort` | string | no | Step-level Codex reasoning effort override |
| `codex_service_tier` | string | no | Step-level Codex service tier override (`fast`) |
| `_attempts` | integer | no | Runner-managed. Current attempt count. Do not set manually. |
| `_recovery_attempts` | integer | no | Runner-managed. Recovery attempts used for this step. Do not set manually. |
| `_last_failure` | string | no | Runner-managed. Structured failure memory for retry or recovery context. Do not set manually. |

### Status Values

- `pending` - Not yet started. Eligible to run if all `depends` are `done`.
- `in_progress` - Currently being executed by the runner.
- `done` - Completed successfully.
- `blocked` - The tool reported a blocker.
- `skipped` - Skipped by user choice or watch-mode decision.

### Tool Mapping

| Tool value | CLI command | Notes |
|------------|-------------|-------|
| `claude-code` | `claude -p ... --model ... --allowedTools ...` | Autonomy-profile aware |
| `codex` | `codex exec -m ... -c model_reasoning_effort=... [-c service_tier=fast] ...` | Autonomy-profile aware |
| `gemini` | `gemini -p "$prompt" -y` | Auto-approve mode |
| `skill:<name>` | Routes to `defaults.skill_runner` CLI | Prepends `Read and follow <skill>/SKILL.md.` to the prompt |
| `skill:<name>:<runner>` | Routes to specified `<runner>` CLI | Same as above but overrides the default skill runner for this step |

### Skills as Tools

Steps can invoke installed skills by using `skill:<name>` in the `tool` field. The runner:

1. Validates that a matching `SKILL.md` exists in one of its configured skill roots.
2. Extracts `allowed-tools` from the SKILL front matter for Claude Code's `--allowedTools` flag.
3. Builds a skill-specific prompt that loads the skill file instead of the full project context.
4. Routes to the CLI runner specified by `defaults.skill_runner` or the explicit `:<runner>` suffix.

Skill lookup order:
1. bundled repo-local `skills/<name>/SKILL.md`
2. extra roots from `RUN_WORKFLOW_PATHS`
3. legacy extra roots from `RUN_SKILL_PATHS`
4. `~/.codex/skills/<name>/SKILL.md`
5. `~/.claude/skills/<name>/SKILL.md`

### Acceptance Execution Roots

- Omit `acceptance.execution_root` to preserve the default of running acceptance commands from the project directory.
- Set `"project"` to run acceptance commands from the blueprint's project directory.
- Set `"repo"` to run acceptance commands from the runner repo root.
- Set an absolute path to use that directory directly.
- Set a relative path to resolve it from the project directory.

### Companion Files

These are created in the same directory as `blueprint.json`:

- `progress.md` - Append-only log of step outcomes
- `launch.json` - Launch receipt capturing the blueprint hash, chosen launch mode, and runtime policy
- `events.jsonl` - Structured machine events
- `run-state.json` - Latest checkpoint state for resume or supervision
- `blockers.md` - Human-readable blocker log
- `blockers.jsonl` - Structured blocker lifecycle log
- `completion-summary.txt` - Durable terminal summary written at run end
- `completion-recap.md` - Durable terminal recap assembled from the terminal snapshot plus handoff notes
- `handoff/` - Step continuity notes written after successful completion or recovery
- `logs/steps/<step-id>/attempt-<n>.log` - Full raw output per attempt for debugging and recovery

Shared operator surface:

```bash
run-workflow --status <path-to-blueprint.json>
run-workflow --follow <path-to-blueprint.json>
```

The shared surface reads `run-state.json`, `events.jsonl`, `blockers.jsonl`, and step attempt logs first. For older run directories, it falls back to `progress.md` and `blockers.md`.
