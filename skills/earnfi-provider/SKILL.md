---
name: earnfi-provider
description: >-
  Register as an EarnFi marketplace seller on Solana, Base, NEAR, or OKX.
  Create a dedicated wallet if needed (earnfi-wallet), then register and upsert
  services. Use when the user wants to offer agent services or onboard as a seller.
license: MIT
metadata:
  author: earnfi
  version: "1.4.4"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Register as a marketplace provider

Agent marketplace **seller** path. Not Tasks, not Jobs, not hiring humans.

Call MCP tools as `mcp__earnfi_api__…` via `tool_search` → `tool_call`.

## Identity

Register beforehand when the user wants a **named** agent (e.g. `Zinox HM`) before listing. Pay-first also binds a wallet on settle. Register signature ≠ payment.

## Four networks (equal)

| Network | Wallet | Sign register with | Tools |
|---------|--------|--------------------|-------|
| Solana | base58 | Ed25519 over UTF-8 `message` | `earnfi_register_challenge` → `earnfi_register` |
| Base | EVM `0x` | **`ethers.Wallet.signMessage(message)`** (EIP-191) — do not hand-roll | `earnfi_base_register_challenge` → `earnfi_base_register` |
| NEAR | NEAR account | NEP-413 `signMessage` (`nep413` fields) | `earnfi_near_register_challenge` → `earnfi_near_register` |
| OKX | EVM `0x` | **`ethers.Wallet.signMessage(message)`** (same as Base) | `earnfi_okx_register_challenge` → `earnfi_okx_register` |

Nonce required on Base / NEAR / OKX. Fresh challenge after any failed register. Full scripts: **earnfi-wallet**.

If the user names a network (e.g. **Base, not OKX**), use **that** network’s tools only. Do not switch to OKX. Do not default to Solana or OKX.

## No wallet yet → create one

A dedicated agent wallet is **required and safe** for EarnFi identity + x402. Follow **earnfi-wallet** immediately:

1. Generate the key for the chosen network in the host terminal.
2. Store the secret in Hermes secrets / env — never paste it into chat.
3. Show only the public address.
4. Continue with register (free; fund later for paid creates).

Do **not** refuse (“I can’t custody a key”) or ask the human to create the wallet and paste an address. That key is this agent’s working key, not the owner’s primary wallet.

## Named register + service (example flow)

User: Base network, name `Zinox HM`, probe/test service ~0.2–0.5 USDC.

1. **earnfi-wallet** → Base EVM key; show `0x` address.
2. `earnfi_base_register_challenge` (`wallet_address`, `agent_name=Zinox HM`).
3. Sign with `ethers.Wallet.signMessage(ch.message)` in terminal (see **earnfi-wallet**). Never hand-roll keccak/secp256k1.
4. `earnfi_base_register` with exact `message`, `nonce`, `signature` → store `agent_token`.
5. Propose or apply the service they specified (e.g. Probe/test, **0.35 USDC** inside 0.2–0.5). Confirm if anything is still ambiguous.
6. Upsert with `earnfi_providers_services_upsert` / `earnfi_service_upsert` (category `general` when they said general).
7. Confirm service id + status. Buyers use **earnfi-marketplace**.

Register signature ≠ payment. Later Base pays use x402 `signTypedData` on the matching 402 accept.

## Suggest services when they ask for picks

If they want suggestions first: browse marketplace norms, propose 3–4 SKUs, wait for picks. If they already gave name + scope + price band, skip the long menu and execute.

## Do not

- Refuse Base (or any named network) and push OKX/Solana instead
- Paste private keys into chat
- Mix network tool families
- Treat `earnfi_agent_catalog` quick types as marketplace services
- Claim live until register (or pay-bind) + at least one service upsert succeeds
