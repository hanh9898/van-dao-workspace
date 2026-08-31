"""Tests for `bin/check-turn.py` — the Stop hook that blocks a turn with work left.

    python -m unittest discover tests -v

Why these matter more than they look: this hook BLOCKS. A blocking hook that gets it
wrong either traps the agent in a loop or gets switched off by the user — and a hook
that is off protects nothing. The most dangerous cases pinned here are
**infinite-loop protection**, **`- [~]` not counting as unfinished**, and the two
false-positive cases in the pitfall-#4 check.
"""

import importlib.util
import io
import json
import subprocess
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


class TestNewFilesMustBeEnglish(Base):
    """Pitfall #4 — the first mechanised one.

    Two cases decide whether this check is usable at all: a pre-existing Vietnamese file
    must not trigger it, and a BMAD-generated artifact must not either. A check that
    fires on those fires on almost every turn, and a check that fires constantly is a
    check that gets switched off.
    """

    def setUp(self):
        super().setUp()
        subprocess.run(["git", "init", "-q"], cwd=ct.ROOT, capture_output=True)

    def _transcript(self, *written_paths):
        """A minimal transcript: one human message, then Write tool_use blocks."""
        records = [{"type": "user", "message": {"role": "user",
                                                "content": [{"type": "text", "text": "go"}]}}]
        for target in written_paths:
            records.append({"type": "assistant", "message": {"role": "assistant", "content": [
                {"type": "tool_use", "name": "Write", "input": {"file_path": target}}]}})
        return self._write_records("transcript.jsonl", records)

    def _write_records(self, name, records):
        path = ct.ROOT / name
        path.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")
        return str(path)

    def _make(self, rel, text, tracked=False):
        target = ct.ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        if tracked:
            subprocess.run(["git", "add", rel], cwd=ct.ROOT, capture_output=True)
            subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                            "commit", "-qm", "x"], cwd=ct.ROOT, capture_output=True)
        return str(target)

    def _run(self, transcript):
        buffer = io.StringIO()
        try:
            with redirect_stderr(buffer):
                ct.check_new_files_are_english(transcript)
        except SystemExit as exc:
            return exc.code, buffer.getvalue()
        return None, buffer.getvalue()

    def test_new_vietnamese_file_blocks(self):
        target = self._make("bin/tool.py", "# bi kip va chi diem\n# bí kíp và chỉ điểm\n")
        code, message = self._run(self._transcript(target))
        self.assertEqual(code, 2)
        self.assertIn("agent-pitfalls", message)

    def test_new_english_file_does_not_block(self):
        target = self._make("bin/tool.py", "# scripture intake, counsel, ordeal\n")
        self.assertIsNone(self._run(self._transcript(target))[0])

    def test_pre_existing_vietnamese_file_does_not_block(self):
        """A tracked file is someone else's migration batch, not new debt. Blocking on it
        would fire on every untranslated file still in the repo."""
        target = self._make("docs/old.md", "# tài liệu cũ chưa chuyển ngữ\n", tracked=True)
        self.assertIsNone(self._run(self._transcript(target))[0])

    def test_bmad_generated_artifact_does_not_block(self):
        """`_bmad-output/` is produced under document_output_language — Vietnamese there
        is configured behaviour, not debt."""
        target = self._make("_bmad-output/story.md", "# câu chuyện người dùng\n")
        self.assertIsNone(self._run(self._transcript(target))[0])

    def test_only_this_turn_counts(self):
        """A Write that happened before the last human message belongs to an earlier turn."""
        target = self._make("bin/old-turn.py", "# bí kíp\n")
        records = [
            {"type": "assistant", "message": {"role": "assistant", "content": [
                {"type": "tool_use", "name": "Write", "input": {"file_path": target}}]}},
            {"type": "user", "message": {"role": "user",
                                         "content": [{"type": "text", "text": "next"}]}},
        ]
        self.assertIsNone(self._run(self._write_records("t2.jsonl", records))[0])

    def test_file_outside_authored_areas_is_ignored(self):
        target = self._make("scratch/notes.md", "# ghi chú tạm\n")
        self.assertIsNone(self._run(self._transcript(target))[0])

    def test_missing_transcript_is_silent(self):
        self.assertIsNone(self._run(str(ct.ROOT / "nope.jsonl"))[0])

    def test_edit_counts_not_only_write(self):
        """Edit creates debt just as well as Write."""
        target = self._make("docs/new.md", "# chỉ điểm mới\n")
        records = [
            {"type": "user", "message": {"role": "user",
                                         "content": [{"type": "text", "text": "go"}]}},
            {"type": "assistant", "message": {"role": "assistant", "content": [
                {"type": "tool_use", "name": "Edit", "input": {"file_path": target}}]}},
        ]
        code, _ = self._run(self._write_records("t3.jsonl", records))
        self.assertEqual(code, 2)


