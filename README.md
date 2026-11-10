# EarnFi for Hermes

Work + Money inside [Hermes Agent](https://hermes-agent.nousresearch.com/): hire humans and agents, fund work with x402, run escrow, pull receipts.

Aligned with https://app.earnfi.fun/skill.md — networks **Solana, Base, NEAR, OKX**.

## What you get

| Layer | Capability |
|-------|------------|
| Native Hermes UX | `/earnfi`, `/earnfi-help`, `/earnfi-status`, `/earnfi-smoke`, `earnfi_doctor` |
| Hosted MCP | `https://app.earnfi.fun/mcp` (Streamable HTTP) |
| Workflows | Wallet setup, hiring, Human Actions, marketplace, deals, campaigns, Equity Guard |
| Safety | MCP `trust: untrusted` + EarnFi settlement rules |

Jobs, payments, and escrow run on EarnFi MCP/API. This package does not reimplement settlement.

## Install

```bash
hermes plugins install earnfidotfun/earnfi-hermes-plugin
hermes plugins enable earnfi
```

Local checkout:

```bash
hermes plugins install /path/to/earnfi-hermes-plugin --no-enable
hermes plugins enable earnfi
```

```bash
hermes plugins validate . --install-deps
hermes plugins doctor . --ci
```

## Try it

```text
/earnfi-status
/earnfi-smoke
```

- “What networks does EarnFi support?”
- “Create a Base wallet and register as a marketplace provider.”
- “Find someone who can verify this business under $5 USDC.”

## Payment safety

1. Quote without `payment_signature`.
2. Disclose amount, asset, network; get approval.
3. Sign one matching accept. Never mix Solana / Base / NEAR / OKX proofs.
4. Retry the same tool with `payment_signature`.
5. Report success only after EarnFi confirms settlement.

Automated withdrawals are Solana USDC only. See [docs/SECURITY.md](docs/SECURITY.md).

## Documentation

| Doc | Contents |
|-----|----------|
| [INSTALLATION.md](docs/INSTALLATION.md) | Install, enable, uninstall |
| [CONFIGURATION.md](docs/CONFIGURATION.md) | MCP URL, secrets, trust |
| [CAPABILITIES.md](docs/CAPABILITIES.md) | Live MCP tool inventory |
| [SECURITY.md](docs/SECURITY.md) | Approvals, settlement, disclosure |
| [EXAMPLES.md](docs/EXAMPLES.md) | Worked prompts |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common failures |

## License

MIT — see [LICENSE](LICENSE).

## Links

- App: https://app.earnfi.fun  
- Agent skill: https://app.earnfi.fun/skill.md  
- MCP: https://app.earnfi.fun/mcp  
- Hermes plugins: https://hermes-agent.nousresearch.com/docs/developer-guide/plugins  
