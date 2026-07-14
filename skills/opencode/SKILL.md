---
name: opencode
description: Delegate bounded review, planning, and explicitly approved editing to a local OpenCode CLI through a guarded wrapper. Use when an OpenCode second-agent pass would improve a repository task and the local CLI is installed.
---

# OpenCode

Use the bundled wrapper for narrow, auditable delegation. Default to read or plan mode; use edit mode only for authorized file changes.

## Workflow

1. Check readiness:
   `python3 <skill-root>/scripts/opencode_delegate.py doctor --cwd /path/to/project`
2. Run an optional probe:
   `python3 <skill-root>/scripts/opencode_delegate.py probe --cwd /path/to/project`
3. Audit sensitive prompts:
   `python3 <skill-root>/scripts/opencode_delegate.py audit-prompt --prompt-file /path/to/prompt.md`
4. Delegate:
   `python3 <skill-root>/scripts/opencode_delegate.py run --cwd /path/to/project --mode read --prompt-file /path/to/prompt.md`
5. Inspect the JSON receipt and artifacts.

The default model is `ollama-cloud/glm-5.2`. Override it only when the task calls for another installed model.

## Boundaries

- Keep the trusted working directory narrow.
- Never include credentials in prompts, files, or command arguments.
- Treat private-data audit failures as blocked.
- A timeout, provider error, or nonzero exit is not completion.
- Do not permit commits, pushes, publication, dependency changes, or unrelated edits.
