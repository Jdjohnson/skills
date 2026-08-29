#!/usr/bin/env node
import { createHash } from "node:crypto";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { basename, dirname, extname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "../..");
const CATALOG = join(ROOT, "references/catalog");
const STYLES = join(CATALOG, "styles");
const WORKSPACE = resolve(ROOT, "../../..");
const INDEX = join(ROOT, "references/index.json");
const LEDGER = join(ROOT, "references/image-sources.json");
const ATTRIBUTION = join(ROOT, "ATTRIBUTION.md");
const REFS = join(ROOT, "assets/refs");
const errors = [];
const DATE = /^\d{4}-\d{2}-\d{2}$/;
const SHA256 = /^[a-f0-9]{64}$/;
const HTTPS = /^https:\/\//;
const IMAGE_EXTENSIONS = new Set([".jpg", ".jpeg", ".png", ".webp"]);
const placeholders = /\b(?:placeholder|unsourced|tbd|todo)\b|canonical design-history references|comparative formal analysis/i;

const fail = (message) => errors.push(message);
const present = (value, minimum = 1) => typeof value === "string" && value.trim().length >= minimum;
const unique = (values) => Array.isArray(values) && values.every((value) => present(value)) && new Set(values).size === values.length;
const digest = (value) => createHash("sha256").update(value).digest("hex");
const posix = (path) => path.split(sep).join("/");

function json(path) {
  try {
    return JSON.parse(readFileSync(path, "utf8"));
  } catch (error) {
    fail(`${path}: ${error.message}`);
    return {};
  }
}

function namedFiles(directory, target, found = []) {
  if (!existsSync(directory)) return found;
  for (const name of readdirSync(directory)) {
    const path = join(directory, name);
    if (statSync(path).isDirectory()) namedFiles(path, target, found);
    else if (name === target) found.push(path);
  }
  return found;
}

function jsonFiles(directory, found = []) {
  if (!existsSync(directory)) return found;
  for (const name of readdirSync(directory)) {
    const path = join(directory, name);
    if (statSync(path).isDirectory()) jsonFiles(path, found);
    else if (name.endsWith(".json")) found.push(path);
  }
  return found;
}

function resolveRecord(path) {
  if (!present(path)) return null;
  if (isAbsolute(path)) return path;
  return path.startsWith("projects/") ? join(WORKSPACE, path) : join(ROOT, path);
}

function imageDimensions(bytes, extension) {
  if (extension === ".png" && bytes.length >= 24) return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) };
  if (extension === ".webp") {
    const chunk = bytes.subarray(12, 16).toString("ascii");
    if (chunk === "VP8X" && bytes.length >= 30) return { width: 1 + bytes[24] + (bytes[25] << 8) + (bytes[26] << 16), height: 1 + bytes[27] + (bytes[28] << 8) + (bytes[29] << 16) };
    if (chunk === "VP8L" && bytes.length >= 25 && bytes[20] === 0x2f) return { width: 1 + bytes[21] + ((bytes[22] & 0x3f) << 8), height: 1 + (bytes[22] >> 6) + (bytes[23] << 2) + ((bytes[24] & 0x0f) << 10) };
    if (chunk === "VP8 " && bytes.length >= 30 && bytes[23] === 0x9d && bytes[24] === 0x01 && bytes[25] === 0x2a) return { width: bytes.readUInt16LE(26) & 0x3fff, height: bytes.readUInt16LE(28) & 0x3fff };
    return null;
  }
  if (![".jpg", ".jpeg"].includes(extension)) return null;
  const frame = new Set([0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf]);
  let offset = 2;
  while (offset + 8 < bytes.length) {
    if (bytes[offset] !== 0xff) {
      offset += 1;
      continue;
    }
    while (bytes[offset] === 0xff) offset += 1;
    const marker = bytes[offset++];
    if (marker === 0xd8 || marker === 0xd9 || marker === 0x01) continue;
    if (offset + 2 > bytes.length) break;
    const length = bytes.readUInt16BE(offset);
    if (length < 2 || offset + length > bytes.length) break;
    if (frame.has(marker) && length >= 7) return { width: bytes.readUInt16BE(offset + 5), height: bytes.readUInt16BE(offset + 3) };
    offset += length;
  }
  return null;
}

