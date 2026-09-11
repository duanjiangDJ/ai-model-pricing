"""Sync-health refresh for the non-check aggregation sources.

OpenRouter and models.dev are third-party catalogs, not check modules, so the check router
(scripts/router.py) preserves their `sources[]` entries verbatim. daily_check must therefore
refresh their `last_ok`/`last_error` itself -- otherwise the entry keeps a frozen `last_ok`
while `auto_sync: true` claims it is tracked (real bug: models.dev sat at 2026-08-21 for three
weeks with `last_error: null`). This pins that contract, including the empty-parse case (a
models.dev run that persists zero providers must NOT look green).

Run: python -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from daily_check import _refresh_manifest_sources  # noqa: E402

NOW = "2026-09-11T00:00:00Z"
STALE = "2026-08-21T11:27:12Z"


def _manifest():
    return {"sources": [
        {"name": "models.dev", "auto_sync": True, "last_ok": STALE, "last_error": None},
        {"name": "OpenRouter API", "auto_sync": True, "last_ok": STALE, "last_error": None},
    ]}


def _by_name(m, name):
    return [s for s in m["sources"] if s["name"] == name][0]


class TestManifestHealth(unittest.TestCase):
    def test_modelsdev_ok_refreshes(self):
        m = _manifest()
        summary = {"network_ok": True, "router_pc": {"modelsdev": {"status": "ok", "providers": 200}}}
        _refresh_manifest_sources(m, summary, NOW, no_network=False)
        md = _by_name(m, "models.dev")
        self.assertEqual(md["last_ok"], NOW)
        self.assertIsNone(md["last_error"])
        self.assertEqual(_by_name(m, "OpenRouter API")["last_ok"], NOW)

    def test_modelsdev_empty_parse_is_not_green(self):
        m = _manifest()
        summary = {"network_ok": True, "router_pc": {"modelsdev": {"status": "ok", "providers": 0}}}
        _refresh_manifest_sources(m, summary, NOW, no_network=False)
        md = _by_name(m, "models.dev")
        self.assertEqual(md["last_ok"], STALE, "empty parse must not advance last_ok")
        self.assertIsNotNone(md["last_error"])

    def test_modelsdev_error_marks_error(self):
        m = _manifest()
        summary = {"network_ok": True, "router_pc": {"modelsdev": {"status": "error", "providers": 0}}}
        _refresh_manifest_sources(m, summary, NOW, no_network=False)
        md = _by_name(m, "models.dev")
        self.assertEqual(md["last_ok"], STALE)
        self.assertIsNotNone(md["last_error"])

    def test_router_pc_false_marks_error(self):
        m = _manifest()
        summary = {"network_ok": True, "router_pc": False}
        _refresh_manifest_sources(m, summary, NOW, no_network=False)
        self.assertIsNotNone(_by_name(m, "models.dev")["last_error"])

    def test_no_network_leaves_modelsdev_untouched(self):
        m = _manifest()
        _refresh_manifest_sources(m, {"network_ok": True}, NOW, no_network=True)
        md = _by_name(m, "models.dev")
        self.assertEqual(md["last_ok"], STALE)
        self.assertIsNone(md["last_error"])

    def test_openrouter_failure_marks_error(self):
        m = _manifest()
        _refresh_manifest_sources(m, {"network_ok": False}, NOW, no_network=False)
        orr = _by_name(m, "OpenRouter API")
        self.assertEqual(orr["last_ok"], STALE)
        self.assertIsNotNone(orr["last_error"])


if __name__ == "__main__":
    unittest.main()
