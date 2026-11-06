---
name: earnfi-payments
description: >-
  EarnFi x402 payments — quotes, PAYMENT-SIGNATURE, network selection,
  settlement verification, idempotency. Never report success from a signature alone.
license: MIT
metadata:
  author: earnfi
  version: "1.0.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Payments & x402

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

## Rules

1. **Discovery:** `earnfi_payment_rails`, `earnfi_agent_x402`, `earnfi_agent_catalog`. Trust the **quote’s** `accepts[]` and live rails registry — do not invent networks.
2. **Pick exactly one** `accepts[]` entry whose network matches the signer you actually have.
3. **Solana (default rail):** USDC x402 with `signed_tx` as documented by the quote.
4. **OKX / X Layer:** use `earnfi_okx_*` only; USDT0 EVM `paymentPayload` — never send a Solana signed_tx there.
5. **Other networks in a quote** (e.g. Base `eip155:8453`, NEAR): only if present in that quote’s `accepts[]`. Sign with the matching scheme (EVM x402 v2 / NEAR delegate). MCP **never holds keys** — Hermes cannot create a wallet for the user; the host or user must sign.
6. **Success criteria:** EarnFi settled success (`requires_payment` false/absent + resource id). A tx hash or local signature alone is **not** success.
7. **Idempotency:** pass `idempotency_key` when the schema allows; retries must not double-charge.
8. **Hermes trust:** write/payment MCP tools require approval (`trust: untrusted`). EarnFi server-side limits remain authoritative.
9. **Withdrawals:** automated cash-out is Solana USDC only. Never imply Base/NEAR/OKX withdraw from pay-in availability.
10. **No wallet?** Stop and ask the user to connect/fund a matching wallet (or use EarnFi app / `@earn-fi/agent-client`). Do not fabricate signatures.

## Failure recovery

- Quote expired → request a fresh quote (same args, no signature).
- Wrong network signature → do not retry with the same payload; re-quote and re-sign correctly.
- Uncertain settlement → re-fetch job/order/deal/receipt tools; never invent confirmation.
