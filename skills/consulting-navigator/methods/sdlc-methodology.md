# SDLC Methodology
## Purpose
Define the end-to-end software development lifecycle so systems are planned, built, tested, released, and maintained under consistent control. It specifies portfolio-level phases, gates, artifacts, and responsibilities while allowing teams to choose an appropriate delivery style inside them.
## Use
- Defining how the organization plans, builds, tests, releases, and maintains software systems
- Standardizing delivery across internal teams and vendors with clear stage gates or iterative loops
- Embedding security, quality, and operations checkpoints into the software lifecycle
## Avoid
- You only need a team-level agile practice playbook—use scrum-framework or agile-product-management
- The problem is IT service operations after go-live—use itil
- You are industrializing ML models specifically—use mlops-lifecycle
## Inputs
**Must-have:** Types of systems delivered (custom, package, integration, platform); regulatory, security, and audit constraints on software change; current delivery pain points across requirements, build, test, and release; tooling for ALM, CI/CD, and environments; roles spanning product, engineering, QA, security, and operations.

**Nice-to-have:** application criticality tiers, vendor contract obligations, incident history, architecture standards, and data classification rules.

**When data is thin:** establish a minimum lifecycle for the highest-risk system class first, then add variants only when their control need is demonstrated.
## Procedure
1. **Classify delivery contexts.** Segment work by system criticality, change type, regulatory exposure, and delivery model. A production payment change should not follow the same evidence path as a low-risk internal report.
2. **Design lifecycle states and entry criteria.** Define how an idea moves through discovery, requirements, design, build, verification, release, operate, and retirement. For each transition, specify required artifacts, decision rights, and allowable exceptions.
3. **Embed controls in the work.** Place security, privacy, architecture, test, accessibility, operational-readiness, and change-control activities where defects are cheapest to prevent. Connect requirements through acceptance evidence and deployment records for traceability.
4. **Define roles, tooling, and handoffs.** Assign product, engineering, quality, security, operations, and vendor responsibilities. Configure repositories, backlog or requirements tools, test evidence, pipelines, and environment promotion so the prescribed controls are usable.
5. **Pilot and govern adoption.** Run representative initiatives through the proposed lifecycle, measure delay and defect effects, revise confusing gates, and establish an exception authority. Publish training and a review rhythm for lifecycle performance.
## Output Contract
Produce a target-state lifecycle design with delivery classes, phase definitions, gate criteria, mandatory artifacts, role matrix, traceability path, tool integration expectations, exception process, and adoption roadmap. It must show how a change moves from request through retirement and which evidence authorizes production release.
## Evidence
Use existing workflow data, audit findings, incidents, and tool records as observed evidence. Treat proposed gate effort, automation coverage, and vendor capability as assumptions to test in pilots. A waiver must state the control omitted, compensating control, risk owner, expiry, and approval. Do not claim end-to-end traceability where requirements, code, tests, and releases cannot be linked.
## Checks
- Every delivery class has proportionate, explicit entry and exit criteria.
- Security and operational checks occur before the release decision.
- Required artifacts have an accountable creator and approver.
- Exception paths are controlled rather than informal bypasses.
- The lifecycle accommodates iterative teams without removing mandatory evidence.
## Failure Modes
- Imposing one heavyweight gate sequence on low-risk work until teams route around it.
- Treating a CI pipeline as proof that security and user acceptance happened.
- Inviting operations only after the release date is fixed.
- Allowing vendors to use unrelated artifacts with no traceability to internal controls.
- Retaining obsolete systems with no lifecycle owner or retirement decision.
