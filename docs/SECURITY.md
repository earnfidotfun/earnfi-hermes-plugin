# Security

## Disclosure (catalog rule 13)

This plugin:

- Connects to EarnFi over the public internet (`app.earnfi.fun`)
- Exposes MCP tools that can create jobs, fund escrow and initiate x402 payments after approval
- Does not embed credentials
- Does not ship telemetry
- Does not patch Hermes core

## Defence in depth

| Layer | Control |
|-------|---------|
| Hermes host | MCP `trust: untrusted` → approve write/payment tools |
| Skills | Quote → disclose → approve → settle → verify |
| EarnFi backend | Payment gates, settlement checks, idempotency, account limits |

Hermes approval is **not** a substitute for EarnFi settlement verification.

## Payment rules

1. Read-only tools stay read-only (`readOnlyHint: true`).
2. Write tools require Hermes approval under `untrusted`.
3. Before paying, disclose amount, asset, network, destination/purpose.
4. Never describe payment as successful until EarnFi confirms settlement.
5. Use `idempotency_key` when available; retries must not double-create paid resources.
6. Never mix Solana, Base, NEAR, and OKX payment proofs. Register signatures are not payments.
7. Never log private keys, seed phrases or raw payment signatures in skills output beyond what the user must see to approve.
8. Automated withdrawals: Solana USDC only. Do not imply Base/NEAR withdraw from pay-in accepts.

## Credentials

Secrets only via Hermes (`requires_env` / secret scope / profile env). This package does not read `.env`, `auth.json` or wallet keystores itself.
