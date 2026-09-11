"""Surge-skip surfacing regression tests (2026-09-11).

`update_model_prices()` refuses to apply a >5x correction (parse-error guard) but used to do
so with nothing but a print -- the rejection was lost the moment the sync log scrolled away.
A skipped correction does NOT self-heal (the same >5x gap re-skips on every later run), so a
stale price could stay published forever: real case, cortecs `qwen3.8-27b` output kept
$2.451 while its declared source (models.dev) reported $0.4 -- a 6.13x gap silently swallowed
on every sync, leaving a row that contradicted its own source.

The writer now records each rejection as a changelog entry (kind="verify",
field="surge_skip:<field>.<currency>", old={"stored": ...}, new={"official": ...}) which
audit.py check #9 turns into a warning while the value is still unresolved. A skip must be
recorded once, not re-appended on every 3h run.

Run: python -m unittest discover -s tests -v
"""
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import toolbox  # noqa: E402


class TestSurgeSkipSurfacing(unittest.TestCase):
    def setUp(self):
        self.saved, self.logs = [], []
        self._save, self._log, self._load = (toolbox.save_provider, toolbox.append_changelog,
                                             toolbox.load_changelog)
        toolbox.save_provider = lambda p: self.saved.append(p)
        toolbox.append_changelog = lambda e: self.logs.append(e)
        toolbox.load_changelog = lambda: {"entries": []}

    def tearDown(self):
        (toolbox.save_provider, toolbox.append_changelog,
         toolbox.load_changelog) = (self._save, self._log, self._load)

    def _prov(self, output=2.451):
        m = {"id": "qwen3.8-27b", "name": "Qwen", "category": "chat", "status": "online",
             "billing_model": ["pay_per_token"],
             "pricing": {"per_mtok": {"input": {"usd": 0.1}, "output": {"usd": output},
                                      "cache_read": {"usd": 0.04}}}}
        return {"provider_id": "cortecs", "verified_at": "2026-01-01T00:00:00Z", "models": [m]}

    def _entries(self):
        return [e for chunk in self.logs for e in chunk]

    def test_skip_recorded_as_changelog_entry(self):
        p = self._prov()
        changed = toolbox.update_model_prices(
            p, {"qwen3.8-27b": {"per_mtok": {"output": 0.4}}}, "2026-09-11T22:00:00Z", "models.dev:api")
        self.assertEqual(p["models"][0]["pricing"]["per_mtok"]["output"]["usd"], 2.451,
                         "a >5x change must be skipped, not written")
        self.assertEqual(changed, [], "a skipped write must not count as a change")
        self.assertEqual(self.saved, [], "a skipped write must not save the provider")
        ents = self._entries()
        self.assertEqual(len(ents), 1, "the skipped correction must still be surfaced")
        e = ents[0]
        self.assertEqual(e["field"], "surge_skip:output.usd")
        self.assertEqual(e["provider_id"], "cortecs")
        self.assertEqual(e["item_id"], "qwen3.8-27b")
        self.assertEqual(e["old"], {"stored": 2.451})
        self.assertEqual(e["new"], {"official": 0.4})
        self.assertEqual(e["source"], "models.dev:api")

    def test_shrink_surge_also_recorded(self):
        """The guard is bidirectional -- an abnormal shrink must be surfaced too."""
        p = self._prov(output=0.4)
        toolbox.update_model_prices(
            p, {"qwen3.8-27b": {"per_mtok": {"output": 0.02}}}, "2026-09-11T22:00:00Z", "models.dev:api")
        self.assertEqual(p["models"][0]["pricing"]["per_mtok"]["output"]["usd"], 0.4)
        ents = self._entries()
        self.assertEqual([e["field"] for e in ents], ["surge_skip:output.usd"])

    def test_identical_pending_skip_not_duplicated(self):
        p = self._prov()
        u = {"qwen3.8-27b": {"per_mtok": {"output": 0.4}}}
        toolbox.update_model_prices(p, u, "2026-09-11T22:00:00Z", "models.dev:api")
        first = self._entries()
        self.assertEqual(len(first), 1)
        # the entry is now pending in the changelog: a repeat run must not append a duplicate
        toolbox.load_changelog = lambda: {"entries": first}
        toolbox.update_model_prices(p, u, "2026-09-12T01:00:00Z", "models.dev:api")
        self.assertEqual(len(self._entries()), 1,
                         "an identical pending skip must not be re-appended every sync")

    def test_normal_change_records_no_surge_entry(self):
        p = self._prov()
        toolbox.update_model_prices(
            p, {"qwen3.8-27b": {"per_mtok": {"output": 2.0}}}, "2026-09-11T22:00:00Z", "models.dev:api")
        ents = self._entries()
        self.assertEqual(len(ents), 1, "one normal update entry, no surge entry")
        self.assertFalse(any(str(e.get("field", "")).startswith("surge_skip:") for e in ents))

    def test_resolved_skip_not_flagged_by_audit_logic(self):
        """A skip whose stored value was corrected no longer matches -> not unresolved."""
        p = self._prov()
        toolbox.update_model_prices(
            p, {"qwen3.8-27b": {"per_mtok": {"output": 0.4}}}, "2026-09-11T22:00:00Z", "models.dev:api")
        entry = self._entries()[0]
        # manual correction applied: stored value now equals what the source wanted
        p["models"][0]["pricing"]["per_mtok"]["output"]["usd"] = 0.4
        cur = p["models"][0]["pricing"]["per_mtok"]["output"]["usd"]
        self.assertNotEqual(cur, entry["old"]["stored"],
                            "resolved skip must drop out of the unresolved set")


if __name__ == "__main__":
    unittest.main()
