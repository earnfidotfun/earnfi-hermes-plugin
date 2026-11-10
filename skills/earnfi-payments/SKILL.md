---
name: earnfi-payments
description: >-
  EarnFi x402 payments on Solana, Base, NEAR, or OKX. Four equal networks.
  Wallet setup via earnfi-wallet. Quote → approve → settle. Never report success
  from a signature alone.
license: MIT
metadata:
  author: earnfi
  version: "1.4.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Payments and networks

Call MCP tools as `mcp__earnfi_api__…` via `tool_search` → `tool_call`.

Product doc: https://app.earnfi.fun/skill.md  
Interfaces: Agent API + MCP. Pick **one** of four equal networks from the wallet you have (or create via **earnfi-wallet**).

## Four networks (Solana, Base, NEAR, OKX)

Same product answer every time. No “rails vs networks.” No demoting OKX or Base.

| Network | Asset | CAIP-2 | Wallet | Register | Pay |
|---------|-------|--------|--------|----------|-----|
| Solana | USDC | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | Solana base58 | `earnfi_register_*` | Default create tools; optional `payment_network=solana` |
| Base | USDC | `eip155:8453` | EVM `0x` | `earnfi_base_register_*` | Default create tools; `payment_network=base` / `eip155:8453` |
| NEAR | USDC | `near:mainnet` | NEAR account | `earnfi_near_register_*` | Default create tools; `payment_network=near` / `near:mainnet` |
| OKX | USDT0 | `eip155:196` | EVM `0x` | `earnfi_okx_register_*` | `earnfi_okx_*` create tools |

When asked “how many networks?” → **four**: Solana, Base, NEAR, OKX. Then ask which wallet they have, or offer to **create** one (**earnfi-wallet**).

Use the matching tool family for the chosen network. Do not mix proofs across networks.

`earnfi_payment_rails` is optional API discovery. It may show two URL bases; that does not change the four-network product answer.

Trust each quote’s `accepts[]`. If one network is missing from a quote, try another or omit `payment_network`.

## Pay flow

```
Paid create without payment_signature
  → 402 + accepts[]
  → Disclose amount, asset, network; get approval
  → Sign ONE matching accept
  → Same tool + payment_signature
  → EarnFi 200: id, secret, agent_token when newly bound
```

`agent_token` optional (pay-first). Register signature ≠ payment.

## Wallet

No wallet yet → **earnfi-wallet** (generate dedicated key, store secret privately, show address only). Fund before paid creates. Register is free.

## Rules

1. Quote first; same args on pay.
2. One accept, one signature, matching network.
3. Success only from EarnFi settled success.
4. `idempotency_key` when allowed.
5. Hermes `trust: untrusted` → approval for write/payment tools.
6. Automated withdrawals: Solana USDC only unless docs say otherwise.
7. Marketplace sellers may use any of the four networks.
