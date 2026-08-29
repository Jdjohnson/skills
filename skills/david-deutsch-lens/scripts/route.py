#!/usr/bin/env python3
"""Deterministic, policy-aware router for David Deutsch argument packets."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "references" / "corpus"
CLUSTERS = CORPUS / "clusters"
BRIDGES = CORPUS / "bridges"

STOP = set(
    "a an and are as at be been being but by can could did do does for from had has have "
    "having how i if in into is it its may might more most must my need needs of on or our "
    "should so than that the their them then there these they this those to want we what when "
    "where which while who will with would you your help use using tell give make think about "
    "no not without because cannot deutsch source sourced"
    .split()
)

CANON = {
    "explanatory": "explanation", "explanations": "explanation", "explain": "explanation",
    "predictions": "prediction", "predicted": "prediction", "critique": "criticism",
    "criticize": "criticism", "criticise": "criticism", "errors": "error",
    "mistakes": "error", "fallible": "fallibilism", "optimistic": "optimism",
    "problems": "problem", "solutions": "solution", "universal": "universality",
    "creative": "creativity", "create": "creativity", "cultures": "culture",
    "institutions": "institution", "organizations": "organization",
    "organisations": "organization", "companies": "business", "company": "business",
    "firms": "business", "multiversal": "multiverse", "computers": "computation",
    "computing": "computation", "algorithms": "computation", "evolutionary": "evolution",
    "evolve": "evolution", "memes": "meme", "societies": "society",
    "decisions": "decision", "choices": "decision", "options": "option", "ai": "agi",
    "llms": "agi", "intelligence": "agi", "bayesianism": "bayesian",
    "bayes": "bayesian", "fallibilist": "fallibilism", "causation": "causal",
    "causes": "causal", "correcting": "correction", "allocation": "allocate",
}

APPLICATION_JOBS = {
    "diagnose", "generate-conjectures", "compare-alternatives", "design-error-correction",
    "evaluate-progress", "assess-transfer", "decide",
}
PRACTICAL_DOMAINS = {"organizations", "finance", "medicine", "law", "relationships", "politics", "morality", "aesthetics", "education", "artificial-intelligence"}
HIGH_STAKES = {
    "medical": ("chest pain", "doctor", "diagnosis", "medication", "emergency", "symptom", "insulin", "chemotherapy", "left arm", "jaw pain"),
    "financial": ("savings", "investment", "invest", "portfolio", "bet", "retirement", "401k", "home-equity", "annuity"),
    "legal": ("lawsuit", "legal advice", "criminal", "contract law", "immigration status", "subpoena"),
    "safety": ("danger", "unsafe", "suicide", "self-harm", "weapon", "emergency"),
}
GLOBAL_DECLINES = {
    "irrelevant-preference": ("kitchen cabinet", "kitchen cabinets", "blue or green", "navy or sage", "tacos or sushi", "for dinner", "paint color", "paint colour"),
    "technical-diagnosis": ("slow sql", "query plan", "database index", "stack trace"),
}
IMPERSONATION = ("pretend you are david deutsch", "answer as david deutsch", "speak as david deutsch", "impersonate deutsch", "in deutsch's voice", "in deutsch’s voice", "first person as deutsch", "persona-based")
CURRENT_VIEW = ("what does deutsch think now", "what would deutsch say", "in 2026", "today's llm", "todays llm")
QUOTE_OR_SOURCE = ("quote", "cite", "passage", "exact wording", "page number", "which page", "paper titled", "did deutsch say", "introduced in", "already defines", "in the fabric of reality", "authorship", "coauthor", "co-authored", "sole-authored", "solo theorem", "wrote,", "wrote '", 'wrote "', "may be invented", "requested chronology", "authenticate", "verify an alleged", "repeat the wording", "verbatim")
TECHNICAL = ("quantum", "multiverse", "constructor theory", "turing principle", "quantum computer")
TRANSFER_TARGET = ("business", "company", "team", "agency", "margin", "startup", "career", "investment", "management", "employee", "marketing", "relationship", "medical", "political", "policy")
ACTIONABLE_DIAGNOSIS = ("should i fire", "should we fire", "diagnose this employee", "diagnose this person", "fire the employee", "fire her", "recommend termination", "terminate my direct report", "dismiss dissenters")
CURRENT_POLITICS = ("which candidate", "who should i vote", "who would he vote")
URGENT_MEDICAL = ("crushing chest pain", "severe chest pain", "can't breathe", "cannot breathe", "left arm and jaw", "pressure is spreading", "stop insulin", "skip chemotherapy")
OVERCLAIM = ("proved", "proves", "confirmed it", "settled result", "proof claim", "established beyond dispute")
TASTE_ORACLE_TARGETS = ("brand name", "brand names", "logo", "design", "paint", "color", "colour", "which looks better")
DECISION_WORDS = ("choose", "select", "rank", "pick", "decide", "best")
UNRELEASED_ROUTES = {
    "bayesianism": ("bayesian", "bayesianism"),
    "taking-children-seriously": ("taking children seriously", "tcs parenting", "coercive parenting"),
    "quantum-decision-theory": ("quantum decision theory",),
}
BAD_EVIDENCE = {"none", "n/a", "na", "unknown", "deutsch says so", "because deutsch says so"}
ACTIVE_BRIDGE_ROUTE_BONUS = 12.0


def read_json(path: str) -> dict:
    raw = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("input must be a JSON object")
    return value


def load_clusters() -> list[dict]:
    rows = []
    for path in sorted(CLUSTERS.glob("*.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        if value.get("status") == "active":
            value["_path"] = str(path.relative_to(ROOT))
            value["_claim_ids"] = [claim["id"] for claim in value.get("claims", [])]
            rows.append(value)
    if not rows:
        raise ValueError("no active clusters")
    return rows


def load_domains() -> dict:
    return json.loads((CORPUS / "domains.json").read_text(encoding="utf-8"))


def load_graph() -> dict:
    return json.loads((CORPUS / "worldview-graph.json").read_text(encoding="utf-8"))


def load_bridges() -> list[dict]:
    rows = []
    for path in sorted(BRIDGES.glob("*.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        if value.get("status") == "active":
            value["_path"] = str(path.relative_to(ROOT))
            rows.append(value)
    return rows


def tokens(value: object) -> set[str]:
    text = " ".join(str(item) for item in value) if isinstance(value, list) else str(value or "")
    output = set()
    for word in re.findall(r"[a-z]+", text.lower().replace("&", " and ")):
        word = CANON.get(word, word)
        if len(word) > 4 and word.endswith("s") and not word.endswith("ss"):
            word = word[:-1]
        word = CANON.get(word, word)
        if len(word) > 1 and word not in STOP:
            output.add(word)
    return output


def normalize_label(value: str) -> str:
    text = value.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", " ", text)
    text = re.sub(r"\b(vs|versus)\b", "and", text)
    text = text.replace("-", " ")
    words = [CANON.get(word, word) for word in text.split()]
    while words and words[0] in {"a", "an", "the"}:
        words.pop(0)
    return " ".join(words)


def phrase_present(text: str, phrases: tuple[str, ...] | list[str]) -> bool:
    """Match whole phrases so a trigger such as `bet` does not match `better`."""
    for phrase in phrases:
        pattern = r"(?<![a-z0-9])" + re.escape(phrase.lower()).replace(r"\ ", r"\s+") + r"(?![a-z0-9])"
        if re.search(pattern, text.lower()):
            return True
    return False


def guardrails(text: str, stakes: str, domains: list[str], target_domains: set[str]) -> tuple[list[str], list[str], bool]:
    warnings: list[str] = []
    flags: list[str] = []
    lower = text.lower()
    elevated = stakes == "elevated"
    domain_category = {"medicine": "medical", "finance": "financial", "law": "legal"}
    for domain, category in domain_category.items():
        if domain in domains:
            elevated = True
            flags.append(category)
    for category, phrases in HIGH_STAKES.items():
        if phrase_present(lower, phrases):
            elevated = True
            flags.append(category)
    if elevated:
        warnings.append("High-stakes boundary: current domain evidence and appropriate expertise control; the Deutsch lens may not delay or displace them.")
    if phrase_present(lower, IMPERSONATION):
        flags.append("impersonation")
        warnings.append("Do not impersonate Deutsch or invent his present view; use dated third-person source reporting only.")
    if phrase_present(lower, CURRENT_VIEW):
        flags.append("current-view")
        warnings.append("Current-view boundary: state only what dated audited sources establish unless current primary evidence is checked.")
    if phrase_present(lower, QUOTE_OR_SOURCE):
        flags.append("verification")
        warnings.append("Quotation/source boundary: authenticate the work, wording, authorship, chronology, and locator before quoting or attributing.")
    if phrase_present(lower, TECHNICAL) and target_domains:
        flags.append("cross-domain-technical-transfer")
        warnings.append("Cross-domain boundary: technical physics or computation may not supply target-domain evidence or a recommendation.")
    if phrase_present(lower, ACTIONABLE_DIAGNOSIS):
        flags.append("actionable-person-diagnosis")
        warnings.append("Do not diagnose or make personnel action from meme, static-society, or anti-rational labels; use ordinary organizational evidence.")
    if any(phrase_present(lower, (phrase,)) and not phrase_is_negated(lower, phrase) for phrase in CURRENT_POLITICS):
        flags.append("current-politics")
        warnings.append("Do not invent a candidate endorsement; separate the sourced institutional criterion from current political analysis.")
    if phrase_present(lower, URGENT_MEDICAL):
        flags.append("urgent-medical")
        warnings.append("Urgent medical action controls: seek emergency assessment now; philosophical analysis must not create delay.")
    if phrase_present(lower, OVERCLAIM):
        flags.append("epistemic-overclaim")
        warnings.append("Epistemic-status boundary: distinguish definition, conjecture, proposed principle, argument, conditional result, experiment, and consensus.")
    return warnings, flags, elevated


def phrase_is_negated(text: str, phrase: str) -> bool:
    escaped = re.escape(phrase.lower()).replace(r"\ ", r"\s+")
    return bool(re.search(r"\b(?:not|isn['’]t|is\s+not|unrelated\s+to)\s+(?:a\s+|about\s+)?" + escaped + r"\b", text.lower()))


def infer_target_domains(explicit: list[str], text: str) -> set[str]:
    target = set(explicit) & PRACTICAL_DOMAINS
    mapping = {
        "organizations": ("organization", "business", "company", "team", "agency", "handoff", "process", "sales", "rebrand", "employee", "startup", "career", "job offer"),
        "finance": ("investment", "portfolio", "margin", "savings", "retirement"),
        "medicine": ("medical", "doctor", "symptom", "medication", "chest pain"),
        "law": ("legal", "lawsuit", "contract law", "subpoena"),
        "relationships": ("relationship", "partner", "marriage"),
        "politics": ("political", "candidate", "vote", "policy"),
    }
    for domain, phrases in mapping.items():
        if phrase_present(text, phrases):
            target.add(domain)
    return target


def graph_edge_between(edge: dict, left: str, right: str) -> bool:
    return {edge.get("from_cluster"), edge.get("to_cluster")} == {left, right}


def matching_bridge(row: dict, target_domains: set[str], bridges: list[dict], query: set[str]) -> dict | None:
    claims = set(row.get("_claim_ids", []))
    for bridge in bridges:
        signal_match = query & tokens(bridge.get("routing_signals", []))
        if claims & set(bridge.get("source_claims", [])) and target_domains & set(bridge.get("target_context", {}).get("domains", [])) and signal_match:
            return bridge
    return None


def route(brief: dict, clusters: list[dict], taxonomy: dict) -> dict:
    problem = str(brief.get("problem", "")).strip()
    if not problem:
        raise ValueError("problem must be a non-empty string")
    context = str(brief.get("context", ""))
    decision = str(brief.get("decision", ""))
    named = brief.get("named_concepts", [])
    domains = brief.get("domains", [])
    jobs = brief.get("reasoning_jobs", [])
    stakes = str(brief.get("stakes", "normal"))
    for field, value in (("named_concepts", named), ("domains", domains), ("reasoning_jobs", jobs)):
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError(f"{field} must be an array of strings")
    unknown_domains = sorted(set(domains) - set(taxonomy["domains"]))
    unknown_jobs = sorted(set(jobs) - set(taxonomy["reasoning_jobs"]))
    if unknown_domains:
        raise ValueError("unknown domains: " + ", ".join(unknown_domains))
    if unknown_jobs:
        raise ValueError("unknown reasoning_jobs: " + ", ".join(unknown_jobs))
    if stakes not in {"normal", "elevated"}:
        raise ValueError("stakes must be normal or elevated")

    full_text = " ".join((problem, context, decision, *named)).strip()
    lower = full_text.lower()
    application_requested = bool(set(jobs) & APPLICATION_JOBS) or phrase_present(
        decision.lower(),
        ("choose", "build", "promise", "size", "wait or seek", "lock the plan", "improve the options", "allocate", "fire", "recommend", "reorganize", "dismiss", "use or ignore"),
    )
    target_domains = infer_target_domains(domains, lower)
    warnings, flags, elevated = guardrails(full_text, stakes, domains, target_domains)
    if "source-check" in jobs and re.search(r"\b(?:19|20)\d{2}\b", lower) and "verification" not in flags:
        flags.append("verification")
        warnings.append("Quotation/source boundary: authenticate the work, wording, authorship, chronology, and locator before quoting or attributing.")
    if "artificial-intelligence" in domains and re.search(r"\b(?:gpt-?\d+|today|current|now|latest|20\d{2})\b", lower):
        if "current-view" not in flags:
            flags.append("current-view")
            warnings.append("Current-view boundary: state only what dated audited sources establish unless current primary evidence is checked.")
    if "politics" in domains and ("decide" in jobs or "source-check" in jobs or application_requested) and re.search(r"\b(?:candidate|nominee|ballot|vote|endorse)\b", lower):
        if "current-politics" not in flags:
            flags.append("current-politics")
            warnings.append("Do not invent a candidate endorsement; separate the sourced institutional criterion from current political analysis.")
    graph = load_graph()
    graph_edges = graph.get("edges", [])
    bridges = load_bridges()

    for route_name, phrases in UNRELEASED_ROUTES.items():
        if any(phrase_present(lower, (phrase,)) and not phrase_is_negated(lower, phrase) for phrase in phrases):
            warnings.append(f"The named {route_name} route is not active in this corpus; do not reconstruct it from model memory.")
            return {"mode": "decline", "reason": "unreleased-named-route", "selected": [], "bridges": [], "worldview_connections": [], "warnings": warnings, "response_boundary": "State that the audited corpus does not yet support this named route; continue with ordinary analysis if useful."}
    for reason, phrases in GLOBAL_DECLINES.items():
        if phrase_present(lower, phrases):
            return {"mode": "decline", "reason": reason, "selected": [], "bridges": [], "worldview_connections": [], "warnings": warnings, "response_boundary": "Say briefly that this worldview supplies no necessary leverage; continue with ordinary domain analysis if useful."}

    if not named and not domains and not jobs:
        return {
            "mode": "decline",
            "reason": "no-deutsch-signal",
            "selected": [],
            "bridges": [],
            "worldview_connections": [],
            "adjacent_packets": [],
            "warnings": warnings,
            "response_boundary": "The structured brief contains no Deutsch concept, domain, or reasoning job. Continue with ordinary analysis unless the brief is reframed with a concrete Deutsch signal.",
        }

    query = tokens(full_text)
    named_norm = {normalize_label(item): item for item in named if item.strip()}
    direct_ids: set[str] = set()
    direct_labels: dict[str, str] = {}
    unresolved_named = []
    label_index = []
    for row in clusters:
        labels = {normalize_label(row["cluster_id"]), normalize_label(row["title"])}
        labels.update(normalize_label(alias) for alias in row.get("aliases", []))
        label_index.append((row, labels))
    for normalized, original in named_norm.items():
        exact = [row for row, labels in label_index if normalized in labels]
        if len(exact) == 1:
            direct_ids.add(exact[0]["cluster_id"])
            direct_labels[exact[0]["cluster_id"]] = normalized
            continue
        name_tokens = tokens(normalized)
        approximate = []
        for row, labels in label_index:
            best = 0.0
            for label in labels:
                label_tokens = tokens(label)
                overlap = name_tokens & label_tokens
                if overlap:
                    best = max(best, len(overlap) / max(1, min(len(name_tokens), len(label_tokens))))
            if best >= 0.75:
                approximate.append((best, row))
        approximate.sort(key=lambda item: (-item[0], item[1]["cluster_id"]))
        if approximate and (len(approximate) == 1 or approximate[0][0] > approximate[1][0]):
            row = approximate[0][1]
            direct_ids.add(row["cluster_id"])
            direct_labels[row["cluster_id"]] = normalized
        else:
            unresolved_named.append(original)
    if unresolved_named and not direct_ids:
        warnings.append("Named-concept boundary: unresolved names were not replaced with model-memory or loosely related packets.")
        return {
            "mode": "decline", "reason": "unresolved-named-concept", "unresolved_named_concepts": unresolved_named,
            "selected": [], "bridges": [], "worldview_connections": [], "adjacent_packets": [], "warnings": warnings,
            "response_boundary": "State that the requested name is not resolved in the audited corpus; ask for another label or continue with ordinary analysis.",
        }

    docs = []
    for row in clusters:
        routing = row["problem"]["routing"]
        docs.append(tokens([row["title"], *row.get("aliases", []), row["problem"]["summary"], *routing.get("keywords", []), *routing.get("structural_predicates", [])]))
    counts: dict[str, int] = {}
    for doc in docs:
        for word in doc:
            counts[word] = counts.get(word, 0) + 1
    idf = {word: math.log((len(clusters) + 1) / (count + 1)) + 1 for word, count in counts.items()}

    scored = []
    for row, doc in zip(clusters, docs):
        routing = row["problem"]["routing"]
        overlap = query & doc
        lexical = sum(idf.get(word, 1.0) for word in overlap)
        direct = row["cluster_id"] in direct_ids
        if not direct and not overlap:
            continue
        score = lexical
        if direct:
            score += 100.0
        score += 1.5 * len(set(domains) & set(row.get("domains", [])))
        score += 1.5 * len(set(jobs) & set(routing.get("reasoning_jobs", [])))
        bridge = matching_bridge(row, target_domains, bridges, query) if application_requested else None
        if bridge:
            score += ACTIVE_BRIDGE_ROUTE_BONUS
        if row["cluster_id"] == "quantum-multiverse" and phrase_present(lower, ("multiverse", "parallel universe", "many worlds", "everett")):
            score += 9
        if row["cluster_id"] == "physical-computation-and-proof" and phrase_present(lower, ("quantum computer", "turing principle", "proof is physical")):
            score += 5
        if any(phrase_present(lower, (item.lower(),)) for item in routing.get("reject_if", [])):
            score -= 12
        fit = sorted(overlap, key=lambda word: (-idf.get(word, 1.0), word))[:6]
        if direct:
            fit = ["named:" + direct_labels[row["cluster_id"]], *fit]
        if bridge:
            fit = ["bridge:" + bridge["id"], *fit]
        scored.append({"score": score, "lexical": lexical, "row": row, "fit": fit, "bridge": bridge})

    ranked = sorted(scored, key=lambda item: (-item["score"], item["row"]["cluster_id"]))
    if direct_ids:
        ranked = [item for item in ranked if item["row"]["cluster_id"] in direct_ids]

    selected_rows: list[dict] = []
    if ranked:
        selected_rows.append(ranked[0])
        if "cross-domain-technical-transfer" in flags:
            limit = 1
        else:
            limit = 3 if len(direct_ids) > 1 or "worldview" in domains or "understand-worldview" in jobs else 1
        for item in ranked[1:]:
            if len(selected_rows) >= limit:
                break
            if direct_ids:
                selected_rows.append(item)
                continue
            primary = selected_rows[0]
            connecting = [edge for edge in graph_edges if graph_edge_between(edge, primary["row"]["cluster_id"], item["row"]["cluster_id"])]
            signal_match = any(query & tokens(edge.get("routing_signals", [])) for edge in connecting)
            relative_strength = item["lexical"] >= max(2.5, 0.55 * max(primary["lexical"], 1.0))
            substantive_fit = len(item["fit"]) >= 2 or "understand-worldview" in jobs
            if connecting and signal_match and relative_strength and substantive_fit:
                selected_rows.append(item)

    taste_oracle = (
        "objective-morality-and-aesthetics" in direct_ids
        and application_requested
        and phrase_present(lower, TASTE_ORACLE_TARGETS)
        and phrase_present(lower, DECISION_WORDS)
    )
    if taste_oracle:
        warnings.append("Objective aesthetics is not a taste oracle; the requested concrete verdict lacks a sourced decision procedure and target-domain warrant.")
        flags.append("taste-oracle")

    selected: list[dict] = []
    selected_bridges: list[dict] = []
    for index, item in enumerate(selected_rows):
        row = item["row"]
        bridge = item.get("bridge")
        policy = row.get("application_policy", "lens")
        source_domains = set(row.get("domains", []))
        cross_domain = bool(target_domains - source_domains)
        boundary_hits = []
        decision_tokens = tokens(decision)
        for boundary in row.get("boundaries", {}).get("not_for", []):
            boundary_tokens = tokens(boundary)
            decision_overlap = decision_tokens & boundary_tokens
            full_overlap = query & boundary_tokens
            if decision_overlap and len(full_overlap) >= min(2, len(boundary_tokens)):
                boundary_hits.append(boundary)
        application_permitted = policy == "lens" and not boundary_hits and (not cross_domain or bridge is not None)
        if application_requested and boundary_hits:
            warnings.append(f"Packet boundary: {row['cluster_id']} is not for {', '.join(boundary_hits)}.")
        lanes = ["deutsch-explicit", "faithful-paraphrase", "skill-synthesis"]
        if application_requested and application_permitted:
            lanes.append("skill-application")
        connected = [edge["id"] for edge in graph_edges if any(graph_edge_between(edge, row["cluster_id"], prior["row"]["cluster_id"]) for prior in selected_rows[:index])]
        selected.append({
            "cluster_id": row["cluster_id"],
            "title": row["title"],
            "role": "primary" if index == 0 else "supporting",
            "fit": item["fit"],
            "application_policy": policy,
            "permitted_lanes": lanes,
            "connected_via": connected,
            "cluster_path": row["_path"],
            "source_routes": row.get("source_routes", []),
            "diagnostic_questions": row["problem"]["routing"].get("diagnostic_questions", [])[:3],
            "not_for": row.get("boundaries", {}).get("not_for", []),
            "decline_if": row.get("boundaries", {}).get("decline_if", []),
        })
        if bridge and bridge["id"] not in {item["id"] for item in selected_bridges}:
            selected_bridges.append({
                "id": bridge["id"], "status": bridge["status"], "bridge_path": bridge["_path"],
                "target_problem": bridge["target_problem"], "warrant": bridge["warrant"],
                "target_evidence": bridge["target_evidence"], "disanalogies": bridge["disanalogies"],
                "failure_conditions": bridge["failure_conditions"],
            })

    selected_ids = {item["cluster_id"] for item in selected}
    worldview_connections = [
        {"id": edge["id"], "type": edge["type"], "from_cluster": edge["from_cluster"], "to_cluster": edge["to_cluster"], "summary": edge["summary"], "ownership": edge["origin"]["representation"]}
        for edge in graph_edges
        if edge["from_cluster"] in selected_ids and edge["to_cluster"] in selected_ids
    ]
    adjacent_packets = []
    if selected:
        primary = selected[0]["cluster_id"]
        for edge in graph_edges:
            if primary not in {edge["from_cluster"], edge["to_cluster"]}:
                continue
            neighbor = edge["to_cluster"] if edge["from_cluster"] == primary else edge["from_cluster"]
            if neighbor in selected_ids:
                continue
            adjacent_packets.append({"cluster_id": neighbor, "via": edge["id"], "type": edge["type"], "summary": edge["summary"], "ownership": edge["origin"]["representation"]})
            if len(adjacent_packets) == 3:
                break

    selected_policies = {item["application_policy"] for item in selected}
    has_application_lane = any("skill-application" in item["permitted_lanes"] for item in selected)
    if any(flag in flags for flag in ("actionable-person-diagnosis", "current-politics", "urgent-medical", "taste-oracle")):
        mode = "decline"
        selected = []
        selected_bridges = []
        worldview_connections = []
        adjacent_packets = []
    elif any(flag in flags for flag in ("impersonation", "current-view", "verification", "cross-domain-technical-transfer")) and selected:
        mode = "source-only"
    elif "epistemic-overclaim" in flags and ("source-only" in selected_policies or any(domain in {"quantum-physics", "constructor-theory", "artificial-intelligence"} for domain in domains)):
        mode = "source-only"
    elif not selected:
        mode = "decline"
    elif application_requested:
        if has_application_lane:
            mode = "lens"
        else:
            mode = "source-only"
            warnings.append("Transfer boundary: no active, case-fitting bridge permits a recommendation; use the source only to generate questions or conjectures.")
    elif direct_ids and "source-only" not in selected_policies:
        mode = "direct"
    elif "source-only" in selected_policies:
        mode = "source-only"
    else:
        mode = "lens"

    if mode == "decline":
        boundary = "The audited worldview does not materially discriminate this case. Use ordinary target-domain analysis."
    elif mode == "source-only":
        boundary = "Explain the verified dated source and boundary; do not impersonate, update, or transfer it into a recommendation."
    elif elevated:
        boundary = "Use the lens only as secondary reasoning support after current target-domain evidence and urgent action."
    elif application_requested:
        boundary = "Validate a structured application plan before answering; the bridge and target evidence, not Deutsch's authority, must warrant the recommendation."
    else:
        boundary = "Preserve source, synthesis, and application ownership; use the smallest selected packet."
    return {
        "mode": mode,
        "application_requested": application_requested,
        "target_domains": sorted(target_domains),
        "unresolved_named_concepts": unresolved_named,
        "selected": selected,
        "bridges": selected_bridges,
        "worldview_connections": worldview_connections,
        "adjacent_packets": adjacent_packets,
        "warnings": warnings,
        "response_boundary": boundary,
    }


def meaningful_text(value: object, minimum: int = 12) -> bool:
    text = str(value or "").strip()
    return len(text) >= minimum and text.lower().rstrip(".") not in BAD_EVIDENCE


def meaningful_list(value: object, minimum: int = 12) -> bool:
    return isinstance(value, list) and bool(value) and all(meaningful_text(item, minimum) for item in value)


def validate_plan(plan: dict, clusters: list[dict], bridges: list[dict]) -> dict:
    errors: list[str] = []
    mode = plan.get("mode")
    if mode not in {"direct", "lens", "source-only", "decline"}:
        errors.append("invalid mode")
    selected = plan.get("selected_clusters", [])
    if not isinstance(selected, list):
        errors.append("selected_clusters must be an array")
        selected = []
    by_id = {row["cluster_id"]: row for row in clusters}
    if len(selected) > 3:
        errors.append("no more than three clusters may be selected")
    if len(set(selected)) != len(selected):
        errors.append("selected_clusters must be unique")
    for cluster_id in selected:
        if cluster_id not in by_id:
            errors.append("unknown cluster: " + str(cluster_id))
    if mode == "decline" and selected:
        errors.append("decline mode must not select clusters")
    if mode in {"direct", "lens", "source-only"} and not selected:
        errors.append("non-decline mode requires at least one cluster")

    roles = plan.get("packet_roles", {})
    if selected and (not isinstance(roles, dict) or set(roles) != set(selected)):
        errors.append("packet_roles must assign every selected cluster exactly once")
    elif isinstance(roles, dict) and not set(roles.values()) <= {"primary", "supporting", "boundary"}:
        errors.append("invalid packet role")
    elif selected and list(roles.values()).count("primary") != 1:
        errors.append("packet_roles must contain exactly one primary")
    if len(selected) > 1:
        edges = load_graph().get("edges", [])
        connected = {selected[0]}
        remaining = set(selected[1:])
        while remaining:
            newly_connected = {
                cluster_id for cluster_id in remaining
                if any(
                    edge.get("from_cluster") in connected and edge.get("to_cluster") == cluster_id
                    or edge.get("to_cluster") in connected and edge.get("from_cluster") == cluster_id
                    for edge in edges
                )
            }
            if not newly_connected:
                errors.append("selected clusters must form a connected worldview subgraph")
                break
            connected |= newly_connected
            remaining -= newly_connected

    lanes = plan.get("lanes", [])
    allowed_lanes = {"deutsch-explicit", "faithful-paraphrase", "skill-synthesis", "skill-application", "unverified"}
    if not isinstance(lanes, list) or not lanes:
        errors.append("lanes must identify at least one ownership lane")
        lanes = []
    elif not set(lanes) <= allowed_lanes:
        errors.append("invalid lane")
    if mode in {"source-only", "decline"} and "skill-application" in lanes:
        errors.append(f"{mode} mode may not include skill-application")
    if lanes == ["unverified"] or set(lanes) == {"unverified"}:
        errors.append("unverified may not be the only ownership lane")
    if mode == "direct" and not {"deutsch-explicit", "faithful-paraphrase"} & set(lanes):
        errors.append("direct mode requires a sourced Deutsch ownership lane")
    if mode == "direct" and any(by_id.get(cluster_id, {}).get("application_policy") == "source-only" for cluster_id in selected):
        errors.append("source-only packet may not use direct mode")
    if "skill-application" in lanes and any(by_id.get(cluster_id, {}).get("application_policy") == "source-only" for cluster_id in selected):
        errors.append("source-only packet may not license skill-application")

    selected_bridge_ids = plan.get("selected_bridges", [])
    if not isinstance(selected_bridge_ids, list):
        errors.append("selected_bridges must be an array")
        selected_bridge_ids = []
    bridge_by_id = {bridge["id"]: bridge for bridge in bridges}
    selected_claims = {claim_id for cluster_id in selected for claim_id in by_id.get(cluster_id, {}).get("_claim_ids", [])}
    for bridge_id in selected_bridge_ids:
        if bridge_id not in bridge_by_id:
            errors.append("selected bridge is not active: " + str(bridge_id))
        elif not selected_claims & set(bridge_by_id[bridge_id].get("source_claims", [])):
            errors.append("selected bridge is not anchored in a selected cluster claim: " + str(bridge_id))

    if "skill-application" in lanes:
        transfer = plan.get("transfer")
        if not isinstance(transfer, dict):
            errors.append("skill-application requires structured transfer")
        else:
            transfer_type = transfer.get("type")
            if transfer_type not in {"same-domain", "cross-domain"}:
                errors.append("transfer.type must be same-domain or cross-domain")
            if transfer_type == "cross-domain" and not selected_bridge_ids:
                errors.append("cross-domain application requires an active selected bridge")
            if transfer.get("application_owner") != "skill":
                errors.append("transfer.application_owner must be skill")
            if not meaningful_text(transfer.get("mechanism"), 20):
                errors.append("transfer.mechanism requires a concrete correspondence")
            if not meaningful_list(transfer.get("target_evidence"), 12):
                errors.append("transfer.target_evidence requires concrete target-domain evidence")
            if not meaningful_list(transfer.get("disanalogies"), 12):
                errors.append("transfer.disanalogies requires material limits")
            if not meaningful_list(transfer.get("defeaters"), 12):
                errors.append("transfer.defeaters requires conditions that would defeat the application")
    return {"ok": not errors, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("route", "plan"))
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    try:
        data = read_json(args.input)
        clusters = load_clusters()
        result = route(data, clusters, load_domains()) if args.command == "route" else validate_plan(data, clusters, load_bridges())
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result.get("ok", True) else 1
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print("error: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
