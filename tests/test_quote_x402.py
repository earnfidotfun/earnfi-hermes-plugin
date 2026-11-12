"""Quote parsing for earnfi_sign_x402."""

from __future__ import annotations

import unittest

from tools.quote_x402 import format_accept_disclosure, parse_quote_json, pick_accept


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


if __name__ == "__main__":
    unittest.main()
