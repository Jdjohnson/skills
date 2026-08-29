# Photography Profile and execution handoff

Return the accepted result in chat. Save exactly one
`photography-profile.md` only when the user asks and the Destination is clear.
The user's pictures and accepted direction are the source of truth; a catalog
look name is never a substitute for them.

Use this order:

```markdown
# Photography Profile: <plain direction name>
Status: ready | prepared but blocked | incomplete

## Shared direction
<one short sentence naming the kind of photograph and intended outcome>
Must-stays: <direct requirements that survive every destination>
Avoid: <hard negatives and anti-cues>
Aim-point: <accepted visual aim, or Coverage gap: no complete visual aim>
Open: <one or two unresolved decisions>

## Locked qualities
<visible lighting character, depth, tonality, texture, composition intent, and mood>

## Adaptive guidance
<operational perspective, distance, framing, focus, light, and reflection guidance>

## In the user's words
<verbatim accepted phrases>

## Approved references
<real references rendered as ![alt](<absolute-local-path>), with exact credits directly below each>

## Execution handoff
<only the requested destination handoff(s), using the contracts below>

## Avoid
<only anti-cues needed to prevent obvious drift, or None>
```

`Shared direction` is destination-neutral and is the single source of truth for the picture sentence,
Must-stays, Avoid, Aim-point or Coverage gap, and Open questions. It contains no
provider-specific prompt syntax, photographer booking or pricing logistics, or
invented technical facts. Keep supplied source roles internal. Explain each
reference with plain take/ignore language using only visible traits or user-stated
negatives. For every component, state the critical target attributes it does not
prove. A press/photo-op or component study may show a pose, gesture, room, or
camera relationship; it does not prove collaboration, authenticity, spontaneity,
or a shared task. Do not turn an anti-reference's absent trait into an Avoid.

## Progress and lifecycle

The user does not need to complete a form or learn role names. Distinguish the
internal objects `Direction candidate`, exact `Working reference`, `Approved
target`, `Current result`, `Generated combination study`, and `Destination`.
Track readiness as `visual aim present` or `visual aim absent / coverage gap
acknowledged`. Selection is not approval. A component board is pieces of the picture, not a
target. A real-photo Approved target requires explicit user acceptance of a
same-genre visual aim or reference board.

An assistant-offered reference rejected in an explained reject-all is
identity-bound in the immediate recovery. Preserve its exact ID and rendered
path in `--exclude` and carry that exclusion through routing; relabeling the
image, role, caption, or treatment does not make it eligible again, and its
paired treatment ID is excluded as well. A partial-fit treatment, place, or
action reference remains a `component study`: it cannot be called a Working
reference, anchor, Approved reference, or target unless it fully satisfies the
controlled constraints or the user explicitly approves that role.

Only a user-accepted complete visual Aim-point/Working reference permits refine/profile or `--anchor-ref`. Direct component-board handoff without it: do not run refine/profile or pass `--anchor-ref`; supplied refs+direction may skip looks, read contract, issue text-led `Coverage gap`; components stay Take/Ignore only, never Working reference/anchor; catalog profile axes/avoid/adapt never override user roles.

Explained reject-all recovery passes `--recovery` with `--exclude`. If those
exclusions exhaust the closer subject set, the query returns zero assistant
references/results with `coverageGap.status: recovery-exhausted`; response prose
may preserve only user-supplied or provisionally-approved structural fallback.
The query invents no structural fallback.

At each transition, explain what is being shown, why, what is locked, what is
open, and one next decision. Refinement keeps the exact Working reference
visible, changes one visible bet, and says `Closer:` and `Still unresolved:`. If
no new visual evidence exists, say `No visual progress yet` or `Coverage gap`.
Text alone never counts as visual refinement.

`Locked` may contain only constraints the user explicitly stated or explicitly
accepted; assistant-proposed actions/styles remain `Options`/`Proposed` until
accepted and cannot silently become locks.

After an explained reject-all or correction, the same response must visibly
advance. When the reason is actionable (a named visual delta, subject, setting,
action, hard exclusion, or a visual defect such as “they feel stock,” “generic,”
or “staged”), render a genuinely new closer real route with a new reference ID/path when eligible; if none exists, only a user-supplied or already user-provisionally-approved structural reference may be a role-scoped study with `Coverage gap: ...`, and it is non-anchor. Route toward a specific visible human moment
without asking the user to restate the request.
Never recycle or relabel an assistant-offered rejected reference. Carry its exact
ID/path and paired treatment through `--exclude`. Do not add a diagnostic
question to that response. If the phrase supplies no visual reason, ask one
diagnostic question only for that unexplained reject-all.

When two supplied images are versions or crops of the same underlying source,
disclose `Non-independent variants` and count them as one evidence source. They
cannot satisfy independent coverage or confidence.

## Execution modes

