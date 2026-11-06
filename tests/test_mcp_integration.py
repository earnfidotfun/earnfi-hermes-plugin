"""Inventory fixture vs live card consistency helpers."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from doctor.checks import SERVER_CARD_URL, _http_get_json


class McpIntegrationTests(unittest.TestCase):
    def test_fixture_matches_live_count(self):
        fixture = json.loads(
            (ROOT / "tests/fixtures/tool_inventory.json").read_text(encoding="utf-8")
        )
        status, card = _http_get_json(SERVER_CARD_URL)
        self.assertEqual(status, 200)
        live_count = len(card.get("tools") or [])
        self.assertEqual(fixture["count"], live_count)
        self.assertEqual(len(fixture["tools"]), live_count)


if __name__ == "__main__":
    unittest.main()
