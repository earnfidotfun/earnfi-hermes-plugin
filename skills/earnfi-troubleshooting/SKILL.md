---
name: earnfi-troubleshooting
description: >-
  Diagnose EarnFi MCP connectivity, Hermes deferred tool names, wrong-network
  payments, missing Base/NEAR register tools, 402 loops, and settlement doubt.
license: MIT
metadata:
  author: earnfi
  version: "1.2.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Troubleshooting

1. `/earnfi-status` or `earnfi_doctor`.
2. `/earnfi-smoke` for read-only checks.
3. Confirm MCP URL `https://app.earnfi.fun/mcp` and plugin enabled. Server key must be `earnfi-api` (not `earnfi`).
4. **“not a known tool name” for `earnfi_*`:** use exact `mcp__earnfi_api__earnfi_…` from `tool_search` / `tool_call`. Bare names always fail.
5. Classify:

| Symptom | Likely cause |
|---------|----------------|
| Host unreachable | Network / DNS / TLS |
| Few MCP tools / only doctor | MCP server named `earnfi` colliding with native toolset; rename to `earnfi-api`, reload |
| Missing `earnfi_base_register_*` / `earnfi_near_register_*` / `payment_network` | Hosted MCP behind Agent API skill. Say so. Offer Solana/OKX register tools that exist, or pay-first bind. Do not invent tools. |
| Register 404 | Wrong network tool family or invented REST path |
| 402 looping | Wrong network proof, params changed between quote and pay, or unpaid retry |
| `payment_network_unavailable` | Filter not in this quote. Omit filter or switch network. Stay on MCP. |
| Auth errors | Token / wallet binding. Pay-first may still work without prior register. |
| Tasks vs Jobs vs marketplace mix-up | Re-read **earnfi-overview** product map |

6. Settlement unclear → re-fetch job/order/deal + receipt tools. Do not claim success from a wallet UI alone.
7. Never bypass Hermes approval or EarnFi payment gates to force a demo.
8. Register signature used as `payment_signature` → always wrong. Re-quote and sign the payment accept.
