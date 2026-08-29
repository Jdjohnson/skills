# Business Continuity Planning
## Purpose
Keep priority business operations running through and after major disruption by pre-agreeing recovery priorities, workarounds, and continuity capabilities. The plan is built around the service the business must sustain, rather than around technology restoration alone.
## Use
- Designing how critical business processes continue through disruption, not only how IT recovers
- Responding to board, customer, or regulatory pressure for formal continuity readiness
- Linking recovery priorities to business impact and maximum tolerable downtime
## Avoid
- The scope is purely restoring systems and data after an IT outage—use disaster-recovery-planning
- You are in the first 72 hours of an active incident and need command, comms, and decisions now—use crisis-management-framework
- You still lack a ranked list of critical processes and dependencies—run impact analysis and supply-chain-resilience-analysis first
## Inputs
**Must-have:**

- Business impact analysis with critical processes, RTOs, and RPOs
- Dependency map of people, sites, systems, suppliers, and data
- Current backup, alternate-site, and workaround capabilities
- Regulatory, customer, and contractual continuity obligations

**Nice-to-have:** contact trees, mutual-aid agreements, emergency spend authority, manual forms, and prior exercise findings.

**When data is thin:** plan a tabletop for the most critical process first and label untested dependencies rather than declaring the whole organization recoverable.
## Procedure
1. **Confirm continuity objectives.** For each priority process, translate impact analysis into a maximum tolerable interruption, minimum service level, recovery-time objective, and recovery-point objective. Output: recovery priorities approved by process owners.
2. **Map the failure path.** Trace the people, facility, applications, data, equipment, utilities, and suppliers required to perform the minimum service. Identify single points of failure and dependencies that have longer recovery times than the process. Output: dependency-and-gap register.
3. **Choose workable continuity strategies.** Select a practical combination of alternate location, remote work, cross-trained staff, manual workaround, backup supplier, and restored-system sequence. Test whether the selected capability can meet the objective. Output: strategy decision for each critical process.
4. **Write activation and recovery playbooks.** Define trigger conditions, incident roles, first-hour actions, customer commitments, manual operating steps, escalation contacts, and the handoff back to normal operations. Output: usable process playbooks.
5. **Exercise and maintain.** Run a scenario that disables a material dependency, time each handoff, record failures, and assign corrective actions. Set review triggers for organizational, supplier, system, or contractual change. Output: exercise record and maintenance calendar.
## Output Contract
The continuity package lists prioritized processes and their objectives, dependency gaps, selected strategies, role-specific activation playbooks, communications responsibilities, exercise results, and open remediation actions. A reader should be able to determine how invoicing, fulfillment, or another named process continues at its minimum acceptable level during a stated disruption.
## Evidence
Use signed obligations, site capabilities, system recovery tests, and staffing rosters as observed evidence. Mark untested remote-access capacity, supplier response time, and manual throughput as assumptions. Treat a recovery-time objective as a business requirement, not proof of technical feasibility. A process cannot be claimed recoverable when a dependency has no named workaround or tested owner.
## Checks
- Priority order reflects business impact rather than the loudest department.
- Every critical dependency has an owner, alternate, or explicit accepted gap.
- Playbooks say who activates them and what occurs before systems return.
- Recovery timing is tested against the stated objective.
- Exercise findings become dated remediation actions, not meeting notes.
## Failure Modes
- Treating a data backup as proof that order fulfillment can resume.
- Designing an alternate site without seats, credentials, or trained staff.
- Publishing a contact list that fails when the primary communication system is down.
- Testing only an IT restore while ignoring manual approvals and supplier cutoffs.
- Leaving recovery priorities unchanged after a product, site, or outsourcing change.
