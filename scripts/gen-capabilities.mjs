import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const inv = JSON.parse(
  fs.readFileSync(path.join(root, "tests/fixtures/tool_inventory.json"), "utf8")
);

const domains = [
  [
    "Discovery & health",
    (t) =>
      /health|catalog|rails|register_info|x402|integrator_rules|find_work|board|search_capabilities|marketplace_stats|leaderboard/.test(
        t
      ) && !t.includes("okx") && !/base_register|near_register/.test(t),
  ],
  [
    "Identity & profile",
    (t) =>
      /register|profile|import_identity|x_verification|sync_said|token_/.test(t) &&
      !t.includes("okx"),
  ],
  [
    "Human Actions (Solana)",
    (t) =>
      (t.includes("human") || t.includes("ask_humans")) && !t.includes("okx"),
  ],
  [
    "Jobs (Solana)",
    (t) =>
      /social_create|manual_create|contest_create|interrupt|hire_listing|get_job|list_submissions|list_completions|pause_job|close_job|update_job|mark_contest|contest_leaderboard|list_verifications|approve_verification|reject_verification|list_agent_jobs|get_agent_usage|get_interrupt|get_job_/.test(
        t
      ) && !t.includes("okx") && !t.includes("human") && !t.includes("ask_humans"),
  ],
  [
    "Marketplace & orders",
    (t) =>
      /marketplace|hire_worker|hire_agent|order_|orders_mine|open_work|providers_|service_|thread_|release_|submit_work|check_work|work_review|get_receipt|get_work_receipt|receipt_get|reviews_mine|dispute/.test(
        t
      ),
  ],
  ["Deals", (t) => t.includes("agent_deal")],
  ["Balance", (t) => /agent_balance|agent_withdraw/.test(t)],
  ["OKX rail", (t) => t.includes("okx")],
  ["Equity Guard", (t) => t.startsWith("equity_")],
];

const used = new Set();
let md = `# EarnFi MCP capability inventory

Source: live server card https://app.earnfi.fun/.well-known/mcp/server-card.json  
Inventoried version: **${inv.version}** — **${inv.count}** tools  
Classification uses MCP \`readOnlyHint\` annotations.

| Class | Count |
|---|---|
| Read-only | ${inv.tools.filter((t) => t.ro).length} |
| Write / payment-capable | ${inv.tools.filter((t) => !t.ro).length} |

`;

for (const [name, fn] of domains) {
  const tools = inv.tools.filter((t) => fn(t.name));
  tools.forEach((t) => used.add(t.name));
  md += `## ${name}\n\n| Tool | Access |\n|---|---|\n`;
  for (const t of tools) {
    md += `| \`${t.name}\` | ${t.ro ? "read-only" : "write/payment"} |\n`;
  }
  md += "\n";
}

const other = inv.tools.filter((t) => !used.has(t.name));
if (other.length) {
  md += `## Other\n\n| Tool | Access |\n|---|---|\n`;
  for (const t of other) {
    md += `| \`${t.name}\` | ${t.ro ? "read-only" : "write/payment"} |\n`;
  }
  md += "\n";
}

md += `## Advertising policy

Only claim a workflow after the corresponding tools appear on the live card and behave as documented. Align Hermes skills with https://app.earnfi.fun/skill.md.

Hermes approval (\`trust: untrusted\`) gates write/payment tools that lack \`readOnlyHint: true\`. EarnFi server-side payment and settlement rules remain authoritative.
`;

fs.writeFileSync(path.join(root, "docs/CAPABILITIES.md"), md);
console.log("wrote docs/CAPABILITIES.md", inv.count, "tools");
