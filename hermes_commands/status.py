""" /earnfi-status """

from __future__ import annotations

from ..doctor.checks import run_doctor
from ..tools.plugin_settings import agent_api_base, mcp_url


def handle_status(raw_args: str = "", **_kwargs) -> str:
    _ = raw_args
    report = run_doctor(mcp_url=mcp_url(), api_base=agent_api_base())
    return report.format_text()
