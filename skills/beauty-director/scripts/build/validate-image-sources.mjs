#!/usr/bin/env node
import { createHash } from "node:crypto";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { basename, dirname, extname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "../..");
const WORKSPACE = resolve(ROOT, "../../..");
const LEDGER_PATH = join(ROOT, "references/image-sources.json");
const ATTRIBUTION_PATH = join(ROOT, "ATTRIBUTION.md");
const REFS_DIR = join(ROOT, "assets/refs");
const RIGHTS_RECEIPT_PATH = join(ROOT, "references/provenance/final-public-source-rights-recheck.json");
const errors = [];
const DATE = /^\d{4}-\d{2}-\d{2}$/;
const SHA256 = /^[a-f0-9]{64}$/;

function present(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function posix(path) {
  return path.split(sep).join("/");
}

function digest(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function resolveRecordPath(path) {
  if (isAbsolute(path)) return path;
  if (path.startsWith("projects/")) return join(WORKSPACE, path);
  return join(ROOT, path);
}

function allReferenceFiles() {
  if (!existsSync(REFS_DIR)) return [];
  const files = [];
  for (const styleId of readdirSync(REFS_DIR).sort()) {
    const directory = join(REFS_DIR, styleId);
    if (!statSync(directory).isDirectory()) continue;
    for (const name of readdirSync(directory).sort()) {
      const path = join(directory, name);
      if (statSync(path).isFile() && [".jpg", ".jpeg", ".png", ".webp"].includes(extname(name).toLowerCase())) {
        files.push(posix(relative(ROOT, path)));
      }
    }
  }
  return files;
}

function jpegDimensions(bytes) {
  let offset = 2;
  const startOfFrame = new Set([0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf]);
  while (offset + 8 < bytes.length) {
    if (bytes[offset] !== 0xff) {
      offset += 1;
      continue;
    }
    while (bytes[offset] === 0xff) offset += 1;
    const marker = bytes[offset];
    offset += 1;
    if (marker === 0xd8 || marker === 0xd9 || marker === 0x01) continue;
    if (offset + 2 > bytes.length) break;
    const length = bytes.readUInt16BE(offset);
    if (length < 2 || offset + length > bytes.length) break;
    if (startOfFrame.has(marker) && length >= 7) {
      return { width: bytes.readUInt16BE(offset + 5), height: bytes.readUInt16BE(offset + 3) };
    }
    offset += length;
  }
  return null;
}

function webpDimensions(bytes) {
  const chunk = bytes.subarray(12, 16).toString("ascii");
  if (chunk === "VP8X" && bytes.length >= 30) {
    const width = 1 + bytes[24] + (bytes[25] << 8) + (bytes[26] << 16);
    const height = 1 + bytes[27] + (bytes[28] << 8) + (bytes[29] << 16);
    return { width, height };
  }
  if (chunk === "VP8L" && bytes.length >= 25 && bytes[20] === 0x2f) {
    const width = 1 + bytes[21] + ((bytes[22] & 0x3f) << 8);
    const height = 1 + (bytes[22] >> 6) + (bytes[23] << 2) + ((bytes[24] & 0x0f) << 10);
    return { width, height };
  }
  if (chunk === "VP8 " && bytes.length >= 30 && bytes[23] === 0x9d && bytes[24] === 0x01 && bytes[25] === 0x2a) {
    return { width: bytes.readUInt16LE(26) & 0x3fff, height: bytes.readUInt16LE(28) & 0x3fff };
  }
  return null;
}

function imageDimensions(bytes, extension) {
  if ([".jpg", ".jpeg"].includes(extension)) return jpegDimensions(bytes);
  if (extension === ".png" && bytes.length >= 24) {
    return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) };
  }
  if (extension === ".webp") return webpDimensions(bytes);
  return null;
}

function expectedAttribution(ledger) {
  const lines = [
    "# Reference Image Attribution",
    "",
    "Every bundled reference is delivered at 800x1000 pixels. Each asset's own attribution and modification note states whether its source was cropped, padded, or proportionally resized. Public-source records preserve their license and file-page evidence; generated records preserve their generator, date, prompt, and modification note.",
    "",
  ];
  for (const record of ledger.images) {
    lines.push(
      `## ${record.styleId} — ${basename(record.localPath)}`,
      "",
      `Local file: ${record.localPath}`,
      "",
      record.attributionText,
      "",
    );
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
    if (record.originType === "generated" && record.generationRecord) {
      lines.push(`Generation record: ${record.generationRecord}`, "");
    }
  }
  return `${lines.join("\n")}\n`;
}

