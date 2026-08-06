# Style evidence schema

Create `references/catalog/styles/<style-id>/evidence.json` for every style. Evidence is approved only after its claims and final visual set have been reviewed. Do not use generic source labels, reconstructed citations, or a mechanical test as a substitute for review.

```json
{
  "version": 1,
  "styleId": "style-id",
  "reviewState": "approved",
  "iconicAnchor": {
    "label": "Recognizable work, artifact, movement, or tradition",
    "creatorOrTradition": "Creator, institution, community, or tradition",
    "sourceUrl": "https://exact-authoritative-source.example/item",
    "whyCanonical": "Specific explanation of the visual grammar this anchor establishes."
  },
  "sources": [
    {
      "title": "Source title",
      "publisher": "Authoritative publisher or institution",
      "url": "https://exact-source.example/page",
      "accessedAt": "YYYY-MM-DD",
      "supports": [
        "Specific claim this source supports about the style."
      ]
    },
    {
      "title": "Second source title",
      "publisher": "Second authoritative publisher or institution",
      "url": "https://exact-source.example/second-page",
      "accessedAt": "YYYY-MM-DD",
      "supports": [
        "A second specific claim used by the style guidance or image review."
      ]
    }
  ],
  "bundledReferenceRationale": "Why the final one-to-three bundled images teach distinct aspects of this style and why the lead is unmistakable.",
  "culturalContext": null,
  "humanVisualReview": {
    "status": "approved",
    "reviewer": "Reviewer name",
    "reviewedAt": "YYYY-MM-DD",
    "fullSize": true,
    "cardScale": true,
    "leadImage": "assets/refs/style-id/reference-01.jpg",
    "notes": "Specific result of the visual review.",
    "reviewRecord": "references/provenance/final-visual-audit.json"
  }
}
```

For a style whose `style.json` has `requiresCulturalReview: true`, replace `culturalContext: null` with:

```json
{
  "culturalContext": {
    "note": "Grounded respectful-use direction specific to the living practice, tradition, and intended applications.",
    "citations": [
      "https://exact-authoritative-source.example/cultural-source-1",
      "https://exact-authoritative-source.example/cultural-source-2"
    ]
  }
}
```

`reviewState`, `humanVisualReview.status`, and all dates are lifecycle evidence. Keep them truthful: drafted, researched, reviewed, and approved are different states.

## Asset ledger additions

Every entry in `references/image-sources.json` also records:

```json
{
  "conditions": {
    "underlyingWork": "Reviewed condition or none known",
    "trademark": "Reviewed condition or none known",
    "peoplePrivacyPublicity": "Reviewed condition or none known",
    "architectureProperty": "Reviewed condition or none known",
    "culturalUse": "Reviewed condition or none known",
    "intendedUse": "Approved scope and any limitation"
  },
  "assetReview": {
    "status": "approved",
    "reviewer": "Reviewer name",
    "reviewedAt": "YYYY-MM-DD",
    "fullSize": true,
    "cardScale": true,
    "visualFit": "strong",
    "misleading": false,
    "distinctTeachingRole": "What this asset teaches that the lead or support set needs.",
    "notes": "Specific result of the full-size and card-scale review.",
    "reviewRecord": "references/provenance/final-visual-audit.json"
  }
}
```

Generated entries additionally require `model`, an exact `prompt`, `promptRecordStatus: "exact"`, `generatedAt`, and `generationRecord` pointing to the retained exact generation receipt.
