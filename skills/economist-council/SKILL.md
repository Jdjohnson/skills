---
name: economist-council
description: |
  Economist council for AI, labor, productivity, growth, inequality, and
  regional adaptation questions. Use when the user wants sourced convergence,
  divergence, and pushback from a standing panel before a talk, decision,
  strategy move, article, or research memo.
---

# Economist Council

Run an AI and economy question through a standing panel of economists, then synthesize where they converge, diverge, and push back.

## Fit

Use this for questions about:

- AI and labor
- productivity and growth
- inequality and distribution
- firm adaptation
- regional resilience
- technological change
- policy, measurement, or institutions

Do not use it as a generic brainstorming shortcut. If the topic has no economic shape yet, clarify the topic first.

## Default Panel

Default to the Big Five unless the user asks for a narrower or broader panel:

- David Autor
- Andrew McAfee
- Erik Brynjolfsson
- Daron Acemoglu
- Philippe Aghion

Optional bench:

- Carl Benedikt Frey
- Anton Korinek
- Pascual Restrepo
- Diane Coyle
- Michael Webb
- Jason Furman
- Anna Salomons
- Joel Mokyr

## Source Discipline

Use `reference/*.md` as the standing cache. If a cached position is missing, either stay silent or mark the statement as an inference from the economist's known framework.

For "latest", stage, publication, or quote-sensitive work, do targeted live lookup and cite current sources.

Do not invent quotes, publications, or positions. Never promote a `TODO:` note from a reference file into output as if it were sourced.

## Flow

### 1. Lock The Question

Restate:

- the question
- intended output
- audience
- default or requested panel
- depth

Do not dispatch the panel until the user confirms or corrects the framing.

### 2. Dispatch The Panel

For each approved economist, extract:

- standing position on the locked topic
- likely agreement
- likely objection
- what evidence they would want
- what question they would ask back

### 3. Synthesize

Do not paste mini-essays back-to-back. Return:

- convergence
- divergence
- strongest pushback
- practical implications
- what remains uncertain
- one question back to the user

### 4. Deepen

On request, deepen one economist, stage a two-voice debate, or upgrade to a quote-backed memo.
