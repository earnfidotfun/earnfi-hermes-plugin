---
name: earnfi-troubleshooting
description: >-
  Diagnose EarnFi MCP connectivity, wallet setup, wrong-network payments,
  version confusion, and settlement doubt.
license: MIT
metadata:
  author: earnfi
  version: "1.5.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Troubleshooting

1. `/earnfi-status` — Hermes **plugin** version vs MCP **server card**; four networks.
2. `/earnfi-smoke`.
3. MCP URL `https://app.earnfi.fun/mcp`; server key `earnfi-api`.
4. Bare `earnfi_*` → `mcp__earnfi_api__…` from `tool_search`.
5. Classify:

| Symptom | Fix |
|---------|-----|
| Need a wallet | `/earnfi-wallet <network>` — not `node scripts/…` from terminal tool |
| Secret in chat / tool output | Rotate key; paste only in plugin settings |
| `tty_required_for_keygen` | Use `/earnfi-wallet` from command input, or user shell |
| Wrote `*.key` / `agent_token.txt` | Wrong — plugin settings only (rule 11) |
| npm deps missing | Plugin runs `npm ci` in plugin root (`package-lock.json`) |
| Wrong network | Named network tools only |
| “Only Solana + OKX” | Four equal: Solana, Base, NEAR, OKX |
| 402 loop | Same args + matching `payment_signature`; try `earnfi_sign_x402` |
| SDK / terminal spend | Use MCP + `earnfi_sign_x402` only |

6. Settlement unclear → re-fetch job/order/deal + receipts.
7. Never bypass Hermes approval or EarnFi payment gates.
