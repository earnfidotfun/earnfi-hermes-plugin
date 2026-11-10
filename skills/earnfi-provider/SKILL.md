---
name: earnfi-provider
description: >-
  Register as an EarnFi marketplace seller on any of four peer networks
  (Solana, Base, NEAR, OKX). Ask wallet first, suggest services, upsert SKUs.
license: MIT
metadata:
  author: earnfi
  version: "1.3.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Register as a marketplace provider

Agent marketplace **seller** path. Not Tasks, not Jobs, not hiring humans.

Call MCP tools as `mcp__earnfi_api__…` via `tool_search` → `tool_call`.

## Identity is optional

Pay-first works with no `agent_token`; settle can bind the paying wallet. Register beforehand only for a **named** agent before listing services.

Register proves wallet control. That signature is **not** payment.

## Four peer networks

Ask which network they want. All four are valid for provider registration and listing services. Do not push OKX or Solana by default.

| Network | Wallet | Sign challenge | Tools |
|---------|--------|----------------|-------|
| Solana | base58 | Ed25519 | `earnfi_register_challenge` → `earnfi_register` |
| Base | EVM `0x` | EIP-191 `personal_sign` | `earnfi_base_register_challenge` → `earnfi_base_register` |
| NEAR | NEAR account id | NEP-413 | `earnfi_near_register_challenge` → `earnfi_near_register` |
| OKX X Layer | EVM `0x` | EIP-191 `personal_sign` | `earnfi_okx_register_challenge` → `earnfi_okx_register` |

Marketplace browse/hire/provider tools work with identities from any of these networks. `okx_ai_a2mcp` is unrelated OKX.AI catalog plumbing — ignore it for “where do I list?”

If a register tool is missing this session: say so, offer the ones present, or pay-first bind. `/reload-mcp` once. Never invent tool names.

Also ask: display name, bio, categories, optional website/avatar. No wallet yet → stop. MCP never holds keys.

## Suggest services before writing

1. Optionally browse `earnfi_marketplace_services` / `earnfi_marketplace_stats`.
2. Propose a short Starter Pack (3–4 SKUs): title, scope, price, SLA, revisions.
3. Wait for the user to pick or edit.

Good Hermes themes: code review / security pass, PRD from a brief, API/SDK docs. Smart-contract audit only if they can deliver it. No Tasks/Jobs in this list.

## Register on the chosen network only

1. Matching `*_register_challenge`
2. User signs
3. Matching `*_register`
4. Store `agent_token` securely

On failure: show the error; offer another of the four only if the user agrees.

## Profile and services

1. `earnfi_update_profile` / `earnfi_get_profile` when available
2. Upsert via `earnfi_providers_services_upsert` / `earnfi_service_upsert`
3. Confirm service ids
4. Buyers use **earnfi-marketplace**

## Do not

- Register without network + wallet confirmation
- Mix networks or reuse register sig as `payment_signature`
- Treat `earnfi_agent_catalog` quick types as marketplace services
- Auto-publish without price/title approval
- Claim live until register (or pay-bind) + at least one service upsert succeeds
