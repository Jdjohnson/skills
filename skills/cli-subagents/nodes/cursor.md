# Cursor

Use Cursor for a separate multi-model coding, implementation, or review lane.

## Model selection

Cursor's inventory is account-dependent and changes often. Use `agent models`, `agent --list-models`, or the authenticated CLI's equivalent to inspect live models. Prefer `Auto` unless the user requests a specific available model.

## Run

```bash
python3 <skill-root>/scripts/cursor_delegate.py doctor --cwd /path/to/project
agent models
python3 <skill-root>/scripts/cursor_delegate.py probe --cwd /path/to/project --model MODEL_ID
python3 <skill-root>/scripts/cursor_delegate.py run --cwd /path/to/project --mode plan --model MODEL_ID --prompt-file /path/to/prompt.md
```

`agent` is Cursor's current primary entry point; `cursor-agent` remains a compatibility alias. The bundled wrapper accepts whichever compatible command is installed. Headless print mode can write and run shell commands, so use edit only with authorization.

## Sources

- [Cursor CLI](https://cursor.com/en-US/cli)
- [Cursor CLI model discovery](https://cursor.com/changelog/cli-jan-08-2026)
- [Cursor CLI parameters](https://docs.cursor.com/en/cli/reference/parameters)
