# Source Hierarchy and Provenance Policy

**Status:** Foundational draft v0.1

## Purpose

Prevent the Skill from confusing what Deutsch stated with what he originated, endorsed, inherited, criticized, co-developed, inspired, or would allegedly apply to a new problem.

```text
assertion ≠ origin ≠ endorsement ≠ influence ≠ derivation ≠ application
```

A source can establish that Deutsch advanced a claim. It does not establish that the claim is true, original to him, accepted by a field, or applicable elsewhere.

## Governing rules

1. **Authority is claim-relative.** Books are often strongest for integrated worldview claims; formal papers for technical claims; explicit corrections for their corrected scope; recordings for what was audibly said.
2. **Claims and relationships need separate evidence.** Evidence for A and B does not prove that Deutsch connected A to B.
3. **Chronology is part of meaning.** Preserve precursors, mature formulations, later extensions, corrections, and abandoned positions.
4. **Missing evidence means unknown.** Search failure does not prove acceptance, rejection, silence, or change of mind.
5. **Synthesis and application are permitted only when owned by the Skill.** They are not Deutsch claims.
6. **“Deutsch” identifies the assertor, not necessarily the originator.** Historical priority requires separate evidence.

## Source tiers

| Tier | Source | Permitted use | Main limit |
|---|---|---|---|
| P1-C | Explicit correction, erratum, retraction, or revision issued by Deutsch | How an identified earlier claim should be qualified | Controls only its stated scope |
| P1-S | Sole-authored book, paper, formal essay, or chapter | Developed Deutsch claims and sustained arguments | Preserve domain, date, version, and posture |
| P1-J | Coauthored paper, chapter, or statement | Joint claims | Never convert silently to sole authorship |
| P2 | Authenticated recording of lecture, interview, podcast, or Q&A | What Deutsch said in that setting | Prompting, editing, spontaneity, and context matter |
| P3 | Authenticated blog, comment, social post, or informal first-person writing | Dated statement or clarification | Normally insufficient alone for continuing doctrine |
| D1 | Transcript, translation, publisher record, archive, bibliography, or index | Locating and checking evidence | Hosting does not transfer authorship or approval |
| S1 | Scholarship, criticism, biography, intellectual history, or review | The secondary author's analysis | Cannot establish a Deutsch claim without primary confirmation |
| C1 | Fan summary, reading notes, community wiki, quote collection, unofficial transcript | Discovery lead | Cannot enter the verified graph directly |
| U0 | Unattributed quote, ambiguous speaker, inaccessible citation, snippet, unsupported AI assertion | Quarantine | Never present as a Deutsch claim |

Tier does not replace judgment about authenticity, authorial control, deliberateness, completeness, domain fit, locator precision, and directness of support.

## Primary-source contexts

### Books

Record title, publisher, territory, year, edition, printing, format, ISBN, chapter, section, edition-specific page, errata, and translator.

Jacket copy, publisher descriptions, indexes, reviews, and promotional text are not automatically Deutsch's words.

### Papers and preprints

Record every author, paper status, journal and DOI, submission/revision/acceptance/publication dates, preprint identifier and exact version, passage location, and the source's epistemic language.

A preprint and journal article are separate manifestations of one work. Never flatten “proposes,” “suggests,” “conjectures,” or “explores” into “proves” or “establishes.”

### Essays and articles

Separate the signed body from editor-supplied title, subtitle, abstract, pull quote, caption, and social preview.

### Talks and lectures

Record event, venue, delivery date, upload date, prepared section versus Q&A, recording, transcript producer, approval status, and timestamp.

### Interviews and podcasts

Record interviewer, full immediate prompt, recording and release dates, editing status, response timestamp, and whether the response is tentative, hypothetical, humorous, or qualified.

Host summaries, episode descriptions, and chapter labels are not Deutsch claims.

### Transcripts

Classify as:

