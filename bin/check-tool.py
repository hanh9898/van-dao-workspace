#!/usr/bin/env python3
"""check-tool.py — a `PreToolUse` hook: refuse a command whose output would be truncated
before it can support a conclusion.

Pitfall #2 in `docs/agent-pitfalls.md`. It has bitten twice, both times the same way: a
`grep ... | head -N` was run to answer "is anything left?", the output looked empty or
short, and a "clean" conclusion followed. `head` had cut the rest off.

`check-turn.py` already warns about this, but it warns *after* the output has been read —
by then the wrong conclusion is already in the transcript. This hook refuses the command
before it runs, which is the whole point: exit 2 on `PreToolUse` blocks the tool call and
cannot be overridden.

The refusal is deliberately narrow, because a hook that fires wrongly gets switched off:

- Only `Bash` commands.
- Only when `grep` and a pipe into `head` both appear.
- **Not** when the command also counts (`wc -l`, `grep -c`, `grep --count`) — counting is
  the correct form and needs no interference.
- **Not** when `head` is reading a file rather than a pipe (`head file.txt`), which is
  ordinary looking-at-things.

The way out is one keystroke: pipe to `wc -l`, or use `grep -c`. That matters — a block
with an expensive escape route is a block that gets disabled.

Exit codes: 0 allow · 2 refuse (the message on stderr reaches the agent).
"""

import json
import re
import sys

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

COUNTS = ("wc -l", "wc -c", "grep -c", "grep --count", "-c ")


def is_truncated_search(command):
    """True when the command searches and then truncates, without counting."""
    if not command or "grep" not in command:
        return False
    if not re.search(r"\|\s*head\b", command):
        return False
    return not any(marker in command for marker in COUNTS)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)          # unreadable payload is not the agent's fault; do not block

    if payload.get("tool_name") != "Bash":
        sys.exit(0)

    command = (payload.get("tool_input") or {}).get("command", "")
    if not is_truncated_search(command):
        sys.exit(0)

    print(
        "[check-tool] refused: this command searches and then truncates with `head`, so its "
        "output cannot support a conclusion about what is left.\n"
        f"  {command.strip()[:200]}\n\n"
        "Pitfall #2 in docs/agent-pitfalls.md — it has bitten twice, both times by reading a "
        "truncated result as 'clean'.\n"
        "Fix: pipe to `wc -l`, or use `grep -c`, and conclude from the count. If you only want "
        "to LOOK at a few matches rather than conclude anything, say so by counting first.",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
