---
name: visualize
description: Turn settled discussions or supplied sources into the simplest useful, editable FigJam diagram, with semantic, structural, visual, and compression review before handoff. Use only when the user explicitly invokes `$visualize`; do not trigger for ordinary explanation, planning, analysis, or requests that merely mention diagrams.
---

# Visualize

Turn a settled verbal model into a sparse, audience-fit FigJam diagram. Do not
make the reader decode the first spatial draft.

Read [diagram routing and QA](references/diagram-routing-and-qa.md) fully before
choosing a form or writing to FigJam.

## Flow

| Step | Purpose |
|---|---|
| Frame | Name the audience, one question, source of truth, target, and truth status |
| Settle | Resolve only gaps that would change the model |
| Route | Choose the simplest fitting diagram or recommend no diagram |
| Specify | Write the compact node-and-edge manifest before drawing |
| Inspect | Check Figma access and the destination's existing visual language |
| Build | Create one bounded section in small, verified steps |
| Review | Check meaning, structure, screenshots, and simplicity; then revise |
| Deliver | Return the link, IDs, QA result, integrity result, and limitations |

## Core Contract

- Run only after explicit invocation. A request that merely discusses visuals
  or FigJam is not enough.
- Treat the active conversation and supplied sources as the starting evidence.
  Read the authoritative material rather than reconstructing it from memory.
- Use one audience and one question per overview. Split detail when one view
  would obscure the primary message.
- Ask one short question at a time only when the answer changes the model,
  target, or truth status. Continue without ceremony when the model is settled.
- Prefer prose, numbered steps, or a table when position, order, connection,
  containment, or time carries no useful meaning.
- Put only reader-facing subject matter on the canvas. Keep prompts, sources,
  uncertainty logs, QA notes, and process commentary off the board.
- Never invent a node, relationship, owner, causal claim, current state, or
  desired state to make the diagram look complete.

## Apply the No-Diagram Gate First

Decide whether spatial structure carries meaning before checking Figma access,
plans, or destinations. Explicit invocation is permission to make this
judgment, not an instruction to force every request onto a canvas.

- If position, order, connection, containment, or time does not improve
  understanding, return the simpler prose, numbered steps, table, or chart and
  stop.
- Do not ask for a Figma plan or destination after choosing no diagram.
- For exact arithmetic or side-by-side values, default to a table unless a
  spatial relationship is itself the question.

## Set the Mutation Boundary

Explicit invocation authorizes the requested diagram, not an arbitrary
destination.

- Use the supplied FigJam board or section when one is named.
- If a new board is needed and more than one eligible plan is available, ask
  which plan to use before creating it.
- If the user asks for a plan or draft specification first, stop before any
  live write.
- For an existing board, add one new section unless the user explicitly asks
  to edit existing content. Record existing node geometry before writing.
- Reuse the same file for revisions. Ask before deleting an earlier version;
  otherwise keep the new version beside it.

## Specify Before Drawing

Prepare a compact working manifest:

```text
Audience:
Question:
Thesis:
Type and reading direction:
Nodes:
Edges and edge meanings:
Groups or lanes:
Observed / sourced / assumed / proposed:
Key:
Excluded detail:
Target board and section:
```

Keep the manifest in working context or temporary local material. Do not paste
it onto the board. If the manifest exposes an unsettled relationship, resolve
that relationship before drawing.

Treat facts and relationships stated directly by the user as supplied evidence,
not assumptions. Mark only an inference or added interpretation as assumed.

## Choose the Figma Route

Discover the current Figma tools instead of assuming they are available.

- Before `use_figma`, load the current `figma-use` and
  `figma-use-figjam` skills and follow them as the API source of truth.
- When native rendering needs a new board, call `whoami`, resolve the plan
  under the mutation boundary above, load `figma-create-new-file`, create one
  FigJam file, and pass its returned `fileKey` to `use_figma`.
- Before `generate_diagram`, load the current `figma-generate-diagram` skill.
- Before writing portable Mermaid intended for later Figma generation, load
  `figma-generate-diagram` and its type-specific reference too.
- Use native `use_figma` as the default live renderer. It supports exact
  styling, scoped repair, structural readback, and a widget-free handoff.
- Use `generate_diagram` only when automatic layout materially helps and its
  inline app resource has been proven healthy in the current runtime.
- Use a hybrid only when the generated base saves real work and the native
  additions remain small.
- If `ui://widget/figjam-diagram.html` fails to load, stop using
  `generate_diagram` for that run. Build natively with `use_figma` instead.
- If `generate_diagram` already returned a file URL before its widget failed,
  verify the created nodes with `get_figjam` and hand off the plain Markdown
  link. Do not regenerate solely because the presentation widget failed.
- If live tools or edit permission are unavailable, return a read-only
  specification or portable handoff. Do not claim a canvas mutation.
- Return fallback material inline unless the user asks for a durable local
  file. Keep any temporary working artifact out of the user's project records.

The Figma skill may recommend sharing a generated base immediately. Do not do
that here. Show the diagram only after the required review and repair pass.

## Build and Review

1. Inspect the target with `get_figjam` and a scoped style read when it already
   contains content.
2. Match canonical names, fills, strokes, type, relative sizes, connector
   semantics, key, and nearby spacing.
3. Build one named section incrementally: structure, nodes, connectors, reflow.
4. Return every created or changed node ID from each write.
5. Run the full review in the reference:
   - semantic check against sources and manifest;
   - structural readback;
   - overview screenshot;
   - readable section screenshot;
   - compression pass;
   - targeted repair and final recheck.
6. Use an independent reviewer for a complex or externally shared diagram. Give
   the reviewer the sources, manifest, readback, screenshots, and QA rubric,
   not the intended answer. The reviewer identifies defects; the builder edits.
7. In Claude Code, do not preload this manual-only skill into the reviewer.
   Pass the artifact and rubric directly.

Do not treat delegation, a successful write call, or a plausible screenshot as
proof. Completion requires final readback and visual inspection.

## Handoff

Keep the receipt short:

```text
Open the FigJam section: <URL>
Type: <diagram type>
Section: <name and ID>
QA: <main fixes and final result>
Integrity: <existing content unchanged, or exact approved edits>
Limitation: <none, or the remaining constraint>
```

Use exact states. A specification is prepared, not created. A base diagram
without its planned extension is partial, not finished.

When nothing was created, omit the empty link template. Say `State:
specification prepared; no board created`, give accurate node and edge counts,
and do not present `none` as a destination or URL. Count once from the final
manifest and never print a conflicting count or parenthetical correction.

## Example

Input:

> `$visualize` Turn the service discussion above into a FigJam diagram for
> the internal team.

Expected behavior: settle the one client-movement question, choose a journey or
service-system form from the reference, use canonical service names, build a
dominant current path with secondary options, review and revise it, then return
the targeted section link and QA receipt.
