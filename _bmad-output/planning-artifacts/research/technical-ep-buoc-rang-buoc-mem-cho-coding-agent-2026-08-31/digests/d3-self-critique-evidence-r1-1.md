# D3 · Measured evidence on self-critique and self-verification — round 1, assistant 3

Budget spent: 11 tool calls, 6 sources. Returned 2026-08-31.
Tooling note from the assistant: several WebFetch calls against arXiv PDF/HTML returned degraded or
synthesized text rather than clean table extraction, which capped verification depth per source.

## Findings

**F1. Intrinsic self-correction *degrades* reasoning accuracy.**
GPT-4 on GSM8K: **95.5% → 91.5%** after a self-correction pass with no external signal. The paper
states performance "consistently dropped across all tested benchmarks" for GPT-3.5 and GPT-4 without
external feedback. It further shows that prior reports of self-correction "success" relied on **oracle
(ground-truth) labels to know when to stop correcting** — not genuine intrinsic ability. Self-consistency
(majority voting) outperformed multi-agent debate as a correction strategy.
Source: Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet",
[arXiv:2310.01798](https://arxiv.org/abs/2310.01798), Google DeepMind / UIUC, **ICLR 2024**,
2023-10-03 (rev. 2024-03-14). Accessed 2026-08-31. Confidence: medium-high — the 95.5/91.5 figures
come from two independent secondary summaries; the raw table did not render via PDF fetch.

**F2. Self-Refine reports large gains from the same shape of loop — apparent contradiction with F1.**
~20% absolute average improvement across 7 tasks using one model as generator, critic and refiner,
with no external feedback and no extra training. Deltas: **+8.7** code optimization, **+13.9** code
readability, **+21.6** sentiment reversal, constrained-generation preference **25.4% → 74.6%** (GPT-4).
Source: Madaan et al., "Self-Refine: Iterative Refinement with Self-Feedback",
[arXiv:2303.17651](https://arxiv.org/abs/2303.17651), 2023-03-30. Accessed 2026-08-31. Confidence:
medium (numbers via search synthesis, not a direct table read).

**F3. Direct measurement of exactly the failure observed in this project.**
Inject an identical error, frame it either as user-introduced (external) or model-introduced
(internal), within the same context. Result: **64.5% of tested models corrected the externally
attributed error but failed to correct the identical internally attributed one.** The capability to
detect the error exists; it is **not activated when the error is framed as the model's own**.
Source: "Self-Correction Bench: Uncovering and Addressing the Self-Correction Blind Spot in LLMs",
[arXiv:2507.02778](https://arxiv.org/html/2507.02778), 2025. Accessed 2026-08-31. Confidence: medium —
search-snippet level; the 64.5% figure is reported-but-not-verified-in-detail.

**F4. A companion paper attributes the failure to a chat-template artifact, not a reasoning deficit.**
Claims the model "retains the capability to check the claim and often re-derives the right answer
silently, but has no learned way to act on a thought-internal substring as a discrete object" — the
conversational role structure suppresses explicit flagging in-context.
Source: "The Self-Correction Illusion: Role Relabeling Gates Explicit Error Flagging in LLMs",
[arXiv:2606.05976v2](https://arxiv.org/html/2606.05976v2), 2026. Accessed 2026-08-31. Confidence:
**low-medium** — snippet only. Treat as a lead, not a settled finding.

**F5. Self-preference bias is measured, and it scales with self-recognition.**
GPT-4 self-recognition accuracy **73.5%** (distinguishing its own outputs from others') on
summarization (XSUM, CNN/DailyMail, ~1,000 articles each). A linear correlation was measured between
self-recognition capability and strength of self-preference bias; fine-tuning on ~500 examples pushed
self-recognition **above 90%** and correspondingly **strengthened** self-preference. Weaker models
(Llama 2) could not distinguish their own outputs at all.
Source: Panickssery et al., "LLM Evaluators Recognize and Favor Their Own Generations",
[NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/7f1f0218e45f5414c79c0679633e47bc-Abstract-Conference.html).
Accessed 2026-08-31. Confidence: medium (via secondary summary; correlation coefficient unconfirmed).

**F6. A separately trained critic model beats both self-critique and paid human reviewers.**
On code with naturally occurring LLM errors, model-written critiques were preferred over human
critiques in **63%** of cases; on code with deliberately inserted bugs, **over 80%**. Human evaluation
found the critic caught more bugs than human contractors paid for code review.
**Crucial caveat:** CriticGPT is a *separately RLHF-trained critic model*, trained on inserted-mistake
examples — not the same model self-checking in the same context. This is evidence for "a different,
purpose-built checker helps", **not** for intrinsic self-checking.
Source: McAleese et al. (OpenAI), "LLM Critics Help Catch LLM Bugs",
[PDF](https://cdn.openai.com/llm-critics-help-catch-llm-bugs-paper.pdf), 2024-06/07. Accessed
2026-08-31. Confidence: medium-high.

## Contradictions

**1. Does self-critique ever help without external feedback?** F1 says no and shows prior positives
depended on oracle labels; F2 reports ~20% average gains from the same loop shape.

Not fully reconciled by what was read this run. They differ in **task type** — Self-Refine's biggest
wins are generative/stylistic (dialogue, readability, sentiment, constrained text) while Huang et al.
test *reasoning* benchmarks with ground-truth correctness — and in **evaluation method** (preference
judgments of quality vs. binary correctness). The plausible reading is that self-critique polishes
subjective output where "better" is a matter of degree, but does not fix factual or logical errors
where correctness is binary. **This reconciliation is inferred from the two papers' scopes, not stated
by any source read this run.**

**2. Can a model detect its own errors at all, in principle?** F3/F4 suggest the capability is latently
present but *gated by how the error is framed* — self-attributed errors go uncorrected while identical
externally attributed ones get fixed. That is a more specific claim than "cannot self-correct", and if
it holds, the same-turn rule violation seen in this project is an **activation/framing** problem rather
than a capability gap — which points at different remedies. Unresolved: F3/F4 verified only at snippet
level.

## Leads worth chasing

- **TACL survey**, "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of
  Self-Correction of LLMs" — peer-reviewed, organizes the conditions under which self-correction does
  and does not work. Likely the single best source to settle contradiction #1.
  [direct.mit.edu/tacl/…/tacl_a_00713](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00713/125177/When-Can-LLMs-Actually-Correct-Their-Own-Mistakes)
- Full reads of **Self-Correction Bench** and **Self-Correction Illusion** — both directly on-point for
  the exact symptom here, both currently medium/low confidence.
- **Constitutional AI** (Bai et al.) — named in the brief, not reached. Relevant because it is the
  middle case: self-critique against a *written* constitution, between pure intrinsic correction and
  full external feedback.
- **Multi-agent debate** (Du et al.) own reported deltas — only Huang et al.'s comparative claim was
  retrieved.
- The **same-context vs. fresh-context** comparison — the most decision-relevant sub-question and the
  thinnest one verified.

## What I looked for and could NOT find

- **A clean controlled comparison on the identical model**: "same model, same context, self-checks" vs.
  "same model, fresh context, checks its own prior output" vs. "different model checks", all three
  reported side by side. Strong circumstantial evidence exists (F3's attribution framing, F6's
  separate-model result) but no single paper running that experiment was found.
- **Sample sizes and confidence intervals** for the 2025/2026 papers (F3, F4) — topline percentages
  only.
- **Constitutional AI's own measured numbers** — pure gap, not investigated.
- **Debate-specific effect sizes** from the original paper.
- **Any large-scale meta-analysis or replication** aggregating self-correction results under one
  metric — the TACL survey may be it, unread.
