#!/usr/bin/env node
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "../..");
const CATALOG = join(ROOT, "references/catalog");
const STYLES_DIR = join(CATALOG, "styles");
const WORKSPACE = join(ROOT, "../../..");
const LEDGER_PATH = join(ROOT, "references/image-sources.json");
const indexPath = join(ROOT, "references/index.json");
const errors = [];
const DATE = /^\d{4}-\d{2}-\d{2}$/;
const HTTPS_URL = /^https:\/\//;

function present(value, minimum = 1) {
  return typeof value === "string" && value.trim().length >= minimum;
}

function uniqueStrings(values) {
  return Array.isArray(values) && values.every((value) => present(value)) && new Set(values).size === values.length;
}

function readJson(path) {
  try {
    return JSON.parse(readFileSync(path, "utf8"));
  } catch (error) {
    errors.push(`${path}: ${error.message}`);
    return {};
  }
}

function resolveReviewRecord(path) {
  if (!present(path)) return null;
  return path.startsWith("projects/") ? join(WORKSPACE, path) : join(ROOT, path);
}

function findNamedFiles(directory, target, found = []) {
  if (!existsSync(directory)) return found;
  for (const name of readdirSync(directory)) {
    const path = join(directory, name);
    if (statSync(path).isDirectory()) findNamedFiles(path, target, found);
    else if (name === target) found.push(path);
  }
  return found;
}

const styleIds = readdirSync(STYLES_DIR)
  .filter((id) => existsSync(join(STYLES_DIR, id, "style.json")))
  .sort();
const styleSet = new Set(styleIds);
const styles = new Map();
const ledger = readJson(LEDGER_PATH);
const approvedLedgerByPath = new Map(
  (ledger.images || [])
    .filter((image) => image.assetReview?.status === "approved" && image.assetReview?.visualFit === "strong")
    .map((image) => [image.localPath, image]),
);
const index = readJson(indexPath);
const indexById = new Map((index.styles || []).map((style) => [style.id, style]));

if (styleIds.length !== 120) errors.push(`catalog must contain exactly 120 styles; found ${styleIds.length}`);
for (const path of findNamedFiles(CATALOG, "sources.md")) {
  errors.push(`${path}: legacy sources.md is not allowed`);
}

