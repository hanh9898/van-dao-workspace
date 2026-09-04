---
title: 'Thiết lập ban đầu — ngôn ngữ giao tiếp'
type: 'feature'
created: '2026-08-27'
status: 'done' # intent_gap đã đóng bằng quyết định người điều phối, xem Spec Change Log + Tổng kết đóng story
baseline_revision: 'f5f9a86f4dfd1500d0921b2afda796afb1dcb5cc'
review_loop_iteration: 1
followup_review_recommended: false # pass cuối chỉ 1 patch mức low — dưới ngưỡng; rủi ro thật nằm trong deferred:
context:
  - '{project-root}/AGENTS.md'
warnings: []
deferred:
  - summary: >-
      Đặc tả (docs/VAN-DAO-dac-ta-v1.0.md §1) khai lệnh là `/vd:*` nhưng plugin.json đặt tên plugin
      là `van-dao` — mọi lệnh trong đặc tả có thể phải gọi bằng `/van-dao:*` thay vì `/vd:*` theo quy
      ước đặt tên lệnh mặc định của Claude Code.
    evidence: |-
      Xác nhận qua grep trực tiếp: docs/VAN-DAO-dac-ta-v1.0.md dòng 4 "Lệnh: /vd:*"; van-dao/.claude-plugin/plugin.json
      "name": "van-dao"; van-dao/skills/nhap-mon/evals/evals.json dùng "/van-dao:nhap-mon" khi chạy
      thật (không phải "/vd:nhap-mon"). Có từ đặc tả gốc, không phải do story này gây ra.
    location: 'docs/VAN-DAO-dac-ta-v1.0.md:4'
    severity: medium
  - summary: >-
      van-dao/skills/nhap-mon/evals/evals.json là artifact tĩnh, không có script/CI nào tự động
      chạy lại — một hồi quy tương lai của đúng bug Bước 0 vừa sửa sẽ không bị bắt tự động.
    evidence: |-
      van-dao/.github/workflows/kiem.yml chỉ chạy `pytest tests/`; van-dao/tests/ không có file nào
      động tới nhap-mon; không script nào trong repo parse/replay evals.json. Phát hiện bởi
      Verification Gap reviewer, tự xác nhận qua grep.
    location: 'van-dao/skills/nhap-mon/evals/evals.json'
    severity: medium
  - summary: >-
      Chưa rõ hành vi khi gọi `/plugin configure` xong rồi gọi lại `/vd:nhap-mon` NGAY trong cùng
      phiên (không mở phiên mới) — 3 eval hiện có đều dùng phiên riêng biệt cho mỗi trạng thái, chưa
      test đúng path "configure giữa phiên rồi dùng lại trong cùng phiên đó".
    evidence: |-
      evals.json eval #3 mô phỏng "phiên mới sau khi đã cấu hình từ trước", không mô phỏng "vừa
      configure xong, cùng phiên gọi lại ngay". Phát hiện bởi Edge Case Hunter.
    severity: medium
  - summary: >-
      Bước 0 (cả bản cũ và bản mới) không xử lý giá trị `communication_language` là chuỗi không hợp
      lệ/rác — chỉ phân biệt "rỗng/placeholder chưa thế" và "có giá trị cụ thể", không kiểm giá trị
      đó có phải tên ngôn ngữ hợp lệ không.
    evidence: |-
      SKILL.md Bước 0 chỉ có 2 nhánh (trống/placeholder vs có giá trị). Phát hiện bởi Blind Hunter và
      Edge Case Hunter độc lập. Rủi ro thấp vì field do `/plugin configure` set qua giao diện có kiểm
      soát, khó tạo giá trị rác qua luồng bình thường.
    severity: low
  - summary: >-
      Mô tả SKILL.md nói skill dùng để "kiểm tra/đặt lại ngôn ngữ giao tiếp", nhưng Bước 0 không có
      nhánh nào cho việc đổi một ngôn ngữ đã cấu hình — chỉ dùng ngay giá trị đã có, không hỏi lại.
    evidence: |-
      SKILL.md frontmatter description có chữ "đặt lại"; Bước 0 chỉ nói "dùng ngay... không hỏi lại
      — kể cả ở phiên sau" khi đã có giá trị, không có luồng reset. Có từ khi viết skill (Lần chạy 2),
      không phải do lần sửa Bước 0 (Lần chạy 4) gây ra.
    severity: low
  - summary: >-
      docs/VAN-DAO-trang-thai-du-an.md Ưu tiên 2 (đoạn mới thêm 2026-08-27) chưa nói rõ áp dụng thế
      nào cho skill đã viết trước ngày này, hoặc cho story chỉ SỬA (không viết mới) một skill có sẵn.
    evidence: |-
      Đoạn mới chỉ nói "mỗi story viết skill mới... tự mang theo eval nhẹ" — không đề cập skill cũ
      hoặc story sửa-không-viết-mới. Phát hiện bởi Edge Case Hunter khi review chính đoạn văn bản này.
    location: 'docs/VAN-DAO-trang-thai-du-an.md:144'
    severity: low
