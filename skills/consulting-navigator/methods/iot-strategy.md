# IoT Strategy
## Purpose
Design how connected devices, data flows, and platforms create prioritized operational or product value over a multi-year IoT roadmap. It links a physical signal to an operating decision and a financial outcome before selecting a platform.
## Use
- Designing a portfolio of connected-product or smart-operations use cases with clear value hypotheses
- Aligning device, connectivity, platform, and analytics choices into one multi-year roadmap
- Deciding where edge processing versus cloud aggregation creates operational or product advantage
## Avoid
- You only need a one-off sensor pilot with no enterprise scale-up path—use pilot-and-scale-methodology
- The bottleneck is ML model deployment rather than device and data architecture—use mlops-lifecycle
- You are still scanning what technologies exist rather than designing deployment—use technology-scouting first
## Inputs
**Must-have:** Priority operational or product problems that connectivity could improve; Current OT/IT landscape, device estate, and connectivity constraints; Data ownership, security, and latency requirements; Rough unit economics or value hypotheses per candidate use case; Vendor and platform options already under consideration.

**Nice-to-have:** Asset criticality, field-service records, radio surveys, lifecycle support plans, and customer consent requirements.

**When data is thin:** Start with discovery measurements on a representative asset class; do not extrapolate pilot connectivity or battery performance from a lab to the whole estate.
## Procedure
1. **Define value cases, not technologies.** Describe the user, physical event, decision, intervention, and measurable benefit for each candidate. Eliminate ideas that collect data without changing a decision or customer experience.
2. **Prioritize the portfolio.** Score use cases on economic upside, feasibility, data availability, safety exposure, and time to proof. Separate a local operational benefit from a reusable connected-product capability.
3. **Trace the end-to-end data path.** For priority cases, specify sensor, device identity, connectivity, gateway, edge processing, cloud ingestion, storage, analytics, application, and action owner. Locate processing according to latency, resilience, bandwidth, and privacy constraints.
4. **Set reference architecture and guardrails.** Choose interoperability standards, device management, security controls, data ownership, API boundaries, and vendor exit provisions. Design for onboarding and patching thousands of devices, not merely one pilot.
5. **Build the roadmap.** Sequence foundational connectivity and platform work before dependent use cases; identify pilots that validate uncertain value or adoption assumptions. Assign product, operations, security, and data-accountability roles.
6. **Measure value and scale decisions.** Establish baseline performance and adoption measures, then use pilot evidence to scale, redesign, or stop each use case.
## Output Contract
An IoT roadmap with ranked value cases, business cases, a reference architecture, edge-versus-cloud decisions, security and data guardrails, delivery waves, dependencies, owners, and scale criteria. It must make clear which investments are shared platform capabilities and which are use-case-specific.
## Evidence
Device counts, outage records, and measured signal coverage are observed. Savings from avoided downtime, adoption rates, and usable data quality are assumptions until the pilot validates them. Record data-retention, consent, and cyber obligations by jurisdiction. Treat vendor feature claims as unverified until tested against the required device, network, and operating environment.
## Checks
- Each priority use case has a named decision recipient and a quantified value mechanism.
- The architecture includes device identity, remote update, monitoring, and decommissioning.
- Edge choices are justified by latency or resilience, not fashion.
- Connectivity coverage and power constraints are tested in actual operating conditions.
- Platform selections preserve ownership and exportability of operational data.
## Failure Modes
- Buying a platform before defining a valuable signal-to-action loop.
- Treating a successful single-site pilot as evidence of fleet-scale supportability.
- Sending safety-critical alerts to the cloud when network loss makes that unsafe.
- Leaving device patch ownership between operations and information security.
