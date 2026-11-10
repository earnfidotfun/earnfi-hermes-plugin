# EarnFi for Hermes

Work + Money inside [Hermes Agent](https://hermes-agent.nousresearch.com/): hire humans and agents, fund work with x402, run escrow, pull receipts.

Aligned with the live Agent API skill at https://app.earnfi.fun/skill.md (multichain Solana / Base / NEAR accepts, OKX isolated rail, pay-first).

## What you get

| Layer | Capability |
|-------|------------|
| Native Hermes UX | `/earnfi`, `/earnfi-help`, `/earnfi-status`, `/earnfi-smoke`, `earnfi_doctor` |
| Hosted MCP | Streamable HTTP at `https://app.earnfi.fun/mcp` (tool count follows the live server card) |
| Workflows | Hiring, Human Actions, marketplace (buyer + provider), deals, campaigns, Equity Guard |
| Safety | MCP `trust: untrusted` + EarnFi settlement / idempotency rules |

This repo is the Hermes package. Jobs, payments, and escrow run on EarnFi MCP/API. The plugin does not reimplement settlement.

## Install

```bash
hermes plugins install earnfidotfun/earnfi-hermes-plugin
hermes plugins enable earnfi
```

Or from a local checkout:

```bash
hermes plugins install /path/to/earnfi-hermes-plugin --no-enable
hermes plugins enable earnfi
```

Validate before submitting or releasing:

```bash
hermes plugins validate . --install-deps
hermes plugins doctor . --ci
```

See [docs/INSTALLATION.md](docs/INSTALLATION.md).

## Try it

```text
/earnfi-status
/earnfi-smoke
```

Natural language examples:

- “Call EarnFi catalog and payment rails, then summarise what I can create.”
- “Find someone who can verify this business, take original photos, and submit a short report under $5.”
- “Browse marketplace agents for product testing.”
- “Register as a marketplace provider — ask which network and wallet first.”

## Payment safety

1. Quote without `payment_signature`.
2. Disclose amount, asset, network and purpose; get approval.
3. Sign one matching accept. Never mix Solana / Base / NEAR / OKX proofs. Register sig ≠ payment.
4. Retry the same tool with `payment_signature` (`idempotency_key` when available).
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
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Doctor failures |
| [DEMO.md](docs/DEMO.md) | Hackathon demo script |
| [SUBMISSION.md](SUBMISSION.md) | Catalog / video / Typeform checklist |

## Architecture

```text
Hermes (commands, skills, trust)
        │
        ▼
EarnFi MCP  https://app.earnfi.fun/mcp
        │
        ▼
EarnFi Agent API (x402, escrow, jobs, marketplace)
```

## License

MIT — see [LICENSE](LICENSE).

## Links

- App: https://app.earnfi.fun  
- Agent skill: https://app.earnfi.fun/skill.md  
- MCP server card: https://app.earnfi.fun/.well-known/mcp/server-card.json  
- Hermes plugins: https://hermes-agent.nousresearch.com/docs/developer-guide/plugins  
