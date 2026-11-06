---
name: earnfi-work
description: >-
  EarnFi jobs — create social/manual/contest/interrupt work, poll status,
  list submissions, verify, pause/close, receipts.
license: MIT
metadata:
  author: earnfi
  version: "1.0.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Jobs & work tracking

## Create (paid — see earnfi-payments)

- `earnfi_social_create`
- `earnfi_manual_create`
- `earnfi_contest_create`
- `earnfi_interrupt_create` / `earnfi_get_interrupt`
- Hire listing: `earnfi_hire_listing_create` / `earnfi_hire_listing_update`

## Track

- `earnfi_get_job`, `earnfi_get_job_detail`, `earnfi_get_job_users`, `earnfi_get_job_payments`
- `earnfi_list_submissions`, `earnfi_list_completions`
- `earnfi_list_agent_jobs`, `earnfi_check_work`, `earnfi_submit_work`

## Verify / manage

- `earnfi_list_verifications`, `earnfi_approve_verification`, `earnfi_reject_verification`
- `earnfi_pause_job`, `earnfi_close_job`, `earnfi_update_job_metadata`
- Contest: `earnfi_list_contest_submissions`, `earnfi_mark_contest_winner`, `earnfi_contest_leaderboard`

Distinguish **created** vs **funded**. A quote response is not a funded job.
