# Skill Quality Lens

**Goal:** judge whether a Claude Code Agent Skill (a `SKILL.md` and its companions — `evals/`,
referenced `agents/*.md`/`commands/*.md` in the same family) is built to the standard a real, shipped
skill needs. This is **not** a check for unhandled branches in the skill's own conversational logic
(that is Edge-Case Hunter's job) and **not** prose/structure polish (the editorial lenses' job). It
checks the skill-*authoring*-specific failure modes that generic review does not catch — distilled
from cross-source research run this project (Anthropic's official Agent Skills best-practices, the
`skill-creator` tool's real source, Superpowers/obra, claude-tutor/kirilxd, GitHub Copilot
custom-instructions research, the CCAR-F exam content on progressive disclosure and context budgets)
and from two real defects this project already shipped once, caught only because the skill was run
for real instead of read and reasoned about.

## Scope

Applies to: a `SKILL.md` file (new or changed), its `evals/` companion, and any `agents/*.md` /
`commands/*.md` sharing the change. Skip content that commissions or specs the skill (a story, a PRD)
— review that with other lenses; this lens judges the skill artifact itself.

## Checks

Walk the content against every check below. Report a finding only where a check **fails** — passing
checks produce nothing, per this lens's stance (matches Edge-Case Hunter: report gaps, not what
already holds).

### 1. Completion and boundary conditions are explicit

- Does the skill state a clear, checkable "done" condition — not just what it does, but how it (or
  whoever invokes it) knows it has actually finished?
- Does it state clear conditions under which it does **not** help — out-of-scope requests, features
  not yet built — committing to an explicit "not supported yet" response rather than silent guessing
  or a plausible-sounding fabrication?

Missing either leaves an agent or user with no signal for when to stop trusting the skill's silence.

### 2. Self-contained — no invisible dependencies

- Does the skill's own content (not its surrounding spec/story) cite requirement IDs, section
  numbers, or paths that exist only in a development workspace that will not ship with the skill?
- Could a reader with **only this file** — no access to the rest of the repo — execute it correctly?

A skill ships alone. A citation to material the runtime user will never have is not traceability;
it is a broken reference the moment the skill leaves the dev workspace.

### 3. Every command the skill tells someone to type has actually been run

- Does the skill's prose instruct a user or agent to invoke a specific slash command, tool, or config
  value?
- Is there direct evidence (an eval transcript, or citable current documentation) that this **exact**
  string was exercised for real and resolved — not assumed correct by pattern-matching a naming
  convention?

A command that "should" work by convention but was never actually invoked is exactly the failure mode
that ships broken instructions with nothing left to catch it — a real recurrence in this project
(a hard-coded short command prefix that the plugin's real name never supported).

### 4. External mechanism claims are verified, not assumed

- Does the skill rely on a specific platform mechanism (a frontmatter flag, a config-substitution
  syntax, an API field, a storage location) to guarantee some property?
- Is there evidence the mechanism was checked against real behavior or current official documentation
  in this change — not carried over from training-data memory of how it "usually" works?

Platform details drift, and memory of them is often wrong in a specific, silent way (a stale field
shape, a renamed API). Both real bugs this project shipped were exactly this: assuming a config
mechanism's shape instead of testing it — caught only by running the skill for real.

**Where 3 and 4 overlap, split them by how the failure surfaces.** An unrun command belongs to check 3
when typing it is what fails — wrong name, wrong prefix, command does not exist. It belongs to check 4
when the string is right and the *mechanism behind it* behaves other than assumed — the flag is
ignored, the field was renamed, the substitution never happens. One defect can be both; report it once
under the check whose fix is different, and say the other applies.

### 5. A claimed hard guarantee is tested at the mechanism level, not the compliance level

- Where the skill claims something is **impossible** for the model to do — not just "instructed not
  to," but structurally blocked (a lock, a disabled auto-invocation, a permission boundary) — is there
  evidence the underlying platform mechanism was actually tripped and observed to hold, rather than
  only observing the model politely decline when asked?

A model choosing to refuse in one conversation is not evidence the enforcement layer would stop a
differently-phrased attempt, a different model, or a future version reasoning differently about the
same instructions. If only compliance-level evidence exists, say so as a finding — don't accept it as
proof of the mechanism-level claim.

### 6. Behavioral eval exists, is real, and is durable

- Does a skill considered "done" have at least a light behavioral eval covering its main scenarios —
  written at or near the time the skill itself was drafted, not deferred to an unscheduled later pass?
- Is each piece of evidence a **verbatim transcript from a real run** — not a description of expected
  behavior, not a simulated/imagined transcript, and not a pointer to a path that will not survive
  past the authoring session (a session-local scratch directory)?
- Was the eval run against the actual packaged skill, not just read as prose and reasoned about?
  **"Packaged" means whatever the real reach path is for this skill's kind** — a plugin skill: installed
  from the built plugin; a workspace skill under `.claude/skills/`: invoked by its real name from the
  workspace root (`claude -p "/name …"`), because that *is* how a user reaches it. What disqualifies an
  eval either way is the same thing: the skill was never actually loaded, only quoted.

An eval that never ran the real skill, or whose evidence can't outlive the session that wrote it,
gives false confidence indistinguishable from no eval at all.

### 7. Description earns its trigger, or the skill doesn't rely on triggering

- Does the skill's frontmatter `description` state **when** to use it — concrete situations or
  phrasing a user might actually say — not only what it does in the abstract?
- If a silent miss (the model handling the request inline without invoking the skill) would be a
  real failure, not just an inconvenience, does the skill force explicit invocation (a bare command,
  `disable-model-invocation`) rather than resting on description-based auto-triggering alone?

Models under-trigger skills whose description reads as a feature list rather than a matching pattern
for real phrasing. Where silent non-invocation is a real failure mode, description quality alone is a
weak guarantee — this is exactly why some skills in this project are commands, not auto-triggered.

### 8. Context budget is respected

- Measure the skill's tokens and locate the **5,000-token mark**. Is anything past it load-bearing —
  a data schema, a write rule, a safety constraint, a required confirmation step?
- Is the main file dramatically larger than its core path needs, with rarely-needed detail written
  inline rather than pushed to a referenced sub-file loaded only when needed?

The numbers are the check, not a style preference. After auto-compaction a skill is re-attached at
only its **first 5,000 tokens**; every re-attached skill draws on a shared **25,000-token** pool; and
a skill invoked early enough in the session is dropped outright once that pool is spent. Content past
the 5,000-token mark is therefore not merely expensive — in a compacted session it is *gone*, while
the skill still runs and still sounds certain. Report where that mark lands and what falls after it,
not just that the file is long. A real case in this project: a 7,334-token skill lost its entire data
schema section this way.

## Output

Emit findings in the canonical fields (`location`, `trigger_condition`, `guard_snippet`,
`potential_consequence`) — no severity, priority, or ranking. `[]` is a valid result when a skill
genuinely meets every check above; re-check before returning it empty, the way Blind Hunter does.
