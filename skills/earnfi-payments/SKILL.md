---
name: earnfi-payments
description: >-
  EarnFi x402 payments on Hermes. Multichain accepts on /v1 (Solana, Base,
  NEAR when quoted), optional payment_network filter, OKX USDT0 isolated rail,
  pay-first with agent_token optional. Never report success from a signature alone.
license: MIT
metadata:
  author: earnfi
  version: "1.2.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Payments and x402

Call MCP tools as `mcp__earnfi_api__…` via `tool_search` → `tool_call`. Never use bare `earnfi_*` names.

Canonical product doc: https://app.earnfi.fun/skill.md (Agent API skill). Prefer MCP over inventing REST paths.

## Pay flow

```
Paid create without payment_signature
  → 402 / requires_payment + accepts[] (+ hint / next_step when present)
  → Disclose amount, asset, network; get user approval
  → Sign ONE accept that matches the user's wallet
  → Same tool, same args, plus payment_signature
  → EarnFi 200 with job/order/deal id, secret, and agent_token when newly bound
```

`agent_token` is optional on paid creates. Pay first; the paying wallet can bind on settle. Registration is optional and only for a named identity beforehand.

Register signatures are never payment proofs. Do not put a register signature in `payment_signature`.

## Two surfaces (do not conflate)

**1. Multichain Agent API (`/api/ai-agent/v1`) — default MCP paid tools**

One API base. A quote’s `accepts[]` may include:

| Network | CAIP-2 | Wallet / proof |
|---------|--------|----------------|
| Solana USDC | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | Solana base58, `signed_tx` |
| Base USDC | `eip155:8453` | EVM `0x`, Base x402 / EIP-3009 style as the quote documents |
| NEAR USDC | `near:mainnet` | NEAR account, `signedDelegateAction` when quoted |

Trust **this quote’s** `accepts[]`. Do not assume `accepts[0]`. Do not assume every network is always present. If a filter returns empty or `payment_network_unavailable`, omit the filter or pick another network that appears.

Optional MCP arg `payment_network` (live on MCP 2.1.0+ paid creates) sends `X-Earnfi-Accepts-Filter`. Keep the same value on quote and pay. Aliases often work: `solana`, `base`, `near`, or full CAIP-2. If a stale session lacks the field, still pick the matching accept from `accepts[]` and sign that one.

**2. OKX / X Layer (`/api/ai-agent/okx/v1`) — `earnfi_okx_*` only**

USDT0 on `eip155:196`. EVM `paymentPayload`. Never send a Solana `signed_tx` to OKX tools, or an OKX payload to multichain `/v1` tools.

## Discovery each session

1. `earnfi_payment_rails` — URL-scoped rails (today often `solana-usdc-x402` + `okx-xlayer-usdt0`). Useful, but **not** the full list of pay networks. Base and NEAR usually show up in quote `accepts[]`, not as separate `/rails` ids.
2. `earnfi_agent_catalog` / `earnfi_agent_x402` / `earnfi_health` as needed.
3. For payment rules in one shot, `tool_search` for `earnfi_integrator_rules` or `earnfi_x402_capabilities` when those tools exist on this MCP session.

## Wallet ask (before signing)

Ask which network the user will pay on, and whether they already have that wallet. MCP never holds keys. Do not invent wallets or signatures.

Proof shapes must match the chosen accept. Solana ≠ Base ≠ NEAR ≠ OKX.

## Rules

1. Quote first. Same args on the pay retry.
2. One accept, one signature, matching network.
3. Success only from EarnFi settled success, not from a local tx hash.
4. Use `idempotency_key` when the tool allows it.
5. Hermes `trust: untrusted` means write/payment tools need host approval.
6. Automated withdrawals are Solana USDC only unless EarnFi docs say otherwise. Pay-in on Base or NEAR does not imply withdraw on those networks.
7. On wrong-network or wrong-rail errors, re-quote and switch tools with the user. Do not declare EarnFi broken.

## Failure recovery

- Quote expired → new quote, same params, no signature.
- Wrong network signature → re-quote; sign the matching accept.
- `payment_network_unavailable` → omit filter or switch network; stay on MCP.
- Settlement unclear → re-fetch job/order/deal and receipt tools.
