---
name: earnfi-equity-guard
description: >-
  Equity Guard — search tokenized equities, ALLOW/WARN/BLOCK trade checks,
  portfolio protection, receipts. Do not override EarnFi decisions.
license: MIT
metadata:
  author: earnfi
  version: "1.0.0"
  homepage: https://github.com/earnfidotfun/earnfi-hermes-plugin
---

# Equity Guard

Read / analysis tools include: `equity_get_glossary`, `equity_search`, `equity_get_passport`,
`equity_get_market_state`, `equity_get_peg`, `equity_get_circuit_breaker`, `equity_get_liquidity`,
`equity_get_portfolio`, `equity_list_corporate_actions`, Meteora pool helpers.

Decision / execution path: `equity_preview_trade`, `equity_check_trade`, `equity_simulate_trade`,
`equity_authorize_trade`, `equity_prepare_execution`, `equity_confirm_execution`,
`equity_verify_receipt`, `equity_export_receipt`, `equity_protect_portfolio`.

Respect ALLOW / WARN / BLOCK. Never invent a more permissive outcome than EarnFi returned.