let ledger = { allowedLicenses: [], images: [] };
let ledgerBytes = Buffer.alloc(0);
try {
  ledgerBytes = readFileSync(LEDGER_PATH);
  ledger = JSON.parse(ledgerBytes.toString("utf8"));
} catch (error) {
  errors.push(`references/image-sources.json: ${error.message}`);
}

const styleIds = new Set(
  readdirSync(join(ROOT, "references/catalog/styles"))
    .filter((id) => existsSync(join(ROOT, "references/catalog/styles", id, "style.json"))),
);
const allowed = new Set(ledger.allowedLicenses || []);
const paths = new Set();
const sourcePages = new Set();
const counts = new Map();
const publicImages = [];
const attribution = existsSync(ATTRIBUTION_PATH) ? readFileSync(ATTRIBUTION_PATH, "utf8") : "";

for (const image of ledger.images || []) {
  const generated = image.originType === "generated";
  if (!generated) publicImages.push(image);
  const commonFields = ["styleId", "localPath", "title", "creator", "attributionText", "modificationNote", "finalSha256"];
  const provenanceFields = generated
    ? ["model", "generator", "generatedAt", "prompt", "promptRecordStatus", "generationRecord"]
    : ["institution", "sourcePage", "directFileUrl", "sourceFileTitle", "sourceFileSha1", "license", "licenseUrl", "rightsChecked"];
  for (const field of [...commonFields, ...provenanceFields]) {
    if (!present(image[field])) errors.push(`${image.localPath || "unknown image"}: missing required ${field}`);
  }
  if (!styleIds.has(image.styleId)) errors.push(`${image.localPath}: unknown style ${image.styleId}`);
  if (paths.has(image.localPath)) errors.push(`${image.localPath}: duplicate localPath`);
  paths.add(image.localPath);
  if (!generated) {
    if (sourcePages.has(image.sourcePage)) errors.push(`${image.localPath}: duplicate sourcePage ${image.sourcePage}`);
    sourcePages.add(image.sourcePage);
  }
  counts.set(image.styleId, (counts.get(image.styleId) || 0) + 1);

  const conditionFields = ["underlyingWork", "trademark", "peoplePrivacyPublicity", "architectureProperty", "culturalUse", "intendedUse"];
  const missingConditions = conditionFields.filter((field) => !present(image.conditions?.[field]));
  if (missingConditions.length) errors.push(`${image.localPath}: missing asset conditions ${missingConditions.join(", ")}`);
  const review = image.assetReview || {};
  if (
    review.status !== "approved" ||
    !present(review.reviewer) ||
    !DATE.test(review.reviewedAt || "") ||
    review.fullSize !== true ||
    review.cardScale !== true ||
    review.visualFit !== "strong" ||
    review.misleading !== false ||
    !present(review.distinctTeachingRole) ||
    !present(review.notes) ||
    review.reviewRecord !== "references/provenance/final-visual-audit.json"
  ) {
    errors.push(`${image.localPath}: assetReview must record approved strong non-misleading fit, teaching role, notes, and independent full/card review record`);
  } else if (!existsSync(resolveRecordPath(review.reviewRecord))) {
    errors.push(`${image.localPath}: assetReview reviewRecord does not exist`);
  }

  if (generated) {
    if (!image.generationRecord?.startsWith("references/provenance/generated/")) {
      errors.push(`${image.localPath}: generationRecord must use the portable in-Skill provenance directory`);
    }
    if (!DATE.test(image.generatedAt || "")) errors.push(`${image.localPath}: invalid generatedAt date`);
    if (image.promptRecordStatus !== "exact") errors.push(`${image.localPath}: promptRecordStatus must be exact`);
    if (!image.attributionText?.includes(image.creator) || !image.attributionText?.includes(image.generatedAt)) {
      errors.push(`${image.localPath}: generated attribution omits creator or date`);
    }
    const recordPath = present(image.generationRecord) ? resolveRecordPath(image.generationRecord) : null;
    if (!recordPath || !existsSync(recordPath)) {
      errors.push(`${image.localPath}: generationRecord does not exist`);
    } else {
      let record;
      try {
        record = JSON.parse(readFileSync(recordPath, "utf8"));
      } catch (error) {
        errors.push(`${image.localPath}: generationRecord is not valid JSON: ${error.message}`);
      }
      if (record) {
        if (record.status !== "portable_exact_generation_record") {
          errors.push(`${image.localPath}: generationRecord status must be portable_exact_generation_record`);
        }
        const comparisons = [
          ["styleId", image.styleId],
          ["finalAsset", image.localPath],
          ["prompt", image.prompt],
          ["model", image.model],
          ["generatedAt", image.generatedAt],
          ["finalSha256", image.finalSha256],
          ["promptRecordStatus", image.promptRecordStatus],
        ];
        if (present(record.generator)) comparisons.push(["generator", image.generator]);
        for (const [field, expected] of comparisons) {
          if (record[field] !== expected) errors.push(`${image.localPath}: generationRecord ${field} does not match ledger`);
        }
        if (present(record.sourceSha256) && !SHA256.test(record.sourceSha256)) {
          errors.push(`${image.localPath}: generationRecord sourceSha256 is invalid`);
        }
        if (present(record.sourceOutput)) {
          const sourcePath = present(record.sourceOutput) ? resolveRecordPath(record.sourceOutput) : null;
          if (!sourcePath || !existsSync(sourcePath)) {
            errors.push(`${image.localPath}: generationRecord sourceOutput does not exist`);
          } else if (!present(record.sourceSha256) || digest(readFileSync(sourcePath)) !== record.sourceSha256) {
            errors.push(`${image.localPath}: generationRecord sourceSha256 mismatch`);
          }
        } else if (present(record.sourceSha256) && !present(record.sourceOutputStatus)) {
          errors.push(`${image.localPath}: generationRecord must explain why the hashed raw source output is not bundled`);
        }
      }
    }
  } else {
    if (!allowed.has(image.license)) errors.push(`${image.localPath}: disallowed license ${image.license}`);
    if (image.license?.startsWith("CC ") && !image.licenseUrl) errors.push(`${image.localPath}: Creative Commons license URL missing`);
    if (!/^https:\/\//.test(image.sourcePage || "")) errors.push(`${image.localPath}: sourcePage must be an exact HTTPS asset page`);
    if (!/^https:\/\//.test(image.directFileUrl || "")) errors.push(`${image.localPath}: invalid directFileUrl`);
    if (!DATE.test(image.rightsChecked || "")) errors.push(`${image.localPath}: invalid rightsChecked date`);
    if (!/^[a-f0-9]{40}$/.test(image.sourceFileSha1 || "")) errors.push(`${image.localPath}: invalid sourceFileSha1`);
    if (Boolean(image.shareAlikeRequired) !== image.license?.includes("BY-SA")) {
      errors.push(`${image.localPath}: shareAlikeRequired does not match ${image.license}`);
    }
  }
  for (const requiredText of generated
    ? [image.creator, image.generatedAt, image.modificationNote]
    : [image.creator, image.license, image.sourcePage, image.modificationNote]) {
    if (requiredText && !image.attributionText?.includes(requiredText)) {
      errors.push(`${image.localPath}: attributionText omits ${requiredText}`);
    }
  }

  const path = join(ROOT, image.localPath || "");
  if (!existsSync(path)) {
    errors.push(`${image.localPath}: file missing`);
    continue;
  }
  const bytes = readFileSync(path);
  const extension = extname(path).toLowerCase();
  const validImage =
    ([".jpg", ".jpeg"].includes(extension) && bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff) ||
    (extension === ".png" && bytes.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]))) ||
    (extension === ".webp" && bytes.subarray(0, 4).toString("ascii") === "RIFF" && bytes.subarray(8, 12).toString("ascii") === "WEBP");
  if (!validImage) errors.push(`${image.localPath}: file signature does not match a supported image extension`);
  const dimensions = imageDimensions(bytes, extension);
  if (!dimensions || dimensions.width !== 800 || dimensions.height !== 1000) {
    errors.push(`${image.localPath}: expected 800x1000 pixels, found ${dimensions ? `${dimensions.width}x${dimensions.height}` : "unreadable dimensions"}`);
  }
  const finalDigest = digest(bytes);
  if (!SHA256.test(image.finalSha256 || "")) errors.push(`${image.localPath}: invalid finalSha256`);
  if (finalDigest !== image.finalSha256) errors.push(`${image.localPath}: SHA-256 mismatch`);
}

