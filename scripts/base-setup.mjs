#!/usr/bin/env node
/**
 * EarnFi Base agent setup: generate EVM key + optional register.
 * Prefer: /earnfi-wallet base --name "My Agent"
 */
import { arg, has, pluginRequire, storeNewSecret } from './lib-deps.mjs';

const agentName = arg('--name', process.env.EARNFI_AGENT_NAME || 'earnfi-agent');
const skipRegister = has('--skip-register');
const apiBase = (
  process.env.EARNFI_BASE_API_BASE || 'https://app.earnfi.fun/api/ai-agent/base/v1'
).replace(/\/$/, '');

const require = pluginRequire();
const { Wallet } = require('ethers');

let wallet;
let hermesStoreRequired = false;
if (process.env.BASE_PRIVATE_KEY) {
  wallet = new Wallet(process.env.BASE_PRIVATE_KEY.trim());
} else {
  wallet = Wallet.createRandom();
  hermesStoreRequired = true;
  storeNewSecret('BASE_PRIVATE_KEY', wallet.privateKey);
}

const out = {
  network: 'base',
  caip2: 'eip155:8453',
  wallet_address: wallet.address,
  agent_name: agentName,
  secret_env: 'BASE_PRIVATE_KEY',
  secret_saved_via: hermesStoreRequired ? 'console_once' : 'settings',
  registered: false,
  token_env: 'EARNFI_AGENT_TOKEN',
  token_saved_via: null,
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
    storeNewSecret('EARNFI_AGENT_TOKEN', String(data.agent_token));
    out.token_saved_via = 'console_once';
  }
}

console.log(JSON.stringify(out, null, 2));
