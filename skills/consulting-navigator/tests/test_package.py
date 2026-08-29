#!/usr/bin/env python3
"""Portable regression tests for the Consulting Navigator package."""

from __future__ import annotations

import importlib.util
import json
import statistics
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_THRESHOLDS = {
    "router-cases-tuning.json": {
        "recall": 0.7777777777777778,
        "precision": 0.5,
        "mrr": 0.8611111111111112,
        "top1": 0.75,
        "forbidden": 9,
    },
    "router-cases-validation.json": {
        "recall": 0.861111111111111,
        "precision": 0.5972222222222222,
        "mrr": 0.9791666666666666,
        "top1": 0.9583333333333334,
        "forbidden": 2,
    },
    "router-cases-holdout.json": {
        "recall": 0.8666666666666667,
        "precision": 0.5444444444444444,
        "mrr": 1.0,
        "top1": 1.0,
        "forbidden": 1,
    },
}


def load_router():
    path = ROOT / "scripts/navigate.py"
    spec = importlib.util.spec_from_file_location("consulting_navigator_test_router", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load router: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ROUTER = load_router()


class PackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = ROUTER.load_index(ROOT / "registry/index.json")
        cls.by_id = {row["i"]: row for row in cls.rows}

    def test_registry_resolves_every_method(self) -> None:
        self.assertTrue(self.rows)
        self.assertEqual(len(self.rows), len(self.by_id), "duplicate registry ids")
        method_ids = {path.stem for path in (ROOT / "methods").glob("*.md")}
        self.assertEqual(set(self.by_id), method_ids)

    @staticmethod
    def plan(methods: list[dict]) -> dict:
        return {
            "case_summary": "Choose a small evidence-aware method stack.",
            "selected_methods": methods,
            "assumptions": [],
            "missing_inputs": [],
            "expected_output": "One supported recommendation.",
        }

    @staticmethod
    def row(method_id: str, *, before: list[str] | None = None) -> dict:
        return {
            "i": method_id,
            "f": "synthetic-family",
            "j": ["gather-evidence"],
            "b": before or [],
            "c": [],
        }

    def test_validate_plan_accepts_valid_plan(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            methods_dir = Path(raw)
            (methods_dir / "source.md").write_text("# Source\n", encoding="utf-8")
            result = ROUTER.validate_plan(
                self.plan(
                    [{"id": "source", "role": "Establish evidence.", "sequence": 1}]
                ),
                [self.row("source")],
                methods_dir,
            )
        self.assertTrue(result["ok"])
        self.assertEqual(result["errors"], [])

    def test_validate_plan_rejects_missing_source(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            result = ROUTER.validate_plan(
                self.plan(
                    [{"id": "source", "role": "Establish evidence.", "sequence": 1}]
                ),
                [self.row("source")],
                Path(raw),
            )
        self.assertFalse(result["ok"])
        self.assertIn("missing method file: source", result["errors"])

    def test_validate_plan_rejects_invalid_bridge_order(self) -> None:
        rows = [self.row("source", before=["bridge"]), self.row("bridge")]
        with tempfile.TemporaryDirectory() as raw:
            methods_dir = Path(raw)
            for method_id in ("source", "bridge"):
                (methods_dir / f"{method_id}.md").write_text(
                    f"# {method_id}\n", encoding="utf-8"
                )
            result = ROUTER.validate_plan(
                self.plan(
                    [
                        {"id": "bridge", "role": "Synthesize evidence.", "sequence": 1},
                        {"id": "source", "role": "Establish evidence.", "sequence": 2},
                    ]
                ),
                rows,
                methods_dir,
            )
        self.assertFalse(result["ok"])
        self.assertIn(
            "reversed order requires override: source -> bridge", result["errors"]
        )

    def test_validate_plan_rejects_source_only_misuse(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            methods_dir = Path(raw)
            (methods_dir / "source.md").write_text("# Source\n", encoding="utf-8")
            result = ROUTER.validate_plan(
                self.plan([{"id": "source"}]),
                [self.row("source")],
                methods_dir,
            )
        self.assertFalse(result["ok"])
        self.assertIn(
            "selected_methods[0] must contain only id, role, sequence",
            result["errors"],
        )

    def test_human_router_fixture_sets(self) -> None:
        for filename, thresholds in FIXTURE_THRESHOLDS.items():
            fixtures = json.loads((Path(__file__).with_name(filename)).read_text(encoding="utf-8"))
            recalls = []
            precisions = []
            reciprocal_ranks = []
            top1 = []
            forbidden_count = 0
            for fixture in fixtures:
                routed = ROUTER.route(fixture["brief"], self.rows)["methods"]
                ids = [item["id"] for item in routed]
                primary = fixture["primary"]
                accepted = set(primary) | set(fixture["acceptable"])
                ranks = [ids.index(method) + 1 for method in primary if method in ids]
                self.assertTrue(ranks, f"{filename}:{fixture['id']} missed all primary methods")
                recalls.append(len(ranks) / len(primary))
                precisions.append(sum(method in accepted for method in ids) / len(ids))
                reciprocal_ranks.append(1 / min(ranks))
                top1.append(bool(ids and ids[0] in primary))
                forbidden_count += sum(method in fixture["forbidden"] for method in ids)
            self.assertGreaterEqual(statistics.mean(recalls), thresholds["recall"], filename)
            self.assertGreaterEqual(statistics.mean(precisions), thresholds["precision"], filename)
            self.assertGreaterEqual(statistics.mean(reciprocal_ranks), thresholds["mrr"], filename)
            self.assertGreaterEqual(statistics.mean(top1), thresholds["top1"], filename)
            self.assertLessEqual(forbidden_count, thresholds["forbidden"], filename)

if __name__ == "__main__":
    unittest.main(verbosity=2)
