# Local Agent CLI Skill Downloads

These zip files package the local-agent CLI skills as individual downloads.
Each archive contains one `skills/<name>/` folder with its `SKILL.md`, helper
script, agent metadata, and tests.

| Skill | Download | Source |
|---|---|---|
| Claude Code | [claude-code-skill.zip](./claude-code-skill.zip) | [skills/claude-code](../../skills/claude-code/SKILL.md) |
| Codex | [codex-skill.zip](./codex-skill.zip) | [skills/codex](../../skills/codex/SKILL.md) |
| Grok Build | [grok-build-skill.zip](./grok-build-skill.zip) | [skills/grok-build](../../skills/grok-build/SKILL.md) |
| OpenCode | [opencode-skill.zip](./opencode-skill.zip) | [skills/opencode](../../skills/opencode/SKILL.md) |

Regenerate these packages from the repo root with:

```bash
python3 .maintainer/package_cli_skills.py
```
