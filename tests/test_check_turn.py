"""Tests for `bin/check-turn.py` — the Stop hook that blocks a turn with work left.

    python -m unittest discover tests -v

Why these matter more than they look: this hook BLOCKS. A blocking hook that gets it
wrong either traps the agent in a loop or gets switched off by the user — and a hook
that is off protects nothing. The two most dangerous cases pinned here are
**infinite-loop protection** and **`- [~]` not counting as unfinished**.
"""

import importlib.util
import io
import json
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("check_turn", ROOT / "bin" / "check-turn.py")
ct = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ct)


class Base(unittest.TestCase):
    """Every case runs against a temp directory — never the repo's real files."""

    def setUp(self):
        self._tmp = TemporaryDirectory()
        tmp = Path(self._tmp.name)
        (tmp / ".git").mkdir()
        self._saved = (ct.ROOT, ct.CRITERIA, ct.STATE)
        ct.ROOT = tmp
        ct.CRITERIA = tmp / ".done-criteria.md"
        ct.STATE = tmp / ".git" / "agent-turn-state.json"

    def tearDown(self):
        ct.ROOT, ct.CRITERIA, ct.STATE = self._saved
        self._tmp.cleanup()

    def write_criteria(self, text):
        ct.CRITERIA.write_text(text, encoding="utf-8")

    def run_check(self):
        """Return the exit code; None means the turn was not blocked."""
        try:
            with redirect_stderr(io.StringIO()):
                ct.check_criteria()
        except SystemExit as exc:
            return exc.code
        return None


class TestCriteria(Base):
    def test_no_file_does_not_block(self):
        """Small tasks need no declaration — the hook must stay silent, or it becomes a tax."""
        self.assertIsNone(self.run_check())

    def test_unfinished_item_blocks(self):
        self.write_criteria("- [x] done\n- [ ] not done\n")
        self.assertEqual(self.run_check(), 2)

    def test_all_done_does_not_block(self):
        self.write_criteria("- [x] a\n- [x] b\n")
        self.assertIsNone(self.run_check())

    def test_deliberately_dropped_item_is_not_unfinished(self):
        """`- [~]` is a documented drop. Without this escape the hook blocks forever on
        something already decided against, and the user switches it off."""
        self.write_criteria("- [x] a\n- [~] dropped: needs a remote, see deferred item 17\n")
        self.assertIsNone(self.run_check())

    def test_indented_item_still_counts(self):
        """A nested list item is still an unfinished item."""
        self.write_criteria("- [x] a\n  - [ ] nested and not done\n")
        self.assertEqual(self.run_check(), 2)


class TestInfiniteLoopProtection(Base):
    """The most dangerous case: block forever and the user switches the hook off."""

    def test_gives_up_after_max_blocks(self):
        self.write_criteria("- [ ] something impossible\n")
        codes = [self.run_check() for _ in range(ct.MAX_BLOCKS + 1)]
        self.assertEqual(codes[:ct.MAX_BLOCKS], [2] * ct.MAX_BLOCKS,
                         "must block the full number of times before giving up")
        self.assertEqual(codes[ct.MAX_BLOCKS], 0,
                         "past the threshold, let the turn end — do not trap the agent")

    def test_counter_cleared_after_giving_up(self):
        self.write_criteria("- [ ] x\n")
        for _ in range(ct.MAX_BLOCKS + 1):
            self.run_check()
        self.assertEqual(json.loads(ct.STATE.read_text(encoding="utf-8")), {},
                         "counter must be clean, else the next block starts pre-charged")

    def test_counters_are_per_reason(self):
        """Two different reasons must not add up into each other."""
        ct.STATE.write_text(json.dumps({"tests-red": ct.MAX_BLOCKS}), encoding="utf-8")
        self.write_criteria("- [ ] x\n")
        self.assertEqual(self.run_check(), 2,
                         "the `tests-red` counter must not silence `criteria-unfinished`")


class TestTruncatedGrepWarning(Base):
    """Warns, does NOT block — `head` while looking is fine, only while concluding is not."""

    def _warn(self, content):
        path = Path(self._tmp.name) / "transcript.jsonl"
        path.write_text(content, encoding="utf-8")
        buffer = io.StringIO()
        with redirect_stderr(buffer):
            ct.check_truncated_grep(str(path))
        return buffer.getvalue()

    def test_warns_on_grep_head(self):
        self.assertIn("agent-pitfalls", self._warn('{"c":"grep -rn abc . | head -8"}\n'))

    def test_silent_when_counted(self):
        self.assertEqual(self._warn('{"c":"grep -rc abc . | wc -l"}\n'), "")

    def test_silent_when_grep_c_used(self):
        self.assertEqual(self._warn('{"c":"grep -c abc x | head -1"}\n'), "")

    def test_missing_transcript_is_silent(self):
        self.assertIsNone(ct.check_truncated_grep(str(Path(self._tmp.name) / "nope")))


if __name__ == "__main__":
    unittest.main()
