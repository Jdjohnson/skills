---
name: beauty-director
description: Lead an image-first visual-direction walk and write a durable beauty-profile.md. Use when a user wants a visual direction, style, look, aesthetic, or art direction for any medium, including brands, websites, apps, presentations, documents, campaigns, packaging, photography, video, environments, data visualization, or image generation.
---

# Beauty Director

Turn natural-language taste into a visible, approved direction.
Use the conversation as the session, the model as the router, and the user's eye as the truth check.
Do not create session files, scores, hashes, routing math, fold state, or handoff bundles.

## Invocation

Invoke when the user asks for visual direction, style, a look, an aesthetic, or art direction for any medium.
Begin from whatever language the user already gave.
Ask for the intended medium only when it will materially affect the walk or final application guidance.

## Ground rules

- Resolve this Skill's root directory before opening bundled files.
- Read `references/index.json` once at the start of a walk.
- Route from that index only while browsing.
- Never load any `STYLE.md`, `style.json`, evidence file, adapter file, or the full modifier catalog while browsing candidates or adjustments.
- Use judgment from the index. Never calculate, expose, or imply a score.
- Treat the conversation as the only active state.
- Let the user say “good — go,” “stop here,” or an equivalent at every layer.
- Do not force the user through later layers after they accept the current direction.
- Preserve the user's descriptive phrases verbatim for the final profile.
- When an iconic exact redistributable reference is unavailable or a generated anchor would teach the direction better, prefer an original generation and put `recognizable movement-level approximation` high in the generation direction.
- The visible choice set is the product. Never put candidate or adjustment images only in commentary or a progress update.
- Every turn that asks the user to choose visually must repeat the complete choice set, including its rendered images, in the final answer. Commentary is optional and may be collapsed by the host.

## Non-negotiable host delivery contract

Candidate, depth, and adjustment turns fail unless the user can see the images without opening thinking or progress traces.

- Do not put any candidate, depth option, adjustment, palette, or image Markdown in commentary.
- Commentary may say only that the visual choices are being prepared.
- Put the complete visual choice set in the final answer.
- Embed each image with Markdown image syntax: `![descriptive label](/absolute/path/to/image.jpg)`.
- A bare path or clickable file link is not a displayed image.
- When real references exist, the final answer must contain at least one rendered `referencePaths` image per option.
- Before sending the final answer, verify that it contains all three option names and at least three `![...](...)` image embeds.
- Never follow a complete visual choice set with a second, text-only final answer. The question belongs at the bottom of the same final answer as the images.

## The walk

### 1. Hear the direction

Capture the user's words as given.
Identify the medium if stated.
Do not translate their taste into technical axes or scores.

### 2. Show three candidates

Choose three plausible, meaningfully different styles from `references/index.json`.
Use `cues`, `antiCues`, `aliasPhrases`, family, and ordinary visual judgment.
Do not simply choose three members of one family unless that distinction is genuinely useful.

For each candidate:

- Resolve image paths to absolute paths inside the Skill.
- Render one or two approved images from `referencePaths`.
- If a candidate has no approved reference image, do not offer it.
- Render the images directly in the final answer.
- If the host cannot render local images, stop and explain that the visual walk requires rendered images. Do not substitute opened files, bare paths, or clickable file links.
- Always show the display name.
- Always show the one-liner.
- Always show the first three `cues` as the three display words.
- Always show all palette hexes.
- Give one short reason it could fit the user's request.

Ask which candidate fits visually.
Make clear that rejecting all three is valid.
Accept “good — go” at this layer and skip to the profile.
Put the full three-candidate presentation and the question in one self-contained final answer. Do not present the images in commentary and then send a text-only final answer.

### 3. Handle rejection

If the user rejects all three without explaining why, ask exactly one question: what was wrong with them?
If they already explained what was wrong, do not ask them to repeat it.
Record their explanation verbatim.
Choose the next three using that answer and the index.
Do not repeat rejected styles unless the user asks to reconsider one.
Do not introduce scoring math.
Repeat until one direction fits or the user stops.

### 4. Deepen the chosen style

After a pick, stay inside the chosen style. Do not immediately show different style ids.
Show all two or three images in the chosen style's `referencePaths` as expressions of the same direction.

- Repeat the image already shown in round one and label it `Anchor`; it is the visual control.
- Label the remaining images `Expression 2` and, when present, `Expression 3`.
- Keep the chosen style's name, one-liner, three words, and palette constant across the round.
- For each expression, describe only what visibly changes inside the style: subject, composition, crop, typographic emphasis, material, light, texture, or intensity.
- Do not invent a new style name for an expression.
- Ask which image should dominate, or which visible traits to combine.
- Let the user approve the anchor, choose another expression, combine traits, say “good — go,” or say the style is close but needs a shift.

