---
name: claude-code
description: Delegate bounded review, planning, and explicitly approved editing to a local Claude Code CLI through a guarded wrapper. Use when a second-agent pass would improve a repository task and the local Claude CLI is installed.
---

# Claude Code

Use the bundled wrapper to create a narrow, auditable delegation. Default to read or plan mode. Use edit mode only when the user has authorized file changes.

## Workflow

1. Run readiness checks:
   `python3 <skill-root>/scripts/claude_delegate.py doctor --cwd /path/to/project`
2. When useful, run the non-mutating probe:
   `python3 <skill-root>/scripts/claude_delegate.py probe --cwd /path/to/project`
3. Audit prompts that may contain sensitive data:
   `python3 <skill-root>/scripts/claude_delegate.py audit-prompt --prompt-file /path/to/prompt.md`
4. Delegate with one prompt source:
   `python3 <skill-root>/scripts/claude_delegate.py run --cwd /path/to/project --mode read --prompt-file /path/to/prompt.md`
5. Inspect the JSON receipt, response text, and artifact paths before reporting the result.

The default model alias is `opus`. Safe mode isolates the run from user customizations; use `--no-safe-mode` only when the task intentionally needs them.

## Boundaries

- Keep the trusted working directory as narrow as possible.
- Do not delegate private source packages or raw client exports unless the user explicitly accepts that boundary and the wrapper supports the requested waiver.
- Never put credentials in prompts, files, or command arguments.
- A timeout or nonzero exit is not a completed delegation.
- The delegate must not commit, push, publish, or make unrelated changes.
- Preserve the exact distinction between findings, proposed edits, actual edits, and verified results.
