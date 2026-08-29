#!/usr/bin/env python3
"""Run behavioral routes, plans, and corruption sentinels."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
CASE_FILE = ROOT / "tests" / "release-cases.json"
sys.dont_write_bytecode = True


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_router(package: Path = ROOT, name: str = "jj_deutsch_release_router"):
    path = package / "scripts" / "route.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_script(package: Path, script: str, name: str):
    path = package / "scripts" / script
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def route_errors(case: dict[str, Any], output: dict[str, Any]) -> list[str]:
    selected = [item["cluster_id"] for item in output["selected"]]
    bridge_ids = [item["id"] for item in output.get("bridges", [])]
    errors = []
    if output["mode"] not in case["expected_modes"]:
        errors.append(f"mode {output['mode']} not in {case['expected_modes']}")
    for cluster_id in case.get("require_clusters", []):
        if cluster_id not in selected:
            errors.append(f"required cluster missing: {cluster_id}")
    for cluster_id in case.get("forbid_clusters", []):
        if cluster_id in selected:
            errors.append(f"forbidden cluster selected: {cluster_id}")
    if len(selected) > case.get("max_selected", 3):
        errors.append("too many clusters selected")
    if "exact_clusters" in case and selected != case["exact_clusters"]:
        errors.append(f"selected {selected} != exact {case['exact_clusters']}")
    if case.get("forbid_empty_fit") and any(not item.get("fit") for item in output["selected"]):
        errors.append("selected packet has empty fit")
    for bridge_id in case.get("require_bridges", []):
        if bridge_id not in bridge_ids:
            errors.append(f"required bridge missing: {bridge_id}")
    for bridge_id in case.get("forbid_bridges", []):
        if bridge_id in bridge_ids:
            errors.append(f"forbidden bridge selected: {bridge_id}")
    if len(selected) > 1 and any(not item.get("connected_via") for item in output["selected"][1:]):
        errors.append("multi-packet route is not explicitly connected")
    warning_text = " ".join(output["warnings"]).lower()
    for fragment in case.get("warning_contains", []):
        if fragment.lower() not in warning_text:
            errors.append(f"warning missing fragment: {fragment}")
    for fragment in case.get("warning_not_contains", []):
        if fragment.lower() in warning_text:
            errors.append(f"warning unexpectedly contains fragment: {fragment}")
    return errors


def evaluate_routes(router) -> dict[str, Any]:
    suite = load(CASE_FILE)
    cases = suite.get("cases", [])
    if not cases or len({case["id"] for case in cases}) != len(cases):
        raise ValueError("routing cases must be non-empty and uniquely identified")
    clusters = router.load_clusters()
    taxonomy = router.load_domains()
    results = []
    for case in cases:
        output = router.route(case["brief"], clusters, taxonomy)
        errors = route_errors(case, output)
        results.append(
            {
                "id": case["id"],
                "priority": case["priority"],
                "ok": not errors,
                "mode": output["mode"],
                "selected": [item["cluster_id"] for item in output["selected"]],
                "errors": errors,
            }
        )
    by_priority = {}
    for priority in ("P0", "P1", "P2"):
        rows = [row for row in results if row["priority"] == priority]
        by_priority[priority] = {"passed": sum(row["ok"] for row in rows), "total": len(rows)}
    return {
        "ok": all(row["ok"] for row in results),
        "suite_version": suite.get("suite_version"),
        "executed_once": len(results),
        "summary": by_priority,
        "failures": [row for row in results if not row["ok"]],
    }


def plan_fixtures() -> list[dict[str, Any]]:
    valid_transfer = {
        "type": "cross-domain",
        "application_owner": "skill",
        "mechanism": "Rival accounts imply mechanisms that target evidence can discriminate.",
        "target_evidence": ["A dated target chronology and a discriminating comparison."],
        "disanalogies": ["The organization is an open system with strategic actors."],
        "defeaters": ["Target evidence favors another mechanism or no discriminating test exists."],
    }
    return [
        {
            "id": "PLAN-valid-bridge",
            "expected_ok": True,
            "plan": {
                "mode": "lens",
                "selected_clusters": ["explanation-and-good-explanations"],
                "packet_roles": {"explanation-and-good-explanations": "primary"},
                "selected_bridges": ["bridge.good-explanations.to-causal-diagnosis.v1"],
                "lanes": ["faithful-paraphrase", "skill-synthesis", "skill-application"],
                "transfer": valid_transfer,
            },
        },
        {
            "id": "PLAN-missing-bridge",
            "expected_ok": False,
            "plan": {
                "mode": "lens",
                "selected_clusters": ["explanation-and-good-explanations"],
                "packet_roles": {"explanation-and-good-explanations": "primary"},
                "selected_bridges": [],
                "lanes": ["faithful-paraphrase", "skill-application"],
                "transfer": valid_transfer,
            },
        },
        {
            "id": "PLAN-source-only-application",
            "expected_ok": False,
            "plan": {
                "mode": "lens",
                "selected_clusters": ["constructor-theory"],
                "packet_roles": {"constructor-theory": "primary"},
                "selected_bridges": [],
                "lanes": ["faithful-paraphrase", "skill-application"],
                "transfer": valid_transfer,
            },
        },
        {
            "id": "PLAN-disconnected-packets",
            "expected_ok": False,
            "plan": {
                "mode": "direct",
                "selected_clusters": ["quantum-multiverse", "objective-morality-and-aesthetics"],
                "packet_roles": {"quantum-multiverse": "primary", "objective-morality-and-aesthetics": "supporting"},
                "selected_bridges": [],
                "lanes": ["faithful-paraphrase"],
            },
        },
        {
            "id": "PLAN-empty-target-evidence",
            "expected_ok": False,
            "plan": {
                "mode": "lens",
                "selected_clusters": ["explanation-and-good-explanations"],
                "packet_roles": {"explanation-and-good-explanations": "primary"},
                "selected_bridges": ["bridge.good-explanations.to-causal-diagnosis.v1"],
                "lanes": ["faithful-paraphrase", "skill-application"],
                "transfer": {**valid_transfer, "target_evidence": []},
            },
        },
        {
            "id": "PLAN-missing-primary-role",
            "expected_ok": False,
            "plan": {
                "mode": "direct",
                "selected_clusters": ["explanation-and-good-explanations"],
                "packet_roles": {"explanation-and-good-explanations": "supporting"},
                "selected_bridges": [],
                "lanes": ["faithful-paraphrase"],
            },
        },
    ]


def evaluate_plans(router) -> dict[str, Any]:
    clusters = router.load_clusters()
    bridges = router.load_bridges()
    results = []
    for fixture in plan_fixtures():
        outcome = router.validate_plan(fixture["plan"], clusters, bridges)
        ok = bool(outcome.get("ok")) is fixture["expected_ok"]
        results.append(
            {
                "id": fixture["id"],
                "ok": ok,
                "expected_ok": fixture["expected_ok"],
                "actual_ok": bool(outcome.get("ok")),
                "errors": outcome.get("errors", []),
            }
        )
    return {"ok": all(row["ok"] for row in results), "passed": sum(row["ok"] for row in results), "total": len(results), "results": results}


def edit_json(package: Path, relative: str, edit: Callable[[dict[str, Any]], None]) -> None:
    path = package / relative
    value = load(path)
    edit(value)
    path.write_text(json.dumps(value), encoding="utf-8")


def corruption_specs() -> list[tuple[str, Callable[[Path], None], str, str]]:
    def missing_origin(package: Path) -> None:
        edit_json(package, "references/corpus/clusters/explanation-and-good-explanations.json", lambda value: value["claims"][0].pop("origin"))

    def unknown_bridge_claim(package: Path) -> None:
        edit_json(package, "references/corpus/bridges/good-explanations-to-causal-diagnosis.json", lambda value: value.__setitem__("source_claims", ["claim.fabricated.v1"]))

    def invalid_relationship(package: Path) -> None:
        edit_json(package, "references/corpus/clusters/explanation-and-good-explanations.json", lambda value: value["relationships"][0].__setitem__("from", value["arguments"][0]["id"]))

    def bad_graph_endpoint(package: Path) -> None:
        edit_json(package, "references/corpus/worldview-graph.json", lambda value: value["edges"][0].__setitem__("to_cluster", "missing-packet"))

    def duplicate_claim_id(package: Path) -> None:
        edit_json(package, "references/corpus/clusters/explanation-and-good-explanations.json", lambda value: value["claims"].append(dict(value["claims"][0])))

    def missing_bridge_disanalogy(package: Path) -> None:
        edit_json(package, "references/corpus/bridges/good-explanations-to-causal-diagnosis.json", lambda value: value.__setitem__("disanalogies", []))

    return [
        ("missing-attribution", missing_origin, "validate_corpus.py", "schema-required fields missing"),
        ("unknown-bridge-claim", unknown_bridge_claim, "validate_corpus.py", "unresolved source claim"),
        ("invalid-relationship-endpoint", invalid_relationship, "validate_corpus.py", "invalid endpoint types"),
        ("bad-worldview-endpoint", bad_graph_endpoint, "validate_corpus.py", "unresolved cluster endpoint"),
        ("duplicate-claim-id", duplicate_claim_id, "validate_corpus.py", "duplicate id"),
        ("missing-bridge-disanalogy", missing_bridge_disanalogy, "validate_corpus.py", "bridge requires disanalogies"),
    ]


def evaluate_corruptions() -> dict[str, Any]:
    results = []
    with tempfile.TemporaryDirectory(prefix="jjd-release-sentinels-") as temp:
        root = Path(temp)
        for index, (mutant_id, mutate, script, expected) in enumerate(corruption_specs()):
            package = root / mutant_id
            shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))
            mutate(package)
            module = load_script(package, script, f"jj_deutsch_sentinel_{index}")
            outcome = module.validate()
            observed = json.dumps(outcome, sort_keys=True)
            results.append(
                {
                    "id": mutant_id,
                    "script": script,
                    "ok": not outcome.get("ok") and expected in observed,
                    "expected_signal": expected,
                }
            )
    return {"ok": all(row["ok"] for row in results), "passed": sum(row["ok"] for row in results), "total": len(results), "results": results}


def evaluate_package() -> dict[str, Any]:
    heavy = [
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".pdf", ".epub", ".mobi"}
    ]
    return {
        "ok": not heavy,
        "heavy_sources": heavy,
    }


def evaluate() -> dict[str, Any]:
    router = load_router()
    routing = evaluate_routes(router)
    plans = evaluate_plans(router)
    corruptions = evaluate_corruptions()
    package = evaluate_package()
    return {
        "ok": all(section["ok"] for section in (routing, plans, corruptions, package)),
        "routing": routing,
        "plans": plans,
        "corruption_sentinels": corruptions,
        "package": package,
    }


def main() -> int:
    try:
        result = evaluate()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["ok"] else 1
    except (OSError, KeyError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        print("error: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