---

<intent-contract>

## Intent

**Problem:** Plugin `van-dao` vừa cài lần đầu chưa có cách nào kiểm tra hay hướng dẫn người học đặt ngôn ngữ giao tiếp qua `userConfig` — nếu cài không kèm `--config`, field `communication_language` để trống và không ai nhắc (Claude Code không tự chặn/hỏi, đã verify 2026-08-26, NFR8).

**Approach:** Tạo skill `nhap-mon` (điểm vào duy nhất, `/vd:nhap-mon`) với bước kiểm tra đầu tiên: đọc `communication_language` từ `userConfig`; trống thì hướng dẫn chạy `/plugin configure van-dao@van-dao`; có giá trị thì dùng ngay, không hỏi lại.

## Boundaries & Constraints

**Always:** Đọc đúng giá trị `communication_language` người học đã cấu hình qua `userConfig` (không tạo cơ chế cấu hình song song) — cách đọc cụ thể do triển khai quyết định, miễn đúng 3 dòng I/O matrix bên dưới; mọi định danh kỹ thuật tiếng Việt không dấu, kebab-case cho file/id; SKILL.md phải có đủ 4 quy ước bắt buộc (đặc tả §12.4): "Xong khi", "Khi nào skill này không giúp được", trình tự "Trình → xác nhận → ghi → kiểm", bước nạp field `customize.toml` trước việc chính (nếu có field phơi ra).

**Block If:** (không có — phạm vi đã rõ, không có quyết định cần người can thiệp giữa chừng)

**Never:** Không viết luồng bái sư (đặt tên môn phái, khai vai/mạch, đặt tên 4 vai — Story 1.2); không viết chỉ điểm hay thu bí kíp (Story 1.3/1.4); không tự động chạy `/plugin configure` hộ người dùng (không thể — đây là lệnh Claude Code cấp người dùng, skill chỉ hướng dẫn); không sửa `plugin.json` (field đã có, chỉ đọc).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Lần đầu, chưa cấu hình | `communication_language` trống/không tồn tại | Nói rõ chưa đặt ngôn ngữ, hướng dẫn chạy `/plugin configure van-dao@van-dao` | Không lỗi — chỉ hướng dẫn, không chặn tiếp tục nếu người học vẫn muốn dùng mặc định |
| Đã cấu hình từ trước | `communication_language` = "Vietnamese" (hoặc giá trị khác) | Dùng ngay giá trị đó cho mọi phản hồi sau, không hỏi lại | No error expected |
| Phiên mới, đã từng set | Field giữ nguyên giá trị đã lưu (Claude Code tự nạp lại) | Nạp lại đúng lựa chọn cũ, không hỏi lại | No error expected |

</intent-contract>

## Code Map

