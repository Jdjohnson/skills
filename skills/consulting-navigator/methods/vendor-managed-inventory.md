# Vendor Managed Inventory
## Purpose
Design and implement a supplier-led replenishment model where the vendor plans and maintains agreed customer inventory levels. It transfers planning work under shared data, service, and ownership rules instead of merely changing reorder points.
## Use
- Transferring replenishment responsibility to suppliers for stable, high-volume items
- Reducing buyer order processing and improving fill rate through shared inventory visibility
- Designing commercial and operational rules for supplier-owned or supplier-planned stock
## Avoid
- Demand is highly volatile or poorly forecasted; stabilize with sales-and-operations-planning and demand-planning-and-forecasting first
- You need pure internal pull without supplier ownership—use just-in-time or kanban-system
- Category strategy and supplier selection are unresolved—use strategic-sourcing first
## Inputs
**Must-have:**
- SKU demand history, variability, and service targets
- Current inventory policy, ownership, and location of stock
- Supplier capability for visibility, planning, and replenishment
- Commercial terms for ownership, liability, and performance penalties
- IT interfaces for inventory and demand signal sharing

**Nice-to-have:** forecast cadence, shelf-life constraints, promotion calendars, disputes, and supplier capacity commitments.

**When data is thin:** begin with stable SKUs, conservative limits, and buyer review until data proves reliable.
## Procedure
1. **Select eligible items and partners.** Screen SKUs for predictable demand, volume, manageable obsolescence, and a capable supplier. Exclude volatile promotions and unresolved quality issues. Output: pilot eligibility list.
2. **Establish the inventory policy.** Define locations, review cadence, target days of supply, minimum and maximum levels, service target, lead time, and who owns inventory at each point. Output: replenishment policy table.
3. **Design the data exchange.** Specify item masters, on-hand balances, consumption, open orders, forecasts, exceptions, transmission frequency, and reconciliation process. Test whether the supplier sees the same inventory truth as the customer. Output: data-interface specification.
4. **Write decision and commercial rules.** Assign who may change limits, how stockouts and excess are escalated, when emergency orders are allowed, and how consignment, liability, returns, and incentives work. Output: operating agreement.
5. **Pilot, measure, and expand.** Run the model on selected SKUs, hold a joint exception review, compare results with the baseline, and correct master data or parameter defects before adding items. Output: scale decision and rollout plan.
## Output Contract
A VMI operating model with eligible SKUs, locations, policy rules, data fields and cadence, decision rights, exceptions, commercial terms, measures, pilot design, and expansion criteria. It makes the vendor accountable for replenishment while preserving customer approval boundaries. It is not a safety-stock calculation or internal kanban design.
## Evidence
Use transactions, physical counts, and confirmed lead times as observed. Identify forecast inputs and demand smoothing as assumptions. Measure availability at the receiving location, not vendor shipment. Reconcile ownership and book quantities each close. Compare supplier planning with actual consumption and record overrides and causes.
## Checks
- Every piloted SKU has a named location, owner, target range, and service target.
- Both parties can reproduce the same on-hand and consumption position from exchanged data.
- The agreement defines stockout, excess, obsolescence, and forecast-error accountability.
- Exception thresholds prevent routine manual expediting from becoming the real process.
- Pilot performance is compared with a pre-pilot baseline on fill rate, inventory, and buyer effort.
## Failure Modes
- Handing replenishment to a supplier while withholding current inventory and consumption data.
- Including erratic launch or promotion items before the basic rules are stable.
- Rewarding supplier volume shipped instead of availability at the customer location.
- Leaving ownership and obsolete-stock liability vague until the first dispute.
- Maintaining buyer-created orders in parallel, which destroys the planning transfer.
