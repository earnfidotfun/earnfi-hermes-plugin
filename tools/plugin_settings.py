"""Resolved plugin settings (set from ``register(ctx)``)."""

from __future__ import annotations

from typing import Any

from doctor.checks import DEFAULT_API_BASE, DEFAULT_MCP_URL

_PLUGIN_CTX: Any = None


def bind_plugin_context(ctx: Any) -> None:
    global _PLUGIN_CTX
    _PLUGIN_CTX = ctx


def mcp_url() -> str:
    if _PLUGIN_CTX is not None:
        value = _PLUGIN_CTX.get_config("mcp_url", DEFAULT_MCP_URL)
        if value:
            return str(value).strip()
    return DEFAULT_MCP_URL


def agent_api_base() -> str:
    if _PLUGIN_CTX is not None:
        value = _PLUGIN_CTX.get_config("agent_api_base", DEFAULT_API_BASE)
        if value:
            return str(value).strip().rstrip("/")
    return DEFAULT_API_BASE.rstrip("/")
