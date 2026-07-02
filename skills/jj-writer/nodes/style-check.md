---
description: |
  Voice drift scan and final style gate for content written as or for Jarad.
---

# Style Check

Run on near-final content before Humanizer. Load [jarad-style-guide](jarad-style-guide.md) and [voice-dna](voice-dna.md) first; for email, also load [email-voice-profile](email-voice-profile.md).

## Rule IDs

Use these IDs in audits and fixes. "Sounds off" is not enough.

### Core Voice

- **SG-01 Practitioner voice**: operator sharing what worked or failed, not a lecturer
- **SG-02 Controlled informality**: casual delivery, exact thinking underneath
- **SG-03 Direct opinion**: state position early in short-form; do not hide in hedges
- **SG-04 Honest uncertainty**: acknowledge limits without hedge stacking
- **SG-05 Specificity**: names, numbers, timestamps, concrete examples over abstractions

### Structure

- **SG-06 Sentence length**: short to medium; split long thoughts
- **SG-07 Paragraph length**: usually 2–4 sentences, rarely above 5
- **SG-08 Minimal transitions**: avoid "Furthermore", "Additionally", "Moreover"
- **SG-09 Prose-first**: avoid bullet-heavy article prose unless format demands it
- **SG-10 Long-form thesis timing**: build to thesis; do not front-load in long-form

### Language Hygiene

- **SG-11 Contractions always**
- **SG-12 No corporate/LinkedIn jargon**: no hype or consultant language
- **SG-13 No em dash dependence**: prefer clean sentence breaks
- **SG-14 No false contrast templates**: no "it's not X, it's Y" scaffolding
- **SG-15 No presumptuous reader framing**: no "what people don't realize..."

### Tone and Craft

- **SG-16 Emotional honesty, flat delivery**: name feelings plainly without intensifiers
- **SG-17 Metaphor discipline**: one metaphor at a time; retire before switching
- **SG-18 No performative voice**: no fake inspiration, manufactured tension, brand-speak
- **SG-19 No hollow writing**: every praise or reasoning sentence must point to a specific fact; if missing, ask or cut
- **SG-20 Email voice**: short operational paragraphs, concrete warmth, direct asks, calm follow-ups, simple closings

## Red-Flag Scan

Severity:

- **Critical**: breaks voice identity or meaning (brand/corporate tone, heavy AI phrasing, thesis distortion)
- **High**: strong drift likely to read "not Jarad" (jargon clusters, padded structure)
- **Medium**: recoverable in edit (long paragraphs, weak specificity, stacked metaphors)
- **Low**: polish-level

Flag SG-11–SG-15 violations, SG-06/SG-07 pacing drift, SG-01/SG-02/SG-18 voice mismatch, SG-10 long-form structure failure, SG-16 emotional inflation, SG-17 metaphor overload.

Output format when auditing:

```markdown
## Red Flags

| Severity | Rule | Problem | Evidence | Fix Direction |
|---|---|---|---|---|
| High | SG-12 | Corporate phrase cluster | "..." | Replace with direct operator language |

### Priority Fix Order
1. [Critical/High issue]
2. ...
```

Quote only the smallest span needed to prove the issue.

## Final Checklist Verdict

Score each category **Pass**, **Needs Work**, or **Fail**:

1. **Voice and stance** (SG-01, SG-03, SG-04, SG-18)
2. **Structure and flow** (SG-06, SG-07, SG-08, SG-10 when applicable)
3. **Language hygiene** (SG-11–SG-15)
4. **Craft quality** (SG-05, SG-16, SG-17)

Verdict rules:

- Any **Fail** in Voice and stance → **REVISE**
- Two or more **Fail** in any category → **REVISE**
- No Fails but **Needs Work** in high-leverage areas → **REVISE (light)**
- All Pass → **PASS**

```markdown
## Style Checklist Verdict
- **Verdict:** [PASS | REVISE | REVISE (light)]
- **Top Blockers:** [if any]

### Category Results
- Voice and stance: [...]
- Structure and flow: [...]
- Language hygiene: [...]
- Craft quality: [...]

### Final Notes
- [What to fix next or why it's publish-ready]
```

## Priority When Rules Conflict

1. Meaning fidelity (do not change the claim unintentionally)
2. Voice authenticity
3. Structural clarity
4. Compression
