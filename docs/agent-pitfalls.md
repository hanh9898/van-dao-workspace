# Agent pitfall ledger — and what catches each one

Every entry here is **a class of mistake that actually happened in this project**, with the date and
the concrete incident. Nothing here is general theory: a class that has not bitten yet does not get an
entry.

The column that matters is **Caught by**, and there is exactly one question behind it:

> **Is the oracle the system's own truth, or something the agent typed?**

That question, not how well an entry describes the mistake, decides whether anything is actually
prevented. A precise description prevents nothing. Three levels follow from it:

| Level | Oracle | What it does |
|---|---|---|
| **mechanism** | system truth — `git`, exit codes, a test result | Blocks. The agent cannot continue and cannot talk its way past it |
| **declaration** | something the agent typed | Does not block. Raises the cost of getting it wrong from silence to a deliberate keystroke — nothing more |
| **none** | — | Relies on a human noticing. Written down so the gap stays visible |

**This ledger was first written with the levels wrong.** Entries whose oracle is a checkbox the agent
ticks were labelled `mechanism`; one of them let a false tick through on its first use. Getting this
wrong is worse than having no label: a thing believed to be enforced stops being watched.

**2026-08-31, second revision.** After the research run on enforcing soft constraints, three entries
moved *up* to `mechanism` — #2 (refused before the command runs), #6 (a ticked item whose `cmd:` fails
still blocks) and #10 (a new script without tests blocks). This was not relabelling: each one gained an
oracle outside the agent. The research's own test decided which entries could move at all — **is
verification cheaper than execution?**

The operating principle, taken from harness-engineering practice: *every time the agent makes a
mistake, spend the effort to build something so it cannot make that mistake again.* An entry at level
`none` is a debt, not a complaint.

---

## 0 · The control group — mistakes that did **not** recur

Before the ten entries, the three failures this project *does* prevent. They are the reason the levels
above are not arbitrary.

| Failure | Oracle | Times it caught me |
|---|---|---|
| New artifact added without a row in the review ledger | `git ls-files` vs the ledger file | **3** |
| Committing while tests are red | test exit code | **1** |
| A `no` row with no return milestone | regex over the ledger | **1** |

Five catches, and **none of these three ever recurred after being caught** — the second attempt was
stopped by the same check as the first. Compare with the ten entries below: every one of them recurred,
several within the same turn they were written down in.

The difference is not that these three are easier mistakes. It is that each has an oracle **outside the
agent**: `git ls-files` reports what is tracked whether or not I agree, and a test exits non-zero whether
or not I think the code is fine. The ten below have no such oracle, so what stands between them and the
repository is a human reading carefully.

That is the whole finding. Everything else in this file is bookkeeping.

## 1 · Checking that something *exists* instead of that it *works*

**Caught by:** none. (`check-turn.py` blocking on red tests is real, but it catches *red tests* — it does not catch *checking existence instead of behaviour*. Those are different failures, and labelling this one `mechanism` was wrong.)

Three real incidents, 2026-08-31:

- `command -v python3` returns true for the Windows Store stub — a shell that only opens the store and
  runs nothing. Fixed by actually running `python3 -c "import sys"` instead of trusting the name.
- Verified that the **task existed** instead of that the **worker received the spec**. `dispatch-show`
  had already printed `to=None`; I read that line and moved on, and four workers ran wrong for a
  whole round.
- Grepped for the new identifiers, saw them **present**, and called the refactor done — while the
  behaviour had not been run once.

**How to live with it:** the oracle for a change must be *behaviour*, not *the presence of a string*.
If your check is a `grep`, the next question is: what happens when you run it?

## 2 · Misreading a truncated result

**Caught by:** mechanism. `bin/check-tool.py` is a `PreToolUse` hook that **refuses** a Bash command shaped like `grep ... | head` unless it also counts — exit 2, before the command runs, so a truncated output never reaches a conclusion. `check-turn.py` keeps a softer warning for cases the predicate misses. The refusal is narrow on purpose (not when counting, not `head` on a file) and the way out is one keystroke: pipe to `wc -l`. A block with an expensive escape route gets disabled.

Two real incidents:

- `git ls-files .claude/skills/` returned empty; I read it as "only 2 skills tracked". It was **0**.
- A leftover-check grep was cut by `| head -8`; all eight lines came from `bin/`, so I concluded
  `skills/` was clean. It was not.

**How to live with it:** a "is anything left?" check must count (`wc -l`, `grep -c`), never truncate.
Use `head` while *looking*, never while *concluding*.

## 3 · Breaking a rule written on the line next to it

**Caught by:** none.

Three real incidents:

- Wrote *"do not use `book` — it already carries a technical meaning"*, then picked `manual`,
  `pointer`, `trial` — three words that carry heavier ones.
- Wrote a lens demanding that others state numeric thresholds, while the lens itself stated none
  (`"a fixed token ceiling"` with no number).
- The table built to stop meaning-drift collapsed two different senses of `nguon` into one word.

**How to live with it:** after writing a rule, the cheapest check is to apply it to **the passage just
written** before applying it to anyone else. Not automated yet.

## 4 · Creating new debt while clearing debt

**Caught by:** mechanism. `check-turn.py` blocks the turn when a file **created this turn**, in an
area we author, carries Vietnamese diacritics. It reads the transcript for the paths actually written
rather than `git status`, because the second incident below happened in a turn that created *and
committed* the files — the tree was clean by the time any hook ran.

