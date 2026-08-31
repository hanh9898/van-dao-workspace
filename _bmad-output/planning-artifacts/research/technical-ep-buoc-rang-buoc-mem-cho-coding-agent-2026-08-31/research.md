---
title: 'technical research: Enforcing soft constraints on coding agents'
type: 'technical'
topic: 'Enforcing soft constraints on coding agents'
decision: 'Can constraints that lack an external oracle be made enforceable, or do they permanently depend on a careful human reader?'
source: 'native run (bmad-deep-recon)'
status: draft
preset: 'standard'
validation: 'normal'
created: '2026-08-31'
updated: '2026-08-31'
---

# technical research: Enforcing soft constraints on coding agents

**Decision this research serves:** Can constraints that lack an external oracle be made enforceable, or
do they permanently depend on a careful human reader?

## Executive summary

**The answer is: partly, and the dividing line is not the one we assumed.**

We assumed the split was *"has an external oracle"* vs *"does not"*. The literature draws it elsewhere.
The TACL survey of self-correction identifies one variable that determines whether an agent can check
its own work: **is verifying the answer easier than producing it?** [20][21] Where verification is
genuinely easier — decomposable outputs, countable properties, structural facts — self-checking works
and can be made mechanical. Where it is not, no amount of prompting or reminding helps, and the
evidence for that is unusually strong.

Four findings carry the decision:

1. **Self-correction without an external signal does not work, and the papers claiming otherwise were
   measuring something else.** The survey states plainly that *no prior work shows successful
   self-correction using self-generated feedback under fair settings* [20]. Self-Refine's celebrated
   ~20% gain comes from deliberately weakening the initial-generation baseline; RCI and Reflexion leak
   ground-truth labels into setups described as feedback-free [20]. Our round-1 "contradiction" between
   Huang and Madaan was not a contradiction — one side had an invalid setup. **Status: overturned.**

2. **Separating the review session helps, measurably but modestly.** A controlled study across 30
   artifacts and 150 injected errors found fresh-session review at F1 **28.6%** vs same-session
   self-review at **24.6%**, and — decisively — reviewing *twice in the same session did not help*
   (p=0.11), which rules out repetition and points at context separation itself [22]. But even the best
   condition **missed roughly 70% of injected errors**, and the source is an unvetted single-author
   preprint.

3. **Metamorphic testing converts subjective rules about text into deterministic checks, with the
   strongest numbers in this whole run.** Error-finding rates of 51–91.2% against production text
   systems, dropping to 0–5.9% after retraining, peer-reviewed at ICSE [6]. This is the one technique
   found that genuinely turns "is this text right" into a repeatable pass/fail.

4. **No production harness verified here blocks completion on an external oracle by default** — and all
   of them use strong verification language anyway [10][11][17]. Claude Code is the exception in a
   specific way: it does not block by itself, it **exposes hook events with an exit-code contract** so a
   team can wire an oracle in, including `TaskCompleted`, where exit 2 blocks a task from being marked
   complete [9].

**What this means for us:** stop trying to make the agent notice its own mistakes, and start sorting
constraints by whether their verification is cheaper than their execution. For the cheap-to-verify
ones, build the check and wire it to a hook. For the rest, a fresh-context reviewer buys a measurable
but partial improvement — and a careful human reader remains the backstop, which the most credible
practitioner source in the field also concludes.

---

## Recommended course of action

Sorted by strength of evidence, not by ease.

### Tier 1 — Do these; the evidence is strong and the work is small

**1 · Sort every constraint by the TACL test before anything else.**
For each rule, ask: *is checking it cheaper than doing it?* This is the single variable the survey
identifies as determining success [21]. Applied to our own ledger of ten pitfalls:

