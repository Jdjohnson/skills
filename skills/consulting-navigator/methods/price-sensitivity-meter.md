# Price Sensitivity Meter
## Purpose
Elicit customer-stated acceptable price ranges and indifference points to bound viable list prices for a product or concept. It uses four direct price-threshold questions and cumulative response curves, so it produces perceived acceptance boundaries rather than observed elasticities or feature-level part-worths.
## Use
- You need stated acceptable price ranges for a product or concept before full market modeling
- Historical transaction data are unavailable or unusable for elasticity estimation
- Early pricing hypotheses must be bounded with survey evidence quickly
## Avoid
- You need feature-level willingness-to-pay trade-offs—use conjoint-analysis
- You have rich transaction history and need behavioral elasticity—use price-elasticity-analysis
- Price realization is leaking after list is set—use pricing-waterfall-analysis
## Inputs
**Must-have:** Defined product or concept description shown to respondents; survey sample of target customers; Van Westendorp four-question price responses; optional competitive reference prices for context.

**Nice-to-have:** segment quotas, purchase-frequency data, current paid price, verbatim price rationale, and concept comprehension checks.

**When data is thin:** treat the curves as directional, widen reported bands, and conduct interviews to verify that respondents understood the concept and currency.
## Procedure
1. **Fix the offer shown to respondents.** Write a neutral, complete description of the product, package, unit, channel, currency, and purchase context. Do not allow different respondents to price different offers. Output: test stimulus.
2. **Field four threshold questions.** Ask at what price the offer is too cheap to trust, a bargain, becoming expensive but still considered, and too expensive to consider. Randomize nothing that changes their meaning. Output: respondent-level price file.
3. **Clean and segment responses.** Remove incomplete or logically inconsistent answers according to a predeclared rule; retain segment, familiarity, and current-price fields. Output: analysis-ready sample.
4. **Build cumulative curves.** Convert each threshold distribution to cumulative shares, reversing direction where needed, and graph their intersections. Output: price sensitivity chart.
5. **Interpret range and points.** Identify the range bounded by unacceptable extremes and the crossings commonly used as indifference and optimal-price references; compare segments without pretending the points are sales forecasts. Output: recommended test band.
6. **Validate the decision use.** Check concept comprehension, competitive context, and outlier influence; specify follow-up testing before setting final price. Output: limitations and next-study plan.
## Output Contract
An assessment with the exact offer stimulus, sample definition, four response distributions, cleaning rules, cumulative curves, acceptable-price band, intersection points, segment comparisons, limitations, and a recommended price-testing range. It must keep stated perceptions separate from predicted demand, revenue, or willingness-to-pay for individual features.
## Evidence
Survey answers are observed statements, not observed purchase behavior. Curve intersections are calculated inferences from the sample. State assumptions about representativeness, concept understanding, respondent familiarity, and whether competitors were visible. Preserve raw distributions and excluded-response rules. If respondents anchor on an implausible currency or package size, fix the stimulus and rerun rather than silently trimming inconvenient answers.
## Checks
- Every respondent sees the same product, unit, and buying context.
- The four thresholds are asked distinctly and pass logical-order checks.
- Sample quotas represent the decision population or the limitation is explicit.
- Curves use the correct cumulative direction and label all intersections.
- Results show distributions and segments, not one unsupported “perfect” price.
## Failure Modes
- Asking about a vague concept so respondents price different imagined products.
- Confusing the lowest acceptable point with a revenue-maximizing price.
- Treating stated bargain thresholds as a substitute for actual purchase behavior.
- Combining currencies, package sizes, or customer types in one curve.
- Removing extreme responses after seeing the desired answer without a declared rule.
