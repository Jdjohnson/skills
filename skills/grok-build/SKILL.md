---
name: grok-build
description: Delegate bounded review, planning, and explicitly approved editing to a local Grok CLI through a guarded wrapper. Use when a Grok second-agent pass would improve a repository task and the local CLI is installed.
---

# Grok Build

Use the bundled wrapper to make a narrow, auditable delegation. Default to read or plan mode. Use edit or trusted modes only when their broader permissions are explicitly justified.

## Workflow

1. Check readiness:
   `python3 <skill-root>/scripts/grok_delegate.py doctor --cwd /path/to/project`
2. Run an optional non-mutating probe:
   `python3 <skill-root>/scripts/grok_delegate.py probe --cwd /path/to/project`
3. Audit a prompt:
   `python3 <skill-root>/scripts/grok_delegate.py audit-prompt --prompt-file /path/to/prompt.md`
4. Delegate:
   `python3 <skill-root>/scripts/grok_delegate.py run --cwd /path/to/project --mode read --prompt-file /path/to/prompt.md`
5. Inspect the JSON receipt and artifacts.

The default model is `grok-4.5`. The public compatibility interface is `--compat host-only|all|none`; `host-only` is the safe default and disables compatibility imports from other agent hosts.

## Boundaries

- Keep the working directory narrow and the prompt explicit.
- Keep MCP, web access, subagents, and compatibility imports off unless the task needs them.
- Never include credentials or raw private source packages.
- A timeout or nonzero exit is not success.
- Do not permit commits, pushes, publication, or unrelated edits.
