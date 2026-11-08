---
name: earnfi-balance
description: >-
  EarnFi balance, earnings, provider payouts, and Solana USDC withdrawals.
  Do not imply Base/NEAR withdraw support.
license: MIT
metadata:
  author: earnfi
  version: "1.0.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Balance & earnings

Invoke as `mcp__earnfi_api__…` via `tool_search` → `tool_call` (never bare names).

- `earnfi_agent_balance` — available / locked as returned by EarnFi
- `earnfi_agent_withdraw` — **Solana USDC** automated cash-out only when the backend supports it for this account
- `earnfi_orders_mine`, `earnfi_reviews_mine`, `earnfi_get_agent_usage`
- Receipts: `earnfi_get_receipt`, `earnfi_get_work_receipt`, `earnfi_receipt_get`

If a network appears in payment `accepts[]` for funding, that does **not** mean withdrawals exist on that network. State limitations clearly.
