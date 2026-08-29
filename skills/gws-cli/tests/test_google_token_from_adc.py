from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import google_token_from_adc  # noqa: E402


class GoogleTokenFromAdcTests(unittest.TestCase):
    def test_private_json_write_is_atomic_and_mode_0600(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "token.json"
            output.write_text("old", encoding="utf-8")
            os.chmod(output, 0o644)

            google_token_from_adc.write_private_json(output, {"refresh_token": "secret"})

            self.assertEqual(json.loads(output.read_text()), {"refresh_token": "secret"})
            self.assertEqual(os.stat(output).st_mode & 0o777, 0o600)
            self.assertEqual(list(output.parent.glob(f".{output.name}.*.tmp")), [])

    def test_private_json_write_refuses_symlink_destination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.json"
            target.write_text("unchanged", encoding="utf-8")
            output = root / "token.json"
            output.symlink_to(target)

            with self.assertRaisesRegex(ValueError, "symlinked credential destination"):
                google_token_from_adc.write_private_json(output, {"refresh_token": "secret"})

            self.assertEqual(target.read_text(encoding="utf-8"), "unchanged")


if __name__ == "__main__":
    unittest.main()
