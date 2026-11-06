---
name: earnfi-troubleshooting
description: >-
  Diagnose EarnFi MCP connectivity, auth, 402 failures, wrong-network
  signatures, stale tool lists, and settlement uncertainty.
license: MIT
metadata:
  author: earnfi
  version: "1.0.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Troubleshooting

1. Run `/earnfi-status` or call `earnfi_doctor`.
2. Run `/earnfi-smoke` for read-only checks.
3. Confirm MCP URL is `https://app.earnfi.fun/mcp` and the plugin is enabled.
4. Classify failures:
   - Unreachable host → network / DNS / TLS
   - Server card missing tools → MCP discovery problem
   - Catalog/rails HTTP errors → Agent API path
   - 402 looping → signature/network mismatch or unpaid retry
   - Auth errors → Agent-Token / wallet binding; pay-first may still work
5. Settlement unclear → re-fetch job/order/deal + receipt tools; do not claim success.
6. Never bypass Hermes approval or EarnFi payment gates to "make the demo work".
