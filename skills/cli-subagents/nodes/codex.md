# Codex

**Status:** Active primary and quality anchor
**Default:** `gpt-5.6-sol`, Medium effort
**Escalate:** High effort for difficult, ambiguous, or quality-critical work

## Route here

Use Sol as the daily driver and workhorse for hard implementation, debugging, research, computer use, and high-value work where polish matters. This is a personal override: OpenAI describes Terra as the economical everyday workhorse, but Sol is the preferred default here.

- `gpt-5.6-sol`: flagship quality for difficult, ambiguous, high-value work.
- `gpt-5.6-terra`: balanced all-rounder when cost and speed matter more.
- `gpt-5.6-luna`: fastest, lowest-cost choice for clear, repeatable, high-volume extraction, classification, transformation, or structured summaries.

## Run

```bash
python3 <skill-root>/scripts/codex_delegate.py doctor --cwd /path/to/project
python3 <skill-root>/scripts/codex_delegate.py probe --cwd /path/to/project --model gpt-5.6-sol --effort medium
python3 <skill-root>/scripts/codex_delegate.py run --cwd /path/to/project --mode plan --model gpt-5.6-sol --effort medium --prompt-file /path/to/prompt.md
```

The CLI sets effort through `model_reasoning_effort`; the wrapper handles that mapping. Use Medium by default and High for consequential work.

## Sources

- [OpenAI current model guide](https://developers.openai.com/api/docs/guides/latest-model)
- [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)
- [Codex CLI commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
