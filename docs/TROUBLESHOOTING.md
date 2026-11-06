# Troubleshooting

## Plugin does not appear

- Confirm install path contains `plugin.yaml` and `__init__.py`
- Run `HERMES_PLUGINS_DEBUG=1 hermes plugins list`
- Enable the plugin: `hermes plugins enable earnfi`

## MCP tools missing

- Confirm `mcp.json` uses `type: streamable-http` and `https://app.earnfi.fun/mcp`
- Check for server name conflicts in user `config.yaml` `mcp_servers`
- Re-enable the plugin after config changes

## `/earnfi-status` failures

| Symptom | Likely cause |
|---------|----------------|
| MCP endpoint unreachable | Network / DNS / TLS / firewall |
| Server card failed | Temporary outage or blocked `.well-known` |
| Catalog/rails HTTP error | Agent API base path issue |
| Missing smoke tools | Stale or unexpected MCP deployment |

## Payment loops on 402

- Signing the wrong accept / wrong network
- Sending Solana material to OKX tools (or reverse)
- Omitting retry of the **same** tool with `payment_signature`

## Settlement uncertain

Re-query job/order/deal and receipt tools. Do not claim success from a wallet UI alone.
