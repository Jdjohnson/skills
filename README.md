# Portable AI Skills

Small, reusable AI skills and thinking prompts.

These are designed to be useful in two ways:

- As copy/paste prompts in any major LLM.
- As skill folders for tools that support reusable skills, such as Codex or Claude Code.

Some skills are single-file prompts. Others include `nodes/`, `references/`,
or `scripts/` folders for deeper mode routing, examples, reusable instructions,
and deterministic helpers. Start with the skill's `SKILL.md`; it is always the
front door.

## Owned Skills

| Skill | Use it for | Link |
|---|---|---|
| brainstorm | Untangling a messy topic before it becomes a plan | [brainstorm](./skills/brainstorm/SKILL.md) |
| steelman | Pressure-testing and strengthening an idea, argument, strategy, or decision | [steelman](./skills/steelman/SKILL.md) |
| run | Planning and supervising larger AI-assisted projects | [run](./skills/run/SKILL.md) |
| chatgpt | Routing ChatGPT Deep Research, Agent, and Pro review into explicit orders | [chatgpt](./skills/chatgpt/SKILL.md) |
| brief | Turning complex material into a concise executive brief | [brief](./skills/brief/SKILL.md) |
| stuck | Getting unstuck with a practical reset plan | [stuck](./skills/stuck/SKILL.md) |
| writer | Taking rough ideas through a structured writing workflow | [writer](./skills/writer/SKILL.md) |
| style-guide | Calibrating and checking writing against a voice or style | [style-guide](./skills/style-guide/SKILL.md) |
| meeting-doc | Creating one useful meeting prep, closeout, or recap document | [meeting-doc](./skills/meeting-doc/SKILL.md) |
| economist-council | Running AI and economy questions through a sourced economist panel | [economist-council](./skills/economist-council/SKILL.md) |

## External References

These are useful public skills or repos that I reference, but do not maintain or republish here.

| Skill | Use it for | Source |
|---|---|---|
| Humanizer | Removing AI writing patterns without changing meaning | [Humanizer](https://github.com/blader/humanizer/blob/main/SKILL.md) |
| Last30Days | Researching current internet discourse and turning it into prompts | [Last30Days](https://github.com/mvanhorn/last30days-skill) |
| Grill Me | Direct plan interrogation | [Grill Me](https://github.com/mattpocock/skills/blob/main/grill-me/SKILL.md) |
| Deep Research | Citation-backed long-form research reports | [Deep Research](https://github.com/199-biotechnologies/claude-deep-research-skill) |

## Using A Skill

If your AI tool supports skills, add the folder under `skills/` and let the tool discover its `SKILL.md`.

If your tool does not support skills, open the `SKILL.md`, copy the core instructions into a new chat, then add your topic or plan underneath.

## Maintenance

Owned skills are exported from a local curated source before publishing. External references should be updated from their upstream repositories.

## Attribution

The `run` skill, installer, command wrapper, and runner are copied from [mostlyserious/run-workflow](https://github.com/mostlyserious/run-workflow), which is licensed under MIT. Its original license notice is preserved in [licenses/mostlyserious-run-workflow-MIT.txt](./licenses/mostlyserious-run-workflow-MIT.txt).
