---
name: work-state
description: Use when you need to know where the work currently stands across both BMAD and Orca before deciding what to do next — asked as "where am I", "what should I do next", "what's in progress", "are the two states in sync", or when a dispatched Orca worker starts and has no inherited context. Also use before dispatching workers, to see what is already running. Reports facts and flags divergence; it does not change any state.
---

# Work State — one place to ask where things stand

## Done when

The caller has, in one answer: **which story is in progress**, **what Orca is running**, **every divergence found**, and **every comparison that could not be made**. The last one is not optional — a comparison that could not run is different from a comparison that ran and found nothing, and collapsing them misleads.

If the script exits nonzero, done means: said plainly that no source could be read, showed the path it searched, and stopped. Not guessing.

## When this skill does not help

- **Deciding what to build.** This reports position, not direction. For "what should the next story be", that is a planning conversation, not a status lookup.
- **Changing anything.** Read-only by design. To fix a divergence, go edit the source that is wrong — this skill only tells you the two disagree.
- **Orca coordination itself.** To dispatch workers, wait on `worker_done`, or manage a DAG, load the `orchestration` guide (`orca skills get orchestration`). This skill only reports what is already running.
- **BMAD routing inside a single skill.** For "which BMAD skill comes next in the standard flow", `bmad-help` knows the catalog and this one does not.
- **Repos without `_bmad-output/`.** The script exits 1 and says so. Do not improvise a substitute answer.

## No customization

This skill exposes no `customize.toml` fields. Paths are derived from the repo root, and thresholds live in the script. Nothing to override; do not invent settings.

## Read → compare → report

### Step 1 — Run the script

```
python bin/work-state.py --brief
```

If you do not know where the repo root is — a dispatched worker often does not — find the script rather than guessing: `git rev-parse --show-toplevel` from anywhere inside the checkout, or search for `bin/work-state.py` upward from the current directory. The script derives the repo root from its own location, so once you can name the file you are done; you do not need to be in any particular directory to run it.

Use `--brief` for a normal answer. Drop it for the full JSON when the caller asks for detail, or when you need the raw `orca.task` / `orca.worktree` arrays to plan a dispatch.

The script reads four sources — `sprint-status.yaml`, every story's frontmatter, `orca orchestration task-list`, `orca worktree ps` — and does the cross-checking itself. **Do not read those sources separately and compare them yourself**: matching story slugs to sprint-status keys needs diacritic normalization and a similarity threshold, and doing it by eye produces confident wrong answers. That logic lives in the script for exactly that reason.

Exit 1 means no source was readable — report it and stop.

### Step 2 — Report the three parts

Always report all three, in this order:

1. **Position** — which story is in progress, what Orca has running.
2. **Divergence** (`lech`) — the two sources actively disagree. This is the finding that matters most; it is invisible to anyone who does not open both places.
3. **Could not compare** (`khong_doi_chieu_duoc`) — a check that did not run. Most common: no Orca Run is bound, so BMAD and Orca were never compared at all.

Never fold part 3 into "no problems found". Say which check did not run and why.

### Step 3 — Suggest, and mark it as a suggestion

Only after the facts. The script deliberately returns no recommendation, because what to do next depends on the caller's intent, which the script cannot see.

Ground every suggestion in something the output actually showed. If nothing in the output supports a next step, say the state looks clean and ask what they want to do — do not manufacture a task.

## If you are a dispatched Orca worker

You started with no inherited context. Before touching anything: run the script, find your own story in the output, and read that story file. Your task spec tells you what to do; the story file tells you what has already been decided and what is out of scope.

Report through your dispatch (`worker_done`), not by editing shared tracking files. `sprint-status.yaml` and story frontmatter belong to whoever coordinates — a worker writing there creates exactly the divergence this skill exists to catch.

## Reading the output

| Field | Means |
|---|---|
| `bmad.dang_lam` | Stories whose frontmatter says `in-progress` |
| `bmad.sprint_status_dang_hoat_dong` | Sprint rows that are not `backlog`/`optional`; the count of skipped rows is reported separately |
| `orca.co_run_binding` | `false` means no Run is bound — every BMAD↔Orca check was skipped |
| `orca.task` | Orchestration tasks, with status and a truncated spec |
| `orca.worktree` | Worktrees **of this repo only**, with branch and workspace status |
| `orca.worktree_repo_khac` | How many worktrees belonged to other repos and were filtered out |
| `lech` | Sources disagree — act on these |
| `khong_doi_chieu_duoc` | Checks that did not run — say so, do not treat as clean |

Three Orca states read very differently and must not be collapsed:

- `app_chay: false` — Orca is not running. The BMAD half still works; the Orca half is unknown. Not an error.
- `co_run_binding: false` — Orca runs but no Run is bound, so **every BMAD↔Orca check was skipped**. This lands in `khong_doi_chieu_duoc`, not in "clean".
- `co_run_binding: true` with `task: []` — a Run is bound and it genuinely has no tasks. Here the comparison **did** run. If a story is in progress, that is a real divergence, and the script reports it as one.

`orca worktree ps` returns worktrees for **every repo on the machine**, so the script keeps only those sharing a `repoId` with the worktree whose path is this repo root, and reports the number it dropped. Reporting all of them would be the exact failure this skill exists to prevent: a reader sees "7 worktrees" and assumes they relate to the story in progress. If no worktree matches this repo root, the script does **not** filter blind — it keeps the list and says why the filter could not run, which lands in `khong_doi_chieu_duoc`.

`worktree: null` means the worktree query failed; `worktree: []` means Orca returned none. The `--brief` line prints `?` for the first case so the two never look alike.
