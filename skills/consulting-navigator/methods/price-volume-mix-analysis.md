# Price-Volume-Mix Analysis
## Purpose
Decompose a period-over-period change in revenue, gross margin, or contribution into pure price, pure volume, and mix effects. The output is a quantified variance bridge that separates pricing actions from volume and portfolio shift before pricing, sales, or portfolio decisions.
## Use
- Revenue and margin moved in opposite directions and owners disagree on the cause.
- Volume targets were hit yet profit missed, or list prices rose while realized price looks flat.
- Finance and commercial teams need one shared bridge for a board pack or review.
- Mix may have shifted toward lower-margin products without an explicit decision.
## Avoid
- You need customer-level profit and cost-to-serve rather than period variance—use customer-profitability-analysis.
- The problem is activity cost drivers rather than price/volume/mix—use activity-based-costing.
- You lack comparable prior-period quantities and prices by product or segment—gather that data first.
- The question is lifetime value under retention scenarios rather than a two-period bridge—use customer-lifetime-value-analysis.
## Inputs
**Must-have:** Prior- and current-period revenue (or margin), unit prices, and unit volumes by product, SKU, or segment; mix weights for both periods; a fixed price definition (list vs realized) and consistent volume units.

**Nice-to-have:** Currency and FX flags; new and discontinued product flags; discount and surcharge detail; contribution margin by SKU.

**When data is missing:** Hold out incomplete SKUs, state coverage percent, and never force the residual to zero by inventing volumes.
## Procedure
1. **Lock the bridge definition** — Choose the metric (revenue, gross margin, or contribution), the two periods, the grain, and the price definition. Output: scope note.
2. **Build a two-period table** — Record prior and current volume and price per line, compute period totals, and flag new and discontinued items. Output: comparison table.
3. **Calculate the price effect** — For continuing items, apply average selling price change times a fixed volume base (typically prior-period volume). Output: price variance by line and total.
4. **Calculate volume and mix effects** — Split the remaining change into pure volume (volume change at a reference price, mix held out) and mix (mix-weight shift times price differentials). Output: volume and mix lines.
5. **Reconcile and interpret** — Confirm price + volume + mix (+ new/exit residual) equals the total change; name which drivers dominate and who owns each. Output: waterfall bridge and narrative.
6. **Map decision hooks** — Route the dominant effect to its follow-up analysis (pricing leakage, elasticity, cost, or portfolio). Output: prioritized follow-ups.
## Output Contract
A quantified PVM bridge with: (1) scope and price/volume definitions, (2) line-level and total price, volume, and mix effects, (3) treatment of new/discontinued products, (4) reconciliation to the total period change, and (5) an interpretation that attributes ownership and supports a pricing, volume, or mix decision. The artifact is a diagnosis bridge, not a customer ranking or discount waterfall.
## Evidence
- **Observed:** system prices, invoiced volumes, and booked revenue by period.
- **Inferred:** effect attributions from the chosen formulas.
- **Assumptions:** price definition, volume base for price effect, and mix formula variant—document them so the bridge is reproducible.
- **Unknowns:** if units or realized price are incomplete, leave a labeled residual rather than false precision.
## Checks
- Bridge reconciles to the total change within an agreed tolerance.
- Price definition is consistent across periods and stated explicitly.
- New and discontinued products are handled transparently, not buried in mix.
- Narrative matches the math—“volume up, mix down” only if the numbers show it.
- Effects sit at an actionable grain, not one opaque residual.
## Failure Modes
- Mixing list and realized price mid-bridge.
- Labeling discounting or new products as “mix.”
- Using inconsistent units (cases vs eaches) across periods.
- Presenting a bridge without ownership or decision implications.
- Over-precision on sparse SKUs that should be rolled up.
