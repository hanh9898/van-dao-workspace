# Input Reconciliation: prfaq-van-dao-workspace-distillate.md → prd.md

Source input: `_bmad-output/planning-artifacts/prfaq-van-dao-workspace-distillate.md`
Target: `_bmad-output/planning-artifacts/prds/prd-van-dao-workspace-2026-08-24/prd.md`

Method: read both files in full; walked the distillate section by section; for each
bullet, located where (if anywhere) it lands in the PRD — a Feature/FR, a Non-Goal, an
Open Question, or an Assumption — per the Finalize step 2 instruction. Special attention
given to the distillate's "Cracks in the foundation" list against PRD §8 Open Questions.

## Section-by-section trace

### Sản phẩm là gì
- Plugin (not "skill") terminology fix → PRD §1 Vision, line 1: "Vấn Đạo là một plugin
  Claude Code…" ✓ Landed.
- Concept type (open-source, personal, no multiplayer/SaaS/unit-economics) → PRD §1 last
  paragraph + Non-Goal #5 ✓ Landed (unit-economics framing implicitly honored by absence
  of any growth/revenue metric in §7).

### Persona đã chốt
- "Dev chuyển hướng BA, hai nhu cầu nối tiếp" → generalized in PRD §2 to "người tự học…
  vai cụ thể… hoặc năng lực nền" — an intentional broadening (PRD frames the product as
  usable beyond the author's own job transition), not a drop. Acceptable generalization.
- "Persona tự suy luận, chưa xác nhận — unknown lớn nhất" → PRD §2: "Người dùng được xác
  nhận duy nhất… là chính tác giả (n=1)… chưa có xác nhận từ người dùng thứ hai nào." ✓
  Landed as a stated caveat, though not elevated to an Open Question (see Gap 1 below,
  which covers the sharper, PRFAQ-level version of this same unknown).

### Requirements signal (Supportive Information phase)
- The directional fix ("không tóm tắt/giảng, chỉ hỏi" → "giải thích đủ rồi mới hỏi sâu")
  landed in PRD §1 Vision paragraph 2 and underlies FR2. ✓
- **But** the distillate is explicit that the Supportive Information phase itself is
  *"Chưa thiết kế — việc cần làm trước khi đưa vào đặc tả, không phải trong 34
  requirement hiện có"* — i.e., only the directional insight should carry forward now;
  the fact that it still needs dedicated design work (placement in F-flow, scaling rule
  tied to cảnh giới, per §7.1 rule 3) was flagged as unfinished business. That
  "still-undesigned, still-needed" status does not appear anywhere in the PRD — not in
  Open Questions, not in Assumptions, not as a caveat in §4.2 Dạy or §6 MVP Scope. FR6/FR7
  cite F-1 and F0 directly with no note that a pre-Socratic explanation step is still
  unspecified. → **Gap 3.**

### Chưa giải quyết — cần quyết định kiến trúc riêng
- Model-agnostic vs Claude-Code-only "crack" → PRD §8 Open Question #1, verbatim in
  substance (cites the same tension between Non-Goals §5.6 "chưa quyết" and the
  Claude-Code-coupled architecture). ✓ Landed, well captured.
- Caution against reusing the book-to-skill/BMAD example to justify lock-in → no PRD
  statement contradicts this; Non-Goal #6 doesn't lean on that example. Consistent by
  omission — not a gap.

### Kỹ thuật / phụ thuộc
- book-to-skill as a real, MIT-licensed, unpinned dependency → not mentioned in PRD.
  Judged out-of-scope for a PRD (implementation/dependency detail, not a product
  decision) — not counted as a gap.
- "Nền kỹ thuật đã xong… còn thiếu push remote" → infra/project-status detail, not
  product-decision content. Not counted as a gap.
- **Hai giả định nền chưa kiểm** (model chấm đúng theo rubric; model đọc đúng cảnh giới)
  — distillate calls these the single highest, unchanging risk of the whole PRFAQ.
  PRD's own Assumptions Index (§9) claims: *"Mục 2 và 3 của bảng đó (model chấm theo
  rubric, model đọc cảnh giới) đã lên Open Questions §8."* Checking §8: Open Question #2
  is entirely about grading/rubric calibration (FR8-FR10 running uncalibrated through
  Vòng 1-3). It does not discuss the second assumption — the model correctly reading
  proficiency level (cảnh giới) from a learner's text — at all. That assumption is only
  indirectly deferred by FR14-FR19 being pushed to Vòng 4 (gated by FR18's own
  calibration requirement). So the Assumptions Index's claim that *both* items reached
  §8 is not accurate — only one did. → **Gap 2.**

### Cạnh tranh
- NotebookLM baseline → PRD §2 ✓.
- book-to-skill differentiation ("hệ tra cứu thuần, không quiz/Socratic") → echoed in
  spirit by PRD §1's "cấu trúc kiểm chứng" differentiation claim. ✓ (not verbatim, but a
  PRD is expected to synthesize competitive findings into positioning, not enumerate
  every competitor by name).
