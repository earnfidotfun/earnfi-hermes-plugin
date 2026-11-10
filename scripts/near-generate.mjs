#!/usr/bin/env node
/**
 * EarnFi NEAR implicit account generate (ed25519).
 * Named register needs NEP-413 (see skill). Pay-first also binds identity.
 * Usage: node near-generate.mjs [--dir PATH]
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

const home = process.env.USERPROFILE || process.env.HOME || process.cwd();
const defaultDir =
  process.env.EARNFI_SECRETS_DIR ||
  (process.env.LOCALAPPDATA
    ? path.join(process.env.LOCALAPPDATA, 'hermes', 'secrets', 'earnfi')
    : path.join(home, '.earnfi-agent'));

const outDir = path.resolve(arg('--dir', defaultDir));
fs.mkdirSync(outDir, { recursive: true });
const pkg = path.join(outDir, 'package.json');
if (!fs.existsSync(pkg)) fs.writeFileSync(pkg, '{"name":"earnfi-agent-secrets","private":true}\n');

function ensureDeps() {
  const req = createRequire(path.join(outDir, 'package.json'));
  try {
    req('near-api-js');
    return;
  } catch {
    /* install */
  }
  const r = spawnSync('npm', ['install', 'near-api-js@5.0.1', '--no-fund', '--no-audit'], {
    cwd: outDir,
    stdio: 'inherit',
    shell: true,
  });
  if (r.status !== 0) process.exit(r.status || 1);
}

ensureDeps();
const require = createRequire(path.join(outDir, 'package.json'));
const { KeyPair } = require('near-api-js');

const keyPath = path.join(outDir, 'near.private.key');
let kp;
if (process.env.NEAR_PRIVATE_KEY) {
  kp = KeyPair.fromString(process.env.NEAR_PRIVATE_KEY.trim());
} else if (fs.existsSync(keyPath)) {
  kp = KeyPair.fromString(fs.readFileSync(keyPath, 'utf8').trim());
} else {
  kp = KeyPair.fromRandom('ed25519');
  fs.writeFileSync(keyPath, kp.toString(), { mode: 0o600 });
}

const pk = kp.getPublicKey();
const accountId = Buffer.from(pk.data).toString('hex');

console.log(
  JSON.stringify(
    {
      network: 'near',
      caip2: 'near:mainnet',
      account_id: accountId,
      public_key: pk.toString(),
      key_path: keyPath,
      note: 'Fund NEAR + Circle USDC before pay. Named register uses NEP-413 (earnfi-wallet skill). Pay-first also binds agent_token.',
    },
    null,
    2
  )
);
console.error(`# Secret at ${keyPath} — do not paste into chat`);
