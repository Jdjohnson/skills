# Grok Build

**Status:** Active subordinate
**Default:** `grok-4.5`, Medium effort
**Oversight:** Have Claude or Codex review consequential output

## Route here

Use Grok 4.5 for research and development that should move faster and more affordably: code exploration, prototypes, engineering research, science, math, and quick implementation branches. It accepts text and image input and supports low, medium, and high reasoning.

Keep Medium as the default. Use High only when the subordinate branch itself needs deeper reasoning. Prefer the Claude or Codex coordinator for the final judgment.

## Run

```bash
python3 <skill-root>/scripts/grok_delegate.py doctor --cwd /path/to/project
python3 <skill-root>/scripts/grok_delegate.py probe --cwd /path/to/project --model grok-4.5 --effort medium
python3 <skill-root>/scripts/grok_delegate.py run --cwd /path/to/project --mode plan --model grok-4.5 --effort medium --prompt-file /path/to/prompt.md
```

Web search and nested subagents stay off unless the task explicitly needs them. The wrapper records any enabled capability.
Read and plan use Grok's read-only sandbox. Edit and trusted modes stay inside its workspace sandbox; only trusted mode auto-approves tools.

## Sources

- [Grok Build overview](https://docs.x.ai/build/overview)
- [Headless scripting](https://docs.x.ai/build/cli/headless-scripting)
- [Grok Build CLI reference](https://docs.x.ai/build/cli/reference)
- [Grok 4.5](https://docs.x.ai/developers/models/grok-4.5)
