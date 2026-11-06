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

1. **Discovery:** `earnfi_payment_rails`, `earnfi_agent_x402`, `earnfi_x402_capabilities` (if listed), `earnfi_agent_catalog`.
2. **Pick exactly one** `accepts[]` entry whose network matches the signer.
3. **Solana:** USDC x402 with `signed_tx` material as documented by the quote.
4. **OKX / X Layer:** USDT0 EVM `paymentPayload` — never send a Solana signed_tx to `earnfi_okx_*`.
5. **Success criteria:** HTTP/tool success with settlement acknowledged and `requires_payment` false/absent. A tx hash or local signature is **not** success.
6. **Idempotency:** pass `idempotency_key` on paid creates when the schema allows; retries must not double-charge.
7. **Hermes trust:** write/payment MCP tools require approval (`trust: untrusted`). Still enforce EarnFi server-side limits.
8. **Networks:** do not advertise Base/NEAR withdrawals because pay-in may list those accepts. Automated withdraw = Solana USDC only.

## Failure recovery

- Quote expired → request a fresh quote (same args, no signature).
- Wrong network signature → do not retry with the same payload; re-quote and re-sign correctly.
- Uncertain settlement → re-fetch job/order/deal/receipt tools; never invent confirmation.
