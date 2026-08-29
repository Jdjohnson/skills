#!/usr/bin/env python3
"""Validate David Deutsch corpus structure and provenance invariants."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "references" / "corpus"
PRIMARY_TIERS = {"P1-C", "P1-S", "P1-J", "P2", "P3"}
REPRESENTATIONS = {
    "quotation", "faithful-paraphrase", "editorial-synthesis", "editorial-application",
    "external-position", "unresolved-interpretation",
}
REL_TYPES = {
    "addresses", "depends_on", "argues_for", "argues_against", "qualifies", "exemplifies",
    "distinguishes_from", "refines", "supersedes", "tension_with", "credits_to", "endorses",
    "rejects", "reformulates", "co_develops", "reported_intellectual_source",
    "historically_influenced", "logically_entails", "motivates", "publicly_argues_for",
    "our_synthesis_connects",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def origin_ok(origin: dict, where: str, errors: list[str]) -> None:
    representation = origin.get("representation")
    if representation not in REPRESENTATIONS:
        errors.append(f"{where}: invalid origin representation")
    represents = origin.get("represents")
    if representation in {"editorial-synthesis", "editorial-application", "unresolved-interpretation"} and represents == "david-deutsch":
        errors.append(f"{where}: editorial material may not represent David Deutsch")


def refs_ok(refs: list, where: str, sources: dict, errors: list[str]) -> None:
    if not isinstance(refs, list):
        errors.append(f"{where}: source_refs must be an array")
        return
    for index, ref in enumerate(refs):
        label = f"{where}.source_refs[{index}]"
        source_id = ref.get("source_id")
        if source_id not in sources:
            errors.append(f"{label}: unknown source_id {source_id}")
            continue
        if not str(ref.get("locator", "")).strip():
            errors.append(f"{label}: precise locator required")
        if ref.get("verification") != "checked":
            errors.append(f"{label}: active evidence must be checked")
        excerpt = ref.get("excerpt")
        if excerpt and len(str(excerpt).split()) > 25:
            errors.append(f"{label}: excerpt exceeds 25-word package limit")


def validate() -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    sources_doc = load(CORPUS / "sources.json")
    domains_doc = load(CORPUS / "domains.json")
    source_rows = sources_doc.get("sources", [])
    sources = {row.get("source_id"): row for row in source_rows}
    if None in sources or len(sources) != len(source_rows):
        errors.append("sources.json: duplicate or missing source_id")
    for source_id, row in sources.items():
        for field in ("title", "source_tier", "source_type", "contributors", "dates", "locations", "authority", "rights", "audit"):
            if field not in row:
                errors.append(f"{source_id}: missing source field {field}")
        integrity = row.get("integrity", {})
        if not integrity.get("algorithm") or not integrity.get("covers") or not integrity.get("checked"):
            errors.append(f"{source_id}: source manifestation integrity record required")
        if row.get("locations", {}).get("private") and integrity.get("algorithm") == "sha256":
            digest = str(integrity.get("digest", ""))
            if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest.lower()):
                errors.append(f"{source_id}: invalid sha256 manifestation digest")
        if row.get("audit", {}).get("record_status") == "active" and row.get("source_tier") == "U0":
            errors.append(f"{source_id}: U0 source cannot be active")
        if row.get("rights", {}).get("storage_mode") not in {"metadata_only", "short_excerpt", "public_pointer"}:
            errors.append(f"{source_id}: invalid storage_mode")

    allowed_domains = set(domains_doc.get("domains", []))
    allowed_levels = set(domains_doc.get("explanation_levels", []))
    allowed_jobs = set(domains_doc.get("reasoning_jobs", []))
    if not allowed_domains or not allowed_levels or not allowed_jobs:
        errors.append("domains.json: domains, explanation_levels, and reasoning_jobs must be non-empty")

    schema = load(CORPUS / "schema.json")
    cluster_required = set(schema.get("required", []))
    record_required = set(schema.get("$defs", {}).get("record", {}).get("required", []))
    claim_required = record_required | set(schema.get("$defs", {}).get("claim", {}).get("required", []))
    argument_required = record_required | set(schema.get("$defs", {}).get("argument", {}).get("required", []))
    relationship_required = set(schema.get("$defs", {}).get("relationship", {}).get("required", []))
    boundaries_required = set(schema.get("$defs", {}).get("boundaries", {}).get("required", []))

    ids: dict[str, str] = {}
    id_kinds: dict[str, str] = {}
    lineages: dict[str, list[tuple[int, str, str]]] = defaultdict(list)
    clusters = []
    for path in sorted((CORPUS / "clusters").glob("*.json")):
        try:
            cluster = load(path)
        except json.JSONDecodeError as error:
            errors.append(f"{path.name}: invalid JSON: {error}")
            continue
        clusters.append(cluster)
        cid = cluster.get("cluster_id")
        where = path.name
        missing_cluster_fields = sorted(cluster_required - set(cluster))
        if missing_cluster_fields:
            errors.append(f"{where}: schema-required fields missing: {missing_cluster_fields}")
        if cid != path.stem:
            errors.append(f"{where}: cluster_id must match filename")
        if cluster.get("status") not in {"active", "candidate", "quarantined"}:
            errors.append(f"{where}: invalid status")
        if cluster.get("application_policy", "lens") not in {"lens", "source-only"}:
            errors.append(f"{where}: invalid application_policy")
        if not set(cluster.get("domains", [])) <= allowed_domains:
            errors.append(f"{where}: unknown domain")
        if not set(cluster.get("explanation_levels", [])) <= allowed_levels:
            errors.append(f"{where}: unknown explanation level")
        problem = cluster.get("problem", {})
        routing = problem.get("routing", {})
        if not str(problem.get("summary", "")).strip():
            errors.append(f"{where}: problem summary required")
        if cluster.get("status") == "active" and not routing.get("structural_predicates"):
            errors.append(f"{where}: active cluster requires structural predicates")
        if not set(routing.get("reasoning_jobs", [])) <= allowed_jobs:
            errors.append(f"{where}: unknown reasoning job")
        if cluster.get("status") == "active" and not cluster.get("boundaries", {}).get("misreadings"):
            errors.append(f"{where}: active cluster requires misreadings")
        if cluster.get("status") == "active" and not cluster.get("criticisms"):
            errors.append(f"{where}: active cluster requires criticism or qualification")
        missing_boundary_fields = sorted(boundaries_required - set(cluster.get("boundaries", {})))
        if missing_boundary_fields:
            errors.append(f"{where}: schema-required boundary fields missing: {missing_boundary_fields}")
        for source_id in cluster.get("source_routes", []):
            if source_id not in sources:
                errors.append(f"{where}: unknown source route {source_id}")

        records = [("problem", problem)]
        for field in ("definitions", "claims", "arguments", "examples", "criticisms"):
            value = cluster.get(field, [])
            if not isinstance(value, list):
                errors.append(f"{where}: {field} must be an array")
                continue
            kind = {"definitions": "definition", "claims": "claim", "arguments": "argument", "examples": "example", "criticisms": "criticism"}[field]
            records.extend((kind, record) for record in value)
        local_ids = set()
        for kind, record in records:
            record_id = record.get("id")
            if not record_id:
                errors.append(f"{where}: record missing id")
                continue
            if record_id in ids:
                errors.append(f"duplicate id {record_id}: {ids[record_id]} and {where}")
            ids[record_id] = where
            id_kinds[record_id] = kind
            local_ids.add(record_id)
            required = claim_required if kind == "claim" else argument_required if kind in {"argument", "criticism"} else record_required
            missing_record_fields = sorted(required - set(record))
            if missing_record_fields:
                errors.append(f"{where}:{record_id}: schema-required fields missing: {missing_record_fields}")
            origin = record.get("origin", {})
            origin_ok(origin, f"{where}:{record_id}", errors)
            refs = record.get("source_refs", [])
            refs_ok(refs, f"{where}:{record_id}", sources, errors)
            if origin.get("representation") in {"quotation", "faithful-paraphrase"}:
                if not refs:
                    errors.append(f"{where}:{record_id}: sourced representation requires evidence")
                for ref in refs:
                    source = sources.get(ref.get("source_id"), {})
                    if source.get("source_tier") not in PRIMARY_TIERS:
                        errors.append(f"{where}:{record_id}: Deutsch paraphrase must use primary evidence")
            lineage = record.get("lineage")
            version = record.get("version")
            lifecycle = record.get("lifecycle", "active")
            if cluster.get("status") == "active" and lifecycle not in {"active", "superseded", "retired"}:
                errors.append(f"{where}:{record_id}: invalid runtime lifecycle")
            if lineage and isinstance(version, int):
                lineages[lineage].append((version, lifecycle, record_id))

        for argument in [*cluster.get("arguments", []), *cluster.get("criticisms", [])]:
            if not argument.get("conclusions"):
                errors.append(f"{where}:{argument.get('id')}: argument requires conclusions")
            for target in argument.get("conclusions", []):
                if target not in local_ids:
                    errors.append(f"{where}:{argument.get('id')}: unresolved conclusion {target}")

        seen_symmetric = set()
        for rel in cluster.get("relationships", []):
            rel_id = rel.get("id")
            if not rel_id:
                errors.append(f"{where}: relationship missing id")
                continue
            if rel_id in ids:
                errors.append(f"duplicate id {rel_id}: {ids[rel_id]} and {where}")
            ids[rel_id] = where
            missing_relationship_fields = sorted(relationship_required - set(rel))
            if missing_relationship_fields:
                errors.append(f"{where}:{rel_id}: schema-required fields missing: {missing_relationship_fields}")
            if rel.get("type") not in REL_TYPES:
                errors.append(f"{where}:{rel_id}: invalid relationship type")
            if rel.get("from") not in local_ids or rel.get("to") not in local_ids:
                errors.append(f"{where}:{rel_id}: unresolved endpoint")
            endpoint_contracts = {
                "addresses": ({"claim"}, {"problem"}),
                "argues_for": ({"argument"}, {"claim"}),
                "argues_against": ({"argument", "criticism"}, {"claim"}),
                "qualifies": ({"criticism", "claim"}, {"claim"}),
            }
            if rel.get("type") in endpoint_contracts:
                allowed_from, allowed_to = endpoint_contracts[rel["type"]]
                if id_kinds.get(rel.get("from")) not in allowed_from or id_kinds.get(rel.get("to")) not in allowed_to:
                    errors.append(f"{where}:{rel_id}: invalid endpoint types for {rel.get('type')}")
            origin_ok(rel.get("origin", {}), f"{where}:{rel_id}", errors)
            refs_ok(rel.get("source_refs", []), f"{where}:{rel_id}", sources, errors)
            if not rel.get("source_refs") and rel.get("origin", {}).get("representation") != "editorial-synthesis":
                errors.append(f"{where}:{rel_id}: relationship needs source evidence or Skill-owned synthesis")
            if rel.get("type") in {"distinguishes_from", "tension_with"}:
                key = (rel.get("type"), *sorted((str(rel.get("from")), str(rel.get("to")))))
                if key in seen_symmetric:
                    errors.append(f"{where}:{rel_id}: duplicate symmetric relationship")
                seen_symmetric.add(key)

    for lineage, versions in lineages.items():
        active = [item for item in versions if item[1] == "active"]
        if len(active) > 1:
            errors.append(f"lineage {lineage}: multiple active versions")

    active_cluster_ids = {cluster.get("cluster_id") for cluster in clusters if cluster.get("status") == "active"}
    graph = load(CORPUS / "worldview-graph.json")
    graph_nodes = set(graph.get("nodes", []))
    if graph_nodes != active_cluster_ids:
        missing = sorted(active_cluster_ids - graph_nodes)
        extra = sorted(graph_nodes - active_cluster_ids)
        errors.append(f"worldview-graph.json: nodes must equal active clusters; missing={missing}, extra={extra}")
    worldview_edge_ids = set()
    for edge in graph.get("edges", []):
        edge_id = edge.get("id")
        where = "worldview-graph.json"
        if not edge_id or edge_id in worldview_edge_ids or edge_id in ids:
            errors.append(f"{where}: duplicate or missing edge id {edge_id}")
            continue
        worldview_edge_ids.add(edge_id)
        ids[edge_id] = where
        if edge.get("type") not in REL_TYPES:
            errors.append(f"{where}:{edge_id}: invalid relationship type")
        source = edge.get("from_cluster")
        target = edge.get("to_cluster")
        if source not in graph_nodes or target not in graph_nodes:
            errors.append(f"{where}:{edge_id}: unresolved cluster endpoint")
        if source == target:
            errors.append(f"{where}:{edge_id}: self-relationship is not allowed")
        if not str(edge.get("summary", "")).strip():
            errors.append(f"{where}:{edge_id}: summary required")
        if not edge.get("routing_signals"):
            errors.append(f"{where}:{edge_id}: routing_signals required")
        origin_ok(edge.get("origin", {}), f"{where}:{edge_id}", errors)
        refs_ok(edge.get("source_refs", []), f"{where}:{edge_id}", sources, errors)
        if not edge.get("source_refs") and edge.get("origin", {}).get("representation") != "editorial-synthesis":
            errors.append(f"{where}:{edge_id}: relationship needs source evidence or Skill-owned synthesis")

    bridge_ids = set()
    active_bridge_ids = set()
    candidate_bridge_ids = set()
    for path in sorted((CORPUS / "bridges").glob("*.json")):
        bridge = load(path)
        bridge_id = bridge.get("id")
        if not bridge_id or bridge_id in bridge_ids:
            errors.append(f"{path.name}: duplicate or missing bridge id")
        bridge_ids.add(bridge_id)
        if bridge.get("status") == "active":
            active_bridge_ids.add(bridge_id)
        elif bridge.get("status") == "candidate":
            candidate_bridge_ids.add(bridge_id)
        else:
            errors.append(f"{path.name}: invalid bridge status")
        origin_ok(bridge.get("origin", {}), path.name, errors)
        for field in ("source_claims", "target_problem", "structural_correspondence", "warrant", "target_evidence", "disanalogies", "failure_conditions", "resulting_claims"):
            value = bridge.get(field)
            if value in (None, "", []):
                errors.append(f"{path.name}: bridge requires {field}")
        if not bridge.get("routing_signals"):
            errors.append(f"{path.name}: active or candidate bridge requires routing_signals")
        if bridge.get("status") == "active" and bridge.get("origin", {}).get("representation") != "editorial-application":
            errors.append(f"{path.name}: active bridge must be Skill-owned editorial application")
        for claim_id in bridge.get("source_claims", []):
            if claim_id not in ids:
                errors.append(f"{path.name}: unresolved source claim {claim_id}")
        if not set(bridge.get("source_context", {}).get("domains", [])) <= allowed_domains:
            errors.append(f"{path.name}: unknown source-context domain")
        if not set(bridge.get("target_context", {}).get("domains", [])) <= allowed_domains:
            errors.append(f"{path.name}: unknown target-context domain")

    forbidden = [path for path in ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".pdf", ".epub", ".mobi"}]
    if forbidden:
        errors.append("copyright-heavy files found in package: " + ", ".join(str(path.relative_to(ROOT)) for path in forbidden))
    if len(clusters) < 12:
        warnings.append("corpus has fewer than 12 clusters; review worldview coverage")

    counts = {
        "sources": len(sources),
        "clusters": len(clusters),
        "records_and_relationships": len(ids),
        "worldview_edges": len(worldview_edge_ids),
        "active_bridges": len(active_bridge_ids),
        "candidate_bridges": len(candidate_bridge_ids),
        "bridges": len(bridge_ids),
    }
    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "counts": counts,
    }


def main() -> int:
    try:
        result = validate()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["ok"] else 1
    except (OSError, KeyError, json.JSONDecodeError) as error:
        print("error: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
