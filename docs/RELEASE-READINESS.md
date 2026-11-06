# Release-readiness report (pre-publish)

**Date:** 2026-11-06  
**Package:** EarnFi for Hermes (local)  
**Decision:** **Not release-ready for catalog / hackathon submission yet.**  
**Reason:** Hermes CLI not installed on this machine; approval behaviour, in-Hermes MCP tool exposure, and funded E2E settlement are **unverified**.

Do **not** push the public repo or open the Nous catalog PR until the blockers below are cleared and this report is approved.

---

## 1. What is proven vs not

| Area | Evidence | Status |
|------|----------|--------|
| Independent Hermes package | Local git repo `earnfi-hermes-plugin` | Done |
| Native structure | `plugin.yaml`, `__init__.py`, commands, doctor | Done |
| Remote MCP discovery | Server card 135 tools v1.9.0; catalog/rails HTTP 200 | Remotely verified |
| Cursor branding (repo-wide) | Only anti-Cursor *guards* in tests/scripts; no product copy | Pass |
| Trust config shape | Matches official portable `plugin.json` extensions | Spec-aligned (runtime unproven) |
| Catalog draft | `catalog/earnfi.yaml` (internal) | Draft only |
| Official catalog path | Must be `plugin-catalog/earnfi.yaml` on `NousResearch/hermes-agent` | Understood; not submitted |
| `hermes plugins validate/doctor` | Hermes CLI missing | **Blocker** |
| In-Hermes slash commands + MCP tools | Not run in Hermes | **Blocker** |
| Approval UX (read vs write vs paid) | Not demonstrated in Hermes | **Blocker** |
| Real funded workflow + settlement + receipt | Not run | **Blocker** |
| Public GitHub + catalog PR + demo + Typeform | Intentionally held | Pending approval |

---

## 2. Trust configuration (official schema)

Official Hermes portable packages place Hermes-only fields under:

`plugin.json` → `extensions["com.nousresearch.hermes"].servers.<mcpServerName>`

**Not** as unknown top-level keys inside Agent Plugins `mcp.json` (that schema rejects unknown fields).

Our layout:

- `mcp.json` — `earnfi` server, `type: streamable-http`, URL only  
- `plugin.json` — `servers.earnfi.trust: "untrusted"` (server name matches `mcp.json`)

Expected host behaviour once Hermes loads the package:

| Tool annotation | Under `trust: untrusted` |
|-----------------|---------------------------|
| `readOnlyHint: true` | No approval prompt |
| Write / paid (no readOnlyHint) | Approval required (Once / Session / Always); fail-closed unattended |

**Not yet demonstrated** in a live Hermes session. Backend settlement rules remain authoritative regardless of Hermes approval.

---

## 3. Catalog submission path

| Location | Role |
|----------|------|
| `earnfi-hermes-plugin/catalog/earnfi.yaml` | **Internal draft only** |
| `NousResearch/hermes-agent` → `plugin-catalog/earnfi.yaml` | **Official PR path** |

Pin a full 40-character SHA of the **published** plugin commit after push. Re-run validate against that tree before opening the PR.

---

## 4. Cursor-reference audit

Repository-wide search for `Cursor` / `cursor`:

- Hits only in `tests/test_manifest.py`, `tests/test_commands.py`, `scripts/node-verify.mjs` (guards that **forbid** Cursor branding).
- No Cursor install steps, marketplace copy, or product identity in README, docs, or skills.

---

## 5. MCP tool inventory vs Hermes exposure

- **Remote inventory:** 135 tools on live server card (see `docs/CAPABILITIES.md`, `tests/fixtures/tool_inventory.json`).
- **Hermes exposure:** **Not verified.** Remote HTTP ≠ Hermes MCP session `tools/list`.
- After Hermes install, require: enable plugin → list MCP tools named `earnfi` → spot-check read tools → spot-check one write tool triggers approval.

---

## 6. Skills review (summary)

| Skill | Verdict |
|-------|---------|
| overview, hiring, human-actions, marketplace, deals, work, balance, equity-guard, campaigns, troubleshooting | Structurally sound; tool names match live card |
| payments | Strong settlement rules; multichain Base/NEAR signing is thinner than `@earn-fi/agent-client` — tighten before release |

---

## 7. Multichain + wallet friction (honest assessment)

### MCP + Agent API

- Hosted MCP instructs: **sign off-device; MCP has no keys**.
- Multichain pay-in on `/api/ai-agent/v1`: agent must pick **one** `accepts[]` entry matching the signer (`solana:…`, `eip155:8453`, `near:mainnet`, …).
- OKX remains a **separate** rail (`/api/ai-agent/okx/v1`); never mix proofs.
- Live `/rails` still centres **Solana USDC** as default; discovery endpoints work. Treat Base/NEAR as available only when they appear in the **quote’s** `accepts[]` for that call.

### Cursor plugin / Hermes plugin

Neither plugin is a wallet app. They:

1. Connect MCP and teach workflows.
2. Expect a **402 quote**, then a **`payment_signature`** built outside MCP.
3. Do **not** auto-create Solana / Base / NEAR wallets, fund ATAs, or open Phantom/MetaMask/FastNEAR for the user.

### Where seamless signing *does* exist

`@earn-fi/agent-client` (SDK/CLI) — Solana, Base, and NEAR signers when the integrator supplies or connects a wallet. That path is for **code integrations**, not automatic inside Cursor/Hermes chat unless the host agent already has wallet tooling.

### Practical UX today

| Situation | Friction |
|-----------|----------|
| Read-only discovery (catalog, marketplace, status) | Low — works after plugin enable |
| Paid create with existing funded wallet + agent that can sign | Medium — quote → approve → sign → retry; network must match accept |
| No wallet / wrong chain / empty USDC | **High** — plugins cannot invent a wallet; user must connect/fund outside or use app/SDK |
| “Seamless setup any network wallet inside Hermes/Cursor” | **Not implemented** — would need host wallet UX + signer bridge, not just MCP |

**Bottom line:** Multichain settlement is supported at the **API/MCP/SDK** layer. Cursor and Hermes plugins are **orchestration + safety instructions**, not frictionless wallet onboarding. Claiming seamless wallet setup in the demo would be inaccurate.

---

## 8. Required Hermes test matrix (still open)

```bash
hermes plugins validate . --install-deps
hermes plugins doctor . --ci
hermes plugins install .
hermes plugins enable earnfi
```

Then in a Hermes session:

1. `/earnfi`, `/earnfi-help`, `/earnfi-status`, `/earnfi-smoke`
2. Call `earnfi_doctor` and free reads (`earnfi_agent_catalog`, `earnfi_marketplace_stats`)
3. Confirm ~135 MCP tools visible to the model
4. Trigger a write tool → confirm approval UI
5. Low-value funded job (if wallet available) → EarnFi settlement → job funded → evidence → receipt  
   **Never** treat signature-only or simulated payment as success.

---

## 9. Recommended sequence (unchanged)

1. Install Hermes + pass validate/doctor + live session tests  
2. Real settlement workflow (or explicitly disclose if demo stops at quote)  
3. Push `earnfidotfun/earnfi-hermes-plugin`  
4. PR `plugin-catalog/earnfi.yaml` with pinned SHA  
5. ≤90s X demo tagging `@NousResearch`  
6. Typeform  

Do not expand tool count for its own sake — prove intention → paid work → verified result.
