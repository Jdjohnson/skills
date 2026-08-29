---
name: manus-api
description: Delegate bounded, credit-spending work through the Manus v2 API, then inspect, continue, or stop the task with redacted receipts. Use for sustained web, research, artifact, or batch work that benefits from an external agent.
---

# Manus API

Resolve `<skill-root>` to this skill's installed folder and use its `scripts/manus_delegate.py`; do not recreate API calls. It keeps tasks private by default, checks credits, classifies failures, and stores redacted receipts under `<cwd>/.tmp/manus/`.

## Run a task

Use an explicit, bounded working directory. Never use a home directory, filesystem root, or broad user directory.

```bash
python3 <skill-root>/scripts/manus_delegate.py doctor --cwd /path/to/project
python3 <skill-root>/scripts/manus_delegate.py run --cwd /path/to/project --prompt-file /path/to/prompt.md
```

`doctor` checks the credential and authoritative spendable balance. The wrapper reads `MANUS_API_KEY` from the environment, `--env-file`, `MANUS_ENV_PATH`, or `.env.local` between the working directory and home. Never print the key or ask the user to paste it into chat.

`run` submits asynchronously unless `--wait` is supplied. A successful receipt proves submission, not completion. Use the returned task ID:

```bash
python3 <skill-root>/scripts/manus_delegate.py status TASK_ID --cwd /path/to/project
python3 <skill-root>/scripts/manus_delegate.py messages TASK_ID --cwd /path/to/project
python3 <skill-root>/scripts/manus_delegate.py follow-up TASK_ID --cwd /path/to/project --prompt-file /path/to/follow-up.md
python3 <skill-root>/scripts/manus_delegate.py stop TASK_ID --cwd /path/to/project
```

Use `probe` only for first setup or an API-change smoke test. Set a different profile with `--profile` or `MANUS_DEFAULT_PROFILE` only when the task or current API requires it.

## Boundaries

- Check spendable credits before a new task. Make extra-cost profile choices explicit.
- Keep `share_visibility=private` unless the user explicitly requests a wider scope.
- Enable connectors or Manus skills only when the task requires them.
- Task submission and necessary task-scoped follow-ups do not authorize deployment, purchase, account access, messaging, or another external action.
- Treat `waiting` as a question or approval boundary. Answer an ordinary task question; obtain user approval before confirming a sensitive external action.
- Use bounded waits and provide progress during a long foreground wait.
- Stop when the user asks or the task is clearly runaway; confirm the stopped state through readback.
- Require terminal state plus output evidence before reporting completion.

Inspect `ok`, `status`, `failure_kind`, `issues`, `credits`, `task`, `messages`, and `artifacts`. Receipts must not contain the API key or raw submitted prompt.
