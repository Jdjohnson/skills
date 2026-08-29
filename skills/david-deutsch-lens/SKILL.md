---
name: david-deutsch-lens
description: Use audited David Deutsch argument packets to explain named concepts or test whether his worldview adds leverage to a problem. Use for source-grounded Deutsch questions and careful applications; not for impersonation, invented current views, or physics-as-metaphor proof.
---

# David Deutsch Lens

Reconstruct only what the audited corpus supports: the original problem, claim, argument, criticism, and sourced relationships. Do not imitate Deutsch's tone or answer as him. Do not flatten explanation into “ask why,” fallibilism into humility, optimism into positivity, universality into scale, or quantum theory into management advice.

## Route first

Resolve `<skill-root>` to this skill's installed folder. Frame the user's reasoning need, not surface verbs:

```json
{
  "problem": "conflict or uncertainty",
  "context": "material supplied facts",
  "decision": "answer or progress sought",
  "named_concepts": [],
  "domains": [],
  "reasoning_jobs": [],
  "stakes": "normal"
}
```

Use slugs from `references/corpus/domains.json`. Put only directly invoked Deutsch ideas in `named_concepts`; inferred relevance belongs in `domains` and `reasoning_jobs`. `stakes` is `normal` or `elevated`.

```bash
printf '%s\n' '{...}' | <skill-root>/scripts/route.sh route --input -
```

Honor the returned mode:

- `direct`: answer a named concept from its originating packet; add no unsolicited application plan.
- `lens`: use the selected packets because they discriminate among explanations or next moves.
- `source-only`: explain dated source material and its boundary; make no target-domain recommendation.
- `decline`: load no packets, briefly explain why the lens is unsupported or unnecessary, then use ordinary analysis if helpful.

Read only returned `cluster_path` and active `bridge_path` files—normally one or two, never more than three. `adjacent_packets` are orientation, not an instruction to load more. A high-level `four-strand-worldview` route is complete unless the user requests a specific technical detail.

## Validate applications

When a `lens` route requests application, validate a plan before drafting:

```json
{
  "mode": "lens",
  "selected_clusters": ["..."],
  "packet_roles": {"...": "primary"},
  "selected_bridges": ["..."],
  "lanes": ["faithful-paraphrase", "skill-synthesis", "skill-application"],
  "transfer": {
    "type": "cross-domain",
    "application_owner": "skill",
    "mechanism": "...",
    "target_evidence": ["..."],
    "disanalogies": ["..."],
    "defeaters": ["..."]
  }
}
```

```bash
printf '%s\n' '{...}' | <skill-root>/scripts/route.sh plan --input -
```

Do not make the application unless it returns `ok: true`. “Deutsch says so” is not a warrant.

## Ownership and transfer

Keep these distinct:

- `Deutsch-explicit`: checked primary source.
- `Faithful paraphrase`: no added premise, relationship, domain, or force.
- `Skill synthesis`: this analysis connects sourced material.
- `Skill application`: this analysis maps it to the user's problem.
- `Unverified`: requested attribution or relationship is absent from the audited corpus.

Relationships are claims; evidence for A and B does not prove Deutsch connected them. Attribute objections to Deutsch, an identified rival source, or this analysis.

Cross-domain use requires a sourced anchor, exact proposed correspondence, independent target evidence, material disanalogies and failure conditions, and explicit ownership of the recommendation. Without an active case-fitting bridge, analogy may generate a question, not a conclusion. Physics, computation, evolution, and constructor theory do not prove business, medical, legal, financial, political, relationship, or personal decisions.

For high-stakes or current claims, use current domain evidence and expertise. For current AI or “what he thinks now,” use dated language; do not update the corpus from memory.

## Answer

Lead with the answer, not routing machinery. Preserve the source's original problem and scope, the argument's force, a real criticism or boundary, the skill-owned application when permitted, evidence that could defeat it, and the next discriminating test or question. Name selected packets and source routes when attribution, controversy, transfer, or consequence risk makes provenance useful.

For quotation, disputed attribution/authorship, chronology, criticism, current-state claims, or cross-domain application, read [fidelity charter](references/fidelity-charter.md) and [source provenance policy](references/source-provenance-policy.md). Run `python3 <skill-root>/scripts/validate_corpus.py` after corpus changes and `python3 <skill-root>/scripts/evaluate.py` after routing or policy changes.
