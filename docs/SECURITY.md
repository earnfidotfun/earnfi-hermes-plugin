# Security

## Disclosure (catalog rule 13)

This plugin:

- Connects to EarnFi over the public internet (`app.earnfi.fun`) via hosted MCP and Agent API
- Exposes MCP tools that can create jobs, fund escrow and initiate x402 payments after Hermes approval
- Ships optional Node setup scripts under `scripts/` for dedicated agent key generation and named register (signing happens locally in the agent terminal)
- Does not embed credentials
- Does not ship telemetry
- Does not patch Hermes core
- Does not self-update

## Credentials (catalog rule 11)

Wallet private keys and `agent_token` values are **Hermes-managed secrets** only:

| Secret | Purpose |
|--------|---------|
| `SOLANA_SECRET_KEY_B58` | Solana agent key (base58) |
| `BASE_PRIVATE_KEY` | Base EVM agent key |
| `OKX_PRIVATE_KEY` | OKX / X Layer EVM agent key |
| `NEAR_PRIVATE_KEY` | NEAR implicit account secret |
| `EARNFI_AGENT_TOKEN` | EarnFi agent identity token after register / pay-bind |

- Read through Hermes profile env / secret scope (declared as optional `type: secret` fields in `plugin.yaml` `config_schema`).
- Setup scripts **never** read or write keystore files, `.env`, `auth.json`, or other credential stores.
- When a script generates a new key or receives an `agent_token`, it emits an `EARNFI_HERMES_STORE` line on stderr for the agent to persist via Hermes secrets — not a plugin-owned file.
- npm packages used by scripts install under the OS temp directory (`earnfi-hermes-npm`) for dependencies only.

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
7. Never paste private keys, seeds, or raw payment signatures into chat.
8. Automated withdrawals: Solana USDC only. Do not imply Base/NEAR withdraw from pay-in accepts.
