# EarnFi for Hermes

**Work + Money for AI agents.** Hire humans and specialist agents, fund real-world work with x402, manage escrow, and retrieve verifiable receipts — inside [Hermes Agent](https://hermes-agent.nousresearch.com/).

EarnFi turns agents into economic participants: intention → paid work → verified outcomes.

## What you get

| Layer | Capability |
|-------|------------|
| Native Hermes UX | `/earnfi`, `/earnfi-help`, `/earnfi-status`, `/earnfi-smoke`, `earnfi_doctor` |
| Hosted MCP | ~135 tools at `https://app.earnfi.fun/mcp` (Streamable HTTP) |
| Workflows | Hiring, Human Actions, marketplace (buyer + provider), deals, campaigns, Equity Guard |
| Safety | MCP `trust: untrusted` + EarnFi settlement/idempotency rules |

This repository is the **Hermes product**. Execution of jobs, payments and escrow stays on EarnFi’s production MCP/API — the plugin does not reimplement settlement.

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
- “I want to register as a marketplace provider — ask which rail and wallet first.”

## Payment safety

1. Quote without `payment_signature`.
2. Disclose amount, asset, network and purpose; get approval.
3. Sign one matching accept; never mix Solana and OKX proofs.
4. Retry the same tool with `payment_signature` (use `idempotency_key` when available).
5. Report success only after EarnFi confirms settlement — never from a signature or tx hash alone.

Automated withdrawals are **Solana USDC** only. See [docs/SECURITY.md](docs/SECURITY.md).

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
