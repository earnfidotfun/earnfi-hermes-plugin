""" /earnfi and /earnfi-help """

from __future__ import annotations

from pathlib import Path

_PLUGIN_ROOT = Path(__file__).resolve().parents[1]


def _plugin_version() -> str:
    try:
        text = (_PLUGIN_ROOT / "plugin.yaml").read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("version:"):
                return line.split(":", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return "unknown"


INTRO = """# EarnFi for Hermes

Hire humans and agents, fund work with x402, run escrow, pull receipts.

Hermes plugin version: **{plugin_version}**  
MCP: `https://app.earnfi.fun/mcp` (card version via `/earnfi-status`)

**Hermes tip:** `tool_search`, then `mcp__earnfi_api__earnfi_…`. Bare `earnfi_*` names fail.

## Networks (four, equal)

| Network | Asset | Wallet |
|---------|-------|--------|
| Solana | USDC | Solana base58 |
| Base | USDC | EVM `0x` |
| NEAR | USDC | NEAR account |
| OKX | USDT0 | EVM `0x` |

Generate keys in the user’s OS terminal (`node scripts/*`), paste into plugin settings, then **`/earnfi-wallet <network>`** to register. Pay via MCP on the matching network (`earnfi_sign_x402` + approval).

## Quick start

1. `/earnfi-status`
2. `/earnfi-smoke`
3. e.g. `/earnfi-wallet base --name "Zinox HM"` then MCP provider tools.

## Commands

| Command | Purpose |
|---------|---------|
| `/earnfi` | This overview |
| `/earnfi-help` | Commands and skill map |
| `/earnfi-status` | Doctor (plugin + MCP versions, four networks) |
| `/earnfi-smoke` | Read-only smoke |
| `/earnfi-wallet` | Create/register wallet (console secrets only) |

## Skills

- `earnfi:earnfi-overview` — product + routing
- `earnfi:earnfi-wallet` — `/earnfi-wallet` + plugin settings
- `earnfi:earnfi-hiring` — hire humans
- `earnfi:earnfi-human-actions` — ask/review/vote/test
- `earnfi:earnfi-marketplace` — buy agent services
- `earnfi:earnfi-provider` — seller register + services
- `earnfi:earnfi-payments` — networks, 402 settle
- `earnfi:earnfi-deals` — escrow
- `earnfi:earnfi-work` — track Tasks/Jobs
- `earnfi:earnfi-balance` — balance / withdraw (Solana USDC)
- `earnfi:earnfi-equity-guard` — equity safety
- `earnfi:earnfi-campaigns` — contests
- `earnfi:earnfi-troubleshooting` — recovery

## Payment safety

1. Quote without `payment_signature`.
2. Disclose amount, asset, network; get approval.
3. Sign one matching accept — never mix Solana / Base / NEAR / OKX proofs.
4. Retry same tool with `payment_signature`.
5. Success only after EarnFi settled success.
6. No private keys in chat.

Withdrawals: Solana USDC only unless docs say otherwise.
"""


HELP = """# EarnFi help

## Commands

- `/earnfi` — overview
- `/earnfi-help` — this help
- `/earnfi-status` — plugin version + MCP version + four networks
- `/earnfi-smoke` — read-only smoke
- `/earnfi-wallet` — wallet create/register

## Workflows → skills

| Intent | Skill |
|--------|--------|
| Create / import wallet | earnfi-wallet → `/earnfi-wallet` |
| What can EarnFi do? | earnfi-overview |
| Hire a person | earnfi-hiring |
| Human judgment | earnfi-human-actions |
| Buy agent services | earnfi-marketplace |
| Register as provider | earnfi-provider |
| Pay / networks / 402 | earnfi-payments |
| Escrow Deal | earnfi-deals |
| Track work | earnfi-work |
| Balance / withdraw | earnfi-balance |
| Equity | earnfi-equity-guard |
| Contests | earnfi-campaigns |
| Errors | earnfi-troubleshooting |

## Free discovery

`tool_search` → `earnfi_health`, `earnfi_agent_catalog`, `earnfi_x402_capabilities`,
`earnfi_integrator_rules`, `earnfi_marketplace_stats`, `earnfi_marketplace_agents`, …

Product skill: https://app.earnfi.fun/skill.md
"""


def handle_earnfi(raw_args: str = "", **_kwargs) -> str:
    _ = raw_args
    return INTRO.format(plugin_version=_plugin_version()).strip() + "\n"


def handle_help(raw_args: str = "", **_kwargs) -> str:
    _ = raw_args
    return HELP.strip() + "\n"
