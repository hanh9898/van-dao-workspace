# D2 · Blocking mechanisms — round 2, closing round-1 gaps

Budget spent: 11 tool calls. Returned 2026-08-31.
Round 2 was aimed at the four targets round 1 could not reach, plus two unsettled questions.

## Findings

**1. Aider — round-1 question SETTLED: ADVISORY, no completion gate.**
The official lint/test page describes `--auto-test` / `--test-cmd` as running tests after edits and
attempting to "fix any errors if the command returns a non-zero exit code" — but **nowhere states that
a session is blocked from ending, or that completion is refused, while tests still fail**.
Source: [aider.chat/docs/usage/lint-test.html](https://aider.chat/docs/usage/lint-test.html) — Aider
official docs. Accessed 2026-08-31. Confidence: **high** (primary source, direct fetch).
The absence of gating language *on a page specifically about this feature* is reasonably strong
evidence of "checked, likely absent" rather than "not found".

**2. Google Jules critic — round-1 question SETTLED: ADVISORY.**
The critic is "integrated directly into the generation process": "every proposed change undergoes
adversarial review before completion", and "the critic flags subtle bugs, missed edge cases, and
inefficient code. Jules then uses this feedback to improve the patch in real-time." That is a
**self-correction loop, not an external refusal gate**. No language describing a hard block, refused
submission, or denied state transition.
Source: [jules.google/docs/changelog/2025-08-083](https://jules.google/docs/changelog/2025-08-083/) —
Google, official changelog. Accessed 2026-08-31. Confidence: **medium-high** — fetched directly, but
content arrived via a summarizing tool rather than raw text; treat exact wording as reported-by-tool.

**3. OpenHands — INCONCLUSIVE at code level.**
Official docs describe a "Stuck Detector" monitoring conversation events for repetition (same tool
calls, repeated errors, monologues) which "can automatically halt execution when stuck patterns are
detected."
Source: [docs.openhands.dev/sdk/guides/agent-stuck-detector](https://docs.openhands.dev/sdk/guides/agent-stuck-detector)
— OpenHands official docs. Accessed 2026-08-31. Confidence: **low-medium**.
**The source file could not be reached** — `raw.githubusercontent.com/.../openhands/controller/stuck.py`
returned 404 (repo restructured toward a new SDK). So it is unverified whether stuck-detection *raises
and halts* or merely *sets a flag the caller may ignore*, and **zero evidence either way** on whether
`AgentFinishAction` / completion is validated before acceptance. This is the largest unresolved gap in
D2.

**4. Factory (Droid Control) — official docs show ADVISORY; a third-party claim contradicts.**
Official docs describe `/verify` as making the droid act as "an investigator, not an advocate" with
"anti-fabrication rules", and `/demo` as checking "the final video against the original commitments
before delivering". These are workflow/instruction-level behaviours — nothing describing a refused
state transition or exit-code gate.
Source: [docs.factory.ai/software-factory/droid-control](https://docs.factory.ai/software-factory/droid-control)
— Factory AI official docs. Accessed 2026-08-31. Confidence: medium. Class: **ADVISORY** as far as this
page shows.

**5. Amp (Sourcegraph) — DID NOT REACH.**
Search returned only marketing and aggregator pages. No primary Sourcegraph documentation fetched;
budget exhausted. This is "did not reach", not "checked and absent".

**6. Cursor — DID NOT REACH.** Zero budget remained.

## Contradictions

**Factory: official docs vs. a third-party account.** A Medium post claims Factory Droid uses a
"deterministic completion gate" with a "Spec → Test → Implement → Verify → Close" pattern where "every
phase must produce a file or exit code" and "the orchestrator never trusts chat output" — which, if
true, would be **BLOCKING** and would be the closest thing found to what this research is looking for.
Surfaced only as a search snippet, never fetched, never confirmed against a primary Factory source.
**Do not cite as confirmed.** Resolving this needs a direct fetch of Factory's gate/hook documentation
under some path other than `droid-control`.

## Leads worth chasing

- **OpenHands source**: `github.com/OpenHands/software-agent-sdk/.../conversation/stuck_detector.py` —
  does stuck-detection raise/halt, or set a flag? And is there `AgentFinishAction` validation in the
  controller loop?
- **Factory**: find the docs page describing the "Spec → Test → Implement → Verify → Close" pattern to
  confirm or refute the deterministic-gate claim.
- **Amp**: `ampcode.com` or Sourcegraph's own docs, not generic search.
- **Cursor**: entirely unexamined.

## What I looked for and could NOT find

Stated with the distinction the brief required:

| Target | Status |
|---|---|
| Aider session gate | **Checked, likely absent** — never described on the page that would describe it |
| Jules hard block | **Checked, likely absent** — no such language in the changelog |
| OpenHands completion validation | **Did not reach** code level; docs assert halting but control flow unconfirmed |
| Factory deterministic gate | **Unresolved contradiction** — official page advisory, third-party claims blocking |
| Amp | **Did not reach** — no primary source examined |
| Cursor | **Did not reach** — no investigation performed |
