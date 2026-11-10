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
            Accept: "application/json",
            "User-Agent": "earnfi-hermes-plugin/refresh-inventory",
          },
        },
        (res) => {
          let body = "";
          res.on("data", (c) => (body += c));
          res.on("end", () => resolve({ status: res.statusCode || 0, body }));
        }
      )
      .on("error", reject);
  });
}

const cardRes = await get("https://app.earnfi.fun/.well-known/mcp/server-card.json");
if (cardRes.status !== 200) {
  throw new Error(`server card HTTP ${cardRes.status}`);
}
const card = JSON.parse(cardRes.body);
const tools = (card.tools || []).map((t) => ({
  name: t.name,
  ro: !!(t.annotations && t.annotations.readOnlyHint === true),
}));
const inv = {
  count: tools.length,
  version: (card.serverInfo && card.serverInfo.version) || "unknown",
  source: "https://app.earnfi.fun/.well-known/mcp/server-card.json",
  tools,
};
const out = path.join(root, "tests/fixtures/tool_inventory.json");
fs.writeFileSync(out, JSON.stringify(inv, null, 2) + "\n");
console.log("wrote", out, inv.count, inv.version);
