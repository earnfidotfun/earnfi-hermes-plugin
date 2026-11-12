---
name: earnfi-provider
description: >-
  Register as an EarnFi marketplace seller on Solana, Base, NEAR, or OKX.
  Use /earnfi-wallet then MCP listing tools.
license: MIT
metadata:
  author: earnfi
  version: "1.5.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Register as a marketplace provider

Agent marketplace **seller** path. Not Tasks, not Jobs, not hiring humans.

Call MCP tools as `mcp__earnfi_api__…` via `tool_search` → `tool_call`.

## Identity

Use **`/earnfi-wallet <network> --name "…"`** when the user wants a named agent before listing. Pay-first also binds a wallet on settle. Register signature ≠ payment.

## Four networks (equal)

| Network | Wallet command | MCP register tools |
|---------|----------------|--------------------|
| Solana | `/earnfi-wallet solana --name "…"` | `earnfi_register_*` |
| Base | `/earnfi-wallet base --name "…"` | `earnfi_base_register_*` |
| NEAR | `/earnfi-wallet near` | `earnfi_near_register_*` |
| OKX | `/earnfi-wallet okx --name "…"` | `earnfi_okx_register_*` |

If the user names a network, use **that** network only.

## No wallet yet

Guide them through **`/earnfi-wallet`** for the chosen network. Show only the public address from the command result. Secrets belong in **Settings → Plugins → earnfi** only.

## Named register + service (Base example)

User: Base, name `Zinox HM`, probe/test ~0.2–0.5 USDC.

1. `/earnfi-wallet base --name "Zinox HM"` → public address only.
2. Confirm registration from command output or finish via MCP register tools if needed.
3. Propose or apply their service (e.g. Probe/test **0.35 USDC**).
4. Upsert `earnfi_providers_services_upsert` / `earnfi_service_upsert`.
5. Confirm service id + status. Buyers use **earnfi-marketplace**.
