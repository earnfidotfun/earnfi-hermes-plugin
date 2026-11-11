# Configuration

## Branding (Desktop / catalog)

| Asset | Path | Spec |
|-------|------|------|
| Logo / icon | `assets/logo.png` | Square mark (`plugin.json` → `logo`) |
| Catalog banner | `assets/earnfi-banner.jpg` | **2:1** (1200×600), brand blues `#1585EE` / `#0449B0` / `#1E2D93` |

Desktop / catalog branding uses `assets/logo.png` and `assets/earnfi-banner.jpg`. `plugin.json` sets `title: EarnFi - Work, Money & Execution Layer`.

## MCP

`mcp.json` points Hermes at:

```text
https://app.earnfi.fun/mcp
```

Transport: Streamable HTTP (`type: streamable-http`).

Do **not** put API keys, agent tokens, or wallet secrets in `mcp.json`.

## Trust

`plugin.json` declares Hermes extension:

```json
"extensions": {
  "com.nousresearch.hermes": {
    "servers": {
      "earnfi-api": { "trust": "untrusted" }
    }
  }
}
```

The MCP server key is **`earnfi-api`**, not `earnfi`. The native plugin toolset is already named `earnfi` (`earnfi_doctor`). Reusing `earnfi` for MCP makes Hermes resolve only the doctor tool and never surface `mcp__earnfi-api__*` tools to the model.

Effect: MCP tools without `readOnlyHint: true` require user approval (Once / Session / Always). Unattended runs fail closed.

A same-name entry in the user’s `config.yaml` `mcp_servers` replaces the package server entry (including trust). Prefer keeping `untrusted` for payment-capable servers.

## Optional secrets

Paid flows are pay-first: Agent-Token is optional and may bind from the paying wallet on settle.

If you use a long-lived token, store it through Hermes secret/env routes (for example profile `.env`), never in the plugin tree. Typical names used by EarnFi integrators:

- `EARNFI_AGENT_TOKEN` — optional Agent-Token for creator routes
- Wallet signing stays off-MCP (Hermes/user wallet tooling) — this plugin never logs private keys

## Plugin settings

`plugin.yaml` `config_schema` documents:

- `mcp_url` (default production MCP)
- `agent_api_base` (default Agent API v1)

Diagnostics use the production defaults unless you change settings in Hermes Desktop / config.
