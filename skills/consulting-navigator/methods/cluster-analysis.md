# Cluster Analysis
## Purpose
Group customers, products, or other units into similarity-based segments from multi-feature data. The method discovers empirical structure in an unlabeled feature matrix before a business team names, sizes, and chooses how to use the segments.
## Use
- You have multi-dimensional object data and need empirically similar groups
- Segmentation must be data-driven rather than a priori labels
- Downstream targeting, pricing, or product design needs a segmented map of the base
## Avoid
- You already have a validated segment scheme and need go-to-market plays—use stp-framework
- The goal is attribute importance or price sensitivity, not grouping—use conjoint-analysis or price-sensitivity-meter
- You need causal drivers of an outcome rather than similarity groups—use regression-analysis
## Inputs
**Must-have:** Observation-level dataset with comparable features across units; chosen distance/similarity logic and scaling approach; decision rule for number of clusters (or range to test); business labels and validation criteria for interpretability; holdout or stability checks for segment robustness.

**Nice-to-have:** weights for commercial importance, geographic context, qualitative interviews, and a prior segmentation to compare against.

**When data is thin:** reduce the feature set, avoid fragile small clusters, and label the result exploratory until a fresh sample confirms it.
## Procedure
1. **Choose the unit and features.** Set one row per customer, product, or account and select features available for every row. Remove identifiers, define the time window, handle missing values, and justify exclusions that may hide a meaningful group.
2. **Prepare the feature space.** Transform skewed variables where needed, standardize comparable numeric features, encode categorical variables appropriately, and select a distance measure that matches the data type. Check whether one high-range feature still dominates distances.
3. **Run candidate clustering models.** Test a justified range of cluster counts and, where useful, compare k-means, hierarchical, density-based, or other structures. Record seed, algorithm settings, and treatment of outliers.
4. **Validate structure and stability.** Review within- and between-cluster separation, cluster sizes, holdout assignments, and resampled stability. Inspect outliers instead of forcing them into a misleading group.
5. **Profile and operationalize the clusters.** Describe each group using features not used as labels alone, give it a business-readable name, size its opportunity, and specify permitted downstream use. Do not turn statistically distinct groups into personas without qualitative validation.
## Output Contract
Deliver a segmented map with data scope, feature dictionary, preparation rules, algorithm and parameter choices, selected cluster count, validation results, membership labels, profiles, sizes, and known limitations. The report must make it possible to reproduce assignments for a new record and explain why the grouping is stable enough for its intended decision.
## Evidence
Raw records and documented transformations are observed. Choices of feature weights, distance, number of clusters, and labels are assumptions or analytic judgments. Preserve row exclusions, imputation rules, and random seeds. If a cluster profile relies on a feature with many missing values or a tiny membership, flag it. Similarity supports segmentation; it does not establish that cluster membership causes behavior.
## Checks
- Rows describe the same unit and time horizon.
- Scaling and distance logic fit the feature types.
- Candidate solutions are compared rather than accepting the first attractive chart.
- Small, unstable, and outlier clusters are examined explicitly.
- Profiles are interpretable and useful without hiding weak validation metrics.
## Failure Modes
- Letting annual spend overwhelm every behavioral feature because variables were not scaled.
- Naming a two-member outlier group a strategic segment.
- Selecting 4 clusters only because a stakeholder requested 4 colored boxes.
- Treating a silhouette statistic as proof that the segments are commercially actionable.
