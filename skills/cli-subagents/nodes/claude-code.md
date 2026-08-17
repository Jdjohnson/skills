# Claude Code

Use Claude Code when an independent Anthropic coding, review, research, or judgment pass fits the task.

## Model selection

Claude Code accepts rolling aliases such as `opus` and `sonnet`. Use an alias when a model must be named, or omit the model to respect the CLI's configured default. Do not hard-code an old dated model ID.

## Run

```bash
python3 <skill-root>/scripts/claude_delegate.py doctor --cwd /path/to/project
python3 <skill-root>/scripts/claude_delegate.py probe --cwd /path/to/project --model sonnet
python3 <skill-root>/scripts/claude_delegate.py run --cwd /path/to/project --mode plan --model sonnet --prompt-file /path/to/prompt.md
```

The wrapper uses headless output and bounded turns. Keep the task packet complete even when the repository has `CLAUDE.md` instructions.

## Sources

- [Claude Code model configuration](https://docs.anthropic.com/en/docs/claude-code/model-config)
- [Claude Code CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-usage)
