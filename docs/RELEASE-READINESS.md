# Release-readiness report (pre-publish)

**Date:** 2026-11-06  
**Package:** EarnFi for Hermes (local)  
**Updated:** 2026-11-07 (Hermes Desktop v0.23.0; MCP model-facing call verified)  
**Decision:** **Hermes-validated for native shell + MCP tool loop; not yet hackathon-complete.**  
**Progress:** `validate` / `doctor` pass; plugin enabled; slash commands OK; live chat called `mcp__earnfi_api__earnfi_payment_rails` and returned real rails JSON.  
**Still open:** interactive Once/Session/Always approval UI demo + funded E2E settlement; public GitHub + catalog PR + demo.

Do **not** open the Nous catalog PR until (ideally) a real micro-payment pass and this report is approved for publish.

---

## 1. What is proven vs not

| Area | Evidence | Status |
|------|----------|--------|
| Independent Hermes package | Local git + junction at `%LOCALAPPDATA%\hermes\plugins\earnfi` | Done |
| Native structure | `plugin.yaml`, `__init__.py`, commands, doctor | Done |
| Remote MCP discovery | Server card 135 tools v1.9.0; catalog/rails HTTP 200 | Verified |
| Cursor branding (repo-wide) | Only anti-Cursor *guards* in tests/scripts; no product copy | Pass |
| Trust config shape | `plugin.json` → `trust: untrusted` | Spec-aligned |
| Catalog draft | `catalog/earnfi.yaml` (internal) | Draft only |
| Official catalog path | Must be `plugin-catalog/earnfi.yaml` on `NousResearch/hermes-agent` | Understood; not submitted |
| `hermes plugins validate --install-deps` | Passed on Hermes v0.23.0 | **Pass** |
| `hermes plugins doctor . --ci` | Runtime discovery/import/registration OK | **Pass** |
| Plugin enable | `hermes plugins enable earnfi` — enabled | **Pass** |
| `/earnfi` `/earnfi-help` `/earnfi-status` `/earnfi-smoke` | Live Hermes chat oneshot — all OK, 135 tools in doctor | **Pass** |
| In-Hermes MCP tool calls (model-facing) | Nous oneshot: `tool_search` → `mcp__earnfi_api__earnfi_payment_rails` → live rails JSON (`solana-usdc-x402`, `okx-xlayer-usdt0`) | **Pass** |
| MCP server naming | Must be `earnfi-api` (not `earnfi`) — same-name collision with plugin toolset hid all MCP tools | **Fixed** |
| Approval UX (read vs write vs paid) | Non-interactive oneshot: write tool `earnfi_manual_create` fail-closed under `trust: untrusted` (“user did not approve… NOT run”). Interactive Once/Session/Always UI not filmed yet | **Partial** |
| Real funded workflow + settlement + receipt | Not run | **Open** |
| Public GitHub + catalog PR + demo + Typeform | Intentionally held | Pending approval |

---

## 2. Trust configuration (official schema)

Official Hermes portable packages place Hermes-only fields under:

`plugin.json` → `extensions["com.nousresearch.hermes"].servers.<mcpServerName>`

**Not** as unknown top-level keys inside Agent Plugins `mcp.json` (that schema rejects unknown fields).

Our layout:

- `mcp.json` — `earnfi-api` server (not `earnfi` — avoids plugin toolset shadow), `type: streamable-http`, URL only  
- `plugin.json` — `servers.earnfi-api.trust: "untrusted"` (server name matches `mcp.json`)

Expected host behaviour once Hermes loads the package:

| Tool annotation | Under `trust: untrusted` |
|-----------------|---------------------------|
| `readOnlyHint: true` | No approval prompt (verified: `earnfi_payment_rails`) |
| Write / paid (no readOnlyHint) | Approval required; fail-closed unattended (verified: `earnfi_manual_create` denied in oneshot) |

Backend settlement rules remain authoritative regardless of Hermes approval. Interactive approval UI still worth capturing in the demo.

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

- **Remote inventory:** 135 tools on live server card (see `docs/CAPABILITIES.md`, `tests/fixtures/tool_inventory.json`); `hermes mcp test earnfi-api` discovers **137** (card + utility wrappers).
- **Hermes exposure:** **Verified** after renaming MCP server to `earnfi-api`. With the old name `earnfi`, tool_search deferred only ~7 tools (doctor path); after rename, deferred catalog jumped to **144** and the model invoked `mcp__earnfi_api__earnfi_payment_rails`.
- **Local host tips:** `mcp_single_query_discovery_timeout: 90`, `mcp_servers.earnfi-api.lazy: true`, `connect_timeout: 90` (cold connect can exceed the default 15s oneshot wait).
- Write gate: non-interactive call to `mcp__earnfi_api__earnfi_manual_create` was denied by the MCP trust gate (fail-closed). Interactive approval UI still open for the demo reel.

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

## 8. Hermes test matrix

### Completed (2026-11-07, Hermes Agent v0.23.0)

```text
hermes plugins validate . --install-deps   → Validation passed
hermes plugins doctor . --ci               → OK (1 tool registered)
# Local path: junction %LOCALAPPDATA%\hermes\plugins\earnfi → repo
hermes plugins enable earnfi               → enabled
hermes chat -q "/earnfi-status" --oneshot -Q  → Overall OK, 135 tools
hermes chat -q "/earnfi-smoke" --oneshot -Q   → Overall OK
hermes chat -q "/earnfi-help" --oneshot -Q    → help rendered
hermes chat -q "/earnfi" --oneshot -Q         → overview rendered
```

Note: `hermes plugins install .` rejects bare `.` — use a Git URL/`owner/repo` for catalog installs, or a local directory under Hermes `plugins/` (junction used for this audit).

### Still open

1. Call MCP tools from a Hermes agent turn (`earnfi_agent_catalog`, etc.) — confirm model-facing MCP names
2. Trigger a write/paid tool → confirm Hermes approval UI under `trust: untrusted`
3. Low-value funded job (if wallet available) → EarnFi settlement → evidence → receipt  
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
