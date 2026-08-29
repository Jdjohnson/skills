# Weighted Average Cost of Capital
## Purpose
Compute the blended after-tax required return on the firm's financing mix for discounting and hurdle-rate use. It derives the rate from capital structure and component financing costs so valuation and investment decisions use a consistent cost of funds.
## Use
- Estimating the blended required return on debt and equity for valuation or capital budgeting
- Setting a firm- or division-level hurdle rate consistent with risk and capital structure
- Refreshing discount-rate assumptions when rates, beta, or leverage change
## Avoid
- You need project ranking once a rate already exists—use npv-and-irr-analysis
- Relative market pricing without a discount rate is sufficient—use valuation-multiples
- The decision hinges on flexibility value under uncertainty—use real-options-analysis with risk-neutral or decision-tree methods
## Inputs
**Must-have:**
- Target capital structure or current debt and equity weights
- Cost of equity inputs (risk-free rate, equity risk premium, beta or equivalent)
- Pre-tax cost of debt and marginal tax rate
- Preferred or hybrid capital terms if material

**Nice-to-have:** debt maturities, comparable betas, country-risk premium, credit spreads, and divisional adjustments.

**When data is thin:** document proxy inputs, use a range, and do not present one rate as fact.
## Procedure
1. **Set scope and capital convention.** Decide whether the rate applies to firm, division, or comparable-risk project. Choose market-value or target weights and state why. Output: scope and weighting basis.
2. **Estimate cost of equity.** Select risk-free rate, equity risk premium, and beta or equivalent. If using comparables, unlever and relever beta for the chosen debt policy. Output: equity-cost calculation.
3. **Estimate pre-tax debt cost.** Use borrowing yields, credit spreads, or lender indications for comparable maturity and seniority. Separate coupon from marginal funding cost for new capital. Output: debt-cost bridge.
4. **Calculate after-tax components and weights.** Apply the marginal tax rate to deductible debt cost, include preferred or hybrid capital where material, and multiply each component by its target weight. Reconcile weights to 100%. Output: WACC bridge.
5. **Stress-test and approve usage.** Show sensitivity to rates, beta, spread, tax, and leverage; explain when a different rate is needed. Record owner, effective date, and applications. Output: rate recommendation and sensitivity table.
## Output Contract
A discount-rate model with scope, capital weights, cost of equity, pre-tax and after-tax debt cost, other components, formula, bridge, sensitivities, market-input dates, and approval date. It states corporate versus risk-adjusted use. It supplies a valuation rate; it does not calculate value or rank projects.
## Evidence
Classify yields, market capitalization, tax law, and debt terms as observed with dates. Treat target leverage, equity risk premium, beta adjustments, and project comparability as judgments. Keep nominal and real rates consistent with cash flows, currency, and inflation. Do not use book weights just for convenience. Show rationale for a division's adjusted rate.
## Checks
- Capital weights sum to 100% and use the declared valuation convention.
- Debt cost reflects marginal financing risk and is tax-adjusted only once.
- Equity inputs have dates and a stated method.
- Cash-flow currency, inflation basis, and tax treatment match the intended DCF.
- Sensitivity shows the rate impact of plausible changes in leverage and market conditions.
## Failure Modes
- Averaging historical coupon rates when new debt would price at a different spread.
- Mixing book debt with market equity without explaining the resulting weights.
- Applying a corporate rate to a project whose risk differs substantially.
- Double-counting tax benefits in both after-tax cash flows and the debt component.
- Updating the risk-free rate while leaving beta, credit spread, and capital structure stale.
