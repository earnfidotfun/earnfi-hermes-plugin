#!/usr/bin/env node
/**
 * EarnFi Base agent setup: generate EVM key + optional register.
 * Secrets: Hermes profile env / secret scope only (BASE_PRIVATE_KEY, EARNFI_AGENT_TOKEN).
 * Never reads or writes keystore files (catalog rule 11).
 *
 * Usage: node base-setup.mjs --name "My Agent" [--skip-register]
 */
import { arg, emitHermesStore, ensureNpm, has } from './lib-deps.mjs';

const agentName = arg('--name', process.env.EARNFI_AGENT_NAME || 'earnfi-agent');
const skipRegister = has('--skip-register');
const apiBase = (
  process.env.EARNFI_BASE_API_BASE ||
  'https://app.earnfi.fun/api/ai-agent/base/v1'
).replace(/\/$/, '');

const require = ensureNpm([{ name: 'ethers', spec: 'ethers@6.13.5' }]);
const { Wallet } = require('ethers');

let wallet;
let hermesStoreRequired = false;
if (process.env.BASE_PRIVATE_KEY) {
  wallet = new Wallet(process.env.BASE_PRIVATE_KEY.trim());
} else {
  wallet = Wallet.createRandom();
  hermesStoreRequired = true;
  emitHermesStore('BASE_PRIVATE_KEY', wallet.privateKey);
}

const out = {
  network: 'base',
  caip2: 'eip155:8453',
  wallet_address: wallet.address,
  agent_name: agentName,
  secret_env: 'BASE_PRIVATE_KEY',
  hermes_store_required: hermesStoreRequired,
  registered: false,
  token_env: 'EARNFI_AGENT_TOKEN',
  token_store_required: false,
};

if (!skipRegister) {
  const chUrl =
    `${apiBase}/register/challenge?wallet_address=${encodeURIComponent(wallet.address)}` +
    `&agent_name=${encodeURIComponent(agentName)}`;
  const chRes = await fetch(chUrl);
  const ch = await chRes.json().catch(() => ({}));
  if (!chRes.ok || !ch.message) {
    out.error = 'challenge_failed';
    out.detail = ch;
    console.log(JSON.stringify(out, null, 2));
    process.exit(1);
  }
  const signature = await wallet.signMessage(ch.message);
  const body = {
    wallet_address: wallet.address,
    agent_name: ch.agent_name || agentName,
    message: ch.message,
    nonce: ch.nonce,
    signature,
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
    out.token_store_required = true;
    emitHermesStore('EARNFI_AGENT_TOKEN', String(data.agent_token));
  }
}

console.log(JSON.stringify(out, null, 2));
if (hermesStoreRequired || out.token_store_required) {
  console.error(
    '# Capture EARNFI_HERMES_STORE lines into Hermes secret scope / profile env. Never paste secrets into chat. Never write keystore files.'
  );
}