function expectedAttribution(ledger) {
  const lines = [
    "# Reference Image Attribution",
    "",
    "Every bundled reference is delivered at 800x1000 pixels. Each asset's own attribution and modification note states whether its source was cropped, padded, or proportionally resized. Public-source records preserve their license and file-page evidence; generated records are MIT licensed and preserve their generator, date, prompt, and modification note.",
    "",
  ];
  for (const record of ledger.images || []) {
    lines.push(`## ${record.styleId} — ${basename(record.localPath)}`, "", `Local file: ${record.localPath}`, "", record.attributionText, "");
    if (record.rightsNote) lines.push(`Rights/fit note: ${record.rightsNote}`, "");
    if (record.conditions) {
      lines.push(
        `Intended-use condition: ${record.conditions.intendedUse}`,
        `Underlying-use conditions: ${[
          record.conditions.underlyingWork,
          record.conditions.trademark,
          record.conditions.peoplePrivacyPublicity,
          record.conditions.architectureProperty,
          record.conditions.culturalUse,
        ].join("; ")}`,
        "",
      );
    }
    if (record.originType === "generated" && record.generationRecord) lines.push(`Generation record: ${record.generationRecord}`, "");
  }
  return `${lines.join("\n")}\n`;
}

const styleIds = readdirSync(STYLES).filter((id) => existsSync(join(STYLES, id, "style.json"))).sort();
const styleSet = new Set(styleIds);
const styles = new Map();
let ledgerBytes = Buffer.alloc(0);
let ledger = {};
try {
  ledgerBytes = readFileSync(LEDGER);
  ledger = JSON.parse(ledgerBytes.toString("utf8"));
} catch (error) {
  fail(`${LEDGER}: ${error.message}`);
}
if (ledger.generatedMediaLicense !== "MIT" || ledger.generatedMediaLicenseFile !== "LICENSE") fail("generated media license must point to the repository MIT license");
const paths = new Set();
const sourcePages = new Set();
const counts = new Map();
const publicImages = [];
const actualReferenceFiles = [];

if (!existsSync(join(ROOT, "agents/openai.yaml"))) fail("agents/openai.yaml must exist");

