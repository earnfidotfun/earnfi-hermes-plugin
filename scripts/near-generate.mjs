#!/usr/bin/env node
/**
 * EarnFi NEAR implicit account generate.
 * Secrets: Hermes profile env / secret scope only (NEAR_PRIVATE_KEY).
 * Never reads or writes keystore files (catalog rule 11).
 *
 * Usage: node near-generate.mjs
 */
import { emitHermesStore, ensureNpm } from './lib-deps.mjs';

const require = ensureNpm([{ name: 'near-api-js', spec: 'near-api-js@5.0.1' }]);
const { KeyPair } = require('near-api-js');

let kp;
let hermesStoreRequired = false;
if (process.env.NEAR_PRIVATE_KEY) {
  kp = KeyPair.fromString(process.env.NEAR_PRIVATE_KEY.trim());
} else {
  kp = KeyPair.fromRandom('ed25519');
  hermesStoreRequired = true;
  emitHermesStore('NEAR_PRIVATE_KEY', kp.toString());
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
      secret_env: 'NEAR_PRIVATE_KEY',
      hermes_store_required: hermesStoreRequired,
      note: 'Fund NEAR + Circle USDC before pay. Named register uses NEP-413. Pay-first also binds agent_token.',
    },
    null,
    2
  )
);
if (hermesStoreRequired) {
  console.error(
    '# Capture EARNFI_HERMES_STORE lines into Hermes secret scope / profile env. Never paste secrets into chat. Never write keystore files.'
  );
}
