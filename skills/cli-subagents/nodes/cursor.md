# Cursor

**Status:** Inactive and explicit-only
**Command:** `cursor-agent`, not `agent`

## Route here

Use Cursor only when the user explicitly names it while access remains, or when its single multi-model harness is the point of the task. Do not route here by default.

Cursor's model inventory is account-dependent and changes often. Run `cursor-agent models` before choosing. Current model families may include Sol, Fable, Grok, Gemini, Composer, and others, but do not hard-code an old inventory.

Use `plan` or `ask` for read-only work. Headless `--print` can use write and shell tools, so edit mode needs explicit authorization. The wrapper requires `--allow-inactive` for probes and runs.

## Run

```bash
python3 <skill-root>/scripts/cursor_delegate.py doctor --cwd /path/to/project
cursor-agent models
python3 <skill-root>/scripts/cursor_delegate.py probe --cwd /path/to/project --allow-inactive --model MODEL_ID
python3 <skill-root>/scripts/cursor_delegate.py run --cwd /path/to/project --allow-inactive --mode plan --model MODEL_ID --prompt-file /path/to/prompt.md
```

Call `cursor-agent` explicitly because `agent` may resolve to another installed CLI.

## Sources

- [Cursor CLI overview](https://docs.cursor.com/en/cli/overview)
- [Cursor headless mode](https://docs.cursor.com/en/cli/headless)
- [Cursor CLI parameters](https://docs.cursor.com/en/cli/reference/parameters)
