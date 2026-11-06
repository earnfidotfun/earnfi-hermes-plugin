# Demo script (~80 seconds)

**Story:** Hermes commissions real human work, pays, and retrieves verifiable evidence.

| Time | Beat | On screen |
|------|------|-----------|
| 0–10s | Problem | Agents can reason but cannot independently do every real-world action |
| 10–20s | Connect | `/earnfi-status` — MCP reachable, tool counts, rails |
| 20–40s | Create + fund | NL request to verify a business / take photos; show 402 quote; approve; settle |
| 40–60s | Human execution | Worker submission / evidence in EarnFi (or time-lapse if async) |
| 60–80s | Result | Hermes retrieves evidence + receipt; state settlement confirmed |

## Rules

- Keep under 90 seconds.
- Tag `@NousResearch` on X.
- Prefer a real low-value mainnet payment.
- If any stage is not live, **say so** — never simulate a successful settlement.

## Suggested prompt

```text
Find someone who can verify this business, take original photographs, and submit a short
factual report. Create a job with a small USDC budget. Quote first and wait for my approval
before paying. After funding, show the job id and how we retrieve evidence and a receipt.
```