for (const id of styleIds) {
  const directory = join(STYLES, id);
  for (const name of ["style.json", "STYLE.md", "evidence.json"]) if (!existsSync(join(directory, name))) fail(`${id}: missing ${name}`);
  const style = json(join(directory, "style.json"));
  const prosePath = join(directory, "STYLE.md");
  const evidencePath = join(directory, "evidence.json");
  const prose = existsSync(prosePath) ? readFileSync(prosePath, "utf8") : "";
  const evidenceText = existsSync(evidencePath) ? readFileSync(evidencePath, "utf8") : "";
  const evidence = evidenceText ? json(evidencePath) : {};
  styles.set(id, { style, prose, evidence, evidenceText });

  if (style.id !== id) fail(`${id}: style.json id is ${style.id}`);
  if (!style.displayName || !style.definition || !style.family) fail(`${id}: missing displayName, definition, or family`);
  if (!unique(style.cues) || style.cues.length < 3) fail(`${id}: cues must contain at least 3 unique values`);
  if (!unique(style.antiCues) || style.antiCues.length < 1) fail(`${id}: antiCues must contain unique values`);
  const overlap = (style.cues || []).filter((cue) => new Set(style.antiCues || []).has(cue));
  if (overlap.length) fail(`${id}: cues and antiCues overlap: ${[...new Set(overlap)].join(", ")}`);
  const palette = style.concerns?.palette;
  if (!palette || !unique(palette.roles) || !unique(palette.hexes) || palette.roles.length !== palette.hexes.length) fail(`${id}: palette roles and hexes must be non-empty, unique, and aligned`);

  if (evidence.version !== 1) fail(`${id}: evidence version must be 1`);
  if (evidence.styleId !== id) fail(`${id}: evidence styleId is ${evidence.styleId}`);
  if (evidence.reviewState !== "approved") fail(`${id}: evidence reviewState must be approved`);
  const anchor = evidence.iconicAnchor || {};
  if (!present(anchor.label) || !present(anchor.creatorOrTradition) || !HTTPS.test(anchor.sourceUrl || "") || !present(anchor.whyCanonical, 40)) fail(`${id}: iconicAnchor needs label, creatorOrTradition, HTTPS sourceUrl, and a specific rationale`);
  if (!Array.isArray(evidence.sources) || evidence.sources.length < 2) fail(`${id}: evidence needs at least 2 sources`);
  else {
    const sourceUrls = new Set();
    for (const [index, source] of evidence.sources.entries()) {
      if (!present(source.title) || !present(source.publisher) || !HTTPS.test(source.url || "") || !DATE.test(source.accessedAt || "")) fail(`${id}: evidence source ${index + 1} needs title, publisher, HTTPS URL, and accessedAt date`);
      if (!unique(source.supports) || source.supports.some((claim) => claim.trim().length < 20)) fail(`${id}: evidence source ${index + 1} needs specific supported claims`);
      if (sourceUrls.has(source.url)) fail(`${id}: duplicate evidence source URL ${source.url}`);
      sourceUrls.add(source.url);
    }
  }
  if (!present(evidence.bundledReferenceRationale, 60)) fail(`${id}: bundledReferenceRationale must explain the final teaching set`);
  if (style.requiresCulturalReview) {
    if (!present(evidence.culturalContext?.note, 60) || !Array.isArray(evidence.culturalContext?.citations) || evidence.culturalContext.citations.length < 2) fail(`${id}: culturally flagged style needs a specific cultural note and at least 2 citations`);
  } else if (evidence.culturalContext !== null) fail(`${id}: culturalContext must be null when cultural review is not required`);

  const review = evidence.humanVisualReview || {};
  if (!present(review.reviewer) || !DATE.test(review.reviewedAt || "") || !present(review.notes, 40) || !present(review.reviewRecord)) {
    fail(`${id}: humanVisualReview must record the approved independent full-size and card-scale review, lead, notes, and review record`);
  } else {
    if (!existsSync(resolveRecord(review.reviewRecord))) fail(`${id}: humanVisualReview reviewRecord does not exist`);
  }

  if (!palette?.hexes?.length || palette.hexes.some((color) => !/^#[0-9a-f]{6}$/i.test(color))) fail(`${id}: invalid palette hexes`);
  if (!evidenceText || placeholders.test(evidenceText)) fail(`${id}: placeholder or generic evidence text`);
}

const families = json(join(CATALOG, "families.json")).families || [];
const familySet = new Set(families.map((family) => family.id));
const familyMembers = new Set();
const containingFamily = new Map();
if (familySet.size !== families.length) fail("family ids must be unique");
for (const family of families) {
  if (!present(family.id) || !present(family.name) || !present(family.definition)) fail(`family ${family.id || "unknown"}: missing id, name, or definition`);
  if (!Array.isArray(family.members) || !family.members.length || new Set(family.members).size !== family.members.length) fail(`family ${family.id || "unknown"}: must contain unique members`);
  for (const id of family.members || []) {
    if (!styleSet.has(id)) fail(`family ${family.id}: unknown member ${id}`);
    if (familyMembers.has(id)) fail(`family membership duplicated: ${id}`);
    familyMembers.add(id);
    if (!containingFamily.has(id)) containingFamily.set(id, family.id);
  }
}
for (const [id, { style }] of styles) {
  if (!familySet.has(style.family)) fail(`${id}: unknown family ${style.family}`);
  if (!familyMembers.has(id)) fail(`${id}: absent from families.json`);
  if (containingFamily.get(id) && containingFamily.get(id) !== style.family) fail(`${id}: style.family ${style.family} does not match containing family ${containingFamily.get(id)}`);
}

const vocabulary = new Set();
for (const tag of json(join(CATALOG, "vocabulary.json")).tags || []) {
  if (vocabulary.has(tag.id)) fail(`vocabulary tag id duplicated: ${tag.id}`);
  vocabulary.add(tag.id);
}
for (const [id, { style }] of styles) for (const cue of [...(style.cues || []), ...(style.antiCues || []), ...(style.emotionalEffects || [])]) if (!vocabulary.has(cue)) fail(`${id}: unknown vocabulary tag ${cue}`);

const aliases = json(join(CATALOG, "aliases.json")).aliases || [];
const aliasPhrases = new Set();
for (const alias of aliases) {
  if (!present(alias.phrase) || !present(alias.normalized) || alias.normalized !== alias.phrase.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim()) fail(`alias ${alias.id || "unknown"}: invalid phrase or normalized value`);
  if (aliasPhrases.has(alias.normalized)) fail(`alias normalized phrase duplicated: ${alias.normalized}`);
  aliasPhrases.add(alias.normalized);
  for (const target of alias.targets || []) if (target.kind === "style" && !styleSet.has(target.id)) fail(`alias ${alias.phrase}: unknown style ${target.id}`);
}

const modifierFiles = readdirSync(join(CATALOG, "modifiers")).filter((name) => name.endsWith(".json")).sort();
const modifierSet = new Set(modifierFiles.map((name) => name.slice(0, -5)));
for (const name of modifierFiles) {
  const modifier = json(join(CATALOG, "modifiers", name));
  if (modifier.id !== name.slice(0, -5)) fail(`${name}: id mismatch`);
  for (const id of modifier.incompatibleStyles || []) if (!styleSet.has(id)) fail(`${modifier.id}: unknown incompatible style ${id}`);
  for (const id of modifier.incompatibleFamilies || []) if (!familySet.has(id)) fail(`${modifier.id}: unknown incompatible family ${id}`);
  for (const id of modifier.incompatibleModifiers || []) if (!modifierSet.has(id)) fail(`${modifier.id}: unknown incompatible modifier ${id}`);
}

const adaptersDir = join(ROOT, "references/adapters");
const adapterIds = existsSync(adaptersDir) ? readdirSync(adaptersDir).filter((id) => statSync(join(adaptersDir, id)).isDirectory()).sort() : [];
for (const id of adapterIds) {
  for (const name of ["adapter.json", "ADAPTER.md"]) if (!existsSync(join(adaptersDir, id, name))) fail(`adapter ${id}: missing ${name}`);
  if (existsSync(join(adaptersDir, id, "adapter.json")) && json(join(adaptersDir, id, "adapter.json")).id !== id) fail(`adapter ${id}: id mismatch`);
}
if (statSync(INDEX).size >= 200 * 1024) fail(`references/index.json is ${statSync(INDEX).size} bytes; must stay under 204800`);

for (const image of ledger.images || []) {
  const generated = image.originType === "generated";
  if (!generated) publicImages.push(image);
  const required = ["styleId", "localPath", "title", "creator", "attributionText", "modificationNote", "finalSha256", ...(generated ? ["model", "generator", "generatedAt", "prompt", "promptRecordStatus", "generationRecord"] : ["institution", "sourcePage", "directFileUrl", "sourceFileTitle", "sourceFileSha1", "license", "licenseUrl", "rightsChecked"])];
  for (const field of required) if (!present(image[field])) fail(`${image.localPath || "unknown image"}: missing required ${field}`);
  if (!styleSet.has(image.styleId)) fail(`${image.localPath}: unknown style ${image.styleId}`);
  if (typeof image.localPath !== "string" || isAbsolute(image.localPath) || image.localPath.includes("..") || !image.localPath.startsWith(`assets/refs/${image.styleId}/`)) fail(`${image.localPath}: localPath must be an in-Skill asset path`);
  if (paths.has(image.localPath)) fail(`${image.localPath}: duplicate localPath`);
  paths.add(image.localPath);
  if (!generated) {
    if (sourcePages.has(image.sourcePage)) fail(`${image.localPath}: duplicate sourcePage ${image.sourcePage}`);
    sourcePages.add(image.sourcePage);
  }
  counts.set(image.styleId, (counts.get(image.styleId) || 0) + 1);

  const conditions = ["underlyingWork", "trademark", "peoplePrivacyPublicity", "architectureProperty", "culturalUse", "intendedUse"];
  const missing = conditions.filter((field) => !present(image.conditions?.[field]));
  if (missing.length) fail(`${image.localPath}: missing asset conditions ${missing.join(", ")}`);
  const review = image.assetReview || {};
  if (review.status !== "approved" || !present(review.reviewer) || !DATE.test(review.reviewedAt || "") || review.fullSize !== true || review.cardScale !== true || review.visualFit !== "strong" || review.misleading !== false || !present(review.distinctTeachingRole) || !present(review.notes) || review.reviewRecord !== "references/provenance/final-visual-audit.json") {
    fail(`${image.localPath}: assetReview must record approved strong non-misleading fit, teaching role, notes, and independent full/card review record`);
  } else if (!existsSync(resolveRecord(review.reviewRecord))) fail(`${image.localPath}: assetReview reviewRecord does not exist`);

  if (generated) {
    if (!image.generationRecord?.startsWith("references/provenance/generated/")) fail(`${image.localPath}: generationRecord must use the portable in-Skill provenance directory`);
    if (!DATE.test(image.generatedAt || "")) fail(`${image.localPath}: invalid generatedAt date`);
    if (image.promptRecordStatus !== "exact") fail(`${image.localPath}: promptRecordStatus must be exact`);
    if (!image.attributionText?.includes(image.creator) || !image.attributionText?.includes(image.generatedAt)) fail(`${image.localPath}: generated attribution omits creator or date`);
    const recordPath = resolveRecord(image.generationRecord);
    if (!recordPath || !existsSync(recordPath)) fail(`${image.localPath}: generationRecord does not exist`);
    else {
      const record = json(recordPath);
      if (record.status !== "portable_exact_generation_record") fail(`${image.localPath}: generationRecord status must be portable_exact_generation_record`);
      for (const [field, expected] of [["styleId", image.styleId], ["finalAsset", image.localPath], ["prompt", image.prompt], ["model", image.model], ["generatedAt", image.generatedAt], ["finalSha256", image.finalSha256], ["promptRecordStatus", image.promptRecordStatus], ...(present(record.generator) ? [["generator", image.generator]] : [])]) {
        if (record[field] !== expected) fail(`${image.localPath}: generationRecord ${field} does not match ledger`);
      }
      if (present(record.sourceSha256) && !SHA256.test(record.sourceSha256)) fail(`${image.localPath}: generationRecord sourceSha256 is invalid`);
      if (present(record.sourceOutput)) {
        const sourcePath = resolveRecord(record.sourceOutput);
        if (!sourcePath || !existsSync(sourcePath)) fail(`${image.localPath}: generationRecord sourceOutput does not exist`);
        else if (!present(record.sourceSha256) || digest(readFileSync(sourcePath)) !== record.sourceSha256) fail(`${image.localPath}: generationRecord sourceSha256 mismatch`);
      } else if (present(record.sourceSha256) && !present(record.sourceOutputStatus)) fail(`${image.localPath}: generationRecord must explain why the hashed raw source output is not bundled`);
    }
  } else {
    if (!(new Set(ledger.allowedLicenses || [])).has(image.license)) fail(`${image.localPath}: disallowed license ${image.license}`);
    if (image.license?.startsWith("CC ") && !image.licenseUrl) fail(`${image.localPath}: Creative Commons license URL missing`);
    if (!HTTPS.test(image.sourcePage || "")) fail(`${image.localPath}: sourcePage must be an exact HTTPS asset page`);
    if (!HTTPS.test(image.directFileUrl || "")) fail(`${image.localPath}: invalid directFileUrl`);
    if (!DATE.test(image.rightsChecked || "")) fail(`${image.localPath}: invalid rightsChecked date`);
    if (!/^[a-f0-9]{40}$/.test(image.sourceFileSha1 || "")) fail(`${image.localPath}: invalid sourceFileSha1`);
    if (Boolean(image.shareAlikeRequired) !== image.license?.includes("BY-SA")) fail(`${image.localPath}: shareAlikeRequired does not match ${image.license}`);
  }
  for (const requiredText of generated ? [image.creator, image.generatedAt, image.modificationNote] : [image.creator, image.license, image.sourcePage, image.modificationNote]) {
    if (requiredText && !image.attributionText?.includes(requiredText)) fail(`${image.localPath}: attributionText omits ${requiredText}`);
  }

  const file = join(ROOT, image.localPath || "");
  if (!existsSync(file)) {
    fail(`${image.localPath}: file missing`);
    continue;
  }
  const bytes = readFileSync(file);
  const extension = extname(file).toLowerCase();
  const valid = ([".jpg", ".jpeg"].includes(extension) && bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff) || (extension === ".png" && bytes.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]))) || (extension === ".webp" && bytes.subarray(0, 4).toString("ascii") === "RIFF" && bytes.subarray(8, 12).toString("ascii") === "WEBP");
  if (!valid) fail(`${image.localPath}: file signature does not match a supported image extension`);
  const dimensions = imageDimensions(bytes, extension);
  if (!dimensions || dimensions.width !== 800 || dimensions.height !== 1000) fail(`${image.localPath}: expected 800x1000 pixels, found ${dimensions ? `${dimensions.width}x${dimensions.height}` : "unreadable dimensions"}`);
  if (!SHA256.test(image.finalSha256 || "")) fail(`${image.localPath}: invalid finalSha256`);
  if (digest(bytes) !== image.finalSha256) fail(`${image.localPath}: SHA-256 mismatch`);
}

