"""Live diagnostics against EarnFi MCP discovery + Agent API surfaces.

Reports real HTTP outcomes. Never invents a green status.
Settlement success is never inferred here — diagnostics are read-only.
"""

from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass, field, asdict
from typing import Any, Optional

DEFAULT_MCP_URL = "https://app.earnfi.fun/mcp"
DEFAULT_API_BASE = "https://app.earnfi.fun/api/ai-agent/v1"
SERVER_CARD_URL = "https://app.earnfi.fun/.well-known/mcp/server-card.json"
OKX_HEALTH_URL = "https://app.earnfi.fun/api/ai-agent/okx/v1/health"

# Core free reads the smoke test expects to exist on the live card.
SMOKE_REQUIRED_TOOLS = (
    "earnfi_health",
    "earnfi_agent_catalog",
    "earnfi_payment_rails",
    "earnfi_marketplace_stats",
    "earnfi_find_work",
    "earnfi_manual_create",
    "earnfi_human_action_create",
    "earnfi_hire_agent",
    "earnfi_agent_deal_create",
    "earnfi_get_receipt",
)


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str
    data: Optional[dict[str, Any]] = None


@dataclass
class DoctorReport:
    overall_ok: bool
    mcp_url: str
    api_base: str
    checks: list[CheckResult] = field(default_factory=list)
    tool_count: int = 0
    readonly_tools: int = 0
    write_tools: int = 0
    server_version: str = ""
    missing_smoke_tools: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "overall_ok": self.overall_ok,
            "mcp_url": self.mcp_url,
            "api_base": self.api_base,
            "tool_count": self.tool_count,
            "readonly_tools": self.readonly_tools,
            "write_tools": self.write_tools,
            "server_version": self.server_version,
            "missing_smoke_tools": self.missing_smoke_tools,
            "checks": [asdict(c) for c in self.checks],
        }

    def format_text(self) -> str:
        lines = [
            "EarnFi system status",
            "====================",
            f"Overall: {'OK' if self.overall_ok else 'ISSUES DETECTED'}",
            f"MCP endpoint: {self.mcp_url}",
            f"Agent API base: {self.api_base}",
            "",
        ]
        for c in self.checks:
            mark = "PASS" if c.ok else "FAIL"
            lines.append(f"[{mark}] {c.name}: {c.detail}")
        lines.append("")
        if self.tool_count:
            lines.append(
                f"Tool discovery: {self.tool_count} tools "
                f"({self.readonly_tools} read-only, {self.write_tools} write/payment)"
            )
        if self.server_version:
            lines.append(f"Server card version: {self.server_version}")
        if self.missing_smoke_tools:
            lines.append(
                "Missing expected tools: " + ", ".join(self.missing_smoke_tools)
            )
        lines.append("")
        lines.append(
            "Payment note: diagnostics never settle funds. "
            "Treat a job as funded only after EarnFi confirms settlement "
            "(success without requires_payment), never from a signature alone."
        )
        lines.append(
            "Security: MCP server trust is untrusted — write/payment tools "
            "require Hermes approval. EarnFi server-side limits remain authoritative."
        )
        return "\n".join(lines)


def _http_get_json(url: str, timeout: float = 20.0) -> tuple[int, Any]:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "earnfi-hermes-plugin/1.0.0",
        },
        method="GET",
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            status = getattr(resp, "status", 200)
            try:
                return status, json.loads(body)
            except json.JSONDecodeError:
                return status, {"raw": body[:500]}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace") if e.fp else ""
        try:
            payload = json.loads(raw) if raw else {"error": str(e)}
        except json.JSONDecodeError:
            payload = {"error": str(e), "raw": raw[:500]}
        return e.code, payload
    except Exception as e:  # noqa: BLE001 — surface network failures to the user
        return 0, {"error": f"{type(e).__name__}: {e}"}