| Pitfall | Is verification cheaper than execution? | Follows |
|---|---|---|
| #2 misreading a truncated result | **Yes** — re-run the command with a counter | Mechanisable |
| #4 creating new debt while clearing debt | **Yes** — grep the files this turn touched | Mechanisable |
| #6 stopping at the easy part | **Yes**, if criteria are countable | Mechanisable |
| #7 false precision | Partly — compare two measurements with one instrument | Semi |
| #8 scope missed when dispatching | **Yes** — list files by command, diff against what was handed out | Mechanisable |
| #10 own measuring script wrong | Partly — run the measurement against a known answer | Semi |
| #1 existence vs. behaviour | **No** — requires knowing what "works" means here | Needs external oracle |
| #3 breaking a rule written next to it | **No** | Needs external oracle |
| #5 switching to an easier method | **No** | Needs external oracle |
| #9 answering one worker of several | **No** | Needs external oracle |

Five of ten are mechanisable and are not currently mechanised. That is the highest-value finding in
this report, and it needed no new technology — only the right question.

**2 · Extend `check-invariants.py` — we already built the technique without knowing its name.**
LEDGER validates edits against structural invariants over an artifact (reference integrity, terminology
consistency) and reports consistency rising **56% → 76%** [7]. Our `check-invariants.py` is the same
idea. Extend it from "did the structure survive" to include terminology consistency against
`naming-map.md`, which directly mechanises pitfall #4.

**3 · Move the completion check from `Stop` to `TaskCompleted`.**
Exit 2 on `TaskCompleted` blocks a task being marked complete [9] — it fires at the exact moment the
agent claims done, which is when pitfall #6 happens. Our current hook is on `Stop`, one step late.

### Tier 2 — Worth doing, with the number in plain sight

**4 · Add a fresh-context reviewer, and treat it as catching one error in four.**
Cross-context review measurably beats same-context self-review, and repetition in the same session does
not help at all [22]. The mechanism is cheap here: a subagent with the research firewall already gives
fresh context. But **budget for F1 ≈ 29%** — it is a second net, not a gate.

**5 · If an LLM judge is used, use the published protocol.**
Report κ rather than raw accuracy, measure position bias with swapped runs, validate on two benchmarks
with different label structures [3]. Raw agreement overstates discriminative ability by **33.8–41.3
points** [1], and position-flip rates reach **17.3%** [2].

### Tier 3 — Do not do these

**6 · Do not build same-context self-review.** The survey is unambiguous under fair settings [20], and
same-session double review measured *worse* than single review [22].

**7 · Do not trust verification language in vendor documentation.** Cognition's own blog confirms its
verification apparatus is a reporting layer, not a gate — inside a document titled *Verifying Agentic
Development at Scale* [10]. Aider and Jules both turned out advisory when their primary docs were read
[17][11].

### What stays with the human

Pitfalls #1, #3, #5 and #9 have no cheap verification and no oracle. The honest position — which the
most credible practitioner source in this field also reaches — is that these remain with a careful
reader. The useful move is not to pretend otherwise but to **shorten the loop**: surface checkable
artifacts earlier so the human sees a divergence in minutes rather than after a batch.

---

## D1 · Can a soft constraint be given an external oracle?

**Metamorphic testing is the strongest evidence, and it works on text.** Rather than needing a known
answer per input, it defines *metamorphic relations* — expected relationships between outputs of
related or perturbed inputs. MTTM applies 11 such relations at character, word and sentence level to
text-moderation systems: error-finding rates **83.9%** (Google), **82.5%** (Huawei), **51%** (Baidu),
up to **91.2%** against academic algorithms; retraining cut this to **0–5.9%** without losing accuracy
on the original test set [6]. Peer-reviewed (ICSE 2023), concrete, and aimed at text rather than code.

**Structural invariants on the artifact are second.** LEDGER builds a dependency graph over document
structure and validates edited nodes against it — reference integrity and terminology consistency —
reporting consistency **56% → 76%** across six models [7]. Confidence medium; the invariant catalog
could not be extracted.