for (const id of styleIds) {
  const directory = join(STYLES_DIR, id);
  for (const name of ["style.json", "STYLE.md", "evidence.json"]) {
    if (!existsSync(join(directory, name))) errors.push(`${id}: missing ${name}`);
  }
  const style = readJson(join(directory, "style.json"));
  styles.set(id, style);
  if (style.id !== id) errors.push(`${id}: style.json id is ${style.id}`);
  if (!style.displayName || !style.definition || !style.family) {
    errors.push(`${id}: missing displayName, definition, or family`);
  }
  if (!uniqueStrings(style.cues) || style.cues.length < 3) errors.push(`${id}: cues must contain at least 3 unique values`);
  if (!uniqueStrings(style.antiCues) || style.antiCues.length < 1) errors.push(`${id}: antiCues must contain unique values`);
  const cueAntiOverlap = (style.cues || []).filter((cue) => new Set(style.antiCues || []).has(cue));
  if (cueAntiOverlap.length) errors.push(`${id}: cues and antiCues overlap: ${[...new Set(cueAntiOverlap)].join(", ")}`);
  const palette = style.concerns?.palette;
  if (!palette || !uniqueStrings(palette.roles) || !uniqueStrings(palette.hexes) || palette.roles.length !== palette.hexes.length) {
    errors.push(`${id}: palette roles and hexes must be non-empty, unique, and aligned`);
  }

  const evidencePath = join(directory, "evidence.json");
  if (!existsSync(evidencePath)) continue;
  const evidence = readJson(evidencePath);
  if (evidence.version !== 1) errors.push(`${id}: evidence version must be 1`);
  if (evidence.styleId !== id) errors.push(`${id}: evidence styleId is ${evidence.styleId}`);
  if (evidence.reviewState !== "approved") errors.push(`${id}: evidence reviewState must be approved`);
  const anchor = evidence.iconicAnchor || {};
  if (!present(anchor.label) || !present(anchor.creatorOrTradition) || !HTTPS_URL.test(anchor.sourceUrl || "") || !present(anchor.whyCanonical, 40)) {
    errors.push(`${id}: iconicAnchor needs label, creatorOrTradition, HTTPS sourceUrl, and a specific rationale`);
  }
  if (!Array.isArray(evidence.sources) || evidence.sources.length < 2) {
    errors.push(`${id}: evidence needs at least 2 sources`);
  } else {
    const sourceUrls = new Set();
    for (const [index, source] of evidence.sources.entries()) {
      if (!present(source.title) || !present(source.publisher) || !HTTPS_URL.test(source.url || "") || !DATE.test(source.accessedAt || "")) {
        errors.push(`${id}: evidence source ${index + 1} needs title, publisher, HTTPS URL, and accessedAt date`);
      }
      if (!uniqueStrings(source.supports) || source.supports.some((claim) => claim.trim().length < 20)) {
        errors.push(`${id}: evidence source ${index + 1} needs specific supported claims`);
      }
      if (sourceUrls.has(source.url)) errors.push(`${id}: duplicate evidence source URL ${source.url}`);
      sourceUrls.add(source.url);
    }
  }
  if (!present(evidence.bundledReferenceRationale, 60)) {
    errors.push(`${id}: bundledReferenceRationale must explain the final teaching set`);
  }
  if (style.requiresCulturalReview) {
    if (!present(evidence.culturalContext?.note, 60) || !Array.isArray(evidence.culturalContext?.citations) || evidence.culturalContext.citations.length < 2) {
      errors.push(`${id}: culturally flagged style needs a specific cultural note and at least 2 citations`);
    }
  } else if (evidence.culturalContext !== null) {
    errors.push(`${id}: culturalContext must be null when cultural review is not required`);
  }
  const review = evidence.humanVisualReview || {};
  if (
    review.status !== "approved" ||
    !present(review.reviewer) ||
    !DATE.test(review.reviewedAt || "") ||
    review.fullSize !== true ||
    review.cardScale !== true ||
    !present(review.leadImage) ||
    !present(review.notes, 40) ||
    review.reviewRecord !== "references/provenance/final-visual-audit.json"
  ) {
    errors.push(`${id}: humanVisualReview must record the approved independent full-size and card-scale review, lead, notes, and review record`);
  } else {
    if (!review.leadImage.startsWith(`assets/refs/${id}/`)) errors.push(`${id}: humanVisualReview leadImage belongs to another style`);
    if (!existsSync(join(ROOT, review.leadImage))) errors.push(`${id}: humanVisualReview leadImage does not exist`);
    if (!existsSync(resolveReviewRecord(review.reviewRecord))) errors.push(`${id}: humanVisualReview reviewRecord does not exist`);
    const approvedLead = approvedLedgerByPath.get(review.leadImage);
    if (!approvedLead || approvedLead.styleId !== id) {
      errors.push(`${id}: humanVisualReview leadImage is not an approved strong ledger asset for this style`);
    }
    if (indexById.get(id)?.referencePaths?.[0] !== review.leadImage) {
      errors.push(`${id}: approved leadImage must be first in the fresh index`);
    }
  }
}

const families = readJson(join(CATALOG, "families.json")).families || [];
const familySet = new Set(families.map((family) => family.id));
const familyMembers = new Set();
const containingFamily = new Map();
if (families.length !== 12) errors.push(`catalog must contain exactly 12 families; found ${families.length}`);
if (familySet.size !== families.length) errors.push("family ids must be unique");
for (const family of families) {
  if (!present(family.id) || !present(family.name) || !present(family.definition)) {
    errors.push(`family ${family.id || "unknown"}: missing id, name, or definition`);
  }
  if (!Array.isArray(family.members) || family.members.length !== 10 || new Set(family.members).size !== 10) {
    errors.push(`family ${family.id || "unknown"}: must contain exactly 10 unique members`);
  }
  for (const id of family.members || []) {
    if (!styleSet.has(id)) errors.push(`family ${family.id}: unknown member ${id}`);
    if (familyMembers.has(id)) errors.push(`family membership duplicated: ${id}`);
    familyMembers.add(id);
    if (!containingFamily.has(id)) containingFamily.set(id, family.id);
  }
}
for (const [id, style] of styles) {
  if (!familySet.has(style.family)) errors.push(`${id}: unknown family ${style.family}`);
  if (!familyMembers.has(id)) errors.push(`${id}: absent from families.json`);
  if (containingFamily.has(id) && containingFamily.get(id) !== style.family) {
    errors.push(`${id}: style.family ${style.family} does not match containing family ${containingFamily.get(id)}`);
  }
}

