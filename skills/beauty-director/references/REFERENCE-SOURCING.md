# Reference sourcing policy

## Selection order

1. Start with the most popular, recognizable representation of the style: its canonical movement, maker, work, artifact, or common application.
2. Verify the exact asset and any underlying work before selecting it. A freely licensed photograph does not clear copyrighted artwork, software, packaging, fashion photography, or other material visible inside it.
3. When the iconic example is redistributable, prefer it over an obscure but merely similar image.
4. When the iconic example is not redistributable, create or select a strong original representation that still shows the style's defining cues. Put `recognizable movement-level approximation` high in relevant generation direction and record the choice in the style evidence.
5. Reject NC, ND, fair-use, editorial-only, unclear, and generic web images.

Keep the research anchor and the bundled asset decision separate in `evidence.json`.

## Style evidence

Every style has `references/catalog/styles/<style-id>/evidence.json` following `references/EVIDENCE-SCHEMA.md`. It records:

- the iconic anchor and why it is canonical;
- real primary, institutional, or scholarly sources and the claims each supports;
- why the bundled references teach the style;
- cultural context and citations when required;
- evidence review and human visual-review state.

Do not use generic source labels or reconstructed citations as evidence.

## Required record

Every shipped crop has exactly one entry in `image-sources.json` with:

- style id;
- title, creator, and institution;
- exact source page and direct source-file URL;
- license and license URL;
- complete attribution text;
- crop or modification note;
- rights-check date;
- final local checksum;
- asset-level underlying-work, trademark, people/privacy/publicity, architecture/property, cultural-use, and intended-use conditions;
- asset reviewer, review date, full-size and card-scale result, and visual-fit state;
- for generated assets: model, exact prompt, generation date, and exact generation-record pointer.

The human-readable `ATTRIBUTION.md` is generated from the same information. The image's own license controls that image; the repository license does not replace it.
