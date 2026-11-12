""" /earnfi-wallet — create/register agent wallet (secrets on user console only). """

from __future__ import annotations

import json
import os
import shlex
import subprocess
from pathlib import Path

_PLUGIN_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = {
    "solana": "solana-setup.mjs",
    "base": "base-setup.mjs",
    "okx": "okx-setup.mjs",
    "near": "near-generate.mjs",
}


def _parse_wallet_args(raw: str) -> tuple[str | None, str, bool]:
    parts = shlex.split(raw or "", posix=os.name != "nt")
    network: str | None = None
    name = os.environ.get("EARNFI_AGENT_NAME", "earnfi-agent")
    skip_register = False
    i = 0
    while i < len(parts):
        p = parts[i].lower()
        if p in _SCRIPTS:
            network = p
        elif p in ("--network", "-n") and i + 1 < len(parts):
            network = parts[i + 1].lower()
            i += 1
        elif p == "--name" and i + 1 < len(parts):
            name = parts[i + 1]
            i += 1
        elif p == "--skip-register":
            skip_register = True
        i += 1
    return network, name, skip_register


def _public_summary(data: dict) -> dict:
    keep = (
        "network",
        "caip2",
        "wallet_address",
        "account_id",
        "public_key",
        "agent_name",
        "registered",
        "secret_env",
        "secret_saved_via",
        "token_env",
        "token_saved_via",
        "error",
        "guidance",
    )
    return {k: data[k] for k in keep if k in data}


def handle_wallet(raw_args: str = "", **_kwargs) -> str:
    network, name, skip_register = _parse_wallet_args(raw_args)
    if not network or network not in _SCRIPTS:
        return (
            "# /earnfi-wallet\n\n"
            "Create a dedicated EarnFi agent wallet (keys shown **once on your console**, not in chat).\n\n"
            "**Usage**\n"
            "- `/earnfi-wallet solana --name \"My Agent\"`\n"
            "- `/earnfi-wallet base --name \"My Agent\"`\n"
            "- `/earnfi-wallet near`\n"
            "- `/earnfi-wallet okx --name \"My Agent\"`\n\n"
            "After generation, paste the secret into **Settings → Plugins → earnfi**.\n\n"
            "Natural-language requests (e.g. “generate a Solana wallet”) → run this command for "
            "the matching network; do **not** use the terminal tool to run `node scripts/*`.\n"
        )

    script = _PLUGIN_ROOT / "scripts" / _SCRIPTS[network]
    if not script.is_file():
        return json.dumps({"success": False, "error": "script_missing", "network": network})

    cmd = ["node", str(script), "--name", name]
    if skip_register and network != "near":
        cmd.append("--skip-register")

    env = os.environ.copy()
    env["EARNFI_HERMES_WALLET_CMD"] = "1"

    try:
        proc = subprocess.run(
            cmd,
            cwd=str(_PLUGIN_ROOT),
            capture_output=True,
            text=True,
            env=env,
            timeout=300,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return json.dumps({"success": False, "error": "wallet_command_failed", "detail": str(exc)})

    stdout = (proc.stdout or "").strip()
    data: dict = {}
    if stdout:
        try:
            data = json.loads(stdout.splitlines()[-1])
        except json.JSONDecodeError:
            data = {"raw_stdout_tail": stdout[-500:]}

    if proc.returncode == 2 and data.get("error") == "tty_required_for_keygen":
        return (
            f"# Wallet setup ({network})\n\n"
            "Could not generate keys in a non-interactive context.\n\n"
            "Run **`/earnfi-wallet "
            f"{network} --name \"{name}\"`** from the Hermes command line (not via terminal `node …`), "
            "or run the script in your own shell, then paste the secret into "
            "**Settings → Plugins → earnfi**.\n"
        )

    if proc.returncode != 0:
        summary = _public_summary(data) if data else {}
        summary["success"] = False
        summary["exit_code"] = proc.returncode
        if proc.stderr and "EARNFI_HERMES_STORE" not in proc.stderr:
            summary["stderr_hint"] = "See Hermes logs; secrets are never returned here."
        return json.dumps(summary, indent=2)

    summary = _public_summary(data)
    summary["success"] = True
    lines = [
        f"# EarnFi wallet ({network})",
        "",
        "If a new secret was generated, it was shown **once on your system console** — "
        "paste it into **Settings → Plugins → earnfi**.",
        "",
        f"- Address / account: `{summary.get('wallet_address') or summary.get('account_id', '—')}`",
        f"- Registered: **{summary.get('registered', False)}**",
        "",
        "Continue with MCP `mcp__earnfi_api__…` tools for jobs and x402 payments.",
    ]
    if summary.get("token_saved_via"):
        lines.insert(4, "- New `EARNFI_AGENT_TOKEN` was also shown on the console once.")
    return "\n".join(lines)
