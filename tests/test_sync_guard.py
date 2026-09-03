import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from sync_openrouter import _apply_bidir_guard  # noqa: E402


class TestBidirGuard(unittest.TestCase):
    """sync_openrouter's bidirectional surge guard keeps old value on a >5x or <1/5x jump."""

    def test_shrink_keeps_old(self):
        # 0.044 -> 0.003625 is a 1/12x shrink; must be blocked (the deepseek 12x-wrong class)
        out = _apply_bidir_guard({"usd": 0.003625}, {"usd": 0.044}, "m.input")
        self.assertEqual(out, {"usd": 0.044})

    def test_grow_keeps_old(self):
        # 0.044 -> 0.528 is a 12x jump; must be blocked
        out = _apply_bidir_guard({"usd": 0.528}, {"usd": 0.044}, "m.input")
        self.assertEqual(out, {"usd": 0.044})

    def test_normal_applies(self):
        # 0.044 -> 0.05 is a normal ~1.14x change; must apply
        out = _apply_bidir_guard({"usd": 0.05}, {"usd": 0.044}, "m.input")
        self.assertEqual(out, {"usd": 0.05})

    def test_none_old_applies_new(self):
        # no stored value -> apply new (first-seen price)
        out = _apply_bidir_guard({"usd": 0.05}, None, "m.input")
        self.assertEqual(out, {"usd": 0.05})

    def test_not_dict_passthrough(self):
        self.assertEqual(_apply_bidir_guard(None, {"usd": 1}, "m"), None)


if __name__ == "__main__":
    unittest.main()
