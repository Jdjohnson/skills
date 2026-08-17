from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")


class SkillContractTests(unittest.TestCase):
    def test_research_privacy_and_stop_boundaries(self) -> None:
        for heading in ("## Core contract", "## Stop and compile", "## Truth and privacy"):
            self.assertIn(heading, SKILL)
        for reference in ("visibility-and-updates.md", "continuity-and-stop.md", "research-quality.md"):
            self.assertIn(reference, SKILL)
        self.assertIn("Do not detach, schedule, daemonize, or hide", SKILL)
        self.assertIn("Do not edit target code, publish, message, purchase, deploy", SKILL)
        quality = (ROOT / "references" / "research-quality.md").read_text(encoding="utf-8")
        self.assertIn("Never put credentials", quality)

    def test_stop_produces_a_source_backed_final_report(self) -> None:
        self.assertIn("Create `final-report.md`", SKILL)
        self.assertIn("A stopped process is not the deliverable", SKILL)
        report = (ROOT / "assets" / "final-report.md.tmpl").read_text(encoding="utf-8")
        for heading in (
            "## Bottom line",
            "## Strongest supported findings",
            "## Important uncertainty and unresolved questions",
            "## Sources",
        ):
            self.assertIn(heading, report)


if __name__ == "__main__":
    unittest.main()
