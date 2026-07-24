# Gemini

**Status:** Active subordinate
**Default:** `gemini-3.6-flash`
**Oversight:** Have Claude or Codex review consequential output

## Route here

Use Gemini for fast, inexpensive, multimodal work, especially image, PDF, audio, video, document extraction, structured parsing, and high-volume subtasks.

- `gemini-3.6-flash`: default for fast agentic work, code, multimodal reasoning, and vision.
- `gemini-3.5-flash-lite`: use for simple, high-throughput extraction, classification, transformation, and JSON work.

Use concrete IDs. Gemini CLI aliases can lag current models. Ordinary `@path` is reliable for text; use Gemini's `read_file` tool or a custom-command `@{path}` when multimodal encoding must be explicit.

## Run

```bash
python3 <skill-root>/scripts/gemini_delegate.py doctor --cwd /path/to/project
python3 <skill-root>/scripts/gemini_delegate.py probe --cwd /path/to/project --model gemini-3.6-flash
python3 <skill-root>/scripts/gemini_delegate.py run --cwd /path/to/project --mode plan --model gemini-3.6-flash --prompt-file /path/to/prompt.md
```

Give Gemini a narrow branch with clear acceptance criteria. Send its result to the Claude or Codex coordinator for synthesis and verification.
A cached Google login is not service-level proof; use `probe` to verify that the current account tier and requested model are actually eligible.

## Sources

- [Gemini 3.6 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-3.6-flash)
- [Latest Gemini models](https://ai.google.dev/gemini-api/docs/latest-model)
- [Gemini CLI headless mode](https://geminicli.com/docs/cli/headless/)
- [Gemini CLI file tools](https://geminicli.com/docs/tools/file-system/)
