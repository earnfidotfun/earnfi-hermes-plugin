"""Security posture checks for manifests and payment skill language."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_BANNED_IN_SKILLS = (
    "do not refuse",
    "EARNFI_HERMES_STORE",
    "hireAndFund",
    "npx earnfi-agent",
)

class SecurityTests(unittest.TestCase):
    def test_mcp_has_no_secrets(self):
        raw = (ROOT / "mcp.json").read_text(encoding="utf-8").lower()
        for needle in ("private", "secret", "api_key", "seed", "0x", "sk-"):
            # allow words in comments? none expected — fail on credential-like keys
            self.assertNotIn(f'"{needle}"', raw)

    def test_trust_untrusted(self):
        data = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(
            data["extensions"]["com.nousresearch.hermes"]["servers"]["earnfi-api"]["trust"],
            "untrusted",
        )

    def test_payments_skill_forbids_false_success(self):
        text = (ROOT / "skills/earnfi-payments/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("signature alone", text.lower())
        self.assertIn("settlement", text.lower())
        self.assertIn("idempotency", text.lower())

    def test_security_doc_disclosure(self):
        text = (ROOT / "docs/SECURITY.md").read_text(encoding="utf-8")
        self.assertIn("app.earnfi.fun", text)
        self.assertIn("x402", text)

    def test_skills_forbid_custody_refusal_and_sdk_spend(self):
        skills_root = ROOT / "skills"
        for skill_md in skills_root.glob("*/SKILL.md"):
            text = skill_md.read_text(encoding="utf-8").lower()
            for needle in _BANNED_IN_SKILLS:
                self.assertNotIn(needle, text, msg=f"{skill_md}: found {needle!r}")

    def test_wallet_skill_routes_natural_language_to_slash(self):
        text = (ROOT / "skills/earnfi-wallet/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("/earnfi-wallet", text)
        self.assertIn("generate a Solana wallet", text)

    def test_readme_no_script_wallet_from_agent(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertNotIn("do not refuse", text)
        self.assertIn("/earnfi-wallet", text)

    def test_emit_hermes_store_removed(self):
        text = (ROOT / "scripts/lib-deps.mjs").read_text(encoding="utf-8")
        self.assertIn("emitHermesStore removed", text)

    def test_no_wallet_cmd_bypass_flag(self):
        for path in (
            ROOT / "scripts/lib-deps.mjs",
            ROOT / "hermes_commands/wallet.py",
        ):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("EARNFI_HERMES_WALLET_CMD", text, msg=str(path))

    def test_tty_only_secret_reveal(self):
        text = (ROOT / "scripts/lib-deps.mjs").read_text(encoding="utf-8")
        self.assertNotIn("process.stderr.write(lines)", text)
        self.assertIn("return false", text.lower())

    def test_sign_tool_uses_minimal_env(self):
        text = (ROOT / "tools/sign_x402.py").read_text(encoding="utf-8")
        self.assertIn("minimal_subprocess_env", text)
        self.assertNotIn("os.environ.copy()", text)

    def test_wallet_uses_minimal_env(self):
        text = (ROOT / "hermes_commands/wallet.py").read_text(encoding="utf-8")
        self.assertIn("minimal_subprocess_env", text)
        self.assertNotIn("os.environ.copy()", text)

    def test_pre_tool_call_hook_registered(self):
        text = (ROOT / "__init__.py").read_text(encoding="utf-8")
        self.assertIn('register_hook("pre_tool_call"', text)
        self.assertIn("pre_tool_call_sign_x402", text)

    def test_sign_schema_requires_quote_json(self):
        text = (ROOT / "__init__.py").read_text(encoding="utf-8")
        self.assertIn("quote_json", text)
        self.assertNotIn("verify_replay", text)

    def test_plugin_yaml_provides_hooks(self):
        text = (ROOT / "plugin.yaml").read_text(encoding="utf-8")
        self.assertIn("pre_tool_call", text)

    def test_wallet_uses_relative_imports(self):
        text = (ROOT / "hermes_commands/wallet.py").read_text(encoding="utf-8")
        self.assertIn("from ..tools.", text)
        self.assertNotIn("from tools.", text)

    def test_plugin_settings_uses_relative_doctor_import(self):
        text = (ROOT / "tools/plugin_settings.py").read_text(encoding="utf-8")
        self.assertIn("from ..doctor.checks", text)
        self.assertNotIn("from doctor.", text)

    def test_npm_install_env_excludes_wallet_keys(self):
        text = (ROOT / "scripts/lib-deps.mjs").read_text(encoding="utf-8")
        self.assertIn("npmInstallEnv", text)
        self.assertIn("--ignore-scripts", text)
        npm_block = text.split("NPM_INSTALL_ENV_KEYS")[1].split("SCRIPT_RUNTIME_ENV_KEYS")[0]
        self.assertNotIn("BASE_PRIVATE_KEY", npm_block)

    def test_hook_accepts_keyword_tool_name(self):
        text = (ROOT / "tools/hooks.py").read_text(encoding="utf-8")
        self.assertIn("tool_name: str", text)
        self.assertNotIn("event: dict", text)

    def test_plugin_provides_sign_tool(self):
        text = (ROOT / "plugin.yaml").read_text(encoding="utf-8")
        in_provides = False
        for line in text.splitlines():
            if line.strip() == "provides_tools:":
                in_provides = True
                continue
            if in_provides:
                if line.startswith("  - earnfi_sign_x402"):
                    return
                if line and not line.startswith("  -"):
                    break
        self.fail("earnfi_sign_x402 not listed under provides_tools in plugin.yaml")


if __name__ == "__main__":
    unittest.main()
