# ITIL
## Purpose
Establish IT service management practices that control incidents, changes, and service value with clear ownership and continual improvement. It designs how services move from demand through delivery and support, not merely how tickets are logged.
## Use
- Designing or professionalizing IT service management practices for incident, problem, change, and request
- Stabilizing service quality and control after rapid growth or tool sprawl
- Aligning IT operations with measurable service value and continual improvement
## Avoid
- You need board-level IT governance and control objectives rather than service practices—use cobit
- The problem is software delivery method, not service operations—use sdlc-methodology or scrum-framework
- You need enterprise architecture structure—use togaf
## Inputs
**Must-have:** Service catalog or list of services offered to the business; Current incident, problem, change, and request volumes and pain points; Tooling landscape for ITSM and monitoring; SLA/OLA expectations and major risk or audit constraints; Operating model roles for service owners and support tiers.

**Nice-to-have:** Major-incident reports, service cost data, configuration records, customer satisfaction data, and release calendar history.

**When data is thin:** Begin with the highest-impact service and its incident flow; make temporary categorization rules explicit before using the data for trend conclusions.
## Procedure
1. **Define services and value streams.** Name the services customers consume, their outcomes, consumers, service owners, support boundaries, and measures. Map how demand, change, incident restoration, and improvement currently flow.
2. **Baseline performance and pain.** Examine incident severity, restore time, recurrence, request lead time, change success, backlog, and customer impact. Segment by service so a high-volume desktop issue does not hide a critical payment outage.
3. **Design priority practices.** Establish the workflow, roles, triggers, records, and handoffs for incident, problem, change enablement, service requests, knowledge, and service-level management. Define the distinction between restoring service and removing a recurring cause.
4. **Set control and automation points.** Configure categorization, impact/urgency priority, major-incident communication, change risk assessment, approval paths, standard changes, and monitoring-to-ticket integration. Keep emergency change use auditable.
5. **Pilot the operating model.** Run the practices on selected services, observe queue behavior and handoffs, train service owners and support tiers, then correct impractical controls.
6. **Establish continual improvement.** Maintain a prioritized improvement register tied to service measures, review it with service owners, and verify whether changes improve customer outcomes rather than only tool compliance.
## Output Contract
An IT service management design with service definitions, value-stream maps, practice workflows, role and escalation model, measures, control points, tooling requirements, adoption waves, and a continual-improvement backlog. It must show how an incident becomes a problem investigation or a change when appropriate.
## Evidence
Ticket, monitoring, change, and service-level records are observed only when classification and timestamps are reliable. Treat anecdotal complaint volume as a prompt for sampling, not a service metric. Document priority rules, SLA clock exclusions, and the evidence for recurring-incident linkage. Where configuration data is incomplete, limit automated impact assessment and retain human triage.
## Checks
- Service owners own outcomes, while process owners maintain practice consistency.
- Priority combines impact and urgency; ticket age alone does not define severity.
- Change paths distinguish standard, normal, and emergency work with appropriate evidence.
- Problem records link recurring incidents to investigation, known errors, and permanent fixes.
- Improvement measures include service experience and reliability, not only closure volume.
## Failure Modes
- Rebranding the service desk while leaving unclear ownership for end-to-end services.
- Closing repetitive incidents quickly without opening a problem investigation.
- Making emergency change the routine path for poor release planning.
- Measuring agent productivity in a way that encourages premature ticket closure.
