# Diagram Routing and QA

Use this reference to choose the form, keep it easy to read, and review the
actual FigJam result before handoff.

## Contents

1. [Start with the reader's question](#start-with-the-readers-question)
2. [Choose a diagram family](#choose-a-diagram-family)
3. [Preserve each form's meaning](#preserve-each-forms-meaning)
4. [Choose the renderer](#choose-the-renderer)
5. [Apply the visual defaults](#apply-the-visual-defaults)
6. [Run the review](#run-the-review)
7. [Use independent review when risk is higher](#use-independent-review-when-risk-is-higher)
8. [Handle fallbacks and partial states](#handle-fallbacks-and-partial-states)

## Start with the reader's question

A diagram earns its place when location, order, connection, containment, or
time makes the answer easier to understand.

Use something simpler when it does not:

- Use prose for one conclusion or explanation.
- Use numbered steps for a short linear sequence with no meaningful branching.
- Use a table for exact values, dense wording, or side-by-side comparison.
- Use a chart rather than a node diagram when quantitative magnitude or trend
  is the main message.

One overview answers one question. Put supporting detail in one adjacent
section rather than forcing it into the same network.

## Choose a diagram family

| Reader's question | Default | Variant when needed | Common mistake |
|---|---|---|---|
| How should choices or capabilities lead to outcomes? | Strategy or outcome logic map | Roadmap when timing matters | Drawing intended logic as proven causality |
| Which option should we choose? | Comparison or decision matrix | Decision tree for sequential conditional rules | Using a Venn diagram for generic comparison |
| What happens next, and who owns it? | Process flow | Swimlanes for owners and handoffs; BPMN only for formal process work | Mixing current and desired states |
| What connects to or depends on what? | System or dependency map | Context or UML view for a technical audience | Mixing process order with system relationships |
| What happens when? | Timeline | Gantt for duration and dependencies | Inventing false date precision |
| Who or what contains, owns, or reports to what? | Hierarchy or tree | Org chart for people; mind map for exploratory grouping | Mixing reporting, collaboration, and influence |
| What does one actor experience across one scenario? | Customer journey | Service blueprint for frontstage, backstage, and supporting work | Combining several actors or inventing emotion |
| What may cause this outcome? | Causal map | Cause tree for elicitation; DAG for acyclic assumptions; causal loop for feedback | Treating arrows as proof |

Treat these as families, not an exhaustive template list. Choose the form from
the relationship, even when the user starts with a different template name.

## Preserve each form's meaning

### Strategy or outcome logic

- Separate activities, outputs, and outcomes.
- Label assumptions or contextual conditions.
- Treat arrows as intended logic unless evidence establishes causality.

### Comparison or decision

- Name the comparison criteria before placing options.
- Use the same criteria for every option.
- Use a tree only when one answer determines the next question.

### Process or swimlane

- Show a start, meaningful steps, decisions, and an end or repeat state.
- Give each edge one clear direction.
- Add lanes only when ownership or handoff is part of the question.
- Keep exceptions subordinate to the primary path.

### System or dependency

- Keep nodes at one level of abstraction.
- Label edges with relationship verbs such as `feeds`, `depends on`, or
  `publishes to`.
- Remove decorative connections that do not answer the question.

### Timeline or Gantt

- Distinguish known dates from targets or estimates.
- Use a timeline for sequence and milestones.
- Use Gantt only when duration, overlap, and dependency matter.

### Hierarchy

- Use one containment or reporting meaning for the primary edges.
- Put collaboration or influence in a separate, clearly labeled style only
  when essential.

### Customer journey or service blueprint

- Use one actor and one scenario per journey.
- Show phases and observable actions before adding thoughts or emotions.
- Do not invent sentiment.
- Add frontstage, backstage, and supporting lanes only when delivery alignment
  is the question.

### Causal reasoning

- Mark causal links as assumptions unless evidence supports them.
- Keep a DAG acyclic.
- Mark polarity and meaningful delays in a causal-loop diagram.
- Do not disguise a generic relationship map as a causal model.

## Choose the renderer

| Situation | Route |
|---|---|
| Any live diagram where exact repair, reliable readback, or widget-free handoff matters | native `use_figma` |
| Small new supported diagram where automatic layout materially helps and the inline app resource is healthy | `generate_diagram` |
| Supported generated structure plus a few purposeful native additions | hybrid |
| Read-only tools or no edit permission | diagram specification and handoff |
| No Figma connection | portable manifest and Mermaid only when the type supports it |

Load the installed Figma skills before calling their tools. Their instructions
override remembered API behavior.

## Apply the visual defaults

### Meaning and hierarchy

- Start with one plain-language thesis near the entry point.
- Use one dominant left-to-right or top-to-bottom reading direction.
- Make the current or primary path visually dominant.
- Make alternate, future, emerging, assumed, and unsupported paths secondary.
- Use one concrete example when the form is unfamiliar.
- Keep explanations beside the node or edge they explain.

### Labels and keys

- Prefer short nouns for nodes and short verb phrases for edges.
- Keep a node label to about two lines when possible.
- Use no more than three meaningful edge styles in one overview.
- Keep the key small and one-to-one: every entry is used and every special
  mark is explained.
- Never use color as the only cue. Pair it with text, shape, fill, border, or
  line style.

### Layout and density

- Target zero edge crossings. If a crossing is unavoidable, make the paths
  visually unambiguous.
- Keep related nodes close and different ideas visibly separated.
- Prefer adding height to a board over forcing a wide scan, unless a truthful
  continuum needs horizontal space.
- If one path requires panning in both axes, split the view.
- Use an overview plus one adjacent detail level rather than several layers of
  hidden or distant explanation.

Treat these as warning thresholds, not laws:

- about 12 primary overview nodes;
- about 20 edges;
- more than 4 logical columns;
- more than 5 lanes;
- more than 7 journey stages.

Crossing a threshold should trigger compression or overview-plus-detail, not an
automatic failure.

### Reader-fit defaults

- Lead with meaning before mechanics.
- Externalize sequence, status, dependencies, and comparison criteria.
- Reduce visual scanning and arbitrary symbols.
- Reuse stable names and a shared visual grammar.
- Do not simplify away the intellectual distinction the diagram must preserve.
- Treat any supplied cognitive or accessibility profile as a design lens, not
  a diagnosis or content for the board.

## Run the review

Do not show the first canvas draft as finished.

### Pass 1: Semantic

Compare the source, manifest, and canvas:

- one audience and one question;
- title and thesis match the actual start and end scope;
- canonical nouns and labels;
- every node and edge source-backed;
- every source fact needed by the audience is present or named under Excluded
  detail; compression has not erased explicit owners, entry channels, or
  disposition states;
- direction, ownership, order, containment, and truth status correct;
- current and proposed states distinct;
- no invented completion, causality, sentiment, or universal path;
- correct primitive: path, state, category, continuum, hierarchy, or matrix;
- no deliverable, example, or annotation promoted into a primary stage.

### Pass 2: Structural

Read back the target subtree:

- expected node and connector counts;
- exact labels and no placeholders;
- correct parents and section containment;
- connector start and end IDs match the manifest;
- arrow caps and visible edge text are correct;
- no orphans, duplicates, or detached labels;
- section bounds contain every child;
- returned changed IDs stay inside the approved target;
- existing geometry diff is empty unless the user approved exact edits.

### Pass 3: Visual

Inspect two screenshots:

1. Overview: entry point, thesis, grouping, hierarchy, and reading direction.
2. Readable section: every label, connector endpoint, key, and annotation.

Check:

- truncation, ellipses, clipping, and overflow;
- overlaps and crowded shared anchors;
- ambiguous endpoints, unnecessary bends, and edge crossings;
- spacing, alignment, relative size, and color contrast;
- key-to-mark consistency;
- primary story visible before secondary paths;
- section bounds and no accidental content at the canvas origin.

### Pass 4: Compression

- Delete words that do not change understanding.
- Shorten labels and remove repeated connector prose.
- Collapse truthful repeat loops into one subordinate repeat opportunity.
- Remove annotations that only repeat a node label.
- Split the diagram when the overview cannot stay readable.

### Pass 5: Repair and integrity

- Fix the smallest set of nodes that resolves each defect.
- Repeat structural readback after any relationship or containment change.
- Repeat both screenshots after any layout, type, color, or label change.
- Claim completion only after final readback and screenshot inspection pass.

## Use independent review when risk is higher

Use a separate reviewer when any of these apply:

- existing-board write;
- branching, lanes, or a legend;
- current-versus-future distinction;
- a novel or uncertain visual primitive;
- external or team audience;
- the overview remains near a density warning after compression.

Give the reviewer:

- authoritative source material;
- the manifest;
- target subtree readback;
- overview and readable screenshots;
- the review sections above.

Do not give the reviewer the intended verdict or suspected defect. Ask it to
return only concrete semantic, structural, visual, and compression findings.
The builder owns repairs and final verification.

For a small linear diagram without these risks, the builder may perform a
fresh second pass itself.

## Handle fallbacks and partial states

- If authentication, seat, or destination is unclear, resolve it before write.
- If the user has several eligible plans, ask once which plan to use.
- For a new native board: `whoami` -> resolve `planKey` ->
  `figma-create-new-file` -> `create_new_file(editorType: figjam)` ->
  `use_figma` with the returned `fileKey`.
- If the write tool is unavailable, give a specification; do not say the board
  exists.
- In a specification-only handoff, recount the manifest's nodes and edges and
  omit link or section placeholders. A missing destination is a state, not a
  fake `none` URL.
- If `ui://widget/figjam-diagram.html` fails, route the run to native
  `use_figma`. The failed widget is presentation state, not proof that a write
  failed or succeeded.
- If a generated write returned a file URL, use `get_figjam` to prove the
  target nodes exist before calling it created, then return the plain Markdown
  link rather than the widget.
- If a generated base lands but native extension fails, report the base as
  created and the extension as failed.
- Stop blind retries. Inspect the error and current state, then make one
  targeted correction.
- After two unresolved attempts at the same layout defect, ask for the one
  specific correction needed.
- Reuse the same FigJam file for revisions to avoid stray drafts.
