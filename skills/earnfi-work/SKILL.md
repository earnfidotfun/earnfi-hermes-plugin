---
name: earnfi-work
description: >-
  EarnFi Tasks and Jobs tracking — social micro-tasks, manual/contest/interrupt
  work, poll status, submissions, verify, pause/close, receipts.
license: MIT
metadata:
  author: earnfi
  version: "1.1.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Tasks, Jobs & work tracking

Use `tool_search` → `tool_call` with exact `mcp__earnfi_api__…` names.

## Taxonomy

- **Tasks** — social micro-actions via `earnfi_social_create` (`quick_job_types` in catalog).
- **Jobs** — skilled/manual gigs via `earnfi_manual_create`, hire listings, verifications.
- **Contests / interrupts** — `earnfi_contest_create`, `earnfi_interrupt_create`.
- **Marketplace orders** — different surface; see **earnfi-marketplace**.

## Create (paid — see earnfi-payments)

- `earnfi_social_create` — Tasks
- `earnfi_manual_create` — Jobs
- `earnfi_contest_create`
- `earnfi_interrupt_create` / `earnfi_get_interrupt`
- Hire listing: `earnfi_hire_listing_create` / `earnfi_hire_listing_update`

OKX rail equivalents: `earnfi_okx_*` only when the user chose that rail.

## Track

- `earnfi_get_job`, `earnfi_get_job_detail`, `earnfi_get_job_users`, `earnfi_get_job_payments`
- `earnfi_list_submissions`, `earnfi_list_completions`
- `earnfi_list_agent_jobs`, `earnfi_check_work`, `earnfi_submit_work`

## Verify / manage

- `earnfi_list_verifications`, `earnfi_approve_verification`, `earnfi_reject_verification`
- `earnfi_pause_job`, `earnfi_close_job`, `earnfi_update_job_metadata`
- Contest: `earnfi_list_contest_submissions`, `earnfi_mark_contest_winner`, `earnfi_contest_leaderboard`

Distinguish **created** vs **funded**. A quote response is not a funded job/task.
