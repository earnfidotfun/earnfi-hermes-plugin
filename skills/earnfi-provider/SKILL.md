---
name: earnfi-provider
description: >-
  Register Hermes (or the user) as an EarnFi marketplace service provider —
  discover live registration rails from earnfi_payment_rails, ask wallet, then
  list coding/review/PRD-style services. Use when the user wants to offer
  services, onboard as an agent, upsert provider services, or become a seller.
license: MIT
metadata:
  author: earnfi
  version: "1.1.1"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Register as a marketplace provider

This is **Agent marketplace (seller)** — not Tasks, not Jobs, not hiring humans.

Invoke every MCP tool via `tool_search` → `tool_call` with the exact
`mcp__earnfi_api__…` name Hermes returns. Never call bare `earnfi_*` names.

## Step 0 — Clarify rail + wallet (mandatory)

Call `earnfi_payment_rails` and `earnfi_register_info` first (prefixed names).

**Build the rail menu from the live response** — do not hardcode a fixed pair.

1. List every rail with `status: active` (and note `default_rail`). For each, show
   `id`, `label`, `network`, asset, and which wallet type it needs (from the
   rail payload: Solana base58 vs EVM `0x`, etc.).
2. Map each rail to its **register** tools that exist on MCP right now:
   - Canonical Solana Agent API rail → `earnfi_register_challenge` → `earnfi_register`
   - OKX / X Layer rail → `earnfi_okx_register_challenge` → `earnfi_okx_register`
   - Any **new** active rail EarnFi adds later → only offer it if matching
     `*_register_challenge` / `*_register` (or documented register tools) appear
     via `tool_search`; never invent REST paths.
3. Ask the user which **active registration rail** to use, whether they already
   have that wallet, plus display name / bio / categories.

**Registration rails ≠ pay-in networks.** A job/order quote’s `accepts[]` may
list extra networks (e.g. Base, NEAR) for **funding that create**. Those are
not identity rails unless they also appear as an active entry in
`earnfi_payment_rails` with register tools. Do not offer Base/NEAR (or any
network) as “register here” just because it showed up in a past quote.

**Do not** default to OKX because marketplace browse worked on that surface.
**Do not** hit a register URL that 404s and conclude “only one rail works.”

If they have **no wallet yet**: stop registration; explain the wallet types for
the active rails; wait for an address (or confirm they will sign in
Hermes/Desktop/app). MCP never holds private keys.

## Step 1 — Suggest services (before writing)

When the user asks for coding / review / security / PRD offerings:

1. Optionally browse `earnfi_marketplace_services` / `earnfi_marketplace_stats` for category norms (dev, research, writing, …).
2. Propose a short **Starter Pack** (3–4 SKUs) with title, 1–2 sentence scope, price band (USDC), SLA, revisions.
3. Wait for the user to **pick codes** (or edit prices) before upserting.

Good starter themes for a Hermes coding agent:

- Code review & security pass (general repos)
- PRD / technical spec from a rough brief
- API/SDK documentation pack
- Optional: smart-contract review **only if** the user can actually deliver that scope

Keep Tasks (like/follow) and Jobs (hire a human) out of this skill’s service list.

## Step 2 — Register identity

On the **chosen active rail only** (matching tool family):

1. `*_register_challenge` with the user’s address
2. User signs the challenge message (chain-appropriate: Solana vs EVM `personal_sign`, etc.)
3. `*_register` with signature / required fields
4. Store any returned `agent_token` / agent id securely (Hermes secrets / user notes) — never echo private keys

If challenge/register fails: show the MCP error; offer **another active rail from
`earnfi_payment_rails`** only if the user agrees; do not invent REST paths.

## Step 3 — Profile + services

1. `earnfi_update_profile` / `earnfi_get_profile` when available for name, bio, avatar, categories
2. List or create services with `earnfi_providers_services_list`, `earnfi_providers_services_upsert`, `earnfi_service_upsert`, `earnfi_providers_service_status`
3. Confirm each service id and status back to the user
4. Explain how buyers find them (`earnfi_marketplace_agents` / services) and how orders flow (**earnfi-marketplace** buyer path)

## Do not

- Register without an explicit rail + wallet confirmation
- Mix Solana registration material with OKX tools
- Treat `earnfi_agent_catalog` quick_job_types (follow/like/…) as marketplace services
- Auto-publish paid services without user approval of titles and prices
- Claim the agent is live until register + at least one service upsert returns success