**LLM-as-judge is weaker than commonly cited.** Across ~541,000 judgments and 21 judges,
chance-corrected agreement ran **κ 0.271–0.898**, while raw exact-match accuracy **overstated
discriminative ability by 33.8–41.3 points** — "kappa deflation" [1]. Reproducibility is high
(test-retest 0.943) yet **position-flip reaches 17.3%** and judge rankings shift by up to **14
positions** across benchmarks [2]. The widely repeated "~80% agreement with humans" is exactly the
uncorrected figure the authors warn against.

**Self-consistency has a blind spot scale does not fix.** Repeated sampling catches content that
varies, but *self-consistent errors* — the model reliably producing the same wrong answer — evade it,
and the blind spot does not shrink with model size [8].

**Not found:** any study measuring judge reliability for checking a coding agent's constraint
compliance; any general named method for turning a subjective rule into a deterministic check outside
these two instances; any measured detection rate for cross-model differential testing.

## D2 · What production harnesses actually block

| Harness | Mechanism | Class |
|---|---|---|
| **Claude Code** | Hooks with exit-code contract: `PreToolUse` (exit 2 blocks, unoverridable), `Stop`/`SubagentStop`, **`TaskCompleted`** (exit 2 blocks marking complete), `PostToolBatch` | **BLOCKING** [9] |
| Codex CLI | OS-level sandbox and approval policy | BLOCKING, different failure class |
| Aider | `--test-cmd` re-runs and feeds failures back | **ADVISORY** — no session gate described [17] |
| Google Jules | Adversarial critic before completion | **ADVISORY** — self-correction loop, not a refusal [11] |
| Devin | Test reports, videos, confidence score | **ADVISORY** — confirmed by Cognition's own blog [10] |
| SWE-agent | `exit_status` taxonomy | ADVISORY — post-hoc telemetry |
| OpenHands | Stuck detector documented as able to halt | **UNCONFIRMED** — source unreachable [18] |
| Factory | `/verify`, `/demo` with anti-fabrication rules | ADVISORY in official docs; third-party claims a gate — **unresolved** [19] |
| Amp, Cursor | — | **Not examined** |

Two findings follow. **First:** among harnesses verified from primary sources, none blocks completion on
an external oracle by default; Claude Code instead exposes the API to wire one in. The thing to build is
the oracle. **Second:** every product uses strong verification language while shipping advisory
behaviour — the failure mode is calling something "verification" because it *describes* the right thing,
not because it *blocks*.

## D3 · Can the agent catch its own mistakes?

**Intrinsic self-correction makes reasoning worse.** GPT-4 on GSM8K falls **95.5% → 91.5%** after a
self-correction pass with no external signal, consistently across benchmarks [12].

**The most on-point result reproduces our exact symptom.** Injecting an identical error framed either
as user-introduced or model-introduced, in the same context: **64.5% of models corrected the
externally attributed error but failed on the identical self-attributed one** [13]. The detection
capability is present; it is not activated when the error is labelled "mine". Confidence medium.

**Self-preference is measured and grows with self-recognition.** GPT-4 identifies its own outputs at
**73.5%**; self-preference bias correlates with that ability, and pushing recognition above **90%**
strengthened the bias [15].

**A separate checker beats self-critique and paid human reviewers.** Model critiques preferred over
human critiques in **63%** of cases on natural errors, **over 80%** on inserted bugs [14]. Decisive
caveat: this is a *separately trained* critic model — evidence that a different purpose-built checker
works, not that self-checking does.

## D4 · The survey, and whether a second pair of eyes helps

**The survey settles D3's contradiction, and not gently.** *"No prior work shows successful
self-correction of responses from LLMs using feedback generated by prompting themselves under fair
settings in general tasks"* [20]. Self-Refine weakens its own initial-generation baseline; RCI uses
ground truth to gate correction; Reflexion uses exact-match against ground truth as "feedback" [20].
The apparent disagreement in the literature is a difference in evaluation validity, not in results.

**Where self-correction genuinely works:** tasks whose verification is much easier than the task itself
(decomposable outputs); or where a reliable external tool exists; or with a fine-tuned feedback
generator. **Reliability of feedback generation is the single determining variable** [21].

