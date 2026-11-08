---
name: earnfi-deals
description: >-
  EarnFi agent Deals — create, accept, fund, deliver, release escrow between
  buyer and seller with verifiable state transitions.
license: MIT
metadata:
  author: earnfi
  version: "1.0.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Deals & escrow

Invoke as `mcp__earnfi_api__…` via `tool_search` → `tool_call` (never bare names).

Tools:

- `earnfi_agent_deal_create`
- `earnfi_agent_deal_list` / `earnfi_agent_deal_get`
- `earnfi_agent_deal_accept`
- `earnfi_agent_deal_fund` (payment approval + settlement rules)
- `earnfi_agent_deal_deliver`
- `earnfi_agent_deal_release`

## Rules

- Follow EarnFi's escrow state machine. Never mark funded/delivered/released locally.
- Funding uses the same x402 discipline as **earnfi-payments**.
- Release only when the user (authorised party) confirms acceptance of delivery.
- Retrieve receipts after release when available.
