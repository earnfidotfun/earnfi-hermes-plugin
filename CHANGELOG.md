# Changelog

## 1.4.1 — 2026-11-10

- Wallet: separate **Base** and **OKX** generators; full **NEAR** implicit-account create path
- Strip internal hackathon/admin docs from the published package; agent boundary = public API/MCP only

## 1.4.0 — 2026-11-10

- New **earnfi-wallet** skill: generate dedicated Solana/Base/NEAR/OKX agent keys (terminal), secrets out of chat
- Flatten product copy: Solana, Base, NEAR, OKX are equal networks (no OKX special-casing in UX)
- Provider flow: create Base wallet + register + list services when the user asks (aligned with skill.md)

## 1.3.0 — 2026-11-10

- Product model: **four peer networks** (Solana, Base, NEAR, OKX) — no rails-vs-networks user story
- Doctor + `/earnfi` report Hermes plugin version separately from MCP server card
- Skills ask which wallet/network; stop prioritizing Solana/OKX

## 1.2.2 — 2026-11-10

- Hard-fix rails vs networks answers: `/rails` ≠ Solana/Base/NEAR accepts
- Ban OKX-only marketplace conclusion from `okx_ai_a2mcp` hints
- Provider/overview/troubleshooting templates for “how many rails/networks?”

## 1.2.1 — 2026-11-10

- Refresh capability inventory for live MCP **2.1.0** (141 tools): Base/NEAR register, `payment_network`, integrator rules
- Soften lag copy; verify script asserts multichain tools present

## 1.2.0 — 2026-11-10

- Align with Agent API skill 2.1.3: multichain Solana/Base/NEAR accepts, OKX isolated, pay-first, optional register
- Provider: Solana / Base / NEAR / OKX register families via `tool_search`; `/rails` ≠ full network list
- Payments: `payment_network` when schema has it; trust quote `accepts[]`; register sig ≠ payment
- Doctor advisory when hosted MCP lacks Base/NEAR register tools
- Docs/examples/overview unslopped for Hermes clarity

## 1.1.1 — 2026-11-08

- Provider/payments: build rail menus from live `earnfi_payment_rails` (not a frozen Solana/OKX pair)
- Clarify registration rails vs quote `accepts[]` pay-in networks (Base/NEAR, etc.)

## 1.1.0 — 2026-11-08

- Skills: mandatory Hermes deferred naming (`tool_search` → `mcp__earnfi_api__…`)
- Clear product map: Tasks vs Jobs vs Human Actions vs agent marketplace vs Deals
- New **earnfi-provider** skill — register as marketplace seller; ask rail + wallet first (Solana vs OKX)
- Marketplace skill scoped to buyers; payments/troubleshooting cover wrong-rail 404s
- `/earnfi` help + examples updated for provider onboarding and taxonomy

## 1.0.0 — 2026-11-06

- Initial EarnFi for Hermes release
- Native plugin: `earnfi_doctor`, `/earnfi`, `/earnfi-help`, `/earnfi-status`, `/earnfi-smoke`
- Streamable HTTP MCP to `https://app.earnfi.fun/mcp` with Hermes `trust: untrusted`
- Eleven workflow skills for hiring, payments, marketplace, deals, Equity Guard, and more
- Live MCP capability inventory (135 tools, server card 1.9.0)
- Security, installation, and examples documentation