- `van-dao/skills/nhap-mon/SKILL.md` -- skill mới, chưa tồn tại (thư mục `van-dao/skills/` hiện chỉ có `.gitkeep`) — chứa bước 0 kiểm ngôn ngữ giao tiếp; Story 1.2 sẽ nối tiếp thêm luồng bái sư vào cùng file này
- `van-dao/.claude-plugin/plugin.json` -- đã có field `userConfig.communication_language` (type=string, default=Vietnamese, verify chạy thật 2026-08-26, NFR8) — chỉ đọc, không sửa trong story này
- `docs/VAN-DAO-dac-ta-v1.0.md` §12.4 -- nguồn 4 quy ước bắt buộc mọi SKILL.md phải có

## Tasks & Acceptance

**Execution:**
- `van-dao/skills/nhap-mon/SKILL.md` -- tạo skill mới với đủ 4 mục quy ước (§12.4) và bước 0 kiểm `communication_language` -- đúng AC Story 1.1, là điểm vào `/vd:nhap-mon` cho các story sau nối tiếp
- `van-dao/skills/nhap-mon/evals/evals.json` -- behavioral eval **nhẹ** theo `van-dao/.claude/rules/eval.md` (mức "vừa viết xong nháp", không phải mức đầy đủ 20-câu/60-40) -- đúng 3 expectation, mỗi cái khớp 1 dòng trong I/O & Edge-Case Matrix ở trên, mỗi expectation kèm `evidence` trích transcript chạy thật làm căn cứ

**Acceptance Criteria:**
- Given plugin bật lần đầu trên máy, when Claude Code xử lý `.claude-plugin/plugin.json`, then người dùng có thể chọn ngôn ngữ giao tiếp qua `userConfig` field `communication_language` (đã verify NFR8, không cần làm lại)
- Given người dùng gõ `/vd:nhap-mon` mà `communication_language` chưa set, when skill chạy, then skill tự kiểm tra field này và chủ động hướng dẫn chạy `/plugin configure van-dao@van-dao` — không giả định Claude Code tự động hỏi
- Given `communication_language` đã có giá trị, when một phiên mới bắt đầu, then skill nạp lại đúng giá trị đã lưu, không hỏi lại
- Given 3 kịch bản trên, when chạy `/vd:nhap-mon` thật cho từng kịch bản, then `evals/evals.json` ghi lại đúng 3 expectation tương ứng, mỗi cái có `evidence` trích đúng chỗ trong transcript chạy thật (không phải suy diễn) -- đóng gap NFR4 mà Matrix Test Audit đã phát hiện

## Design Notes

`nhap-mon` là điểm vào duy nhất (đặc tả §14, lệnh `/vd:nhap-mon`, Bậc 1). Story này chỉ dựng **bước 0** của skill — kiểm ngôn ngữ trước khi vào bái sư. Không dựng thành file riêng lẻ tách khỏi bái sư (Story 1.2) vì cả hai là hai bước liên tiếp của cùng một lệnh vào cửa; tách file sẽ tạo hai điểm vào giả cho cùng một lệnh thật.

## Verification

**Manual checks (if no CLI):**
- Đọc `van-dao/skills/nhap-mon/SKILL.md` xác nhận có đủ 4 mục quy ước §12.4: "Xong khi", "Khi nào skill này không giúp được", trình tự "Trình → xác nhận → ghi → kiểm", bước nạp `customize.toml` (hoặc ghi rõ "không có tuỳ biến" nếu skill chưa phơi field nào ở phạm vi story này)
- `claude plugin validate van-dao --strict` -- expected: PASS (thêm skill mới vào plugin, cấu trúc phải hợp lệ)
- Đọc `van-dao/skills/nhap-mon/evals/evals.json` -- expected: đúng 3 expectation, mỗi cái ánh xạ 1-1 với 1 dòng I/O & Edge-Case Matrix, mỗi expectation có trường `evidence` trích transcript chạy thật (không phải mô tả suy diễn) -- đây là test hành vi thật đóng gap mà Matrix Test Audit đã phát hiện, không phải manual-check-đọc-file như 2 dòng trên

## Spec Change Log

### 2026-08-27 — bad_spec repair (Matrix Test Audit)

