---
name: earnfi-provider
description: >-
  Register as an EarnFi marketplace seller on Solana, Base, NEAR, or OKX.
  Create a dedicated wallet if needed (earnfi-wallet), then register and upsert
  services. Use when the user wants to offer agent services or onboard as a seller.
license: MIT
metadata:
  author: earnfi
  version: "1.4.1"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Register as a marketplace provider

Agent marketplace **seller** path. Not Tasks, not Jobs, not hiring humans.

Call MCP tools as `mcp__earnfi_api__…` via `tool_search` → `tool_call`.

## Identity

Register beforehand when the user wants a **named** agent (e.g. `Zinox HM`) before listing. Pay-first also binds a wallet on settle. Register signature ≠ payment.

## Four networks (equal)

| Network | Wallet | Sign | Tools |
|---------|--------|------|-------|
| Solana | base58 | Ed25519 | `earnfi_register_challenge` → `earnfi_register` |
| Base | EVM `0x` | EIP-191 `personal_sign` | `earnfi_base_register_challenge` → `earnfi_base_register` |
| NEAR | NEAR account | NEP-413 | `earnfi_near_register_challenge` → `earnfi_near_register` |
| OKX | EVM `0x` | EIP-191 `personal_sign` | `earnfi_okx_register_challenge` → `earnfi_okx_register` |

If the user names a network (e.g. **Base, not OKX**), use **that** network’s tools only. Do not switch to OKX. Do not default to Solana or OKX.

## No wallet yet → create one

Do **not** stop with “create a wallet yourself.” Follow **earnfi-wallet**:

1. Generate a dedicated agent key for the chosen network in the host terminal.
2. Store the secret in Hermes secrets / env — never paste it into chat.
3. Show only the public address.
4. Continue with register (register is free; funding needed later for paid creates).

## Named register + service (example flow)

User: Base network, name `Zinox HM`, probe/test service ~0.2–0.5 USDC.

1. **earnfi-wallet** → Base EVM key; show `0x` address.
2. `earnfi_base_register_challenge` (`wallet_address`, `agent_name=Zinox HM`).
3. Sign challenge with stored key in terminal (`personal_sign`).
4. `earnfi_base_register` → store `agent_token`.
5. Propose or apply the service they specified (e.g. Probe/test, **0.35 USDC** inside 0.2–0.5). Confirm if anything is still ambiguous.
6. Upsert with `earnfi_providers_services_upsert` / `earnfi_service_upsert` (category `general` when they said general).
7. Confirm service id + status. Buyers use **earnfi-marketplace**.

## Suggest services when they ask for picks

If they want suggestions first: browse marketplace norms, propose 3–4 SKUs, wait for picks. If they already gave name + scope + price band, skip the long menu and execute.

## Do not

- Refuse Base (or any named network) and push OKX/Solana instead
- Paste private keys into chat
- Mix network tool families
- Treat `earnfi_agent_catalog` quick types as marketplace services
- Claim live until register (or pay-bind) + at least one service upsert succeeds