for (const styleId of styleIds) {
  const count = counts.get(styleId) || 0;
  if (count < 1 || count > 3) errors.push(`${styleId}: expected 1-3 ledger images, found ${count}`);
}

const filesystemPaths = allReferenceFiles();
for (const path of filesystemPaths) {
  if (!paths.has(path)) errors.push(`${path}: reference image has no source-ledger record`);
}
for (const path of paths) {
  if (!filesystemPaths.includes(path)) errors.push(`${path}: source-ledger record has no reference image`);
}

if (!existsSync(ATTRIBUTION_PATH)) {
  errors.push("ATTRIBUTION.md: missing");
} else if (attribution !== expectedAttribution(ledger)) {
  errors.push("ATTRIBUTION.md: stale — run npm run build:attribution");
}

if (!existsSync(RIGHTS_RECEIPT_PATH)) {
  errors.push(`${posix(relative(WORKSPACE, RIGHTS_RECEIPT_PATH))}: final live rights verification receipt missing`);
} else {
  let receipt;
  try {
    receipt = JSON.parse(readFileSync(RIGHTS_RECEIPT_PATH, "utf8"));
  } catch (error) {
    errors.push(`${posix(relative(WORKSPACE, RIGHTS_RECEIPT_PATH))}: ${error.message}`);
  }
  if (receipt) {
    const summary = receipt.summary || {};
    if (summary.total !== publicImages.length) {
      errors.push(`final rights receipt: summary.total must equal current public ledger count ${publicImages.length}`);
    }
    if (summary.passed !== publicImages.length) {
      errors.push(`final rights receipt: summary.passed must equal current public ledger count ${publicImages.length}`);
    }
    if (summary.exceptions !== 0) errors.push("final rights receipt: summary.exceptions must be 0");
    if (summary.allPass !== true) errors.push("final rights receipt: summary.allPass must be true");
    if (summary.ledgerSha256 !== digest(ledgerBytes)) errors.push("final rights receipt: ledgerSha256 does not match canonical ledger");
    const records = Array.isArray(receipt.records) ? receipt.records : [];
    const recordPaths = new Set();
    const publicByPath = new Map(publicImages.map((image) => [image.localPath, image]));
    for (const record of records) {
      if (recordPaths.has(record.localPath)) errors.push(`final rights receipt: duplicate localPath ${record.localPath}`);
      recordPaths.add(record.localPath);
      const image = publicByPath.get(record.localPath);
      if (!image) {
        errors.push(`final rights receipt: unknown public asset ${record.localPath}`);
        continue;
      }
      if (record.status !== "pass") errors.push(`${record.localPath}: final live rights verification did not pass`);
      if (record.styleId !== image.styleId) errors.push(`${record.localPath}: rights receipt styleId does not match ledger`);
      if (record.sourcePage !== image.sourcePage) errors.push(`${record.localPath}: rights receipt sourcePage does not match ledger`);
    }
    for (const image of publicImages) {
      if (!recordPaths.has(image.localPath)) errors.push(`${image.localPath}: absent from final live rights verification receipt`);
    }
    if (recordPaths.size !== publicImages.length) {
      errors.push(`final rights receipt: path coverage ${recordPaths.size} does not equal public ledger count ${publicImages.length}`);
    }
  }
}

if (errors.length) {
  console.error(`validate-image-sources: FAIL (${errors.length} error(s))`);
  for (const error of errors) console.error(`  - ${error}`);
  process.exit(1);
}

console.log("validate-image-sources: OK");
console.log(`  images: ${paths.size}`);
console.log(`  styles with references: ${counts.size}`);
console.log("  provenance, exact generation receipts, 800x1000 dimensions, live rights, approvals, checksums, and attribution: verified");
