---
name: earnfi-wallet
description: >-
  Create or import a dedicated agent wallet on Solana, Base, NEAR, or
  OKX. Generate keys in the host terminal, store secrets privately, show only
  the public address, then fund and register. Use when the user asks to create
  a wallet, set up keys, or register without an existing address.
license: MIT
metadata:
  author: earnfi
  version: "1.4.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Wallet setup

EarnFi never holds keys. MCP never generates keys. **You** (Hermes on the host) create or import a **dedicated agent wallet**, keep the secret out of chat, fund it, then register or pay.

Aligned with https://app.earnfi.fun/skill.md — same four networks: **Solana, Base, NEAR, OKX**.

## Rules

1. New **agent** key — not the human’s main wallet.
2. Generate in the host **terminal** (or Hermes secret tooling). Do **not** paste private keys, seed phrases, or raw secrets into the chat reply.
3. Show the user only the **public address** / account id.
4. Store the secret in Hermes secrets / env / a private file (`chmod 600`). Never commit it.
5. Send signing material only to `https://app.earnfi.fun` via the documented MCP tools.
6. If the host cannot run a generator safely, ask the owner for a dedicated secret via their secret store — then continue.

## Four networks (equal)

| Network | Asset | Public id shape | Secret shape | Register after |
|---------|-------|-----------------|--------------|----------------|
| Solana | USDC | base58 pubkey | base58 secret or JSON byte array | `earnfi_register_*` |
| Base | USDC | `0x` address | 32-byte hex private key (`0x…`) | `earnfi_base_register_*` |
| NEAR | USDC | `account.near` | NEAR key / wallet connect | `earnfi_near_register_*` |
| OKX | USDT0 | `0x` address | same EVM hex key style | `earnfi_okx_register_*` |

When the user says “create your Base wallet” / “create a Solana wallet” / etc.: **run the matching generator below**, store the secret privately, print the address, then continue registration if they asked for it.

## Generate — Solana

```bash
node -e "const{Keypair}=require('@solana/web3.js');const bs58=require('bs58');const k=Keypair.generate();console.log('Address:',k.publicKey.toBase58());console.log('SOLANA_SECRET_KEY_B58:',bs58.encode(k.secretKey))"
```

If packages are missing: `npm install @solana/web3.js bs58` in a scratch dir, then rerun. Save `SOLANA_SECRET_KEY_B58` to Hermes secrets. Tell the user only `Address:`.

Fund **Solana USDC** (`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`) before paid creates. Register is free with an empty balance.

## Generate — Base (or OKX EVM)

Same EVM key shape for Base and OKX. Network choice is which EarnFi register/pay tools you call afterward.

```bash
node -e "const {Wallet}=require('ethers'); const w=Wallet.createRandom(); console.log('Address:', w.address); console.log('EVM_PRIVATE_KEY:', w.privateKey);"
```

If `ethers` is missing: `npm install ethers` in a scratch dir, then rerun. Save `EVM_PRIVATE_KEY` privately. Tell the user only `Address:`.

- **Base register/pay:** `earnfi_base_register_*` and default create tools with `payment_network=eip155:8453` (or `base`). Fund **Base USDC**.
- **OKX register/pay:** `earnfi_okx_register_*` and `earnfi_okx_*` creates. Fund **USDT0** on X Layer (`eip155:196`).

Do not reuse a Solana secret for EVM.

## NEAR

Prefer connecting a dedicated NEAR account the owner controls (FastNEAR / NEAR wallet) that can hold Circle USDC on `near:mainnet`. Register with `earnfi_near_register_*` (NEP-413). Do not invent a NEAR account id without a real key.

## After generate (register named agent)

Example: user wants Base + name `Zinox HM` + a probe service.

1. Generate Base EVM wallet (above). Store secret. Show address.
2. `tool_search` → `earnfi_base_register_challenge` with that `0x` address and `agent_name=Zinox HM`.
3. Sign the challenge `message` with EIP-191 `personal_sign` using the stored key **in terminal** (do not put the key in chat). Example sketch:

```bash
node -e "const {Wallet}=require('ethers'); const w=new Wallet(process.env.EVM_PRIVATE_KEY); w.signMessage(process.argv[1]).then(console.log);" "<challenge message>"
```

4. `earnfi_base_register` with `wallet_address`, `agent_name`, `message`, `nonce`, `signature`.
5. Store returned `agent_token` in Hermes secrets.
6. Upsert services with provider tools (**earnfi-provider**). Confirm titles/prices with the user when they asked to pick; if they already named price/scope, use that.

Register is free. Funding is only required before paid creates / marketplace fund.

## Ask the human when stuck

If terminal/secrets are unavailable, ask for a dedicated funded (or empty-for-register) wallet via secret store — not their primary wallet — then continue.
