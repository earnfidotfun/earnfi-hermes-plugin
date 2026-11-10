---
name: earnfi-troubleshooting
description: >-
  Diagnose EarnFi MCP connectivity, Hermes deferred tool names, wrong-network
  payments, version confusion, 402 loops, and settlement doubt.
license: MIT
metadata:
  author: earnfi
  version: "1.3.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Troubleshooting

1. `/earnfi-status` or `earnfi_doctor` — reports **Hermes plugin version** and **MCP server card version** separately, plus four peer networks.
2. `/earnfi-smoke` for read-only checks.
3. Confirm MCP URL `https://app.earnfi.fun/mcp` and plugin enabled. Server key must be `earnfi-api` (not `earnfi`).
4. **“not a known tool name” for `earnfi_*`:** use exact `mcp__earnfi_api__earnfi_…` from `tool_search` / `tool_call`. Bare names always fail. Doctor is not a substitute for marketplace/payment MCP tools.
5. Classify:

| Symptom | Likely cause |
|---------|----------------|
| Host unreachable | Network / DNS / TLS |
| Few MCP tools / only doctor | MCP server named `earnfi` colliding with native toolset; rename to `earnfi-api`, reload |
| Missing Base/NEAR register or `payment_network` | Stale session. `/reload-mcp` or new chat. Live MCP 2.1.0+ has them. |
| “Only Solana + OKX” | Wrong. Product answer is four peers: Solana, Base, NEAR, OKX. See **earnfi-payments**. |
| “Marketplace requires OKX” | Wrong. Any of the four networks works for sellers. |
| Confusing plugin vs MCP version | Plugin = Hermes package (`plugin.yaml`). MCP = server card. Doctor prints both. |
| Register 404 | Wrong network tool family |
| 402 looping | Wrong network proof or params changed between quote and pay |
| `payment_network_unavailable` | That network missing from this quote; try another of the four |
| Auth errors | Token / wallet binding; pay-first may still work |
| Tasks vs Jobs vs marketplace | Re-read **earnfi-overview** |

6. Settlement unclear → re-fetch job/order/deal + receipt tools.
7. Never bypass Hermes approval or EarnFi payment gates.
8. Register signature as `payment_signature` → always wrong.