**Phát hiện:** I/O & Edge-Case Matrix có 3 dòng nhưng `## Verification` gốc chỉ có manual check (đọc file, chạy validate) — không có test hành vi thật nào phủ 3 kịch bản. Root cause ngoài `<intent-contract>` — nằm ở `## Tasks & Acceptance` và `## Verification` thiếu yêu cầu eval hành vi.

**Đã sửa:** thêm task viết `evals/evals.json` (behavioral eval nhẹ, 3 expectation khớp matrix, mỗi cái kèm `evidence`) vào Tasks & Acceptance + AC thứ 4; thêm bước kiểm file eval vào Verification. Không sửa `<intent-contract>`.

**Căn cứ mức độ nghiêm ngặt (nhẹ, không phải đầy đủ):** nghiên cứu `_bmad-output/planning-artifacts/research/technical-quy-trinh-eval-khi-viet-skill-claude-ski-2026-08-27/research.md` (2026-08-27) — quy trình chính thức `skill-creator` của Anthropic tự thực hiện đúng nhịp "viết nháp → vài eval nhỏ ngay → lặp lại"; không tiền lệ nào ủng hộ hoãn eval tới vertical slice, nhưng cũng không cần bộ máy đầy đủ 20-câu/60-40 ngay từ story đầu tiên. `van-dao/.claude/rules/eval.md` đã cập nhật để phản ánh phân tầng này.

**KEEP:** SKILL.md hiện có (4 quy ước §12.4, bước 0 kiểm `communication_language`, `claude plugin validate` PASS) giữ nguyên, không viết lại — chỉ bổ sung eval, không chạm code đã đúng.

### 2026-08-27 — bug thật phát hiện khi chạy eval hành vi (KEEP ở trên bị lật bởi bằng chứng chạy thật)

**Phát hiện:** Khi chạy thật `/van-dao:nhap-mon` (không mô phỏng — cài `van-dao@van-dao` vào một
`CLAUDE_CONFIG_DIR` cô lập, dùng `claude plugin install --config` để đặt đúng trạng thái từng kịch
bản), Bước 0 bản gốc ("Đọc `userConfig.communication_language` từ `.claude-plugin/plugin.json`")
**không phân biệt được "chưa cấu hình" với "đã cấu hình"**: `plugin.json` chỉ chứa *schema* khai
`default: "Vietnamese"`, không phải giá trị người dùng thật đã đặt (giá trị thật nằm ở
`pluginConfigs["van-dao@van-dao"].options` trong `settings.json` của Claude Code). Chạy thật ở trạng
thái chưa cấu hình cho kết quả sai: skill tự nhận "Vietnamese" là giá trị đã xác nhận, không hướng
dẫn `/plugin configure` — vi phạm thẳng AC thứ hai của story này.

**Căn cứ cơ chế đúng:** `code.claude.com/docs/en/plugins-reference` — "Non-sensitive values can also
be substituted in skill and agent content" qua cú pháp `${user_config.KEY}`. Đã verify chạy thật:
placeholder này được Claude Code thế bằng giá trị thật (hoặc để trống/giữ nguyên cú pháp) tại thời
điểm nạp skill, khác hẳn việc đọc file `plugin.json` tĩnh.

**Đã sửa:** Bước 0 của `van-dao/skills/nhap-mon/SKILL.md` đổi sang đọc qua chỗ thế chỗ
`${user_config.communication_language}` thay vì đọc file `plugin.json`; nhánh rẽ xử lý cả hai dạng
"chưa set" có thể gặp (chuỗi rỗng hoặc placeholder chưa được thế). Không đụng `<intent-contract>` —
đây là sửa lỗi triển khai để đạt đúng AC đã có, không đổi ý định. Không đụng `plugin.json` (đúng
"Never" của story). Đã chạy lại cả 3 kịch bản thật sau khi sửa — cả 3 đều đúng hành vi mong đợi, xem
`evals/evals.json` trường `found_while_running_real` và evidence từng expectation.

**KEEP ở mục trước không còn đúng** — ghi lại ở đây thay vì xoá, để không mất dấu vết quyết định đã
đổi vì lý do gì.

