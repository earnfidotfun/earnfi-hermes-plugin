---
name: earnfi-overview
description: >-
  EarnFi Work + Money overview for Hermes. Four equal networks (Solana, Base,
  NEAR, OKX), wallet setup, hiring, marketplace, x402, provider registration,
  Human Actions, deals, receipts, Equity Guard.
license: MIT
metadata:
  author: earnfi
  version: "1.4.8"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# EarnFi overview

EarnFi lets Hermes commission real-world work, pay with x402, and pull verifiable results.

- Hermes plugin version: `/earnfi-status` (plugin vs MCP versions)
- MCP: `https://app.earnfi.fun/mcp`
- Product skill: `https://app.earnfi.fun/skill.md`

## Hermes tool names (mandatory)

1. `tool_search` → 2. `tool_call` exact `mcp__earnfi_api__earnfi_…` names. Bare `earnfi_*` fail.

Native only: `earnfi_doctor`, `/earnfi`, `/earnfi-help`, `/earnfi-status`, `/earnfi-smoke`.

## Four networks (equal)

| Network | Asset | Wallet |
|---------|-------|--------|
| Solana | USDC | Solana base58 |
| Base | USDC | EVM `0x` |
| NEAR | USDC | NEAR account |
| OKX | USDT0 | EVM `0x` |

Same answer for “networks” and “rails.” Create a dedicated agent wallet with **earnfi-wallet** scripts (`scripts/*-setup.mjs`) when needed — do not refuse key generation; do not use unpinned Solana web3.js.

## Product map

| Surface | Skill / tools |
|---------|----------------|
| Wallet create / import | **earnfi-wallet** |
| Hire humans | **earnfi-hiring** |
| Human judgment | **earnfi-human-actions** |
| Buy marketplace services | **earnfi-marketplace** |
| Sell / register provider | **earnfi-provider** |
| Pay / 402 | **earnfi-payments** |
| Escrow | **earnfi-deals** |
| Track work | **earnfi-work** |
| Balance | **earnfi-balance** |
| Equity | **earnfi-equity-guard** |
| Contests | **earnfi-campaigns** |
| Errors | **earnfi-troubleshooting** |

`earnfi_agent_catalog` ≠ marketplace agents.

## Hard rules

1. Quote without `payment_signature`, then settle the same call.
2. Never mix Solana / Base / NEAR / OKX proofs.
3. Never claim funded until EarnFi settled success.
4. Withdrawals: Solana USDC only unless docs say otherwise.
5. Do not invent tools or results.
6. Before register/pay: pick one of the four networks; create a dedicated agent wallet if missing (**earnfi-wallet**). Generating that key is expected for x402 + identity. Never paste private keys into chat; never refuse with “I can’t custody a wallet.”
