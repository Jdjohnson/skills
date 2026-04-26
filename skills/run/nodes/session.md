---
description: |
  Guided planning mode for larger or fuzzier projects. Builds a live
  session.md while shaping the work, then locks into blueprint.json,
  progress.md, and a launch-ready package.
---

## Session Workshop

Load shared controls:
- [[../_shared/nodes/interaction-gates.md]]
- [[../_shared/nodes/output-discipline.md]]
- [[safety.md]]

Reference: [[blueprint-schema.md]]

---

## Purpose

Use `session` when the project needs more structure than a direct prompt.

This mode is for projects that are:
- higher leverage
- fuzzier in scope
- riskier if shaped poorly
- more dependent on the right tool and execution posture

`/run` routes here by default. `/run session` is the explicit form.

---

## Inputs

- User's project description
- Optional: likely repo directory or subdirectory this work should live in
- Optional: existing files, briefs, constraints, or acceptance criteria that materially shape the run

---

## Operating Rules

1. Ask questions when ambiguity materially affects strategy, scope, risk, or launch posture.
2. Do not ask on every phrasing choice. Prefer a reasonable recommendation and invite correction.
3. Create the run directory early once a stable draft name exists.
4. Create `session.md` immediately after the directory is chosen, then keep it current throughout the workshop.
5. Maintain one current-truth `session.md`. Rewrite stale wording instead of stacking correction history.
6. End with a human-readable launch package. Do not auto-launch the run.

## Voice

When the run package includes prose a human will read directly:
- keep `Executive Summary`, `Why This Run`, and `Intended Outcome` warm, direct, and plainspoken
- lead with the answer, not the buildup
- avoid report voice, filler, and fake certainty
- keep checklist rows, IDs, tool routing, dependencies, and launch commands technical

---

## Session Flow - Five Stages

Run each stage in order. Pause for input anywhere uncertainty materially changes the plan.

### Stage 1: Frame

**Goal**: Understand the run at the level of outcome, stakes, and constraints.

1. Ask for the project in broad terms: goal, stakes, files, constraints, and what "done" looks like.
2. Reflect back a draft:
   - project name
   - executive summary
   - why this run exists
   - intended outcome
   - scope
   - constraints
3. Once the draft project name is stable enough, propose the project directory:
   - existing repo subdirectory when clearly related
   - otherwise `./runs/<project-slug>/`
4. After the user approves the directory, create `session.md` there immediately and write the current truth.

### Stage 2: Pressure-Test

**Goal**: Find weak spots before decomposition.

1. Pressure-test:
   - what success actually means
   - what is explicitly out of scope
   - what assumptions are risky
   - what decisions need to be made now versus later
2. Ask focused follow-ups only where the answer changes strategy, step structure, or launch mode recommendation.
3. Update `session.md` so it includes:
   - exclusions
   - key decisions
   - open questions

### Stage 3: Decompose

**Goal**: Turn the project into a bounded executable run.

1. Propose a run checklist with bounded steps.
2. Each step should expose:
   - `id`
   - title
   - what the step does
   - primary output
   - done condition
   - dependencies
   - noteworthy risk or ambiguity when relevant
3. Keep steps atomic and concrete.
4. Update the `Run Checklist` and `Dependencies` sections in `session.md` as the checklist evolves.

### Stage 4: Route

**Goal**: Assign the right execution tool and posture to each step.

1. Recommend a tool for each step, including `skill:*` routing when relevant.
2. Show skill steps with their runner in plain English, for example:
   - `skill:research-brief (via claude-code)`
3. Capture only meaningful overrides for:
   - default tool
   - skill runner
   - models
   - timeout
   - capabilities
4. Update `Tool Map` in `session.md`.
5. Recommend the likely launch mode fit:
   - `standard`
   - `adaptive`
   - `expansion`

### Stage 5: Lock

**Goal**: Turn the session into launch artifacts and a clear handoff.

1. Present the final package as a human-readable review, not raw JSON.
2. On approval:
   - write `blueprint.json`
   - initialize `progress.md`
   - update `session.md` to its locked current-truth state
3. Present the launch layer:
   - validation command
   - `standard` launch command
   - `adaptive` launch command
   - `expansion` launch command
4. Explain the ladder in plain English:
   - `standard`: run the approved plan and stop on failure or blocker
   - `adaptive`: fixed scope, bounded blocker removal, restart on disruption or timeout
   - `expansion`: adaptive behavior plus bounded step creation during execution
5. Keep `--supervised` available only as legacy compatibility language.

---

## `session.md` Contract

`session.md` is the live source of truth during planning.

Create it early and keep it clean. Update stale language to the latest truth rather than appending correction logs.

Write the session as if a new user may read it later without any outside context. Avoid references to a private workflow, home workspace, or prior conventions the reader would not know.

### Required Sections

- `# Session - <project name>`
- `## Executive Summary`
- `## Why This Run`
- `## Intended Outcome`
- `## Scope`
- `## Constraints`
- `## Exclusions`
- `## Key Decisions`
- `## Open Questions`
- `## Run Checklist`
- `## Tool Map`
- `## Dependencies`
- `## Launch Modes`
- `## Launch`

### Run Checklist Row Contract

Each planned step should show:
- step id
- title
- what it will do
- tool
- primary output
- done condition
- dependencies
- noteworthy risk or ambiguity when relevant

---

## Final Launch Package Contract

Before the run starts, present three layers:

### 1. Executive Layer

- what we are building
- why the run exists
- intended outcome
- major exclusions
- biggest risks or assumptions

Write this layer for a general reader who is encountering the run for the first time. It should make sense without any outside context.

### 2. Execution Layer

- full step checklist
- tool for each step
- skill usage called out explicitly
- capability needs or major overrides when relevant

### 3. Launch Layer

```bash
# Validate the package before launch
run-workflow --validate <path>/blueprint.json

# Standard: run the approved plan and stop on failure or blocker
run-workflow --launch-mode standard <path>/blueprint.json

# Adaptive: fixed scope, bounded blocker removal, restart on disruption or timeout
run-workflow --launch-mode adaptive <path>/blueprint.json

# Expansion: adaptive behavior plus bounded step creation during execution
run-workflow --launch-mode expansion <path>/blueprint.json
```

Close with a plain-language explanation of which launch mode you recommend and why.

Use the `standard` / `adaptive` / `expansion` ladder as the primary handoff. Mention `--supervised` only as legacy compatibility.

---

## Output Contract

- `session.md` created early and updated throughout planning
- `blueprint.json` written at lock time
- `progress.md` initialized at lock time
- final launch package presented with `--validate` plus `standard`, `adaptive`, and `expansion` commands
