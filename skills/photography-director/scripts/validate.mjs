#!/usr/bin/env node

import { createHash } from "node:crypto";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const CATALOG = join(ROOT, "references/catalog");
const errors = [];
const CLAIM_POLICIES = new Set(["observed", "inferred", "confirmed-or-documented", "documented-or-inferred"]);
const CLAIM_BASES = new Set(["observed", "confirmed", "documented", "inferred"]);
const EXACT_FIELDS = new Set(["camera", "cameraModel", "lens", "lensModel", "focalLength", "aperture", "shutter", "shutterSpeed", "iso", "filmStock", "process", "modifier", "lightingHardware"]);
function check(condition, message) {
  if (!condition) errors.push(message);
}

function read(path) {
  return readFileSync(path, "utf8");
}

function json(path) {
  try {
    return JSON.parse(read(path));
  } catch (error) {
    errors.push(`${relative(ROOT, path)} is not valid JSON: ${error.message}`);
    return {};
  }
}

function jsonDirectory(path) {
  return readdirSync(path)
    .filter((name) => name.endsWith(".json"))
    .sort()
    .map((name) => json(join(path, name)));
}

function duplicates(values) {
  const seen = new Set();
  return values.filter((value) => seen.has(value) || !seen.add(value));
}

function jpegDimensions(buffer) {
  if (buffer[0] !== 0xff || buffer[1] !== 0xd8) throw new Error("not a JPEG");
  const sizeMarkers = new Set([0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf]);
  let offset = 2;
  while (offset + 8 < buffer.length) {
    while (buffer[offset] === 0xff) offset += 1;
    const marker = buffer[offset++];
    if (marker === 0xd8 || marker === 0x01) continue;
    if (marker === 0xd9 || marker === 0xda) break;
    const length = buffer.readUInt16BE(offset);
    if (sizeMarkers.has(marker)) {
      return { height: buffer.readUInt16BE(offset + 3), width: buffer.readUInt16BE(offset + 5) };
    }
    if (length < 2) throw new Error("invalid JPEG segment");
    offset += length;
  }
  throw new Error("JPEG dimensions not found");
}

function filesBelow(path) {
  return readdirSync(path, { withFileTypes: true }).flatMap((entry) => {
    const child = join(path, entry.name);
    return entry.isDirectory() ? filesBelow(child) : [child];
  });
}

function runQuery(args, label) {
  const result = spawnSync(process.execPath, [join(ROOT, "scripts/query.mjs"), ...args], {
    cwd: ROOT,
    encoding: "utf8",
    timeout: 10_000,
  });
  check(result.status === 0, `${label} query failed: ${(result.stderr || "").trim()}`);
  check((result.stdout || "").length <= 7_500, `${label} query exceeded 7,500 characters`);
  try {
    const packet = JSON.parse(result.stdout);
    check(!Object.hasOwn(packet, "query"), `${label} query echoed input text`);
    return packet;
  } catch (error) {
    errors.push(`${label} query returned invalid JSON: ${error.message}`);
    return {};
  }
}

const ledger = json(join(ROOT, "references/source-ledger.json"));
const subjectCatalog = json(join(CATALOG, "subject-sets.json"));
const visibleFitCatalog = json(join(CATALOG, "visible-fit.json"));
const aliases = json(join(CATALOG, "aliases.json")).aliases || [];
const looks = jsonDirectory(join(CATALOG, "looks"));
const axes = jsonDirectory(join(CATALOG, "axes"));
const axisValues = axes.flatMap((axis) => (axis.values || []).map((value) => ({ ...value, axisId: axis.id })));
const support = (subjectCatalog.references || []).map((reference) => ({
  ...(subjectCatalog.sourceDefaults || {}),
  ...reference,
  review: {
    ...(subjectCatalog.sourceDefaults?.review || {}),
    ...(reference.review || {}),
    teachingRole: reference.teachingRole || reference.review?.teachingRole || "",
  },
}));
const visibleFitReferences = visibleFitCatalog.references || [];
const references = [...(ledger.references || []), ...support];
const referenceMap = new Map(references.map((reference) => [reference.id, reference]));
const lookIds = new Set(looks.map((look) => look.id));
const axisValueIds = new Set(axisValues.map((value) => value.id));
const axisValueMap = new Map(axisValues.map((value) => [value.id, value]));
const lookReferencesByAxisValue = new Map(axisValues.map((value) => [value.id, new Set()]));

check(visibleFitCatalog.version === 1, "visible-fit catalog must use version 1");
check(duplicates(visibleFitReferences.map((reference) => reference.id)).length === 0, "visible-fit reference IDs must be unique");
check(duplicates(looks.map((look) => look.id)).length === 0, "look IDs must be unique");
check(duplicates(axes.map((axis) => axis.id)).length === 0, "axis IDs must be unique");
check(duplicates(axisValues.map((value) => value.id)).length === 0, "axis-value IDs must be globally unique");
check(duplicates(references.map((reference) => reference.id)).length === 0, "reference IDs must be unique");
check(duplicates((subjectCatalog.sets || []).map((set) => set.id)).length === 0, "subject-set IDs must be unique");
const pressPhotoRole = referenceMap.get("ref-candid-event-reportage")?.review?.teachingRole || "";
const pressPhotoRoleGuard = (role) =>
  /visible subject\/photographer exchange/i.test(role) &&
  /does not prove collaboration/i.test(role) &&
  /authentic working task/i.test(role);
check(pressPhotoRoleGuard(pressPhotoRole), "press/photo-op role must state visible proof limits");
check(!pressPhotoRoleGuard(pressPhotoRole.replace("does not prove collaboration", "demonstrates collaboration")), "press/photo-op role mutation was not detected");

for (const look of looks) {
  check(look.version === 1 && look.id && look.displayName && look.definition, `look ${look.id || "<missing>"} is incomplete`);
  check((look.referenceIds || []).length > 0, `look ${look.id} has no reference`);
  for (const id of look.referenceIds || []) check(referenceMap.has(id), `look ${look.id} has unresolved reference ${id}`);
  for (const ids of Object.values(look.axisValues || {})) {
    for (const id of ids) {
      check(axisValueIds.has(id), `look ${look.id} has unresolved axis value ${id}`);
      for (const referenceId of look.referenceIds || []) lookReferencesByAxisValue.get(id)?.add(referenceId);
    }
  }
  for (const cue of look.cues || []) {
    const value = axisValueMap.get(cue);
    if (value?.claimPolicy === "inferred") check(value.visibleCues?.[0], `inferred look cue ${cue} lacks an appearance-safe visible term`);
  }
}

