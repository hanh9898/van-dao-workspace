# Agent pitfall ledger — and what catches each one

Every entry here is **a class of mistake that actually happened in this project**, with the date and
the concrete incident. Nothing here is general theory: a class that has not bitten yet does not get an
entry.

The column that matters is **Caught by**. It has three levels, and the level drives behaviour — not
the prose describing the mistake:

| Level | Meaning |
|---|---|
| **mechanism** | A test or hook blocks it. Violate it and something goes red; you cannot continue |
| **declaration** | Cannot be blocked, but forces a sentence to be written. Lying becomes a deliberate act |
| **none** | Currently relies on a human noticing. Written down so the gap is visible |

The operating principle, taken from harness-engineering practice: *every time the agent makes a
mistake, spend the effort to build something so it cannot make that mistake again.* An entry at level
`none` is a debt, not a complaint.

---

## 1 · Checking that something *exists* instead of that it *works*

**Caught by:** mechanism (partly) — `bin/check-turn.py` blocks the turn when tests are red.

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

**Caught by:** mechanism — `check-turn.py` warns when a turn used `grep` piped into `head` to conclude
"clean".

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

**Caught by:** none.

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

**Caught by:** mechanism — `.done-criteria.md` lists countable criteria and `check-turn.py` blocks
while any `- [ ]` remains.

Three real incidents:

- Ran **1 of 8** eval scenarios and presented batch 3c as complete. The other seven were the ones
  covering the branches the skill exists to handle.
- Proposed four mechanisms for this very ledger, then narrowed it to two for no technical reason.
- Ticked "rewrite all four files in English" while one of the four was still untouched.

**How to live with it:** write countable criteria **before** starting. Every mistake of this shape
happens in the gap between *the task as given* and *the task as silently redefined*; that gap only
closes by writing it down.

**Known limit of the mechanism:** the hook reads the tick, not the truth. The third incident above
slipped through because I ticked an item I had not finished. A declaration raises the cost of lying
from silence to a deliberate keystroke — it does not remove it.

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

**Caught by:** none.

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

**Caught by:** none.

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
