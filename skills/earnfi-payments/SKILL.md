---
name: earnfi-payments
description: >-
  EarnFi x402 payments — quotes, PAYMENT-SIGNATURE, rail/wallet selection,
  settlement verification, idempotency. Never report success from a signature alone.
license: MIT
metadata:
  author: earnfi
  version: "1.1.1"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Payments & x402

Invoke MCP tools as `mcp__earnfi_api__…` via `tool_search` → `tool_call`.

## Canonical flow

```
Quote (no payment_signature)
  → Payment Required (402 / requires_payment + accepts[])
  → User approval (amount, asset, network, purpose)
  → Payment signature for ONE matching accept
  → Same MCP tool + payment_signature
  → EarnFi settlement confirmation
  → Funded resource (job_id / order_id / deal_id + secret)
```

## Rails & wallets (ask before assuming)

**Source of truth:** `earnfi_payment_rails` (live). Enumerate every `status: active`
rail and the `default_rail`. Present those to the user — when EarnFi enables more
rails, they appear here automatically; do not maintain a frozen two-rail menu.

Today’s live examples (verify each session; may grow):

| Rail id (example) | Network / asset | Wallet | Tool family |
|-------------------|-----------------|--------|-------------|
| `solana-usdc-x402` (often default) | Solana USDC | Solana base58 | `earnfi_*` (non-okx) |
| `okx-xlayer-usdt0` | X Layer USDT0 | EVM `0x` | `earnfi_okx_*` only |

**Two different surfaces:**

1. **Registration / identity rails** — active entries in `earnfi_payment_rails`
   that have matching `*_register_*` MCP tools (see **earnfi-provider**).
2. **Pay-in networks on a quote** — entries inside that quote’s `accepts[]`.
   These can include extra networks (e.g. Base, NEAR) **for that payment only**.
   Offer them for funding when present; do **not** treat them as “register on
   this network” unless they are also an active rail with register tools.

If the user has **no wallet**, ask which **active rail** (or which accept) they
want, then what wallet to create/connect. MCP **never holds keys**.

## Rules

1. **Discovery:** always call `earnfi_payment_rails` (plus catalog/x402 as needed). Trust the **quote’s** `accepts[]` for that create.
2. **Pick exactly one** `accepts[]` entry matching the signer the user actually has.
3. **Solana rail:** USDC x402 `signed_tx` as the quote documents.
4. **OKX / X Layer rail:** `earnfi_okx_*` only; EVM `paymentPayload` — never a Solana `signed_tx`.
5. **Other networks in a quote** (Base, NEAR, …): only if present in that quote’s `accepts[]`; still not a registration rail by themselves.
6. **New rails:** when `earnfi_payment_rails` shows a new `active` id, use its documented MCP tool family from `tool_search` — never invent endpoints.
7. **Success:** EarnFi settled success only — not a local tx hash alone.
8. **Idempotency:** `idempotency_key` when allowed; no double-charge retries.
9. **Hermes trust:** write/payment tools need approval (`trust: untrusted`).
10. **Withdrawals:** automated cash-out is Solana USDC only (unless rails/docs say otherwise).
11. Wrong-rail 404s are agent errors — re-check live rails + matching tools with the user.

## Failure recovery

- Quote expired → fresh quote (same args, no signature).
- Wrong network signature → re-quote; re-sign correctly.
- Uncertain settlement → re-fetch job/order/deal/receipt tools.
