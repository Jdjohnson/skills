# Grok Build

Use Grok Build for a separate xAI research, development, or implementation lane.

## Model selection

Run `grok models` after authentication and select the current Build or code model exposed by the CLI. xAI retired earlier coding slugs in 2026, so never preserve an old default solely because it worked in a previous installation.

## Run

```bash
python3 <skill-root>/scripts/grok_delegate.py doctor --cwd /path/to/project
grok models
python3 <skill-root>/scripts/grok_delegate.py probe --cwd /path/to/project --model MODEL_ID
python3 <skill-root>/scripts/grok_delegate.py run --cwd /path/to/project --mode plan --model MODEL_ID --prompt-file /path/to/prompt.md
```

Check whether the authenticated path uses a consumer subscription or separately billed API account. Keep web search and nested agents off unless the bounded task needs them.

## Sources

- [Grok Build documentation](https://docs.x.ai/build)
- [xAI model retirement guidance](https://docs.x.ai/developers/migration/may-15-retirement)
