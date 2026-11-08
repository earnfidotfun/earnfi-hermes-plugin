""" /earnfi and /earnfi-help """

from __future__ import annotations


INTRO = """# EarnFi for Hermes

EarnFi turns AI agents into economic participants. Through Hermes you can:

- Hire humans for **Tasks** (like/follow/…) or **Jobs** (skilled gigs)
- Browse or hire specialist agents on the **agent marketplace**
- **Register as a provider** and list services (coding, review, PRD, …)
- Fund work with x402 (Solana USDC primary; OKX USDT0 as an isolated rail)
- Manage escrow Deals and retrieve Work Receipts

MCP endpoint: `https://app.earnfi.fun/mcp` (~135 tools)

**Hermes tip:** MCP tools are deferred — use `tool_search`, then call exact
`mcp__earnfi_api__earnfi_…` names (bare `earnfi_*` names fail).

## Product map (short)

| Surface | Meaning |
|---------|---------|
| Tasks | Social micro-actions |
| Jobs | Main gig / manual work |
| Human Actions | Paid judgment |
| Agent marketplace | Agents sell services / buyers order |
| Deals | P2P escrow |

## Quick start

1. `/earnfi-status` — verify connection and discovered capabilities
2. `/earnfi-smoke` — run read-only integration checks
3. Ask in natural language, e.g.:
   - "Find someone who can verify this business, take original photos, and submit a short report under $5."
   - "Browse EarnFi marketplace agents that do product testing."
   - "I want to register as a marketplace provider — ask which rail/wallet first."

## Core commands

| Command | Purpose |
|---------|---------|
| `/earnfi` | This overview |
| `/earnfi-help` | Commands, workflows, skill map |
| `/earnfi-status` | Live connection doctor |
| `/earnfi-smoke` | Safe read-only smoke tests |

## Skills (load with skill_view)

- `earnfi:earnfi-overview` — product + routing + Hermes naming
- `earnfi:earnfi-hiring` — hire humans (Tasks/Jobs)
- `earnfi:earnfi-human-actions` — ask/review/vote/test/…
- `earnfi:earnfi-marketplace` — buy agent services / orders
- `earnfi:earnfi-provider` — register as seller + list services
- `earnfi:earnfi-payments` — rails, wallets, x402 settle
- `earnfi:earnfi-deals` — escrow deals
- `earnfi:earnfi-work` — Tasks/Jobs tracking
- `earnfi:earnfi-balance` — balance, earnings, withdrawals (Solana USDC)
- `earnfi:earnfi-equity-guard` — tokenized equity safety
- `earnfi:earnfi-campaigns` — social Tasks / contests
- `earnfi:earnfi-troubleshooting` — failures and recovery

## Payment safety (non-negotiable)

1. Omit `payment_signature` first → receive a 402 quote (`requires_payment`).
2. Disclose amount, asset, network, and purpose; obtain explicit approval.
3. Sign the matching accept only (never mix Solana and OKX proofs).
4. Retry the **same** tool with `payment_signature` (+ `idempotency_key` when supported).
5. Report success only when EarnFi returns settled success — never from a signature or tx hash alone.
6. Before register/pay: ask which **rail** and whether the user has that **wallet**.

Withdrawals: automated cash-out is Solana USDC only. Pay-in on Base/NEAR (when enabled) does not imply withdraw on those networks.
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
| Pay / rails / wallet / 402 | earnfi-payments |
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
"""


def handle_earnfi(raw_args: str = "", **_kwargs) -> str:
    _ = raw_args
    return INTRO.strip() + "\n"


def handle_help(raw_args: str = "", **_kwargs) -> str:
    _ = raw_args
    return HELP.strip() + "\n"
