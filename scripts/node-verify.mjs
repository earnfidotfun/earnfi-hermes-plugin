/**
 * Lightweight verification when CPython is unavailable on the build host.
 * Mirrors doctor + static manifest checks.
 */
import fs from "fs";
import https from "https";
import path from "path";
import { fileURLToPath } from "url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function get(url) {
  return new Promise((resolve, reject) => {
    https
      .get(
        url,
        {
          headers: {
            "User-Agent": "earnfi-hermes-plugin/1.0.0",
            Accept: "application/json",
          },
        },
        (res) => {
          let body = "";
          res.on("data", (c) => (body += c));
          res.on("end", () =>
            resolve({ status: res.statusCode || 0, body })
          );
        }
      )
      .on("error", reject);
  });
}

function assert(cond, msg) {
  if (!cond) throw new Error(msg);
}

const mcp = JSON.parse(fs.readFileSync(path.join(root, "mcp.json"), "utf8"));
const pj = JSON.parse(fs.readFileSync(path.join(root, "plugin.json"), "utf8"));
assert(mcp.mcpServers["earnfi-api"].type === "streamable-http", "mcp type");
assert(!mcp.mcpServers.earnfi, "mcp server must not collide with plugin toolset earnfi");
assert(
  pj.extensions["com.nousresearch.hermes"].servers["earnfi-api"].trust === "untrusted",
  "trust"
);

const banned = /\bCursor\b/i;
const scan = [];
for (const rel of ["README.md", "SUBMISSION.md", "CHANGELOG.md"]) {
  scan.push(path.join(root, rel));
}
for (const f of fs.readdirSync(path.join(root, "docs"))) {
  // Internal gate doc may mention forbidden host names while auditing them.
  if (f === "RELEASE-READINESS.md") continue;
  scan.push(path.join(root, "docs", f));
}
function walk(d) {
  for (const n of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, n.name);
    if (n.isDirectory()) walk(p);
    else if (n.name === "SKILL.md") scan.push(p);
  }
}
walk(path.join(root, "skills"));
const offenders = scan.filter((p) => banned.test(fs.readFileSync(p, "utf8")));
assert(offenders.length === 0, "Cursor branding: " + offenders.join(", "));

const skills = fs
  .readdirSync(path.join(root, "skills"), { withFileTypes: true })
  .filter((d) => d.isDirectory());
assert(skills.length >= 10, "skills count");

const card = await get("https://app.earnfi.fun/.well-known/mcp/server-card.json");
assert(card.status === 200, "server card HTTP");
const cardJson = JSON.parse(card.body);
assert((cardJson.tools || []).length === 135, "expected 135 tools");

const catalog = await get("https://app.earnfi.fun/api/ai-agent/v1/catalog");
const rails = await get("https://app.earnfi.fun/api/ai-agent/v1/rails");
assert(catalog.status === 200, "catalog");
assert(rails.status === 200, "rails");

const mcpProbe = await get("https://app.earnfi.fun/mcp");
assert(mcpProbe.status > 0, "mcp reachable");

console.log(
  JSON.stringify(
    {
      ok: true,
      tools: cardJson.tools.length,
      version: cardJson.serverInfo?.version,
      catalog: catalog.status,
      rails: rails.status,
      mcp: mcpProbe.status,
      skills: skills.length,
    },
    null,
    2
  )
);
