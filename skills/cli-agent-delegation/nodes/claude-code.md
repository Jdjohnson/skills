# Claude Code

Use Claude Code when an independent Anthropic coding, review, research, or judgment pass fits the task.

## Model selection

Omit `--model` to use the authenticated CLI's configured default. If the user requests a model, verify that the current account exposes it before the real run; prefer a live rolling alias over a dated ID when the CLI supports one.

## Run

```bash
python3 <skill-root>/scripts/claude_delegate.py doctor --cwd /path/to/project
python3 <skill-root>/scripts/claude_delegate.py probe --cwd /path/to/project
python3 <skill-root>/scripts/claude_delegate.py run --cwd /path/to/project --mode plan --prompt-file /path/to/prompt.md
```

The wrapper uses headless output and bounded turns. Keep the task packet complete even when the repository has `CLAUDE.md` instructions.

## Sources

- [Claude Code model configuration](https://docs.anthropic.com/en/docs/claude-code/model-config)
- [Claude Code CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-usage)
