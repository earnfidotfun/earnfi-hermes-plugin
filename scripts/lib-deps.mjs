/**
 * Shared Node helpers for EarnFi Hermes setup/sign scripts.
 *
 * - Dependencies live in the plugin package (package.json + lockfile).
 * - Secrets are revealed once on a real TTY only — never as EARNFI_HERMES_STORE JSON.
 * - Non-TTY (model terminal tools) refuse key generation.
 */
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const PLUGIN_ROOT = path.resolve(__dirname, '..');

export function isInteractiveTty() {
  return Boolean(process.stdin.isTTY && process.stdout.isTTY && process.stderr.isTTY);
}

/** Slash command `/earnfi-wallet` or user-owned shell may show secrets on the real console only. */
export function mayRevealNewSecret() {
  return process.env.EARNFI_HERMES_WALLET_CMD === '1' || isInteractiveTty();
}

/** Resolve require() against the plugin root (npm ci / package-lock). */
export function pluginRequire() {
  ensurePluginDeps();
  return createRequire(path.join(PLUGIN_ROOT, 'package.json'));
}

/**
 * Ensure node_modules matches the lockfile under the plugin root.
 * Uses npm ci (no shell). Falls back to npm install only if lockfile missing.
 */
export function ensurePluginDeps() {
  const pkgJson = path.join(PLUGIN_ROOT, 'package.json');
  const lock = path.join(PLUGIN_ROOT, 'package-lock.json');
  const marker = path.join(PLUGIN_ROOT, 'node_modules', '.package-lock.json');
  if (!fs.existsSync(pkgJson)) {
    throw new Error('Missing plugin package.json — reinstall earnfi-hermes-plugin.');
  }
  const needInstall =
    !fs.existsSync(path.join(PLUGIN_ROOT, 'node_modules')) ||
    (fs.existsSync(lock) && !fs.existsSync(marker));
  if (!needInstall) {
    try {
      createRequire(pkgJson)('@solana/web3.js');
      return;
    } catch {
      // fall through to install
    }
  }
  const npmCmd = process.platform === 'win32' ? 'npm.cmd' : 'npm';
  const args = fs.existsSync(lock)
    ? ['ci', '--omit=dev', '--no-fund', '--no-audit']
    : ['install', '--omit=dev', '--no-fund', '--no-audit'];
  const r = spawnSync(npmCmd, args, {
    cwd: PLUGIN_ROOT,
    stdio: 'inherit',
    shell: false,
    env: process.env,
  });
  if (r.error) throw r.error;
  if (r.status !== 0) process.exit(r.status || 1);
}

/**
 * Write a one-time secret notice to the controlling terminal only.
 * Never print secrets on captured stdout/stderr used by model tools.
 */
export function storeNewSecret(envName, value) {
  if (!mayRevealNewSecret()) {
    refuseNonTtyGenerate(envName);
  }
  if (!revealSecretOnTty(envName, value)) {
    refuseNonTtyGenerate(envName);
  }
}

export function revealSecretOnTty(envName, value) {
  if (!mayRevealNewSecret()) {
    return false;
  }
  const lines = [
    '',
    '════════════════════════════════════════════════════════════',
    `EarnFi secret (shown once) — paste into Hermes:`,
    `  Settings → Plugins → earnfi → ${envName}`,
    '────────────────────────────────────────────────────────────',
    value,
    '════════════════════════════════════════════════════════════',
    'Do not paste this value into chat. Do not share it.',
    '',
  ].join('\n');
  try {
    const ttyPath = process.platform === 'win32' ? '\\\\.\\CON' : '/dev/tty';
    const fd = fs.openSync(ttyPath, 'w');
    try {
      fs.writeSync(fd, lines);
    } finally {
      fs.closeSync(fd);
    }
    return true;
  } catch {
    // Fallback: only when we already know we have a real TTY attached.
    process.stderr.write(lines);
    return true;
  }
}

export function refuseNonTtyGenerate(envName) {
  const out = {
    success: false,
    error: 'tty_required_for_keygen',
    secret_env: envName,
    guidance: [
      `Run /earnfi-wallet with the network flag in the Hermes chat input, or`,
      `run this script yourself in a real terminal (TTY).`,
      `Then paste ${envName} into Settings → Plugins → earnfi.`,
      `Model/terminal tools cannot generate or display private keys.`,
    ],
  };
  console.log(JSON.stringify(out, null, 2));
  process.exit(2);
}

export function arg(name, fallback = '') {
  const i = process.argv.indexOf(name);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

export function has(flag) {
  return process.argv.includes(flag);
}

/** @deprecated Removed — secrets must never be emitted as captureable JSON. */
export function emitHermesStore() {
  throw new Error('emitHermesStore removed: secrets are TTY-only; paste into Settings → Plugins → earnfi');
}
