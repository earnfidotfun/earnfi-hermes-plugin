/**
 * Shared npm deps helper. Installs packages into os.tmpdir() only — never a
 * credential/keystore directory (Hermes catalog rule 11).
 */
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createRequire } from 'node:module';

export function depsDir() {
  return path.join(os.tmpdir(), 'earnfi-hermes-npm');
}

/**
 * @param {Array<{ name: string, spec: string }>} packages
 * @returns {NodeRequire}
 */
export function ensureNpm(packages) {
  const dir = depsDir();
  fs.mkdirSync(dir, { recursive: true });
  const pkgPath = path.join(dir, 'package.json');
  if (!fs.existsSync(pkgPath)) {
    fs.writeFileSync(pkgPath, '{"name":"earnfi-hermes-npm","private":true}\n');
  }
  let req = createRequire(pkgPath);
  const missing = [];
  for (const p of packages) {
    try {
      req(p.name);
    } catch {
      missing.push(p.spec);
    }
  }
  if (missing.length) {
    const r = spawnSync('npm', ['install', ...missing, '--no-fund', '--no-audit'], {
      cwd: dir,
      stdio: 'inherit',
      shell: true,
    });
    if (r.status !== 0) process.exit(r.status || 1);
    req = createRequire(pkgPath);
  }
  return req;
}

/** Emit a secret for the Hermes agent to store via secret scope — never files. */
export function emitHermesStore(name, value) {
  console.error(`EARNFI_HERMES_STORE ${JSON.stringify({ name, value })}`);
}

export function arg(name, fallback = '') {
  const i = process.argv.indexOf(name);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

export function has(flag) {
  return process.argv.includes(flag);
}