def _http_probe(url: str, timeout: float = 15.0) -> tuple[bool, str]:
    """Best-effort reachability probe (GET). MCP Streamable HTTP may not be a plain JSON GET."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "earnfi-hermes-plugin/1.0.0", "Accept": "*/*"},
        method="GET",
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            status = getattr(resp, "status", 200)
            return True, f"HTTP {status}"
    except urllib.error.HTTPError as e:
        # 4xx/405 still proves the host answered — useful for MCP endpoints.
        if 400 <= e.code < 500:
            return True, f"HTTP {e.code} (endpoint reachable)"
        return False, f"HTTP {e.code}: {e.reason}"
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"


def run_doctor(
    *,
    mcp_url: str = DEFAULT_MCP_URL,
    api_base: str = DEFAULT_API_BASE,
) -> DoctorReport:
    checks: list[CheckResult] = []
    tool_count = 0
    readonly = 0
    write = 0
    version = ""
    missing: list[str] = []

    reachable, detail = _http_probe(mcp_url)
    checks.append(
        CheckResult(
            name="MCP endpoint reachability",
            ok=reachable,
            detail=detail if reachable else f"Unreachable — {detail}",
        )
    )

    status, card = _http_get_json(SERVER_CARD_URL)
    if status == 200 and isinstance(card, dict) and "tools" in card:
        tools = card.get("tools") or []
        tool_count = len(tools)
        names = []
        for t in tools:
            if not isinstance(t, dict):
                continue
            names.append(str(t.get("name") or ""))
            ann = t.get("annotations") or {}
            if ann.get("readOnlyHint") is True:
                readonly += 1
            else:
                write += 1
        info = card.get("serverInfo") or {}
        version = str(info.get("version") or "")
        missing = [n for n in SMOKE_REQUIRED_TOOLS if n not in names]
        checks.append(
            CheckResult(
                name="MCP server card / tool discovery",
                ok=tool_count > 0 and not missing,
                detail=(
                    f"Discovered {tool_count} tools "
                    f"({readonly} read-only / {write} write). "
                    + (
                        f"Missing: {', '.join(missing)}"
                        if missing
                        else "Required smoke tools present."
                    )
                ),
                data={"tool_count": tool_count, "version": version},
            )
        )
    else:
        err = card.get("error") if isinstance(card, dict) else card
        checks.append(
            CheckResult(
                name="MCP server card / tool discovery",
                ok=False,
                detail=f"Failed to load server card (HTTP {status}): {err}",
            )
        )

    # Solana rail has no dedicated /health — EarnFi MCP earnfi_health aggregates /rails + /catalog.
    c_status, c_body = _http_get_json(api_base.rstrip("/") + "/catalog")
    catalog_ok = c_status == 200 and isinstance(c_body, dict)
    checks.append(
        CheckResult(
            name="Agent catalog",
            ok=catalog_ok,
            detail=f"HTTP {c_status}: {_short(c_body)}",
            data={"keys": list(c_body.keys())[:12]} if isinstance(c_body, dict) else None,
        )
    )

    r_status, r_body = _http_get_json(api_base.rstrip("/") + "/rails")
    rails_ok = r_status == 200 and isinstance(r_body, dict)
    checks.append(
        CheckResult(
            name="Payment rails",
            ok=rails_ok,
            detail=f"HTTP {r_status}: {_short(r_body)}",
            data=r_body if isinstance(r_body, dict) else None,
        )
    )

    aggregate_ok = catalog_ok and rails_ok
    checks.append(
        CheckResult(
            name="Solana Agent API health (catalog+rails)",
            ok=aggregate_ok,
            detail=(
                "OK — mirrors MCP earnfi_health (GET /catalog + GET /rails)."
                if aggregate_ok
                else f"Failed — catalog HTTP {c_status}, rails HTTP {r_status}."
            ),
            data={"catalog": c_status, "rails": r_status},
        )
    )

    o_status, o_body = _http_get_json(OKX_HEALTH_URL)
    # OKX rail may be disabled — report truthfully without failing overall alone.
    okx_ok = o_status == 200
    checks.append(
        CheckResult(
            name="OKX rail health (optional)",
            ok=okx_ok,
            detail=(
                f"HTTP {o_status}: {_short(o_body)}"
                if okx_ok
                else f"Not available or unreachable (HTTP {o_status}): {_short(o_body)}"
            ),
        )
    )

    checks.append(
        CheckResult(
            name="Authentication",
            ok=True,
            detail=(
                "Public discovery endpoints do not require Agent-Token. "
                "Paid creates are pay-first (x402); Agent-Token is optional and may bind "
                "from the paying wallet on settle. Configure secrets via Hermes env/secret "
                "scope only — never embed keys in the plugin."
            ),
        )
    )

    # Overall: core Solana discovery path must pass; OKX optional.
    core_names = {
        "MCP endpoint reachability",
        "MCP server card / tool discovery",
        "Solana Agent API health (catalog+rails)",
        "Agent catalog",
        "Payment rails",
    }
    overall = all(c.ok for c in checks if c.name in core_names)

    return DoctorReport(
        overall_ok=overall,
        mcp_url=mcp_url,
        api_base=api_base,
        checks=checks,
        tool_count=tool_count,
        readonly_tools=readonly,
        write_tools=write,
        server_version=version,
        missing_smoke_tools=missing,
    )


def run_smoke(
    *,
    mcp_url: str = DEFAULT_MCP_URL,
    api_base: str = DEFAULT_API_BASE,
) -> DoctorReport:
    """Read-only integration smoke — same checks as doctor; naming for the slash command."""
    return run_doctor(mcp_url=mcp_url, api_base=api_base)


def _short(body: Any, limit: int = 180) -> str:
    try:
        text = json.dumps(body, ensure_ascii=False) if not isinstance(body, str) else body
    except TypeError:
        text = str(body)
    text = text.replace("\n", " ")
    return text if len(text) <= limit else text[: limit - 3] + "..."