- `author_issued`
- `author_approved`
- `publisher_produced`
- `professional_unverified`
- `community_produced`
- `machine_generated`
- `unknown`

Author hosting or linking does not automatically imply approval. Machine transcripts are discovery tools until checked against audio.

### Social material

Record authenticated account, canonical ID, full thread/reply context, publication and modification dates, deletion status, and archival provenance.

One post can support “Deutsch wrote X at time T.” It rarely supports “Deutsch's worldview holds X” by itself.

### Translations

Treat each translation as a separate manifestation. Record original work, translator, language, edition, approval status, and original locator. The original controls exact wording when accessible.

## Work and manifestation model

Use separate identifiers:

- `work_id` — the underlying intellectual work.
- `manifestation_id` — an edition, version, translation, recording, transcript, or archive.

Keep composition/delivery, first publication, version publication, upload, modification, correction, and access dates distinct.

Upload date is not delivery date. Reprint date is not first publication. A later statement does not supersede an earlier one merely because it is later.

## Chronology relationships

- `anticipates`
- `precursor_to`
- `develops`
- `clarifies`
- `narrows`
- `extends`
- `corrects`
- `reaffirms`
- `abandons`
- `retracts`
- `supersedes`
- `apparently_conflicts_with`
- `contradicts`
- `translation_of`
- `transcript_of`
- `retrospective_attribution`

Before recording contradiction, normalize propositions, verify stable definitions, domain, scope, modality, speaker, edition, version, and any explicit correction. Use `apparently_conflicts_with` when unresolved.

## Claim-level provenance axes

Every claim independently records:

1. Assertor.
2. Authorship context: sole, joint, interview, reported speech, or secondary attribution.
3. Origin attribution and its basis.
4. Stance: asserts, endorses, provisionally accepts, reports, credits, criticizes, rejects, or remains undecided.
5. Provenance mode: quote, paraphrase, synthesis, inference, or application.
6. Epistemic status: definition, argument, conjecture, proposal, speculation, criticism, recollection, or conclusion within the source.
7. Scope and domain.
8. Chronology and later qualifications.
9. Independent confidence dimensions.

## Attribution classes

- `deutsch_explicit`
- `deutsch_joint`
- `deutsch_endorsed`
- `deutsch_extended`
- `deutsch_criticizes`
- `deutsch_time_bounded`
- `shared`
- `adjacent`
- `critic_attribution`
- `skill_synthesis`
- `skill_inference`
- `skill_application`
- `unverified_attribution`

## Evidence thresholds

### “Deutsch said or wrote X in source S”

One authenticated direct passage with precise locator.

### “Deutsch argues X”

One sustained sole-authored primary treatment, or multiple consistent primary passages including one deliberate source.

### “X is part of Deutsch's continuing worldview”

A sustained formal treatment, substantial primary corroboration or later reaffirmation, no known material correction, and evidence connecting it to the wider worldview.

### “Deutsch connects X to Y”

A direct relational passage, a demonstrated argument, or an explicitly labeled Skill synthesis with the bridge shown.

### “Deutsch originated X”

Historical-priority research. Deutsch's own account supports self-attribution, not decisive priority proof. Prefer narrower verbs such as “formulated,” “developed,” “extended,” or “described as original by Deutsch.”

### Cross-domain use

Always `skill_application`, with structural correspondence, independent target warrant, limits, and failure conditions.

## Intellectual-lineage relationships

Keep these distinct:

- `credits_to`
- `endorses`
- `criticizes`
- `rejects`
- `qualifies`
- `extends`
- `reformulates`
- `co_develops`
- `reported_intellectual_source`
- `historically_influenced`
- `logically_entails`
- `motivates`
- `publicly_argues_for`
- `our_synthesis_connects`

For example, an autobiographical statement that one idea influenced another supports `reported_intellectual_source`; it does not automatically support `logically_entails`.

## Adjacent thinkers