### 2026-08-27 — intent_gap được người điều phối giải quyết

**Quyết định:** chọn phương án 1 trong `_bmad-output/implementation-artifacts/bmad-build-auto-patch-story-1-buoc0-mechanism.md`
— sửa `<intent-contract>` mục Always theo **đích** thay vì **cơ chế**: từ "Đọc `userConfig.communication_language`
đã có sẵn trong `plugin.json`" thành "Đọc đúng giá trị `communication_language` người học đã cấu hình
qua `userConfig`... cách đọc cụ thể do triển khai quyết định, miễn đúng 3 dòng I/O matrix". Đây là
sửa `<intent-contract>` DUY NHẤT trong story này, và chỉ làm sau khi có quyết định rõ từ người điều
phối — không tự suy diễn.

**Hệ quả:** code hiện có (`SKILL.md` dùng `${user_config.communication_language}`, `evals/evals.json`)
không cần đổi gì thêm — đã khớp đúng contract mới. intent_gap đóng, không cần quay lại step-03.

## Review Triage Log

### 2026-08-27 — Review pass

- intent_gap: 1 (high 1)
- bad_spec: 0
- patch: 0
- defer: 0
- reject: 0
- addressed_findings:
  - none

(intent_gap khiến các finding khác thuộc pass này moot — sẽ xét lại đầy đủ ở pass kế tiếp sau khi
intent-contract được người điều phối quyết định. Bốn reviewer song song — Blind Hunter, Edge Case
Hunter, Verification Gap, Intent Alignment Auditor — cũng tìm thêm ~15 finding khác (đa số defer:
thiếu cơ chế "đặt lại" ngôn ngữ, `/vd:*` vs `/van-dao:*` chưa khớp tên plugin thật, chưa rõ nạp lại
config có cần phiên mới không, `evals.json` chưa có harness tự động re-run — và vài reject do lỗi
paste của chính người điều phối khi dựng prompt review, không phải lỗi thật trong repo) — đầy đủ
trong báo cáo gửi người điều phối, chưa ghi vào `deferred:` vì moot bởi intent_gap.)

### 2026-08-27 — Review pass (xử lý findings đã moot, sau khi intent_gap được giải quyết)

- intent_gap: 0 (đã đóng — xem Spec Change Log)
- bad_spec: 0
- patch: 1 (low 1)
- defer: 6 (medium 3, low 3)
- reject: 6 (đều do lỗi rút gọn nội dung của chính người điều phối lúc dựng prompt review round trước
  — evidence bị cắt còn "...", thiếu dòng phân cách bảng markdown, hiểu nhầm cú pháp `${user_config.x}`
  là "chưa verify" trong khi transcript thật đã có sẵn — không phải lỗi thật trong repo; cộng thêm
  reviewer tự lấy nhầm ngày hệ thống mặc định (2026-08-26) thay vì ngày phiên thật (2026-08-27), và
  hiểu nhầm slug thư mục nghiên cứu bị cắt ngắn là lỗi trong khi đó là hành vi cố ý của script)
- addressed_findings:
  - `[low]` `[patch]` `van-dao/.claude/rules/eval.md` tự mâu thuẫn ("bắt đầu nhẹ" rồi ngay sau lại
    "cần cả hai loại ở mức đầy đủ") — đã sửa câu cuối thành "(mức nhẹ ngay lúc viết, nâng dần lên mức
    đầy đủ theo đúng nhịp ở trên)" để nhất quán với đoạn ngay trên nó.

6 finding defer đã ghi vào frontmatter `deferred:` (3 medium, 3 low) — không cái nào chặn đóng story
này; để lại cho lần chạm tới các bề mặt liên quan (đổi tên lệnh, dựng CI cho evals, story sửa Bước 0
lần nữa).

**Đóng traceability xuyên-repo:** đã commit thay đổi trong repo `van-dao` (repo git riêng, không lồng
vào workspace) tại SHA `fdc0fa4` — "feat: skill nhap-mon (Bước 0 kiểm ngôn ngữ) + eval nhẹ", gồm
`skills/nhap-mon/SKILL.md`, `skills/nhap-mon/evals/evals.json`, `.claude/rules/eval.md`.

