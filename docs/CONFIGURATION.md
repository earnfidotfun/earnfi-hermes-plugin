# Configuration

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
      "earnfi": { "trust": "untrusted" }
    }
  }
}
```

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
- `agent_api_base` (default Solana Agent API v1)

Diagnostics use the production defaults unless you change settings in Hermes Desktop / config.
