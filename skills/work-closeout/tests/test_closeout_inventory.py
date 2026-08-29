from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "closeout_inventory.py"


class CloseoutInventoryTests(unittest.TestCase):
    def test_inventory_is_bounded_read_only_and_classifies_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            subject = workspace / "subject"
            files = {
                "current/status.md": "Current state: drafted but not sent.\n",
                "generated/draft.md": "Status: drafted but not sent.\n",
                "evidence/source.md": "Historical: drafted but not sent.\n",
                "protected/note.md": "Human note: drafted but not sent.\n",
                "misc/readme.md": "Other: drafted but not sent.\n",
            }
            for relative, content in files.items():
                path = subject / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            before = {path: (subject / path).read_text(encoding="utf-8") for path in files}

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--workspace",
                    str(workspace),
                    "--root",
                    "subject",
                    "--term",
                    "not sent",
                    "--class-rule",
                    "canonical-current=subject/current/**",
                    "--class-rule",
                    "generated-artifact=subject/generated/**",
                    "--class-rule",
                    "raw-source=subject/evidence/**",
                    "--class-rule",
                    "protected-human=subject/protected/**",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            classes = {item["path"]: item["class"] for item in payload["matches"]}
            self.assertEqual(classes["subject/current/status.md"], "canonical-current")
            self.assertEqual(classes["subject/generated/draft.md"], "generated-artifact")
            self.assertEqual(classes["subject/evidence/source.md"], "raw-source")
            self.assertEqual(classes["subject/protected/note.md"], "protected-human")
            self.assertEqual(classes["subject/misc/readme.md"], "other")
            self.assertEqual(payload["class_rules"][0]["class"], "canonical-current")
            after = {path: (subject / path).read_text(encoding="utf-8") for path in files}
            self.assertEqual(after, before)

            broad = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--workspace",
                    str(workspace),
                    "--root",
                    str(workspace),
                    "--term",
                    "not sent",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(broad.returncode, 0)
            self.assertIn("workspace-root scans require", broad.stderr)


if __name__ == "__main__":
    unittest.main()
