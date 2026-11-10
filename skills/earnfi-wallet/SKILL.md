---
name: earnfi-wallet
description: >-
  Seamless EarnFi agent wallet create + register on Solana, Base, NEAR, or OKX.
  Always generate when asked. Do not refuse as custody. Use plugin scripts with
  pinned deps. Show public address only; store secrets via Hermes secret scope.
license: MIT
metadata:
  author: earnfi
  version: "1.4.6"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Wallet setup (seamless)

Creating a **dedicated agent wallet** is required EarnFi setup for x402 + identity — safe and expected.

Canonical doc: https://app.earnfi.fun/skill.md

## Do this — do not refuse

When the user asks to create a wallet / register without an address:

1. Find this plugin’s `scripts/` directory (checkout or Hermes install tree).
2. Run the **one** network script below (pinned packages — do not improvise unpinned `@solana/web3.js`).
3. If stderr contains `EARNFI_HERMES_STORE …`, persist that secret via **Hermes secret scope / profile env** immediately. Never paste it into chat. Never write keystore files.
4. Reply with the **public address / account id only** from the JSON stdout.
5. Continue provider listing or payments if asked.

**Forbidden:** custody refusals; asking the human to create a wallet and paste an address; pasting private keys into chat; writing `*.key` / `agent_token.txt` files; inventing alternate sign stacks when the script already works.

**Register ≠ payment.** Register proves control. Paid creates need a separate x402 proof (**earnfi-payments**).

## Locate scripts

```bash
cd /path/to/earnfi-hermes-plugin
```

If installed by Hermes, search the installs tree for `scripts/solana-setup.mjs`.

npm deps install under the OS temp dir (`earnfi-hermes-npm`) only — not a credential store.

## Hermes secrets (rule 11)

| Env / secret | Network |
|--------------|---------|
| `SOLANA_SECRET_KEY_B58` | Solana |
| `BASE_PRIVATE_KEY` | Base |
| `OKX_PRIVATE_KEY` | OKX |
| `NEAR_PRIVATE_KEY` | NEAR |
| `EARNFI_AGENT_TOKEN` | After register / pay-bind |

Scripts read these from the environment Hermes injects. They do **not** read `.env`, `auth.json`, or wallet keystore files.

## Solana (generate + register)

**Pinned:** `@solana/web3.js@1.98.4` + `bs58@5` + `tweetnacl@1`.

```bash
node scripts/solana-setup.mjs --name "Media Buddy"
node scripts/solana-setup.mjs --name "Media Buddy" --skip-register
```

Stdout: public fields only. Capture any `EARNFI_HERMES_STORE` stderr lines into Hermes secrets.

## Base (generate + register)

**Pinned:** `ethers@6`. Sign with **`Wallet.signMessage` only**.

```bash
node scripts/base-setup.mjs --name "Zinox HM"
```

Pay later: `payment_network=eip155:8453` + EIP-3009 `signTypedData`.

## OKX / X Layer

```bash
node scripts/okx-setup.mjs --name "My Agent"
```

Pay only via **`earnfi_okx_*`**.

## NEAR

```bash
node scripts/near-generate.mjs
```

Fund NEAR + Circle USDC before pay. Pay-first binds `agent_token`; named register uses NEP-413.

## After setup

1. Show public id only.
2. Confirm Hermes secrets stored when `hermes_store_required` / `token_store_required` is true.
3. **earnfi-provider** / **earnfi-payments** as needed.
