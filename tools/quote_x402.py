"""Parse and verify EarnFi x402 quotes before signing."""

from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.request
from typing import Any


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


def verify_quote_replay(quote: dict[str, Any], payment_network: str) -> None:
    """When the quote includes a resource URL, re-fetch and require matching accepts."""
    resource = quote.get("resource")
    if not isinstance(resource, dict):
        return
    url = (resource.get("url") or resource.get("href") or "").strip()
    if not url:
        return
    method = (resource.get("method") or "GET").upper()
    headers = {"Accept": "application/json"}
    extra = resource.get("headers")
    if isinstance(extra, dict):
        for k, v in extra.items():
            if isinstance(k, str) and v is not None:
                headers[k] = str(v)

    req = urllib.request.Request(url, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:  # noqa: S310 — user-attested EarnFi quote URL
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

    local_fp = accepts_fingerprint(quote.get("accepts") or [])
    fresh_accepts = fresh.get("accepts") or []
    fresh_fp = accepts_fingerprint(fresh_accepts)
    if local_fp != fresh_fp:
        raise ValueError("quote accepts[] no longer match live 402 response")

    pick_accept(fresh, payment_network)


def build_challenge_for_signer(quote: dict[str, Any]) -> dict[str, Any]:
    return {
        "x402Version": quote.get("x402Version") or quote.get("x402_version") or 2,
        "accepts": quote.get("accepts") or [],
        "resource": quote.get("resource"),
    }
