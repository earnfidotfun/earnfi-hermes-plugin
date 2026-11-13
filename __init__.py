"""EarnFi for Hermes — native plugin registration.

Execution of jobs, payments, escrow and marketplace operations is performed
exclusively through the hosted EarnFi MCP server (see mcp.json). This package
adds Hermes-native commands, diagnostics, workflow skills and trust posture.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from .doctor.checks import PEER_NETWORKS, run_doctor
from .hermes_commands import handle_earnfi, handle_help, handle_smoke, handle_status, handle_wallet
from .tools.hooks import pre_tool_call_sign_x402
from .tools.plugin_settings import agent_api_base, bind_plugin_context, mcp_url
from .tools.sign_x402 import earnfi_sign_x402

logger = logging.getLogger(__name__)

_PLUGIN_ROOT = Path(__file__).resolve().parent
_SKILLS_DIR = _PLUGIN_ROOT / "skills"

EARNFI_SIGN_X402_SCHEMA = {
    "name": "earnfi_sign_x402",
    "description": (
        "Build an x402 PAYMENT-SIGNATURE for an EarnFi 402 quote using wallet secrets "
        "configured in Settings → Plugins → earnfi. Pass the full MCP 402 JSON as quote_json. "
        "Returns payment_signature only — never private keys. Hermes approval is required "
        "before signing. After signing, retry the same mcp__earnfi_api__ tool with payment_signature."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "payment_network": {
                "type": "string",
                "description": "CAIP-2 network from the quote accept (e.g. solana:5eykt4…, eip155:8453).",
            },
            "quote_json": {
                "type": "string",
                "description": "Full JSON body from the EarnFi MCP 402 response (unchanged).",
            },
        },
        "required": ["payment_network", "quote_json"],
    },
}

EARNFI_DOCTOR_SCHEMA = {
    "name": "earnfi_doctor",
    "description": (
        "Run EarnFi connection diagnostics: Hermes plugin version, MCP server "
        "card version, four networks (Solana/Base/NEAR/OKX), tool discovery, "
        "Agent API health. Read-only; never settles payments. Use for version "
        "checks, connectivity, or troubleshooting."
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
    report = run_doctor(mcp_url=mcp_url(), api_base=agent_api_base())
    if str(fmt).lower() == "json":
        return json.dumps(report.to_dict())
    return json.dumps(
        {
            "success": report.overall_ok,
            "report_text": report.format_text(),
            "plugin_version": report.plugin_version,
            "tool_count": report.tool_count,
            "server_version": report.server_version,
            "peer_networks": list(PEER_NETWORKS),
            "readonly_tools": report.readonly_tools,
            "write_tools": report.write_tools,
        }
    )


def register(ctx):
    """Wire Hermes tools, slash commands and bundled skills."""
    bind_plugin_context(ctx)

    ctx.register_hook("pre_tool_call", pre_tool_call_sign_x402)

    ctx.register_tool(
        name="earnfi_doctor",
        toolset="earnfi",
        schema=EARNFI_DOCTOR_SCHEMA,
        handler=earnfi_doctor,
    )
    ctx.register_tool(
        name="earnfi_sign_x402",
        toolset="earnfi",
        schema=EARNFI_SIGN_X402_SCHEMA,
        handler=earnfi_sign_x402,
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
    ctx.register_command(
        "earnfi-wallet",
        handler=handle_wallet,
        description="Register agent wallet from plugin settings (keygen in user terminal only)",
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
        "EarnFi plugin registered (doctor + sign tools, 5 slash commands, skills from %s)",
        _SKILLS_DIR,
    )
