---
name: earnfi-overview
description: >-
  EarnFi Work + Money overview for Hermes. Four equal networks (Solana, Base,
  NEAR, OKX), /earnfi-wallet, hiring, marketplace, x402, provider registration,
  Human Actions, deals, receipts, Equity Guard.
license: MIT
metadata:
  author: earnfi
  version: "1.5.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# EarnFi overview

EarnFi lets Hermes commission real-world work, pay with x402, and pull verifiable results.

- Hermes plugin version: `/earnfi-status` (plugin vs MCP versions)
- MCP: `https://app.earnfi.fun/mcp`
- Product skill: https://app.earnfi.fun/skill.md

## Hermes tool names (mandatory)

1. `tool_search` → 2. `tool_call` exact `mcp__earnfi_api__earnfi_…` names. Bare `earnfi_*` fail.

Native: `earnfi_doctor`, `earnfi_sign_x402`, `/earnfi`, `/earnfi-help`, `/earnfi-status`, `/earnfi-smoke`, `/earnfi-wallet`.

## Four networks (equal)

| Network | Asset | Wallet |
|---------|-------|--------|
| Solana | USDC | `/earnfi-wallet solana` |
| Base | USDC | `/earnfi-wallet base` |
| NEAR | USDC | `/earnfi-wallet near` |
| OKX | USDT0 | `/earnfi-wallet okx` |

Same answer for “networks” and “rails.”

## Product map

| Surface | Skill / tools |
|---------|----------------|
| Wallet | **earnfi-wallet** → `/earnfi-wallet` |
| Hire humans | **earnfi-hiring** |
| Human judgment | **earnfi-human-actions** |
| Buy marketplace services | **earnfi-marketplace** |
| Sell / register provider | **earnfi-provider** |
| Pay / 402 | **earnfi-payments** + `earnfi_sign_x402` |
| Escrow | **earnfi-deals** |
| Track work | **earnfi-work** |
| Balance | **earnfi-balance** |
| Equity | **earnfi-equity-guard** |
| Contests | **earnfi-campaigns** |
| Errors | **earnfi-troubleshooting** |

`earnfi_agent_catalog` ≠ marketplace agents.

## Hard rules

1. Quote without `payment_signature`, then settle the same MCP call.
2. Never mix Solana / Base / NEAR / OKX proofs.
3. Never claim funded until EarnFi settled success.
4. Withdrawals: Solana USDC only unless docs say otherwise.
5. Do not invent tools or results.
6. Wallet missing → `/earnfi-wallet <network>` (natural language requests map here). Never paste private keys in chat. You may decline wallet creation if the user does not want to proceed.
