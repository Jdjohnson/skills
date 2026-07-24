# Claude Code

**Status:** Active quality anchor
**Default:** `fable`, Medium effort
**Escalate:** High effort for consequential creative, personal, design, judgment, or taste work

## Route here

Use Fable for creativity, personal issues, design, judgment, taste, ambiguous root-cause work, architecture, deep research, and long tasks where investigation and verification matter. This is a personal routing preference: Anthropic also positions Fable for demanding reasoning, long-horizon agents, ambitious coding, migrations, and vision-heavy documents.

Fable's exact model ID is `claude-fable-5`; Claude Code accepts the `fable` alias. The wrapper intentionally defaults to Medium even though Anthropic's general Fable default is High. Fable availability and usage credits depend on the account.

## Run

```bash
python3 <skill-root>/scripts/claude_delegate.py doctor --cwd /path/to/project
python3 <skill-root>/scripts/claude_delegate.py probe --cwd /path/to/project --model fable --effort medium
python3 <skill-root>/scripts/claude_delegate.py run --cwd /path/to/project --mode plan --model fable --effort medium --prompt-file /path/to/prompt.md
```

Raise to `--effort high` when nuance or quality matters. The wrapper uses headless output, bounded turns, a narrow tool set, and safe mode by default.

## Sources

- [Claude Code model configuration](https://code.claude.com/docs/en/model-config)
- [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference)
- [Fable 5](https://www.anthropic.com/claude/fable)