const vocabularyRecords = readJson(join(CATALOG, "vocabulary.json")).tags || [];
const vocabulary = new Set();
for (const tag of vocabularyRecords) {
  if (vocabulary.has(tag.id)) errors.push(`vocabulary tag id duplicated: ${tag.id}`);
  vocabulary.add(tag.id);
}
for (const [id, style] of styles) {
  for (const cue of [...(style.cues || []), ...(style.antiCues || []), ...(style.emotionalEffects || [])]) {
    if (!vocabulary.has(cue)) errors.push(`${id}: unknown vocabulary tag ${cue}`);
  }
}

const aliases = readJson(join(CATALOG, "aliases.json")).aliases || [];
const aliasPhrases = new Set();
for (const alias of aliases) {
  if (!present(alias.phrase) || !present(alias.normalized) || alias.normalized !== alias.phrase.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim()) {
    errors.push(`alias ${alias.id || "unknown"}: invalid phrase or normalized value`);
  }
  if (aliasPhrases.has(alias.normalized)) errors.push(`alias normalized phrase duplicated: ${alias.normalized}`);
  aliasPhrases.add(alias.normalized);
  for (const target of alias.targets || []) {
    if (target.kind === "style" && !styleSet.has(target.id)) {
      errors.push(`alias ${alias.phrase}: unknown style ${target.id}`);
    }
  }
}

const modifierFiles = readdirSync(join(CATALOG, "modifiers"))
  .filter((name) => name.endsWith(".json"))
  .sort();
const modifierSet = new Set(modifierFiles.map((name) => name.slice(0, -5)));
for (const name of modifierFiles) {
  const modifier = readJson(join(CATALOG, "modifiers", name));
  if (modifier.id !== name.slice(0, -5)) errors.push(`${name}: id mismatch`);
  for (const id of modifier.incompatibleStyles || []) {
    if (!styleSet.has(id)) errors.push(`${modifier.id}: unknown incompatible style ${id}`);
  }
  for (const id of modifier.incompatibleFamilies || []) {
    if (!familySet.has(id)) errors.push(`${modifier.id}: unknown incompatible family ${id}`);
  }
  for (const id of modifier.incompatibleModifiers || []) {
    if (!modifierSet.has(id)) errors.push(`${modifier.id}: unknown incompatible modifier ${id}`);
  }
}

const adaptersDir = join(ROOT, "references/adapters");
const adapterIds = readdirSync(adaptersDir)
  .filter((id) => statSync(join(adaptersDir, id)).isDirectory())
  .sort();
for (const id of adapterIds) {
  for (const name of ["adapter.json", "ADAPTER.md"]) {
    if (!existsSync(join(adaptersDir, id, name))) errors.push(`adapter ${id}: missing ${name}`);
  }
  const adapterPath = join(adaptersDir, id, "adapter.json");
  if (existsSync(adapterPath) && readJson(adapterPath).id !== id) errors.push(`adapter ${id}: id mismatch`);
}

if (existsSync(indexPath) && statSync(indexPath).size >= 200 * 1024) {
  errors.push(`references/index.json is ${statSync(indexPath).size} bytes; must stay under 204800`);
}
const freshness = spawnSync(process.execPath, [join(ROOT, "scripts/build/build-index.mjs"), "--check"], {
  cwd: ROOT,
  encoding: "utf8",
});
if (freshness.status !== 0) {
  errors.push((freshness.stderr || freshness.stdout || "index freshness check failed").trim());
}

if (errors.length) {
  console.error(`validate-catalog: FAIL (${errors.length} error(s))`);
  for (const error of errors) console.error(`  - ${error}`);
  process.exit(1);
}

console.log("validate-catalog: OK");
console.log(`  styles: ${styleIds.length} (derived from references/catalog/styles/)`);
console.log(`  modifiers: ${modifierFiles.length}`);
console.log(`  adapters: ${adapterIds.length}`);
console.log(`  index: fresh, ${statSync(indexPath).size} bytes`);
