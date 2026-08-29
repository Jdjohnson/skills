# Jarad Johnson's Agent Skills

Twenty-four reusable skills for thinking, research, writing, visual direction,
and agent workflows.

## Install

Browse the collection and choose which skills and agents to install:

```bash
npx skills@latest add Jdjohnson/skills
```

Install one skill:

```bash
npx skills@latest add Jdjohnson/skills --skill visual-direction
```

List without installing, or update installed skills:

```bash
npx skills@latest add Jdjohnson/skills --list
npx skills update
```

The installer uses project scope by default. Review a skill's `SKILL.md` and
bundled scripts before installing it.

## Gift a skill to your agent

Paste this into an agent that can access the current project's files and
terminal:

```text
Install the `visual-direction` Agent Skill from https://github.com/Jdjohnson/skills for this project and the agent you are currently using. First review https://github.com/Jdjohnson/skills/blob/main/skills/visual-direction/SKILL.md and its neighboring bundled files. Then run `npx skills@latest add Jdjohnson/skills --skill visual-direction`. Install only that skill, preserve its complete folder, and tell me where it was installed. Do not install globally or add other skills without asking. If this environment cannot install skills, say so instead of claiming success.
```

Replace `visual-direction` with any skill below.

## Skills

### Think and decide

| Skill | Use it for |
| --- | --- |
| [consulting-navigator](./skills/consulting-navigator/SKILL.md) | Choosing the right analysis method for an ambiguous business decision |
| [cfo-decision-advisor](./skills/cfo-decision-advisor/SKILL.md) | Making practical calls on cash, margin, pricing, capacity, and financial risk |
| [guided-brainstorm](./skills/guided-brainstorm/SKILL.md) | Turning an early idea into clearer options through focused questions |
| [idea-stress-test](./skills/idea-stress-test/SKILL.md) | Pressure-testing and strengthening an established idea |
| [decision-walkthrough](./skills/decision-walkthrough/SKILL.md) | Resolving supplied material one decision at a time |
| [execution-trust](./skills/execution-trust/SKILL.md) | Keeping decisions and commitments from decaying |
| [david-deutsch-lens](./skills/david-deutsch-lens/SKILL.md) | Applying source-grounded David Deutsch arguments carefully |

### Research and knowledge

| Skill | Use it for |
| --- | --- |
| [checkpointed-research](./skills/checkpointed-research/SKILL.md) | Running durable, multi-pass, source-backed research |
| [executive-brief](./skills/executive-brief/SKILL.md) | Turning a topic or source into a concise decision brief |
| [source-backed-wiki](./skills/source-backed-wiki/SKILL.md) | Building a local wiki with traceable claims |
| [journal-reflection](./skills/journal-reflection/SKILL.md) | Finding grounded patterns across supplied journals |
| [genealogy-site-publisher](./skills/genealogy-site-publisher/SKILL.md) | Publishing family history with privacy and provenance controls |

### Write and direct

| Skill | Use it for |
| --- | --- |
| [visual-direction](./skills/visual-direction/SKILL.md) | Finding and refining an image-led visual language |
| [photography-director](./skills/photography-director/SKILL.md) | Directing a photograph and preparing its execution handoff |
| [plain-language-writer](./skills/plain-language-writer/SKILL.md) | Writing clear, natural, audience-aware prose |
| [adhd-friendly-output](./skills/adhd-friendly-output/SKILL.md) | Making dense material easier to scan and act on |

### Agents and operations

| Skill | Use it for |
| --- | --- |
| [chatgpt-handoff](./skills/chatgpt-handoff/SKILL.md) | Preparing and reconciling bounded ChatGPT assignments |
| [cli-agent-delegation](./skills/cli-agent-delegation/SKILL.md) | Delegating bounded work to installed agent CLIs |
| [manus-api](./skills/manus-api/SKILL.md) | Sending sustained work to Manus with credit controls |
| [gws-cli](./skills/gws-cli/SKILL.md) | Running guarded Google Workspace CLI operations |
| [comms-intake](./skills/comms-intake/SKILL.md) | Triaging a configured local message queue |
| [time-partner](./skills/time-partner/SKILL.md) | Planning, tracking, reviewing, and reflecting in period |
| [work-closeout](./skills/work-closeout/SKILL.md) | Reconciling proven outcomes across configured records |
| [session-friction-review](./skills/session-friction-review/SKILL.md) | Extracting validated workflow friction from a visible session |


## Maintain

Each package lives at `skills/<name>/` and follows the open Agent Skills
format. Validate metadata and run deterministic package tests with:

```bash
python3 scripts/validate.py
bash scripts/test.sh
```

See [STANDARD.md](./STANDARD.md) for the short authoring contract.

## License

Original code, writing, and identified generated media are MIT licensed.
Third-party reference media keeps its source license; see
[THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md) and the attribution files
inside the two visual skills.
