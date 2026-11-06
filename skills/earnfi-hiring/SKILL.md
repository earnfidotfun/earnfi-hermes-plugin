---
name: earnfi-hiring
description: >-
  Hire humans on EarnFi end-to-end: scope, budget, approve payment, fund,
  monitor delivery, inspect evidence, complete with receipt.
license: MIT
metadata:
  author: earnfi
  version: "1.0.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Hire a human worker (workflow)

Use this when Hermes must get a **person** to do real-world or hands-on work (photos, site check, QA, delivery confirmation).

## Sequence

1. **Understand the objective** — location, deliverables, deadline, budget, evidence required.
2. **Choose work type**
   - Structured field/manual task → `earnfi_manual_create` or `earnfi_hire_worker`
   - Catalog discovery → `earnfi_search_capabilities` / `earnfi_find_work` / `earnfi_agent_catalog`
   - Human judgment variants → use **earnfi-human-actions** instead
3. **Collect missing requirements** before paying (title, instructions, slots, reward_per_user).
4. **Quote** — call the create/hire tool **without** `payment_signature`. Expect `requires_payment` / accepts[].
5. **Disclose & approve** — amount, asset, network, purpose. Wait for explicit user approval.
6. **Settle** — sign the matching accept; retry **same tool** with `payment_signature`. Prefer `idempotency_key`.
7. **Verify funding** — success only if EarnFi confirms settlement (job/action id + not `requires_payment`). Store `secret` / `agent_token` if returned.
8. **Monitor** — `earnfi_check_work`, `earnfi_get_job`, `earnfi_list_submissions`, or Human Action result tools.
9. **Inspect evidence** — submissions, photos, text; request revision if supported.
10. **Finish** — `earnfi_get_receipt` / `earnfi_get_work_receipt` / `earnfi_receipt_get`; summarize for the user.

## Do not

- Skip approval because a tool is "just creating a draft".
- Report "funded" from a wallet signature alone.
- Mix OKX and Solana payment material.
- Fabricate worker identities or fake evidence.
