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

4. A file CREATED this turn, in an area we author, carries Vietnamese diacritics
   while the project is mid-migration to English  ->  BLOCK (exit 2)
   Pitfall #4, committed twice, caught by the user both times and by no scan. This is
   the first mechanised pitfall and it is deliberately narrow: it reads the transcript
   for the paths actually written, because the failure it targets happened in a turn
   that created *and committed* the files — `git status` would have been clean by the
   time any hook ran.

Infinite-loop protection: after blocking `MAX_BLOCKS` times in a row for the same
reason, stop blocking and say so plainly. A hook that blocks forever gets switched off,
and a hook that is off protects nothing.

Exit codes: 0 carry on (possibly with a warning on stderr) · 2 blocked, the agent must
keep working.
"""

import json
import re
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

# Set once in main() so later checks can reach the transcript without threading it
# through every signature. A dict rather than a bare name so tests can set it directly.
LAST_TRANSCRIPT = {"path": None}

# Areas we author ourselves and have committed to English. `_bmad-output/` is excluded
# on purpose: BMAD generates it under `document_output_language`, so Vietnamese there is
# the configured behaviour, not debt.
AUTHORED_AREAS = ("bin/", "tests/", "docs/", ".claude/skills/", "_bmad/custom/")

VIETNAMESE = re.compile(
    "[à-ãè-êìíò-õùúý"
    "ăđĩũơưạ-ỹ]", re.IGNORECASE)


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


def git(*args, cwd=None):
    # `cwd=ROOT` as a default would bind ROOT at definition time, so the helper would keep
    # pointing at the real repo even after ROOT is reassigned. Resolve it per call instead.
    return subprocess.run(["git", *args], cwd=cwd or ROOT, capture_output=True,
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


def proof_commands():
    """Every `cmd: <shell>` line in the criteria file, paired with the item above it.

    A tick is something I type; a command is something the system runs. Pairing them is
    what moves this check from a declaration to a mechanism — see the research finding
    that self-reported completion is exactly what fails.
    """
    if not CRITERIA.is_file():
        return []
    pairs, item = [], "(unnamed item)"
    for line in CRITERIA.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if stripped.startswith(("- [x]", "- [X]", "- [ ]", "- [~]")):
            item = stripped
        elif stripped.lower().startswith("cmd:"):
            command = stripped[4:].strip().strip("`")
            if command:
                pairs.append((item, command))
    return pairs


def check_proofs():
    """Check 5: every claimed-done item that carries a proof command must actually pass.

    This is the mechanism the ledger's pitfall #6 needed. Ticking `[x]` is no longer
    enough — if an item names a command, the command decides.
    """
    failures = []
    for item, command in proof_commands():
        if item.startswith("- [~]"):
            continue          # deliberately dropped; its command is not a promise
        result = subprocess.run(command, cwd=ROOT, shell=True, capture_output=True,
                                text=True, encoding="utf-8", errors="replace")
        if result.returncode != 0:
            tail = ((result.stderr or result.stdout) or "").strip()[-400:]
            failures.append(f"{item}\n      cmd: {command}\n      -> exit "
                            f"{result.returncode}\n      {tail}")
    if not failures:
        return
    block("proof-failed",
          "[check-turn] item(s) in `.done-criteria.md` name a proof command that FAILS:\n  "
          + "\n  ".join(failures)
          + "\n\nThe tick is not the oracle — the command is. Either make the command pass, "
            "or untick the item and say what is actually left.")


def check_new_scripts_have_tests():
    """Check 6: a new script under bin/ must come with tests.

    Pitfall #10 in the ledger — a measuring script that is itself wrong, three times in
    one session. Verification here is cheap: the test file either exists or it does not.
    """
    missing = []
    for raw_path in files_written_this_turn(LAST_TRANSCRIPT.get("path")):
        try:
            rel = Path(raw_path).resolve().relative_to(ROOT.resolve()).as_posix()
        except (ValueError, OSError):
            continue
        if not rel.startswith("bin/") or not rel.endswith(".py"):
            continue
        if git("ls-files", "--error-unmatch", rel).returncode == 0:
            continue          # already tracked: not a new script
        stem = Path(rel).stem.replace("-", "_")
        expected = ROOT / "tests" / f"test_{stem}.py"
        if not expected.is_file():
            missing.append(f"{rel} -> expected tests/test_{stem}.py")
    if not missing:
        return
    block("new-script-untested",
          "[check-turn] new script(s) under bin/ with no matching test file:\n  "
          + "\n  ".join(missing)
          + "\n\nPitfall #10: a measuring script that is itself wrong, three times in one "
            "session. This is the cheapest class to verify — the test file exists or it "
            "does not.")


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


def files_written_this_turn(transcript_path, tail_bytes=3_000_000):
    """Paths passed to Write/Edit since the last human message.

    Reads the tail of the transcript rather than `git status`, because the failure this
    targets happened in a turn that created *and committed* the files — by the time any
    hook ran, the tree was clean.
    """
    if not transcript_path:
        return []
    path = Path(transcript_path)
    if not path.is_file():
        return []
    try:
        with open(path, "rb") as fh:
            fh.seek(max(0, path.stat().st_size - tail_bytes))
            raw = fh.read().decode("utf-8", errors="replace")
    except OSError:
        return []

    lines = raw.splitlines()[1:]          # first line is probably cut mid-record
    records = []
    for line in lines:
        try:
            records.append(json.loads(line))
        except Exception:
            continue

    # Only this turn: everything after the last real human message.
    start = 0
    for i, rec in enumerate(records):
        msg = rec.get("message") or {}
        if rec.get("type") != "user" or msg.get("role") != "user":
            continue
        content = msg.get("content")
        if isinstance(content, str) or (
            isinstance(content, list)
            and any(b.get("type") == "text" for b in content if isinstance(b, dict))
        ):
            start = i

    written = []
    for rec in records[start:]:
        for block in (rec.get("message") or {}).get("content") or []:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            if block.get("name") not in ("Write", "Edit", "NotebookEdit"):
                continue
            target = (block.get("input") or {}).get("file_path")
            if target:
                written.append(target)
    return written


def check_new_files_are_english(transcript_path):
    """Check 4: a file created this turn, in an area we author, must be English."""
    offenders = []
    seen = set()
    # Resolve BOTH sides: on Windows the repo root can be a short name (HBLAB_~1) while a
    # path from the transcript resolves to the long one, and `relative_to` then misses.
    try:
        root = ROOT.resolve()
    except OSError:
        root = ROOT
    for raw_path in files_written_this_turn(transcript_path):
        try:
            rel = Path(raw_path).resolve().relative_to(root).as_posix()
        except (ValueError, OSError):
            continue
        if rel in seen:
            continue
        seen.add(rel)
        if not rel.startswith(AUTHORED_AREAS):
            continue
        # Pre-existing files are someone else's migration batch, not new debt.
        if git("ls-files", "--error-unmatch", rel).returncode == 0:
            continue
        try:
            text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        hits = sum(1 for line in text.splitlines() if VIETNAMESE.search(line))
        if hits:
            offenders.append((rel, hits))

    if not offenders:
        return
    listing = "\n  ".join(f"{rel} — {n} line(s)" for rel, n in offenders)
    block("new-file-not-english",
          "[check-turn] file(s) created this turn carry Vietnamese diacritics, while the "
          "project is mid-migration to English:\n  " + listing
          + "\n\nThis is pitfall #4 in docs/agent-pitfalls.md — creating new debt while "
            "clearing debt. It has happened twice and a human caught it both times.\n"
            "Rewrite them in English now: a scan afterwards only clears what you remember "
            "to scan for, and what you just wrote is never on that list.")


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    # A Stop hook can fire again after it blocked; do not stack blocks.
    if payload.get("stop_hook_active"):
        sys.exit(0)

    LAST_TRANSCRIPT["path"] = payload.get("transcript_path")

    check_criteria()
    check_proofs()
    check_tests()
    check_new_files_are_english(payload.get("transcript_path"))
    check_new_scripts_have_tests()
    check_truncated_grep(payload.get("transcript_path"))

    write_state({})   # turn ended clean — clear the counter
    sys.exit(0)


if __name__ == "__main__":
    main()