Infer Destination only from user evidence: naming the recipient/use, supplying
self-shoot equipment, uploading a generated result, or explicitly choosing a
mode. Once known, preserve `executionMode` and `outputContext` on every query,
including supplied-result analysis. Do not assume AI as a default. If unknown,
ask once: `AI generation`, `a photographer`, `self-shooting`, or `both`; say that
the answer immediately finalizes the preserved direction and handoff. Ordinary
acceptance does not silently select AI; if the destination remains unknown, ask
again rather than choosing one silently.

### Destination readiness

Before calling a handoff execution-ready, resolve every destination blocker the
user made material. For a material website hero, exact aspect ratio/crop family
and copy-space direction are required; if unresolved, label that handoff
`prepared but blocked`, not accepted/final. Optional preferences are not
blockers. Before any final handoff, compare each `Locked`/`Must-have`, `Avoid`, `Option/Preference`, and blocker against user's exact stated/accepted constraints; move assistant-inferred ideas to `Proposed`/`Options`; every `Avoid` needs an exact user-stated anti-cue or visible anti-reference trait; unsourced/absence-derived qualifiers stay `Proposed`, never `Avoid`; resolve conflict or mark blocking. Final pre-send audit covers headings, prose, lists, image alt text, captions; invented qualifiers are removed, not paraphrased. Unstated retouching, depth, exact copy-space character, crew sufficiency, and similar production advice remain `Proposed`/`Options`, never settled discretion. Use `AI status: ready | prepared but blocked | incomplete` and `Photographer status:
ready | prepared but blocked | incomplete`; `incomplete` means required branch proof or input is missing.

### AI Prompt Kit

Return one copy-ready Portable prompt and a short execution note. The prompt is
an AI-only handoff; do not emit it in photographer-only or self-shoot-only
profiles. The Shared direction remains destination-neutral.

#### Portable prompt

Write one natural-language prompt, not a platform command:

```text
Create a photograph of {{SUBJECT}} in {{SETTING}}, {{ACTION}} if relevant,
composed for {{ORIENTATION}}.

Make it this kind of picture: <plain genre or photographic situation>. Preserve
these visible qualities: <approved Must-stays and locked qualities>. Use
<lighting character>, <depth behavior>, <composition intent>, <color/tonal
treatment>, and <texture/process appearance>.

Keep the subject's attention and visible action consistent with the Shared
direction. Use the role-bounded reference inputs as follows: <take from each;
ignore the stated contradictions>. Adapt perspective, lens class, relative
camera distance, framing, focus placement, and light position to make the scene
physically plausible while preserving the aim.

