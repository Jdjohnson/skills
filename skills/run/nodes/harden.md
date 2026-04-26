---
description: |
  Verify/revise planning mode for strengthening an existing thesis, claim,
  draft, strategy, or plan into a more defensible artifact.
---

## Hardening Workshop

Load shared controls:
- [[../_shared/nodes/interaction-gates.md]]
- [[../_shared/nodes/output-discipline.md]]
- [[safety.md]]

Reference: [[blueprint-schema.md]]

---

## Purpose

Use `harden` when the user already has a thesis, argument, claim, draft, or plan and wants a bounded run that:

- finds the weakest claims
- verifies the evidence that matters most
- revises the artifact against that evidence
- returns a stronger final version

If the seed is still too foggy to state as a one-sentence thesis with a clear conclusion, stop and route to `steelman` before planning the run.

---

## Inputs

- seed thesis, argument, claim, draft, or plan
- intended use
- what counts as strong evidence
- what would materially weaken or falsify the conclusion
- source allowance, constraints, and stakes
- optional: likely project directory or related repo path

---

## Operating Rules

1. Ask only questions that change the proof bar, step structure, or stop rule.
2. Use the same planning artifact surface as `session`: `session.md`, `blueprint.json`, and `progress.md`.
3. Keep the loop verification-centered. Avoid critique/rewrite cycles that do not change the evidence base.
4. Default to one or two verify/revise passes. Add a third only when stakes are high and meaningful new evidence remains available.
5. Keep outputs lean by default:
   - `hardened/final.md`
   - `hardened/one-paragraph-summary.md`
6. End with a normal launch package. Do not auto-launch the run.

---

## Hardening Flow

### Stage 1: Frame The Thesis

Reflect back:
- project name
- executive summary
- intended outcome
- thesis in one sentence
- proof bar
- likely stop rule

Once the project name is stable enough, propose the run directory. Prefer `./runs/<project-slug>/` unless the user supplied a better location.

### Stage 2: Set The Proof Bar

Pressure-test:
- whether the thesis is specific enough to verify
- which claims are central and fragile
- what evidence is allowed
- what would change the conclusion if false

Update `session.md` with the proof bar, exclusions, key decisions, open questions, and stop rule.

### Stage 3: Decompose The Loop

Propose the lightest viable checklist:
- capture the current artifact and identify top red claims
- verify/revise pass 1
- verify/revise pass 2 only if planned or still needed
- final synthesis and one-paragraph summary

Each step should expose `id`, title, action, tool, primary output, done condition, dependencies, red-claim focus, evidence allowance, and skip/stop condition.

### Stage 4: Lock

On approval:
- write `blueprint.json`
- initialize `progress.md` as runtime scaffolding only
- update `session.md` to the locked current truth
- present the command handoff from [[runner-handoff.md]]

---

## Output Contract

- `session.md` created early and updated throughout planning
- `blueprint.json` written at lock time
- `progress.md` initialized at lock time
- final launch package includes validate, status, follow, and one recommended launch command
