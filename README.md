# Portable AI Skills

These are public versions and source snapshots of skills I actually use.

The repo has three lanes:

- Portable skills that are meant to copy cleanly into another tool.
- Jarad Pack skills from Dot Core, kept under their `jj-*` names and normalized for this repo.
- Workspace personal skills from my Dot workspace, normalized for this repo and still allowed to assume local tools, private systems, or credentials.

Each owned skill starts at `SKILL.md`. That file is the front door. Most behavior lives in `nodes/`, with `references/`, `scripts/`, or `tests/` added only when a skill needs examples, source material, helper code, or validation.

## Portable Skills

These are the more general versions. They avoid local workspace assumptions and are the safest starting point for reuse.

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

## Jarad Pack For Dot Core

These are skill-package exports from Dot Core's `jarad-pack` add-on. They are included for parity with the Dot product source and may mention Dot routes or local handling rules.

| Skill | Use it for | Link |
|---|---|---|
| jj-brainstorm | Exploring messy ideas, strategy, options, and open questions | [jj-brainstorm](./skills/jj-brainstorm/SKILL.md) |
| jj-brief | Creating concise executive briefs from source material | [jj-brief](./skills/jj-brief/SKILL.md) |
| jj-chatgpt | Routing ChatGPT orders and ChatGPT returns through Dot | [jj-chatgpt](./skills/jj-chatgpt/SKILL.md) |
| jj-steelman | Pressure-testing and strengthening ideas or decisions | [jj-steelman](./skills/jj-steelman/SKILL.md) |
| jj-writing | Developing drafts from ideas, notes, source material, or rough text | [jj-writing](./skills/jj-writing/SKILL.md) |

## Dot Workspace Personal Skills

These are package exports from `.dot-skills/`. They are useful as source snapshots or personal installs, but many are intentionally local and require the matching CLI, MCP, workspace, or credentials.

### Local Agent CLI Skills

These wrap local agent CLIs so another agent can delegate bounded review, planning, editing, or smoke-test work without hand-building shell commands. They are also packaged as individual downloads in [downloads/cli-skills](./downloads/cli-skills/README.md).

| Skill | Use it for | Source | Download |
|---|---|---|---|
| claude-code | Delegating bounded work to the local Claude Code CLI | [source](./skills/claude-code/SKILL.md) | [zip](./downloads/cli-skills/claude-code-skill.zip) |
| codex | Delegating bounded review, planning, and editing to the local Codex CLI | [source](./skills/codex/SKILL.md) | [zip](./downloads/cli-skills/codex-skill.zip) |
| grok-build | Delegating bounded work to the local Grok Build CLI | [source](./skills/grok-build/SKILL.md) | [zip](./downloads/cli-skills/grok-build-skill.zip) |
| opencode | Delegating bounded work to the local OpenCode CLI | [source](./skills/opencode/SKILL.md) | [zip](./downloads/cli-skills/opencode-skill.zip) |

### Dot And Workspace Skills

| Skill | Use it for | Link |
|---|---|---|
| dot-recall | Searching local Dot Recall context when MEMORY.md is thin | [dot-recall](./skills/dot-recall/SKILL.md) |
| gpt-researcher | Routing autonomous deep research through GPT Researcher/MCP | [gpt-researcher](./skills/gpt-researcher/SKILL.md) |
| gws-cli | Guarded Google Workspace CLI routing for Docs, Drive, Sheets, Gmail, and Calendar | [gws-cli](./skills/gws-cli/SKILL.md) |
| jj-intake | Triage for Dot's external comms queue from SMS/email | [jj-intake](./skills/jj-intake/SKILL.md) |
| jj-log | Explicit closeout logging to Dot Today, memory notes, and named Asana tasks | [jj-log](./skills/jj-log/SKILL.md) |
| jj-reflect | Reflecting across journal material and Dot timeline day folders | [jj-reflect](./skills/jj-reflect/SKILL.md) |
| jj-writer | Rewriting and checking text against Jarad's voice and style | [jj-writer](./skills/jj-writer/SKILL.md) |
| ms-crm | Creating MSCRM deals through an approval-gated flow | [ms-crm](./skills/ms-crm/SKILL.md) |

## External References

These are useful public skills or repos that I reference, but don't maintain or republish here.

| Skill | Use it for | Source |
|---|---|---|
| Humanizer | Removing AI writing patterns without changing meaning | [Humanizer](https://github.com/blader/humanizer/blob/main/SKILL.md) |
| Last30Days | Researching current internet discourse and turning it into prompts | [Last30Days](https://github.com/mvanhorn/last30days-skill) |
| Grill Me | Direct plan interrogation | [Grill Me](https://github.com/mattpocock/skills/blob/main/grill-me/SKILL.md) |
| Deep Research | Citation-backed long-form research reports | [Deep Research](https://github.com/199-biotechnologies/claude-deep-research-skill) |

## Using A Skill

If your AI tool supports skills, copy the whole folder under `skills/` and let the tool discover its `SKILL.md`.

If your tool doesn't support skills, open `SKILL.md`, copy the relevant instructions into a new chat, then add your topic, draft, notes, or question underneath.

For portable reuse, start with the skills in `Portable Skills`. For my local Dot setup, use the `jj-*` and Dot workspace personal skills only when the surrounding toolchain is present.

## Maintenance

Portable skills are checked for parity files, working node links, output contracts, and accidental local leakage. Dot-local skills are checked for a valid `SKILL.md`, internal links, and generated cache files.

Jarad Pack source comes from Dot Core. Workspace personal skill source comes from `.dot-skills/`. Derived agent-home copies are not canonical source.

## Attribution

The `run` skill, installer, command wrapper, and runner are copied from [mostlyserious/run-workflow](https://github.com/mostlyserious/run-workflow), which is licensed under MIT. Its original license notice is preserved in [licenses/mostlyserious-run-workflow-MIT.txt](./licenses/mostlyserious-run-workflow-MIT.txt).
