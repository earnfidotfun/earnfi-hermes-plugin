""" /earnfi-wallet — register using plugin settings (no keygen without user terminal). """

from __future__ import annotations

import json
import os
import shlex
import subprocess
from pathlib import Path

from ..tools.env_utils import (
    has_configured_wallet_secret,
    minimal_subprocess_env,
    wallet_secret_env_for_network,
)
from ..tools.plugin_settings import agent_api_base

_PLUGIN_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = {
    "solana": "solana-setup.mjs",
    "base": "base-setup.mjs",
    "okx": "okx-setup.mjs",
    "near": "near-generate.mjs",
}

_NETWORK_API_ENV = {
    "solana": "EARNFI_AGENT_API_BASE",
    "base": "EARNFI_BASE_API_BASE",
    "okx": "EARNFI_OKX_API_BASE",
}

_API_BASE_DEFAULTS = {
    "solana": "https://app.earnfi.fun/api/ai-agent/v1",
    "base": "https://app.earnfi.fun/api/ai-agent/base/v1",
    "okx": "https://app.earnfi.fun/api/ai-agent/okx/v1",
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


def _no_secret_help(network: str, name: str) -> str:
    script = _SCRIPTS[network]
    return (
        f"# Wallet setup ({network})\n\n"
        "No wallet secret is configured in **Settings → Plugins → earnfi**.\n\n"
        "Hermes cannot generate private keys on gateway or headless hosts.\n\n"
        "**Create a key in your OS terminal**\n"
        f"```bash\n"
        f"cd path/to/earnfi-hermes-plugin\n"
        f'node scripts/{script} --name "{name}"\n'
        "```\n"
        "The secret prints **once on your console**. Paste it into plugin settings, then run\n"
        f"`/earnfi-wallet {network} --name \"{name}\"` again to register.\n"
    )


def handle_wallet(raw_args: str = "", **_kwargs) -> str:
    network, name, skip_register = _parse_wallet_args(raw_args)
    if not network or network not in _SCRIPTS:
        return (
            "# /earnfi-wallet\n\n"
            "Register a dedicated EarnFi agent wallet using a secret already in plugin settings.\n\n"
            "**Usage**\n"
            "- `/earnfi-wallet solana --name \"My Agent\"`\n"
            "- `/earnfi-wallet base --name \"My Agent\"`\n"
            "- `/earnfi-wallet near`\n"
            "- `/earnfi-wallet okx --name \"My Agent\"`\n\n"
            "New keys: generate in **your own terminal** (`node scripts/*-setup.mjs`), paste into "
            "**Settings → Plugins → earnfi**, then run this command to register.\n\n"
            "Natural-language requests (e.g. “generate a Solana wallet”) → guide the user through "
            "that flow; do **not** run `node scripts/*` from the terminal tool.\n"
        )

    secret_env = wallet_secret_env_for_network(network)
    if not secret_env or not has_configured_wallet_secret(secret_env):
        return _no_secret_help(network, name)

    script = _PLUGIN_ROOT / "scripts" / _SCRIPTS[network]
    if not script.is_file():
        return json.dumps({"success": False, "error": "script_missing", "network": network})

    cmd = ["node", str(script), "--name", name]
    if skip_register and network != "near":
        cmd.append("--skip-register")

    api_env_key = _NETWORK_API_ENV.get(network)
    extra: dict[str, str] = {"EARNFI_AGENT_NAME": name}
    if api_env_key and network == "solana":
        extra[api_env_key] = agent_api_base()
    elif api_env_key:
        extra[api_env_key] = _API_BASE_DEFAULTS[network]

    env = minimal_subprocess_env(
        extra=extra,
        wallet_env=secret_env,
        include_agent_token=True,
    )

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
            data = {"raw_stdout_tail": stdout[-240:]}

    if proc.returncode == 2 and data.get("error") == "tty_required_for_keygen":
        return _no_secret_help(network, name)

    if proc.returncode != 0:
        summary = _public_summary(data) if data else {}
        summary["success"] = False
        summary["exit_code"] = proc.returncode
        return json.dumps(summary, indent=2)

    summary = _public_summary(data)
    summary["success"] = True
    lines = [
        f"# EarnFi wallet ({network})",
        "",
        f"- Address / account: `{summary.get('wallet_address') or summary.get('account_id', '—')}`",
        f"- Registered: **{summary.get('registered', False)}**",
        "",
        "Continue with MCP `mcp__earnfi_api__…` tools for jobs and x402 payments.",
    ]
    return "\n".join(lines)