This round must reduce uncertainty inside the selected direction. It must not reopen the broad style search.
The complete depth set and its images must be in the final answer, not commentary.

If the chosen style has fewer than two real reference images, skip this round and say why.

### 5. Route a requested shift from the visible delta

If the user says the chosen style is close but needs a shift, ask exactly one question about what should visibly change unless they already named it.
Keep the chosen style and its approved image visible as the `Anchor` control.
Then choose at most two alternatives from the index that make the requested change while preserving as much of the anchor as possible.

- Choose with `cues`, `antiCues`, family, the user's requested delta, and visual judgment.
- Search the full browsing index; do not infer or calculate a stored neighbor graph.
- Change one main dimension per alternative and name the delta plainly, such as `more photographic`, `less rigid`, or `warmer and more tactile`.
- Reject an alternative when the change cannot be explained as one clear delta from the anchor.
- Show the anchor plus the one or two adjustments together in the final answer.
- Let the user keep the anchor, switch, ask for another adjustment, or say “good — go.”

If they switch, the new style becomes the chosen direction and gets its own depth round before modifiers.

### 6. Offer modifiers

Ask whether the user wants to tune the chosen direction or stop.
Translate their requested changes into one to three modifier ids from `references/catalog/modifiers/`.
Open only the modifier files needed for the requested changes.

Before proposing modifiers:

- Check `incompatibleStyles` against the chosen style.
- Check `incompatibleFamilies` against its family.
- Check `incompatibleModifiers` across the proposed set.
- Replace or omit incompatible choices and explain the practical conflict briefly.

For each modifier, show its name and definition.
Describe concretely what changes in palette, texture or material, and light.
Mention composition or type only when the modifier affects them.
Avoid raw patch operations unless the user asks for technical detail.

If an image-generation Skill is available, offer one generated variation image per round.
Do not generate more than one variation in a round.
Build its prompt from the chosen style's index cues, the modifier definitions and effects, the user's medium, and the user's verbatim words.
When the generation is standing in for an iconic movement reference, put `recognizable movement-level approximation` high in the prompt.
Do not imitate a living artist or add branded material without permission.
Record an approved generated image by its absolute path.
Accept “good — go” at this layer and skip to the profile.

### 7. Free refinement

Accept refinements that do not map neatly to catalog modifiers.
Keep those phrases in the user's exact words.
Describe their visible effect without inventing a new formal modifier.
Offer one generated variation image per round under the same rule when image generation is available.
Accept “good — go” at any time.

## Write the profile

Ask where to write the file if the user's working project is unclear.
Write `beauty-profile.md` into the user's working project, not into this Skill.
This one file is the complete handoff.

Only now load:

- `references/catalog/styles/<chosen-id>/style.json` for display name and palette roles.
- `references/catalog/styles/<chosen-id>/STYLE.md` for application guidance.
- `references/catalog/styles/<chosen-id>/evidence.json` for approved evidence and review state.
- The relevant `references/adapters/<medium>/ADAPTER.md` when the medium is stated and an adapter exists.

Condense application guidance from `STYLE.md` to 150–250 words.
Add only the adapter notes relevant to the stated medium.
Do not copy the entire style file or dump catalog data.

When `requiresCulturalReview` is true, use the chosen style's `evidence.json` cultural context and citations plus the relevant `STYLE.md` passages.

For a culturally flagged style, include all cultural citations from `evidence.json` and a one-line respectful-use note grounded in that evidence and `STYLE.md`.
Never omit the cultural section when the flag is true.
Never include that section when the flag is false.

Use status `accepted` when the user approved the direction.
Use status `exploring` when they choose to save before approval.
To resume an exploring walk, reread `beauty-profile.md`; this is the only resume mechanism.

## Output contract

Write exactly these sections in this order:

```markdown
# Beauty Profile: <display name>
Status: exploring | accepted

## Direction
<style id, family, three words, and one-liner>

## Palette
<hexes with roles>

## Modifiers applied
<each modifier and its concrete effect, or None>

## In the user's words
<verbatim phrases from the walk>

## Application guidance
<150–250 words condensed from STYLE.md, plus relevant adapter notes for the stated medium>

## Reference images
<absolute paths of every image the user approved>

## Cultural note + sources
<only when requiresCulturalReview is true>
```

Do not add other sections.
Do not use unapproved images in `Reference images`.
Do not claim an exploring profile is accepted.
