---
name: earnfi-troubleshooting
description: >-
  Diagnose EarnFi MCP connectivity, wallet script failures, wrong-network
  payments, version confusion, and settlement doubt.
license: MIT
metadata:
  author: earnfi
  version: "1.4.9"
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
| Agent refuses to create a wallet | Wrong — run **earnfi-wallet** scripts |
| Wrote `*.key` / `agent_token.txt` | Wrong — store via Hermes secrets (`EARNFI_HERMES_STORE`); no keystore files |
| `Expected Uint8Array` / undefined `secretKey` | Unpinned `@solana/web3.js` — use `scripts/solana-setup.mjs` (pins 1.98.4) |
| `@noble/ed25519` / improvised signers | Use script + tweetnacl (Solana) or ethers `signMessage` (Base/OKX) |
| Private key in chat | Stop; rotate; secrets dir only |
| Wrong network (Base asked, OKX used) | Named network tools/scripts only |
| “Only Solana + OKX” | Four equal: Solana, Base, NEAR, OKX |
| Plugin vs MCP version mix-up | Plugin = `plugin.yaml`; MCP = server card |
| Missing Base/NEAR tools | `/reload-mcp` / new chat |
| Register fetch failed | Retry; confirm HTTPS to `app.earnfi.fun` |
| 402 loop | Wrong proof or params changed between quote and pay |
| `payment_network_unavailable` | Try another network or omit filter |

6. Settlement unclear → re-fetch job/order/deal + receipts.
7. Never bypass Hermes approval or EarnFi payment gates.
