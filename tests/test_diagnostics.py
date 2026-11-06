"""Live (or network) diagnostics against EarnFi production discovery endpoints."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from doctor.checks import run_doctor, run_smoke, SMOKE_REQUIRED_TOOLS


class DiagnosticsTests(unittest.TestCase):
    def test_doctor_live(self):
        report = run_doctor()
        self.assertTrue(report.overall_ok, report.format_text())
        self.assertGreaterEqual(report.tool_count, 100)
        self.assertEqual(report.missing_smoke_tools, [])
        self.assertGreater(report.readonly_tools, 0)
        self.assertGreater(report.write_tools, 0)

    def test_smoke_live(self):
        report = run_smoke()
        self.assertTrue(report.overall_ok, report.format_text())

    def test_smoke_required_tools_listed(self):
        self.assertIn("earnfi_manual_create", SMOKE_REQUIRED_TOOLS)
        self.assertIn("earnfi_health", SMOKE_REQUIRED_TOOLS)


if __name__ == "__main__":
    unittest.main()
