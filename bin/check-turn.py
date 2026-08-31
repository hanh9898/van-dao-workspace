#!/usr/bin/env python3
"""check-turn.py — a `Stop` hook: block the turn while measurable work is unfinished.

Why this exists: `docs/agent-pitfalls.md` lists ten classes of mistake that actually
happened in this project. The three worst — stopping at the easy part, quietly swapping
in an easier method, reporting done before verifying — all occur in the gap between
**the task as given** and **the task as the agent silently redefined it**. No reminder
closes that gap; only a declaration written up front, which something else can compare
against.

Three checks, ordered by how hard they bite:

1. `.done-criteria.md` still has a `- [ ]` item  ->  BLOCK (exit 2)
   The up-front declaration. An item dropped on purpose is written `- [~]` with a
   reason and does not count as unfinished.

2. A `.py` file changed and the tests are red  ->  BLOCK (exit 2)
   Same rule as the git pre-commit hook, but it fires earlier: when the agent means to
   stop, well before commit time.

3. The turn used `grep` piped into `head` to conclude "nothing left"  ->  WARN (exit 0)
   Pitfall #2 in the ledger; it has bitten twice. Not a block, because it is easy to
   flag wrongly — `head` while *looking* is fine, only `head` while *concluding* is not.

Infinite-loop protection: after blocking `MAX_BLOCKS` times in a row for the same
reason, stop blocking and say so plainly. A hook that blocks forever gets switched off,
and a hook that is off protects nothing.

Exit codes: 0 carry on (possibly with a warning on stderr) · 2 blocked, the agent must
keep working.
"""

import json
import subprocess
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CRITERIA = ROOT / ".done-criteria.md"
STATE = ROOT / ".git" / "agent-turn-state.json"
MAX_BLOCKS = 2


def read_state():
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def write_state(data):
    try:
        STATE.write_text(json.dumps(data), encoding="utf-8")
    except OSError:
        pass


def block(reason, message):
    """Block the turn — unless the same reason has already blocked it too many times."""
    state = read_state()
    count = state.get(reason, 0) + 1
    if count > MAX_BLOCKS:
        write_state({})
        print(f"[check-turn] blocked {MAX_BLOCKS} times for `{reason}` and it is still "
              f"not done — giving up on blocking.\n{message}\n"
              f"Tell the user plainly that this is unfinished, and why.", file=sys.stderr)
        sys.exit(0)
    write_state({reason: count})
    print(message, file=sys.stderr)
    sys.exit(2)


def git(*args, cwd=ROOT):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def check_criteria():
    """Check 1: the up-front declaration still has unfinished items."""
    if not CRITERIA.is_file():
        return
    lines = CRITERIA.read_text(encoding="utf-8", errors="replace").splitlines()
    pending = [line.strip() for line in lines if line.strip().startswith("- [ ]")]
    if not pending:
        return
    block("criteria-unfinished",
          "[check-turn] `.done-criteria.md` still has unfinished items:\n  "
          + "\n  ".join(pending[:8])
          + "\n\nFinish them, or if one is being dropped on purpose change `- [ ]` to "
            "`- [~]` and give the reason — a documented drop is a decision, a silent "
            "one is forgetting.")


def check_tests():
    """Check 2: a .py file changed and the tests are red."""
    status = git("status", "--porcelain")
    if status.returncode != 0:
        return
    if not [line for line in status.stdout.splitlines() if line.strip().endswith(".py")]:
        return
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "tests", "-q"],
                            cwd=ROOT, capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
    if result.returncode == 0:
        return
    block("tests-red",
          "[check-turn] .py files changed and the tests are RED:\n"
          + (result.stderr or result.stdout)[-1200:]
          + "\n\nGet them green before ending the turn.")


def check_truncated_grep(transcript_path):
    """Check 3: `grep` piped into `head` used to conclude "clean". Warn only."""
    if not transcript_path:
        return
    path = Path(transcript_path)
    if not path.is_file():
        return
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[-400:]
    except OSError:
        return
    suspects = sum(
        1 for line in lines
        if "grep" in line and "| head" in line and "wc -l" not in line and "grep -c" not in line
    )
    if suspects:
        print(f"[check-turn] this turn ran {suspects} command(s) shaped like `grep ... | head`. "
              "If any of them backed a conclusion such as 'clean / nothing left', that "
              "conclusion does not hold — `head` cut off the rest. Count with `grep -c` or "
              "`wc -l` and conclude again. (Pitfall #2 in docs/agent-pitfalls.md; it has "
              "bitten twice.)", file=sys.stderr)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    # A Stop hook can fire again after it blocked; do not stack blocks.
    if payload.get("stop_hook_active"):
        sys.exit(0)

    check_criteria()
    check_tests()
    check_truncated_grep(payload.get("transcript_path"))

    write_state({})   # turn ended clean — clear the counter
    sys.exit(0)


if __name__ == "__main__":
    main()
