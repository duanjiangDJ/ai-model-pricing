"""Regression test for the off_peak (time-of-day) derived-price contract.

`pricing.off_peak` is a DERIVED-price contract, not prose: `per_mtok` holds the PEAK
(standard) tier and the off-peak price is `per_mtok x multiplier`, applied outside
`window.peak` (everything outside the peak window is off-peak). The block therefore cannot
contradict the price it derives.

Nothing checked it until 2026-09-14: schema.json types `multiplier` as a bare number and
`days`/`utc` as bare strings, and no audit rule read the block. Verified by injecting
violations into a scratch copy of the repo -- `multiplier: 2.0` (an "off-peak" rate at TWICE
the peak rate), an `off_peak` block whose `per_mtok` carries no non-zero price (nothing to
discount), and a malformed window (days ["monday"], utc ["1-4"]) all passed validate +
audit with zero output, so a writer that stored peak/off-peak INVERTED (2.0 instead of 0.5)
or halved the price a second time (off-peak tier stored in per_mtok while still declaring
0.5) would have published a wrong derived price forever.

Real anchor (official api-docs.deepseek.com/quick_start/pricing/, fetched 2026-09-14):
deepseek-flash peak cache-miss $0.3 / output $1.2, off-peak half, peak window Mon-Fri
01:00-04:00 & 06:00-10:00 UTC -- i.e. multiplier 0.5 with per_mtok at the PEAK tier.
"""
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from toolbox import off_peak_violation  # noqa: E402


def _pricing(multiplier=0.5, days=("mon", "tue", "wed", "thu", "fri"),
             utc=("01:00-04:00", "06:00-10:00"), tz="UTC", base=0.3):
    return {
        "per_mtok": {"input": {"usd": base,
                               "cny": (base * 6.8 if base is not None else None)}},
        "off_peak": {
            "multiplier": multiplier,
            "window": {"peak": {"days": list(days), "utc": list(utc)}, "tz": tz,
                       "note": "All other hours are off-peak."},
        },
    }


def _sev(violations):
    return [s for s, _ in violations]


class TestOffPeakContract(unittest.TestCase):
    def test_absent_block_is_clean(self):
        self.assertEqual(off_peak_violation({"per_mtok": {"input": {"usd": 0.3}}}), [])
        self.assertEqual(off_peak_violation(None), [])
        self.assertEqual(off_peak_violation({"off_peak": None}), [])

    def test_deepseek_shaped_block_is_clean(self):
        self.assertEqual(off_peak_violation(_pricing()), [])

    def test_cny_only_base_counts_as_a_base(self):
        # A CNY-only vendor (per_mtok carries only `cny`) is still a base to discount from.
        self.assertEqual(
            off_peak_violation(_pricing(base=None) | {"per_mtok": {"input": {"cny": 2.0}}}), []
        )

    def test_inverted_multiplier_fails(self):
        # THE bug class: a writer storing peak/off-peak inverted (2.0, not 0.5) would publish
        # an "off-peak" rate at twice the peak rate.
        v = off_peak_violation(_pricing(multiplier=2.0))
        self.assertEqual(_sev(v), ["fail"])

    def test_multiplier_of_one_fails(self):
        # No discount at all -> the declared off-peak window is a no-op that misleads.
        self.assertEqual(_sev(off_peak_violation(_pricing(multiplier=1.0))), ["fail"])

    def test_zero_or_negative_multiplier_fails(self):
        self.assertEqual(_sev(off_peak_violation(_pricing(multiplier=0.0))), ["fail"])
        self.assertEqual(_sev(off_peak_violation(_pricing(multiplier=-0.5))), ["fail"])

    def test_non_numeric_multiplier_fails(self):
        self.assertEqual(_sev(off_peak_violation(_pricing(multiplier="half"))), ["fail"])

    def test_null_multiplier_warns(self):
        v = off_peak_violation(_pricing(multiplier=None))
        self.assertEqual(_sev(v), ["warn"])
        self.assertIn("multiplier", v[0][1])

    def test_no_price_base_fails(self):
        # An off-peak rate is not a standalone price: with no non-zero per_mtok there is
        # nothing to derive it from.
        for pm in ({"input": None, "output": None},
                   {"input": {"usd": None, "cny": None}},
                   {}):
            v = off_peak_violation({"per_mtok": pm, "off_peak": _pricing()["off_peak"]})
            self.assertEqual(_sev(v), ["fail"], pm)

    def test_malformed_window_fails(self):
        v = off_peak_violation(_pricing(days=("monday",), utc=("1-4",)))
        self.assertEqual(_sev(v), ["fail", "fail"])

    def test_missing_tz_warns(self):
        self.assertEqual(_sev(off_peak_violation(_pricing(tz=None))), ["warn"])

    def test_missing_window_warns(self):
        v = off_peak_violation({"per_mtok": {"input": {"usd": 0.3}},
                                "off_peak": {"multiplier": 0.5, "window": None}})
        self.assertEqual(_sev(v), ["warn"])

    def test_missing_peak_inside_window_warns(self):
        v = off_peak_violation({"per_mtok": {"input": {"usd": 0.3}},
                                "off_peak": {"multiplier": 0.5,
                                             "window": {"peak": None, "tz": "UTC"}}})
        self.assertEqual(_sev(v), ["warn"])

    def test_non_object_block_fails(self):
        self.assertEqual(
            _sev(off_peak_violation({"per_mtok": {"input": {"usd": 0.3}}, "off_peak": "half"})),
            ["fail"],
        )

    def test_repo_data_satisfies_the_contract(self):
        # Every model that currently declares off_peak must be derivable (guards the real
        # files, so a bad writer value cannot land unnoticed either).
        import glob
        checked = 0
        for f in glob.glob(os.path.join(ROOT, "data", "feed", "providers", "*.json")):
            prov = json.load(open(f, encoding="utf-8"))
            for m in prov.get("models", []):
                if (m.get("pricing") or {}).get("off_peak"):
                    checked += 1
                    self.assertEqual(
                        off_peak_violation(m["pricing"]), [],
                        f"{prov['provider_id']} :: {m['id']}",
                    )
        self.assertGreater(checked, 0, "no model declares off_peak -- fixture drifted")


if __name__ == "__main__":
    unittest.main()
