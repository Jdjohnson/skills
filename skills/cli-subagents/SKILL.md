---
name: cli-subagents
description: Route bounded work to locally available Claude Code, Codex, Gemini, Grok Build, Cursor, or OpenCode CLI agents through guarded wrappers. Use when a second model, separate context window, independent review, or supervised parallel branch would materially improve a task.
---

# CLI Subagents

Choose one locally available CLI, give it a bounded job, and verify its output before using it. Keep the current agent as coordinator.

## Nodes

| Node | Use it for |
|---|---|
| [Claude Code](nodes/claude-code.md) | A separate Anthropic coding and reasoning lane |
| [Codex](nodes/codex.md) | OpenAI coding, debugging, review, and implementation |
| [Gemini](nodes/gemini.md) | Multimodal work and Google's automatic model routing |
| [Grok Build](nodes/grok-build.md) | xAI research and development work |
| [Cursor](nodes/cursor.md) | Cursor's multi-model coding-agent harness |
| [OpenCode](nodes/opencode.md) | A provider-neutral harness with configured providers |

There is no maintainer-controlled on/off registry. A node is usable when its CLI is installed, authenticated, healthy, and suitable for the task. Run its `doctor` command before relying on it and `probe` when model or account access is uncertain.

## Current model selection

Provider catalogs change faster than this skill. Discover live availability instead of preserving a maintainer's old model choices:

- Claude Code: use its rolling `opus` or `sonnet` alias when a model must be named, or let the CLI use its configured default.
- Codex: let the CLI use its configured default unless the user names a model. For an explicit current OpenAI frontier lane, verify the current official model catalog first.
- Gemini: prefer the CLI's `auto` model routing unless the user requests a concrete model.
- Grok Build: inspect `grok models` and select the current Build/code model shown by the authenticated CLI.
- Cursor: inspect `agent models` or `agent --list-models`; prefer `Auto` unless the user requests a specific live model.
- OpenCode: run `opencode models --refresh` and select an available `provider/model` entry rather than guessing.

Never claim a model or paid tier is available merely because a CLI is installed.

## Routing

1. Match the task to the CLI's current capabilities, available model, account policy, and cost.
2. Respect an explicit user choice of CLI or model when it is available and safe.
3. When several nodes fit, choose the smallest useful independent lane and explain the choice briefly.
4. Do not route work solely to spend a subscription allowance or because a CLI happens to be installed.
5. Use higher reasoning effort only when the task warrants it; narrow prompts and verification still matter more.

## Task packet

Before `run`, provide the goal, mode, acceptance checks, relevant paths, required context, and exact mutation boundary. The working directory may provide file access, but the prompt must still be sufficient.

Do not put credentials in prompts or arguments. Apply the active workspace's privacy and delegation rules; the public skill does not grant any provider standing access to private, financial, personnel, or company-sensitive material.

## Delegation

1. Read the chosen node.
2. Keep the working directory as narrow as practical.
3. Run the wrapper's `doctor` command.
4. Use `probe` when authentication, account tier, or requested model access is uncertain.
5. Run one bounded task in `read`, `plan`, or `edit` mode. Use edit only when edits are authorized.
6. Inspect the wrapper result, artifacts, and project diff.
7. Verify material claims and changes independently.

Do not let a delegate commit, push, publish, send messages, deploy, purchase, or change systems outside the trusted working directory unless the user separately authorizes that action.

## Results

Prefer the wrapper's machine-readable result or last-message output. Receipts may include the prompt, stdout, stderr, metadata, and before/after Git status. Read them as evidence, not proof of correctness.

`audit-prompt` and `--data-classification` are compatibility metadata only. They do not inspect, sanitize, or block task content.
