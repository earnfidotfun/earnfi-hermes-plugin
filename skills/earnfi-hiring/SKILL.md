---
name: earnfi-hiring
description: >-
  Hire humans on EarnFi end-to-end: Tasks (social micro-actions) or Jobs
  (skilled/manual gigs), budget, approve payment, fund, monitor delivery,
  inspect evidence, complete with receipt. Not for marketplace agent services.
license: MIT
metadata:
  author: earnfi
  version: "1.1.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Hire a human (Tasks & Jobs)

Use when Hermes must get a **person** to do work. This is **not** the agent marketplace (see **earnfi-marketplace** / **earnfi-provider**).

Invoke MCP tools only as `mcp__earnfi_api__…` via `tool_search` → `tool_call`.

## Tasks vs Jobs

| Kind | Examples | Create tools |
|------|----------|--------------|
| **Tasks** | Follow, like, repost, quote, comment, video view, combos | `earnfi_social_create` (see `quick_job_types` on `earnfi_agent_catalog`) |
| **Jobs** | Manual / freelance gigs with deliverables & review | `earnfi_manual_create`, `earnfi_hire_worker`, hire listings |
| **Human Actions** | Ask, review, vote, test, research, … | **earnfi-human-actions** |
| **Contests** | Prize pools | **earnfi-campaigns** |

Ask the user which kind they want if unclear. Do not call social Task types “jobs” in user-facing copy.

## Sequence

1. **Objective** — location, deliverables, deadline, budget, evidence.
2. **Choose type** — Tasks / Jobs / Human Actions / Contest (table above).
3. **Discovery (optional)** — `earnfi_search_capabilities`, `earnfi_find_work`; use `earnfi_agent_catalog` for Task/Job type policies — **not** for marketplace agent profiles.
4. **Collect requirements** before paying.
5. **Quote** — create tool **without** `payment_signature`.
6. **Disclose & approve** — amount, asset, network, purpose.
7. **Settle** — matching accept + same tool with `payment_signature` (**earnfi-payments**).
8. **Verify funding** — EarnFi settled success only.
9. **Monitor** — `earnfi_check_work`, `earnfi_get_job`, submissions / Human Action results.
10. **Receipt** — `earnfi_get_receipt` / related receipt tools.

## Do not

- Skip approval because a tool is "just creating a draft".
- Report "funded" from a wallet signature alone.
- Mix OKX and Solana payment material.
- Fabricate worker identities or fake evidence.
- Confuse marketplace agent services with human Task/Job creates.
