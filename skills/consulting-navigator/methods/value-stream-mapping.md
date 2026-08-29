# Value Stream Mapping
## Purpose
Decompose end-to-end material and information flow into a current-state map and design a future-state value stream that cuts lead time and waste. It exposes how demand, queues, batches, and control signals create delay across one product or service family.
## Use
- Visualizing material and information flow from customer request to delivery for one product family
- Exposing lead time, inventory, and handoff waste before lean redesign
- Aligning operations on a future-state value stream and kaizen priorities
## Avoid
- You only need a one-page process boundary before detailed work—use sipoc-analysis
- The focus is customer emotions and brand moments, not material/info flow—use customer-journey-mapping
- You need multi-layer service frontstage/backstage roles—use service-blueprinting
## Inputs
**Must-have:**
- Selected product family or service family and customer demand rate
- Walk-the-flow observations of process steps, cycle times, and uptime
- Inventory levels, batch sizes, and queue times between steps
- Information flow that triggers and controls production or fulfillment
- Current performance metrics (lead time, on-time delivery, scrap, changeover)

**Nice-to-have:** daily demand mix, changeovers, supplier cadence, rework rates, and layouts.

**When data is thin:** map observed paths, mark estimates, and conduct another walk before capital or layout changes.
## Procedure
1. **Choose the family and demand basis.** Select products with similar routing; define daily demand, available work time, and customer cadence. Calculate takt after excluding breaks. Output: scope and demand sheet.
2. **Walk upstream from the customer.** Record each process, operator count, cycle time, uptime, changeover, scrap, inventory, and queue. Follow the physical item, not a conference-room description. Output: observation log.
3. **Map material and information.** Draw suppliers, processes, inventories, shipments, scheduling signals, and the information loop from customer order to release. Add a timeline that separates touch time from waiting time. Output: current-state map.
4. **Diagnose flow constraints.** Compare cycle times to takt, find pacemaker candidates, quantify queue days, and identify push, batching, rework, or unclear signal causes. Confirm observations with operators before naming a kaizen burst. Output: waste and constraint list.
5. **Design and sequence the future state.** Specify where continuous flow, supermarkets, pull signals, leveling, or smaller batches belong. Draw the future-state map, then break the gap into owner-led loops with measurable lead-time targets. Output: future-state map and kaizen plan.
## Output Contract
Two maps for one family: observed current and future states, with material and information paths, inventory, timing, demand basis, and a timeline. The package includes lead time, touch time, percent value-added, constraint evidence, and owner-led kaizen bursts. It supports a flow-redesign decision, not documentation of steps.
## Evidence
Treat stopwatch readings, counts, and timestamps as observed; mark inferred waits and unavailable branches separately. Use one observation window so inventory and demand rates compare. Record physical, electronic, and scheduler queues. Demand mix, uptime, and batch-size assumptions must be visible. Do not turn a target into a current-state measurement.
## Checks
- The map follows a single family from customer demand through delivery.
- Timeline totals reconcile to process observations and inventory waiting assumptions.
- Information signals show who releases work and at what frequency.
- Future-state elements solve a mapped cause, not a fashionable lean practice.
- Kaizen bursts have a measurable flow outcome and a named owner.
## Failure Modes
- Drawing a process map without timing, inventory, or control information.
- Timing operators while missing the days a job sits in an electronic queue.
- Mixing unrelated product routings and producing meaningless averages.
- Proposing pull while leaving the scheduling release mechanism unchanged.
- Designing future flow without operator review or demand realism.
