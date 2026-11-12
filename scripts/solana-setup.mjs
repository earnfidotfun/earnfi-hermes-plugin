#!/usr/bin/env node
/**
 * EarnFi Solana agent setup: generate key (pinned web3.js 1.x) + optional register.
 * Secrets: Settings → Plugins → earnfi (SOLANA_SECRET_KEY_B58, EARNFI_AGENT_TOKEN).
 * Never reads or writes keystore files (catalog rule 11).
 *
 * Usage: node solana-setup.mjs --name "My Agent" [--skip-register]
 * Prefer: /earnfi-wallet solana --name "My Agent"
 */
import { arg, has, pluginRequire, storeNewSecret } from './lib-deps.mjs';

const agentName = arg('--name', process.env.EARNFI_AGENT_NAME || 'earnfi-agent');
const skipRegister = has('--skip-register');
const apiBase = (process.env.EARNFI_AGENT_API_BASE || 'https://app.earnfi.fun/api/ai-agent/v1').replace(
  /\/$/,
  ''
);

const require = pluginRequire();
const { Keypair } = require('@solana/web3.js');
const bs58mod = require('bs58');
const bs58 = bs58mod.default || bs58mod;
const nacl = require('tweetnacl');

let kp;
let hermesStoreRequired = false;
if (process.env.SOLANA_SECRET_KEY_B58) {
  kp = Keypair.fromSecretKey(bs58.decode(process.env.SOLANA_SECRET_KEY_B58.trim()));
} else {
  kp = Keypair.generate();
  hermesStoreRequired = true;
  storeNewSecret('SOLANA_SECRET_KEY_B58', bs58.encode(kp.secretKey));
}

const address = kp.publicKey.toBase58();
const out = {
  network: 'solana',
  wallet_address: address,
  agent_name: agentName,
  secret_env: 'SOLANA_SECRET_KEY_B58',
  secret_saved_via: hermesStoreRequired ? 'console_once' : 'settings',
  registered: false,
  token_env: 'EARNFI_AGENT_TOKEN',
  token_saved_via: null,
};

if (!skipRegister) {
  const chUrl =
    `${apiBase}/register/challenge?wallet_address=${encodeURIComponent(address)}` +
    `&agent_name=${encodeURIComponent(agentName)}`;
  const chRes = await fetch(chUrl);
  const ch = await chRes.json().catch(() => ({}));
  if (!chRes.ok || !ch.message) {
    out.error = 'challenge_failed';
    out.detail = ch;
    console.log(JSON.stringify(out, null, 2));
    process.exit(1);
  }
  const sigBytes = nacl.sign.detached(Buffer.from(ch.message, 'utf8'), kp.secretKey);
  const body = {
    wallet_address: address,
    agent_name: ch.agent_name || agentName,
    message: ch.message,
    nonce: ch.nonce,
    signature: Array.from(sigBytes),
  };
  const regRes = await fetch(`${apiBase}/register`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', accept: 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await regRes.json().catch(() => ({}));
  if (!regRes.ok) {
    out.error = 'register_failed';
    out.detail = data;
    console.log(JSON.stringify(out, null, 2));
    process.exit(1);
  }
  out.registered = true;
  out.agent_name = data.agent_name || agentName;
  if (data.agent_token) {
    storeNewSecret('EARNFI_AGENT_TOKEN', String(data.agent_token));
    out.token_saved_via = 'console_once';
  }
}

console.log(JSON.stringify(out, null, 2));