- claude-tutor / AI-learning-skill (general-topic competitors) → not named, but the
  "single book, not general topic" differentiator is present via §2 and glossary. ✓
  synthesized.
- Book2Course V2 HN feedback ("template-like, quiz hời hợt, thiếu chiều sâu" — evidence
  the problem is hard) → not cited by name, but the underlying risk (AI pedagogy may not
  transfer as well as hoped) is captured in PRD §9 Assumptions Index row 2: "Kỹ thuật sư
  phạm được kiểm chứng cho người dạy là con người (FR2-FR5) sẽ chuyển tốt sang AI dạy qua
  văn bản… hiệu quả học thực tế thấp hơn kỳ vọng." Close enough in substance — not
  counted as a gap.
- "Khoảng trống thời cơ hẹp, không rộng" → implicit in the honest, unhyped framing
  throughout (n=1, no adoption plan). Not counted as a gap.
- "Risk of being a solution in search of a problem" (Dreyfus self-assessment demand
  unproven) + "Socratic AI tutoring hiệu quả chưa ngã ngũ" → the academic-validity half
  lands in PRD §9 row 2 ("PRFAQ Customer FAQ đã tự nhận câu hỏi học thuật này chưa ngã
  ngũ") and FR17 (Dreyfus framed as unvalidated hypothesis, citing Gobet & Chassy 2009).
  The narrower "nobody has confirmed real demand for Dreyfus self-assessment" angle is
  not separately called out, but it's substantially the same risk as the
  persona-unconfirmed caveat in §2/§9 row "n=1 là ràng buộc thật". Judged adequately
  covered, not a standalone gap.

### Scope — trong/ngoài
- `phuc-khao` Bậc-1/Vòng-2 correction → PRD §6 explicitly narrates this exact correction
  ("nhãn Bậc từng lệch với Vòng một lần (trường hợp phuc-khao)") and FR9a-c/FR10a-b are
  placed correctly in MVP. ✓ Well landed, including the meta-lesson about not using Bậc
  to cut MVP.
- Out-of-scope: truong-lao/κ-calibration/thoai-canh.py/canh-gioi.md (needs ≥2 sources) →
  PRD §6 Vòng 4 table, FR14 "≥2 nguồn". ✓
- Out-of-scope: all of Bậc 2 (ha-son, phuc-menh, đạo tâm multi-mach, tra-tang-kinh-cac,
  ban-do.py) → PRD §6 Vòng 3 table (FR22, FR28, FR29). ✓
- Supportive Information "chưa scope hoá" → see Gap 3 above (same underlying issue).

### Timeline / resource
- "Không ước lượng số, chỉ chuỗi phụ thuộc" → PRD §6 explicitly states Vòng is a
  dependency chain, not a time commitment. ✓
- Build-order chain (bước 3→4→5+5b→6→7→8) → reflected via §16-step citations throughout
  §4 and §6. ✓
- **Bảo trì: không hứa SLA, best-effort, mã nguồn mở cá nhân** + **"Phân phối/người dùng
  đầu: chưa có kế hoạch — thành thật, chưa nghĩ tới"** (also listed as a "Needs more
  heat" action item: "Kế hoạch tối thiểu cho người dùng đầu tiên/bảo trì, nếu thật sự mở
  cho người khác như đã chốt") → Not present anywhere in the PRD. Given the PRD commits
  to the product being open-source and independently installable by others (§1, §2), the
  complete absence of any maintenance-expectation statement (no SLA / best-effort) or
  open question about a first-user/distribution plan is a real omission. → **Gap 4.**

### The Verdict
- Forged in steel (3 items) → all reflected: differentiation (§1), data/privacy
  (Non-Goal #3), Dreyfus-as-discipline (FR14-19, R11 reference). ✓
- Needs more heat:
  1. Supportive Information design → **Gap 3**.
  2. Minimum first-user/maintenance plan → **Gap 4**.
  3. Verify persona with a real person outside the author → partially landed as a
     caveat in §2 and §9 ("n=1 là ràng buộc thật"), but not elevated to an Open
     Question the way its sibling crack-list item is. Folded into Gap 1 below since it's
     the same underlying unresolved-validation issue as Crack #3.
- **Cracks in the foundation** (explicitly named as needing a decision before committing
  more work — the PRD is instructed to check these against Open Questions):
  1. Model-agnostic vs Claude-Code-only → **PRD §8 OQ#1. Landed correctly.**
  2. Hai giả định nền chưa kiểm → **partially landed** (grading half only — see Gap 2).
  3. **"Chưa có người thật (không phải tác giả) đọc thông cáo và phản ứng — toàn bộ
     Customer FAQ là tự vấn tự đáp"** → **not landed as an Open Question.** PRD §8 has
     exactly two Open Questions (platform choice, calibration gap); neither addresses
     the fact that no one outside the author has yet reacted to the pitch/PRFAQ. §2's
     "chưa có xác nhận từ người dùng thứ hai nào" is a weaker, generic echo — it notes
     the persona is unconfirmed but doesn't carry forward the distillate's specific
     framing that this is a foundation-level risk requiring resolution before further
     investment. → **Gap 1 (highest-priority finding).**
- Khuyến nghị cuối (đi bước 3; get real-person reaction early) → process advice for the
  author, not PRD content. N/A.

### Review lens naive-reader (post-Verdict)
- 9 mechanical PRFAQ fixes + epigraph translation → upstream document fixes, not
  PRD-relevant. N/A.
- Language decision "người dạy/người chấm" → "AI/AI agent" → PRD honors this
  consistently: Vision uses "một AI tách biệt với AI vừa dạy", FR8 says "hai tiến trình
  AI tách biệt". The Tám Vai role names (Thư linh, Giám khảo, etc.) are fantasy labels
  for AI roles, not claims of human involvement, and are used consistently with "AI"
  language elsewhere. ✓ Landed.
- The phuc-khao Bậc-3→Bậc-1 finding → already covered above under Scope. ✓

## Gaps found

1. **Crack in the foundation #3 — no real-person validation of the pitch — is missing
   from Open Questions.** The distillate names this as one of three items that "phải
   quyết định trước khi commit thêm" (Customer FAQ is entirely self-authored/self-
   answered, no outside reaction obtained yet). PRD §8 Open Questions has only two items
   (platform choice; calibration gap during MVP) — neither is this one. PRD §2 has a
   related but softer statement ("chưa có xác nhận từ người dùng thứ hai nào") that
   reads as a persona caveat, not as a flagged foundational risk requiring resolution.
   Recommend adding a third Open Question capturing this, or explicitly folding it into
   existing Assumptions with an owner/revisit-condition, per the pattern PRD §8 already
   uses for OQ#1 and OQ#2.

2. **Assumptions Index (§9) overstates where the "model reads cảnh giới correctly"
   assumption landed.** §9 says both the grading-rubric assumption and the
   proficiency-reading assumption "đã lên Open Questions §8," but §8 OQ#2 discusses only
   the grading/rubric half (FR8-FR10 running without calibration through Vòng 1-3). The
   "model correctly infers proficiency level from learner text" assumption has no
   dedicated discussion in §8 — it's only implicitly deferred via FR14-FR19 living
   entirely in Vòng 4. This is an internal accuracy issue in the PRD's own
   cross-reference, traceable back to the distillate's "hai giả định nền chưa kiểm…
   rủi ro cao nhất" pairing not being carried through symmetrically.

3. **Supportive Information phase's "still undesigned, needs work before spec" status
   isn't flagged anywhere in the PRD.** The distillate is explicit that only the
   directional insight ("explain then question") should carry forward now — the phase
   itself needs dedicated design (placement in F-flow before F0, scaling rule tied to
   cảnh giới, 4C/ID framework) before it can become a real FR. The directional insight
   did land (PRD §1 Vision, FR2), but nothing in §4 Features, §6 MVP Scope, §8 Open
   Questions, or §9 Assumptions notes that this pre-Socratic explanation step is still
   unspecified in the F-flow. A reader of the PRD alone would not know this design gap
   exists.

4. **No maintenance/distribution-plan statement or open question, despite the PRD
   committing to open-source availability for other users.** The distillate states
   plainly: "Bảo trì: không hứa SLA, best-effort, mã nguồn mở cá nhân" and "Phân
   phối/người dùng đầu: chưa có kế hoạch — thành thật, chưa nghĩ tới," and separately
   lists a minimal first-user/maintenance plan as a "Needs more heat" action item. The
   PRD (§1, §2) affirms the product will be open-source and independently installable,
   but says nothing about maintenance expectations or the absence of a distribution
   plan — this doesn't appear in Non-Goals, Open Questions, or Assumptions.

## Items intentionally not counted as gaps

- book-to-skill dependency details (license, pinning) — implementation-level, not
  product-decision content expected in a PRD.
- Named individual competitors (claude-tutor, AI-learning-skill, Book2Course V2) — PRD
  synthesizes competitive findings into positioning rather than listing every source;
  the underlying risks these evidence (pedagogy-transfer risk, market-gap narrowness)
  are captured elsewhere in Assumptions/Vision.
- Persona narrowed from "dev chuyển hướng BA" to general "người tự học" — read as a
  deliberate, reasonable broadening for an open-source plugin, not a dropped decision.
- Verdict's closing recommendation ("đi bước 3… đừng đợi tới bước 8") — process advice
  for the author's next action, not PRD subject matter.
