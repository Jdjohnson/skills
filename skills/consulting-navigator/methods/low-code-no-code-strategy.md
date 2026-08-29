# Low-Code/No-Code Strategy
## Purpose
Design where and how low-code/no-code platforms accelerate delivery under governance so business makers and IT share a safe, scalable model.
## Use
- Accelerating delivery of forms, workflows, and departmental apps without growing engineering headcount linearly
- Defining guardrails so citizen development scales without creating unmanageable risk
- Choosing platform scope, operating model, and a multi-year LCNC adoption roadmap
## Avoid
- The work is pure robotic desktop automation of legacy UIs—use rpa-implementation-framework
- You need a full digital operating model beyond app delivery—use digital-transformation-framework
- The decision is build versus buy for a major system of record—use buy-vs-build-analysis
## Inputs
**Must-have:**
- Demand patterns for apps, workflows, and automation candidates
- Current development capacity, backlog, and shadow-IT footprint
- Security, data, and integration constraints
- Platform shortlist or incumbent LCNC tools
- Skills and support model for IT and business makers

**Nice-to-have:** software inventory, architecture standards, identity-management requirements, licensing economics, maker community data, and examples of failed local apps.

**When data is thin:** inventory a representative sample of requests and shadow tools. Set provisional boundaries tightly until architecture, security, and support capacity are understood.
## Procedure
1. **Inventory demand and existing workarounds.** Group requests by user problem, data sensitivity, integration needs, transaction criticality, and expected change rate. Output: use-case portfolio.
2. **Set the eligibility boundary.** Define what is allowed for citizen makers, what needs central review, what requires professional engineering, and what is prohibited. Output: decision matrix.
3. **Evaluate platforms against the boundary.** Test identity, data residency, auditability, API connectivity, lifecycle controls, accessibility, and total licensing cost using representative use cases. Output: platform fit assessment.
4. **Design the operating model.** Specify a center of excellence, maker enablement, reusable components, environment strategy, release controls, support tiers, and exception handling. Output: governance blueprint.
5. **Sequence adoption waves.** Select pilots that prove value and controls, measure time-to-delivery and incidents, then expand by domain with sunset or migration rules for fragile apps. Output: roadmap and scorecard.
## Output Contract
Produce an LCNC roadmap that contains the use-case segmentation, platform decision, build-boundary matrix, governance roles, lifecycle controls, reusable services, training path, funding model, and phased adoption measures. It must let a business leader decide whether a request can proceed and tell IT how that app will be supported, audited, and retired.
## Evidence
Base risk tiers on data classification, decision criticality, external exposure, and integration privileges—not on who requests the app. Treat vendor roadmap claims and maker productivity estimates as assumptions until tested in the enterprise environment. Retain an inventory with owner, data stores, connectors, deployment environment, and support tier for every production app. A successful demo does not prove maintainability.
## Checks
- The same use case receives the same disposition regardless of business unit.
- Prohibited patterns include system-of-record replacement, unmanaged credentials, and unreviewed sensitive data flows.
- Production apps have named product owners and a support route.
- Platform selection tests governance features as well as screen-building speed.
- Adoption measures include defect, security, and orphan-app indicators alongside throughput.
## Failure Modes
- Encouraging citizen development without an inventory, creating invisible production dependencies.
- Applying enterprise architecture review to a simple form until speed benefits disappear.
- Letting makers share privileged connector accounts.
- Treating a pilot’s enthusiastic creator as a sustainable support model.
- Buying multiple overlapping platforms before defining the boundary each should serve.
