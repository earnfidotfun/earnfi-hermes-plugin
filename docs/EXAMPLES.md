# Examples

## Discovery

```text
Run /earnfi-status and summarise EarnFi connectivity and tool counts.
```

```text
What EarnFi networks are supported? Answer Solana, Base, NEAR, OKX as equals.
```

```text
What version is the EarnFi Hermes plugin, and what is the MCP server card version?
Run /earnfi-status and report both separately.
```

```text
Create your Base EVM wallet. Register yourself on the agent marketplace using
Base (not OKX). Name: Zinox HM. Service: general probe/test, 0.2–0.5 USDC.
```

Expected: `/earnfi-wallet base --name "Zinox HM"` → show address only →
upsert probe service in that price band.

```text
Create a Solana wallet named Media Buddy and register it on EarnFi.
```

Expected: `/earnfi-wallet solana --name "Media Buddy"` → public address + registered; never paste the secret in chat.

```text
Create a NEAR wallet for EarnFi, show me only the account id, then explain how
to fund USDC and register with earnfi_near_register.
```

Expected: `/earnfi-wallet near` → account_id only.

## Hire a human (Job)

```text
Find someone who can verify this business in Port Harcourt, take original photographs,
and submit a short factual report. Budget $5 USDC. Create and fund the Job only after
I approve the payment quote. Then show me the job id and how we will poll for evidence.
```

Expected: collect brief → quote without signature → present amount/network from accepts[] →
wait → settle → confirm funded → explain polling/receipt tools. Not a marketplace agent order.

## Social Task

```text
I want a Task for likes on this X post, small budget. Quote first, wait for my approval.
If accepts[] includes Base as well as Solana, ask which network I will sign on.
```

## Marketplace (buyer)

```text
Show EarnFi marketplace stats and three agents that look suitable for product testing.
Do not hire anyone yet. Use mcp__earnfi_api__ marketplace tools, not agent_catalog.
```

## Register as provider (seller)

```text
I want Hermes listed as a marketplace service provider for coding and code review.
Ask which network (Solana, Base, NEAR, or OKX) and whether I already have that wallet.
tool_search for earnfi_register, earnfi_base_register, earnfi_near_register, earnfi_okx_register.
If some register tools are missing from MCP, say so and offer what is available.
Suggest 3–4 service packages I can pick from. Do not register until I confirm.
```

## Human Action

```text
Create an EarnFi Human Action to review this landing page copy for clarity.
One slot, small reward. Quote first and wait for my approval before paying.
```

## Deals

```text
Explain how EarnFi Deals escrow works, then list my deals if authenticated.
```

## Equity Guard

```text
Run an Equity Guard glossary lookup and explain ALLOW/WARN/BLOCK before any trade tooling.
```
