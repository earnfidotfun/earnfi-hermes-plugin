#!/usr/bin/env node
/**
 * EarnFi NEAR implicit account generate.
 * Prefer: /earnfi-wallet near
 */
import {
  canGenerateKeysHere,
  pluginRequire,
  refuseNonTtyGenerate,
  storeNewSecret,
} from './lib-deps.mjs';

const require = pluginRequire();
const { KeyPair } = require('near-api-js');

let kp;
let hermesStoreRequired = false;
if (process.env.NEAR_PRIVATE_KEY) {
  kp = KeyPair.fromString(process.env.NEAR_PRIVATE_KEY.trim());
} else {
  if (!canGenerateKeysHere()) {
    refuseNonTtyGenerate('NEAR_PRIVATE_KEY');
  }
  kp = KeyPair.fromRandom('ed25519');
  hermesStoreRequired = true;
  storeNewSecret('NEAR_PRIVATE_KEY', kp.toString());
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
      secret_saved_via: hermesStoreRequired ? 'console_once' : 'settings',
      note: 'Fund NEAR + Circle USDC before pay. Register via MCP or pay-first bind.',
    },
    null,
    2
  )
);
