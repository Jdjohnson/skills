# Generic AI Skills

A public bank of 14 reusable skills for thinking, planning, writing, meetings,
research, and agent tooling. Published skills avoid private workspace
assumptions, personal voice profiles, client context, and organization-specific
routing.

## Install

```bash
npx skills@latest add Jdjohnson/skills
```

Inspect the inventory or install selected skills:

```bash
npx skills@latest add Jdjohnson/skills --list
npx skills@latest add Jdjohnson/skills --skill brainstorm --skill autoresearch
```

Each skill starts at `skills/<name>/SKILL.md`. Supporting nodes, references,
scripts, tests, and assets stay inside that skill's directory.

## Skills

### Thinking and planning

| Skill | Use it for |
|---|---|
| [brainstorm](./skills/brainstorm/SKILL.md) | Exploring messy topics before they become a plan or decision |
| [brief](./skills/brief/SKILL.md) | Creating concise briefs from pasted text, files, URLs, or topics |
| [decision-walkthrough](./skills/decision-walkthrough/SKILL.md) | Walking supplied material one decision at a time with a running log |
| [plan](./skills/plan/SKILL.md) | Co-creating day, week, or month plans through lightweight approval phases |
| [steelman](./skills/steelman/SKILL.md) | Pressure-testing and strengthening an idea, argument, or decision |

### Writing, reflection, and meetings

| Skill | Use it for |
|---|---|
| [writer](./skills/writer/SKILL.md) | Turning rough ideas, notes, or drafts into publishable prose |
| [reflect](./skills/reflect/SKILL.md) | Reflecting on journal entries or similar personal writing supplied or located by the user |
| [meeting](./skills/meeting/SKILL.md) | Preparing, closing, finding history, and reviewing meeting patterns |
| [work-log](./skills/work-log/SKILL.md) | Explicitly closing out an active work thread into configured records |

### Agent and tooling

| Skill | Use it for |
|---|---|
| [chatgpt](./skills/chatgpt/SKILL.md) | Routing explicit ChatGPT orders, Deep Research, Agent, or Pro review |
| [cli-subagents](./skills/cli-subagents/SKILL.md) | Routing bounded work across locally available CLI agents |
| [gws-cli](./skills/gws-cli/SKILL.md) | Running guarded Google Workspace CLI reads and approved mutations |
| [papercut](./skills/papercut/SKILL.md) | Reviewing the visible session for small workflow friction on explicit request |

### Research

| Skill | Use it for |
|---|---|
| [autoresearch](./skills/autoresearch/SKILL.md) | Running checkpointed, source-backed research with durable working notes |

## Maintenance

The maintainer validator enforces the exact inventory, portable metadata,
working internal links, parity fixtures, source scrubbing, and the absence of
generated caches. Regression tests are local and must not perform live external
mutations.

## Attribution

Jarad Johnson is the repository author.
