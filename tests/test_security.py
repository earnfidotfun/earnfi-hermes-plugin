"""Security posture checks for manifests and payment skill language."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SecurityTests(unittest.TestCase):
    def test_mcp_has_no_secrets(self):
        raw = (ROOT / "mcp.json").read_text(encoding="utf-8").lower()
        for needle in ("private", "secret", "api_key", "seed", "0x", "sk-"):
            # allow words in comments? none expected — fail on credential-like keys
            self.assertNotIn(f'"{needle}"', raw)

    def test_trust_untrusted(self):
        data = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(
            data["extensions"]["com.nousresearch.hermes"]["servers"]["earnfi-api"]["trust"],
            "untrusted",
        )

    def test_payments_skill_forbids_false_success(self):
        text = (ROOT / "skills/earnfi-payments/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("signature alone", text.lower())
        self.assertIn("settlement", text.lower())
        self.assertIn("idempotency", text.lower())

    def test_security_doc_disclosure(self):
        text = (ROOT / "docs/SECURITY.md").read_text(encoding="utf-8")
        self.assertIn("app.earnfi.fun", text)
        self.assertIn("x402", text)


if __name__ == "__main__":
    unittest.main()
