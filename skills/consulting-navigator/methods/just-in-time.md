# Just-In-Time
## Purpose
Design and run a pull replenishment system that produces and delivers only what is needed, when needed, in the quantity needed—minimizing inventory while protecting flow. It synchronizes the whole replenishment cadence, including suppliers, rather than merely adding visual signals.
## Use
- You need to cut inventory and lead time by synchronizing production and replenishment to actual demand
- Material and WIP buffers are masking flow problems and inflating cost of goods
- A pull-based replenishment cadence is feasible with suppliers and internal cells
## Avoid
- Demand is highly erratic and you lack a forecast or leveling mechanism—use demand-planning-and-forecasting first
- You need a full waste-elimination operating system rather than inventory pull alone—use lean-manufacturing
- The constraint is capacity or process reliability, not excess stock—use theory-of-constraints or total-productive-maintenance
## Inputs
**Must-have:** Demand pattern by SKU or part family (volume, variability, mix); current inventory positions, lead times, and lot sizes by stage; supplier delivery reliability, minimum order quantities, and replenishment lead times; process cycle times, changeover times, and capacity by work center; service-level targets and stockout cost assumptions.

**Nice-to-have:** demand seasonality, quality hold history, transport cut-off times, and supplier flexibility agreements.

**When data is thin:** begin with a stable high-runner family, meter actual consumption, and make every lead-time estimate visible before reducing a buffer.
## Procedure
1. **Select the product family and pace.** Calculate daily demand and takt from available production time. Separate predictable demand from spikes that need a managed exception path.
2. **Expose the present replenishment loop.** Trace each part from supplier through storage, fabrication, and shipment. Record replenishment lead time, transfer batch, changeover constraint, and every inventory location.
3. **Level the release pattern.** Smooth mix and volume within the practical planning horizon so downstream processes see a repeatable pitch. Reduce lot size only after testing whether changeovers and quality can support it.
4. **Set replenishment cadence.** Define withdrawal frequency, delivery routes, supplier call-off timing, supermarket locations, and the maximum inventory permitted at each loop. Use a Kanban System where an explicit card or electronic authorization is needed.
5. **Pilot and stabilize.** Run the new cadence with daily shortage review. Correct late supply, unstable cycle time, and quality defects at their cause before making the lower inventory target permanent.
## Output Contract
Produce a pull-plan for a named product family: takt and pitch, leveled release pattern, replenishment loops, delivery frequency, lot rules, inventory caps, supplier call-offs, and an exception protocol. It must specify who sees consumption, who authorizes replenishment, and what condition stops production. Include an implementation sequence that protects customer service while inventory is reduced.
## Evidence
Use shipment history and measured cycle times for pace calculations; label forecast-driven demand as an assumption. Measure physical stock at the point of use rather than relying solely on ERP balances. Record supplier lead time as a distribution when delivery performance varies. A proposed buffer reduction requires a stated failure response, not confidence that demand will behave normally.
## Checks
- Takt uses net available time and the selected product-family demand, not plant-wide averages.
- Every loop has an owner, trigger, replenishment quantity, and maximum inventory.
- Changeover capability supports the planned lot size.
- Delivery frequency is feasible with dock, route, and supplier capacity.
## Failure Modes
- Cutting stock before resolving unstable machines, quality holds, or supplier misses.
- Calling a weekly forecast push schedule “pull” because it has smaller lots.
- Applying one cadence to parts with radically different demand or replenishment times.
- Allowing expedites to bypass the loop until the designed signals become irrelevant.
