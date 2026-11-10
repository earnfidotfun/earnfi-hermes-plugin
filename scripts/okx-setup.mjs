#!/usr/bin/env node
/**
 * EarnFi OKX / X Layer agent setup: generate EVM key + optional register.
 * Usage: node okx-setup.mjs --name "My Agent" [--dir PATH] [--skip-register]
 */
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

path.dirname(fileURLToPath(import.meta.url));

function arg(name, fallback = '') {
  const i = process.argv.indexOf(name);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}
function has(flag) {
  return process.argv.includes(flag);
}

const home = process.env.USERPROFILE || process.env.HOME || process.cwd();
const defaultDir =
  process.env.EARNFI_SECRETS_DIR ||
  (process.env.LOCALAPPDATA
    ? path.join(process.env.LOCALAPPDATA, 'hermes', 'secrets', 'earnfi')
    : path.join(home, '.earnfi-agent'));

const outDir = path.resolve(arg('--dir', defaultDir));
const agentName = arg('--name', process.env.EARNFI_AGENT_NAME || 'earnfi-agent');
const skipRegister = has('--skip-register');
const apiBase = (
  process.env.EARNFI_OKX_API_BASE ||
  'https://app.earnfi.fun/api/ai-agent/okx/v1'
).replace(/\/$/, '');

fs.mkdirSync(outDir, { recursive: true });
const pkg = path.join(outDir, 'package.json');
if (!fs.existsSync(pkg)) fs.writeFileSync(pkg, '{"name":"earnfi-agent-secrets","private":true}\n');

function ensureDeps() {
  const req = createRequire(path.join(outDir, 'package.json'));
  try {
    req('ethers');
    return;
  } catch {
    /* install */
  }
  const r = spawnSync('npm', ['install', 'ethers@6.13.5', '--no-fund', '--no-audit'], {
    cwd: outDir,
    stdio: 'inherit',
    shell: true,
  });
  if (r.status !== 0) process.exit(r.status || 1);
}

ensureDeps();
const require = createRequire(path.join(outDir, 'package.json'));
const { Wallet } = require('ethers');

const keyPath = path.join(outDir, 'okx.private.key');
const tokenPath = path.join(outDir, 'agent_token.txt');

let wallet;
if (process.env.OKX_PRIVATE_KEY) {
  wallet = new Wallet(process.env.OKX_PRIVATE_KEY.trim());
} else if (fs.existsSync(keyPath)) {
  wallet = new Wallet(fs.readFileSync(keyPath, 'utf8').trim());
} else {
  wallet = Wallet.createRandom();
  fs.writeFileSync(keyPath, wallet.privateKey, { mode: 0o600 });
}

const out = {
  network: 'okx',
  caip2: 'eip155:196',
  wallet_address: wallet.address,
  agent_name: agentName,
  key_path: keyPath,
  registered: false,
  token_stored: false,
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
  if (data.agent_token) {
    fs.writeFileSync(tokenPath, String(data.agent_token), { mode: 0o600 });
    out.token_stored = true;
    out.token_path = tokenPath;
  }
  out.agent_name = data.agent_name || agentName;
}

console.log(JSON.stringify(out, null, 2));
console.error(`# Secret at ${keyPath} — do not paste into chat`);