for (const value of axisValues) {
  check(value.id && value.displayName && value.definition, `axis value in ${value.axisId} is incomplete`);
  check(CLAIM_POLICIES.has(value.claimPolicy), `axis value ${value.id} has invalid claim policy ${value.claimPolicy}`);
  check((value.referenceIds || []).length > 0, `axis value ${value.id} has no teaching reference`);
  check((lookReferencesByAxisValue.get(value.id) || new Set()).size > 0, `axis value ${value.id} is unused by every look`);
  for (const id of value.referenceIds || []) {
    check(referenceMap.has(id), `axis value ${value.id} has unresolved reference ${id}`);
    check(lookReferencesByAxisValue.get(value.id)?.has(id), `axis value ${value.id} uses ${id}, but no look using the value supplies that reference`);
  }
}

for (const alias of aliases) {
  check(alias.phrase && (alias.targets || []).length > 0, "alias is missing a phrase or target");
  for (const target of alias.targets || []) {
    if (target.kind === "look") check(lookIds.has(target.id), `alias ${alias.phrase} has unresolved look ${target.id}`);
    else if (target.kind === "axis-value") check(axisValueIds.has(target.id), `alias ${alias.phrase} has unresolved axis value ${target.id}`);
    else check(false, `alias ${alias.phrase} has unsupported target kind ${target.kind}`);
  }
}

for (const set of subjectCatalog.sets || []) {
  check((set.triggers || []).length > 0 && set.role, `subject set ${set.id} is incomplete`);
  check((set.referenceIds || []).length === 3, `subject set ${set.id} must contain exactly three references`);
  check((set.treatmentLookIds || []).length === 3, `subject set ${set.id} must contain exactly three compatible treatment looks`);
  if (set.requiredLocks) {
    check(Array.isArray(set.requiredLocks) && set.requiredLocks.length > 0 && set.requiredLocks.every((lock) => typeof lock === "string" && lock), `subject set ${set.id} has invalid required locks`);
    check(duplicates(set.requiredLocks).length === 0, `subject set ${set.id} repeats a required lock`);
  }
  if (set.catalogGap) check(typeof set.catalogGap === "string" && set.catalogGap.length > 20, `subject set ${set.id} has an invalid catalog gap`);
  if (set.transferCard) check(Array.isArray(set.transferCard) && set.transferCard.length === 6 && set.transferCard.every((field) => typeof field === "string" && field.includes(":")), `subject set ${set.id} must provide six labeled transfer fields`);
  if (set.sampleCoverage) check(Array.isArray(set.sampleCoverage) && set.sampleCoverage.length === 2 && set.sampleCoverage.every((terms) => Array.isArray(terms) && terms.length > 0), `subject set ${set.id} has invalid sample coverage`);
  if (set.alsoDiffers) {
    check(set.alsoDiffers && typeof set.alsoDiffers === "object" && !Array.isArray(set.alsoDiffers), `subject set ${set.id} has invalid also-differs data`);
    for (const [referenceId, differences] of Object.entries(set.alsoDiffers || {})) {
      check((set.referenceIds || []).includes(referenceId), `subject set ${set.id} has also-differs data for unrelated ${referenceId}`);
      check(Array.isArray(differences) && differences.length > 0 && differences.every((difference) => typeof difference === "string" && difference), `subject set ${set.id} has invalid also-differs values for ${referenceId}`);
    }
  }
  for (const id of set.referenceIds || []) check(referenceMap.has(id), `subject set ${set.id} has unresolved reference ${id}`);
  for (const id of set.treatmentLookIds || []) check(lookIds.has(id), `subject set ${set.id} has unresolved treatment look ${id}`);
}

for (const reference of visibleFitReferences) {
  check(referenceMap.has(reference.id), `visible-fit reference ${reference.id} is not in the catalog`);
  check(["single", "group"].includes(reference.subjectCount), `visible-fit reference ${reference.id} has an invalid subjectCount`);
  for (const field of ["settings", "actions", "traits"]) {
    check(Array.isArray(reference[field]) && reference[field].length > 0 && reference[field].every((value) => typeof value === "string" && value), `visible-fit reference ${reference.id} has invalid ${field}`);
  }
  if (reference.traitStudyFor) check(Array.isArray(reference.traitStudyFor) && reference.traitStudyFor.every((setId) => typeof setId === "string" && setId), `visible-fit reference ${reference.id} has invalid traitStudyFor`);
}

