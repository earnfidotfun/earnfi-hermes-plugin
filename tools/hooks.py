"""Hermes ``pre_tool_call`` hooks for EarnFi spend tools."""

from __future__ import annotations

import json
import logging
from typing import Any

from .quote_x402 import format_accept_disclosure, parse_quote_json, pick_accept

logger = logging.getLogger(__name__)

_SIGN_TOOL = "earnfi_sign_x402"


def pre_tool_call_sign_x402(
    tool_name: str = "",
    args: dict | None = None,
    **kwargs: Any,
) -> dict[str, Any] | None:
    bare = (tool_name or kwargs.get("tool_name") or "").split(":")[-1]
    if bare != _SIGN_TOOL:
        return None

    a = args or kwargs.get("args") or {}
    payment_network = (a.get("payment_network") or a.get("network") or "").strip()
    quote_raw = a.get("quote_json")
    if not payment_network or quote_raw is None:
        return {
            "action": "block",
            "message": "earnfi_sign_x402 requires payment_network and quote_json from the MCP 402 response.",
            "rule_key": "earnfi:x402:invalid-args",
        }

    try:
        if isinstance(quote_raw, dict):
            quote = parse_quote_json(quote_raw)
        else:
            quote = parse_quote_json(str(quote_raw))
        accept = pick_accept(quote, payment_network)
        message = format_accept_disclosure(accept, payment_network)
    except (ValueError, json.JSONDecodeError) as exc:
        logger.warning("earnfi_sign_x402 pre_tool_call blocked: %s", exc)
        return {
            "action": "block",
            "message": f"Invalid x402 quote: {exc}",
            "rule_key": "earnfi:x402:invalid-quote",
        }

    return {
        "action": "approve",
        "message": message,
        "rule_key": f"earnfi:x402:{payment_network}",
    }
