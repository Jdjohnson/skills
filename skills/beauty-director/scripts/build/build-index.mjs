#!/usr/bin/env node
import { existsSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "../..");
const CATALOG = join(ROOT, "references/catalog");
const STYLES_DIR = join(CATALOG, "styles");
const INDEX_PATH = join(ROOT, "references/index.json");
const LEDGER_PATH = join(ROOT, "references/image-sources.json");

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function approvedStrong(image) {
  return image.assetReview?.status === "approved" && image.assetReview?.visualFit === "strong";
}

function buildIndex() {
  const families = readJson(join(CATALOG, "families.json")).families || [];
  const aliases = readJson(join(CATALOG, "aliases.json")).aliases || [];
  const ledger = readJson(LEDGER_PATH);
  const discovered = readdirSync(STYLES_DIR)
    .filter((id) => existsSync(join(STYLES_DIR, id, "style.json")))
    .sort();
  const ordered = [
    ...families.flatMap((family) => family.members || []),
    ...discovered.filter((id) => !families.some((family) => (family.members || []).includes(id))),
  ];
  if (discovered.length !== 120) {
    throw new Error(`expected exactly 120 styles, found ${discovered.length}`);
  }
  if (ordered.length !== 120 || new Set(ordered).size !== 120) {
    throw new Error(`family ordering must resolve exactly 120 unique styles, found ${new Set(ordered).size}`);
  }

  const aliasPhrases = new Map(ordered.map((id) => [id, []]));
  for (const alias of aliases) {
    for (const target of alias.targets || []) {
      if (target.kind === "style" && aliasPhrases.has(target.id)) {
        aliasPhrases.get(target.id).push(alias.phrase);
      }
    }
  }

  const approvedByStyle = new Map(ordered.map((id) => [id, []]));
  const approvedPaths = new Set();
  for (const image of ledger.images || []) {
    if (!approvedStrong(image)) continue;
    if (!approvedByStyle.has(image.styleId)) throw new Error(`approved ledger asset has unknown style ${image.styleId}`);
    if (approvedPaths.has(image.localPath)) throw new Error(`duplicate approved ledger path ${image.localPath}`);
    if (!image.localPath.startsWith(`assets/refs/${image.styleId}/`)) {
      throw new Error(`${image.localPath}: approved ledger path does not belong to ${image.styleId}`);
    }
    if (!existsSync(join(ROOT, image.localPath))) throw new Error(`${image.localPath}: approved ledger file is missing`);
    approvedPaths.add(image.localPath);
    approvedByStyle.get(image.styleId).push(image.localPath);
  }

  const styles = ordered.map((id) => {
    const style = readJson(join(STYLES_DIR, id, "style.json"));
    const evidence = readJson(join(STYLES_DIR, id, "evidence.json"));
    const review = evidence.humanVisualReview || {};
    if (review.status !== "approved" || review.fullSize !== true || review.cardScale !== true) {
      throw new Error(`${id}: evidence humanVisualReview is not approved at full size and card scale`);
    }
    const lead = review.leadImage;
    if (typeof lead !== "string" || !lead.startsWith(`assets/refs/${id}/`)) {
      throw new Error(`${id}: approved leadImage does not belong to the style`);
    }
    const approved = approvedByStyle.get(id) || [];
    if (!approved.includes(lead)) throw new Error(`${id}: approved leadImage is not an approved strong ledger asset`);
    if (approved.length < 1 || approved.length > 3) {
      throw new Error(`${id}: expected 1-3 approved strong ledger assets, found ${approved.length}`);
    }
    const referencePaths = [lead, ...approved.filter((path) => path !== lead).sort()];
    const palette = style.concerns?.palette || {};
    return {
      id,
      displayName: style.displayName,
      family: style.family,
      oneLiner: style.definition,
      cues: style.cues || [],
      antiCues: style.antiCues || [],
      aliasPhrases: [...new Set(aliasPhrases.get(id))],
      paletteHexes: palette.hexes || [],
      requiresCulturalReview: Boolean(style.requiresCulturalReview),
      referencePaths,
    };
  });

  if (styles.length !== 120) throw new Error(`expected exactly 120 index styles, found ${styles.length}`);
  return `${JSON.stringify({ version: 2, styles }, null, 2)}\n`;
}

let output;
try {
  output = buildIndex();
} catch (error) {
  console.error(`build-index: FAIL — ${error.message}`);
  process.exit(1);
}

if (process.argv.includes("--check")) {
  if (!existsSync(INDEX_PATH) || readFileSync(INDEX_PATH, "utf8") !== output) {
    console.error("build-index: STALE — run npm run build:index");
    process.exit(1);
  }
  console.log(`build-index: FRESH (${JSON.parse(output).styles.length} styles)`);
  process.exit(0);
}

writeFileSync(INDEX_PATH, output);
console.log(`build-index: WROTE references/index.json (${JSON.parse(output).styles.length} styles, ${Buffer.byteLength(output)} bytes)`);
