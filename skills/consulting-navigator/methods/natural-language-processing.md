# Natural Language Processing
## Purpose
Apply computational language methods to large text corpora to extract themes, sentiment, entities, and patterns humans cannot code consistently at scale. The technique produces a repeatable pipeline and error-measured insights, not a collection of memorable quotes.
## Use
- Large volumes of unstructured text must be classified, themed, or scored at scale
- You need consistent extraction of topics, entities, or sentiment from reviews, tickets, chats, or notes
- Human coding cannot keep pace with the corpus and reproducibility matters
## Avoid
- The corpus is tiny and deep interpretation is the goal—use expert-interviewing, focus-groups, or ethnographic-research
- You need causal models of numeric outcomes from structured predictors—use regression-analysis
- You only need a single closed-ended survey instrument—use survey-design-methodology
## Inputs
**Must-have:** Text corpus with source, date, and linkage keys where possible; analysis goals (topics, sentiment, entities, intent, or similarity); labeled examples or taxonomy if supervised classification is required; quality criteria for precision, recall, or human-in-the-loop review.

**Nice-to-have:** language distribution, channel metadata, annotation guidelines, a consent review, and an outcome metric to join to text patterns.

**When data is thin:** sample and manually annotate representative text before selecting a model. A smaller validated classifier is preferable to an untested claim of corpus-wide insight.
## Procedure
1. **Frame the decision and unit.** Define whether a document, sentence, ticket, or conversation turn is classified and what decision will use the result. Freeze inclusion, date, and language rules.
2. **Prepare the corpus.** Deduplicate, remove boilerplate, preserve source metadata, redact or restrict sensitive data, and inspect language and length distributions. Split data by time or customer where leakage would otherwise occur.
3. **Choose the analytic task.** Use entity extraction for names and products, classification for known intents, topic discovery for unknown themes, or sentiment only where polarity is meaningful. Create a taxonomy with definitions and examples before supervised labeling.
4. **Train or configure and evaluate.** Hold out labeled text, calculate precision and recall by important class, inspect false positives and false negatives, and compare performance across channels, languages, and customer segments.
5. **Operationalize the insight.** Apply the approved pipeline, aggregate outputs at an appropriate level, retain confidence and version information, and route uncertain cases to human review. Monitor drift when vocabulary or products change.
## Output Contract
A text-insight package with corpus scope, preprocessing rules, task definition, taxonomy or prompts, model and version, evaluation results, error examples, confidence thresholds, aggregate findings, and a human-review path. It must show how raw text became each reported metric and which error types limit interpretation.
## Evidence
Raw messages and labeling decisions are evidence, subject to privacy controls. Model outputs are inferred classifications, not customer facts. State assumptions about language detection, sarcasm, negation, and representativeness. Report class counts alongside confidence and error rates; a growing topic can reflect a routing change rather than customer sentiment. Keep personal data out of exports unless an approved use case requires a controlled link.
## Checks
- The text unit and label definitions match the business question.
- Train, validation, and evaluation sets avoid duplicate or future-data leakage.
- Precision and recall are reported for decision-critical classes.
- Human reviewers inspect low-confidence and high-impact errors.
- Findings are sliced for channel or language bias where material.
## Failure Modes
- Calling keyword counts sentiment analysis without testing context or negation.
- Training on duplicate tickets that make accuracy appear unrealistically high.
- Treating a topic-model label as stable when different runs produce different clusters.
- Publishing customer text with identifiers in an executive dashboard.
- Automating a high-impact decision from a classifier whose rare negative class was never evaluated.
