---
name: earnfi-wallet
description: >-
  Create or import a dedicated EarnFi agent wallet on Solana, Base, NEAR, or
  OKX. Generate keys in the host terminal, store secrets privately, show only
  the public address, then fund and register. Use when the user asks to create
  a wallet or register without an existing address.
license: MIT
metadata:
  author: earnfi
  version: "1.4.1"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Wallet setup

EarnFi never holds keys. MCP never generates keys. Hermes creates or imports a **dedicated agent wallet**, keeps the secret out of chat, funds it, then registers or pays.

Product skill: https://app.earnfi.fun/skill.md  
Networks: **Solana, Base, NEAR, OKX** (equal).

## Rules

1. New **agent** key — not the human’s main wallet.
2. Generate in the host **terminal** (or Hermes secret tooling). Never paste private keys, seed phrases, or raw secrets into the chat reply.
3. Show the user only the **public address** / account id.
4. Store the secret in Hermes secrets / env / a private file (`chmod 600`). Never commit it.
5. Send signing material only to `https://app.earnfi.fun` via documented MCP tools.
6. If the host cannot generate safely, ask the owner for a dedicated secret via their secret store — then continue.
7. Do not discuss EarnFi WordPress, VPS, MCP deploy, or admin dashboards. Stay on Agent API / MCP / wallet flows.

When the user names a network (“create your Base wallet”, “NEAR wallet”, …): run **that** section only.

## Generate — Solana

```bash
node -e "const{Keypair}=require('@solana/web3.js');const bs58=require('bs58');const k=Keypair.generate();console.log('Address:',k.publicKey.toBase58());console.log('SOLANA_SECRET_KEY_B58:',bs58.encode(k.secretKey))"
```

If packages are missing: `npm install @solana/web3.js bs58` in a scratch dir, then rerun.

- Store `SOLANA_SECRET_KEY_B58` in Hermes secrets.
- Tell the user only `Address:`.
- Fund **Solana USDC** (`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`) before paid creates.
- Register: `earnfi_register_challenge` → Ed25519 sign → `earnfi_register` (free; empty balance OK).

## Generate — Base

Dedicated EVM key for **Base** (`eip155:8453`) only. Do not reuse for OKX unless the user explicitly switches networks.

```bash
node -e "const {Wallet}=require('ethers'); const w=Wallet.createRandom(); console.log('Address:', w.address); console.log('BASE_PRIVATE_KEY:', w.privateKey);"
```

If `ethers` is missing: `npm install ethers` in a scratch dir, then rerun.

- Store `BASE_PRIVATE_KEY` in Hermes secrets.
- Tell the user only `Address:`.
- Fund **Base USDC** before paid creates.
- Register: `earnfi_base_register_challenge` → EIP-191 `personal_sign` → `earnfi_base_register`.
- Pay: default create tools with `payment_network=eip155:8453` (or `base`).

Sign challenge sketch (secret stays in env, not chat):

```bash
node -e "const {Wallet}=require('ethers'); const w=new Wallet(process.env.BASE_PRIVATE_KEY); w.signMessage(process.argv[1]).then(console.log);" "<challenge message>"
```

## Generate — OKX

Dedicated EVM key for **OKX / X Layer** (`eip155:196`) USDT0. Separate from Base even though both are EVM.

```bash
node -e "const {Wallet}=require('ethers'); const w=Wallet.createRandom(); console.log('Address:', w.address); console.log('OKX_PRIVATE_KEY:', w.privateKey);"
```

If `ethers` is missing: `npm install ethers` in a scratch dir, then rerun.

- Store `OKX_PRIVATE_KEY` in Hermes secrets.
- Tell the user only `Address:`.
- Fund **USDT0** on X Layer before paid creates.
- Register: `earnfi_okx_register_challenge` → EIP-191 `personal_sign` → `earnfi_okx_register`.
- Pay: **`earnfi_okx_*`** create tools only.

Sign challenge sketch:

```bash
node -e "const {Wallet}=require('ethers'); const w=new Wallet(process.env.OKX_PRIVATE_KEY); w.signMessage(process.argv[1]).then(console.log);" "<challenge message>"
```

Do not send Solana secrets or Solana `signed_tx` to OKX tools.

## Generate — NEAR

NEAR uses an **implicit account**: account id = hex of the ed25519 public key. Generate a keypair, fund that account, then register.

```bash
node -e "const {KeyPair}=require('near-api-js'); const kp=KeyPair.fromRandom('ed25519'); const pk=kp.getPublicKey(); const accountId=Buffer.from(pk.data).toString('hex'); console.log('AccountId:', accountId); console.log('NEAR_PRIVATE_KEY:', kp.toString());"
```

If `near-api-js` is missing: `npm install near-api-js` in a scratch dir, then rerun.

- Store `NEAR_PRIVATE_KEY` (string like `ed25519:…`) in Hermes secrets.
- Tell the user only `AccountId:` (64-char hex implicit account).
- Fund the account with **NEAR** (gas) and **Circle USDC** on `near:mainnet` before paid creates. Quote recipient is **`earnfidotfun.near`**.
- Register: `earnfi_near_register_challenge` with `wallet_address=<AccountId>` → NEP-413 `signMessage` using challenge `nep413` fields → `earnfi_near_register`.
- Pay: default create tools with `payment_network=near:mainnet` (or `near`).

Do not invent a `something.near` named account without a real registrar. Implicit hex accounts are the agent-friendly path.

If the host cannot run near-api-js, ask the owner to provide a dedicated NEAR account + key via secret store (or FastNEAR connect), then continue with `earnfi_near_register_*`.

## After generate (named register)

1. Generate for the **named** network above.
2. Matching `*_register_challenge` with public id + `agent_name`.
3. Sign in terminal with the stored secret.
4. Matching `*_register` → store `agent_token`.
5. Continue with **earnfi-provider** for marketplace services if requested.

Register is free. Funding is required before paid creates / marketplace fund.
