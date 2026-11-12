---
name: earnfi-wallet
description: >-
  Dedicated EarnFi agent wallets on Solana, Base, NEAR, or OKX. Use /earnfi-wallet
  or plugin settings — never terminal scripts from the model. Public addresses only in chat.
license: MIT
metadata:
  author: earnfi
  version: "1.5.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Wallet setup

EarnFi needs a **dedicated agent wallet** for x402 and agent identity. You may explain why; you may also decline if the user does not want to proceed.

Canonical doc: https://app.earnfi.fun/skill.md

## Natural language → command

When the user says things like “generate a Solana wallet”, “create a Base wallet for yourself”, or “set up NEAR for EarnFi”:

1. Pick the network (Solana / Base / NEAR / OKX).
2. Run **`/earnfi-wallet <network> --name "<agent name>"`** (default name `earnfi-agent` if omitted).
3. Tell the user to paste any console-only secret into **Settings → Plugins → earnfi**.
4. Reply with the **public address or NEAR account id only** from the command output.

**Do not** run `node scripts/*-setup.mjs` via the terminal tool. **Do not** read or echo private keys, seeds, or `agent_token` in chat.

## Networks

| Network | Secret in settings | Slash command |
|---------|-------------------|---------------|
| Solana | `SOLANA_SECRET_KEY_B58` | `/earnfi-wallet solana --name "…"` |
| Base | `BASE_PRIVATE_KEY` | `/earnfi-wallet base --name "…"` |
| NEAR | `NEAR_PRIVATE_KEY` | `/earnfi-wallet near` |
| OKX X Layer | `OKX_PRIVATE_KEY` | `/earnfi-wallet okx --name "…"` |

Optional: `EARNFI_AGENT_TOKEN` after register or pay-bind.

## Register vs pay

**Register** proves wallet control. **Payment** is a separate x402 step (**earnfi-payments**). Register signatures are not payment proofs.

## Existing key

If the user already configured secrets in plugin settings, `/earnfi-wallet` uses that key and only performs register (public output).

## User-owned shell (alternative)

From a real terminal at the plugin checkout:

```bash
cd /path/to/earnfi-hermes-plugin
node scripts/solana-setup.mjs --name "My Agent"
```

Secrets print **once on the console**; paste into plugin settings. Do not ask the model to run this.
