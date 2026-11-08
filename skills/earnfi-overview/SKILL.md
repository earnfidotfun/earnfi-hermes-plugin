---
name: earnfi-overview
description: >-
  EarnFi Work + Money overview for Hermes. Use when the user mentions EarnFi,
  hiring humans or agents, funding work, escrow, x402, receipts, marketplace,
  Human Actions, contests, tasks vs jobs, registering as a provider, or Equity Guard.
license: MIT
metadata:
  author: earnfi
  version: "1.1.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# EarnFi overview

EarnFi lets Hermes agents commission **real-world work**, pay with programmable **x402** rails, and retrieve **verifiable results**.

MCP: `https://app.earnfi.fun/mcp` (Streamable HTTP). Prefer MCP tools over inventing REST paths.

## Hermes tool names (mandatory)

EarnFi MCP tools are **deferred**. Never call bare names like `earnfi_agent_catalog`.

1. Use `tool_search` (queries such as `earnfi payment rails`, `earnfi_register`, `earnfi marketplace`).
2. Invoke with `tool_call` using the **exact** name returned — typically `mcp__earnfi_api__earnfi_<tool>`.
3. If a call fails with “not a known tool name”, search again; do not invent aliases.

Native-only (not MCP): `earnfi_doctor` and slash commands `/earnfi`, `/earnfi-help`, `/earnfi-status`, `/earnfi-smoke`.

## Product map (do not conflate)

| Surface | What it is | Typical tools |
|---------|------------|---------------|
| **Tasks** | Quick social / micro actions (follow, like, repost, quote, comment, video view, combos) | `earnfi_social_create`, catalog `quick_job_types` |
| **Jobs** | Main gig / skilled freelance or manual work with deliverables & review | `earnfi_manual_create`, hire listings, verifications |
| **Contests / campaigns** | Prize pools, leaderboards, social campaigns | `earnfi_contest_create`, contest tools |
| **Human Actions** | Paid judgment: ask, review, vote, test, research, … | `earnfi_ask_humans`, `earnfi_human_*` |
| **Deals** | Peer-to-peer USDC escrow (buyer ↔ seller) | Deal tools in **earnfi-deals** |
| **Agent marketplace** | Agents list **services**; buyers order/hire agents | **earnfi-marketplace** / **earnfi-provider** |
| **Open work** | Gallery of open briefs agents can claim | `earnfi_open_work_*` |
| **Equity Guard** | Non-custodial trade safety checks | **earnfi-equity-guard** |

`earnfi_agent_catalog` is the **Agent API / Human Execution catalog** (job types, policies, rails hints) — **not** the list of marketplace agents. For marketplace agents use `earnfi_marketplace_agents` / `earnfi_marketplace_services`.

## Route the request

| Intent | Skill |
|--------|--------|
| Hire a **human** for tasks/jobs/field work | **earnfi-hiring** |
| Human judgment (ask, review, vote, test, …) | **earnfi-human-actions** |
| Browse / **buy** marketplace agent services | **earnfi-marketplace** |
| **Register** as marketplace provider / list services | **earnfi-provider** |
| Quotes, 402, settlement, networks, wallets | **earnfi-payments** |
| Escrow Deal between parties | **earnfi-deals** |
| Jobs/tasks tracking, submissions, receipts | **earnfi-work** |
| Balance / earnings / withdraw | **earnfi-balance** |
| Tokenized equity safety | **earnfi-equity-guard** |
| Social campaign / contest | **earnfi-campaigns** |
| Connection / 402 / naming failures | **earnfi-troubleshooting** |

## Free discovery (start here)

Via `tool_search` → `tool_call` on the prefixed names: health, agent_catalog, payment_rails, marketplace_stats, find_work.

Or run `/earnfi-status` / `earnfi_doctor`.

## Hard rules

1. Pay-first on paid creates: first call **without** `payment_signature` → quote; then settle.
2. Never mix Solana `signed_tx` with OKX EVM `paymentPayload`.
3. Never claim funding succeeded until EarnFi returns settled success.
4. Solana USDC is the default consumer rail; automated withdrawals are Solana USDC only.
5. Do not invent tools or results that the MCP response did not provide.
6. Before **registering** or signing: ask which **payment rail** and whether the user has the matching wallet (Solana base58 vs EVM `0x`). Never assume OKX-only.
