# Price Elasticity Analysis
## Purpose
Estimate demand elasticity so price changes can be translated into expected volume, revenue, and margin outcomes. It estimates revealed customer response from observed price-volume variation with controls, rather than asking respondents for an acceptable range or designing value propositions.
## Use
- You must estimate how unit demand responds to price changes for list, promo, or segment prices
- Pricing decisions require volume and margin forecasts under alternative price points
- You need to compare elasticity across SKUs, segments, or channels
## Avoid
- No historical price variation exists—use price-sensitivity-meter or conjoint-analysis
- You need full feature-price trade-offs for a new concept—use conjoint-analysis
- The issue is discount leakage after list price is set—use pricing-waterfall-analysis
## Inputs
**Must-have:** Transaction or panel data with price and volume over time or cells; controls for promotions, seasonality, distribution, and competitive prices; defined product/segment units of analysis; cost or margin data if net-profit impact is required.

**Nice-to-have:** competitor price series, inventory availability, product changes, customer contract flags, and randomized or quasi-experimental price tests.

**When data is thin:** report a bounded hypothesis or run a controlled test; do not fit a coefficient to one price move that coincided with a promotion or stockout.
## Procedure
1. **Specify the demand unit and decision.** Define SKU, pack, channel, customer segment, time interval, price measure, and whether the decision concerns list, net, or promotional price. Output: estimation specification.
2. **Prepare the analytical panel.** Merge volume, realized price, discounts, promotion, availability, seasonality, distribution, and competitor variables; flag returns, stockouts, and changed packs. Output: cleaned panel and exclusions log.
3. **Choose and estimate a response model.** Fit an appropriate log-log, semi-log, discrete-choice, or panel model; include controls and segment interactions where sample size supports them. Output: coefficients and diagnostics.
4. **Challenge identification.** Test whether price moves were caused by demand conditions, check multicollinearity and outliers, compare holdout accuracy, and inspect whether signs and magnitudes are commercially plausible. Output: validated elasticity range.
5. **Translate scenarios into economics.** Apply candidate prices to forecast volume, revenue, contribution, and share; show uncertainty bands and cross-effects where material. Output: price scenario deck and recommendation.
## Output Contract
A forecast model that records the data grain, price definition, sample period, controls, model form, elasticity estimates with uncertainty, diagnostics, exclusions, and volume/revenue/margin scenarios. It must distinguish correlation from causal evidence and make the recommended price decision reproducible from the documented inputs.
## Evidence
Observed evidence includes invoices, scanner data, realized discounts, volumes, stockouts, and dated promotions. Coefficients and predicted scenarios are inferred estimates. State assumptions about competitor response, unchanged distribution, and stable product quality. Separate list-price changes from net-price changes after rebates. If the sample has no independent variation, describe the result as descriptive association and seek an experiment rather than claiming behavioral elasticity.
## Checks
- Price is measured consistently after discounts, rebates, and pack-size changes.
- Promotion, availability, seasonality, and distribution are controlled or their omission is justified.
- The estimation window includes enough variation for the segment-level claim made.
- Holdout or back-test performance is shown alongside in-sample fit.
- Scenario profit uses incremental margin and flags capacity or inventory constraints.
## Failure Modes
- Dividing a single volume change by a price change while ignoring a simultaneous promotion.
- Using list price when customers transact at widely different net prices.
- Treating stockouts as inelastic demand because sales did not rise after a discount.
- Applying an aggregate coefficient to every channel and customer segment.
- Choosing the revenue-maximizing price when margin or retention is the objective.