Avoid: <short anti-cue list>.
```

Keep the prompt concise enough to edit by hand. Prefer visible outcomes over
gear names. Do not include model variants, weights, seeds, aspect-ratio flags,
living-photographer imitation, exact camera bodies, exact lens measurements,
aperture, shutter, ISO, film stock, physical light source, capture process, or
generic filler unless that fact is genuinely confirmed/documented and
transferable. The bounded copy-ready block contains only generation
instructions and visual content. Keep `Generated combination study`, receipt
paths, input paths/roles, input hashes, acceptance, visual QA, and `AI status`
outside that block. Adapter preflight, output controls, and the generation
receipt stay outside the prompt too.

The AI branch requires an accepted visual Aim-point. If no complete real-photo
target exists, say `Coverage gap` and keep the AI handoff pending until the user
supplies or accepts an Aim-point. A generated image is a labeled study/result,
never real-photo proof. If offered, label it exactly **`Generated combination study`** and immediately add: “generated exploration; not a real-photo reference or final target.” Offer it only after the gap and component limits are shown and
the user asks for or agrees to that one visible experiment. Never generate to
fill a candidate quota or automatically after a rejection.

The AI Prompt Kit's short execution note may name viewpoint,
perspective/lens class, relative working distance, framing, depth/focus
behavior, light character and position, color, texture, and mood. Do not present
physical camera equipment or exact exposure as though appearance proves it. List
exact input paths and role boundaries, output, adapter or model preflight, and
receipt outside the prompt. Record `VISUAL ACCEPTANCE PENDING HUMAN CONFIRMATION`
until the generated output passes the visible checklist and the user accepts it;
a failed hard-lock result is `Failed generated result` and must preserve the
prior anchor without a content retry.

Record every study's exact submitted prompt, input paths in order with roles,
output, and receipt. `AI status: ready` is allowed only when the exact final
Portable prompt block itself was submitted, its output passed visual QA with
that receipt, and readable participant acceptance names that exact block.
Earlier or unpreserved prompts, receipt paths, hashes, or generated studies do
not prove readiness. Without that submission and acceptance, use `AI status:
incomplete` and name the missing proof.

### Photographer Brief

Make `Execution handoff` exactly this independently sendable commissioning brief
and fill every line:

```markdown
# Photographer Brief
Intended use: <outcome and story>
Must-haves (user-stated or explicitly accepted only): <subject, action, setting, composition, light, depth, finish>
Constraints: <access, privacy, screen/property content, releases, schedule, and blockers>
Approved references:
- Take: <each rendered reference, role, contribution, and proof limit>
- Ignore: <contradictions and what the reference does not prove>
Avoid:
- User: <exact user-stated anti-cue>
- Visible anti-reference: <visible trait only>
Proposed visual/production guidance: <room context, depth, crew, retouching, and other assistant recommendations>
Coverage to shoot: <hero alternatives; 3–5 candid environmental working supports; details; vertical only if requested>
Photographer discretion: <camera, lens, exposure, lighting, medium, position, focus, moments, crew, and feasible coverage>
Deliverables: <crop/orientation, selects, masters, exports, proofing, retouching, rights/usage, and priced options>
Confirm before quote/booking: <unresolved production or delivery choices; separate preferences and options>
Branch status: Photographer status: ready | prepared but blocked | incomplete
```

`Must-haves` carries only direct user requirements and visible anti-cues; every `Avoid`
line is `User:` or `Visible anti-reference:` only, with unsourced items omitted. `Approved
references` is the recipient-facing `Reference roles (Take / Ignore)` boundary:
render every component/target reference and say what it contributes, what to
ignore, and what it does not prove. Use visible anti-reference traits only; do not
invent an Avoid. `Constraints` must include known booking blockers. `Deliverables`
must cover crop/orientation, selects, masters, exports, proofing, retouching,
rights/usage, and priced options, but unasked retouching/depth/copy-space/crew
choices remain `Proposed`/`Options`, never `Must`/`Avoid` or settled discretion; invented
qualifiers are removed, not paraphrased;
put them under `Confirm before quote/booking` when useful.

State true blockers before booking. A text-led brief may proceed with `Coverage
gap` stated; this is not booking approval. The photographer chooses camera, lens,
exposure, lighting hardware, and crew unless the user supplied a genuine
production requirement. A perspective or lens-class hypothesis is a starting
conversation, not a specification. Do not call `ready` when a required section
is missing or a blocking production/delivery choice remains. Photographer status:
incomplete until a human cold readback confirms the independently sendable brief is
actionable; after that proof, booking/logistics blockers mean prepared but blocked;
ready requires that proof and resolved blockers. Do not contact a photographer as a
normal Skill prerequisite.

### Self-Shoot Plan

Use only the user's supplied equipment and conditions. Name one explicit key source;
keep the window and boards subordinate as fill/reflection controls. An avoided black
background never returns as a board, backdrop, or field. A generic component study is
not the user's actual item or identity and cannot become an Approved target without
acceptance. Unresolved direction, reference, or coverage is `prepared but blocked`;
exact orientation may remain open only when a named first diagnostic frame will resolve it.
If essential inventory or
output needs are missing, ask once for the missing camera bodies, lenses,
lights/modifiers, support, location/ambient conditions, or output needs; do not recommend purchases or invent gear. When inputs are known, the handoff is incomplete until all seven appear:

1. actual camera and lens;
2. starting aperture/shutter/ISO ranges;
3. camera distance;
4. camera height;
5. focus point or plane;
6. light/modifier placement; and
7. a short test-and-adjust sequence.

Label settings as starting guidance, not observed facts. Keep the honest visual
gap visible.

### Both

`both` has no enclosing `Photography Profile` or shared-parent wrapper. Emit
two independently sendable, self-contained top-level artifacts, exactly
`# AI Prompt Kit` and `# Photographer Brief`. Each repeats only a minimal
`Shared direction:` sentence and its own status, then contains its own complete
handoff; no recipient reconstructs a parent section. Never paste prompt prose
into the commissioning brief, copy booking logistics into the AI prompt, or
turn a lens hypothesis into an AI capture claim. If the AI Aim-point gate is
unmet, say the photographer handoff is text/gap but incomplete until cold readback
while the AI handoff is pending; report `AI status` and `Photographer status` separately. `Both status:
ready | prepared but blocked | incomplete`; `ready` requires both branches ready.
Never call the package ready while either is prepared but blocked or incomplete.

## Evidence and claim boundary

Keep `Observed`, `Confirmed`, `Documented`, and `Possible cause (inferred from appearance)` separate. Exact gear, exposure, film, lighting hardware, process,
spontaneity, staging, date, or authenticity require confirmation or reliable
documentation. A generated result cannot prove a real shoot or process. Preserve
each study's exact prompt, input paths in order/roles, output path, and receipt.
The exact final Portable prompt plus visual QA is required for AI verification;
an earlier or unpreserved study cannot prove the final prompt.

For historical work, date displays or label them contemporary/later and say
`period appearance, not authentic process` for an AI imitation. For a
cross-subject transfer, operationalize the chosen perspective class, working
distance, framing, focus, light position, and reflection control; the transferred
treatment and displayed reference become the new look and anchor, never the
source-subject look or reference.
