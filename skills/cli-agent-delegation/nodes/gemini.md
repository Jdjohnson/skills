# Gemini

Use Gemini for multimodal work or a separate Google coding and research lane.

## Model selection

Gemini CLI's default model is `auto`, which routes between available models. Prefer `auto` unless the user requests a concrete model, then probe that exact model before work.

## Run

```bash
python3 <skill-root>/scripts/gemini_delegate.py doctor --cwd /path/to/project
python3 <skill-root>/scripts/gemini_delegate.py probe --cwd /path/to/project --model auto
python3 <skill-root>/scripts/gemini_delegate.py run --cwd /path/to/project --mode plan --model auto --prompt-file /path/to/prompt.md
```

Read and plan use Gemini's read-only plan mode. Edit uses its reviewed edit mode. Authentication method affects model and quota access, so a cached login is not proof that a requested model is available.

## Sources

- [Gemini CLI model routing](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/model-routing.md)
- [Gemini CLI configuration](https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/configuration.md)
