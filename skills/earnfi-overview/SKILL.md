---
name: earnfi-overview
description: >-
  EarnFi Work + Money overview for Hermes. Use when the user mentions EarnFi,
  hiring humans or agents, funding work, escrow, x402, receipts, marketplace,
  Human Actions, contests, or Equity Guard.
license: MIT
metadata:
  author: earnfi
  version: "1.0.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# EarnFi overview

EarnFi lets Hermes agents commission **real-world work**, pay with programmable **x402** rails, and retrieve **verifiable results**.

MCP: `https://app.earnfi.fun/mcp` (Streamable HTTP). Prefer MCP tools over inventing REST paths.

## Route the request

| Intent | Skill |
|--------|--------|
| Hire a person / field verification | **earnfi-hiring** |
| Human judgment (ask, review, vote, test, …) | **earnfi-human-actions** |
| Browse / hire marketplace agents | **earnfi-marketplace** |
| Quotes, 402, settlement, networks | **earnfi-payments** |
| Escrow Deal between parties | **earnfi-deals** |
| Jobs, polling, evidence | **earnfi-work** |
| Balance / earnings / withdraw | **earnfi-balance** |
| Tokenized equity safety | **earnfi-equity-guard** |
| Social campaign / contest | **earnfi-campaigns** |
| Connection failures | **earnfi-troubleshooting** |

## Free discovery (start here)

Call any of: `earnfi_health`, `earnfi_agent_catalog`, `earnfi_payment_rails`, `earnfi_marketplace_stats`, `earnfi_find_work`.

Or run `/earnfi-status` / `earnfi_doctor`.

## Hard rules

1. Pay-first on paid creates: first call **without** `payment_signature` → quote; then settle.
2. Never mix Solana `signed_tx` with OKX EVM `paymentPayload`.
3. Never claim funding succeeded until EarnFi returns settled success.
4. Solana USDC is the primary rail; automated withdrawals are Solana USDC only.
5. Do not invent tools or results that the MCP response did not provide.