const expectedImages = new Set();
for (const reference of references) {
  check(["bundled", "authorized-remote"].includes(reference.displayMode), `reference ${reference.id} has unsupported display mode ${reference.displayMode}`);
  check(reference.originType === "real-photograph", `reference ${reference.id} is not recorded as real photography`);
  check((ledger.allowedLicenses || []).includes(reference.license), `reference ${reference.id} uses unapproved license ${reference.license}`);
  check(/^https:\/\//.test(reference.licenseUrl || ""), `reference ${reference.id} lacks an HTTPS license record`);
  check(reference.realPhotographyStatus === "verified", `reference ${reference.id} is not verified as real photography`);
  check(reference.review?.status === "approved" && reference.review?.fullSize === true && reference.review?.conversationScale === true && reference.review?.visualFit === "strong", `reference ${reference.id} lacks approved full-size and conversation-scale review`);
  check(/^https:\/\//.test(reference.sourcePage || "") && /^https:\/\//.test(reference.assetUrl || "") && reference.title && reference.creator, `reference ${reference.id} lacks internal source metadata`);
  check(Array.isArray(reference.technicalClaims), `reference ${reference.id} technicalClaims must be an array`);
  for (const claim of reference.technicalClaims || []) {
    check(claim.field && claim.value && CLAIM_BASES.has(claim.basis) && claim.source, `reference ${reference.id} has a malformed technical claim`);
    if (EXACT_FIELDS.has(claim.field)) check(["confirmed", "documented"].includes(claim.basis), `reference ${reference.id} exact ${claim.field} claim must be confirmed or documented`);
  }
  if (/^CC BY/.test(reference.license || "")) check(reference.attributionText, `reference ${reference.id} requires attribution text`);
  if (/pexels\.com/.test(reference.sourcePage || "")) {
    check(reference.license === "Pexels License" && reference.displayMode === "authorized-remote", `Pexels reference ${reference.id} must remain remote-only under the Pexels License`);
  }
  if (reference.displayMode === "authorized-remote") {
    check(reference.license === "Pexels License", `remote reference ${reference.id} is not a Pexels record`);
    check(!reference.localPath && !reference.sha256 && !reference.bundledDimensions, `remote reference ${reference.id} retains bundled-file metadata`);
    continue;
  }
  check(typeof reference.localPath === "string" && reference.localPath.startsWith("assets/references/") && !reference.localPath.includes(".."), `reference ${reference.id} has unsafe local path`);
  const path = resolve(ROOT, reference.localPath || "");
  check(existsSync(path), `reference ${reference.id} image is missing`);
  expectedImages.add(path);
  if (!existsSync(path)) continue;
  const buffer = readFileSync(path);
  const digest = createHash("sha256").update(buffer).digest("hex");
  check(digest === reference.sha256, `reference ${reference.id} SHA-256 mismatch`);
  try {
    const dimensions = jpegDimensions(buffer);
    check(dimensions.width === reference.bundledDimensions?.width && dimensions.height === reference.bundledDimensions?.height, `reference ${reference.id} dimension mismatch`);
    check(Math.max(dimensions.width, dimensions.height) <= 1_100, `reference ${reference.id} exceeds 1,100 pixels`);
  } catch (error) {
    errors.push(`reference ${reference.id}: ${error.message}`);
  }
}
const actualImages = filesBelow(join(ROOT, "assets/references")).filter((path) => /\.jpe?g$/i.test(path));
for (const path of actualImages) check(expectedImages.has(path), `untracked bundled image ${relative(ROOT, path)}`);
for (const path of expectedImages) check(actualImages.includes(path), `ledger image absent from bundle ${relative(ROOT, path)}`);

const naturalMotion = runQuery([
  "looks", "--query", "child running through a sprinkler with natural movement; not frozen, doesn't look like sports, don't pose them, never turn it into an athlete shot",
  "--limit", "5",
], "sprinkler and negative intent");
check(naturalMotion.subjectSet?.id === "sprinkler-play" && naturalMotion.subjectSet?.complete, "sprinkler query lost its complete subject set");
check(naturalMotion.noSearch === true, "complete sprinkler route must forbid live search");
check(naturalMotion.results?.length === 3, "sprinkler subject set must return exactly three paired treatments");
check(!(naturalMotion.results || []).some((look) => look.id === "frozen-sports-action"), "explicit negative motion intent admitted frozen sports");
const rejectedPortraitRefs = ["ref-professional-calm-office", "ref-professional-candid-smile", "ref-professional-lowkey-desk"];
const rejectionReroute = runQuery([
  "looks", "--query", "founder portrait workplace working alert capable caught in a real moment; no arms-crossed stock pose, avoid over-retouched skin without corporate polish",
  "--limit", "5", "--exclude", rejectedPortraitRefs.join(","), "--recovery",
], "explained rejection");
check(rejectionReroute.subjectSet?.id === "warm-real-founder" && rejectionReroute.subjectSet?.complete, "explained rejection lost the complete singular-founder reroute");
check(!(rejectionReroute.subjectSet?.references || []).some((reference) => rejectedPortraitRefs.includes(reference.id)), "explained rejection reused a rejected portrait reference");
check(rejectionReroute.results?.length === 3, "complete explained-rejection reroute must return exactly three look treatments");
check(!rejectionReroute.recoveryExhausted && rejectionReroute.results?.every((result) => !rejectedPortraitRefs.includes(result.id)), "complete explained-rejection recovery did not preserve the replacement route");
const preparedFoodRecoveryExclusions = [
  "ref-bright-editorial-food", "ref-restaurant-shrimp-pasta", "ref-window-light-food-story",
  "bright-editorial-food", "window-light-food-story", "dark-moody-tabletop",
];
const preparedFoodRecovery = runQuery([
  "looks", "--query", "prepared food appetizing ingredients overhead", "--limit", "5",
  "--exclude", preparedFoodRecoveryExclusions.join(","), "--recovery",
], "J7 recovery exhausted");
const preparedFoodReturnedReferenceIds = [
  ...(preparedFoodRecovery.subjectSet?.references || []),
  ...(preparedFoodRecovery.subjectSet?.eligibleCandidates || []),
  ...(preparedFoodRecovery.subjectSet?.traitStudies || []),
  ...(preparedFoodRecovery.hardFit?.eligibleCandidates || []),
].map((reference) => reference.id);
check(preparedFoodRecovery.recoveryExhausted === true && preparedFoodRecovery.coverageGap?.status === "recovery-exhausted", "J7 recovery did not emit the explicit exhausted-recovery signal");
check(preparedFoodRecovery.subjectSet?.id === "prepared-food" && preparedFoodRecovery.results?.length === 0 && preparedFoodReturnedReferenceIds.length === 0 && (preparedFoodRecovery.subjectSet?.treatmentLookIds || []).length === 0, "J7 recovery exhausted the prepared-food set but returned assistant refs or treatments");
const arrangedFounderExclusions = [
  "approachable-environmental-portrait", "polished-commercial-headshot", "low-key-character-portrait",
  "ref-professional-calm-office", "ref-professional-candid-smile", "ref-professional-lowkey-desk",
];
const arrangedFounderReroute = runQuery([
  "looks", "--query", "founder working, real workplace, active moment, alert capable, unposed, not arranged",
  "--exclude", arrangedFounderExclusions.join(","), "--limit", "5",
], "arranged founder rejection");
check(arrangedFounderReroute.subjectSet?.id === "warm-real-founder" && arrangedFounderReroute.subjectSet?.complete, "arranged founder rejection lost the complete singular real-work reroute");
check(!(arrangedFounderReroute.subjectSet?.references || []).some((reference) => arrangedFounderExclusions.includes(reference.id)) && !(arrangedFounderReroute.results || []).some((result) => arrangedFounderExclusions.includes(result.id)), "arranged founder rejection reused an excluded reference or treatment");
const frozenFounderTreatmentExclusions = [
  "approachable-environmental-portrait", "polished-commercial-headshot", "low-key-character-portrait",
];
const frozenFounderRejectedReferences = [
  "ref-professional-calm-office", "ref-professional-candid-smile", "ref-professional-lowkey-desk",
];
const frozenFounderReroute = runQuery([
  "looks", "--query", "founder alert capable real moment unposed working", "--limit", "5",
  "--exclude", frozenFounderTreatmentExclusions.join(","),
], "frozen founder treatment-only rejection");
check(frozenFounderReroute.subjectSet?.id === "warm-real-founder" && frozenFounderReroute.subjectSet?.complete, "treatment-only founder rejection lost the singular real-work reroute");
check(!(frozenFounderReroute.subjectSet?.references || []).some((reference) => frozenFounderRejectedReferences.includes(reference.id)), "treatment-only founder rejection reused a photo paired with a rejected treatment");
const terseFounderReroute = runQuery([
  "looks", "--query", "founder working alert capable observational unposed", "--limit", "5",
  "--exclude", frozenFounderTreatmentExclusions.join(","),
], "terse founder treatment-only rejection");
check(terseFounderReroute.noSearch === true && terseFounderReroute.subjectSet?.id === "warm-real-founder" && terseFounderReroute.subjectSet?.complete, "terse founder rejection fell through to a larger incomplete packet");
check(!(terseFounderReroute.subjectSet?.references || []).some((reference) => frozenFounderRejectedReferences.includes(reference.id)), "terse founder rejection reused an excluded photo");
const workingMomentFounderReroute = runQuery([
  "looks", "--query", "founder alert capable caught in a real working moment candid observational active unarranged not posed not corporate", "--limit", "5",
  "--exclude", frozenFounderTreatmentExclusions.join(","),
], "founder real-working-moment rejection");
check(workingMomentFounderReroute.noSearch === true && workingMomentFounderReroute.subjectSet?.id === "warm-real-founder" && workingMomentFounderReroute.subjectSet?.complete, "founder real-working-moment phrasing lost the singular founder set to a generic team route");
check(/alt text/.test(workingMomentFounderReroute.subjectSet?.role || ""), "founder replacement role no longer protects alt-text identity honesty");
const perfumeTransfer = runQuery([
  "looks", "--query", "Use this feeling for a perfume bottle instead of a person.",
  "--limit", "5",
], "perfume subject transfer");
check(perfumeTransfer.subjectSet?.id === "perfume-bottle-transfer" && perfumeTransfer.subjectSet?.complete, "perfume transfer lost its complete subject set");
check(perfumeTransfer.mode === "looks" && perfumeTransfer.noSearch === true && !perfumeTransfer.needsSearch, "perfume transfer must remain a no-search looks route");
check(perfumeTransfer.results?.length === 3, "perfume transfer must return exactly three paired treatments");
check(perfumeTransfer.subjectSet?.pairByIndex === true, "perfume transfer must preserve indexed reference/treatment pairing");
check(JSON.stringify(perfumeTransfer.subjectSet?.references?.map((reference) => reference.id)) === JSON.stringify(["ref-quiet-lived-in-perfume", "ref-luxury-still-life-polish", "ref-amber-candle-wood"]), "perfume transfer changed its curated reference order");
check(JSON.stringify(perfumeTransfer.results?.map((result) => result.id)) === JSON.stringify(["quiet-environmental-product", "luxury-still-life-polish", "dark-moody-tabletop"]), "perfume transfer changed its curated treatment order");
check(perfumeTransfer.subjectSet?.references?.[0]?.id === "ref-quiet-lived-in-perfume" && perfumeTransfer.results?.[0]?.id === "quiet-environmental-product", "perfume transfer no longer leads with the quiet lived-in real-photo pair");
check(JSON.stringify(perfumeTransfer.subjectSet?.transferCard) === JSON.stringify([
  "Lens class: natural or short-telephoto perspective",
  "Relative distance: work farther back than a portrait close-up so the bottle keeps environmental context",
  "Framing: environmental close still life with breathing room around the glass",
  "Focus: front label and near bottle edge crisp, background softly recognizable",
  "Light placement: broad soft source to one side or rear-side of the bottle",
  "Reflection control: camera angled off the bright reflection, with dark or neutral cards just outside frame",
]), "perfume transfer changed one of its six explicit glass-adaptation fields");
const clinicPacket = runQuery(["looks", "--query", "small modern clinic calm precise warm believable materials", "--limit", "5"], "small clinic");
check(clinicPacket.subjectSet?.references?.[0]?.id === "ref-clinic-axial-reception", "clinic route no longer leads with a small axial clinic interior");
check(JSON.stringify(clinicPacket.subjectSet?.requiredLocks) === JSON.stringify([
  "calm centered geometry",
  "material truth",
  "upright perspective",
  "deep spatial clarity",
  "restrained warmth with credible whites and grays",
  "human welcome",
]), "clinic route lost its accepted geometry, material, warmth, or welcome locks");
const clinicExteriorTransfer = runQuery([
  "looks", "--query", "small modern clinic building entrance exterior; calm centered geometry and deep spatial clarity; gentle late-afternoon warmth with credible whites and grays; natural materials and human scale; avoid amber wash, orange color cast, sterile CGI polish, tilted verticals", "--limit", "5",
], "clinic exterior transfer");
check(clinicExteriorTransfer.subjectSet?.id === "clinic-built-world" && clinicExteriorTransfer.subjectSet?.complete && clinicExteriorTransfer.noSearch === true, "clinic exterior transfer lost its complete no-search set");
check(JSON.stringify(clinicExteriorTransfer.subjectSet?.transferCard) === JSON.stringify([
  "Viewpoint: use a centered frontal or near-frontal exterior view with verticals upright",
  "Relative distance: step back enough to show the full entrance, approach, and surrounding materials",
  "Framing: keep the door and threshold legible within the facade, with breathing room but not a distant streetscape",
  "Focus: hold the entrance, facade materials, and ordinary-use cues clearly readable",
  "Light placement: use gentle late-afternoon side or front-side light while keeping whites and grays credible",
  "Human welcome: make the door, path, threshold, and ordinary-use cues easy to read; do not substitute human scale alone",
]), "clinic exterior transfer changed one of its six concrete architecture adaptations");
const nightMotorcycle = runQuery(["looks", "--query", "motorcycle moving through city at night speed lights readable bike rider", "--limit", "5"], "night motorcycle cause honesty");
check(nightMotorcycle.subjectSet?.id === "night-motorcycle-motion" && !(nightMotorcycle.results || []).some((result) => /flash|rear-curtain/i.test(`${result.name} ${(result.terms || []).join(" ")}`)), "night motorcycle packet exposes an undocumented flash or sync claim");
const pictorialLake = runQuery(["looks", "--query", "new lakeside campaign pictorial softness tonal range atmosphere layered composition", "--limit", "5"], "pictorial lakeside transfer");
const wildlifePacket = runQuery(["looks", "--query", "grebe chick swimming pond reflected water telephoto wildlife", "--limit", "5"], "wildlife metadata");
const wildlifeAnchor = wildlifePacket.subjectSet?.references?.find((reference) => reference.id === "ref-super-telephoto-wildlife");
check((wildlifeAnchor?.confirmed || []).some((claim) => claim.field === "cameraModel" && claim.value === "Canon EOS 5D Mark III"), "wildlife packet lost confirmed camera metadata");
check((wildlifeAnchor?.confirmed || []).some((claim) => claim.field === "date" && claim.value === "2013-05-13 20:21:22"), "wildlife packet lost confirmed creation timestamp");
check(!(wildlifeAnchor?.confirmed || []).some((claim) => Object.hasOwn(claim, "source")), "runtime claim packet leaked internal source URLs");
const botanicalProcesses = runQuery([
  "looks", "--query", "botanical cyanotype photogram historical process", "--limit", "5",
], "cyanotype botanical processes");
check(botanicalProcesses.noSearch === true && botanicalProcesses.subjectSet?.id === "cyanotype-botanical-processes" && botanicalProcesses.subjectSet?.complete, "cyanotype botanical route lost its complete no-search set");
const windowAdjacencies = runQuery([
  "looks", "--query", "woman indoor leaning direct-gaze portrait bright backlight shallow-focus editorial", "--limit", "5",
], "window sample adjacencies");
check(windowAdjacencies.noSearch === true && windowAdjacencies.subjectSet?.id === "window-portrait-adjacencies", "window sample wording lost its complete no-search set");
check((windowAdjacencies.subjectSet?.requiredLocks || []).includes("glass or window relationship"), "window route lost required locks");
check((windowAdjacencies.subjectSet?.references || []).filter((reference) => reference.alsoDiffers).length === 2, "window route lost deterministic also-differs disclosures");
const terseWindowAdjacencies = runQuery([
  "looks", "--query", "woman interior leaning editorial backlit-haze shallow-depth", "--limit", "5",
], "terse window sample adjacencies");
check(terseWindowAdjacencies.noSearch === true && terseWindowAdjacencies.subjectSet?.id === "window-portrait-adjacencies" && terseWindowAdjacencies.subjectSet?.complete, "terse window sample wording lost its complete no-search set");
const expandedWindowAdjacencies = runQuery([
  "looks", "--query", "young woman portrait indoors beside a large window leaning at the sill looking toward camera luminous highlights deep interior shadows warm muted color shallow focus close vertical asymmetric editorial framing", "--limit", "5",
], "expanded human window sample adjacencies");
check(expandedWindowAdjacencies.noSearch === true && expandedWindowAdjacencies.subjectSet?.id === "window-portrait-adjacencies" && expandedWindowAdjacencies.subjectSet?.complete, "expanded human window analysis lost its complete no-search portrait set");
const glazingWindowAdjacencies = runQuery([
  "looks", "--query", "intimate editorial portrait; person posed beside interior glazing, turning toward camera; strong backlit glow, lifted haze, deep shadow, warm muted color, soft detail, shallow depth, close vertical composition", "--limit", "5",
], "interior glazing window sample adjacencies");
check(glazingWindowAdjacencies.noSearch === true && glazingWindowAdjacencies.subjectSet?.id === "window-portrait-adjacencies" && glazingWindowAdjacencies.subjectSet?.complete, "interior-glazing portrait language drifted into an architecture packet");
check(glazingWindowAdjacencies.results?.[1]?.terms?.includes("highlight spread") && !glazingWindowAdjacencies.results?.[1]?.terms?.includes("diffusion-heavy-lens-character"), "window softness treatment exposed an inferred mechanism as a visible term");
check(glazingWindowAdjacencies.results?.[2]?.terms?.includes("high-contrast-tonality") && !glazingWindowAdjacencies.results?.[2]?.terms?.includes("split-lighting"), "window reflection treatment exposed a split-light pattern the paired photograph does not show");
check(looks.find((look) => look.id === "low-key-character-portrait")?.axisValues?.lighting?.includes("split-lighting"), "low-key portrait lost its expert split-lighting axis after public-cue repair");
const emptyGlazingArchitecture = runQuery([
  "looks", "--query", "interior glazing portrait without people empty atrium architecture", "--limit", "5",
], "empty interior glazing architecture");
check(emptyGlazingArchitecture.subjectSet?.id !== "window-portrait-adjacencies", "empty glazing architecture incorrectly routed to the person-centric portrait set");
const multiSampleBridge = runQuery([
  "looks", "--query", "sample A: close intimate quiet window portrait; sample B: lively party energy without ugly flash", "--multi-sample", "--limit", "5",
], "multi-sample social bridge");
check(multiSampleBridge.noSearch === true && multiSampleBridge.subjectSet?.id === "ambient-social-bridge", "multi-sample blend lost the ambient social bridge");
check((multiSampleBridge.subjectSet?.requiredLocks || []).includes("intimate portrait distance"), "multi-sample bridge lost required locks");
check((multiSampleBridge.subjectSet?.references || []).every((reference) => reference.alsoDiffers?.length === 2), "multi-sample bridge lost deterministic also-differs disclosures");
check(multiSampleBridge.subjectSet?.references?.[2]?.id === "ref-professional-candid-smile" && /smile|people|social|expression/i.test(multiSampleBridge.subjectSet.role), "multi-sample third adjacency no longer demonstrates visible social energy");
const foodRefinement = runQuery([
  "refine", "--id", "bright-editorial-food", "--anchor-ref", "ref-bright-editorial-food",
  "--query", "less perfect arrangement, more lived in; hold bright overhead view, colorful ingredients, clear edible texture", "--limit", "4",
], "food refinement disclosures");
check(JSON.stringify(foodRefinement.subjectSet?.requiredLocks) === JSON.stringify(["bright exposure", "vivid ingredient color", "clear ingredient detail", "natural edible texture"]), "food refinement lost literal required locks");
check(foodRefinement.supportingReferences?.every((reference) => reference.alsoDiffers?.length === 2), "food refinement lost viewpoint, light, or depth disclosures");
const machinedRefinement = runQuery([
  "refine", "--id", "sculptural-hard-light-product", "--anchor-ref", "ref-machined-metal-component",
  "--query", "soften the shadows a little but keep the edges and machining marks really clear", "--limit", "4",
], "machined component shadow refinement");
check(JSON.stringify(machinedRefinement.subjectSet?.requiredLocks) === JSON.stringify(["edge definition", "machining texture", "material honesty", "sculptural form"]), "machined refinement lost literal material and form locks");
check(machinedRefinement.supportingReferences?.length === 2 && machinedRefinement.supportingReferences.every((reference) => reference.alsoDiffers?.length === 2), "machined refinement lost support-difference disclosures");
const cyclistRefinement = runQuery([
  "refine", "--id", "rolling-automotive-pan", "--anchor-ref", "ref-urban-cyclist-dusk",
  "--query", "more motion in the background but rider tack sharp; keep dusk; avoid nightclub neon; hold cyclist, bicycle, downtown setting, subdued dusk color", "--limit", "4",
], "cyclist motion refinement");
check(JSON.stringify(cyclistRefinement.subjectSet?.requiredLocks) === JSON.stringify(["rider readability", "cyclist and bicycle", "downtown setting", "dusk", "subdued dusk color"]), "cyclist refinement lost rider, setting, dusk, or color locks");
check(cyclistRefinement.supportingReferences?.length === 2 && cyclistRefinement.supportingReferences.every((reference) => reference.alsoDiffers?.length === 2), "cyclist refinement lost support color or framing disclosures");
check(cyclistRefinement.supportingReferences?.every((reference) => reference.alsoDiffers.some((difference) => /color|night|daylight|fluorescent/.test(difference)) && reference.alsoDiffers.some((difference) => /framing|view|context/.test(difference))), "cyclist refinement no longer names both color and framing differences for every support");
const cyanotypeCombination = runQuery([
  "refine", "--id", "cyanotype-botanical-photogram", "--anchor-ref", "ref-cyanotype-botanical-photogram",
  "--query", "dancer mid-leap with luminous motion trails; hold Prussian-blue field, white contact silhouette, fine botanical branching detail, flat graphic depth",
  "--limit", "4", "--generation-check",
], "cyanotype motion combination");
check(cyanotypeCombination.noSearch === true && !cyanotypeCombination.needsSearch && cyanotypeCombination.subjectSet?.id === "cyanotype-motion-components", "reviewed cyanotype combination must forbid live search");
check(typeof cyanotypeCombination.catalogGap === "string" && cyanotypeCombination.catalogGap === cyanotypeCombination.subjectSet?.catalogGap, "cyanotype combination lost its explicit catalog gap");
const motionComponent = cyanotypeCombination.combinationComponents?.find((reference) => reference.id === "ref-rear-curtain-flash-motion");
check(motionComponent && !/flash|sync/i.test(`${motionComponent.role} ${(motionComponent.alsoDiffers || []).join(" ")}`), "cyanotype motion component exposes an undocumented flash or sync claim");
check(JSON.stringify(cyanotypeCombination.deltas?.slice(0, 3).map((delta) => delta.id)) === JSON.stringify(["light-trails", "subject-motion-blur", "frozen-motion"]), "hold text polluted cyanotype delta ranking");
const unresolvedCombination = runQuery([
  "refine", "--id", "cyanotype-botanical-photogram", "--anchor-ref", "ref-cyanotype-botanical-photogram",
  "--query", "replace the specimen with a mirrored glass skyscraper", "--limit", "4", "--generation-check",
], "unresolved generation check");
check(unresolvedCombination.needsSearch === true && !unresolvedCombination.noSearch && !unresolvedCombination.catalogGap, "unresolved generation check must request one search");
const selectedAnchorReference = "ref-professional-candid-smile";
const refinement = runQuery(["refine", "--id", "approachable-environmental-portrait", "--anchor-ref", selectedAnchorReference, "--query", "more blurred background while holding setting light color texture and human presence", "--limit", "4"], "refinement");
check(refinement.anchor?.id === "approachable-environmental-portrait" && refinement.deltas?.length === 4, "refinement route lost anchor or deltas");
check(refinement.anchor?.references?.length === 1 && refinement.anchor.references[0]?.id === selectedAnchorReference, "refinement replaced the user's exact selected reference with the look lead");
check(refinement.noSearch === true && !refinement.subjectSet?.references && !refinement.subjectSet?.treatmentLookIds, "refinement packet is not compact or catalog-only");
const backgroundBlur = runQuery(["refine", "--id", "approachable-environmental-portrait", "--anchor-ref", "ref-professional-calm-office", "--query", "more blurred background; hold recognizable setting, soft light, natural texture, restrained color, approachable human presence", "--limit", "4"], "background blur locks");
check(backgroundBlur.subjectSet?.requiredLocks?.includes("soft light"), "background-blur packet lost the literal soft-light lock");
check(backgroundBlur.supportingReferences?.every((reference) => reference.alsoDiffers?.length === 2), "background-blur packet lost support-difference disclosure");
const constrainedSoloHomeOfficeRefinement = runQuery([
  "refine", "--id", "task-focused-workplace-portrait", "--anchor-ref", "ref-founder-home-office-work",
  "--query", "founder real working moment; add foreground and background blur; keep one person working in a home office", "--limit", "4",
  "--hard-constraint", "subject-count=single", "--hard-constraint", "setting=home-office", "--hard-constraint", "action=solo-work",
  "--mode", "photographer", "--output", "website hero photograph", "--exclude", "ref-founder-screenprint-work",
], "hard-fit solo home-office refinement");
const constrainedHardFit = constrainedSoloHomeOfficeRefinement.hardFit;
const constrainedEligible = constrainedHardFit?.eligibleCandidates || [];
const constrainedCoverageGap = constrainedHardFit?.coverageGap;
check(constrainedSoloHomeOfficeRefinement.mode === "refine", "hard-fit refine receipt returned the wrong mode");
check(constrainedSoloHomeOfficeRefinement.executionModeStatus === "known" && constrainedSoloHomeOfficeRefinement.executionMode === "a photographer" && constrainedSoloHomeOfficeRefinement.outputContext === "website hero photograph", "hard-fit refine dropped mode or output context");
check(constrainedSoloHomeOfficeRefinement.anchor?.references?.[0]?.id === "ref-founder-home-office-work", "hard-fit refine replaced the exact anchor reference");
check(constrainedSoloHomeOfficeRefinement.needsSearch === true && constrainedSoloHomeOfficeRefinement.noSearch !== true, "incomplete hard-fit refine incorrectly reported noSearch");
check(constrainedSoloHomeOfficeRefinement.subjectSet?.complete === false, "incomplete hard-fit refine was marked complete");
check(JSON.stringify(constrainedEligible.map((reference) => reference.id)) === JSON.stringify(["ref-founder-home-office-work"]), "hard-fit refine changed the eligible candidate IDs");
check(JSON.stringify(constrainedHardFit?.constraints) === JSON.stringify({
  source: "controlled-cli",
  "subject-count": ["single"],
  setting: ["home-office"],
  action: ["solo-work"],
  "excluded-reference": ["ref-founder-screenprint-work"],
}), "hard-fit refine did not preserve the exact controlled constraints");
check(constrainedHardFit?.complete === false && constrainedHardFit?.eligibleTreatmentLookIds?.length === constrainedEligible.length && constrainedHardFit?.eligibleTreatmentLookIds?.length > 0 && constrainedHardFit?.eligibleTreatmentLookIds?.every((id, index) => id === (["task-focused-workplace-portrait"][index])), "hard-fit refine lost nonempty indexed treatment pairing");
check(JSON.stringify(constrainedSoloHomeOfficeRefinement.subjectSet?.treatmentLookIds) === JSON.stringify(constrainedHardFit?.eligibleTreatmentLookIds), "hard-fit refine exposed an ambiguous or mismatched treatment alias");
check(constrainedCoverageGap?.scope === "eligible-candidates" && constrainedCoverageGap.required === 3 && constrainedCoverageGap.found === constrainedEligible.length && constrainedCoverageGap.reason === `only ${constrainedEligible.length} catalog references visibly satisfy all controlled constraints`, "hard-fit refine lost the bounded structural coverage gap");
check(JSON.stringify(constrainedSoloHomeOfficeRefinement.subjectSet?.coverageGap) === JSON.stringify(constrainedCoverageGap), "hard-fit refine did not carry the structural coverage gap into the subject packet");
check(Array.isArray(constrainedHardFit?.missingCoverage) && !constrainedHardFit?.missingCoverage?.some((item) => item.scope === "eligible-candidates"), "structural gap polluted ordinary missingCoverage semantics");
check(constrainedSoloHomeOfficeRefinement.subjectSet?.eligibleCandidates?.every((reference) => reference.fitRole === "eligible-target" && reference.anchorEligible === true), "hard-fit refine lost eligible-target labels");
check(constrainedSoloHomeOfficeRefinement.subjectSet?.traitStudies?.every((reference) => reference.fitRole === "trait-study" && reference.anchorEligible === false && /not an anchor/i.test(reference.traitStudyReason || "")), "hard-fit refine admitted a trait study as an anchor");
check(Array.isArray(constrainedSoloHomeOfficeRefinement.subjectSet?.missingCoverage), "hard-fit refine did not surface missingCoverage");
check((constrainedSoloHomeOfficeRefinement.subjectSet?.treatmentLookIds || []).every((id) => id === "task-focused-workplace-portrait"), "hard-fit refine returned an unpaired treatment");
check(!constrainedSoloHomeOfficeRefinement.supportingReferences || constrainedSoloHomeOfficeRefinement.supportingReferences.length === 0, "incomplete hard-fit refine returned incompatible supporting references");
check((constrainedSoloHomeOfficeRefinement.supportingReferences || []).every((reference) => constrainedEligible.some((candidate) => candidate.id === reference.id)), "hard-fit refine returned an incompatible supporting reference");
check((constrainedHardFit?.exclusions || []).some((item) => item.referenceId === "ref-founder-screenprint-work" && /explicit reference exclusion/i.test(item.reason || "")), "hard-fit refine did not preserve --exclude evidence");
const constrainedReturnedReferenceIds = [
  ...(constrainedSoloHomeOfficeRefinement.subjectSet?.references || []),
  ...(constrainedSoloHomeOfficeRefinement.subjectSet?.eligibleCandidates || []),
  ...(constrainedSoloHomeOfficeRefinement.subjectSet?.traitStudies || []),
  ...(constrainedSoloHomeOfficeRefinement.supportingReferences || []),
].map((reference) => reference.id);
check(!constrainedReturnedReferenceIds.includes("ref-founder-screenprint-work"), "hard-fit refine returned an explicitly excluded reference");
check(constrainedSoloHomeOfficeRefinement.deltas?.every((delta) => !Object.hasOwn(delta, "references")), "incomplete hard-fit refine returned unrelated delta image references");
const backwardCompatibleProfile = runQuery(["profile", "--id", "luxury-still-life-polish"], "backward-compatible profile");
check(backwardCompatibleProfile.look?.id === "luxury-still-life-polish" && backwardCompatibleProfile.look?.locked && backwardCompatibleProfile.look?.adapt && backwardCompatibleProfile.executionModeStatus === "unknown" && !backwardCompatibleProfile.executionMode, "backward-compatible profile route is incomplete");
const explicitAi = runQuery(["looks", "--query", "hazy quiet lake remembered not tourism", "--mode", "ai", "--output", "reusable generated image", "--limit", "5"], "explicit AI execution context");
check(explicitAi.executionModeStatus === "known" && explicitAi.executionMode === "AI generation" && explicitAi.outputContext === "reusable generated image", "explicit AI mode or output was dropped from the choice packet");
const credibleWorkingPortrait = runQuery(["looks", "--query", "three bright credible working portraits real texture readable workplace setting environmental portrait natural human presence", "--limit", "5"], "credible working portrait phrase boundary");
check(credibleWorkingPortrait.subjectSet?.id === "approachable-portrait" && credibleWorkingPortrait.subjectSet?.complete && credibleWorkingPortrait.results?.every((item) => !item.id.includes("food")), "credible falsely matched edible or lost the portrait route");
const constrainedSoloHomeOffice = runQuery([
  "looks", "--query", "one person working from a home office, no team, no group, real working moment", "--limit", "5",
  "--hard-constraint", "subject-count=single", "--hard-constraint", "setting=home-office", "--hard-constraint", "action=solo-work",
], "hard-fit solo home-office constraints");
check(constrainedSoloHomeOffice.noSearch !== true && constrainedSoloHomeOffice.needsSearch === true, "explicit solo home-office constraints incorrectly returned complete/noSearch");
check(constrainedSoloHomeOffice.subjectSet?.id !== "team-at-work" || constrainedSoloHomeOffice.subjectSet?.complete !== true, "solo home-office constraints returned team-at-work as a complete subject set");
check(constrainedSoloHomeOffice.hardFit?.complete === false && constrainedSoloHomeOffice.hardFit?.eligibleCandidates?.length < 3, "solo home-office hard fit did not require three eligible candidates");
check(constrainedSoloHomeOffice.subjectSet?.eligibleCandidates?.every((reference) => reference.fitRole === "eligible-target" && reference.anchorEligible === true), "eligible solo home-office references were not labeled as target candidates");
check(constrainedSoloHomeOffice.subjectSet?.traitStudies?.every((reference) => reference.fitRole === "trait-study" && reference.anchorEligible === false && /not an anchor/i.test(reference.traitStudyReason || "")), "analogical references were not labeled as non-anchor trait studies");
check((constrainedSoloHomeOffice.subjectSet?.traitStudies || []).every((reference) => reference.credit || reference.id !== "ref-team-project-meeting"), "trait-study reference lost its required credit");
check(constrainedSoloHomeOffice.results?.length === constrainedSoloHomeOffice.hardFit?.eligibleCandidates?.length, "incomplete hard-fit route padded results beyond eligible targets");
check(constrainedSoloHomeOffice.results?.every((result) => constrainedSoloHomeOffice.hardFit?.eligibleTreatmentLookIds?.includes(result.id)), "incomplete hard-fit route returned an unpaired treatment");
const zeroScoreHardFit = runQuery([
  "looks", "--query", "completely unrelated astronomy taxonomy", "--limit", "5",
  "--hard-constraint", "subject-count=single", "--hard-constraint", "setting=home-office", "--hard-constraint", "action=solo-work",
], "hard-fit zero-score subject query");
check(zeroScoreHardFit.needsSearch === true && zeroScoreHardFit.noSearch !== true, "zero-score hard-fit subject query did not request search");
check(!zeroScoreHardFit.subjectSet && (zeroScoreHardFit.hardFit?.missingCoverage || []).some((item) => item.scope === "query"), "zero-score hard-fit subject query lacked query-scope missing coverage");
check((zeroScoreHardFit.hardFit?.eligibleCandidates || []).length === 0 && (zeroScoreHardFit.results || []).length === 0, "zero-score hard-fit subject query borrowed a setting/person target or padded result");
const unflaggedExplicitRed = runQuery([
  "looks", "--query", "one person working from a home office, no team, no group, real working moment", "--limit", "5",
], "unflagged explicit red constraints");
check(unflaggedExplicitRed.noSearch !== true && unflaggedExplicitRed.subjectSet?.id !== "team-at-work", "explicit negative team/group wording still returned team-at-work complete/noSearch");
const constrainedGroupWork = runQuery([
  "looks", "--query", "team at work people collaborating in office meeting", "--limit", "5",
  "--hard-constraint", "subject-count=group", "--hard-constraint", "setting=office", "--hard-constraint", "action=group-work",
], "hard-fit ordinary group work constraints");
check(constrainedGroupWork.noSearch === true && constrainedGroupWork.needsSearch !== true && constrainedGroupWork.subjectSet?.id === "team-at-work", "ordinary group-work constraints lost their complete no-search route");
check(constrainedGroupWork.hardFit?.eligibleCandidates?.length === 3 && constrainedGroupWork.hardFit?.eligibleCandidates?.every((reference) => reference.fitRole === "eligible-target"), "group-work hard fit did not return three eligible target candidates");
check((constrainedGroupWork.hardFit?.missingCoverage || []).length === 0, "group-work hard fit reported unexpected missing coverage");
const constrainedGroupWorkLimited = runQuery([
  "looks", "--query", "team at work people collaborating in office meeting", "--limit", "1",
  "--hard-constraint", "subject-count=group", "--hard-constraint", "setting=office", "--hard-constraint", "action=group-work",
], "hard-fit limit");
check(constrainedGroupWorkLimited.noSearch === true && constrainedGroupWorkLimited.results?.length === 1, "hard-fit route ignored --limit 1");
check(constrainedGroupWorkLimited.results?.[0]?.id === constrainedGroupWorkLimited.hardFit?.eligibleTreatmentLookIds?.[0], "hard-fit --limit result lost indexed target pairing");
const constrainedUnknownCoverage = runQuery([
  "looks", "--query", "quiet misty lake shoreline landscape", "--limit", "5", "--hard-constraint", "subject-count=single",
], "hard-fit missing visible coverage");
check(constrainedUnknownCoverage.needsSearch === true && constrainedUnknownCoverage.noSearch !== true && (constrainedUnknownCoverage.hardFit?.missingCoverage || []).length === 3, "unknown visible fit was guessed instead of reported as missing coverage");
check((constrainedUnknownCoverage.hardFit?.missingCoverage || []).every((item) => /unknown|not inferred/i.test(item.reason || "")), "missing coverage did not explain the unknown-fit boundary");
check((constrainedUnknownCoverage.results || []).length === 0, "incomplete unknown-coverage hard-fit route padded generic treatments");
const excludedGroupTraits = runQuery([
  "looks", "--query", "team at work people collaborating in office meeting", "--limit", "5",
  "--hard-constraint", "subject-count=group", "--hard-constraint", "setting=office", "--hard-constraint", "action=group-work", "--exclude-trait", "group-work",
], "hard-fit excluded traits");
check(excludedGroupTraits.noSearch !== true && excludedGroupTraits.needsSearch === true, "explicitly excluded group-work trait was admitted as complete");
check((excludedGroupTraits.hardFit?.eligibleCandidates || []).length === 0 && (excludedGroupTraits.hardFit?.traitStudies || []).length === 0 && (excludedGroupTraits.hardFit?.exclusions || []).length === 3, "excluded group-work references were not blocked and recorded");
check((excludedGroupTraits.hardFit?.exclusions || []).every((item) => /excluded trait: group-work/.test(item.reason || "")), "excluded trait reason was not carried explicitly");
check((excludedGroupTraits.results || []).length === 0, "excluded hard-fit route padded generic treatments");
const industrialMachinery = runQuery(["looks", "--query", "people working with industrial machinery; workers and machines equally present; moody gritty documentary realism; natural texture; restrained color; avoid fake cinematic lighting, teal-orange grading, staged hero shots, excessive haze", "--limit", "5"], "industrial machinery route priority");
check(industrialMachinery.noSearch === true && industrialMachinery.subjectSet?.id === "industrial-workplace" && industrialMachinery.subjectSet?.complete, "industrial machinery query drifted into a generic team packet");
check(JSON.stringify(industrialMachinery.subjectSet?.references?.map((reference) => reference.id)) === JSON.stringify(["ref-industrial-workplace-documentary", "ref-industrial-human-machine-portrait", "ref-industrial-color-production-reportage"]), "industrial machinery query changed curated industrial references");
const aiProfile = runQuery(["profile", "--id", "overcast-minimal-landscape", "--mode", "ai", "--output", "reusable generated image"], "AI profile context");
check(aiProfile.executionModeStatus === "known" && aiProfile.executionMode === "AI generation" && aiProfile.outputContext === "reusable generated image" && aiProfile.look?.id === "overcast-minimal-landscape", "profile route dropped explicit AI mode or output");
const anchoredAiProfile = runQuery(["profile", "--id", "overcast-minimal-landscape", "--anchor-ref", "ref-misty-lake-rocky-shore", "--mode", "ai"], "anchored AI profile");
check(JSON.stringify(anchoredAiProfile.look?.references?.map((reference) => reference.id)) === JSON.stringify(["ref-misty-lake-rocky-shore"]), "profile route replaced the selected approved reference");
const selfShootPacket = runQuery(["looks", "--query", "professional approachable self portrait at home window", "--mode", "self-shoot", "--output", "vertical profile image", "--limit", "5"], "self-shoot execution context");
check(selfShootPacket.executionModeStatus === "known" && selfShootPacket.executionMode === "self-shooting" && selfShootPacket.outputContext === "vertical profile image", "self-shoot mode or output was dropped from the choice packet");
const selfShootAlias = runQuery(["profile", "--id", "approachable-environmental-portrait", "--mode", "self-shooting"], "self-shoot mode alias");
check(selfShootAlias.executionModeStatus === "known" && selfShootAlias.executionMode === "self-shooting", "self-shooting mode alias is not accepted");

if (errors.length) {
  console.error(`Photography Director validation failed (${errors.length}):`);
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

const remoteImages = references.filter((reference) => reference.displayMode === "authorized-remote").length;
console.log(`Photography Director valid: ${looks.length} looks, ${axisValues.length} axis values, ${actualImages.length} bundled and ${remoteImages} remote references.`);
