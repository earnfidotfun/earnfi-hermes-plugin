""" /earnfi-smoke — safe read-only checks only """

from __future__ import annotations

from ..doctor.checks import run_smoke
from ..tools.plugin_settings import agent_api_base, mcp_url


def handle_smoke(raw_args: str = "", **_kwargs) -> str:
    _ = raw_args
    report = run_smoke(mcp_url=mcp_url(), api_base=agent_api_base())
    header = "EarnFi smoke test (read-only)\n" + ("=" * 34) + "\n"
    body = report.format_text()
    # Drop the shared title to avoid duplication.
    if body.startswith("EarnFi system status"):
        body = body.split("\n", 2)[-1]
    footer = (
        "\nSmoke scope: discovery + health + catalog + rails only. "
        "No payments, creates, or withdrawals were attempted.\n"
    )
    return header + body + footer
