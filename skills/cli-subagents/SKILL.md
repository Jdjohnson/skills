---
name: cli-subagents
description: Route bounded work to local Claude Code, Codex, Gemini, Grok Build, Cursor, or OpenCode CLI subagents through guarded wrappers. Use when a CLI agent, second-model pass, or supervised fast-model branch would improve a task; Cursor and OpenCode are explicit-only inactive nodes.
---

# CLI Subagents

Choose one node, give it a bounded job, and verify its output before using it. Keep the current agent as coordinator.

## Nodes

| Node | Status | Use it for |
|---|---|---|
| [Claude Code](nodes/claude-code.md) | Active quality anchor | Creativity, design, judgment, taste, personal issues, and ambiguous work |
| [Codex](nodes/codex.md) | Active primary | Daily work and difficult tasks where quality matters |
| [Gemini](nodes/gemini.md) | Active subordinate | Fast, inexpensive, vision-heavy, and high-volume work |
| [Grok Build](nodes/grok-build.md) | Active subordinate | Fast, affordable research and development |
| [Cursor](nodes/cursor.md) | Inactive | Explicit use only while access remains |
| [OpenCode](nodes/opencode.md) | Inactive | Explicit use only with a configured provider |

Read only the chosen node before delegating.

## Routing

1. Use Codex by default for hard work, implementation, and the daily-driver lane.
2. Use Claude Code when creativity, human judgment, design, taste, or sensitive personal reasoning is central.
3. Use Gemini for cheap, fast, multimodal work. Have Codex or Claude review consequential output.
4. Use Grok Build for quick research and development. Have Codex or Claude review consequential output.
5. Use Cursor or OpenCode only when the user names that CLI or explicitly approves the inactive node.

Use Medium effort by default for Claude, Codex, and Grok. Raise Claude or Codex to High when errors would be costly or the work depends on nuanced judgment. Do not treat higher effort as a substitute for narrower prompts and verification.

## Delegation

1. Keep the trusted working directory as narrow as possible.
2. Follow the active workspace's delegation and privacy rules. Never put credentials in prompts or arguments.
3. Run the node wrapper's `doctor` command.
4. Use `probe` when setup, authentication, or model access is uncertain.
5. Run one bounded task in `read`, `plan`, or `edit` mode. Use edit mode only when edits are authorized.
6. Inspect the wrapper receipt, response, artifacts, and project diff.
7. Verify material claims and changes independently. A successful CLI exit is not proof that the work is correct.

Do not let a delegate commit, push, publish, send messages, or change systems outside the trusted working directory unless the user separately authorizes that action.
