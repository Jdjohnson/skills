# OpenCode

Use OpenCode when a provider-neutral harness with a configured provider fits the task.

## Model selection

OpenCode builds its catalog from connected providers. Run `opencode models --refresh` and use an exact `provider/model` entry shown there. Do not hard-code a provider or model into this skill.

## Run

```bash
python3 <skill-root>/scripts/opencode_delegate.py doctor --cwd /path/to/project --no-model-required
opencode models --refresh
python3 <skill-root>/scripts/opencode_delegate.py run --cwd /path/to/project --mode plan --model provider/model --prompt-file /path/to/prompt.md
```

Read and plan use a restricted planning agent. Edit uses the configured build agent. Confirm provider cost, data policy, and authentication before passing sensitive material.

## Sources

- [OpenCode CLI](https://dev.opencode.ai/docs/cli/)
- [OpenCode models](https://opencode.ai/v2/docs/models)
