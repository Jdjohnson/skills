# Generic AI Skills

A public bank of 15 reusable skills for thinking, planning, writing, meetings, research, and agent tooling. Published skills avoid private workspace assumptions, personal voice profiles, client context, and organization-specific routing.

## Install

```bash
npx skills@latest add Jdjohnson/skills
```

Inspect the inventory or install selected skills:

```bash
npx skills@latest add Jdjohnson/skills --list
npx skills@latest add Jdjohnson/skills --skill brainstorm --skill plan
```

Each skill starts at `skills/<name>/SKILL.md`. Supporting nodes, references, scripts, and tests stay inside that skill's directory.

Version 3 consolidates the former `claude-code`, `codex`, `grok-build`, and `opencode` skills into `cli-subagents`. Use `$cli-subagents` and select the matching node.

## Skills

### Thinking and planning

| Skill | Use it for |
|---|---|
| [brainstorm](./skills/brainstorm/SKILL.md) | Exploring messy topics before they become a plan or decision |
| [brief](./skills/brief/SKILL.md) | Creating concise briefs from pasted text, files, URLs, or topics |
| [decision-walkthrough](./skills/decision-walkthrough/SKILL.md) | Walking supplied material one decision at a time with a running log |
| [plan](./skills/plan/SKILL.md) | Co-creating day, week, or month plans through lightweight approval phases |
| [steelman](./skills/steelman/SKILL.md) | Pressure-testing and strengthening an idea, argument, or decision |
| [stuck](./skills/stuck/SKILL.md) | Diagnosing a block and choosing a practical starting move |

### Writing and meetings

| Skill | Use it for |
|---|---|
| [writer](./skills/writer/SKILL.md) | Turning rough ideas, notes, or drafts into publishable prose |
| [meeting](./skills/meeting/SKILL.md) | Preparing, closing, finding history, and reviewing meeting patterns |
| [work-log](./skills/work-log/SKILL.md) | Explicitly closing out an active work thread into configured records |

### Agent and tooling

| Skill | Use it for |
|---|---|
| [chatgpt](./skills/chatgpt/SKILL.md) | Routing explicit ChatGPT orders, Deep Research, Agent, or Pro review |
| [cli-subagents](./skills/cli-subagents/SKILL.md) | Routing bounded work across active and inactive local CLI agents |
| [context-sweep](./skills/context-sweep/SKILL.md) | Gathering configured source activity into a daily note with checkpoints |
| [gws-cli](./skills/gws-cli/SKILL.md) | Running guarded Google Workspace CLI reads and approved mutations |
| [run](./skills/run/SKILL.md) | Planning and running larger projects with tool routing and resume support |

### Research

| Skill | Use it for |
|---|---|
| [economist-council](./skills/economist-council/SKILL.md) | Examining AI-and-economy questions through a sourced economist panel |

## Upstream skills I use

These projects are linked, not republished here:

- Matt Pocock's [grill-me](https://github.com/mattpocock/skills/tree/main/grill-me) and [grill-with-docs](https://github.com/mattpocock/skills/tree/main/grill-with-docs). Their complete chain also includes `grilling` and `domain-modeling`.
- [Humanizer](https://github.com/blader/humanizer), MIT-licensed by Siqi Chen.
- [GPT Researcher](https://github.com/assafelovic/gpt-researcher), Apache-2.0 licensed.

## Maintenance

The maintainer validator enforces the exact inventory, portable metadata, working internal links, parity fixtures, source scrubbing, and the absence of generated caches or committed install archives. Regression tests are local and must not perform live external mutations.

## Attribution

Jarad Johnson is the repository author. The bundled `run` adaptation comes from [Mostly Serious's run-workflow](https://github.com/mostlyserious/run-workflow); its MIT notice is preserved in [licenses/mostlyserious-run-workflow-MIT.txt](./licenses/mostlyserious-run-workflow-MIT.txt).
