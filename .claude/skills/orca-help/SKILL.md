---
name: orca-help
description: Use when you want to do something with Orca but are not sure which mode or command fits — asked as "how do I hand this off", "can Orca run these in parallel", "how do I schedule this", "which orca command does X", "can Orca drive the browser", or when about to use Orca and unsure whether the task needs supervision. Routes to the right mode and the right version-matched guide; it does not reproduce guide content.
---

# Orca Help — pick the mode, then load the right guide

## Done when

The caller knows three things: **which mode fits** (or that none does), **which guide to load and the exact command to load it**, and **which preconditions are not yet met**. If a precondition fails, done means saying so and stopping — not routing anyway and letting the failure surface later.

If the request turns out not to need Orca at all, done means saying that plainly.

## When this skill does not help

- **"Where does the work stand?"** — that is `work-state`, which reads BMAD and Orca state together. This skill routes; that one reports.
- **Command details, flags, exact syntax.** This skill deliberately holds none. The version-matched guide does, and it is one command away. Reproducing any of it here creates a second copy that drifts from the binary that will actually run.
- **Non-Orca work.** Ordinary shell commands, editing files, running tests in the current terminal — none of that needs Orca. Say so rather than routing to a mode.
- **BMAD flow questions.** For which BMAD skill comes next, that is `bmad-help`.

## No customization

No `customize.toml` fields. Everything comes from the live Orca binary; there is nothing to configure here.

## Route → check → point

### Step 1 — Classify

Three modes cover **coordination**. A fourth path covers everything else, and it is not a fallback for failure — Orca does far more than coordinate.

| The request sounds like | Mode | Why |
|---|---|---|
| "hand this off", "give it to another agent", "another worktree", "let X take over" | **Handoff** | Ownership transfers and you stop watching. Creating tasks or dispatches here manufactures lifecycle obligations nobody asked for |
| "run these in parallel and tell me when done", "wait for results", "B depends on A", "supervise", "decision gate" | **Orchestration** | Coordination state matters: Run, Task, Dispatch, `worker_done` |
| "every morning", "on a schedule", "daily", cron-like phrasing | **Automation** | Nobody is present when it runs |
| **anything else Orca does** — drive the browser, read a desktop app, control an emulator, read a Linear ticket, publish an artifact, manage worktrees or terminals directly | **Direct use** | No coordination involved. Go straight to Step 3 and find the matching guide |

**Naming a custom model or reasoning effort does not make a handoff supervised.** "Hand this to codex with high effort" is still a handoff.

**When to ask instead of deciding.** The default for "give this to another agent" is Handoff — that is settled, do not ask. Ask exactly one question only when the request contains a signal pointing both ways: it names another agent *and* asks for results, progress, or completion. Then ask: *do you want to be told when it finishes, or are you handing it over?*

**A request can touch two modes.** "Dispatch these four in parallel, then every morning re-run the failures" is Orchestration plus Automation. Handle them as two separate pieces of work rather than forcing one label.

**If the mode is Orchestration, mention two things now**, because both are cheaper to plan for than to hit:

- A dispatched worker normally cannot dispatch further workers. The depth limit is a setting (Orca desktop app → Settings → Orchestration → Nested worker depth), and creating a new Run does not reset it. Split work before dispatching rather than discovering the limit mid-run.
- **Orca does not detect conflicts.** It places workers where told and does not know two of them are about to write the same file. Either give each its own worktree, or state in each task spec that workers only edit files and the coordinator commits.

### Step 2 — Check preconditions before routing

Run these; do not assume.

```
orca status --json
```

- `app.running: false` → tell the user to start Orca (`orca open --json`) and stop. Nothing else will work.
- Command not found at all → Orca is not installed on this machine. Say so; there is nothing to route to.

For **Orchestration only**, one more:

```
orca orchestration task-list --json
```

`run_required` means the feature is enabled and simply has nothing bound yet — normal before `run-create`, not an error. A different error (feature disabled, for instance) is a real block: report it and stop.

On Linux outside an Orca terminal the executable is `orca-ide`. The Orca guide warns that bare `orca` there resolves to the GNOME screen reader and starts speech — quoted from the guide, not verified here. On this machine and on macOS, `orca` is correct.

### Step 3 — Point at the guide, do not summarize it

List what guides this binary actually ships — never recite a remembered list, because topics change between releases:

```
orca skills list --json
```

Then load the one whose description matches the request:

```
orca skills get <topic>
```

**There is no guide named `automation`.** Scheduling lives inside the `orca-cli` guide alongside worktrees and terminals. Do not send the caller looking for a topic that does not exist — check the list before naming one.

If `orca skills list` fails while Orca is running, do not guess a topic name. Report the failure; `orca --help` still lists command groups and is a usable fallback for orientation.

Guides are served by the binary itself so they cannot drift from the commands that will run. Read the guide before running its commands; do not reconstruct flags from memory or from an earlier session.

**When the guide is not enough** — a specific flag, an unusual subcommand — two more sources, in order:

```
orca agent-context --json     # machine-readable schema for every command (large: filter, don't read whole)
orca skills installed --json  # which skills this Orca host has, for "what do I already have"
```

### How much to hand back

If the caller asked *which* command, give that command. If they asked *how to do a task*, give the first command of the path and let the guide carry the rest — a half-remembered sequence is worse than none.

## If the answer is "you don't need Orca"

Say it. A single task in the current terminal, a quick edit, a test run — these need no worktree, no Run, no dispatch. Routing them into orchestration adds ceremony and a lifecycle to close, and buys nothing.
