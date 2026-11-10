---
name: earnfi-payments
description: >-
  EarnFi x402 payments on Solana, Base, NEAR, or OKX. Four equal networks.
  Wallet setup via earnfi-wallet. Quote → approve → settle. Never report success
  from a signature alone.
license: MIT
metadata:
  author: earnfi
  version: "1.4.4"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Payments and networks

Call MCP tools as `mcp__earnfi_api__…` via `tool_search` → `tool_call`.

Product doc: https://app.earnfi.fun/skill.md  
Interfaces: Agent API + MCP. Pick **one** of four equal networks from the wallet you have (or create via **earnfi-wallet**).

## Four networks (Solana, Base, NEAR, OKX)

Same product answer every time. No “rails vs networks.” No demoting OKX or Base.

| Network | Asset | CAIP-2 | Wallet | Register sign | Pay proof |
|---------|-------|--------|--------|---------------|-----------|
| Solana | USDC | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | Solana base58 | Ed25519 → `earnfi_register_*` | Solana `signed_tx` via default create tools; optional `payment_network=solana` |
| Base | USDC | `eip155:8453` | EVM `0x` | `Wallet.signMessage` → `earnfi_base_register_*` | EIP-3009 `signTypedData` via default create tools; `payment_network=base` / `eip155:8453` |
| NEAR | USDC | `near:mainnet` | NEAR account | NEP-413 → `earnfi_near_register_*` | NEP-366 `signedDelegateAction`; `payment_network=near` / `near:mainnet` |
| OKX | USDT0 | `eip155:196` | EVM `0x` | `Wallet.signMessage` → `earnfi_okx_register_*` | EVM `paymentPayload` via **`earnfi_okx_*` only** |

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

No wallet yet → **earnfi-wallet** now (generate dedicated agent key; do not refuse). Store secret privately; show address only. Fund before paid creates. Register is free.

## Rules

1. Quote first; same args on pay.
2. One accept, one signature, matching network.
3. Success only from EarnFi settled success.
4. `idempotency_key` when allowed.
5. Hermes `trust: untrusted` → approval for write/payment tools.
6. Automated withdrawals: Solana USDC only unless docs say otherwise.
7. Marketplace sellers may use any of the four networks.
