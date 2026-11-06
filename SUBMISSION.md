# Hackathon submission checklist

Track status separately: **implemented** · **tested** · **verified** · **submitted**.

| Deliverable | Status | Evidence |
|-------------|--------|----------|
| Public repo `earnfidotfun/earnfi-hermes-plugin` | implemented (local) | Local git ready; GitHub publish blocked — run `gh auth login` then create/push |
| Native `plugin.yaml` + `__init__.py` | implemented | Root files |
| `mcp.json` streamable-http + trust via `plugin.json` | implemented | Manifests |
| Commands `/earnfi` `/earnfi-help` `/earnfi-status` `/earnfi-smoke` | implemented | `hermes_commands/` |
| Doctor + smoke (live HTTP) | verified | `node scripts/node-verify.mjs` — 135 tools, catalog/rails 200 |
| Hermes workflow skills (11) | implemented | `skills/` |
| CAPABILITIES inventory (135 tools) | verified against live card | `docs/CAPABILITIES.md` |
| Docs + SECURITY disclosure | implemented | `docs/` |
| Automated unit tests | implemented | `tests/` (CPython missing on build host; use `node-verify` + install Python to run unittest) |
| `hermes plugins validate` | pending | Hermes CLI not installed on build machine |
| Real Hermes install + MCP discovery | pending | Requires Hermes runtime |
| Real funded E2E + receipt | pending | Requires wallet + worker |
| Catalog PR `plugin-catalog/earnfi.yaml` | pending | Draft in `catalog/earnfi.yaml`; pin SHA after push |
| X demo &lt;90s + `@NousResearch` | pending | See `docs/DEMO.md` |
| Typeform | pending | https://form.typeform.com/to/FwJLvOln |

**Local commit SHA (pre-push):** `9f91725479e660f76acbdea35a07bef353f73e9b`

## Catalog entry draft

```yaml
name: earnfi
repo: https://github.com/earnfidotfun/earnfi-hermes-plugin
sha: "<40-char-commit-sha>"
description: >-
  Hire humans and agents, fund real-world work via x402, manage escrow,
  and retrieve verifiable receipts.
maintainer: EarnFi
tier: community
category: tools
requires_hermes: ">=0.5.0"
version: "1.0.0"
title: EarnFi
readme: true
capabilities:
  provides_tools:
    - earnfi_doctor
  provides_hooks: []
  provides_middleware: []
  requires_env: []
```

Update `requires_hermes` to match the Hermes version you validated against.

## Official links

- Plugins: https://hermes-agent.nousresearch.com/docs/developer-guide/plugins
- Catalog: https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/catalog-submission
- Hermes repo: https://github.com/NousResearch/hermes-agent
- Form: https://form.typeform.com/to/FwJLvOln
