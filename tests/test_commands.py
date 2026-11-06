"""Slash-command handler smoke (no Hermes host)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hermes_commands.overview import handle_earnfi, handle_help


class CommandTests(unittest.TestCase):
    def test_earnfi_intro(self):
        text = handle_earnfi("")
        self.assertIn("EarnFi for Hermes", text)
        self.assertIn("/earnfi-status", text)
        self.assertNotRegex(text, r"(?i)\bcursor\b")

    def test_help(self):
        text = handle_help("")
        self.assertIn("/earnfi-smoke", text)
        self.assertIn("earnfi-hiring", text)


if __name__ == "__main__":
    unittest.main()
