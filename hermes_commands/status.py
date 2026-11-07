""" /earnfi-status """

from __future__ import annotations

from ..doctor.checks import DEFAULT_API_BASE, DEFAULT_MCP_URL, run_doctor


def handle_status(raw_args: str = "", **_kwargs) -> str:
    _ = raw_args
    report = run_doctor(mcp_url=DEFAULT_MCP_URL, api_base=DEFAULT_API_BASE)
    return report.format_text()
