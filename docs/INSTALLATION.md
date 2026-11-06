# Installation

## Requirements

- Hermes Agent with plugin support (`requires_hermes` in `plugin.yaml`)
- Network access to `https://app.earnfi.fun`

## Install from GitHub

```bash
hermes plugins install earnfidotfun/earnfi-hermes-plugin
hermes plugins enable earnfi
hermes plugins list
```

Portable MCP packages stay disabled until enabled — always run `enable`.

## Install from a local path

```bash
cd earnfi-hermes-plugin
hermes plugins validate . --install-deps
hermes plugins install . --no-enable
hermes plugins enable earnfi
```

## First checks

```text
/earnfi
/earnfi-status
/earnfi-smoke
```

You should see live tool counts from the MCP server card and passing health/catalog/rails checks.

## Uninstall

```bash
hermes plugins disable earnfi
hermes plugins remove earnfi
```

## Catalog install (after listing)

```bash
hermes plugins install earnfi
hermes plugins enable earnfi
```
