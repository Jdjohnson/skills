# Waterfall Methodology
## Purpose
Plan and execute delivery as a linear sequence of gated phases so each stage completes and is accepted before the next begins. It establishes baselines, formal handoffs, and controlled changes for work whose requirements and dependencies can be specified early.
## Use
- Requirements can be specified with high confidence before detailed design and build
- Contractual, regulatory, or engineering constraints favor sequential phase gates
- Producing a baseline roadmap of analysis → design → build → test → deploy with formal exits
## Avoid
- Uncertainty is high and learning must change scope every few weeks—use scrum-framework
- You need a full governance method with board roles and tolerances—use prince2
- Flow efficiency of continuous work items is the problem—use kanban-system
## Inputs
**Must-have:**
- Stable high-level requirements or statement of work
- Phase definitions and exit/entry criteria
- Major deliverables and acceptance standards per phase
- Constraints on sequence (regulatory, contractual, technical dependencies)
- Budget and milestone date envelope

**Nice-to-have:** work breakdown, supplier lead times, verification protocol, change board, and prior estimates.

**When data is thin:** retain uncertainty, create discovery deliverables before baseline approval, and avoid a false freeze.
## Procedure
1. **Define lifecycle and deliverables.** Tailor analysis, requirements, design, build, verification, deployment, and closure. Identify output and acceptance evidence for each. Output: phase model.
2. **Baseline requirements and interfaces.** Document scope, constraints, dependencies, contract assumptions, and traceable requirements. Obtain formal acceptance from the authorities who can authorize the next phase. Output: approved requirements baseline.
3. **Plan sequential work and gates.** Build the work breakdown, dependencies, resources, milestones, entry criteria, exit criteria, and gate reviewers. Include verification activity early enough that it can be planned, even though execution follows build. Output: integrated baseline schedule.
4. **Execute each phase to evidence.** Produce the phase deliverable, conduct reviews, resolve defects, and collect the agreed evidence before opening downstream work. Output: accepted phase package.
5. **Control changes and close.** Route requested changes through impact analysis for cost, schedule, requirements, and previously approved work. Update controlled baselines only after authorization, then complete final acceptance and lessons learned. Output: change log and closure record.
## Output Contract
A phase-gated delivery plan with lifecycle, requirements baseline, deliverables, milestones, dependencies, roles, criteria, acceptance evidence, change control, dates, and budget. It tells vendors and sponsors what must be accepted before the next phase. It is a sequential delivery contract, not a sprint backlog or funding framework.
## Evidence
Treat signed requirements, approved designs, test records, and contract terms as controlled evidence. Mark estimates, dependency dates, and unvalidated interface behavior as assumptions. Preserve requirement-to-test traceability; a signed document is not proof that the delivered item works. Any material change must show its effect on downstream work and on prior acceptance evidence. If requirements are unstable, report that condition rather than hiding it in contingency.
## Checks
- Every phase has entry criteria, a tangible deliverable, exit criteria, and an approver.
- Requirements trace through design, build, verification, and acceptance.
- The critical path reflects genuine technical or contractual dependencies.
- No phase gate relies only on a calendar date or verbal assurance.
- Change requests state impacts before an approval decision.
## Failure Modes
- Starting detailed build before requirements and interfaces are actually accepted.
- Treating a phase label as a gate while leaving exit evidence undefined.
- Freezing ambiguous requirements and moving rework into change control later.
- Deferring verification planning until after build, when test environments and criteria are unavailable.
- Allowing urgent vendor work to bypass baselines without recording the impact.
