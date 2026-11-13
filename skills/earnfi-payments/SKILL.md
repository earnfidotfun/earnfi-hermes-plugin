---
name: earnfi-payments
description: >-
  EarnFi x402 via MCP only: quote → disclose → approve → sign → settle. Use earnfi_sign_x402
  or user off-device signing; never SDK/CLI spend paths.
license: MIT
metadata:
  author: earnfi
  version: "1.5.2"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Payments and networks

Call MCP tools as `mcp__earnfi_api__…` via `tool_search` → `tool_call`.

Product doc: https://app.earnfi.fun/skill.md  
No wallet configured → **earnfi-wallet** (`/earnfi-wallet …`) first.

## Four networks (equal)

| Network | Asset | Register | Pay |
|---------|-------|----------|-----|
| Solana | USDC | `/earnfi-wallet solana` or `earnfi_register_*` | MCP create + x402 |
| Base | USDC | `/earnfi-wallet base` or Base register tools | MCP + EIP-3009 proof |
| NEAR | USDC | `/earnfi-wallet near` + register / pay-first | MCP + NEP-366 |
| OKX | USDT0 | `/earnfi-wallet okx` or OKX register tools | `earnfi_okx_*` only |

Never mix proofs across networks.

## Settlement flow (only path)

```
1. Paid MCP call WITHOUT payment_signature → 402 JSON (save full body as quote_json)
2. Disclose amount, asset, network, payTo; get Hermes approval for the write tool
3. earnfi_sign_x402(payment_network, quote_json) — triggers Hermes approval (pre_tool_call); returns payment_signature only, OR user signs off-device
4. Same MCP tool + same args + payment_signature
5. Success only after EarnFi settled HTTP 200 / confirmed settlement
```

**Forbidden:** `npm install @earn-fi/agent-client`, `hireAndFund`, `npx earnfi-agent`, or any terminal/SDK path that spends or passes secrets on the command line.

## Rules

1. Quote first; identical args on pay.
2. One accept, matching `payment_network`.
3. Never claim funded from a signature alone — verify settlement.
4. `idempotency_key` when allowed.
5. MCP `trust: untrusted` → approve write/payment tools.
6. Register signature ≠ payment.
7. Automated withdrawals: Solana USDC only unless docs say otherwise.
8. Fund USDC (or OKX USDT0) before settle; Solana USDC ATA must exist.
