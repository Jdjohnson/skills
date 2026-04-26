# Portable AI Skills

Small, reusable AI skills and thinking prompts.

These are designed to be useful in two ways:

- As **copy/paste prompts** in any major LLM.
- As **skill folders** for tools that support reusable skills, such as Codex or Claude Code.

## Skills

| Skill | Use it for | Link |
|---|---|---|
| Brainstorm | Untangling a messy topic before it becomes a plan | [brainstorm](./skills/brainstorm/SKILL.md) |
| Steelman | Pressure-testing and strengthening an idea, argument, strategy, or decision | [steelman](./skills/steelman/SKILL.md) |
| Run | Planning and supervising larger AI-assisted projects | [run](./skills/run/SKILL.md) |

## External Reference

I also use Matt Pocock's public [Grill Me skill](https://github.com/mattpocock/skills/blob/main/grill-me/SKILL.md) for direct plan interrogation.

## Using A Skill

If your AI tool supports skills, add the folder under `skills/` and let the tool discover its `SKILL.md`.

If your tool does not support skills, open the `SKILL.md`, copy the core instructions into a new chat, then add your topic or plan underneath.

## Attribution

The `run` skill, installer, command wrapper, and runner are copied from [mostlyserious/run-workflow](https://github.com/mostlyserious/run-workflow), which is licensed under MIT. Its original license notice is preserved in [licenses/mostlyserious-run-workflow-MIT.txt](./licenses/mostlyserious-run-workflow-MIT.txt).
