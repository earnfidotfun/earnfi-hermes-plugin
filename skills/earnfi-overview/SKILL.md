---
name: earnfi-overview
description: >-
  EarnFi Work + Money overview for Hermes. Four peer networks (Solana, Base,
  NEAR, OKX), hiring, marketplace, x402, provider registration, Human Actions,
  deals, receipts, Equity Guard. Use when the user mentions EarnFi.
license: MIT
metadata:
  author: earnfi
  version: "1.3.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# EarnFi overview

EarnFi lets Hermes commission real-world work, pay with x402, and pull verifiable results.

- Hermes plugin: see `/earnfi-status` (plugin version + MCP version)
- MCP: `https://app.earnfi.fun/mcp`
- Product skill: `https://app.earnfi.fun/skill.md`
- Prefer MCP over inventing REST. Code SDK: `@earn-fi/agent-client`

## Hermes tool names (mandatory)

EarnFi MCP tools are deferred. Never call bare names like `earnfi_agent_catalog`.

1. `tool_search` (e.g. `earnfi payment`, `earnfi_register`, `earnfi marketplace`, `earnfi_base_register`)
2. `tool_call` with the exact name, usually `mcp__earnfi_api__earnfi_<tool>`
3. On “not a known tool name”, search again

Native only: `earnfi_doctor`, `/earnfi`, `/earnfi-help`, `/earnfi-status`, `/earnfi-smoke`.

When the user asks plugin version or supported networks, run `/earnfi-status` or `earnfi_doctor`, and also `tool_search` for `earnfi_x402_capabilities` / register tools. Do not stop at doctor alone if MCP tools are available.

## Four peer networks

| Network | Asset | Typical wallet |
|---------|-------|----------------|
| Solana | USDC | Solana base58 |
| Base | USDC | EVM `0x` |
| NEAR | USDC | NEAR account |
| OKX X Layer | USDT0 | EVM `0x` |

Equal options. Owner or agent picks from the wallet they have. See **earnfi-payments**.

## Product map

| Surface | What it is | Typical tools |
|---------|------------|---------------|
| Tasks | Social / micro actions | `earnfi_social_create` |
| Jobs | Skilled or manual gigs | `earnfi_manual_create` |
| Contests / campaigns | Prize pools | `earnfi_contest_create` |
| Human Actions | Paid judgment | `earnfi_ask_humans`, `earnfi_human_*` |
| Deals | P2P escrow | **earnfi-deals** |
| Agent marketplace | Buy or sell agent services | **earnfi-marketplace** / **earnfi-provider** |
| Open work | Open briefs | `earnfi_open_work_*` |
| Equity Guard | Trade safety | **earnfi-equity-guard** |

`earnfi_agent_catalog` ≠ marketplace agents. Use `earnfi_marketplace_agents` / `earnfi_marketplace_services`.

## Route the request

| Intent | Skill |
|--------|--------|
| Hire a human | **earnfi-hiring** |
| Human judgment | **earnfi-human-actions** |
| Buy marketplace services | **earnfi-marketplace** |
| Register / list as seller | **earnfi-provider** |
| Networks, wallets, 402 | **earnfi-payments** |
| Escrow Deal | **earnfi-deals** |
| Track jobs/tasks | **earnfi-work** |
| Balance / withdraw | **earnfi-balance** |
| Equity | **earnfi-equity-guard** |
| Contests | **earnfi-campaigns** |
| Errors | **earnfi-troubleshooting** |

## Hard rules

1. Quote without `payment_signature`, then settle the same call.
2. Never mix Solana, Base, NEAR, and OKX proofs.
3. Never claim funded until EarnFi settled success.
4. Withdrawals: Solana USDC only unless docs say otherwise.
5. Do not invent tools or results.
6. Before register or pay: ask which of the four networks and whether they have that wallet.
