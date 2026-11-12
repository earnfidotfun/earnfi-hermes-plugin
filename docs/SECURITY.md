# Security

## Disclosure (catalog rule 13)

This plugin:

- Connects to EarnFi over the public internet (`app.earnfi.fun`) via hosted MCP and Agent API
- Exposes MCP tools that can create jobs, fund escrow and initiate x402 payments after Hermes approval
- Ships optional Node setup scripts (user-owned terminal only) and `/earnfi-wallet` for register when secrets are already in plugin settings
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

- Configured in **Settings → Plugins → earnfi** (`plugin.yaml` optional `type: secret` fields).
- Setup scripts **never** read or write keystore files, `.env`, `auth.json`, or credential stores on disk.
- New secrets are shown **once** on the user’s real console device (`/dev/tty` / `CON`) when scripts run in a user-owned terminal; they are **never** written to captured stdout/stderr or chat.
- `/earnfi-wallet` does **not** generate keys on gateway or headless hosts; it registers only when the secret is already in plugin settings.
- The model must **not** run `node scripts/*` via the terminal tool to generate keys.
- Child Node processes receive a **minimal env** (wallet secret for that call only via Hermes secret scope — not full `os.environ`).
- Node dependencies install with **`npm ci`** from `package.json` + `package-lock.json` in the plugin root (`node_modules/` is not a secret store).

## Payments

- Settle spend **only** through EarnFi MCP tools under `trust: untrusted` (Hermes approval).
- Native **`earnfi_sign_x402`** builds `payment_signature` from the full MCP `quote_json`, verifies accepts when possible, and requires **`pre_tool_call` Hermes approval** before signing; it returns the signature only, never private keys.
- **Do not** use `@earn-fi/agent-client` / CLI / terminal SDK paths from agent skills.

## Defence in depth

| Layer | Control |
|-------|---------|
| Hermes host | MCP `trust: untrusted` → approve write/payment tools |
| Plugin | `earnfi_sign_x402` for local signing; `/earnfi-wallet` for keygen |
| Skills | Quote → disclose → approve → sign → settle → verify |
| EarnFi backend | Payment gates, settlement checks, idempotency, account limits |

## Payment rules

1. Read-only tools stay read-only (`readOnlyHint: true`).
2. Write tools require Hermes approval under `untrusted`.
3. Before paying, disclose amount, asset, network, destination/purpose.
4. Never describe payment as successful until EarnFi confirms settlement.
5. Use `idempotency_key` when available.
6. Never mix Solana, Base, NEAR, and OKX payment proofs.
7. Never paste private keys, seeds, or raw payment signatures into chat.
8. Automated withdrawals: Solana USDC only unless docs say otherwise.
