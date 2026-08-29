# Kano Model
## Purpose
Categorize product attributes by how their presence or absence changes customer satisfaction so investment matches must-be, performance, and delighter dynamics. It detects nonlinear reactions that a single importance score cannot reveal.
## Use
- Classifying features by how they drive satisfaction versus dissatisfaction
- Separating must-be, performance, and delighter attributes before roadmap trade-offs
- Explaining why incremental investment on some features yields little perceived gain
## Avoid
- You need a single numeric rank under capacity constraints—use feature-prioritization after Kano categories
- You need to translate customer needs into technical requirements matrices—use quality-function-deployment
- You lack any customer response data and only have internal opinions—gather via voice-of-the-customer or survey-design-methodology first
## Inputs
**Must-have:** Defined feature or attribute list to evaluate; customer responses to functional and dysfunctional (present/absent) questions; segment definition if satisfaction drivers differ by segment; current performance baseline on must-be attributes.

**Nice-to-have:** open-text explanation for each answer, competitive performance data, and a follow-up interview sample.

**When data is thin:** limit the attribute set and report counts by response pattern; never assign categories from internal enthusiasm alone.
## Procedure
1. **Frame attributes neutrally.** Break the offer into distinct, understandable attributes. Avoid bundled questions such as “fast and secure checkout,” which hide different satisfaction effects.
2. **Write paired questions.** For every attribute, ask how the respondent feels when it is present and how they feel when it is absent, using the same response scale for both conditions.
3. **Field by relevant segment.** Randomize question order, screen for actual users or buyers, and capture enough responses to inspect inconsistent patterns rather than only a total average.
4. **Classify paired responses.** Apply the evaluation table to label each respondent’s result as must-be, one-dimensional, attractive, indifferent, reverse, or questionable. Summarize the dominant category and the distribution.
5. **Translate categories into choices.** Repair poor must-be performance before adding delight. Set performance targets for one-dimensional attributes, treat attractive features as experiments, and send the resulting categories to feature prioritization for capacity decisions.
## Output Contract
Deliver an attribute classification table with paired-question wording, sample definition, response counts, category distribution, dominant category, segment differences, and recommended treatment. Flag questionable responses and attributes with a divided result. The output is a satisfaction typology, not a disguised rank-ordered roadmap.
## Evidence
Responses are observed opinions under a hypothetical presence or absence. The dominant classification is an inference and must show its denominator. Keep reverse answers visible; they may indicate a segment mismatch or a confusing feature. Do not assume today’s delighter remains novel next year, and record when data is too sparse to distinguish attractive from indifferent.
## Checks
- Every attribute has one unambiguous functional and dysfunctional pair.
- The sample represents the segment whose roadmap decision is being made.
- Category totals reconcile to usable responses and questionable answers are reported.
- A must-be recommendation considers current execution quality, not category alone.
## Failure Modes
- Asking respondents to rank features and calling the result a Kano classification.
- Combining two attributes so the paired answers cannot be interpreted.
- Treating an attractive feature as mandatory for every customer segment.
- Ignoring reverse responses that reveal a feature creates friction for some users.
