# D1 · Techniques that give a soft constraint an external oracle — round 1, assistant 1

Budget spent: 11 tool calls, 8 sources. Returned 2026-08-31.

## Findings

**1. LLM-judge agreement with humans is far weaker than raw accuracy suggests.**
21 LLM judges, ~541,000 judgments across MT-Bench, JudgeBench, RewardBench. Chance-corrected
agreement (Cohen's κ): 0.376–0.511 (MT-Bench), 0.271–0.875 (JudgeBench), 0.616–0.898 (RewardBench).
Raw exact-match accuracy **overstated true discriminative ability by 33.8–41.3 percentage points**
("kappa deflation").
Source: [arXiv:2606.19544v1](https://arxiv.org/html/2606.19544v1) — "Reliability without Validity: A
Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models", Norman, Rivera, Hughes (UC Berkeley),
2026-06-17. Accessed 2026-08-31. Confidence: high. Class: primary empirical.

**2. High reproducibility coexists with severe position bias.**
Test-retest reliability averaged 0.943 on MT-Bench, 0.911 on harder benchmarks — but position-flip
rate (verdict changes when response order is swapped) averaged 9.9% on MT-Bench, rising to 17.3% on
JudgeBench; bias up to 0.192 in cost-optimized models. Judge rankings shift by up to **14 positions**
across benchmarks.
Source: same as #1. Confidence: high.

**3. The authors' own protocol for using a judge as a semi-reliable oracle.**
Report κ (not raw accuracy) as the primary metric; measure position bias via position-swapped runs;
validate across ≥2 benchmarks with different label structures; audit consistency and bias jointly —
either metric alone is misleading.
Source: same as #1. Confidence: high (the paper's stated recommendation, not extrapolation).

**4. A second paper corroborates directionally, but its numbers could not be extracted.**
"Coin Flip Judge" reports low inter-rater agreement with human baselines, high variance on identical
repeated inputs, and position/majority bias.
Source: [arXiv:2606.13685v1](https://arxiv.org/pdf/2606.13685), Abel Yagubyan, 2026-06. Accessed
2026-08-31. Confidence: **low** — PDF text did not parse; abstract-level gloss only, single author,
unclear venue. Directionally corroborating #1–2, not independent numeric evidence.

**5. Metamorphic testing tests systems that have no ground-truth oracle.**
Metamorphic relations (MRs) define expected relationships between outputs of related/perturbed
inputs, instead of requiring a known-correct answer per input. CheckList operationalises this with
Invariance and Directional Expectation test types.
Source: [arXiv:2511.02108](https://arxiv.org/abs/2511.02108). Accessed 2026-08-31. Confidence: medium
(search-snippet level; abstract not independently fetched).

**6. Strongest direct evidence in this dimension: metamorphic testing works on TEXT artifacts, with
measured numbers.**
MTTM applies 11 metamorphic relations at character/word/sentence perturbation levels to toxic text
and measures error-finding rate (EFR) against production moderation systems: Google **83.9%**, Huawei
**82.5%**, Baidu **51%**, best academic algorithms up to **91.2%**. Retraining on MTTM-generated cases
cut EFR to **0%–5.9%** while preserving accuracy on the original test set.
Source: [arXiv:2302.05706](https://arxiv.org/abs/2302.05706) — "MTTM: Metamorphic Testing for Textual
Content Moderation Software", Wang et al., **ICSE 2023**. Accessed 2026-08-31. Confidence: high —
concrete numbers, peer-reviewed venue, target is text classification not code.

**7. Structural invariants on the artifact, measured.**
LEDGER builds an explicit dependency graph over document structure (hierarchy, explicit references,
implicit dependencies, semantic relations) and validates edited nodes against it — checking reference
integrity (do referenced targets still exist after the edit) and terminology consistency (do dependent
nodes still match changed terms). Result: consistency **56% → 76%** across six models.
Source: [arXiv:2606.28379v1](https://arxiv.org/abs/2606.28379) — "LEDGER: Scaling Agentic Document
Editing with Dependency-aware Graph Retrieval", Wang et al., 2026-06-30. Accessed 2026-08-31.
Confidence: medium — headline number from the abstract; the methodology section (which invariants
exactly, how "consistency" is defined) could not be extracted this run.

**8. Self-consistency has a blind spot that does not shrink with scale.**
Sampling the same generation repeatedly and comparing outputs detects content that varies — but
**self-consistent errors** exist: when a model reliably produces the same wrong answer every time,
sampling-based self-consistency is blind to it, and this blind spot does not shrink with model scale.
Source: [arXiv:2505.17656](https://arxiv.org/pdf/2505.17656) — "Too Consistent to Detect: A Study of
Self-Consistent Errors in LLMs". Accessed 2026-08-31. Confidence: medium (abstract via search, not a
direct read).

## Contradictions

**Vendor optimism vs. measured pessimism on judge/human agreement.** A LangChain resource claims
"strong LLM judges reach ~80% agreement with human evaluators, roughly the level humans reach with
each other" (vendor blog, not independently fetched, confidence low, marketing-adjacent register).
This sits against finding #1: chance-corrected κ on JudgeBench dropped as low as **0.271**.

The two are not strictly incompatible — raw exact-match agreement genuinely can reach ~80% on some
label distributions — but the vendor framing elides exactly the kappa-deflation effect the primary
paper identifies as the central pitfall. Citing raw "80% agreement" without chance-correction **is**
the specific mistake #1's authors warn against.

## Leads worth chasing

- **LLMORPH** — 36 metamorphic relations across multiple NLP tasks using LLM-based transformations to
  uncover faulty behaviour at scale without labeled data. Could generalise MTTM beyond moderation to
  prose-quality or spec-compliance rules.
- **CheckList** Invariance / Directional Expectation types — a template for expressing "perturb the
  input this way, the judged property should/should not change" as a deterministic pass/fail over
  text. Exactly the shape needed here. Worth a primary read.
- **LEDGER's actual invariant catalog** — the closest published thing to "invariant checking on the
  artifact"; methodology section not yet extracted.
- **MetaRAG** — metamorphic testing for hallucination detection in RAG.
- **Cross-model differential testing** — the search surfaced only *same-model* resampling. Running the
  same task on two different models and diffing was not evidenced this run; needs its own search.

## What I looked for and could NOT find

- **No study measuring LLM-as-judge reliability for judging coding-agent constraint compliance**
  ("did the agent follow instruction X in this diff"). All retrieved judge data is general
  response-quality benchmarking. Applicability to this use case is **inferred, not evidenced**.
- **No general named technique for "turning a subjective rule into a deterministic check"** outside
  the specific instances of metamorphic testing and structural-invariant validation. Nothing under
  framings like "oracle synthesis for subjective criteria" or "operationalizing style guides as tests".
- **Property-based testing for documents as a tradition distinct from metamorphic testing** — search
  collapsed the two; neither confirmed nor ruled out.
- **Numbers for the Coin Flip Judge paper** — PDF unparseable twice.
- **Cross-model / cross-ordering differential testing with measured FP/FN rates** — not found. Only
  same-model resampling, and that with a documented blind spot (#8).
