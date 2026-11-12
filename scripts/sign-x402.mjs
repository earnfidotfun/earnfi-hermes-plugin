#!/usr/bin/env node
/**
 * Build x402 PAYMENT-SIGNATURE from a 402 quote (stdin JSON).
 * Reads wallet secrets from Hermes-injected env only; stdout is payment_signature only.
 *
 * Stdin: { "payment_network": "solana:…", "x402Version": 2, "accepts": [...], "resource": {...} }
 * Stdout: { "success": true, "payment_signature": "…", "network": "…" }
 */
import fs from 'node:fs';
import { pluginRequire } from './lib-deps.mjs';

const require = pluginRequire();
const { Connection } = require('@solana/web3.js');
const { clientFromEnv } = require('@earn-fi/agent-client');
const { pickAcceptFromChallenge } = require('@earn-fi/agent-client/dist/accepts.js');
const { buildPaymentSignaturePayload, encodePaymentSignatureHeader } = require(
  '@earn-fi/agent-client/dist/x402.js'
);
const { assertPreflightPayment } = require('@earn-fi/agent-client/dist/preflight.js');
const { Wallet } = require('ethers');

function evmWalletFromEnv(varName) {
  const pk = (process.env[varName] || '').trim();
  if (!pk) return undefined;
  const w = new Wallet(pk);
  return {
    address: w.address,
    signTypedData: (domain, types, value) => w.signTypedData(domain, types, value),
    signMessage: (msg) => w.signMessage(msg),
  };
}

const raw = fs.readFileSync(0, 'utf8');
const input = JSON.parse(raw);
const paymentNetwork = String(
  input.payment_network || input.network || ''
).trim();
const challenge = {
  x402Version: input.x402Version ?? input.x402?.x402Version ?? 2,
  accepts: input.accepts || input.x402?.accepts || input.paymentRequired?.accepts,
  resource: input.resource || input.x402?.resource || input.paymentRequired?.resource,
};

if (!paymentNetwork || !challenge.accepts?.length) {
  console.log(JSON.stringify({ success: false, error: 'invalid_quote_payload' }));
  process.exit(1);
}

let evmWallet;
if (paymentNetwork.startsWith('eip155:8453')) {
  evmWallet = evmWalletFromEnv('BASE_PRIVATE_KEY');
} else if (paymentNetwork.startsWith('eip155:196')) {
  evmWallet = evmWalletFromEnv('OKX_PRIVATE_KEY');
}

const rpc = (process.env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com').trim();
const client = clientFromEnv({
  paymentNetwork,
  connection: new Connection(rpc),
  evmWallet,
});

const accept = pickAcceptFromChallenge(challenge, paymentNetwork);
if (
  !client.skipPaymentPreflight &&
  String(accept.network ?? '').startsWith('solana:') &&
  client.wallet &&
  client.connection
) {
  await assertPreflightPayment({
    wallet: client.wallet,
    connection: client.connection,
    requirements: accept,
  });
}

const paymentBody = await buildPaymentSignaturePayload(accept, challenge, {
  wallet: client.wallet,
  connection: client.connection,
  evmWallet: client.evmWallet ?? evmWallet,
  near: client.near,
});

const payment_signature = encodePaymentSignatureHeader(paymentBody);
console.log(
  JSON.stringify({
    success: true,
    payment_signature,
    network: accept.network,
  })
);
