# Codex

Use Codex for a separate OpenAI coding, debugging, implementation, or review lane.

## Model selection

Omit `--model` to respect the authenticated CLI's configured default. When the user requests a specific current model, verify it against official OpenAI documentation before passing it. Do not preserve an old coding-model pin in the skill.

## Run

```bash
python3 <skill-root>/scripts/codex_delegate.py doctor --cwd /path/to/project
python3 <skill-root>/scripts/codex_delegate.py probe --cwd /path/to/project
python3 <skill-root>/scripts/codex_delegate.py run --cwd /path/to/project --mode plan --prompt-file /path/to/prompt.md
```

Read and plan use a read-only sandbox; edit uses workspace-write. A broader sandbox remains an explicit override. Keep the packet sufficient even when Codex loads project `AGENTS.md` files.

## Sources

- [OpenAI model catalog](https://developers.openai.com/api/docs/models)
- [Codex documentation](https://developers.openai.com/codex)
