"""Approval-gated x402 signing — returns payment_signature only (no private keys)."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

_PLUGIN_ROOT = Path(__file__).resolve().parents[1]


def earnfi_sign_x402(args: dict, **_kwargs) -> str:
    """Build PAYMENT-SIGNATURE for an EarnFi 402 quote using configured plugin secrets."""
    a = args or {}
    payment_network = (a.get("payment_network") or a.get("network") or "").strip()
    accepts = a.get("accepts")
    if not payment_network or not accepts:
        return json.dumps(
            {
                "success": False,
                "error": "payment_network and accepts are required",
            }
        )

    payload = {
        "payment_network": payment_network,
        "x402Version": a.get("x402_version", 2),
        "accepts": accepts,
        "resource": a.get("resource"),
    }

    script = _PLUGIN_ROOT / "scripts" / "sign-x402.mjs"
    try:
        proc = subprocess.run(
            ["node", str(script)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            cwd=str(_PLUGIN_ROOT),
            env=os.environ.copy(),
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

    # Never forward stderr; stdout must not contain secrets.
    return json.dumps(
        {
            "success": True,
            "payment_signature": out.get("payment_signature"),
            "network": out.get("network"),
            "next_step": "Retry the same MCP tool with identical args + payment_signature.",
        }
    )
