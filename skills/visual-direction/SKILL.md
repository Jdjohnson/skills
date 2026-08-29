---
name: visual-direction
description: Lead an image-first visual-direction walk, refine an approved direction, and optionally record it for a project. Use for art direction, style, look, aesthetic, or cross-medium visual language.
---

# Visual Direction

Use the user's eye as the approval authority. Preserve their descriptive language verbatim. Keep routing scores, hashes, neighbors, and review machinery internal.

## Browse

Resolve this skill's root and read only `references/index.json` before approval. Ask for the medium only when it would materially change the walk.

Choose exactly three eligible, meaningfully different styles from cues, anti-cues, aliases, family, and judgment. Require approved display references. For each show:

1. rendered reference image;
2. style name;
3. one plain-language reason it fits; and
4. `Take:` / `Ignore:` guidance based on visible traits.

Ask which is closest and what to carry forward. Do not ask the user to score dimensions or inspect catalog metadata.

If all are rejected without a reason, ask only: “What was wrong with them?” If the reason is given, quote it, exclude the rejected IDs, and show three genuinely new directions in the same response. Continue until one fits or the user stops; never relabel a rejected reference.

## Refine

After a style is chosen, identify the next visible decision—such as composition, color, material, type, image treatment, motion, or density. Show at most three useful variations and keep the approved anchor visible. Lock only what the user explicitly accepts. Distinguish proposed from approved.

Use requested modifier files only when they materially clarify an effect. Describe freeform refinements in natural language without inventing a catalog modifier.

If image generation is available, offer at most one real variation per round. Generate only with the user's agreement, use the chosen cues and user language, and record only an approved result. Never fabricate an output, imitate a living artist, or introduce a brand without permission.

## Evidence and cultural boundary

Provenance, image integrity, lawful display terms, cultural evidence, attribution, and human visual review are hard gates. Do not offer a catalog item that lacks them. For culturally rooted directions, retain the evidence-grounded respectful-use note and citations. Use movement- or tradition-level language; do not imply ownership, authenticity, or endorsement that the evidence does not establish.

## Record the result

Save only when the user asks and the destination is clear. Then load the selected `style.json`, `STYLE.md`, `evidence.json`, and only the relevant medium adapter. Write exactly one `visual-direction.md` outside this skill:

```markdown
# Visual Direction: <plain name>
Status: accepted | exploring
Medium: <medium>

## Direction
<150–250 words grounded in STYLE.md and accepted user language>

## Locked qualities
<only explicitly accepted qualities>

## In the user's words
<verbatim phrases>

## Approved references
<rendered approved paths with required credit>

## Application notes
<relevant adapter guidance only>

## Avoid
<accepted negatives or None>

## Cultural context
<only when required: respectful-use note and citations>
```

Use `accepted` only after approval; an explicitly requested early save remains `exploring`. Resume from the saved file without dumping the full catalog.