For Popper, Everett, Turing, Church, Dawkins, Marletto, and others, preserve separate records for:

- their claims;
- Deutsch's attribution to them;
- Deutsch's endorsement, criticism, reformulation, or extension;
- historical-priority evidence;
- coauthored work;
- and Skill synthesis.

Author order does not establish intellectual ownership. Later joint work does not make earlier sole-authored work joint, or vice versa.

## Secondary sources and criticism

Use secondary work to discover primary sources, identify predecessors, surface contradictions, present alternate interpretations, investigate priority, and criticize synthesis.

Every criticism record identifies the critic, target, objection, source, locator, cited evidence, any response, and adjudication status. Never write “critics say” without a critic and source.

## Inaccessible and absent evidence

For inaccessible, paywalled, dead, ambiguous, disputed, or absent evidence:

- Record metadata, access attempt, date, failure type, and alternate locations searched.
- Do not infer from title, snippet, chapter label, citation, or secondary quotation.
- Preserve transcript variants and check the recording when available.
- Quarantine ambiguous attribution.
- Record no-findings as `unknown`, including source classes and terms searched.
- Treat link failure as a revalidation trigger, not deletion or negative evidence.

## Confidence

Never collapse confidence to one number. Record:

- `source_identity`: verified / probable / uncertain / failed
- `text_fidelity`: verified / high / medium / low / unknown
- `support_strength`: direct / strong / partial / weak / none
- `interpretive_confidence`: high / medium / low
- `origin_confidence`: high / medium / low / unresolved
- `verification_state`: candidate / verified / disputed / superseded / rejected

Overall confidence equals the weakest material component. It is not a measure of whether the underlying theory is true.

## Quote and copyright discipline

- Use normalized paraphrases as the working layer.
- Store only the shortest excerpt needed to verify wording; default to no more than 25 words per source record.
- Keep a precise locator so context can be reopened.
- Do not assemble excerpts that reconstruct a work.
- Do not store full copyrighted books, articles, or transcripts inside the Skill.
- Distinguish verbatim, cleaned transcript, translation, and paraphrase.
- Verify wording before quoting and do not quote machine transcripts as exact without audio check.

The 25-word default is an operational limit, not a legal safe harbor.

## Minimal source record

```json
{
  "source_id": "src-dd-...",
  "work_id": "work-dd-...",
  "manifestation_id": "man-dd-...",
  "title": "",
  "source_tier": "P1-S",
  "source_type": "book",
  "contributors": [],
  "language": "en",
  "publication_context": {},
  "dates": {},
  "version": {},
  "identifiers": {},
  "locations": {},
  "integrity": {},
  "authority": {},
  "rights": {
    "storage_mode": "metadata_only"
  },
  "audit": {
    "record_status": "candidate",
    "policy_version": "0.1"
  }
}
```

## Verification and release gates

Every new source begins as `candidate`. Verification reopens the source and checks speaker/author, locator, context, qualifications, posture, coauthorship, and known corrections.

Foundational claims and relationship edges require a second review pass.

A corpus release fails if it contains:

- A verified Deutsch claim without primary evidence.
- A joint claim presented as sole-authored.
- Synthesis or application presented as explicit.
- A quotation without a verified locator.
- A known correction omitted from an affected claim.
- An apparent contradiction silently harmonized.
- An inaccessible source treated as negative evidence.
- An application presented as “Deutsch would say.”

Corrections create new versions and explicit edges. Historical records remain recoverable.

## Runtime behavior

The expensive provenance work happens during corpus compilation. Runtime uses verified argument packets and expands provenance when attribution is weak, disputed, cross-domain, consequential, or explicitly requested.

The runtime may not create a new `deutsch_explicit` or `deutsch_endorsed` record from model memory. Novel connections default to `skill_synthesis` or `skill_inference`; cross-domain recommendations default to `skill_application`.

Direct invocation of a named concept does not bypass provenance.
