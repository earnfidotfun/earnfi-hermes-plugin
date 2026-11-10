---
name: earnfi-payments
description: >-
  EarnFi x402 payments on Hermes. Distinguish URL rails (/rails) from pay
  networks (Solana/Base/NEAR accepts + OKX). Optional payment_network. Pay-first.
  Never report success from a signature alone. Use for rails, networks, wallets, 402.
license: MIT
metadata:
  author: earnfi
  version: "1.2.2"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Payments and x402

Call MCP tools as `mcp__earnfi_api__…` via `tool_search` → `tool_call`. Never use bare `earnfi_*` names.

Canonical product doc: https://app.earnfi.fun/skill.md

## Critical: rails ≠ networks

`earnfi_payment_rails` returns **URL-scoped rails** (today usually two):

| Rail id | API base | Role |
|---------|----------|------|
| `solana-usdc-x402` (default) | `/api/ai-agent/v1` | Canonical multichain Agent API |
| `okx-xlayer-usdt0` | `/api/ai-agent/okx/v1` | Isolated OKX / X Layer USDT0 |

That list is **not** the full set of networks a user can pay or register on.

On the **default** `/v1` rail, a paid-create quote’s `accepts[]` may include:

| Network | CAIP-2 | Typical wallet / proof |
|---------|--------|------------------------|
| Solana USDC | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | Solana base58, `signed_tx` |
| Base USDC | `eip155:8453` | EVM `0x`, Base x402 |
| NEAR USDC | `near:mainnet` | NEAR account, `signedDelegateAction` when quoted |

OKX adds **X Layer USDT0** (`eip155:196`) only through `earnfi_okx_*` tools.

Register (optional named identity) maps to MCP tools, not to `/rails` row count:

| Network | Tools |
|---------|--------|
| Solana | `earnfi_register_challenge` → `earnfi_register` |
| Base | `earnfi_base_register_challenge` → `earnfi_base_register` |
| NEAR | `earnfi_near_register_challenge` → `earnfi_near_register` |
| OKX | `earnfi_okx_register_challenge` → `earnfi_okx_register` |

### When the user asks “how many rails / networks?”

Answer in **two layers**. Never stop at `/rails` alone.

1. **URL rails** from `earnfi_payment_rails` (count + ids).
2. **Pay / register networks** on the default rail: call `earnfi_x402_capabilities` and/or quote once without `payment_signature` (or cite live `accepts[]` from a recent quote). List every `network` that appears. Mention OKX as a separate rail.
3. Say plainly: Base and NEAR are networks on the multichain `/v1` rail. They often do **not** appear as separate `/rails` ids. Doctor noting Base/NEAR register tools means those MCP tools exist, not that the networks are “not live.”

### Do not misread OKX marketplace hints

An OKX rail field like `marketplace.okx_ai_a2mcp` means OKX.AI **A2MCP catalog listing** for that rail. It does **not** mean EarnFi’s agent marketplace (`earnfi_marketplace_*`, provider services) is OKX-only.

EarnFi marketplace browse/hire/provider tools are on the default MCP/Agent API path. Provider registration can be Solana, Base, NEAR, or OKX. Do **not** tell the user they must use OKX to list services.

## Pay flow

```
Paid create without payment_signature
  → 402 / requires_payment + accepts[] (+ hint / next_step)
  → Disclose amount, asset, network; get approval
  → Sign ONE accept matching the user’s wallet
  → Same tool, same args, plus payment_signature
  → EarnFi 200: id, secret, agent_token when newly bound
```

`agent_token` is optional on paid creates. Register signatures are never payment proofs.

## Discovery each session

1. `earnfi_payment_rails` — URL rails only.
2. `earnfi_x402_capabilities` / `earnfi_integrator_rules` — networks + rules.
3. `earnfi_agent_catalog` / `earnfi_health` as needed.
4. For a concrete network list, trust a fresh quote’s `accepts[]`.

Optional `payment_network` on paid tools (MCP 2.1.0+) sends `X-Earnfi-Accepts-Filter`. Keep it the same on quote and pay. Aliases: `solana`, `base`, `near`, or full CAIP-2.

## Wallet ask

Ask which **network** they will pay or register on, and whether they have that wallet. MCP never holds keys. Proof shapes: Solana ≠ Base ≠ NEAR ≠ OKX.

## Rules

1. Quote first. Same args on the pay retry.
2. One accept, one signature, matching network.
3. Success only from EarnFi settled success.
4. `idempotency_key` when allowed.
5. Hermes `trust: untrusted` → host approval for write/payment tools.
6. Withdrawals: Solana USDC only unless docs say otherwise.
7. Wrong network → re-quote; do not declare EarnFi broken.

## Failure recovery

- Quote expired → new quote, no signature.
- Wrong network signature → re-quote; sign the matching accept.
- `payment_network_unavailable` → omit filter or switch network; stay on MCP.
- Settlement unclear → re-fetch job/order/deal + receipt tools.
