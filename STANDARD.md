# Skill Authoring Standard

Applies to every skill in this repo. Based on the OpenAI Codex skills
documentation and Anthropic's skill-creator guidance. Team members run
these skills in both Codex and Claude Code, and Codex behavior sets the
bar.

## How Codex loads skills

Facts that drive the rules below:

- Codex keeps only each skill's name, description, and path in context. It
  reads the full SKILL.md only after deciding to use the skill. The
  combined list of all skill names and descriptions gets at most 2% of the
  context window, about 8,000 characters. Long descriptions crowd out
  other skills and can be shortened by the tool, so the first sentence has
  to carry the trigger.
- Skills trigger two ways: explicitly (`$skill-name`) or implicitly when
  the request matches the description. The description is the whole
  trigger contract. "When to use" lives there, never in the body.
- A skill is a folder: SKILL.md (required), plus optional `scripts/` for
  runnable code, `references/` or `nodes/` for docs loaded on demand,
  `assets/` for templates, and `agents/openai.yaml` for Codex display
  metadata.
- Codex requires only `name` and `description` in frontmatter. Extra
  fields are ignored, so nothing important can live in them.

## The description

- First sentence: what the skill does and the words a person would
  actually use when they need it. Front-load; assume everything after
  sentence one can be cut by the tool.
- Two or three sentences, roughly 50 words.
- Name the modes or nodes if the skill has them, in one breath.
- Add "do not use for X" only when a genuine near-miss exists (a sibling
  skill that competes for the same request).
- Keep explicit-invocation-only gates where they exist. Skills that must
  never fire on their own say so in one short clause.

## The body

- Short. Under 500 lines is the ceiling; one screen is the target. If a
  skill needs more, push detail into `nodes/` or `references/` files and
  point to them with "read X when Y."
- Imperative voice. Say why a rule exists instead of writing MUST in
  caps. A model that understands the reason follows the rule in cases the
  author didn't predict.
- Each node or mode gets a clear name (a plain verb or noun) and a
  one-line purpose, listed in one table near the top.
- Show exact output formats where format matters. One example beats three
  paragraphs.
- Cut anything not pulling its weight: repeated warnings, restated rules,
  overcomplete lists, defensive boilerplate.

## The writing

Skill files are read by models and maintained by people, so they follow
the same rules as any other writing here:

- Plain words. "Use" not "leverage," "is" not "serves as."
- No AI tells: no "not just X but Y," no synonym cycling, no rule-of-three
  padding, no `crucial`/`delve`/`robust`/`seamless`, no mechanical
  bolding, no dash-heavy sentences.
- Concrete over vague. Name the file, the command, the number.
- A new teammate should understand every sentence on first read without
  knowing internal shorthand.

## What a standards pass must not change

- Safety rules, allowed-surface lists, approval gates, and off-limits
  sections keep exactly the same meaning and strictness. Tighten wording,
  never scope.
- Skill names and invocation forms stay stable. Renames break habits and
  saved commands.
- No merging, splitting, or deleting skills, and no new modes, config, or
  process. Less over more.

## Checklist for any skill edit

1. Description: first sentence carries the trigger, total under ~50
   words, invocation gate preserved.
2. Node/mode table present, each line plain.
3. Body reads clean top to bottom, detail pushed to child files.
4. Safety and scope contracts equivalent in meaning.
5. No AI tells left.
