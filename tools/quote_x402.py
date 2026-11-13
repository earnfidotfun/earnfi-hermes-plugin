"""Parse and verify EarnFi x402 quotes before signing."""

from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.request
from typing import Any
from urllib.parse import urljoin, urlparse

from .plugin_settings import agent_api_base, mcp_url

_DEFAULT_HOSTS = frozenset({"app.earnfi.fun", "earnfi.fun", "docs.earnfi.fun"})


def _allowed_hosts() -> set[str]:
    hosts = set(_DEFAULT_HOSTS)
    for raw in (mcp_url(), agent_api_base()):
        parsed = urlparse(str(raw).strip())
        if parsed.hostname:
            hosts.add(parsed.hostname.lower())
    return hosts


def _unwrap_quote_body(raw: dict[str, Any]) -> dict[str, Any]:
    body = dict(raw)
    for key in ("paymentRequired", "x402", "payment_required"):
        nested = body.get(key)
        if isinstance(nested, dict):
            for k, v in nested.items():
                if k not in body or body[k] in (None, [], {}):
                    body[k] = v
    return body


def parse_quote_json(quote_json: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(quote_json, str):
        quote_json = json.loads(quote_json)
    if not isinstance(quote_json, dict):
        raise ValueError("quote_json must be a JSON object")
    return _unwrap_quote_body(quote_json)


def accepts_fingerprint(accepts: list[Any]) -> str:
    canonical = json.dumps(accepts, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def pick_accept(quote: dict[str, Any], payment_network: str) -> dict[str, Any]:
    accepts = quote.get("accepts")
    if not isinstance(accepts, list) or not accepts:
        raise ValueError("quote missing accepts[]")
    net = payment_network.strip().lower()
    for item in accepts:
        if not isinstance(item, dict):
            continue
        item_net = str(item.get("network") or "").strip().lower()
        if item_net == net or item_net.startswith(net) or net.startswith(item_net):
            return item
    raise ValueError(f"no accept matching payment_network {payment_network!r}")


def format_accept_disclosure(accept: dict[str, Any], payment_network: str) -> str:
    amount = accept.get("maxAmountRequired") or accept.get("amount") or accept.get("max_amount")
    asset = accept.get("asset") or accept.get("currency") or "USDC"
    pay_to = accept.get("payTo") or accept.get("recipient") or accept.get("pay_to")
    network = accept.get("network") or payment_network
    return (
        "Approve EarnFi x402 payment?\n"
        f"- Network: {network}\n"
        f"- Amount: {amount}\n"
        f"- Asset: {asset}\n"
        f"- Pay to: {pay_to}"
    )


def _earnfi_origin() -> str:
    parsed = urlparse(mcp_url().strip())
    if parsed.scheme and parsed.netloc:
        return f"{parsed.scheme}://{parsed.netloc}"
    return "https://app.earnfi.fun"


def safe_replay_url(quote: dict[str, Any]) -> str | None:
    """Build an https URL on an allowed EarnFi host — never trust model headers/method."""
    resource = quote.get("resource")
    if not isinstance(resource, dict):
        return None
    raw = (resource.get("url") or resource.get("href") or resource.get("path") or "").strip()
    if not raw:
        return None
    if raw.startswith("/"):
        raw = urljoin(_earnfi_origin() + "/", raw.lstrip("/"))
    parsed = urlparse(raw)
    if parsed.scheme != "https":
        raise ValueError("quote resource must use https")
    host = (parsed.hostname or "").lower()
    if host not in _allowed_hosts():
        raise ValueError(f"quote resource host {host!r} is not an allowed EarnFi host")
    return raw


def verify_quote_replay(quote: dict[str, Any], payment_network: str, chosen_accept: dict[str, Any]) -> None:
    """GET the allowlisted EarnFi URL only; require the same single accept fingerprint."""
    url = safe_replay_url(quote)
    if not url:
        return

    req = urllib.request.Request(url, method="GET", headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:  # noqa: S310
            status = getattr(resp, "status", None) or resp.getcode()
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        status = exc.code
        body = (exc.read() or b"").decode("utf-8", errors="replace")
        if status not in (402, 403):
            raise ValueError(f"quote replay returned HTTP {status}, expected 402") from exc
    except urllib.error.URLError as exc:
        raise ValueError(f"quote replay failed: {exc}") from exc

    if status not in (402, 403):
        raise ValueError(f"quote replay returned HTTP {status}, expected 402")

    try:
        fresh = _unwrap_quote_body(json.loads(body))
    except json.JSONDecodeError as exc:
        raise ValueError("quote replay body is not JSON") from exc

    fresh_accept = pick_accept(fresh, payment_network)
    if accepts_fingerprint([chosen_accept]) != accepts_fingerprint([fresh_accept]):
        raise ValueError("live 402 accept does not match the approved quote")


def build_challenge_for_signer(quote: dict[str, Any], chosen_accept: dict[str, Any]) -> dict[str, Any]:
    return {
        "x402Version": quote.get("x402Version") or quote.get("x402_version") or 2,
        "accepts": [chosen_accept],
        "resource": quote.get("resource"),
    }
