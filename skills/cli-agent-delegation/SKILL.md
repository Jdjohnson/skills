---
name: cli-agent-delegation
description: Delegate bounded work to an installed local coding-agent CLI when a separate context, provider, or independent review would materially help. Includes guarded wrappers for discovery, read, plan, and authorized edit runs.
---

# CLI Agent Delegation

Use one suitable local CLI as a bounded delegate while the current agent remains responsible for scope and verification.

## Providers

| CLI | Guidance |
|---|---|
| Claude Code | [nodes/claude-code.md](nodes/claude-code.md) |
| Codex | [nodes/codex.md](nodes/codex.md) |
| Gemini | [nodes/gemini.md](nodes/gemini.md) |
| Grok Build | [nodes/grok-build.md](nodes/grok-build.md) |
| Cursor | [nodes/cursor.md](nodes/cursor.md) |
| OpenCode | [nodes/opencode.md](nodes/opencode.md) |

A provider is usable only when its CLI is installed, authenticated, healthy, and appropriate for the task. Discover live model access; do not infer it from installation or preserve dated model IDs. Respect the user's provider or model choice when available and safe.

## Delegate

1. Choose the smallest useful independent lane and read its provider guidance.
2. Build a self-contained task packet: goal, mode, acceptance checks, relevant paths and context, mutation boundary, prohibited actions, and desired result format.
3. Keep the working directory narrow. Run `doctor`, then `probe` when authentication or model access is uncertain.
4. Run one bounded `read`, `plan`, or authorized `edit` task. A task request does not authorize commit, push, publish, deploy, send, purchase, or changes outside the trusted working directory.
5. Inspect the structured result, artifacts, and repository diff. Treat receipts as evidence, not correctness proof.
6. Verify material claims and edits independently before using them.

## Safety

- Never place credentials in prompts or arguments. Follow the active workspace's data and provider policy.
- Use edit mode only when edits are authorized. Do not broaden sandboxes merely to bypass a failure.
- Stop on ambiguous provider output, unexpected changes, missing result content, or an unverified model/account claim.
- Wrapper artifacts may contain private task context. Keep them local, access-controlled, and subject to the workspace's retention policy.
