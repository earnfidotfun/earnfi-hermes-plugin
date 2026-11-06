---
name: earnfi-campaigns
description: >-
  EarnFi social campaigns and contests — create, fund, track participation,
  leaderboards and winners.
license: MIT
metadata:
  author: earnfi
  version: "1.0.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Campaigns & contests

- Social: `earnfi_social_create` (and OKX `earnfi_okx_social_create` only on OKX rail)
- Contest: `earnfi_contest_create`, `earnfi_list_contest_submissions`, `earnfi_contest_leaderboard`, `earnfi_mark_contest_winner`
- Interrupt / quick human prompts: `earnfi_interrupt_create`

Always apply **earnfi-payments** before treating a campaign as funded. Confirm prize pools and fees from the quote, not guesses.
