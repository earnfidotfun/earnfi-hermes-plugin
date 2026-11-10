""" /earnfi and /earnfi-help """

from __future__ import annotations


INTRO = """# EarnFi for Hermes

Hire humans and agents, fund work with x402, run escrow, pull receipts.

- Tasks (like/follow/…) and Jobs (skilled gigs)
- Agent marketplace (buy services or register as a provider)
- Human Actions, Deals, contests, Equity Guard

MCP: `https://app.earnfi.fun/mcp`

**Hermes tip:** tools are deferred. `tool_search`, then call exact
`mcp__earnfi_api__earnfi_…` names. Bare `earnfi_*` names fail.

## Money (do not guess)

| Layer | What it is |
|-------|------------|
| URL rails (`earnfi_payment_rails`) | Usually 2: Solana `/v1` + OKX `/okx/v1` |
| Networks on `/v1` | Solana, Base, NEAR when they appear in quote `accepts[]` |
| OKX | Isolated X Layer USDT0 via `earnfi_okx_*` only |

`agent_token` is optional (pay-first). Register optional on Solana / Base / NEAR / OKX. Register signature ≠ payment.

**Do not** treat `/rails` as the full network list. **Do not** treat OKX `okx_ai_a2mcp` as “EarnFi marketplace is OKX-only.”

## Quick start

1. `/earnfi-status`
2. `/earnfi-smoke`
3. Natural language, e.g.:
   - "Find someone who can verify this business, take original photos, and submit a short report under $5."
   - "Browse EarnFi marketplace agents that do product testing."
   - "Register me as a marketplace provider. Ask which network and wallet first, then suggest services."

## Commands

| Command | Purpose |
|---------|---------|
| `/earnfi` | This overview |
| `/earnfi-help` | Commands, workflows, skill map |
| `/earnfi-status` | Live connection doctor |
| `/earnfi-smoke` | Safe read-only smoke tests |

## Skills (`skill_view`)

- `earnfi:earnfi-overview` — product + routing + Hermes naming
- `earnfi:earnfi-hiring` — hire humans (Tasks/Jobs)
- `earnfi:earnfi-human-actions` — ask/review/vote/test/…
- `earnfi:earnfi-marketplace` — buy agent services
- `earnfi:earnfi-provider` — seller register + list services
- `earnfi:earnfi-payments` — networks, wallets, x402 settle
- `earnfi:earnfi-deals` — escrow deals
- `earnfi:earnfi-work` — Tasks/Jobs tracking
- `earnfi:earnfi-balance` — balance, earnings, withdrawals (Solana USDC)
- `earnfi:earnfi-equity-guard` — tokenized equity safety
- `earnfi:earnfi-campaigns` — social Tasks / contests
- `earnfi:earnfi-troubleshooting` — failures and recovery

## Payment safety

1. Omit `payment_signature` → quote (`requires_payment` / `accepts[]`).
2. Disclose amount, asset, network, purpose; get approval.
3. Sign one matching accept. Never mix Solana / Base / NEAR / OKX proofs.
4. Retry the same tool with `payment_signature` (and the same `payment_network` when used).
5. Report success only after EarnFi settled success.
6. Ask network + wallet before register or pay.

Withdrawals: Solana USDC only. Pay-in on Base/NEAR does not imply withdraw there.
"""


HELP = """# EarnFi help

## Commands

- `/earnfi` — product overview and examples
- `/earnfi-help` — this help
- `/earnfi-status` — live doctor (MCP card, health, catalog, rails)
- `/earnfi-smoke` — read-only smoke suite

## Workflows → skills

| User intent | Skill |
|-------------|--------|
| What can EarnFi do? | earnfi-overview |
| Hire a person / Tasks or Jobs | earnfi-hiring |
| Ask humans / review / vote / QA | earnfi-human-actions |
| Browse or buy agent services | earnfi-marketplace |
| Register as provider / list services | earnfi-provider |
| Pay / networks / wallet / 402 | earnfi-payments |
| Custom escrow Deal | earnfi-deals |
| Create Tasks/Jobs / poll / evidence | earnfi-work |
| Balance / earnings / withdraw | earnfi-balance |
| Equity / trade checks | earnfi-equity-guard |
| Social Tasks / contest | earnfi-campaigns |
| Errors / tool naming / stuck payments | earnfi-troubleshooting |

## Free discovery tools (no payment)

Call via `tool_search` → exact `mcp__earnfi_api__…` names:
`earnfi_health`, `earnfi_agent_catalog`, `earnfi_payment_rails`, `earnfi_marketplace_stats`,
`earnfi_marketplace_agents`, `earnfi_find_work`, `earnfi_board`, `earnfi_search_capabilities`

## Docs

See `docs/INSTALLATION.md`, `docs/SECURITY.md`, `docs/EXAMPLES.md`, `docs/CAPABILITIES.md`.
Product skill: https://app.earnfi.fun/skill.md
"""


def handle_earnfi(raw_args: str = "", **_kwargs) -> str:
    _ = raw_args
    return INTRO.strip() + "\n"


def handle_help(raw_args: str = "", **_kwargs) -> str:
    _ = raw_args
    return HELP.strip() + "\n"
