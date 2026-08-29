# TOGAF
## Purpose
Frame and structure enterprise architecture work so current and target states across business, data, application, and technology are designed under a standard method. The discipline makes design choices and their dependencies governable across initiatives.
## Use
- Establishing enterprise architecture practice with a standard ADM-style method and artifact set.
- Framing current and target architecture across business, data, application, and technology domains.
- Governing major change programs so solutions fit an enterprise target state.
## Avoid
- You only need a strategy-to-IT fit diagnosis without full EA method—use it-strategy-alignment.
- You need IT control and assurance objectives rather than architecture method—use cobit.
- You need service management practices for run operations—use itil.
## Inputs
**Must-have:** Business strategy and capability priorities; inventory of applications, data domains, and infrastructure; known pain points (duplication, integration debt, compliance); stakeholders who will own architecture governance; scope boundaries for the architecture effort (enterprise vs. domain).

**Nice-to-have:** capability maps, integration inventories, standards catalogues, and investment roadmaps.

**When data is thin:** establish a bounded domain architecture and a discovery backlog; do not present an enterprise-wide target model as fact when only one business area has been examined.
## Procedure
1. **Establish the architecture mandate.** Confirm sponsor, scope, principles, repository, decision rights, and how conformance will be enforced. Translate strategy into capabilities and measurable architecture concerns.
2. **Describe the baseline by domain.** Map business capabilities and processes, data ownership and flows, applications and interfaces, then platforms and networks. Mark pain points such as duplicate masters or brittle point-to-point links.
3. **Design the target state.** Define desired capabilities, domain building blocks, data principles, integration patterns, and technology standards. Trace each target element to a business outcome and state what intentionally remains outside scope.
4. **Analyze gaps and dependencies.** Identify components to retain, retire, replace, build, or procure. Sequence dependencies, transition states, risks, and standards exceptions; avoid a target diagram that cannot be migrated to.
5. **Govern delivery and change.** Produce work packages, architecture contracts, review checkpoints, and a change-request path. Maintain requirements traceability so new initiatives update the architecture rather than bypassing it.
## Output Contract
The architecture package contains scope and principles, baseline and target views across the four domains, a standards and decision log, gap analysis, transition architectures, and a prioritized migration roadmap. Each work package names its accountable owner, dependency, and conformance test. It must enable design review and investment sequencing, rather than merely documenting the application estate.
## Evidence
Treat system inventories, interface logs, approved policies, and accountable-owner interviews as observed inputs. Mark inferred flows where evidence comes from workshops rather than runtime traces. State assumptions about future volumes, acquisitions, vendor capability, and funding. Unknown data ownership or technical debt is a risk register item, not an empty box on a diagram. Version every view with its scope and effective date.
## Checks
- The baseline reconciles with named owners for material applications and data domains.
- Each target component has a capability rationale and a decision record.
- Business, data, application, and technology views use consistent definitions.
- Transition states identify coexistence, migration, and decommission conditions.
- Governance includes an exception process with expiry, not an aspirational standards list.
## Failure Modes
- Producing polished diagrams without decisions that teams must follow.
- Declaring a canonical data source while leaving stewardship unresolved.
- Designing a target state with no bridge for legacy interfaces.
- Treating a vendor product catalogue as the enterprise architecture.
- Allowing projects to claim exceptions indefinitely.