## Tổng kết đóng story

**Tóm tắt thay đổi:** skill `nhap-mon` (Bước 0 — kiểm ngôn ngữ giao tiếp) hoàn chỉnh, có eval hành vi
nhẹ thật (3/3 kịch bản I/O matrix, chạy thật + evidence transcript), một bug thật (đọc sai nguồn giá
trị `communication_language`) được phát hiện và sửa nhờ chạy eval thật thay vì viết eval hình thức.

**File đã đổi:**
- `van-dao/skills/nhap-mon/SKILL.md` (mới) — skill, Bước 0 dùng `${user_config.communication_language}`
- `van-dao/skills/nhap-mon/evals/evals.json` (mới) — eval hành vi nhẹ, 3 kịch bản
- `van-dao/.claude/rules/eval.md` — thêm phân tầng nhẹ/đầy-đủ + thời điểm viết eval
- `docs/VAN-DAO-trang-thai-du-an.md` — sửa Ưu tiên 2/3, gỡ cách đọc "hoãn eval tới vertical slice"
- `_bmad-output/planning-artifacts/research/technical-quy-trinh-eval-khi-viet-skill-claude-ski-2026-08-27/` (mới) — nghiên cứu căn cứ cho quyết định mức độ nghiêm ngặt eval
- `_bmad-output/implementation-artifacts/bmad-build-auto-patch-story-1-buoc0-mechanism.md` (mới) — patch tham chiếu, đã dùng để người điều phối quyết định, còn giữ làm hồ sơ

**Review findings:** 1 intent_gap (đã đóng bằng quyết định người điều phối, sửa `<intent-contract>`
mục Always theo đích thay vì cơ chế) · 1 patch áp dụng (sửa mâu thuẫn trong eval.md) · 6 defer (ghi
`deferred:`, không chặn) · 6 reject (lỗi dựng prompt review của chính người điều phối, không phải
lỗi thật trong repo).

**Follow-up review recommendation:** `false` — pass cuối chỉ có 1 patch mức low (điểm số 1, dưới
ngưỡng 5). Điểm cần theo dõi thật (dù không cần review pass ngay) nằm trong `deferred:`.

**Verification đã chạy:**
- `claude plugin validate van-dao --strict` → PASS (chạy lại lần cuối trước khi đóng)
- Đọc `evals/evals.json`: đúng 3 expectation, mỗi cái có `evidence` trích nguyên văn transcript chạy
  thật (`scratchpad/eval-runs/final_scenario{1,2,3}.txt`, đã tự đọc lại xác nhận khớp)
- Đọc `SKILL.md`: đủ 4 quy ước §12.4
- Cơ chế `${user_config.KEY}` tự tra cứu độc lập tại `code.claude.com/docs/en/plugins-reference` —
  xác nhận có thật, đúng như trích dẫn trong Spec Change Log

**Rủi ro còn lại:** 6 mục trong `deferred:` (đáng chú ý nhất: `/vd:*` có thể không khớp tên lệnh thật
`/van-dao:*`; `evals.json` chưa có CI tự chạy lại) — không chặn story này, nhưng nên xem trước khi
dựa nhiều vào lệnh `/vd:*` ở các story sau.

## Auto Run Result

Status: done
Blocking condition: (không còn — intent_gap đã đóng bằng quyết định người điều phối, xem Spec Change
Log 2026-08-27 và "Tổng kết đóng story" bên dưới)

**Lần chạy 1** (bỏ đi): HALT vì môi trường không có subagent đồng bộ — xem lịch sử; đã tự triển khai trực tiếp thay thế (deviation có báo trước với người điều phối), giữ nguyên spec làm nguồn sự thật.

