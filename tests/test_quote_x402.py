"""Quote parsing for earnfi_sign_x402."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.quote_x402 import (  # noqa: E402
    format_accept_disclosure,
    parse_quote_json,
    pick_accept,
    safe_replay_url,
)


class QuoteTests(unittest.TestCase):
    def test_pick_accept_by_network(self):
        quote = parse_quote_json(
            {
                "x402Version": 2,
                "accepts": [
                    {
                        "network": "eip155:8453",
                        "maxAmountRequired": "500000",
                        "asset": "USDC",
                        "payTo": "0xabc",
                    }
                ],
            }
        )
        accept = pick_accept(quote, "eip155:8453")
        self.assertEqual(accept["payTo"], "0xabc")
        text = format_accept_disclosure(accept, "eip155:8453")
        self.assertIn("0xabc", text)
        self.assertIn("USDC", text)

    def test_rejects_non_https_resource(self):
        quote = parse_quote_json(
            {
                "accepts": [{"network": "eip155:8453"}],
                "resource": {"url": "http://app.earnfi.fun/x"},
            }
        )
        with self.assertRaises(ValueError):
            safe_replay_url(quote)

    def test_build_signer_single_accept(self):
        from tools.quote_x402 import build_challenge_for_signer

        quote = parse_quote_json(
            {
                "x402Version": 2,
                "accepts": [
                    {"network": "eip155:8453", "payTo": "0x1"},
                    {"network": "solana:5eykt4", "payTo": "x"},
                ],
            }
        )
        chosen = pick_accept(quote, "eip155:8453")
        challenge = build_challenge_for_signer(quote, chosen)
        self.assertEqual(len(challenge["accepts"]), 1)
        self.assertEqual(challenge["accepts"][0]["payTo"], "0x1")


if __name__ == "__main__":
    unittest.main()
