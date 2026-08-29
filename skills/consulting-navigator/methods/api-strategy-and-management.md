# API Strategy & Management
## Purpose
Design the API portfolio, standards, and operating model that turn capabilities into reusable, governed digital products. It treats an interface as a managed product with consumers, a lifecycle, service commitments, and accountable owners.
## Use
- Productizing internal capabilities as APIs for partners, channels, or internal reuse
- Designing API portfolio, ownership, monetization, and lifecycle management
- Reducing integration cost while enabling ecosystem or multi-channel delivery
## Avoid
- The question is broader multi-party value creation without interface design—use ecosystem-strategy
- You need enterprise architecture standards overall—use togaf or it-strategy-alignment
- Security posture is the sole gap without API product design—use cybersecurity-framework
## Inputs
**Must-have:** Domain/capability map of reusable services and data products; current integration inventory and pain points; target consumers (internal, partner, public) and commercial intent; non-functional requirements for security, latency, and scale.

**Nice-to-have:** Traffic volumes, developer research, current contracts, API usage analytics, service ownership, and competitor or partner requirements.

**When data is thin:** Begin with a consumer interview and a small contract prototype; avoid publishing a broad catalog based solely on the producing team’s idea of reuse.
## Procedure
1. **Identify candidate capabilities and consumers.** Map business domains, data, and services that multiple products or partners may need. Describe the consumer job and current integration pain for each candidate.
2. **Rationalize the portfolio.** Group duplicate endpoints, decide what is a reusable product versus a private integration, and prioritize candidates by consumer value, reuse potential, strategic importance, and cost to operate.
3. **Design interface and lifecycle standards.** Define resource or event conventions, versioning, documentation, testing, deprecation, compatibility, error behavior, and service-level expectations. Make choices that let consumers migrate predictably.
4. **Set access and commercial policies.** Specify authentication, authorization, rate limits, consent, data classification, onboarding, support, quotas, pricing or chargeback, and contract terms by consumer type.
5. **Establish the operating model.** Assign product owner, technical steward, support path, funding, gateway administration, review forum, and metrics. Clarify what domain teams own versus the platform team.
6. **Publish, observe, and evolve.** Launch a small number of high-value interfaces, measure adoption, errors, latency, developer effort, and revenue or savings, then version or retire products based on actual use.
## Output Contract
Deliver an API portfolio roadmap and management model listing candidate APIs, intended consumers, business value, ownership, interface and versioning standards, security and access rules, service levels, lifecycle stage, commercial terms, dependencies, launch sequence, and operating metrics. It must make it clear which interfaces will be treated as products and how consumers can rely on them.
## Evidence
Integration inventory, traffic logs, incident data, and consumer interviews are observed evidence. Reuse forecasts and monetization estimates are assumptions with an identified customer segment and volume basis. Separate a technically reusable service from one that consumers will actually adopt. For any API exposing sensitive data, retain the data-classification and access-decision record with the portfolio entry.
## Checks
- Every planned interface has a named consumer and owner.
- Versioning and deprecation rules prevent silent breaking changes.
- Non-functional commitments are measurable and suitable for the consumer type.
- Access, rate limits, and data handling reflect risk rather than being copied across all APIs.
- Portfolio metrics include adoption and developer experience, not endpoint count alone.
## Failure Modes
- Publishing internal service wrappers as “products” without a consumer problem or support model.
- Making incompatible changes under the same version and causing partner outages.
- Centralizing all design decisions until domain teams bypass the standards.
- Treating an API gateway purchase as a portfolio and lifecycle strategy.
