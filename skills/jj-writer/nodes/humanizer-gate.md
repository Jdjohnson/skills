---
description: |
  Mandatory Humanizer pass before handoff for content written as or for Jarad.
---

# Humanizer Gate

Any time the AI drafts or rewrites text **on Jarad's behalf**, run Humanizer before final handoff unless Jarad explicitly opts out.

## Required Pass

Before showing near-final content to Jarad or saving it as a send-ready draft:

1. Load the installed **humanizer** skill (or apply `/humanizer` in the agent UI).
2. Default to **rewrite** mode unless Jarad asked for audit-only diagnostics.
3. Preserve meaning, facts, intent, and Jarad's directness, specificity, and edge.
4. Do not neutralize strong opinions into generic prose.

Humanizer removes AI-writing tells. JJ Writer nodes define Jarad's voice. Both apply; they are not interchangeable.

## Conflict Order

If Humanizer and JJ Writer guidance conflict:

1. **Meaning** — do not change the claim unintentionally
2. **Jarad voice** — practitioner tone, controlled informality, specificity
3. **AI-pattern cleanup** — remove tells without flattening voice

## Opt-Out

Skip Humanizer only when Jarad explicitly asks for:

- a rough/raw draft
- a deliberately unpolished pass
- audit-only style review without rewrite

If skipped, say so briefly in the response.

## Sequence with Style Check

Recommended order on near-final content:

1. [style-check](style-check.md) — Jarad-specific voice drift
2. Fix any **REVISE** blockers from style-check
3. **Humanizer** — final AI-pattern cleanup
4. Handoff to Jarad (still draft-only for outbound until explicit send approval)

## Humanizer Constraints for Jarad Content

- Preserve core meaning and argument
- Keep specifics, edge, and natural rhythm
- Do not add fake specificity, fake emotion, or unsupported claims
- Match register to context: casual, executive, technical, sales, internal, public
- For neutral, technical, or legal text, plain and direct is the human voice

## Integration

- JJ Writer does not duplicate Humanizer's pattern library; it **requires** Humanizer as the final gate.
- `jj-writing` and other drafting skills produce the draft; JJ Writer + Humanizer polish it for Jarad's voice.
