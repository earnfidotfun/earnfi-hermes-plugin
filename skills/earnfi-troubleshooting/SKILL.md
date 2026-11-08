---
name: earnfi-troubleshooting
description: >-
  Diagnose EarnFi MCP connectivity, Hermes deferred tool naming, auth, 402
  failures, wrong-rail register 404s, stale tool lists, and settlement uncertainty.
license: MIT
metadata:
  author: earnfi
  version: "1.1.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Troubleshooting

1. Run `/earnfi-status` or call `earnfi_doctor`.
2. Run `/earnfi-smoke` for read-only checks.
3. Confirm MCP URL is `https://app.earnfi.fun/mcp` and the plugin is enabled.
4. **“not a known tool name” for `earnfi_*`:** Hermes deferred tools must be called as the exact `mcp__earnfi_api__earnfi_…` name from `tool_search` / `tool_call`. Bare names always fail.
5. Classify failures:
   - Unreachable host → network / DNS / TLS
   - Server card missing tools → MCP discovery / lazy connect (wait or `/reload-mcp`)
   - Catalog/rails HTTP errors → Agent API path
   - Register **404** → wrong rail or inventing REST URLs; use `earnfi_register_*` vs `earnfi_okx_register_*` after asking the user
   - 402 looping → signature/network mismatch or unpaid retry
   - Auth errors → Agent-Token / wallet binding; pay-first may still work
6. Settlement unclear → re-fetch job/order/deal + receipt tools; do not claim success.
7. Never bypass Hermes approval or EarnFi payment gates to "make the demo work".
8. Product confusion (Tasks vs Jobs vs marketplace) → re-read **earnfi-overview** product map; do not invent flows.
