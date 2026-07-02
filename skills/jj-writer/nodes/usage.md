---
description: |
  How JJ Writer plugs into existing Dot writing workflows without replacing them.
---

# Usage

JJ Writer is a voice/style layer, not a writing workflow. Do not run a separate intake, structure, or multi-phase wizard here.

## Relationship to Existing Skills

| Skill | Role | JJ Writer's job |
|-------|------|-----------------|
| `jj-writing` | Draft development from ideas, notes, outlines | Apply voice calibration before final draft; style-check and Humanizer after |
| `docs` | Google Doc creation and handoff | Apply JJ Writer when doc content is in Jarad's voice |
| `humanizer` | Remove AI-writing tells | Required final pass via [humanizer-gate](humanizer-gate.md) |
| `jj-brief`, `jj-brainstorm`, `jj-steelman` | Distillation, exploration, pressure-testing | Do not substitute JJ Writer for these; apply JJ Writer only if output will be published or sent as Jarad |

## Standard Companion Sequence

When any skill or task produces content for Jarad:

1. **Classify** — email, short-form, long-form, proposal/client note, internal note, or revision-only.
2. **Load voice** — [voice-dna](voice-dna.md) + [jarad-style-guide](jarad-style-guide.md); add [email-voice-profile](email-voice-profile.md) for email.
3. **Draft or revise** — use the active skill's normal process.
4. **Style-check** — run [style-check](style-check.md) on near-final text.
5. **Humanizer** — run [humanizer-gate](humanizer-gate.md) before handoff.

## Content-Type Routing

| Type | Load | Notes |
|------|------|-------|
| Email, reply, follow-up | voice-dna, jarad-style-guide, email-voice-profile | Short paragraphs, clear next step |
| Short-form (social, quick take) | voice-dna, jarad-style-guide | State opinion early; stay specific |
| Long-form (article, essay, post) | voice-dna, jarad-style-guide | Build toward thesis; do not front-load |
| Proposal, client note, sales | voice-dna, jarad-style-guide, email-voice-profile if email-shaped | Grounded, useful, no hype |
| Revision-only | voice-dna, jarad-style-guide (+ email profile if email) | Preserve meaning; fix voice drift |

## What JJ Writer Does Not Do

- Replace `jj-writing` intake, structure, draft, or revision nodes
- Invent a new multi-phase writing wizard
- Send outbound messages without explicit approval (Dot outbound rules still apply)
- Write to workspace root or edit `HUMAN.md` / `human/` unless explicitly asked

## Quick Triggers

- "Write this as me" / "in my voice" → load JJ Writer nodes, then draft
- "Does this sound like me?" → style-check only
- "Humanize this" → humanizer-gate (Humanizer skill handles the pass)
- "Email to [person]" → load all three voice nodes, draft, style-check, Humanizer
