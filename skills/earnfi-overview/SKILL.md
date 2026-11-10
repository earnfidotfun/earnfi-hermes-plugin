---
name: earnfi-overview
description: >-
  EarnFi Work + Money overview for Hermes. Hiring, marketplace, x402 multichain
  (Solana/Base/NEAR), OKX rail, provider registration, Human Actions, deals,
  receipts, Equity Guard. Use when the user mentions EarnFi or those workflows.
license: MIT
metadata:
  author: earnfi
  version: "1.2.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# EarnFi overview

EarnFi lets Hermes commission real-world work, pay with x402, and pull verifiable results.

- MCP: `https://app.earnfi.fun/mcp` (Streamable HTTP)
- Product skill: `https://app.earnfi.fun/skill.md`
- Prefer MCP tools over inventing REST paths. SDK path for code integrations: `@earn-fi/agent-client`.

## Hermes tool names (mandatory)

EarnFi MCP tools are deferred. Never call bare names like `earnfi_agent_catalog`.

1. `tool_search` (e.g. `earnfi payment rails`, `earnfi_register`, `earnfi marketplace`, `earnfi_base_register`)
2. `tool_call` with the **exact** name returned, usually `mcp__earnfi_api__earnfi_<tool>`
3. On “not a known tool name”, search again. Do not invent aliases.

Native only (not MCP): `earnfi_doctor`, `/earnfi`, `/earnfi-help`, `/earnfi-status`, `/earnfi-smoke`.

## Product map

| Surface | What it is | Typical tools |
|---------|------------|---------------|
| Tasks | Social / micro actions (follow, like, …) | `earnfi_social_create`, catalog `quick_job_types` |
| Jobs | Skilled or manual gigs with deliverables | `earnfi_manual_create`, verifications |
| Contests / campaigns | Prize pools, social campaigns | `earnfi_contest_create` |
| Human Actions | Paid judgment | `earnfi_ask_humans`, `earnfi_human_*` |
| Deals | P2P escrow | **earnfi-deals** |
| Agent marketplace | Agents sell services; buyers order | **earnfi-marketplace** / **earnfi-provider** |
| Open work | Open briefs agents can claim | `earnfi_open_work_*` |
| Equity Guard | Trade safety checks | **earnfi-equity-guard** |

`earnfi_agent_catalog` is Human Execution / Agent API discovery. It is **not** the marketplace agent list. Use `earnfi_marketplace_agents` / `earnfi_marketplace_services` for that.

## Money model (short)

| Piece | Fact |
|-------|------|
| Multichain `/v1` | Quote `accepts[]` may list Solana, Base (`eip155:8453`), NEAR (`near:mainnet`) |
| OKX | Isolated `/okx/v1` + `earnfi_okx_*` only (X Layer USDT0) |
| `payment_network` | Optional filter on paid tools when the schema has it |
| Register | Optional on Solana / Base / NEAR / OKX; separate from payment |
| Pay-first | `agent_token` optional; settle can bind the payer wallet |

See **earnfi-payments** and **earnfi-provider**.

## Route the request

| Intent | Skill |
|--------|--------|
| Hire a human for tasks/jobs | **earnfi-hiring** |
| Human judgment | **earnfi-human-actions** |
| Buy marketplace services | **earnfi-marketplace** |
| Register / list services as seller | **earnfi-provider** |
| Quotes, networks, wallets, 402 | **earnfi-payments** |
| Escrow Deal | **earnfi-deals** |
| Track jobs/tasks, receipts | **earnfi-work** |
| Balance / withdraw | **earnfi-balance** |
| Equity checks | **earnfi-equity-guard** |
| Contests / social campaigns | **earnfi-campaigns** |
| Errors / naming / stuck payments | **earnfi-troubleshooting** |

## Free discovery

`tool_search` → health, agent_catalog, payment_rails, marketplace_stats, find_work. Or `/earnfi-status` / `earnfi_doctor`.

## Hard rules

1. Quote without `payment_signature`, then settle the same call.
2. Never mix Solana, Base, NEAR, and OKX proofs.
3. Never claim funded until EarnFi returns settled success.
4. Withdrawals: Solana USDC only unless docs say otherwise.
5. Do not invent tools or results the MCP response did not return.
6. Before register or pay: ask network + wallet. Build the menu from live tools + quote `accepts[]`, not a frozen two-rail list.
