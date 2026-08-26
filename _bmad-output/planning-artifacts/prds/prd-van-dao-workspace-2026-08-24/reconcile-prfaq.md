# Input Reconciliation — PRFAQ vs PRD

**PRD:** `_bmad-output/planning-artifacts/prds/prd-van-dao-workspace-2026-08-24/prd.md`
**Source input:** `_bmad-output/planning-artifacts/prfaq-van-dao-workspace.md` (Working Backwards PRFAQ, stage 5-verdict, complete)
**Date:** 2026-08-25

## Method

Read both documents in full. Walked every Customer FAQ answer, every Internal FAQ answer, the Verdict (Forged in steel / Needs more heat / Cracks in the foundation), and the Press Release body against the PRD's Vision, §2 Users, §3 Terminology, §4 Features (FR list), §5 Non-Goals, §6 MVP Scope, §7 Success Metrics, §8 Open Questions, §9 Assumptions Index — looking for (a) promises/claims with no corresponding FR/Non-Goal/Open Question, (b) qualitative signal the FR-list structure tends to flatten (tone, hedges, caveats), and (c) direct contradictions.

## Clean matches (no gap — listed briefly so it's clear these were checked, not skipped)

- NotebookLM/quiz-vs-vận dụng differentiation → FR2, FR5, FR8, FR9a-c. Consistent.
- "Không hứa Socratic tốt hơn, chỉ hứa cổng kiểm chứng" → PRD Assumptions Index row on FR2-FR5 explicitly cites "PRFAQ Customer FAQ đã tự nhận câu hỏi học thuật này chưa ngã ngũ." Consistent, well-threaded.
- Platform lock-in ("chỉ chạy Claude Code, đang cân nhắc mở rộng") → Non-Goal #6 + Open Question #1, same hedge level ("chưa quyết" / "đang cân nhắc"), same owner/reopen condition. Consistent.
- Dreyfus / cảnh giới not proven, gated by κ ≥ 0.6 and 20 samples → FR15, FR17, FR18, FR19, and Open Question #2. Consistent, PRD adds precision (0.6, ≥20) the PRFAQ left qualitative ("đủ cao") — elaboration, not contradiction.
- No telemetry / local-only storage → Non-Goal #3, matches Customer FAQ data-privacy answer and Verdict's "Forged in steel" #2.
- Cờ bất đồng (disagreement flag): not blocking, not hidden, no push notification → FR10a/FR10b match Customer FAQ "chấm sai" answer closely, including "không chặn."
- BABOK / non-programming books supported → PRD §2 explicitly lists "phân tích nghiệp vụ" and cites BABOK-adjacent framing; matches Customer FAQ answer.
- "Không ước lượng thời gian" dev-timeline discipline (AGENTS.md rule cited in Internal FAQ) → PRD §6 explicitly preserves this ("Vòng ... không phải mốc thời gian ... không phải cam kết 'xong trong X tuần'"). Consistent.
- n=1 / persona not externally confirmed → PRD §2 states this baldly ("Người dùng được xác nhận duy nhất tính tới bản đầu là chính tác giả... chưa có xác nhận từ người dùng thứ hai nào") and Assumptions Index row 6. This actually answers Verdict's "Needs more heat" #3 (persona imagined, not confirmed) reasonably well.
- Two foundational unproven assumptions (model grades correctly / model reads cảnh giới from text) → Open Question #2 + Assumptions Index rows 2 & 6, and Verdict's "Cracks in the foundation" #2. Consistent, well-threaded through both docs and into the spec doc.
- "Người" → "AI agent" wording discipline (coaching note, Stage-post-Verdict) → PRD FR8, FR9a-c consistently say "AI"/"tiến trình AI," never personifies grader as "người" except FR18's calibration step, which correctly needs a literal human rater ("người chấm tay") for κ ground-truth — same distinction PRFAQ's own Dreyfus answer makes ("cả AI và một người có chuyên môn"). Not a contradiction.

## Gaps found

### 1. Verdict's single most serious "crack in the foundation" — no external demand validation — has no PRD counterpart

The Verdict's "Cracks in the foundation" section ranks three items; the third is explicitly framed as unresolved, not just risky: *"'Giải pháp đi tìm vấn đề' — chưa được bác bỏ, chỉ được trả lời bằng lý lẽ, không phải bằng chứng ngoài... chưa có một người thật, không phải người tạo, đọc thông cáo này và phản ứng."* The Verdict's closing recommendation reinforces this as an action item, not background color: *"đừng đợi tới bước 8 mới hỏi một người thật (không phải bạn) có đọc xong thông cáo này mà muốn dùng không — càng sớm càng rẻ."*

The PRD's Open Questions (§8) contains exactly two items: platform lock-in and grading-calibration confidence. Neither is this one. The Assumptions Index (§9) comes closest with "n=1 là ràng buộc thật, không phải khiêm tốn," but that row is scoped narrowly to a downstream risk ("Người dùng thứ hai với nhu cầu khác có thể đòi điều chỉnh giả định 'đủ dữ liệu' ở Định hướng/Đo") — it does not capture the Verdict's actual concern, which is about product-market validation ("giải pháp đi tìm vấn đề"), not data sufficiency for a specific feature.