class TestProofCommands(Base):
    """Pitfall #6, promoted from declaration to mechanism.

    The point of this check is that a tick is not evidence. These cases pin the two halves
    of that: a ticked item whose command fails must still block, and a deliberately
    dropped item's command must not be treated as a promise.
    """

    def _run(self):
        buffer = io.StringIO()
        try:
            with redirect_stderr(buffer):
                ct.check_proofs()
        except SystemExit as exc:
            return exc.code, buffer.getvalue()
        return None, buffer.getvalue()

    def test_ticked_item_with_failing_command_still_blocks(self):
        """The case that matters: I ticked it, the command disagrees, the command wins."""
        self.write_criteria("- [x] all done\n      cmd: exit 1\n")
        code, message = self._run()
        self.assertEqual(code, 2)
        self.assertIn("The tick is not the oracle", message)

    def test_passing_command_does_not_block(self):
        self.write_criteria("- [x] all done\n      cmd: exit 0\n")
        self.assertIsNone(self._run()[0])

    def test_dropped_item_command_is_not_a_promise(self):
        """`- [~]` means decided against; its command must not hold the turn hostage."""
        self.write_criteria("- [~] dropped: no cheap oracle exists\n      cmd: exit 1\n")
        self.assertIsNone(self._run()[0])

    def test_no_criteria_file_is_silent(self):
        self.assertIsNone(self._run()[0])

    def test_item_without_command_is_ignored(self):
        self.write_criteria("- [x] plain item, no proof\n")
        self.assertIsNone(self._run()[0])

    def test_backticks_are_stripped_from_the_command(self):
        self.write_criteria("- [x] done\n      cmd: `exit 0`\n")
        self.assertIsNone(self._run()[0])

    def test_command_is_attributed_to_the_item_above_it(self):
        self.write_criteria("- [x] first item\n      cmd: exit 0\n"
                            "- [x] second item\n      cmd: exit 1\n")
        code, message = self._run()
        self.assertEqual(code, 2)
        self.assertIn("second item", message)
        self.assertNotIn("first item", message)


class TestNewScriptsNeedTests(Base):
    """Pitfall #10 — a measuring script that is itself wrong, three times in one session."""

    def setUp(self):
        super().setUp()
        subprocess.run(["git", "init", "-q"], cwd=ct.ROOT, capture_output=True)
        self._saved_transcript = dict(ct.LAST_TRANSCRIPT)

    def tearDown(self):
        ct.LAST_TRANSCRIPT.clear()
        ct.LAST_TRANSCRIPT.update(self._saved_transcript)
        super().tearDown()

    def _turn_wrote(self, *rels):
        records = [{"type": "user", "message": {"role": "user",
                                                "content": [{"type": "text", "text": "go"}]}}]
        for rel in rels:
            target = ct.ROOT / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("# x\n", encoding="utf-8")
            records.append({"type": "assistant", "message": {"role": "assistant", "content": [
                {"type": "tool_use", "name": "Write", "input": {"file_path": str(target)}}]}})
        path = ct.ROOT / "t.jsonl"
        path.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")
        ct.LAST_TRANSCRIPT["path"] = str(path)

    def _run(self):
        buffer = io.StringIO()
        try:
            with redirect_stderr(buffer):
                ct.check_new_scripts_have_tests()
        except SystemExit as exc:
            return exc.code, buffer.getvalue()
        return None, buffer.getvalue()

    def test_new_script_without_test_blocks(self):
        self._turn_wrote("bin/measure.py")
        code, message = self._run()
        self.assertEqual(code, 2)
        self.assertIn("tests/test_measure.py", message)

    def test_new_script_with_test_does_not_block(self):
        self._turn_wrote("bin/measure.py", "tests/test_measure.py")
        self.assertIsNone(self._run()[0])

    def test_hyphenated_script_maps_to_underscored_test(self):
        """`bin/check-thing.py` pairs with `tests/test_check_thing.py`."""
        self._turn_wrote("bin/check-thing.py", "tests/test_check_thing.py")
        self.assertIsNone(self._run()[0])

    def test_non_python_file_in_bin_is_ignored(self):
        self._turn_wrote("bin/notes.md")
        self.assertIsNone(self._run()[0])

    def test_file_outside_bin_is_ignored(self):
        self._turn_wrote("docs/thing.py")
        self.assertIsNone(self._run()[0])


if __name__ == "__main__":
    unittest.main()
