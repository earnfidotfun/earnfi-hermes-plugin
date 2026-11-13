"""Approval-gated x402 signing — returns payment_signature only (no private keys)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from .env_utils import minimal_subprocess_env, wallet_secret_env_for_payment_network
from .plugin_settings import verify_x402_replay
from .quote_x402 import (
    build_challenge_for_signer,
    parse_quote_json,
    pick_accept,
    verify_quote_replay,
)

_PLUGIN_ROOT = Path(__file__).resolve().parents[1]


def earnfi_sign_x402(args: dict, **_kwargs) -> str:
    """Build PAYMENT-SIGNATURE for an EarnFi 402 quote using configured plugin secrets."""
    a = args or {}
    payment_network = (a.get("payment_network") or a.get("network") or "").strip()
    quote_raw = a.get("quote_json")
    if not payment_network or quote_raw is None:
        return json.dumps(
            {
                "success": False,
                "error": "payment_network and quote_json are required",
            }
        )

    try:
        quote = (
            parse_quote_json(quote_raw)
            if isinstance(quote_raw, dict)
            else parse_quote_json(str(quote_raw))
        )
        chosen = pick_accept(quote, payment_network)
        if verify_x402_replay():
            verify_quote_replay(quote, payment_network, chosen)
        challenge = build_challenge_for_signer(quote, chosen)
    except (ValueError, json.JSONDecodeError) as exc:
        return json.dumps({"success": False, "error": "invalid_quote", "detail": str(exc)})

    wallet_env = wallet_secret_env_for_payment_network(payment_network)
    if not wallet_env:
        return json.dumps(
            {
                "success": False,
                "error": "unsupported_payment_network",
                "payment_network": payment_network,
            }
        )

    payload = {
        "payment_network": payment_network,
        "x402Version": challenge.get("x402Version", 2),
        "accepts": challenge.get("accepts") or [],
        "resource": challenge.get("resource"),
    }

    script = _PLUGIN_ROOT / "scripts" / "sign-x402.mjs"
    try:
        proc = subprocess.run(
            ["node", str(script)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            cwd=str(_PLUGIN_ROOT),
            env=minimal_subprocess_env(
                wallet_env=wallet_env,
                include_agent_token=True,
            ),
            timeout=120,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return json.dumps({"success": False, "error": "sign_failed", "detail": str(exc)})

    tail = (proc.stdout or "").strip().splitlines()
    if not tail:
        return json.dumps(
            {
                "success": False,
                "error": "empty_signer_output",
                "exit_code": proc.returncode,
            }
        )
    try:
        out = json.loads(tail[-1])
    except json.JSONDecodeError:
        return json.dumps({"success": False, "error": "invalid_signer_json"})

    if proc.returncode != 0 or not out.get("success"):
        return json.dumps(out)

    return json.dumps(
        {
            "success": True,
            "payment_signature": out.get("payment_signature"),
            "network": out.get("network"),
            "next_step": "Retry the same MCP tool with identical args + payment_signature.",
        }
    )