for (const id of styleIds) {
  const count = counts.get(id) || 0;
  if (count < 1) fail(`${id}: expected at least one ledger image`);
}
if (existsSync(REFS)) {
  for (const styleId of readdirSync(REFS).sort()) {
    const directory = join(REFS, styleId);
    if (!statSync(directory).isDirectory()) continue;
    for (const name of readdirSync(directory).sort()) {
      const file = join(directory, name);
      if (statSync(file).isFile() && IMAGE_EXTENSIONS.has(extname(name).toLowerCase())) actualReferenceFiles.push(posix(relative(ROOT, file)));
    }
  }
}
for (const path of actualReferenceFiles) if (!paths.has(path)) fail(`${path}: reference image has no source-ledger record`);
for (const path of paths) if (!actualReferenceFiles.includes(path)) fail(`${path}: source-ledger record has no reference image`);

if (!existsSync(ATTRIBUTION)) fail("ATTRIBUTION.md: missing");
else if (readFileSync(ATTRIBUTION, "utf8") !== expectedAttribution(ledger)) fail("ATTRIBUTION.md: stale — run npm run build:attribution");

const freshness = spawnSync(process.execPath, [join(ROOT, "scripts/build/build-index.mjs"), "--check"], { cwd: ROOT, encoding: "utf8" });
if (freshness.status !== 0) fail((freshness.stderr || freshness.stdout || "index freshness check failed").trim());

if (errors.length) {
  console.error(`validate: FAIL (${errors.length} error(s))`);
  for (const error of errors) console.error(`  - ${error}`);
  process.exit(1);
}

console.log("validate: OK");
console.log(`  catalog: ${styles.size} styles / ${families.length} families / ${modifierFiles.length} modifiers / ${adapterIds.length} adapters`);
console.log("  evidence: cultural and human visual review records verified");
console.log(`  images: ${paths.size} approved ledger-backed references; hashes, dimensions, provenance, rights, and attribution verified`);
console.log(`  index: fresh, ${statSync(INDEX).size} bytes`);
