# Portable AI Skills

These are public versions of skills I actually use.

The goal is simple: make reusable AI workflows that are stronger than a
single prompt but still easy to copy into another tool. They should help with
thinking, writing, briefings, meetings, research direction, and larger
AI-assisted projects without dragging a private workspace behind them.

Each owned skill starts at `SKILL.md`. That file is the front door. Most of the
actual behavior lives in `nodes/`, with `references/` or `scripts/` added only
when a skill needs examples, source material, or helper code.

I keep the public versions portable on purpose. They don't assume my local
files, private notes, daily workflow, or machine setup. If a skill needs
context, it asks for it.

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
| context-sweep | Sweeping high-signal cross-app context into a daily note | [context-sweep](./skills/context-sweep/SKILL.md) |

## External References

These are useful public skills or repos that I reference, but don't maintain or republish here.

| Skill | Use it for | Source |
|---|---|---|
| Humanizer | Removing AI writing patterns without changing meaning | [Humanizer](https://github.com/blader/humanizer/blob/main/SKILL.md) |
| Last30Days | Researching current internet discourse and turning it into prompts | [Last30Days](https://github.com/mvanhorn/last30days-skill) |
| Grill Me | Direct plan interrogation | [Grill Me](https://github.com/mattpocock/skills/blob/main/grill-me/SKILL.md) |
| Deep Research | Citation-backed long-form research reports | [Deep Research](https://github.com/199-biotechnologies/claude-deep-research-skill) |

## Using A Skill

If your AI tool supports skills, copy the whole folder under `skills/` and let
the tool discover its `SKILL.md`.

If your tool doesn't support skills, open `SKILL.md`, copy the relevant
instructions into a new chat, then add your topic, draft, notes, or question
underneath.

## Maintenance

I keep a deeper private working set, then strip the private context before
publishing here. For external references, check the upstream repos before
copying anything forward.

## Attribution

The `run` skill, installer, command wrapper, and runner are copied from [mostlyserious/run-workflow](https://github.com/mostlyserious/run-workflow), which is licensed under MIT. Its original license notice is preserved in [licenses/mostlyserious-run-workflow-MIT.txt](./licenses/mostlyserious-run-workflow-MIT.txt).