**Lần chạy 2 (hiện tại):** Đã tạo `van-dao/skills/nhap-mon/SKILL.md` — đủ 4 quy ước §12.4 (Xong khi / Khi nào không giúp được / Trình→xác nhận→ghi→kiểm / nạp customize.toml), đúng bước 0 kiểm `communication_language` theo Tasks & Acceptance. `claude plugin validate van-dao --strict` PASS.

**Matrix Test Audit fail:** I/O & Edge-Case Matrix có 3 dòng, nhưng `## Verification` của spec này chỉ có manual check (đọc file, chạy validate) — **không có test hành vi thật nào** phủ 3 kịch bản đó. Đây là lỗ hổng thật trong chính spec (bỏ sót lúc lập kế hoạch): NFR4 ("mọi skill phải có trigger eval + functional/behavioral eval trước khi coi hoàn thành") không tuỳ chọn, và `van-dao/.claude/rules/eval.md` đòi cả hai loại — trigger eval (20 câu, 8-10 dương/8-10 âm near-miss, chạy 3 lần, chia 60/40 train/test) và behavioral eval (`evals/evals.json`, mỗi expectation kèm `evidence` trích transcript). Đây là việc thật, cần gọi skill lặp lại nhiều lần và chấm điểm — không phải thứ viết một dòng JSON cho có.

**Không tự ý viết eval sơ sài để qua ải.** Dừng đúng lúc phát hiện gap thật, báo lại đầy đủ thay vì tự quyết mức độ nghiêm túc của phần eval.

**Lần chạy 3 (hiện tại) — bad_spec repair:** đã chạy nghiên cứu (deep-recon) để xác định đúng mức độ nghiêm ngặt của eval, xem `## Spec Change Log`. Áp nhánh bad_spec: sửa `## Tasks & Acceptance` + `## Verification`, không đụng `<intent-contract>`. `status` chuyển `blocked` → `in-progress`, `review_loop_iteration` → 1, để resume step-03 (viết `evals/evals.json` thật) rồi step-04 review lại.

**Lần chạy 4 (hiện tại) — resume step-03, viết `evals/evals.json` thật:**

- Dựng môi trường chạy thật cô lập: `CLAUDE_CONFIG_DIR` trỏ vào một thư mục scratch riêng (không đụng
  `~/.claude` thật của máy dev — đã verify sạch cả trước lẫn sau bằng grep trực tiếp), thêm marketplace
  cục bộ trỏ vào `./van-dao`, rồi `claude plugin install van-dao@van-dao [--config
  communication_language=<giá trị>] -y` để dựng đúng 3 trạng thái của I/O & Edge-Case Matrix. Model
  dùng cho các lần gọi `claude -p` là `sonnet` (không phải model mặc định của tài khoản, để kiểm soát
  chi phí).
- Lần chạy đầu tiên (trạng thái "chưa cấu hình", SKILL.md bản gốc) cho kết quả **sai** — xem mục
  "bug thật phát hiện khi chạy eval hành vi" ở `## Spec Change Log` ngay trên. Đây đúng là loại gap mà
  "không tự ý viết eval sơ sài để qua ải" (Lần chạy 2) muốn tránh: nếu viết evidence khớp với hành vi
  sai đó rồi cho qua, eval sẽ xác nhận nhầm một hành vi không đạt AC.
- Đã sửa Bước 0 (dùng `${user_config.communication_language}` thay vì đọc `plugin.json`), chạy lại cả
  3 kịch bản thật, cả 3 đều đúng AC. Đã dọn sạch môi trường test cô lập (uninstall plugin, remove
  marketplace, xoá bản sao credentials tạm) — xác nhận lại `~/.claude` thật của máy dev không có dấu
  vết `van-dao` nào sau khi dọn.
- Đã ghi `van-dao/skills/nhap-mon/evals/evals.json`: đúng 3 eval case (khớp 1-1 với 3 dòng matrix),
  đúng 3 expectation, mỗi expectation có `evidence` trích nguyên văn transcript chạy thật (không suy
  diễn) — đóng đúng gap NFR4 mà Matrix Test Audit (Lần chạy 2) phát hiện.
