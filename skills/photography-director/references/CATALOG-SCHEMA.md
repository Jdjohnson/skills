# Photography Director catalog schema

Use these records as the rich source of truth. `references/router.jsonl` and `references/axis-router.jsonl` are generated browsing data, never the authoring surface.

## Claim basis

Every claim uses one of:

- `observed`: a visible effect;
- `confirmed`: exact metadata or authoritative equipment record;
- `documented`: a reliable source explicitly states it;
- `inferred`: plausible but unproven.

An exact camera, lens, focal length, aperture, shutter, ISO, film stock, process, modifier, or lighting-hardware claim must be `confirmed` or `documented`. Store inferred mechanisms only with qualified language.

Reference linkage means that a photograph teaches a value's visible appearance or context. It does not, by itself, confirm that the photograph used the named camera, lens, format, process, or lighting setup. For a value whose policy is `confirmed-or-documented`, the runtime must find a matching technical claim or explicit source statement before presenting the mechanism as fact; otherwise it must describe only the appearance or effect.

## Axis file

Each `references/catalog/axes/<axis-id>.json` contains:

```json
{
  "version": 1,
  "id": "focus-depth",
  "displayName": "Focus and depth",
  "definition": "What this axis controls.",
  "values": [
    {
      "id": "shallow-focus",
      "displayName": "Shallow focus",
      "definition": "Visible definition.",
      "aliases": ["blurred background"],
      "visibleCues": ["narrow plane of sharp focus"],
      "antiCues": ["front-to-back sharpness"],
      "claimPolicy": "observed",
      "applicability": ["portrait", "product"],
      "incompatibilities": [],
      "referenceIds": ["ref-id"]
    }
  ]
}
```

IDs are lowercase hyphen-case and globally unique within their record kind. Arrays contain unique, non-empty values. A value must have at least one reference; add a contrast/support reference when adjacent terms are easily confused.

## Canonical look file

Each `references/catalog/looks/<look-id>.json` contains:

```json
{
  "version": 1,
  "id": "window-light-editorial-portrait",
  "displayName": "Window-Light Editorial Portrait",
  "family": "portrait-editorial",
  "definition": "One visible sentence.",
  "aliases": ["soft editorial portrait"],
  "cues": ["soft-side-light", "shallow-focus", "restrained-color"],
  "antiCues": ["hard-direct-flash", "clinical-retouching"],
  "axisValues": {
    "genre-use": ["editorial", "portrait"],
    "lighting": ["window-light", "soft-side-light"]
  },
  "lockedQualities": ["soft directional light"],
  "adaptiveGuidance": ["choose framing and lens class for the subject"],
  "applicability": ["people", "small groups"],
  "incompatibilities": [],
  "referenceIds": ["lead-reference-id"],
  "evidence": {
    "sources": [
      {
        "title": "Authoritative source",
        "publisher": "Publisher",
        "url": "https://example.com",
        "accessedAt": "YYYY-MM-DD",
        "supports": ["Specific catalog claim"]
      }
    ]
  }
}
```

Every look needs one unmistakable real-photography lead. Add at most two support references, each with a distinct teaching role. User-facing look names describe a transferable photographic tradition or treatment, not a living photographer.

## Source ledger

`references/source-ledger.json` contains `version` and `references`. Each reference records:

```json
{
  "id": "reference-id",
  "sourceKind": "wikimedia-commons",
  "displayMode": "bundled",
  "originType": "real-photograph",
  "title": "Source title",
  "creator": "Photographer or institution",
  "sourcePage": "https://exact-source-page.example",
  "assetUrl": "https://exact-file-or-approved-display-url.example",
  "localPath": "assets/references/reference-id.jpg",
  "license": "Public domain",
  "licenseUrl": "https://license.example",
  "attributionText": "Required credit, or empty when none is required.",
  "accessedAt": "YYYY-MM-DD",
  "modification": "Proportionally resized; no crop.",
  "sha256": "64 lowercase hex characters for local assets",
  "realPhotographyStatus": "verified",
  "technicalClaims": [
    {
      "field": "focalLength",
      "value": "85 mm",
      "basis": "confirmed",
      "source": "embedded EXIF"
    }
  ],
  "visualTags": ["shallow-focus", "soft-side-light"],
  "review": {
    "status": "approved",
    "reviewedAt": "YYYY-MM-DD",
    "fullSize": true,
    "conversationScale": true,
    "visualFit": "strong",
    "teachingRole": "What this image visibly demonstrates.",
    "notes": "Specific visual review result."
  }
}
```

Allowed `displayMode` values:

- `bundled`: approved local asset;
- `authorized-remote`: source-approved remote display;
- `research-only`: never a candidate;
- `generated-gap`: clearly labeled synthetic combination study.

`originType` is `real-photograph` or `generated`. A reference cannot be both. `research-only` references do not satisfy visible catalog coverage.

In public distributions, Pexels references must be `authorized-remote`. Keep their source metadata, but do not bundle the image files.

## Coverage file

`references/catalog/coverage.json` freezes:

- every required axis ID;
- every required value ID per axis;
- every canonical look ID;
- the reference IDs that teach each item;
- review state for each item;
- explicit rationale for any planned term intentionally excluded.

Completion requires zero missing required values, zero unknown IDs, zero duplicate IDs, and zero visible nodes without approved display references.

## Generated routers

`references/router.jsonl` contains one bounded-searchable line per canonical look: identity, family, definition, aliases, visible cues, anti-cues, applicability, axis-value IDs, and approved display records.

`references/axis-router.jsonl` contains one bounded-searchable line per axis value: identity, definitions, aliases, visible cues, anti-cues, claim policy, applicability, and up to three approved teaching references. Rich authoring records may retain more supporting references.

Run `npm run build:router` after editing the catalog. Do not store scores, neighbors, session state, exact source ledgers, long evidence, or duplicated source prose in either router.
