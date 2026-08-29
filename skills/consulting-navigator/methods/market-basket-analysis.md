# Market Basket Analysis
## Purpose
Mine multi-item transaction data for association rules that show which products co-occur and which cross-sell or assortment moves are supportable.
## Use
- You have transaction-level multi-item purchase or order data
- You need co-occurrence rules for assortment, bundling, or cross-sell offers
- You want frequent itemsets before building personalized recommenders
## Avoid
- You need causal drivers of demand or price response—use regression-analysis or price-elasticity-analysis
- You only have stated preferences, not baskets—use conjoint-analysis or survey-design-methodology
- You need segment structure first, not co-purchase rules—use cluster-analysis
## Inputs
**Must-have:**
- Transaction or order records with multi-item baskets and timestamps
- Product or SKU master with categories and stable identifiers
- Minimum support and confidence thresholds or business lift targets
- Channel and store or site filters if co-occurrence varies by context

**Nice-to-have:** product margin, promotion exposure, stockout flags, substitution candidates, customer eligibility rules, and a test channel for offers or placement.

**When data is thin:** combine only comparable periods or categories and raise the support threshold. A surprising pair in eight baskets is a hypothesis, not a merchandising instruction.
## Procedure
1. **Construct the basket table.** Define a transaction boundary, remove returns and duplicate lines appropriately, and map SKUs to the product grain that a merchant can act on. Output: analysis-ready baskets.
2. **Choose the population.** Split stores, channels, customer types, seasons, or promotion states when their buying missions differ; exclude periods dominated by stockouts. Output: scoped cohorts.
3. **Mine frequent itemsets.** Apply a support threshold to find combinations present often enough to matter, then generate directional rules such as A → B. Output: candidate rule set.
4. **Score and filter rules.** Calculate support, confidence, lift, and incremental margin; remove tautological category pairs, duplicate variants, and rules that cannot be offered together. Output: ranked opportunities.
5. **Design a commercial test.** Translate selected rules into adjacency, bundle, recommendation, or coupon treatments with a holdout and guardrails for cannibalization. Output: test backlog.
## Output Contract
Provide a rule book showing antecedent and consequent items, population, basket count, support, confidence, lift, expected margin, and recommended action. Include exclusions, segments where the rule differs, and a test plan for the highest-value rules. The deliverable identifies associations; it must not present co-purchase as proof that placement or promotion caused a sale.
## Evidence
Treat transaction records and available-product status as observed. Treat product hierarchy decisions, thresholds, and margin estimates as assumptions that must be documented. Compare rules against a relevant baseline: a high confidence can be unremarkable when the consequent is purchased by almost everyone. Label seasonal, promotional, and channel effects that may create a spurious association. Validate a recommendation through an experiment before forecasting realized cross-sell.
## Checks
- Each basket has a stable transaction identifier and a defensible time boundary.
- Support is reported with its denominator, not as a raw count alone.
- Lift accompanies confidence for every promoted rule.
- Rules respect inventory, customer eligibility, and product compatibility.
- The short list includes a commercial action and a measurable holdout test.
## Failure Modes
- Combining every SKU variant so the algorithm “discovers” obvious family duplicates.
- Recommending a high-confidence item that is already bought by nearly all customers.
- Reading a promotion-created pair as a durable affinity.
- Ignoring stockouts, which make companion items appear less associated.
- Selecting hundreds of mathematically valid rules with no merchant decision attached.
