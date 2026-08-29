# Time Series Forecasting
## Purpose
Project future values of a metric from its own ordered history by modeling trend, seasonality, and serial dependence. Use it to create a repeatable baseline before managers add event intelligence or planning judgment.
## Use
- You have ordered historical observations and need future values of the same metric.
- Seasonality, trend, and autocorrelation dominate over cross-sectional drivers.
- A statistical baseline forecast is required for planning, inventory, or financial outlooks.
## Avoid
- Cross-sectional drivers and elasticities are the main question—use regression-analysis or marketing-mix-modeling.
- You need to stress one business case assumption set—use sensitivity-analysis.
- History is too short or broken to support a series model—use expert-interviewing or delphic-method judgment forecasts.
## Inputs
**Must-have:** Historical time-stamped series at consistent grain (daily, weekly, monthly); calendar, seasonality, and known event or holiday flags; forecast horizon, cadence, and accuracy metrics (MAPE, bias, etc.); policy for handling structural breaks, missing periods, and outliers.

**Nice-to-have:** prior forecast vintages, promotion calendars, weather or outage annotations, and a documented override process.

**When data is thin:** use the longest comparable series available, publish a shorter horizon, and label the result as a directional baseline rather than estimating detail the history cannot support.
## Procedure
1. **Set the series contract.** Name the measure, unit, geography, aggregation level, cutoff date, forecast horizon, and decision that consumes it. Fill missing periods and confirm that a zero means zero rather than an absent record.
2. **Inspect the history.** Plot the series, seasonal subseries, and lag correlations. Separate calendar effects, level shifts, exceptional events, and data errors; retain a log explaining any correction or exclusion.
3. **Create holdout periods.** Reserve the latest complete cycles as a test set. Compare seasonal-naive, moving-average, exponential-smoothing, and autoregressive candidates against the same cutoff, rather than choosing a sophisticated model by appearance.
4. **Fit and diagnose the selected model.** Estimate trend and seasonal components on the training portion. Examine residuals for remaining pattern, biased error, and unusually influential observations; refit if the residuals still carry predictable structure.
5. **Issue and maintain the forecast.** Produce point forecasts, prediction intervals, and a bias review by horizon. Record an owner, refresh date, override reason codes, and the rule for declaring a structural break.
## Output Contract
A forecast pack provides the cleaned series definition, a chart of actuals and forecast, model comparison on held-out periods, selected specification, prediction intervals, accuracy by horizon, and an override register. It states the practical use of the baseline, such as replenishment or staffing. It is not a driver-coefficient study or an unconstrained planning consensus.
## Evidence
Treat timestamped transactions and calendar flags as observed. Treat an outlier classification or a detected regime shift as an inference supported by the plot and operational corroboration. Document choices of seasonal period, transform, and missing-value treatment as assumptions. A future promotion, competitor action, or policy change is an external scenario, not evidence that the historical pattern will repeat. Keep human adjustments separate from the statistical forecast and measure their later accuracy.
## Checks
- The series has no duplicated timestamps, unexplained gaps, or mixed units.
- Test periods include at least one meaningful seasonal cycle where seasonality is claimed.
- The selected model beats an appropriate naive benchmark or the report says it does not.
- Residuals are checked for autocorrelation and systematic bias.
- Intervals widen with horizon when uncertainty warrants it, and versions can be reconstructed.
## Failure Modes
- Treating a one-off stockout as a demand collapse.
- Training on data later used to declare the model accurate.
- Using monthly totals to forecast a weekly operational decision.
- Removing inconvenient peaks without retaining an audit trail.
- Letting sales overrides replace the baseline without recording their reason or error.
