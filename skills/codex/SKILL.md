---
name: codex
description: Delegate bounded review, planning, and explicitly approved editing to a local Codex CLI through a guarded wrapper. Use when a second Codex pass would improve a repository task and the local Codex CLI is installed.
---

# Codex

Use the bundled wrapper for a narrow, auditable second-agent pass. Default to `read` or `plan`; use `edit` only for approved file changes.

## Workflow

1. Check readiness:
   `python3 <skill-root>/scripts/codex_delegate.py doctor --cwd /path/to/project`
2. Run an optional non-mutating probe:
   `python3 <skill-root>/scripts/codex_delegate.py probe --cwd /path/to/project`
3. Audit sensitive prompts:
   `python3 <skill-root>/scripts/codex_delegate.py audit-prompt --prompt-file /path/to/prompt.md`
4. Run one bounded delegation:
   `python3 <skill-root>/scripts/codex_delegate.py run --cwd /path/to/project --mode read --prompt-file /path/to/prompt.md`
5. Inspect the JSON receipt and saved artifacts before reporting completion.

The wrapper defaults to `gpt-5.5` with high reasoning effort. Override the model or effort only when the task requires it. `--allow-private-data` and `--full-access` are exceptional controls: use them only after explicit user authorization and surface them in the receipt.

## Boundaries

- Keep the trusted working directory narrow.
- Never include credentials in prompts, files, or arguments.
- Treat private-data findings as blocked unless explicitly waived.
- A timeout, malformed response, or nonzero exit is not success.
- Do not let the delegate commit, push, publish, install dependencies, or touch unrelated files.
- Verify edits independently before relying on them.
