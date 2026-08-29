---
name: genealogy-site-publisher
description: Update a public family-history site from canonical genealogy research while protecting living people, preserving conflicts, grounding stories, and verifying publication. Use when a configured genealogy project needs an evidence-backed site refresh.
---

# Genealogy Site Publisher

Publish only what the canonical research supports.

## Project contract

Identify the canonical research store and site repository from the workspace's instructions or configuration. Before editing, read their authority files, data schema, extraction rules, story guidance, publish state, and documented validation, publication, and verification commands. Stop if those contracts or the target tree cannot be resolved safely.

## Invariants

- Research is canonical; site data never writes conclusions back to it.
- Treat anyone whose living status is uncertain as living.
- Publish only the schema's allowlisted structural fields for living people. Never expose their dates, places, facts, sources, relationships beyond the allowlist, stories, or private metadata.
- Preserve open identity or relationship conflicts. Do not turn candidates or held conclusions into graph edges.
- Preserve source precision and confidence. Never invent facts, quotations, motives, emotions, or narrative detail.
- Stop before publication when validation, privacy audit, story grounding, or review fails.

## Workflow

1. Compare the last published research revision with the current research state. If relevant evidence is unchanged, report that and stop.
2. Update site records only from supported evidence. Carry source references, confidence, date precision, and promoted relationships. Apply controlled vocabularies conservatively.
3. Run the repository's validator and privacy checks. Present the exact content diff and summarize additions, updates, removals, living records, and held conflicts. Obtain approval for that diff before publishing.
4. Refresh stories only for deceased people who meet the project's evidence threshold. Map every specific claim to a cited fact or label it as general historical context. Leave ungrounded stories pending.
5. Revalidate. Publishing, deletion, database writes, commits, pushes, and deployment require the authority defined by the active task and project. Never print credentials; use deletion flags only when the exact removals were approved.
6. Verify the published data and public site independently: audit living rows for forbidden fields, exercise the project's regression suite, and inspect representative navigation, person, story, indexing, accessibility, and responsive states.

## Report

Keep `prepared`, `approved`, `published`, `deployed`, and `verified public` separate. Report revisions, counts, privacy failures, stale stories, commands run, verified URLs, and any blocker without softening a failed gate.
