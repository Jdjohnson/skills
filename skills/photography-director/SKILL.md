---
name: photography-director
description: Develop a real-photography-led visual direction and prepare a separate AI, photographer, self-shoot, or combined execution handoff. Use when the picture must be clarified before production.
---

# Photography Director

Start with the user's pictures. Describe `Take` and `Ignore` from visible traits only. A component image may show pose, gesture, place, action, or finish; it does not prove identity, authenticity, spontaneity, collaboration, process, or the user's actual item. State what each reference does not prove.

Keep `Must-stays`, `Avoid`, reference roles, `Working reference`, `Destination`, and open decisions explicit. `Locked` contains only user-stated or explicitly accepted constraints. Assistant ideas remain `Options` or `Proposed`; never infer an Avoid from a missing trait.

## Find a direction

Resolve `<skill-root>` to this skill's installed folder.

```bash
node <skill-root>/scripts/query.mjs looks --query 'user words and useful photographic terms' --limit 5
```

Render returned references with credit. Obey `noSearch`; search once only when `needsSearch` is true. A component board is not a complete visual aim. Selection is not approval: only a user-accepted, same-genre visual aim can become the `Working reference` or `Approved target`.

For an explained rejection, rerun with `--recovery --exclude`, preserving rejected reference IDs, paths, and paired treatments. In the same response, show a genuinely new closer route. Never relabel or recycle a rejected image. If exclusions exhaust the set, return no assistant reference or treatment and state `Coverage gap: recovery exhausted`. Ask one diagnostic question only when a reject-all gives no visual reason.

## Refine

Only an accepted complete visual aim permits `refine`, `profile`, or `--anchor-ref`:

```bash
node <skill-root>/scripts/query.mjs refine --id <look-id> --anchor-ref <reference-id> --query 'visible delta and qualities to hold' --limit 4
```

Keep the exact anchor visible, change one visible bet, and say `Closer:` and `Still unresolved:`. Without new visual evidence, say `No visual progress yet` or `Coverage gap`; prose alone is not refinement. A direct component-board handoff remains text-led and must not inherit catalog locks, Avoids, or an anchor.

Treat supplied or generated images as `Observed` / `Current result`, not automatically as anchors. Separate `Observed`, `Confirmed`, `Documented`, and `Possible cause (inferred from appearance)`. Exact gear, exposure, process, date, staging, and authenticity require confirmation or documentation.

A generated image is a **Generated combination study**—“generated exploration; not a real-photo reference or final target”—until the user accepts it. Never generate to fill a quota or automatically after rejection. A confirmed hard-lock conflict is a `Failed generated result`: preserve the prior anchor and exact prompt, ordered inputs/roles, output, and receipt; stop without content retry.

## Prepare the handoff

Ask once for the destination if evidence does not establish it: `AI generation`, `a photographer`, `self-shooting`, or `both`. Ordinary acceptance never silently chooses AI. Repeat `--mode` and `--output` on later queries.

Before final output, read [the handoff contract](references/PROMPT-CONTRACT.md) and follow only the selected destination section. It is the single source of truth for output shape, blocker status, exact prompt boundaries, photographer cold readback, and self-shoot requirements.

Before calling any branch ready, compare every Must-have, Avoid, preference, option, and blocker with the user's exact accepted constraints. Remove invented qualifiers. A material unresolved production or delivery choice is `prepared but blocked`; missing branch proof is `incomplete`.

- AI requires an accepted visual aim, submission of the exact final portable prompt, receipt, visible QA, and acceptance.
- A photographer brief remains `incomplete` until a human cold read confirms it is independently actionable.
- A self-shoot plan uses only supplied equipment and conditions; never invent gear or purchases.
- `both` returns two self-contained artifacts and reports branch states separately; it is ready only when both are ready.

Save `photography-profile.md` only when the user asks and the destination is clear. For sourcing or catalog maintenance, read [reference sourcing](references/REFERENCE-SOURCING.md) and [catalog schema](references/CATALOG-SCHEMA.md).
