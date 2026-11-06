""" /earnfi-smoke — safe read-only checks only """

from __future__ import annotations

from doctor.checks import DEFAULT_API_BASE, DEFAULT_MCP_URL, run_smoke


def handle_smoke(raw_args: str = "", **_kwargs) -> str:
    _ = raw_args
    report = run_smoke(mcp_url=DEFAULT_MCP_URL, api_base=DEFAULT_API_BASE)
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
