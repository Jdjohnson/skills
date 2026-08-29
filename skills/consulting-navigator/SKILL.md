---
name: consulting-navigator
description: Frame an ambiguous business decision, route it to a small set of local analysis methods, and synthesize one evidence-aware recommendation. Use when choosing the analytical approach matters; not for simple lookups, editing, or code tasks.
---

# Consulting Navigator

Start with the decision. Use the smallest sufficient method stack—normally two or three—and return one integrated answer, not a framework catalog. Separate facts, inferences, assumptions, and unknowns.

If a missing fact could change the decision itself, the evidence base, risk tolerance, or an irreversible action, ask one concise question and stop. Otherwise proceed with labeled assumptions.

## Route and validate

Resolve `<skill-root>` to this skill's installed folder. Frame:

```json
{"problem":"...","decision":"...","context":"...","constraints":[],"desired_output":"...","practice_areas":[],"reasoning_jobs":[]}
```

```bash
python3 <skill-root>/scripts/navigate.py route --input - <<'JSON'
{ ... }
JSON
```

Choose one to five candidates, normally two or three. Give each a distinct role and sequence. Four or five require an explicitly broad problem and a `breadth_justification`.

```json
{"case_summary":"...","selected_methods":[{"id":"...","role":"...","sequence":1}],"assumptions":[],"missing_inputs":[],"expected_output":"..."}
```

```bash
python3 <skill-root>/scripts/navigate.py plan --input - <<'JSON'
{ ... }
JSON
```

Fix errors until `ok` is true. If deliberately reversing a registered order, add one justified `sequence_overrides` item.

Read only returned `method_path` files and never more than five. Apply each selected method's procedure and output contract, then synthesize around the decision. Do not scan `methods/`, open `registry/index.json`, or reroute merely to explore alternatives.

## Output

Lead with the conclusion or plan. Give integrated supporting logic, labeled assumptions and missing evidence, and the next action. End with a short `Approach used` note naming selected methods and other material data sources or tools.

Taxonomy slugs are defined by the router. Common practice areas include strategy, growth, pricing, product, operations, organization, finance, technology, and risk; reasoning jobs include framing, diagnosis, evidence gathering, forecasting, option generation, prioritization, solution design, implementation, risk governance, and learning.
