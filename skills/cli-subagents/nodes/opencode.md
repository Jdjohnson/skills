# OpenCode

**Status:** Inactive and explicit-only
**Model:** Discover live; OpenCode is provider-neutral

## Route here

Use OpenCode only when the user explicitly names it and identifies a configured provider or wants its provider-neutral harness. Ending an OpenCode Go subscription does not disable the open-source CLI, but it removes that subscription-backed model lane.

Run `opencode models` before delegation. Model IDs use `provider/model`; do not treat any one model as intrinsic to OpenCode.

Built-in agent strengths:

- `build`: development with full tools.
- `plan`: restricted planning and analysis.
- `general`: multi-step research and execution.
- `explore`: fast, read-only codebase search.
- `scout`: read-only external dependency and documentation research.

## Run

```bash
python3 <skill-root>/scripts/opencode_delegate.py doctor --cwd /path/to/project --no-model-required
opencode models
python3 <skill-root>/scripts/opencode_delegate.py run --allow-inactive --cwd /path/to/project --mode plan --model provider/model --prompt-file /path/to/prompt.md
```

Do not route here automatically. `probe` and `run` require `--allow-inactive`. Confirm the selected provider's cost, data policy, and authentication before use.

## Sources

- [OpenCode CLI](https://opencode.ai/docs/cli)
- [OpenCode models](https://opencode.ai/docs/models)
- [OpenCode agents](https://opencode.ai/docs/agents)
- [OpenCode Go](https://opencode.ai/docs/go)
