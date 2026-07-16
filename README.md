# Generic AI Skills

A public bank of 18 reusable skills for thinking, planning, writing, meetings, research, and agent tooling. Published skills avoid private workspace assumptions, personal voice profiles, client context, and organization-specific routing.

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

## Skills

### Thinking and planning

| Skill | Use it for |
|---|---|
| [brainstorm](./skills/brainstorm/SKILL.md) | Finding the shape of a messy idea before turning it into a plan |
| [brief](./skills/brief/SKILL.md) | Turning source material into a concise executive brief |
| [decision-walkthrough](./skills/decision-walkthrough/SKILL.md) | Working through source material one decision at a time and recording the settled result |
| [plan](./skills/plan/SKILL.md) | Co-creating day, week, or month plans through approval phases |
| [steelman](./skills/steelman/SKILL.md) | Pressure-testing and strengthening an idea, argument, or decision |
| [stuck](./skills/stuck/SKILL.md) | Diagnosing a block and choosing a practical starting move |

### Writing and meetings

| Skill | Use it for |
|---|---|
| [writer](./skills/writer/SKILL.md) | Developing source-backed writing through a structured process |
| [meeting](./skills/meeting/SKILL.md) | Preparing, closing, finding, and reviewing meetings |
| [work-log](./skills/work-log/SKILL.md) | Explicitly closing out an active work thread into configured records |

### Agent and tooling

| Skill | Use it for |
|---|---|
| [chatgpt](./skills/chatgpt/SKILL.md) | Packaging explicit ChatGPT research, agent, and review handoffs |
| [claude-code](./skills/claude-code/SKILL.md) | Delegating bounded work to the Claude Code CLI |
| [codex](./skills/codex/SKILL.md) | Delegating bounded work to the Codex CLI |
| [context-sweep](./skills/context-sweep/SKILL.md) | Gathering high-signal context from configured sources into a daily note |
| [grok-build](./skills/grok-build/SKILL.md) | Delegating bounded work to the Grok CLI |
| [gws-cli](./skills/gws-cli/SKILL.md) | Running guarded Google Workspace CLI operations |
| [opencode](./skills/opencode/SKILL.md) | Delegating bounded work to the OpenCode CLI |
| [run](./skills/run/SKILL.md) | Planning and supervising larger AI-assisted projects |

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
