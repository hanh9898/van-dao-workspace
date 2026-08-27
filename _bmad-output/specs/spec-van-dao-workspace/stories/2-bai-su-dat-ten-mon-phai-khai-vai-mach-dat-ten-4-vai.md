---
title: 'Bái sư — đặt tên môn phái, khai vai/mạch, đặt tên 4 vai'
type: 'feature'
created: '2026-08-27'
status: 'done'
baseline_revision: 'b6ccdf9204a6ede6c2feceaec22805db74b5c291'
review_loop_iteration: 1
followup_review_recommended: true # patch mức high (/vd: → /van-dao:) trong pass này — xem Review Triage Log
context:
  - '{project-root}/AGENTS.md'
warnings: ['oversized'] # 1439 từ tiếng Việt (dấu) — story phức tạp hơn 1.1 thật (thêm 1 skill mới + nhánh vai/mạch), không nén thêm được mà không mất rõ ràng
deferred:
  - summary: >-
      Không có script/CI nào tự chạy lại evals.json — một hồi quy tương lai vào bái sư (nhap-mon)
      hay nhap-mon-ky sẽ không bị bắt tự động.
    evidence: |-
      Verification Gap reviewer xác nhận: kiem.yml chỉ chạy pytest tests/ (không đụng skills/); không
      script/hook nào tham chiếu evals.json. Cùng lớp finding đã defer từ Story 1.1, nay lan sang
      story này — recurring, không phải mới.
    severity: medium
  - summary: >-
      Cơ chế disable-model-invocation của nhap-mon-ky mới được test ở mức "AI tự nguyện từ chối bằng
      lời" (2 eval), chưa test được liệu Claude Code có THẬT SỰ chặn ở tầng nền tảng nếu AI không tự
      giác từ chối hay không.
    evidence: |-
      2 reviewer độc lập (Intent Alignment, Verification Gap) cùng phát hiện: eval id 8/9 đều là AI
      từ chối trong hội thoại (compliance layer), không phải một phép thử ép nhap-mon tự gọi
      nhap-mon-ky qua cơ chế thật để xem platform có chặn không (mechanism layer).
    location: 'van-dao/skills/nhap-mon-ky/SKILL.md'
    severity: medium
  - summary: >-
      Chưa có tham-chieu/*.schema.md cho ho-so.json và nhap-mon-ky.md — hình dạng field
      (ten_mon_phai, vai, mach, mach_nguon, ten_vai) chỉ ghi ở dạng văn xuôi trong 2 SKILL.md.
    evidence: |-
      Verification Gap reviewer: repo có tiền lệ bi-kip.schema.md đi cặp kiem-bi-kip.py, nhưng
      ho-so.json/nhap-mon-ky.md chưa có script đọc/ghi tất định nào để đi cặp — không có consumer
      để chứng minh regression ngay, nhưng hình dạng cũng không được ghi ở đâu chống trôi trong
      tương lai.
    severity: low
  - summary: >-
      Một số edge case đầu vào chưa có hướng dẫn tường minh trong SKILL.md: chuỗi rỗng/toàn khoảng
      trắng cho tên môn phái/vai/mạch, hai vai trùng tên, ký tự đặc biệt cần escape khi ghi JSON, và
      nhánh "đã biết" khi người học chỉ khai vai mà không khai mạch (hoặc ngược lại).
    evidence: |-
      Edge Case Hunter liệt kê ~10 finding thuộc nhóm này. Rủi ro thấp ở mức "nhẹ" (LLM tự xử lý hợp
      lý phần lớn ca này dù không có luật viết ra), nhưng đáng quay lại khi có báo cáo thật về hành vi
      sai ở các ca biên này.
    severity: low
  - summary: >-
      Không có đường sửa vai/mạch/tên 4 vai sau khi đã ghi (chỉ tên môn phái có hướng dẫn đổi tên rõ
      ràng); cũng chưa có xử lý khi ho-so.json/nhap-mon-ky.md không đọc/ghi được (JSON hỏng, lỗi
      quyền, đầy đĩa).
    evidence: |-
      Blind Hunter + Edge Case Hunter cùng nêu. Thấp ưu tiên ở MVP một người dùng (n=1, tác giả tự
      sửa tay hồ sơ nếu cần) — quay lại khi có người dùng thứ hai hoặc gặp ca thật.
    severity: low
---

<intent-contract>

## Intent

**Problem:** Sau Story 1.1, `/vd:nhap-mon` chỉ kiểm ngôn ngữ giao tiếp rồi dừng — người học chưa có hồ sơ (tên môn phái), chưa khai vai/mạch để hệ biết định hướng, chưa có cam kết nhập môn tự tay ghi, và 4 vai trực tiếp nói chuyện chưa có tên riêng để xưng hô.

**Approach:** Nối tiếp ngay sau Bước 0 trong cùng `nhap-mon/SKILL.md`: đặt tên môn phái → dẫn ghi nhập môn ký qua một skill riêng `disable-model-invocation` (người học tự gõ lệnh, tự viết, hệ không ghi hộ) → khai vai + mạch (nhánh "chưa biết" hỏi VAI trước, suy mạch từ vai kèm cờ nguồn gợi ý) → đặt tên riêng cho 4 vai nói-với-người-học. Nghi thức bái sư chỉ tính là đã kích hoạt khi cả khai-vai/mạch VÀ nhập-môn-ký đều xong.

## Boundaries & Constraints

**Always:** Nghi thức bái sư chỉ coi là kích hoạt khi đủ cả bốn phần: tên môn phái, vai + mạch, tên 4 vai, VÀ nhập môn ký — thiếu bất kỳ phần nào thì bái sư chưa xong, không giả vờ đã xong (đúng khuôn AC "Given ... when hoàn tất bái sư..." bên dưới); nhánh "chưa biết muốn luyện gì" hỏi VAI trước ("ngươi làm nghề gì"), không hỏi mạch trước — mạch là khái niệm của hệ, người mới không trả lời được; "ghi nhập môn ký" nằm ở skill riêng có `disable-model-invocation: true`, chỉ ghi nguyên văn lời người học tự gõ, không được soạn sẵn/viết hộ dù bản AI viết "hay hơn"; chỉ đặt tên cho đúng 4 vai nói-với-người-học (Trưởng môn, Tàng kinh trưởng lão, Thư linh, Giám khảo) — gợi ý sẵn vài tên kèm cho tự nhập, không ép chọn từ danh sách; tên môn phái là một trường trong hồ sơ, không phải tên thư mục — đổi tên không được mất hồ sơ; mọi định danh kỹ thuật tiếng Việt không dấu, kebab-case cho file/id; SKILL.md mới hoặc sửa phải giữ đủ 4 quy ước bắt buộc (§12.4: "Xong khi", "Khi nào skill này không giúp được", trình tự "Trình → xác nhận → ghi → kiểm", bước nạp `customize.toml`) và không trích số hiệu requirement/số mục đặc tả trong nội dung skill (AD-11) — viết lại bằng lời tự nhiên; behavioral eval nhẹ (2-3 kịch bản khớp I/O matrix, evidence trích transcript chạy thật) đi cùng ngay khi viết xong nháp, không hoãn (AD-10).

**Block If:** (không có — phạm vi đã rõ từ SPEC.md CAP-8/CAP-16 và đặc tả §10.0, không có quyết định cần người can thiệp giữa chừng)

**Never:** Không làm đột phá cảnh giới (nghi thức thứ ba, cần cơ chế Đo chưa có ở MVP) — hỏi tới thì trả lời rõ "chưa hỗ trợ ở bản này", không đoán liều; không làm chỉ điểm (gọi tên sách cụ thể) — đó là story kế tiếp, dừng đúng ở "khai vai + mạch"; không đặt tên cho 4 vai chấm/im lặng (Sơn phong trưởng lão, Nghiệm Công Sứ, Phúc Khảo Sứ, Chú Giải Sứ) vì chúng không hiện ra với người học; không dựng sổ đạo tâm đầy đủ (`dao-tam`, story khác) — chỉ dựng đúng cơ chế tự-ghi cho nhập môn ký, dùng chung khuôn `disable-model-invocation` nhưng không dùng chung lý do với đạo tâm (đạo tâm dựa trên sở hữu tâm lý với công sức đã bỏ ra; nhập môn ký dựa trên cam kết viết tay trước khi có công sức nào — hai căn cứ khác nhau, đừng copy nguyên văn lý do của nhau trong bất kỳ văn bản nào); không sửa `van-dao/.claude-plugin/plugin.json`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Lần đầu, đã biết muốn luyện gì | Ngôn ngữ đã xác nhận (Story 1.1), chưa có hồ sơ | Hỏi tên môn phái → dẫn ghi nhập môn ký (lệnh riêng) → hỏi thẳng vai + mạch → đặt tên 4 vai → xác nhận bái sư xong | Không lỗi |
| Lần đầu, chưa biết muốn luyện gì | Như trên, người học nói "chưa biết"/"chưa rõ" | Hỏi VAI trước ("ngươi làm nghề gì"), suy mạch từ vai kèm cờ nguồn gợi ý, xác nhận với người học trước khi ghi | Không lỗi — không tự chốt mạch mà không hỏi lại |
| Đã bái sư xong từ trước | Hồ sơ đã có tên môn phái + vai/mạch + nhập môn ký | Không lặp lại nghi thức — nhận diện đã xong, hướng người học sang bước tiếp theo (chỉ điểm/thu bí kíp) | Không lỗi — không bái sư lại |
| Khai xong vai/mạch nhưng chưa ghi nhập môn ký | Vai/mạch đã lưu, chưa gọi lệnh ghi nhập môn ký | Nghi thức bái sư CHƯA tính kích hoạt — nhắc rõ còn thiếu bước tự ghi, không giả vờ đã xong | Không lỗi — chỉ nhắc, không chặn người học dừng ở đây |
| Hỏi về đột phá cảnh giới giữa lúc bái sư | Người học hỏi lên cấp/cảnh giới | Trả lời rõ "chưa hỗ trợ ở bản này", không đoán liều, không im lặng bỏ qua | Không lỗi |

</intent-contract>

## Code Map

- `van-dao/skills/nhap-mon/SKILL.md` -- nối tiếp Bước 0 (Story 1.1) bằng bước bái sư: đặt tên môn phái, dẫn sang `nhap-mon-ky`, khai vai/mạch, đặt tên 4 vai; cập nhật "Xong khi" cho hết phạm vi mới
- `van-dao/skills/nhap-mon-ky/` (mới) -- skill riêng `disable-model-invocation: true`, chỉ ghi nguyên văn lời người học tự gõ khi tự gọi lệnh
- `docs/VAN-DAO-dac-ta-v1.0.md` §10.0 -- nguồn flowchart bái sư (đọc để bám đúng nhánh, không sửa)
- `_bmad-output/specs/spec-van-dao-workspace/SPEC.md` CAP-8, CAP-16 -- nguồn intent/success của story này
- `_bmad-output/specs/spec-van-dao-workspace/stories/1-thiet-lap-ban-dau-ngon-ngu-giao-tiep.md` -- Story 1.1 liền trước, cùng file `nhap-mon/SKILL.md`, cùng quy ước AD-10/AD-11 vừa áp dụng

## Tasks & Acceptance

**Execution:**
- `van-dao/skills/nhap-mon/SKILL.md` -- thêm bước bái sư nối tiếp Bước 0; kiểm hồ sơ đã có chưa để không lặp nghi thức -- đúng luồng §10.0, tránh bái sư lại cho người học cũ
- `van-dao/skills/nhap-mon-ky/SKILL.md` -- skill mới, `disable-model-invocation: true`, đủ 4 quy ước §12.4 -- tách riêng để đảm bảo không AI nào ghi hộ được (R32/FR22 áp dụng đúng cơ chế, khác lý do)
- `van-dao/skills/nhap-mon/evals/evals.json` -- mở rộng thêm expectation khớp các kịch bản bái sư mới trong I/O matrix, evidence trích transcript chạy thật (AD-10, mức nhẹ)

**Acceptance Criteria:**
- Given người học đã xác nhận ngôn ngữ (Story 1.1) và chưa có hồ sơ, when hoàn tất bái sư, then hồ sơ có tên môn phái, vai, mạch, tên 4 vai nói-với-người-học, và một bản ghi nhập môn ký do chính người học gõ
- Given người học nói "chưa biết muốn luyện gì", when khai vai/mạch, then hệ hỏi VAI trước, suy mạch kèm cờ nguồn gợi ý, và xác nhận lại với người học trước khi lưu
- Given người học đã bái sư xong ở phiên trước, when gọi lại `/vd:nhap-mon`, then hệ không lặp lại nghi thức bái sư
- Given người học đã khai vai/mạch nhưng chưa gọi lệnh ghi nhập môn ký, when hỏi trạng thái bái sư, then hệ trả lời rõ chưa kích hoạt, không giả vờ đã xong

## Review Triage Log

### 2026-08-27 — Review pass

- intent_gap: 0
- bad_spec: 0
- patch: 7 (high 1, medium 2, low 4)
- defer: 5 (medium 2, low 3)
- reject: 3
- addressed_findings:
  - `[high]` `[patch]` `/vd:nhap-mon`/`/vd:nhap-mon-ky` không hoạt động — plugin khai `name: van-dao`,
    tra code.claude.com/docs xác nhận không có cơ chế alias/prefix riêng cho plugin (đã dùng subagent
    claude-code-guide tra cứu độc lập, không đoán). Người điều phối quyết định: bỏ hẳn `/vd:`, dùng
    `/van-dao:*` xuyên suốt. Đã sửa 2 SKILL.md của story này + toàn bộ `docs/VAN-DAO-dac-ta-v1.0.md`
    (35 chỗ) — đóng dứt điểm finding đã defer từ Story 1.1, không defer lần 3.
  - `[medium]` `[patch]` Câu "Always" của chính spec này chỉ nêu 2 điều kiện kích hoạt bái sư (vai/mạch
    + nhập môn ký) trong khi AC #1 và toàn bộ thiết kế đòi đủ 4 phần — sửa lại câu Always cho khớp AC,
    không đổi hành vi (implementation đã đúng theo AC từ đầu).
  - `[medium]` `[patch]` `evals.json` id 10 thực ra là trích lại đúng lượt hội thoại của id 5 (cùng
    session, cùng prompt), trình bày như một kịch bản độc lập gây hiểu nhầm mức độ phủ thật — đã gộp
    thành 1 expectation mới trong id 5, xoá id 10.
  - `[low]` `[patch]` `evals.json` id 5 trích dẫn sai "xem eval id 8" (đúng ra là kịch bản vừa gộp,
    nay đã tự chứa, không cần trích chéo).
  - `[low]` `[patch]` `evals.json` id 9 `matrix_row` trích "AC ..." (định danh chỉ có ở workspace) —
    viết lại bằng lời tự nhiên, đúng tinh thần AD-11 áp cho cả `evals/` (nằm dưới `skills/**`).
  - `[low]` `[patch]` `evals.json` trường `level` ghi sai số kịch bản mới thêm ("2-3 nữa" thay vì 6) —
    sửa cho khớp thực tế.
  - `[low]` `[patch]` `nhap-mon-ky/SKILL.md` mẫu ghi timestamp thiếu offset múi giờ (ISO 8601 không
    đầy đủ) — thêm hướng dẫn kèm offset/`Z`.
- 3 finding reject (không phải lỗi thật): casing snake_case (JSON field) vs kebab-case (file/id) —
  quy ước kỹ thuật thông thường, không phải mâu thuẫn; thứ tự bước bái sư linh hoạt (không bắt buộc
  làm nhập môn ký trước vai/mạch) — lựa chọn thiết kế hợp lý, spec không cấm; sơ đồ §10.0 không vẽ
  node "đặt tên 4 vai" — sơ đồ minh hoạ luồng chỉ điểm, không phải danh sách đầy đủ mọi bước bái sư
  (CAP-16 đã khai riêng phần này).

Follow-up review recommendation: `true` — patch mức **high** trong pass này (điểm 1×high vượt ngưỡng
theo công thức chuẩn). Không tự chạy thêm một pass 4-reviewer nữa ngay (các fix đều cơ học — string
replace, dọn JSON, sửa câu chữ — đã tự verify `claude plugin validate --strict` PASS + JSON hợp lệ
sau mỗi bước) nhưng gắn cờ đúng quy định để một lượt soát người/tương lai biết ưu tiên xem lại đâu.

## Design Notes

`nhap-mon-ky` tách skill riêng thay vì làm luôn trong `nhap-mon` vì `disable-model-invocation` là thuộc tính cấp-skill (áp cho toàn bộ skill, không áp được cho một đoạn hội thoại con) — nếu gộp vào `nhap-mon`, cả Bước 0 (kiểm ngôn ngữ) cũng bị khoá theo, sai với ý định ("Dùng khi người học gõ /vd:nhap-mon" vẫn nên tự kích hoạt được bình thường). `nhap-mon` dẫn người học sang gọi `nhap-mon-ky` bằng lệnh tường minh, đúng khuôn Story 1.1 đã dùng cho `/plugin configure` (skill hướng dẫn, không tự chạy hộ việc chỉ người dùng mới làm được).

## Verification

**Commands:**
- `claude plugin validate van-dao --strict` -- expected: PASS (thêm skill `nhap-mon-ky`, sửa `nhap-mon`, cấu trúc phải hợp lệ)

**Manual checks (if no CLI):**
- Đọc `van-dao/skills/nhap-mon/SKILL.md` và `van-dao/skills/nhap-mon-ky/SKILL.md` xác nhận đủ 4 quy ước §12.4 mỗi file, và không trích số hiệu FR/NFR/§ nào (AD-11)
- Đọc `van-dao/skills/nhap-mon-ky/SKILL.md` xác nhận có `disable-model-invocation: true` trong frontmatter
- Đọc `van-dao/skills/nhap-mon/evals/evals.json` xác nhận có expectation mới khớp từng dòng I/O matrix ở trên, mỗi expectation có `evidence` trích nguyên văn transcript chạy thật (không suy diễn, không chỉ trỏ path scratchpad — AD-10)

## Auto Run Result

**Lần chạy 1:** Subagent implement bị dừng đột ngột giữa chừng do lỗi hạ tầng (API error) đúng lúc chuẩn bị viết `evals.json` — thông báo ban đầu báo `status: failed`. Vì SKILL.md của cả `nhap-mon` và `nhap-mon-ky` đã hoàn tất và đúng (tự đọc lại xác nhận), đã launch một subagent thứ hai chỉ để hoàn tất phần eval còn thiếu — **deviation có báo trước** (đúng tiền lệ Story 1.1 Lần chạy 1), tránh làm lại phần đã xong.

Ngay sau đó, subagent THỨ NHẤT bất ngờ gửi thông báo `completed` — hoá ra nó đã tự phục hồi sau lỗi API và chạy tiếp tới hết, tự viết luôn `evals.json` (7 kịch bản mới, id 4-10) bằng đúng phương pháp chạy thật đa lượt (`--resume`, cô lập cả `CLAUDE_CONFIG_DIR` lẫn `HOME`/`USERPROFILE`) mà không cần subagent thứ hai. Đã phát hiện nguy cơ 2 subagent cùng ghi một file → `TaskStop` subagent thứ hai ngay lập tức; xác nhận nó mới chỉ chạy `claude plugin validate` (không side-effect), chưa hề chạm `evals.json`/SKILL.md — không có xung đột ghi thật xảy ra.

**Đã tự đọc lại toàn bộ 2 file SKILL.md + evals.json** (không chỉ tin báo cáo subagent): cả hai đúng, đủ 4 quy ước §12.4, không trích FR/NFR/§ (AD-11), evidence trích nguyên văn transcript thật, không trỏ scratchpad. `claude plugin validate van-dao --strict` tự chạy lại lần nữa, PASS.

**Bug thật phát hiện khi chạy eval (giống lớp bug của Story 1.1):** skill dùng đường dẫn home đã biết từ trước thay vì tự tra lại ở đầu mỗi phiên mới, khiến kịch bản "đã bái sư xong từ trước" (phiên claude mới) nhận nhầm hồ sơ "chưa có". Đã sửa cả hai SKILL.md thêm bước xác định lại home hiện tại trước khi đọc/ghi bất kỳ đường dẫn `~/.vandao/` nào, chạy lại xác nhận đúng — chi tiết trong `evals.json` trường `note_bug_found`/`found_while_running_real_story2`.

Chưa commit trong repo `van-dao` — chờ qua step-04 review trước.

**Lần chạy 2 — step-04 review + đóng story:** 4 reviewer song song (Blind Hunter, Edge Case Hunter,
Verification Gap, Intent Alignment) xong, xem `## Review Triage Log`. Tất cả patch đã áp dụng trực
tiếp (không cần loopback step-03 — không có bad_spec/intent_gap thật, chỉ patch cơ học). Riêng finding
`/vd:` được người điều phối (không phải tôi tự quyết) chốt hướng xử lý, kèm nghiên cứu xác nhận qua
`claude-code-guide` trước khi sửa — không đoán.

Verify cuối: `claude plugin validate van-dao --strict` PASS; `evals.json` hợp lệ JSON (9 kịch bản,
id 1-9). Đã ghi quyết định `/vd:`→`/van-dao:` và định hướng chuyển tiếng Anh sau bản Việt đầu vào
`SPEC.md` Open Questions qua đúng skill `bmad-spec` (memlog + edit, không hand-edit ngoài quy trình).

**Commit:** repo `van-dao` (SKILL.md × 2, evals.json) và repo `van-dao-workspace` (story spec này,
SPEC.md + memlog, `docs/VAN-DAO-dac-ta-v1.0.md`) — thực hiện ngay sau khi ghi xong phần này.
