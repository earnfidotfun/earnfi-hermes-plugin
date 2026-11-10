---
name: earnfi-troubleshooting
description: >-
  Diagnose EarnFi MCP connectivity, deferred tool names, wallet setup failures,
  wrong-network payments, version confusion, and settlement doubt.
license: MIT
metadata:
  author: earnfi
  version: "1.4.1"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Troubleshooting

1. `/earnfi-status` — Hermes **plugin** version vs MCP **server card** version; four networks.
2. `/earnfi-smoke`.
3. MCP URL `https://app.earnfi.fun/mcp`; server key `earnfi-api` (not `earnfi`).
4. Bare `earnfi_*` → use `mcp__earnfi_api__…` from `tool_search`.
5. Classify:

| Symptom | Fix |
|---------|-----|
| “I can’t create a wallet” | Use **earnfi-wallet**: generate in terminal, secret in Hermes store, address only in chat |
| Private key in chat | Stop; rotate that key; store via secrets only |
| Wrong network (Base asked, OKX used) | Follow the user’s named network tools only |
| “Only Solana + OKX” | Wrong — four equal: Solana, Base, NEAR, OKX |
| Plugin vs MCP version mix-up | Plugin = `plugin.yaml`; MCP = server card |
| Missing Base/NEAR tools | `/reload-mcp` / new chat (MCP 2.1.0+) |
| 402 loop | Wrong proof or params changed between quote and pay |
| `payment_network_unavailable` | Try another of the four or omit filter |

6. Settlement unclear → re-fetch job/order/deal + receipts.
7. Never bypass Hermes approval or EarnFi payment gates.
