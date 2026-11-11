# Changelog

## 1.4.9 — 2026-11-11

- Fix README code fences; keep campaign copy; re-pin catalog sha/image

## 1.4.8 — 2026-11-11

- README and catalog details: Work, Money & Execution Layer positioning; capabilities, innovation, and technical implementation

## 1.4.7 — 2026-11-11

- Catalog banner refresh (2:1 `assets/earnfi-banner.jpg` / `.png`); keep pin `sha` and `image` on the same commit

## 1.4.6 — 2026-11-11

- Catalog rule 11: setup scripts never read/write keystore files; secrets via Hermes secret scope / profile env; optional `config_schema` secrets; banner pin aligned to entry sha

## 1.4.5 — 2026-11-10

- Seamless wallet scripts: pinned Solana web3.js 1.98.4 + tweetnacl register; Base/OKX ethers setup; NEAR generate; payments prefer SDK where local keys exist

## 1.4.4 — 2026-11-10

- Align Base/OKX register with skill.md: `ethers.Wallet.signMessage` only; register ≠ payment; NEAR NEP-413 vs NEP-366 pay

## 1.4.3 — 2026-11-10

- Wallet: creating a dedicated agent key is required and expected for x402/identity — do not refuse as custody

## 1.4.2 — 2026-11-10

- Remove non-product operational wording from skills and docs

## 1.4.1 — 2026-11-10

- Wallet: separate **Base** and **OKX** generators; full **NEAR** implicit-account create path
- Trim non-user docs from the package

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
