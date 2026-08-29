# Last Mile Delivery Optimization
## Purpose
Design and optimize the final delivery leg across modes, density, SLAs, and cost-to-serve. It balances route economics with the customer promise at the doorstep, pickup point, or locker rather than redesigning the full distribution network.
## Use
- Redesigning the final delivery leg for cost, speed, and customer promise reliability
- Choosing last-mile modes (fleet, 3PL, pickup, locker, crowd) by density and SLA
- Fixing high failed-attempt rates, thin density, or unprofitable delivery zones
## Avoid
- The problem is national node placement, not the final drop—use logistics-network-design
- You need partner selection governance before redesigning routes—use 3pl-4pl-selection-framework
- Channel strategy (store vs web fulfillment) is unresolved—use omnichannel-strategy first
## Inputs
**Must-have:** Order density, drop profiles, and time-window mix by geography; current last-mile cost, success rate, and SLA performance; available modes, hubs, and pickup alternatives; customer promise standards and willingness-to-pay for speed.

**Nice-to-have:** address-quality rates, parking and access constraints, returns volumes, courier capacity calendars, and customer pickup preference data.

**When data is thin:** measure one representative route day by zone and distinguish actual stops from planned stops before changing a delivery promise.
## Procedure
1. **Segment the service territory.** Group orders by density, distance, time window, package profile, access conditions, and return propensity. Separate zones whose economics differ even when they share a postal code.
2. **Establish drop economics.** Calculate cost per successful delivery, stops per route-hour, kilometers per stop, first-attempt success, and penalty or refund cost. Trace failed attempts and waiting time to their causes.
3. **Design mode and promise rules.** Compare fleet, parcel carrier, crowd, locker, pickup, and consolidation options against each segment’s service need. Set eligibility rules for premium speed, scheduled windows, and pickup incentives.
4. **Optimize routes and capacity.** Build route territories, delivery sequences, cut-off times, load factors, and overflow contracts. Treat returns and reattempts as planned workload, not an afterthought.
5. **Pilot the highest-value change.** Test one zone with a defined customer message, operational runbook, and measurement period. Scale only if cost, SLA, and customer response improve together.
## Output Contract
Deliver a final-delivery operating plan: zone segments, baseline economics, mode assignment rules, route and capacity design, customer-promise policy, exception handling, and pilot roadmap. Include the choices that change an order’s fulfillment path and the owner who may override them. The plan must show unit economics for successful and failed drops.
## Evidence
Use scan events and invoice data for successful-drop and cost measures; mark driver-reported delay reasons as provisional until sampled. Attribute returns separately from forward delivery. State assumptions about pickup adoption, carrier surge capacity, and willingness to accept slower service. A route optimizer’s estimate is a forecast, not proof of curbside feasibility.
## Checks
- Geography is segmented by stop density and constraints, not only administrative boundaries.
- Costs include reattempts, customer contacts, refunds, and returns where material.
- Every promised window has enough route and handoff capacity.
- The pilot has a control zone or before-period comparison.
## Failure Modes
- Lowering cost per package by merging routes until promised windows become impossible.
- Treating a delivered scan as a successful handoff when the parcel is stolen or refused.
- Offering lockers in areas where customer uptake or walking access is poor.
- Optimizing outbound routes while return pickups consume the saved capacity.
