# RPA Implementation Framework
## Purpose
Plan and govern robotic process automation so high-volume rule-based work is automated safely with measurable savings and maintainable bots. The framework selects suitable work and builds controls for UI-based automation after launch.
## Use
- Automating high-volume, rules-based tasks sitting on legacy UIs that are not near replacement
- Standing up an RPA factory with intake, prioritization, build standards, and support
- Sequencing bots after process standardization so automation compounds rather than freezes waste
## Avoid
- The process is broken end-to-end and needs redesign first—use business-process-reengineering or value-stream-mapping
- You need application rebuild or workflow apps rather than UI bots—use low-code-no-code-strategy or sdlc-methodology
- Work is judgment-heavy or unstructured with no stable rules—do not force RPA
## Inputs
**Must-have:**
- Candidate process inventory with volumes, rules stability, and exception rates
- As-is process maps for priority candidates
- System access, security, and control requirements for bots
- Baseline FTE effort and error rates for benefits tracking
- RPA platform constraints and support model options

**Nice-to-have:** release calendars, audit findings, business-continuity requirements, and reusable component inventory.

**When data is thin:** choose a discovery pilot that measures volume, variation, and exceptions before promising savings or unattended operation.
## Procedure
1. Establish intake criteria and score candidates for volume, rule stability, input quality, exception rate, benefit, control complexity, and process maturity. Exclude processes needing redesign or human judgment.
2. Walk the as-is process with operators, documenting every screen, decision rule, data source, exception, credential, handoff, and manual workaround. Standardize avoidable variants before automation design.
3. Select the operating mode and architecture: attended or unattended, queue design, reusable components, environment separation, and human fallback. Specify bot ownership and service-level expectations.
4. Design controls for identity, least-privilege access, credential vaulting, change approval, audit logs, exception handling, reconciliation, and segregation of duties. Confirm that bot actions are traceable.
5. Build and test against representative happy paths and exception cases. Reconcile outputs to the source system, perform user acceptance testing, and document release and rollback steps.
6. Launch through an operations model with monitoring, incident routing, change control, benefits tracking, and periodic requalification as source interfaces or rules change.
## Output Contract
Provide an RPA roadmap and operating model covering candidate scores, automation boundaries, process-readiness findings, architecture, controls, test evidence, release sequence, support roles, exception workflow, and benefits baseline. For each approved bot include a business owner, technical owner, credential/control design, service target, change path, and measure of savings or errors avoided. The plan must make fragile UI dependencies and manual fallback visible; it is not a generic automation wishlist.
## Evidence
Use transaction volumes, process observations, access reviews, audit requirements, and measured handling time as observed inputs. Label expected straight-through rate, UI stability, savings realization, and exception growth as assumptions subject to pilot evidence. Never equate a bot demonstration with production readiness when credentials, recovery, or monitoring remain unproven.
## Checks
- Candidate selection accounts for exceptions and control burden, not volume alone.
- The as-is map contains every manual variant before the bot is sized.
- Bot credentials are vaulted, rotated, and limited to required actions.
- Test evidence covers business exceptions, reconciliation, and outage recovery.
- Production monitoring has named responders and measurable service thresholds.
## Failure Modes
- Automating a wasteful process and making the waste run faster.
- Building selectors that fail when a vendor changes a screen label.
- Sharing a human password with an unattended bot and losing auditability.
- Counting theoretical FTE savings while the manual team and bot support cost both remain.
- Releasing without an exception queue, leaving transactions stranded after the first mismatch.
