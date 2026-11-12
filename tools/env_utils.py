"""Minimal subprocess environments — never pass full Hermes ``os.environ`` to Node/npm."""

from __future__ import annotations

import os
import sys
from typing import Mapping

_PASSTHROUGH_KEYS = (
    "PATH",
    "PATHEXT",
    "HOME",
    "USERPROFILE",
    "HOMEDRIVE",
    "HOMEPATH",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "SYSTEMROOT",
    "SystemRoot",
    "WINDIR",
    "TEMP",
    "TMP",
    "TMPDIR",
    "APPDATA",
    "LOCALAPPDATA",
    "ProgramFiles",
    "ProgramFiles(x86)",
    "ComSpec",
    "NODE_OPTIONS",
    "npm_config_cache",
    "npm_config_registry",
    "npm_config_proxy",
    "npm_config_https_proxy",
    "npm_config_userconfig",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "NO_PROXY",
    "SOLANA_RPC_URL",
    "EARNFI_AGENT_API_BASE",
    "EARNFI_BASE_API_BASE",
    "EARNFI_OKX_API_BASE",
    "EARNFI_AGENT_NAME",
)


def minimal_subprocess_env(
    extra: Mapping[str, str] | None = None,
    *,
    include_agent_token: bool = False,
    wallet_env: str | None = None,
) -> dict[str, str]:
    """Build a stripped env for Node child processes."""
    out: dict[str, str] = {}
    for key in _PASSTHROUGH_KEYS:
        val = os.environ.get(key)
        if val:
            out[key] = val

    try:
        from agent.secret_scope import get_secret
    except ImportError:
        get_secret = None  # type: ignore[assignment,misc]

    if get_secret is not None and wallet_env:
        scoped = (get_secret(wallet_env, "") or "").strip()
        if scoped:
            out[wallet_env] = scoped
        if include_agent_token:
            token = (get_secret("EARNFI_AGENT_TOKEN", "") or "").strip()
            if token:
                out["EARNFI_AGENT_TOKEN"] = token

    if extra:
        for k, v in extra.items():
            if v is not None and str(v).strip():
                out[k] = str(v)

    # Never pass the removed wallet bypass flag.
    out.pop("EARNFI_HERMES_WALLET_CMD", None)
    return out


_NETWORK_SECRET_ENV = {
    "solana": "SOLANA_SECRET_KEY_B58",
    "base": "BASE_PRIVATE_KEY",
    "okx": "OKX_PRIVATE_KEY",
    "near": "NEAR_PRIVATE_KEY",
}

_CAIP_TO_SECRET = (
    ("solana:", "SOLANA_SECRET_KEY_B58"),
    ("eip155:8453", "BASE_PRIVATE_KEY"),
    ("eip155:196", "OKX_PRIVATE_KEY"),
    ("near:", "NEAR_PRIVATE_KEY"),
)


def wallet_secret_env_for_network(network: str) -> str | None:
    return _NETWORK_SECRET_ENV.get(network.lower())


def wallet_secret_env_for_payment_network(payment_network: str) -> str | None:
    p = (payment_network or "").strip().lower()
    for prefix, env_name in _CAIP_TO_SECRET:
        if p.startswith(prefix):
            return env_name
    return None


def has_configured_wallet_secret(env_name: str) -> bool:
    try:
        from agent.secret_scope import get_secret

        return bool((get_secret(env_name, "") or "").strip())
    except Exception:
        fallback = (os.environ.get(env_name) or "").strip()
        return bool(fallback)


def hermes_process_has_console() -> bool:
    """True only when this Python process has a real controlling terminal."""
    try:
        return bool(sys.stdin.isatty() and sys.stdout.isatty())
    except Exception:
        return False
