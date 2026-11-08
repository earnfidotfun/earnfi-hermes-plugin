---
name: earnfi-payments
description: >-
  EarnFi x402 payments — quotes, PAYMENT-SIGNATURE, rail/wallet selection,
  settlement verification, idempotency. Never report success from a signature alone.
license: MIT
metadata:
  author: earnfi
  version: "1.1.0"
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

Live registry: `earnfi_payment_rails`.

| Rail | Network / asset | Wallet | Tool family |
|------|-----------------|--------|-------------|
| `solana-usdc-x402` (default) | Solana USDC | Solana base58 | `earnfi_*` (non-okx) |
| `okx-xlayer-usdt0` | X Layer USDT0 | EVM `0x` | `earnfi_okx_*` only |

If the user has **no wallet**, ask which rail they want to use, then what wallet to create/connect. MCP **never holds keys**. Do not invent a wallet or signature.

## Rules

1. **Discovery:** `earnfi_payment_rails`, `earnfi_agent_x402`, `earnfi_agent_catalog`. Trust the **quote’s** `accepts[]`.
2. **Pick exactly one** `accepts[]` entry matching the signer the user actually has.
3. **Solana:** USDC x402 `signed_tx` as the quote documents.
4. **OKX / X Layer:** `earnfi_okx_*` only; EVM `paymentPayload` — never a Solana `signed_tx`.
5. **Other networks in a quote** (e.g. Base, NEAR): only if present in that quote’s `accepts[]`.
6. **Success:** EarnFi settled success only — not a local tx hash alone.
7. **Idempotency:** `idempotency_key` when allowed; no double-charge retries.
8. **Hermes trust:** write/payment tools need approval (`trust: untrusted`).
9. **Withdrawals:** automated cash-out is Solana USDC only.
10. Wrong-rail 404s (e.g. calling Solana register paths as OKX REST) are agent errors — switch tools/rail with the user, don’t declare the product broken.

## Failure recovery

- Quote expired → fresh quote (same args, no signature).
- Wrong network signature → re-quote; re-sign correctly.
- Uncertain settlement → re-fetch job/order/deal/receipt tools.
