/**
 * Shared Node helpers for EarnFi Hermes setup/sign scripts.
 *
 * - Dependencies live in the plugin package (package.json + lockfile).
 * - Secrets are revealed once on the real console device only (/dev/tty or \\.\CON).
 * - Non-TTY subprocesses (model terminal, gateway) refuse key generation.
 */
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const PLUGIN_ROOT = path.resolve(__dirname, '..');

const NPM_INSTALL_ENV_KEYS = new Set([
  'PATH',
  'PATHEXT',
  'HOME',
  'USERPROFILE',
  'HOMEDRIVE',
  'HOMEPATH',
  'LANG',
  'LC_ALL',
  'LC_CTYPE',
  'SYSTEMROOT',
  'SystemRoot',
  'WINDIR',
  'TEMP',
  'TMP',
  'TMPDIR',
  'APPDATA',
  'LOCALAPPDATA',
  'ProgramFiles',
  'ProgramFiles(x86)',
  'ComSpec',
  'NODE_OPTIONS',
  'npm_config_cache',
  'npm_config_registry',
  'npm_config_proxy',
  'npm_config_https_proxy',
  'npm_config_userconfig',
  'HTTP_PROXY',
  'HTTPS_PROXY',
  'NO_PROXY',
]);

const SCRIPT_RUNTIME_ENV_KEYS = new Set([
  ...NPM_INSTALL_ENV_KEYS,
  'SOLANA_RPC_URL',
  'EARNFI_AGENT_API_BASE',
  'EARNFI_BASE_API_BASE',
  'EARNFI_OKX_API_BASE',
  'EARNFI_AGENT_NAME',
]);

/** npm ci only — never pass wallet secrets into install scripts. */
export function npmInstallEnv() {
  const out = {};
  for (const key of NPM_INSTALL_ENV_KEYS) {
    if (process.env[key]) out[key] = process.env[key];
  }
  return out;
}

/** Node setup/sign scripts — secrets only via explicit ``extra`` from the plugin parent. */
export function minimalProcessEnv(extra = {}) {
  const out = {};
  for (const key of SCRIPT_RUNTIME_ENV_KEYS) {
    if (process.env[key]) out[key] = process.env[key];
  }
  for (const [k, v] of Object.entries(extra)) {
    if (v !== undefined && v !== null && String(v).trim()) out[k] = String(v);
  }
  delete out.EARNFI_HERMES_WALLET_CMD;
  return out;
}

/** True only when this Node process has a real TTY (user-owned shell). */
export function isInteractiveTty() {
  return Boolean(process.stdin.isTTY && process.stdout.isTTY && process.stderr.isTTY);
}

export function canGenerateKeysHere() {
  return isInteractiveTty();
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
    ? ['ci', '--omit=dev', '--no-fund', '--no-audit', '--ignore-scripts']
    : ['install', '--omit=dev', '--no-fund', '--no-audit', '--ignore-scripts'];
  const r = spawnSync(npmCmd, args, {
    cwd: PLUGIN_ROOT,
    stdio: 'inherit',
    shell: false,
    env: npmInstallEnv(),
  });
  if (r.error) throw r.error;
  if (r.status !== 0) process.exit(r.status || 1);
}

/**
 * Write a one-time secret notice to the controlling console device only.
 */
export function revealSecretOnTty(envName, value) {
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
    return false;
  }
}

export function storeNewSecret(envName, value) {
  if (!canGenerateKeysHere()) {
    refuseNonTtyGenerate(envName);
  }
  if (!revealSecretOnTty(envName, value)) {
    refuseNonTtyGenerate(envName);
  }
}

export function refuseNonTtyGenerate(envName) {
  const out = {
    success: false,
    error: 'tty_required_for_keygen',
    secret_env: envName,
    guidance: [
      'Run this script in your own OS terminal (not via Hermes terminal tool or /earnfi-wallet on gateway).',
      `Then paste ${envName} into Settings → Plugins → earnfi.`,
      'Model/terminal tools cannot generate or display private keys.',
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
