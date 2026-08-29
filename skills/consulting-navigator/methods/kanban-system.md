# Kanban System
## Purpose
Install a visual pull-signal system that limits WIP and authorizes production or replenishment only when the downstream process consumes. Its design object is the permission signal, its count, and the operating rules that make excess work visible.
## Use
- You need a visual pull mechanism that authorizes work or material movement only when consumption occurs
- WIP is uncontrolled and push scheduling creates overproduction and queues
- Material or task flow between stations can be governed by cards, bins, or electronic signals
## Avoid
- You need plant-wide waste elimination and value-stream redesign—use lean-manufacturing
- Demand and capacity must be leveled before signals will stabilize—use just-in-time with demand leveling first
- The work is pure project knowledge work with no repeatable flow units—consider scrum-framework or critical-path-method instead
## Inputs
**Must-have:** Defined flow path, work units, and consumption points; current WIP levels, replenishment lead times, and container or batch sizes; customer or downstream demand rate and variation; rules for signal creation, withdrawal, and emergency override; physical or digital board/card design constraints.

**Nice-to-have:** a stable location code, defect quarantine rules, and evidence from previous stockouts or starvation events.

**When data is thin:** start with one loop and a conservative card count, then observe actual replenishment time before tightening the limit.
## Procedure
1. **Define the loop boundary.** Name the supplying process, consuming process, unit container, and point at which consumption becomes real. Exclude rework and quality-hold material from normal signals.
2. **Measure demand and replenishment time.** Collect consumption by interval and end-to-end refill time, including waiting, transport, setup, and inspection. Choose the service level and a limited safety factor.
3. **Calculate and allocate signals.** Set the number of cards or electronic tokens from demand during replenishment, container size, and the agreed buffer. Give every token an item, quantity, loop, and home location.
4. **Write operating rules.** Specify when a card is removed, where it travels, who may produce, how completed containers return, and how an emergency bypass is recorded and cleared.
5. **Run the board and tune it.** Audit missing cards, empty slots, blocked items, and unauthorized WIP each shift. Change the signal count only after a demand or lead-time change is demonstrated.
## Output Contract
Provide a working pull-loop specification: flow diagram, token calculation, container standards, card or board fields, physical locations, normal operating rules, override controls, and audit metrics. It must make the WIP ceiling observable and assign responsibility for restoring a missing or misused signal.
## Evidence
Use time studies and consumption records for the calculation; identify any estimate used for lead time or variation. Treat a card count as a control parameter, not a target for production. Record emergency overrides separately so demand volatility and process failure do not hide inside the normal loop.
## Checks
- Each token has exactly one authorization purpose and cannot silently multiply.
- Container quantity matches handling, quality, and downstream consumption constraints.
- The calculated limit is visible at the point of work.
- Starvation, blocked work, and lost-card conditions have named recovery rules.
## Failure Modes
- Printing cards without withdrawing authorization when the downstream bin is still full.
- Mixing defective material into available containers and overstating usable WIP.
- Increasing cards whenever a shortage occurs instead of examining the delayed refill.
- Creating a digital board that operators cannot update at the consumption point.
