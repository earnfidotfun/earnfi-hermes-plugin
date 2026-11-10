---
name: earnfi-payments
description: >-
  EarnFi x402 payments. Four peer networks: Solana, Base, NEAR, OKX. Ask which
  wallet/network to use. Quote → approve → settle. Never report success from a
  signature alone. Use for networks, wallets, rails questions, or 402 flows.
license: MIT
metadata:
  author: earnfi
  version: "1.3.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Payments and networks

Call MCP tools as `mcp__earnfi_api__…` via `tool_search` → `tool_call`. Never use bare `earnfi_*` names.

Product doc: https://app.earnfi.fun/skill.md  
Interfaces: Agent API + MCP. The owner or agent picks a network from the wallet they already have (or will connect).

## Four peer networks (equal options)

Present these as the supported set. Do **not** rank Solana/OKX above Base/NEAR. Do **not** invent a “rails vs networks” story for the user.

| Network | Asset | CAIP-2 / chain | Wallet | Register tools | Pay tools |
|---------|-------|----------------|--------|----------------|-----------|
| **Solana** | USDC | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | Solana base58 | `earnfi_register_challenge` → `earnfi_register` | Default create tools; optional `payment_network=solana` |
| **Base** | USDC | `eip155:8453` | EVM `0x` | `earnfi_base_register_challenge` → `earnfi_base_register` | Same create tools; `payment_network=base` or `eip155:8453` |
| **NEAR** | USDC | `near:mainnet` | NEAR account | `earnfi_near_register_challenge` → `earnfi_near_register` | Same create tools; `payment_network=near` or `near:mainnet` |
| **OKX X Layer** | USDT0 | `eip155:196` | EVM `0x` | `earnfi_okx_register_challenge` → `earnfi_okx_register` | **`earnfi_okx_*` create tools only** |

When the user asks “how many networks / rails?” answer: **four** — Solana, Base, NEAR, OKX. Then ask which wallet they have.

### Tool routing only (keep internal)

- Solana / Base / NEAR paid creates share the default MCP tools on `/api/ai-agent/v1`. Pick the network with `payment_network` and/or by signing the matching entry in `accepts[]`.
- OKX paid creates use `earnfi_okx_*` only. Never mix OKX proofs with Solana/Base/NEAR tools (or the reverse).
- `earnfi_payment_rails` is an API discovery document. It may list two URL bases. That does **not** change the product answer: four networks.
- Trust each quote’s `accepts[]`. If a network is missing from one quote (`payment_network_unavailable`), omit the filter or switch network. Do not drop Base/NEAR from the menu forever.

## Pay flow

```
Paid create without payment_signature
  → 402 / requires_payment + accepts[]
  → Disclose amount, asset, network; get approval
  → Sign ONE accept for the chosen network
  → Same tool, same args, plus payment_signature
  → EarnFi 200: id, secret, agent_token when newly bound
```

`agent_token` is optional (pay-first). Register is optional named identity. Register signature ≠ `payment_signature`.

## Discovery

1. Prefer `earnfi_x402_capabilities` / `earnfi_integrator_rules` / a fresh unpaid quote for what is live right now.
2. `earnfi_payment_rails` is optional background.
3. Before signing: ask which of the four networks and whether they have that wallet. MCP never holds keys.

## Rules

1. Quote first. Same args on pay.
2. One accept, one signature, matching network.
3. Success only from EarnFi settled success.
4. `idempotency_key` when allowed.
5. Hermes `trust: untrusted` → approval for write/payment tools.
6. Automated withdrawals are Solana USDC only unless docs say otherwise.
7. Marketplace sellers can use any of the four networks. `okx_ai_a2mcp` is not “marketplace = OKX only.”

## Failure recovery

- Quote expired → new quote.
- Wrong network signature → re-quote; sign the matching accept.
- `payment_network_unavailable` → omit filter or pick another of the four; stay on MCP.
- Settlement unclear → re-fetch job/order/deal + receipt tools.