**Fresh-context review, measured.** 30 artifacts, 150 injected errors, 360 reviews: CCR (fresh session)
F1 **28.6%**, same-session self-review **24.6%** (p=0.008, d=0.52), context-aware subagent **23.8%**,
same-session review twice **21.7%**. Reviewing twice in one session did not beat reviewing once
(p=0.11) — the benefit is context separation itself, not repetition [22]. Confidence medium-low, and
every condition misses ~70% of errors.

**Production practice has no numbers.** Several vendors describe shipping a separate reviewer with no
inherited context as a blocking gate; **none published a measured catch rate** [24].

---

## Sources

| # | Source | Publisher, date |
|---|---|---|
| [1][2][3] | [Reliability without Validity: LLM-as-a-Judge across Agreement, Consistency and Bias](https://arxiv.org/html/2606.19544v1) | arXiv, 2026-06 |
| [6] | [MTTM: Metamorphic Testing for Textual Content Moderation Software](https://arxiv.org/abs/2302.05706) | ICSE 2023 |
| [7] | [LEDGER: Scaling Agentic Document Editing with Dependency-aware Graph Retrieval](https://arxiv.org/abs/2606.28379) | arXiv, 2026-06 |
| [8] | [Too Consistent to Detect: Self-Consistent Errors in LLMs](https://arxiv.org/pdf/2505.17656) | arXiv, 2025-05 |
| [9] | [Claude Code hooks reference](https://code.claude.com/docs/en/hooks) | Anthropic, official docs |
| [10] | [Verifying Agentic Development at Scale](https://cognition.com/blog/testing-development) | Cognition |
| [11] | [Jules changelog 2025-08](https://jules.google/docs/changelog/2025-08-083/) | Google |
| [12] | [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798) | ICLR 2024 |
| [13] | [Self-Correction Bench](https://arxiv.org/html/2507.02778) | arXiv, 2025 |
| [14] | [LLM Critics Help Catch LLM Bugs](https://cdn.openai.com/llm-critics-help-catch-llm-bugs-paper.pdf) | OpenAI, 2024 |
| [15] | [LLM Evaluators Recognize and Favor Their Own Generations](https://proceedings.neurips.cc/paper_files/paper/2024/hash/7f1f0218e45f5414c79c0679633e47bc-Abstract-Conference.html) | NeurIPS 2024 |
| [17] | [Aider linting and testing](https://aider.chat/docs/usage/lint-test.html) | Aider, official docs |
| [18] | [OpenHands stuck detector](https://docs.openhands.dev/sdk/guides/agent-stuck-detector) | OpenHands, official docs |
| [19] | [Factory Droid Control](https://docs.factory.ai/software-factory/droid-control) | Factory AI |
| [20][21] | [When Can LLMs Actually Correct Their Own Mistakes?](https://arxiv.org/html/2406.01297v3) | TACL / MIT Press, 2024 |
| [22] | [Cross-Context Review](https://arxiv.org/abs/2603.12123) | arXiv, 2026-03 |

## Open questions

Reported rather than dropped, per the run's stopping rules.

1. **Factory's completion gate** — official docs show advisory behaviour; an unfetched third-party post
   claims a deterministic gate with exit-code enforcement. If true it would be the closest match to what
   this research sought. Unresolved.
2. **OpenHands** — the stuck detector is documented as able to halt execution, but the source file
   returned 404 after a repo restructure, so halt-vs-flag is unconfirmed, and there is no evidence
   either way about completion validation.
3. **Amp and Cursor** — not examined. This is *did not reach*, not *checked and absent*.
4. **The 64.5% self-attribution figure** [13] is the finding that best matches our symptom and is
   verified only at abstract level. A result that fits a prior hypothesis this neatly deserves a full
   read before it carries weight.
5. **Cross-context review** rests on one unvetted single-author preprint [22]. Three related papers
   surfaced and were not read: adversarial structured-disagreement review, self-review failures in code
   modernization, and reviewability measurement in agent work.
6. **Human inspection baselines** (~55–60%) came from search synthesis, not primary papers.
