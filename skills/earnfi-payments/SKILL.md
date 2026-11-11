---
name: earnfi-payments
description: >-
  EarnFi x402 payments on Solana, Base, NEAR, or OKX. Four equal networks.
  Wallet via earnfi-wallet scripts. Quote → approve → settle. Prefer
  @earn-fi/agent-client for Solana/Base/NEAR settle when a local key exists.
license: MIT
metadata:
  author: earnfi
  version: "1.4.7"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Payments and networks

Call MCP tools as `mcp__earnfi_api__…` via `tool_search` → `tool_call`.

Product doc: https://app.earnfi.fun/skill.md  
No wallet yet → **earnfi-wallet** scripts first (do not refuse).

## Four networks (equal)

| Network | Asset | CAIP-2 | Register | Pay |
|---------|-------|--------|----------|-----|
| Solana | USDC | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | `scripts/solana-setup.mjs` / `earnfi_register_*` | Default create tools + `payment_network=solana` **or** `@earn-fi/agent-client` |
| Base | USDC | `eip155:8453` | `scripts/base-setup.mjs` / `earnfi_base_register_*` | Default creates + `payment_network=eip155:8453` (EIP-3009 `signTypedData`) |
| NEAR | USDC | `near:mainnet` | `scripts/near-generate.mjs` + NEP-413 or pay-first | Default creates + `payment_network=near:mainnet` (NEP-366); SDK preferred |
| OKX | USDT0 | `eip155:196` | `scripts/okx-setup.mjs` / `earnfi_okx_register_*` | **`earnfi_okx_*` only** |

When asked “how many networks?” → **four**. Offer to create a wallet via **earnfi-wallet**.

Never mix proofs. `earnfi_payment_rails` may show two URL bases; that does not change the four-network answer.

## Seamless settle paths

### A — MCP (all networks)

```
Paid create WITHOUT payment_signature
  → 402 + accepts[] (+ hint / next_step)
  → Disclose amount, asset, network; get Hermes approval
  → Sign ONE matching accept off-device (MCP has no keys)
  → Same tool + same args + payment_signature
  → EarnFi 200 → store secret / agent_token
```

### B — SDK (Solana / Base / NEAR)

When a local key already exists (from **earnfi-wallet** scripts):

```bash
npm install @earn-fi/agent-client
# Solana example — set SOLANA_SECRET_KEY_B58 + SOLANA_RPC_URL
npx earnfi-agent preflight --secret-key-bs58 "$SOLANA_SECRET_KEY_B58"
# Then use client.createSocialJob / hireAndFund / createHumanAction, etc.
```

SDK picks the accept for `paymentNetwork`, signs, and retries. Still disclose amount before settling. OKX stays on MCP `earnfi_okx_*` / OKX API base.

## Rules

1. Quote first; identical args on pay.
2. One accept, matching network.
3. Success only from EarnFi settled 200.
4. `idempotency_key` when allowed.
5. Hermes `trust: untrusted` → approve write/payment tools.
6. Register signature ≠ payment.
7. Automated withdrawals: Solana USDC only unless docs say otherwise.
8. Fund USDC (or OKX USDT0) **before** settle; Solana USDC ATA must exist.
