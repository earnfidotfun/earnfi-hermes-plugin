"""Static manifest checks — no Hermes runtime required."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ManifestTests(unittest.TestCase):
    def test_plugin_yaml_exists(self):
        text = (ROOT / "plugin.yaml").read_text(encoding="utf-8")
        self.assertIn("name: earnfi", text)
        self.assertIn("earnfi_doctor", text)
        self.assertIn("requires_hermes:", text)

    def test_mcp_json_streamable_http(self):
        data = json.loads((ROOT / "mcp.json").read_text(encoding="utf-8"))
        server = data["mcpServers"]["earnfi-api"]
        self.assertEqual(server["type"], "streamable-http")
        self.assertEqual(server["url"], "https://app.earnfi.fun/mcp")
        self.assertNotIn("http", server["type"].replace("streamable-http", ""))
        # Must not collide with native plugin toolset name `earnfi`
        self.assertNotIn("earnfi", data["mcpServers"])

    def test_plugin_json_trust_extension(self):
        data = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        trust = data["extensions"]["com.nousresearch.hermes"]["servers"]["earnfi-api"]["trust"]
        self.assertEqual(trust, "untrusted")
        self.assertEqual(data["repository"], "https://github.com/earnfidotfun/earnfi-hermes-plugin")

    def test_no_cursor_branding_in_user_docs(self):
        banned = re.compile(r"\bCursor\b", re.I)
        paths = [
            p
            for p in (ROOT / "docs").glob("*.md")
            if p.name != "RELEASE-READINESS.md"
        ] + [
            ROOT / "README.md",
            ROOT / "SUBMISSION.md",
        ]
        for skill in (ROOT / "skills").rglob("SKILL.md"):
            paths.append(skill)
        offenders = []
        for path in paths:
            text = path.read_text(encoding="utf-8")
            if banned.search(text):
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [], f"Cursor branding found in: {offenders}")

    def test_skills_present(self):
        skills = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())
        self.assertGreaterEqual(len(skills), 10)
        for name in skills:
            self.assertTrue((ROOT / "skills" / name / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