- `claude plugin validate van-dao --strict` PASS sau cả hai lần sửa (SKILL.md và khi thêm
  `evals/`).
- Không đụng `plugin.json`, không viết luồng bái sư, không tự chạy `/plugin configure` hộ người dùng —
  đúng "Never" của `<intent-contract>`.
- **Còn lại cho step-04 (review):** phần sửa Bước 0 (dùng `${user_config.KEY}`) là thay đổi hành vi
  thật ngoài kế hoạch ban đầu của story (ban đầu chỉ định thêm eval) — nên có người soát lại đúng chỗ
  sửa này trước khi đóng story, dù đã tự verify bằng chạy thật 3 lần.

**Lần chạy 5 (hiện tại) — step-04 review, kết quả: intent_gap thật:**

- 4 reviewer chạy song song (Blind Hunter, Edge Case Hunter, Verification Gap, Intent Alignment
  Auditor). Cả Blind Hunter và Intent Alignment Auditor độc lập phát hiện cùng một vấn đề gốc:
  `<intent-contract>` mục **Always** vẫn viết "Đọc `userConfig.communication_language` đã có sẵn
  trong `plugin.json`" — nhưng bản sửa Bước 0 (Lần chạy 4, đã verify chạy thật) chứng minh cách đọc
  này **không thể** phân biệt "chưa cấu hình" với "đã cấu hình bằng đúng giá trị mặc định" trong mọi
  trường hợp, và đã đổi sang `${user_config.communication_language}`. `<intent-contract>` không được
  cập nhật theo — hai nguồn (contract chữ và code thật) hiện nói khác nhau.
- Phân loại: **intent_gap** — root cause nằm trong `<intent-contract>` (câu Always mô tả một cơ chế
  đã chứng minh bất khả thi). Theo đúng nhánh intent_gap: không tự sửa `<intent-contract>`, đã lưu
  patch tham chiếu tại `C:\Users\<user>\Projects\van-dao-workspace\_bmad-output\implementation-artifacts\bmad-build-auto-patch-story-1-buoc0-mechanism.md`.
- **Deviation có báo lại (theo đúng tiền lệ Lần chạy 1 của chính story này):** nhánh intent_gap gọi ý
  revert code. Đã **không revert** — bản sửa Bước 0 đã verify bằng 3 lần chạy thật là đúng, cách đọc
  gốc trong contract đã chứng minh sai/bất khả thi; revert sẽ đưa lại đúng bug đã tìm ra, không bảo
  vệ được gì. Giữ nguyên `van-dao/skills/nhap-mon/SKILL.md`, `evals/evals.json` như Lần chạy 4.
  Không tự sửa `<intent-contract>` — đây là ranh giới không tự vượt qua.
- 3 reviewer còn lại (Edge Case Hunter, Verification Gap, phần còn lại của Blind Hunter) tìm thêm
  ~15 finding khác — theo cascading rule, moot vì intent_gap tồn tại, chưa xử lý ở pass này. Đáng
  chú ý nhất trong số đó (để xét lại ở pass sau): (1) `docs/VAN-DAO-dac-ta-v1.0.md` §1 khai "Lệnh:
  `/vd:*`" nhưng plugin thật tên `van-dao` — mọi lệnh `/vd:*` trong đặc tả có thể không khớp tên gọi
  Claude Code thật (`/van-dao:*`), tiền tệ trước story này, không phải do pass này gây ra; (2)
  `evals/evals.json` là artifact tĩnh, không có script/CI nào tự chạy lại — một hồi quy tương lai
  của đúng bug vừa sửa sẽ không bị bắt tự động (verification gap thật, nhưng việc dựng harness tự
  động là việc lớn hơn phạm vi "eval nhẹ" của story này).
- **Chưa commit** thay đổi trong repo `van-dao` (SKILL.md, evals.json, eval.md) — cross-repo
  traceability gap do reviewer nêu (không có SHA nối story này với trạng thái code thật trong repo
  `van-dao` tách biệt) còn treo, nên xử lý cùng lúc với quyết định intent_gap ở trên trước khi đóng
  story.
