"""EarnFi for Hermes — native plugin registration.

Execution of jobs, payments, escrow and marketplace operations is performed
exclusively through the hosted EarnFi MCP server (see mcp.json). This package
adds Hermes-native commands, diagnostics, workflow skills and trust posture.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from doctor.checks import DEFAULT_API_BASE, DEFAULT_MCP_URL, run_doctor
from hermes_commands import handle_earnfi, handle_help, handle_smoke, handle_status

logger = logging.getLogger(__name__)

_PLUGIN_ROOT = Path(__file__).resolve().parent
_SKILLS_DIR = _PLUGIN_ROOT / "skills"

EARNFI_DOCTOR_SCHEMA = {
    "name": "earnfi_doctor",
    "description": (
        "Run EarnFi connection diagnostics: MCP reachability, server-card tool "
        "discovery, Agent API health, catalog and payment rails. Read-only; "
        "never settles payments. Use when the user asks if EarnFi is connected "
        "or when troubleshooting."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "format": {
                "type": "string",
                "enum": ["text", "json"],
                "description": "Response format (default text).",
            }
        },
        "required": [],
    },
}


def earnfi_doctor(args: dict, **_kwargs) -> str:
    """Tool handler — always returns a JSON string for Hermes tools."""
    fmt = (args or {}).get("format") or "text"
    report = run_doctor(mcp_url=DEFAULT_MCP_URL, api_base=DEFAULT_API_BASE)
    if str(fmt).lower() == "json":
        return json.dumps(report.to_dict())
    return json.dumps(
        {
            "success": report.overall_ok,
            "report_text": report.format_text(),
            "tool_count": report.tool_count,
            "server_version": report.server_version,
            "readonly_tools": report.readonly_tools,
            "write_tools": report.write_tools,
        }
    )


def register(ctx):
    """Wire Hermes tools, slash commands and bundled skills."""
    ctx.register_tool(
        name="earnfi_doctor",
        toolset="earnfi",
        schema=EARNFI_DOCTOR_SCHEMA,
        handler=earnfi_doctor,
    )

    ctx.register_command(
        "earnfi",
        handler=handle_earnfi,
        description="EarnFi overview — hire humans, fund work, receipts",
    )
    ctx.register_command(
        "earnfi-help",
        handler=handle_help,
        description="EarnFi commands, skills and workflows",
    )
    ctx.register_command(
        "earnfi-status",
        handler=handle_status,
        description="Live EarnFi connection and capability doctor",
    )
    ctx.register_command(
        "earnfi-smoke",
        handler=handle_smoke,
        description="Read-only EarnFi integration smoke tests",
    )

    if _SKILLS_DIR.is_dir():
        for child in sorted(_SKILLS_DIR.iterdir()):
            skill_md = child / "SKILL.md"
            if child.is_dir() and skill_md.is_file():
                try:
                    ctx.register_skill(child.name, skill_md)
                except Exception as exc:  # noqa: BLE001 — don't disable the whole plugin
                    logger.warning("EarnFi skill registration skipped for %s: %s", child.name, exc)

    logger.info(
        "EarnFi plugin registered (doctor tool, 4 slash commands, skills from %s)",
        _SKILLS_DIR,
    )