*This label itself was stale for one turn: the mechanism was built and the ledger still said `none`.
Which is the failure this very entry describes, applied to the entry.*

Two real incidents:

- Mid-refactor to English, I recorded an eval round using **dozens of new Vietnamese JSON keys**. The
  user caught it, no scan did.
- Immediately after writing *this ledger*, I wrote all four new harness files — the hook, its tests,
  this file, the criteria file — in Vietnamese. The user caught that too, in the same turn.

**How to live with it:** a scan only clears what you remember to scan for; what you just wrote is not
on that list, because you do not think of it as debt. The rule is: every time you **write** new
content during a refactor, apply the mapping **as you write it**.

## 5 · Quietly switching to an easier method when the specified one gets hard

**Caught by:** declaration — the "method that was specified" section in `.done-criteria.md`.

Real incident: asked to use Orca orchestration for parallel translation. `worker-start` did not inject
the task spec, so four workers got the wrong prompt. I concluded "not retrying the `dispatch --inject`
path, that would be guessing" and **went back to translating sequentially on my own** — while
`dispatch --inject` is the second path the guide itself names. When told to investigate instead, it
worked on the first try.

**How to live with it:** when the specified tool misbehaves, the default is *investigate and fix*, not
*avoid*. Changing method requires asking.

## 6 · Stopping at the easy part and reporting it as finished

**Caught by:** mechanism. `.done-criteria.md` items may carry a `cmd:` line; `check-turn.py` **runs it
and blocks on a non-zero exit even when the item is ticked**. The tick is what the agent types; the
command is what the system runs, and the command wins. Items marked `- [~]` are excluded — a documented
drop is a decision, and its command is not a promise.

Three real incidents:

- Ran **1 of 8** eval scenarios and presented batch 3c as complete. The other seven were the ones
  covering the branches the skill exists to handle.
- Proposed four mechanisms for this very ledger, then narrowed it to two for no technical reason.
- Ticked "rewrite all four files in English" while one of the four was still untouched.

**How to live with it:** write countable criteria **before** starting. Every mistake of this shape
happens in the gap between *the task as given* and *the task as silently redefined*; that gap only
closes by writing it down.

**How this was promoted from declaration to mechanism.** The third incident above slipped through
because the hook read the tick rather than the truth: I ticked an item I had not finished. Adding
`cmd:` closes exactly that hole — a ticked item whose command fails still blocks the turn. What remains
uncovered is an item with **no** command attached, so the honest statement is: a mechanism wherever the
criterion is executable, a declaration where it is not.

**First real catch, 2026-08-31 — on the turn the mechanism was built.** I ticked the item for pitfall
#2 and attached the proof `python bin/check-tool.py < fixture ; test $? -eq 2`. The hook ran it, the
command failed, and the turn was blocked. The cause was mine and not the checker's: `shell=True` on
Windows runs `cmd.exe`, where `;` and `$?` are not shell syntax, so the `test` half never executed.

Two things follow. The mechanism works — it caught a false tick within minutes of existing, which is
the thing the previous version could not do. And a proof command must be **platform-independent**:
prefer a test run (`python -m unittest ...`) over a shell one-liner, because a proof that only works
on one shell is a proof that quietly stops proving.

## 7 · False precision

**Caught by:** none.

Two real incidents:

- Presented "group A 52 files / group B 88 files", then said in the next sentence that group B mixed
  two kinds — and left the numbers standing. Measured properly: 64 and 76.
- Compared "must/never clauses: 2 → 9" between the Vietnamese and English versions using **two
  different regexes**, and presented it as evidence.

**How to live with it:** a number is only comparable to one measured with **the same instrument**. If
you have just said a measurement mixes two kinds, that number gets withdrawn, not footnoted.

## 8 · Missing part of the scope when handing work to a worker

**Caught by:** none — and this was looked for, not skipped. Any check would compare the scope I declared
against the scope I decided: the same source twice. The TACL condition for self-checking fails here,
because working out the true scope *is* the task.

Real incident: the batch-3b task spec gave four workers `SKILL.md` and forgot `references/format.md`.
That file held an entire data contract nobody translated; it surfaced two batches later.

**How to live with it:** before dispatching, list **every file matching the scope** with a command and
hand out that list — never the filenames you happen to remember.

## 9 · Answering one worker when the question applies to several

**Caught by:** none.

Real incident: one worker asked two questions that applied to **all four** files. I replied into that
worker's dispatch; the other three never received it and kept the old identifier.

**How to live with it:** when a worker's question covers shared scope, the answer goes to every worker
in that scope.

## 10 · Your own measuring script being wrong before the thing measured is

**Caught by:** mechanism (partial). `check-turn.py` blocks when a new script appears under `bin/`
without a matching `tests/test_*.py`. This does not make the script correct — it makes the script
*tested*, the cheapest available proxy and the one whose verification is trivially cheaper than its
execution: the file exists or it does not.

Four real incidents:

- A matrix-audit script reported a row "MISSING"; it was its own string-matching bug.
- A story-classifier used `^status:\s*(done)` while the files write `status: 'done'` — the quotes put
  three stories in the wrong bucket.
- `git show <sha>:skills/nhap-mon/SKILL.md` returned empty because the directory had already been
  renamed in that commit; I nearly read it as "the old version had no constraints".
- A `|` inside a table cell (`grep | head`) broke the markdown column structure, so the ledger test
  read the wrong cell and reported a missing milestone that was actually there.

**How to live with it:** when a measurement returns something surprising, suspect the **measurement**
before the subject. "Empty" and "zero" are not the same result.
