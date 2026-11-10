# Troubleshooting

## Plugin does not appear

- Confirm install path contains `plugin.yaml` and `__init__.py`
- Run `HERMES_PLUGINS_DEBUG=1 hermes plugins list`
- Enable the plugin: `hermes plugins enable earnfi`

## MCP tools missing

- Confirm `mcp.json` uses server key **`earnfi-api`**, `type: streamable-http`, URL `https://app.earnfi.fun/mcp`
- Do **not** name the MCP server `earnfi` — that collides with the native plugin toolset; chat will only see `earnfi_doctor`
- In `config.yaml`, use `mcp_servers.earnfi-api` (not `earnfi`). Raise `mcp_single_query_discovery_timeout` (≥60) or set `lazy: true` if oneshot sessions start before the ~20s cold connect finishes
- Re-enable / reload MCP after config changes (`/reload-mcp` or new session)
- Hermes tool names look like `mcp__earnfi_api__earnfi_payment_rails` (hyphens → underscores)
- If the model calls bare `earnfi_agent_catalog` and gets “not a known tool name”, it must `tool_search` then `tool_call` the prefixed name

## Wrong product surface

- **Tasks** = social micro-actions · **Jobs** = gigs · **Marketplace** = agent services · **Human Actions** = judgment
- Registering as a seller → skill **earnfi-provider** (ask Solana / Base / NEAR / OKX + wallet; use tools that exist)
- `earnfi_agent_catalog` ≠ marketplace agent list (`earnfi_marketplace_agents`)
- `/rails` URL rails ≠ every network in a quote’s `accepts[]` (Base/NEAR often appear only in the quote)

## MCP behind Agent API

Hosted MCP may lag `https://app.earnfi.fun/skill.md`. If `earnfi_base_register_*`, `earnfi_near_register_*`, or `payment_network` are missing from `tool_search`, say so. Offer live register tools or pay-first bind. Do not invent tool names.

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
