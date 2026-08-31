# D2 · Blocking mechanisms in production harnesses — round 1, assistant 2

Budget spent: 11 tool calls, 6 sources reached (Amp, Factory, Cursor not reached). Returned 2026-08-31.

Every finding is tagged **BLOCKING** (the harness fails or halts the run) or **ADVISORY** (the model
is told something and may ignore it). That distinction was the brief's core requirement.

## Findings

**1. Claude Code — hook events that block, with an exit-code contract. BLOCKING.**
The hook system defines lifecycle events that block agent behaviour via process exit codes / JSON
decision fields, independent of what the model decides:

| Event | What exit code 2 does |
|---|---|
| `PreToolUse` | Blocks the tool call — **cannot be overridden even by a JSON "allow"** |
| `Stop` / `SubagentStop` | Forces `continue: true`; the agent cannot end the turn |
| **`TaskCompleted`** | **Blocks a task from being marked complete** |
| `PostToolBatch` | Halts the loop before the next model call |

Hooks run arbitrary shell commands, so an external oracle (git diff scope check, test exit code,
regex over a tracked file) wires directly into the block condition.
Source: [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks) — Anthropic, official
docs, live (no pub date stated). Accessed 2026-08-31. Confidence: high. Class: primary/official.

**2. Aider — lint/test loop tied to process exit codes. BLOCKING (per-edit).**
Runs a linter and/or `--test-cmd` after every edit; non-zero exit captures the failure output, feeds
it back to the model, re-runs. Described as a "self-healing loop". Same shape as the git-state /
exit-code oracles already trusted here.
Source: [aider.chat/docs/usage/lint-test.html](https://aider.chat/docs/usage/lint-test.html) — Aider
official docs. Accessed 2026-08-31. Confidence: **medium** — obtained via search summary, not a direct
fetch; exact wording unverified.
**Open question, not resolved:** whether it also gates *session completion*, i.e. whether Aider can
end a session while tests still fail.

**3. Devin / Cognition — verification is explicitly NOT a blocking gate. ADVISORY.**
Devin produces test reports (pass/fail assertions, labeled videos, screenshots) surfaced to engineers
and pushed to Slack for human review. The primary source contains **no** mention of CI rejecting
unverified PRs, test failures blocking merges, or a mandatory passing check before Devin reports work
done. The confidence score (🟢🟡🔴) is a self-reported signal correlated with success — low confidence
does not block Devin, it triggers Devin to ask clarifying questions.
Source: [cognition.com/blog/testing-development](https://cognition.com/blog/testing-development) —
Cognition, official company blog. Accessed 2026-08-31. Confidence: high (directly fetched and read).
Class: primary. **First-party confirmation that the "verification" apparatus is a reporting layer, not
an enforcement gate.**

**4. Google Jules — a "Critic" adversarial-review step before completion. Likely BLOCKING, unverified.**
Jules runs a critic agent that adversarially reviews every proposed change before completion, catching
patches that pass tests but introduce subtle logic errors or silently drop required fields. The critic
"doesn't fix code, it flags it, then hands it back to Jules to improve."
Source: [jules.google/docs/changelog/2025-08-083](https://jules.google/docs/changelog/2025-08-083/) —
Google, 2025-08. Accessed 2026-08-31. Confidence: **medium** — search-engine synthesis, not a direct
fetch. Whether the critic's flag can literally prevent completion, or is a strongly weighted
suggestion the model may override, was **not** confirmed.

**5. OpenAI Codex CLI — OS-level sandbox and approval policy. BLOCKING, but different failure class.**
Platform-native enforcement (macOS/Linux/WSL/Windows) restricting file writes and network access, plus
an approval policy that pauses for human confirmation on specified command classes. Genuinely blocking
because it is enforced by the OS, not the model — but it targets unsafe or unapproved *actions*. No
evidence it targets scope-narrowing or false completion.
Source: [developers.openai.com/codex/agent-approvals-security](https://developers.openai.com/codex/agent-approvals-security),
[/codex/security](https://developers.openai.com/codex/security) — OpenAI official docs. Accessed
2026-08-31. Confidence: medium (search summary, not direct fetch). Adjacent, not a direct hit.

**6. SWE-agent — exit-status taxonomy is telemetry, not an in-loop gate. ADVISORY.**
Trajectories record a terminal `exit_status` (`submitted`, `exit_cost`, `exit_context`, `exit_forfeit`)
in `.traj` files, used by downstream and third-party offline analysis. Nothing retrieved shows an
in-session blocking check against scope-narrowing or premature completion — it logs *why* a run ended,
it does not prevent an ending.
Source: [SWE-agent trajectories docs](https://github.com/SWE-agent/SWE-agent/blob/main/docs/usage/trajectories.md),
[swe-agent.com/latest/usage/cli](https://swe-agent.com/latest/usage/cli/) — Princeton NLP. Accessed
2026-08-31. Confidence: medium (secondhand retrieval).

## Contradictions

No claim-vs-claim contradiction. The interesting tension is **structural, inside a single document**:
Cognition brands its offering as "Verifying Agentic Development at Scale" while the same blog confirms
none of the apparatus is a blocking gate — it is a human-reviewed transparency layer.

Treat as a cautionary data point: **"verification" in vendor docs does not imply an enforced oracle.**

## Leads worth chasing

- **OpenHands** primary repo not examined — searches surfaced only third-party academic papers using
  its trajectory logs. Check `AgentController`, stuck-detection / loop-detector code, and whether
  `AgentFinishAction` requires any check before being accepted.
- **Amp (Sourcegraph) and Factory** — not searched at all; budget exhausted. Genuinely unexamined, not
  "no mechanism found".
- **Aider** — fetch the docs page directly to settle whether `--test-cmd` gates session completion.
- **Jules critic** — fetch the changelog directly to settle hard block vs. advisory annotation.
- **Claude Code `TaskCompleted` / `PostToolBatch`** — the docs describe the API but not a documented
  instance of wiring a git-diff scope check to catch silent scope-narrowing. Worth finding a real
  example.
- **SWE-agent** — is `exit_forfeit` / `exit_cost` autosubmission ever used deliberately as a guard
  against narrowing scope to hit a budget, or purely a resource safeguard?

## What I looked for and could NOT find

- **OpenHands**: no evidence of a *production harness* mechanism (as opposed to offline research
  tooling built on its logs) that blocks scope-narrowing or false completion.
- **Amp, Factory**: zero findings — unexamined, not absent.
- **Devin**: explicitly confirmed by primary source to have **no** blocking gate for false completion.
- **SWE-agent**: no blocking completion-checker for either failure class.
- **Codex CLI**: blocking enforcement is real but scoped to safety/permissions, not to scope
  substitution or false "done".
- Not reached: Cursor, Devin's agent-loop internals beyond the blog, and any production (not research)
  trajectory-diff or replay-checking tooling in any of the ten named harnesses.
