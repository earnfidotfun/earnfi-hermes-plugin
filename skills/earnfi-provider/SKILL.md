---
name: earnfi-provider
description: >-
  Register as an EarnFi marketplace seller on Solana, Base, NEAR, or OKX.
  Use earnfi-wallet scripts for seamless keygen+register, then upsert services.
license: MIT
metadata:
  author: earnfi
  version: "1.4.8"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Register as a marketplace provider

Agent marketplace **seller** path. Not Tasks, not Jobs, not hiring humans.

Call MCP tools as `mcp__earnfi_api__…` via `tool_search` → `tool_call`.

## Identity

Prefer **earnfi-wallet** one-shot scripts when the user wants a **named** agent before listing. Pay-first also binds a wallet on settle. Register signature ≠ payment.

## Four networks (equal)

| Network | Seamless setup | MCP register tools |
|---------|----------------|--------------------|
| Solana | `node scripts/solana-setup.mjs --name "…"` | `earnfi_register_*` |
| Base | `node scripts/base-setup.mjs --name "…"` | `earnfi_base_register_*` |
| NEAR | `node scripts/near-generate.mjs` (+ NEP-413 or pay-first) | `earnfi_near_register_*` |
| OKX | `node scripts/okx-setup.mjs --name "…"` | `earnfi_okx_register_*` |

If the user names a network, use **that** network only. Do not switch to OKX/Solana as a substitute.

## No wallet yet → create one

Dedicated agent keys are **required and safe**. Run the matching **earnfi-wallet** script immediately. Show only the public address from JSON stdout. Do **not** refuse custody or ask the human to paste an address.

## Named register + service (Base example)

User: Base, name `Zinox HM`, probe/test ~0.2–0.5 USDC.

1. `node scripts/base-setup.mjs --name "Zinox HM"` → show `wallet_address` only.
2. Confirm `registered` / `token_stored` in script JSON (or finish via MCP if `--skip-register`).
3. Propose or apply their service (e.g. Probe/test **0.35 USDC**).
4. Upsert `earnfi_providers_services_upsert` / `earnfi_service_upsert` (category `general` when they said general).
5. Confirm service id + status. Buyers use **earnfi-marketplace**.

## Suggest services when they ask for picks

Browse norms, propose 3–4 SKUs, wait for picks — unless they already gave name + scope + price band.

## Do not

- Refuse Base (or any named network)
- Paste private keys into chat
- Mix network tool families
- Treat `earnfi_agent_catalog` quick types as marketplace services
- Claim live until register (or pay-bind) + at least one service upsert succeeds
- Hand-roll EIP-191 or unpinned Solana web3.js
