"""Tests for `bin/check-tool.py` — the PreToolUse hook that refuses truncated searches.

    python -m unittest discover tests -v

This hook BLOCKS a tool call before it runs, so the false-positive cases matter more than
the true-positive one. A hook that refuses ordinary commands gets switched off, and then
it protects nothing. Most cases below are therefore about what it must NOT refuse.
"""

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "bin" / "check-tool.py"
_spec = importlib.util.spec_from_file_location("check_tool", SCRIPT)
ctool = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ctool)


class TestDetection(unittest.TestCase):
    """The predicate, tested directly — cheaper than spawning a process per case."""

    def test_grep_piped_to_head_is_truncated(self):
        self.assertTrue(ctool.is_truncated_search("grep -rn foo . | head -8"))

    def test_counting_is_not_truncated(self):
        """`wc -l` is the correct form; interfering with it would be pure noise."""
        self.assertFalse(ctool.is_truncated_search("grep -rn foo . | wc -l"))

    def test_grep_c_is_not_truncated(self):
        self.assertFalse(ctool.is_truncated_search("grep -c foo bar.txt | head -1"))

    def test_grep_count_long_flag_is_not_truncated(self):
        self.assertFalse(ctool.is_truncated_search("grep --count foo . | head -3"))

    def test_head_on_a_file_is_not_truncated(self):
        """Reading the top of a file is ordinary looking, not concluding."""
        self.assertFalse(ctool.is_truncated_search("head -20 README.md"))

    def test_command_without_grep_is_ignored(self):
        self.assertFalse(ctool.is_truncated_search("git log --oneline | head -5"))

    def test_empty_command_is_ignored(self):
        self.assertFalse(ctool.is_truncated_search(""))
        self.assertFalse(ctool.is_truncated_search(None))

    def test_spacing_variants_still_caught(self):
        for command in ("grep foo . |head -2", "grep foo . |  head", "grep foo .|head -1"):
            with self.subTest(command=command):
                self.assertTrue(ctool.is_truncated_search(command))


class TestHookProcess(unittest.TestCase):
    """End to end: exit codes are the contract the harness reads."""

    def _run(self, payload):
        return subprocess.run([sys.executable, str(SCRIPT)],
                              input=json.dumps(payload), capture_output=True,
                              text=True, encoding="utf-8", errors="replace")

    def test_refuses_with_exit_2(self):
        result = self._run({"tool_name": "Bash",
                            "tool_input": {"command": "grep -rn abc . | head -8"}})
        self.assertEqual(result.returncode, 2)
        self.assertIn("agent-pitfalls", result.stderr)
        self.assertIn("wc -l", result.stderr, "the message must name the cheap way out")

    def test_allows_counting(self):
        result = self._run({"tool_name": "Bash",
                            "tool_input": {"command": "grep -rn abc . | wc -l"}})
        self.assertEqual(result.returncode, 0)

    def test_ignores_other_tools(self):
        """A Write whose content happens to mention the pattern must not be refused."""
        result = self._run({"tool_name": "Write",
                            "tool_input": {"file_path": "x.md",
                                           "content": "grep foo | head -3"}})
        self.assertEqual(result.returncode, 0)

    def test_unreadable_payload_does_not_block(self):
        """A broken payload is the harness's problem, not the agent's — never block on it."""
        result = subprocess.run([sys.executable, str(SCRIPT)], input="not json",
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0)

    def test_missing_tool_input_does_not_block(self):
        self.assertEqual(self._run({"tool_name": "Bash"}).returncode, 0)


if __name__ == "__main__":
    unittest.main()
