---
name: earnfi-human-actions
description: >-
  Paid Human Actions on EarnFi — ask, review, vote, test, research, verify,
  moderate, feedback. Pay-first x402; poll results; receipts.
license: MIT
metadata:
  author: earnfi
  version: "1.1.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Human Actions

Invoke as `mcp__earnfi_api__…` via `tool_search` → `tool_call` (never bare names).

Generic: `earnfi_human_action_create` with `action_type` in
`ask | review | vote | test | research | verify | moderate | feedback`.

Dedicated Solana-rail tools:

| Type | Tool |
|------|------|
| Ask | `earnfi_ask_humans` |
| Review | `earnfi_human_review` |
| Vote | `earnfi_human_vote` |
| Test | `earnfi_human_test` |
| Research | `earnfi_human_research` |
| Verify | `earnfi_human_verify` |
| Moderate | `earnfi_human_moderate` |
| Feedback | `earnfi_human_feedback` |

## Flow

1. Call without `payment_signature` → quote.
2. Confirm amount/network with the user.
3. Retry with `payment_signature`.
4. Poll `earnfi_human_action_result` with `action_id` + `secret`.
5. Attach receipt tools when the user needs proof.

OKX equivalents exist as `earnfi_okx_human_*` — only when the user explicitly wants the OKX USDT0 rail. Never mix rails.
