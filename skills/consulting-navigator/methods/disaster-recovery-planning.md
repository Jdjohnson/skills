# Disaster Recovery Planning
## Purpose
Restore critical IT infrastructure, applications, and data to agreed service levels after a major outage or disaster. The plan turns recovery objectives into technical architecture, executable runbooks, and tested restoration decisions.
## Use
- Designing how IT systems, data, and tech services are restored after major outage or disaster
- Setting and validating RTO/RPO against architecture, backups, and failover capability
- Producing testable recovery runbooks for critical applications and infrastructure
## Avoid
- You need whole-business process continuity including people, sites, and suppliers—use business-continuity-planning
- The immediate need is executive crisis command and external communications—use crisis-management-framework
- The primary gap is preventative security controls rather than recovery design—use cybersecurity-framework first
## Inputs
**Must-have:** Inventory of critical systems, data stores, and dependencies; Agreed RTO/RPO targets from business impact analysis; Current backup, replication, and alternate-site or multi-region capability; Prior incident and restore-test results.

**Nice-to-have:** vendor recovery commitments, infrastructure diagrams, application owners, and emergency access procedures.

**When data is thin:** classify systems provisionally and prioritize discovery of dependency chains before assigning an RTO.
## Procedure
1. Inventory applications, infrastructure, data stores, interfaces, identities, and external providers. Map the dependency order required for a service to become usable, not merely powered on.
2. Confirm business impact and set recovery time objective, recovery point objective, minimum service level, and recovery owner for each tier. Resolve targets that conflict with cost or technical feasibility.
3. Choose recovery patterns—backup restore, pilot light, warm standby, active-active, or alternate-site—and design replication, network, identity, and data-integrity controls to meet each target.
4. Write runbooks with activation authority, restoration sequence, commands or console paths, validation checks, communication handoffs, and rollback criteria. Identify third-party access and license dependencies.
5. Exercise scenarios from declared disaster through service validation, measure actual RTO/RPO, log defects, and update architecture and procedures after each test.
## Output Contract
An implementation plan with tiered service inventory, dependency map, approved RTO/RPO targets, selected recovery architecture, backup and replication specifications, runbooks, contacts, test calendar, and remediation backlog. For every critical service, the package must state who declares recovery, how data integrity is checked, and what “restored” means to users.
## Evidence
Backup logs, replication status, failover records, and timed exercises are observed. A modeled recovery duration is inferred until a realistic test proves it. Vendor commitments and unavailable staff assumptions require documented terms and alternates. Unknown dependencies, credential availability, or data corruption behaviors invalidate an RTO claim and must be listed as test scope.
## Checks
- RTO and RPO are approved by the business owner and matched to a feasible technical design.
- The dependency map includes identity, DNS, integration, and third-party services.
- Runbooks can be executed by an on-call team without the original author.
- Restore tests validate transaction integrity, not only server availability.
- Test results measure elapsed time from declaration to usable service.
## Failure Modes
- Declaring an application recoverable because a virtual machine starts while its database and identity provider remain unavailable.
- Setting a four-hour RTO with nightly backups that can lose 24 hours of transactions.
- Testing a clean failover but never rehearsing restoration from a corrupted backup.
