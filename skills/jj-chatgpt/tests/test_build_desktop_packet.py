"""Smoke tests for the ChatGPT Desktop packet helper."""

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import build_desktop_packet


class TestBuildDesktopPacket(unittest.TestCase):
    def test_packet_name_prompt_and_suffix_behavior(self):
        with TemporaryDirectory() as tmpdir:
            desktop_root = Path(tmpdir) / "Desktop"

            first = build_desktop_packet.build_packet(
                lane="deep-research",
                slug="Vendor Landscape",
                prompt_text="Exact prompt text",
                upload_paths=[],
                desktop_root=desktop_root,
                packet_date="2026-04-22",
            )
            second = build_desktop_packet.build_packet(
                lane="deep-research",
                slug="Vendor Landscape",
                prompt_text="Exact prompt text",
                upload_paths=[],
                desktop_root=desktop_root,
                packet_date="2026-04-22",
            )

            first_dir = Path(first.packet_dir)
            second_dir = Path(second.packet_dir)

            self.assertEqual(
                first_dir.name,
                "chatgpt-deep-research-vendor-landscape-packet-2026-04-22",
            )
            self.assertEqual(
                second_dir.name,
                "chatgpt-deep-research-vendor-landscape-packet-2026-04-22-2",
            )
            self.assertEqual(
                (first_dir / "PROMPT.md").read_text(encoding="utf-8"),
                "Exact prompt text",
            )

    def test_packet_is_flat_and_renames_colliding_files(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            desktop_root = root / "Desktop"
            source_root = root / "source"

            file_a = source_root / "alpha" / "brief.md"
            file_b = source_root / "beta" / "brief.md"
            file_c = source_root / "gamma" / "PROMPT.md"

            for path, content in (
                (file_a, "alpha brief"),
                (file_b, "beta brief"),
                (file_c, "uploaded prompt named file"),
            ):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")

            result = build_desktop_packet.build_packet(
                lane="agent",
                slug="Pricing Sweep",
                prompt_text="Agent prompt",
                upload_paths=[str(file_a), str(file_b), str(file_c)],
                desktop_root=desktop_root,
                packet_date="2026-04-22",
            )

            packet_dir = Path(result.packet_dir)
            packet_entries = sorted(path.name for path in packet_dir.iterdir())

            self.assertEqual(
                packet_entries,
                ["PROMPT-2.md", "PROMPT.md", "brief-2.md", "brief.md"],
            )
            self.assertEqual(
                (packet_dir / "brief.md").read_text(encoding="utf-8"),
                "alpha brief",
            )
            self.assertEqual(
                (packet_dir / "brief-2.md").read_text(encoding="utf-8"),
                "beta brief",
            )
            self.assertEqual(
                (packet_dir / "PROMPT-2.md").read_text(encoding="utf-8"),
                "uploaded prompt named file",
            )

    def test_packet_limits_upload_files_and_reports_omissions(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            desktop_root = root / "Desktop"
            source_root = root / "source"

            upload_paths = []
            for index in range(1, 23):
                path = source_root / f"file-{index:02d}.md"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"file {index}", encoding="utf-8")
                upload_paths.append(str(path))

            result = build_desktop_packet.build_packet(
                lane="pro-review",
                slug="Architecture Decision",
                prompt_text="Review prompt",
                upload_paths=upload_paths,
                desktop_root=desktop_root,
                packet_date="2026-04-22",
            )

            packet_dir = Path(result.packet_dir)

            self.assertEqual(len(result.included_files), 20)
            self.assertEqual(len(result.omitted_files), 2)
            self.assertEqual(len(list(packet_dir.iterdir())), 21)
            self.assertEqual(
                result.omitted_files,
                [
                    str((source_root / "file-21.md").resolve()),
                    str((source_root / "file-22.md").resolve()),
                ],
            )


if __name__ == "__main__":
    unittest.main()