This is a genuine drop: the PRFAQ's own verdict treats this as the top foundational risk and gives it an explicit next action; the PRD's structured gates (Open Questions / Assumptions) never captured it.

### 2. Supportive Information phase — Verdict flagged it as "chưa có thiết kế," PRD absorbs it silently

Verdict "Needs more heat" #1: *"Pha Supportive Information (tóm lược trước Socratic) mới chỉ là ý tưởng đúng hướng, chưa có thiết kế... Cần thiết kế thật trước khi viết vào đặc tả, không chỉ nhắc trong PRFAQ."* Stage-1 coaching notes go further: *"Đây là mở rộng phạm vi kiến trúc thật, chưa thiết kế — việc cần làm sau khi PRFAQ xong, không phải trong 34 requirement hiện có."*

The PRD's Vision and FR1/FR2 quietly treat this as settled — FR1 requires the system to "giải nghĩa được ý và nội dung cơ bản" and FR2 requires each idea to close with a question, i.e., explain-then-ask is baked into the FR list as if the design question were closed. FR4 (scaffolding co giãn theo cảnh giới) is adjacent but is explicitly about hint level *during* questioning, not the up-front explanation phase's own scaling — the PRFAQ notes tie that scaling to "§7.1 giàn giáo dày lên giữa chừng" as a *hoped-for* reuse, not a confirmed design.

No Open Question, Non-Goal, or Assumption in the PRD flags that this phase's design is still open. Given the PRFAQ explicitly called this out as a real gap needing resolution before it goes into a spec, its complete disappearance from the PRD's tracking sections is a real reconciliation gap — not just a nice-to-have.

### 3. Press Release promise "cho bạn biết trước sẽ mất khoảng bao lâu, bao nhiêu chương" has no matching FR

"Cách hoạt động" section: *"Vấn Đạo cho bạn biết trước sẽ mất khoảng bao lâu, bao nhiêu chương, trước khi thật sự bắt đầu."* This is a specific, concrete commitment made to the customer, in the section of the PR devoted to describing what literally happens.

FR6 (closest match) only requires that "Lộ đồ (kế hoạch học cả quyển) phải được trình người học duyệt trước khi bắt đầu học" — it does not require the lộ đồ to state an estimated duration. Chapter count is very likely implied by "kế hoạch học cả quyển," but the time estimate is not obviously implied and has no FR anchoring it. Worth either folding an explicit clause into FR6 or adding a line noting it's covered by the Lộ đồ's expected content.

### 4. "Chưa có kế hoạch" for maintenance/first user — Verdict says revisit before onboarding, PRD doesn't track it

Internal FAQ: *"Một mình bạn bảo trì được bao lâu... Không hứa SLA"* and *"Người đầu tiên ngoài bạn biết tới và cài Vấn Đạo bằng cách nào? Chưa có kế hoạch."* Verdict "Needs more heat" #2 explicitly elevates this beyond a throwaway answer: *"Chấp nhận được cho pha hiện tại (trước bước 8), nhưng nếu thật sự 'cho cả người khác' như đã chốt ở Stage 1, đây là việc phải quay lại trước khi mời ai cài thử."*

PRD §2 scopes the product to n=1 for the first release, which somewhat neutralizes the urgency, but the PRD never records the Verdict's actual condition — that distribution/maintenance readiness is a real pending item to revisit *before* inviting a second user, not something already resolved by the n=1 scoping. Open Question #1's reopen condition ("khi có nhu cầu thật từ người dùng thứ hai") is adjacent but is about the platform-lock-in decision specifically, not about maintenance/support readiness. Minor compared to #1 and #2 above, but a real dropped commitment.

### 5. (Minor / terminology note, not a hard contradiction) Headline scope "người tự học kỹ thuật" vs. PRD's broader Tâm pháp/BABOK scope

The PR headline and subhead both say "người tự học kỹ thuật" (technical self-learners). The PRD §2 deliberately broadens this to include "năng lực nền dùng được ở mọi vai (tư duy, giao tiếp, dẫn dắt...)" and explicitly names phân tích nghiệp vụ/BABOK as in-scope — which actually matches the PRFAQ's own Customer FAQ answer ("Vấn Đạo không giới hạn theo ngành") rather than its headline. This is a pre-existing tension inside the PRFAQ itself (headline narrower than FAQ), and the PRD resolves it toward the more authoritative FAQ answer — a defensible choice, not an error. Flagging only so the drift from the headline's literal wording is a documented, deliberate choice rather than an silent one.

## Summary

4 real gaps (1-4), 1 minor terminology note (5). None are contradictions the PRD got wrong — all are cases of the PRFAQ recording a qualitative signal (a verdict-level risk, a flagged-as-undesigned mechanism, a concrete promise, a "revisit before X" condition) that the PRD's FR/Non-Goal/Open-Question structure did not carry forward. Recommend either adding two Open Question rows (external validation / "giải pháp đi tìm vấn đề", and Supportive Information design status) and a small clause to FR6 or its Ghi chú, plus a short Assumptions Index or Open Questions note on distribution/maintenance readiness before onboarding a second user.
