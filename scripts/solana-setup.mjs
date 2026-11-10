#!/usr/bin/env node
/**
 * EarnFi Solana agent setup: generate key (pinned web3.js 1.x) + optional register.
 * Usage:
 *   node solana-setup.mjs --name "My Agent" [--dir PATH] [--skip-register]
 * Env: EARNFI_AGENT_NAME, EARNFI_SECRETS_DIR, SOLANA_SECRET_KEY_B58 (reuse existing)
 * Prints JSON with address only (no secret). Secret written to DIR/solana.key.b58
 */
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

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
const apiBase = (process.env.EARNFI_AGENT_API_BASE || 'https://app.earnfi.fun/api/ai-agent/v1').replace(/\/$/, '');

fs.mkdirSync(outDir, { recursive: true });
const pkg = path.join(outDir, 'package.json');
if (!fs.existsSync(pkg)) fs.writeFileSync(pkg, '{"name":"earnfi-agent-secrets","private":true}\n');

function ensureDeps() {
  const req = createRequire(path.join(outDir, 'package.json'));
  try {
    req('@solana/web3.js');
    req('bs58');
    req('tweetnacl');
    return;
  } catch {
    /* install */
  }
  const r = spawnSync(
    'npm',
    ['install', '@solana/web3.js@1.98.4', 'bs58@5.0.0', 'tweetnacl@1.0.3', '--no-fund', '--no-audit'],
    { cwd: outDir, stdio: 'inherit', shell: true }
  );
  if (r.status !== 0) process.exit(r.status || 1);
}

ensureDeps();
const require = createRequire(path.join(outDir, 'package.json'));
const { Keypair } = require('@solana/web3.js');
const bs58mod = require('bs58');
const bs58 = bs58mod.default || bs58mod;
const nacl = require('tweetnacl');

const keyPath = path.join(outDir, 'solana.key.b58');
const tokenPath = path.join(outDir, 'agent_token.txt');

let kp;
if (process.env.SOLANA_SECRET_KEY_B58) {
  kp = Keypair.fromSecretKey(bs58.decode(process.env.SOLANA_SECRET_KEY_B58.trim()));
} else if (fs.existsSync(keyPath)) {
  kp = Keypair.fromSecretKey(bs58.decode(fs.readFileSync(keyPath, 'utf8').trim()));
} else {
  kp = Keypair.generate();
  fs.writeFileSync(keyPath, bs58.encode(kp.secretKey), { mode: 0o600 });
}

const address = kp.publicKey.toBase58();
const out = {
  network: 'solana',
  wallet_address: address,
  agent_name: agentName,
  key_path: keyPath,
  registered: false,
  token_stored: false,
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
  if (data.agent_token) {
    fs.writeFileSync(tokenPath, String(data.agent_token), { mode: 0o600 });
    out.token_stored = true;
    out.token_path = tokenPath;
  }
  out.agent_name = data.agent_name || agentName;
}

console.log(JSON.stringify(out, null, 2));
console.error(`# Secret at ${keyPath} — do not paste into chat`);
