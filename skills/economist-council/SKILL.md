---
name: economist-council
version: 1.1.0
description: |
  Economist council for AI, labor, productivity, growth, inequality, and
  regional adaptation questions. Use when the user wants sourced convergence,
  divergence, and pushback from a standing panel before a talk, decision,
  strategy move, article, or research memo.
argument-hint: "[AI/economy topic, framing, or rough question]"
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Economist Council

Run an AI-and-economy question through a standing panel of economists, then synthesize convergence, divergence, and pushback.

## Mode Routing

| Mode | Trigger | When | Node |
|------|---------|------|------|
| `intake` | default or new topic | Lock the actual question before dispatch | [[nodes/intake-lock.md]] |
| `panel` | panel choice or scope question | Choose default or bench economists | [[nodes/panel-selection.md]] |
| `dispatch` | confirmed topic and panel | Synthesize economist views from cache and targeted lookup | [[nodes/dispatch-synthesis.md]] |
| `deep-dive` | "go deeper", debate, latest, quote-backed | Press one economist, disagreement, or source gap | [[nodes/deep-dive.md]] |

Default mode: `intake`.

## Core Rules

1. Load [[nodes/intake-lock.md]] and [[nodes/source-discipline.md]] first.
2. Use this for AI, labor, productivity, growth, inequality, firm adaptation, regional resilience, technological change, policy, measurement, or institutions.
3. Do not use this as a generic brainstorming shortcut. If the topic has no economic shape yet, clarify before dispatch.
4. Use [[nodes/panel-selection.md]] for the Big Five default panel and optional bench.
5. Use the portable cache under `references/` before live lookup unless freshness, quotations, or recent developments matter.
6. Do not invent quotes, publications, or positions. If a statement is inferred from a framework, label it as extrapolated.
7. Save output only when the user asks or provides a destination.

## Output Contract

- Intake: locked question, intended output, audience, panel, and depth.
- Dispatch: convergence, divergence, strongest pushback, practical implications, uncertainty, and one useful question back.
- Deep dive: focused disagreement, one economist deeper, two-voice debate, or source-backed update.

## Node Map

- [[nodes/intake-lock.md]]
- [[nodes/panel-selection.md]]
- [[nodes/source-discipline.md]]
- [[nodes/dispatch-synthesis.md]]
- [[nodes/deep-dive.md]]
- [[nodes/output-format.md]]
