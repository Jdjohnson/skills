---
name: jj-writer
description: >
  Improve AI-created content for Jarad Johnson using his voice DNA, writing
  style guide, and email writing guidance. Use whenever the AI is writing for
  Jarad or on Jarad's behalf: emails, replies, proposals, posts, articles,
  social copy, personal notes, outbound drafts, or any text that should sound
  like him. Also use when checking whether writing sounds like Jarad.
---

# JJ Writer

Voice and style companion for any AI-created content for Jarad. This skill does **not** replace the current writing workflow (`jj-writing`, `docs`, or other drafting skills). Those skills keep their process. JJ Writer supplies the voice layer they should use when the output is for Jarad or in his voice.

## When to Use

Use JJ Writer when:

- drafting or revising text **as Jarad** or **for Jarad**
- checking whether a draft sounds like Jarad
- writing email, replies, follow-ups, proposals, posts, articles, social copy, or personal notes on his behalf

Do **not** use JJ Writer as the primary workflow for brainstorming, briefs, steelmanning, or general writing development. Route those to their existing skills first, then apply JJ Writer when the output needs Jarad's voice.

## Companion Flow

Full usage rules: [usage](nodes/usage.md)

1. Classify content type enough to load the right guidance (email, short-form, long-form, proposal/client note, internal note, or revision).
2. Load [voice-dna](nodes/voice-dna.md) and [jarad-style-guide](nodes/jarad-style-guide.md) before drafting or revising.
3. For email, replies, follow-ups, and outbound notes, also load [email-voice-profile](nodes/email-voice-profile.md).
4. Let the active writing skill or task workflow handle intake, structure, drafting, and revision.
5. Run [style-check](nodes/style-check.md) on near-final content.
6. Run [humanizer-gate](nodes/humanizer-gate.md) before handoff unless Jarad explicitly opts out.

## Core Rules

- Preserve meaning and intent over polish.
- Avoid fake specificity, unsupported warmth, and corporate filler.
- Match Jarad's controlled informality: casual delivery, exact thinking underneath.
- For email: short operational paragraphs, concrete warmth, direct asks, simple closings.
- Do not store voice-specific content in `resources/preferences/writing.md`; that file is for general preferences. JJ Writer nodes are the voice system of record.

## Node Map

| Node | Purpose |
|------|---------|
| [usage](nodes/usage.md) | How JJ Writer plugs into existing writing workflows |
| [voice-dna](nodes/voice-dna.md) | Rhythm and instinct samples for pattern matching |
| [jarad-style-guide](nodes/jarad-style-guide.md) | Full style rules for AI output as Jarad |
| [email-voice-profile](nodes/email-voice-profile.md) | Channel-specific email guidance |
| [style-check](nodes/style-check.md) | Voice drift scan and final gate |
| [humanizer-gate](nodes/humanizer-gate.md) | Mandatory Humanizer pass before handoff |

## Integration with Other Skills

- **jj-writing**: use for draft development; apply JJ Writer for voice calibration, style check, and Humanizer gate on near-final output.
- **humanizer**: required final cleanup pass for content written on Jarad's behalf. See [humanizer-gate](nodes/humanizer-gate.md).
- **docs**: use for Google Doc creation; apply JJ Writer when the doc content should sound like Jarad.
