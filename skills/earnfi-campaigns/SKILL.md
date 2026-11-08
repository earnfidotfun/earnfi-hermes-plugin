---
name: earnfi-campaigns
description: >-
  EarnFi social Tasks/campaigns and contests — create, fund, track participation,
  leaderboards and winners. Distinguishes Tasks (like/follow/…) from Jobs and
  marketplace services.
license: MIT
metadata:
  author: earnfi
  version: "1.1.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Campaigns, Tasks & contests

Use `tool_search` → `tool_call` with exact `mcp__earnfi_api__…` names.

- **Social Tasks** (follow, like, repost, …): `earnfi_social_create` — and OKX `earnfi_okx_social_create` only on the OKX rail after the user chooses it
- **Contest**: `earnfi_contest_create`, `earnfi_list_contest_submissions`, `earnfi_contest_leaderboard`, `earnfi_mark_contest_winner`
- **Interrupt / quick human prompts**: `earnfi_interrupt_create`

Catalog `quick_job_types` describes **Tasks**, not marketplace agent services and not full freelance **Jobs**.

Always apply **earnfi-payments** before treating a campaign as funded. Confirm prize pools and fees from the quote, not guesses.
