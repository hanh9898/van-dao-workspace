---
title: 'technical research: claude-tutor (kirilxd) — plugin dạy học trên Claude Code'
type: 'technical'
topic: 'claude-tutor (kirilxd/claude-tutor) — plugin dạy học qua Claude Code, đối chiếu Vấn Đạo'
decision: 'Cách viết SKILL.md/agents/hooks của Vấn Đạo — đối chiếu domain dạy-học, đóng khoản nợ đặc tả §17'
source: 'Native run — web thật, kéo trực tiếp file gốc github.com/kirilxd/claude-tutor (branch main)'
status: complete
preset: 'standard'
validation: 'normal'
claims_verified: 3
claims_unverified: 0
created: '2026-08-25'
updated: '2026-08-26'
---

# technical research: claude-tutor (kirilxd) — plugin dạy học trên Claude Code

**Decision this research serves:** claude-tutor giải **đúng bài toán sản phẩm** của Vấn Đạo (dạy qua Claude Code) chứ không chỉ đúng kỹ thuật viết skill — "Turn Claude Code into your personal tutor — personalized learning plans, adaptive quizzes, SM-2 spaced repetition, and a web dashboard." Đặc tả Vấn Đạo đã tự ghi nhận thiếu cơ chế eval (trigger + functional) mà claude-tutor có — đây là lượt đọc kỹ để đóng khoản nợ đó, cộng đối chiếu kiến trúc/văn phong.

## 1. Tóm tắt điều hành

claude-tutor là plugin nhỏ (5 skill: `learn`, `quiz`, `resources`, `review`, `dashboard`), 115 sao, cập nhật 20/07/2026, 100% dữ liệu cục bộ tại `~/.claude/learning/` [1][11]. Bốn phát hiện quan trọng nhất:

1. **Cơ chế eval 2 tầng đúng khoản nợ Vấn Đạo §17**: `trigger_evals` (routing đúng skill chưa — `--max-turns 1`, không chạy thật) và `functional_evals` (kết quả sau khi chạy thật, có `expectations[]`) — đây là mẫu hình cụ thể, có thể tái dùng gần nguyên trạng [12][13][14].
2. **Có lớp `commands/` tách biệt với `skills/`** mà BMAD không có — quan hệ không đồng nhất: command cho việc hội thoại là pointer mỏng ("Follow the `learn` skill instructions..."), command cho việc máy móc (dashboard) tự chứa logic Bash [8][9][10].
3. **Không có persona, không có rào chắn giọng điệu tương đương FR33** của Vấn Đạo — "gia sư" hoàn toàn trung tính chức năng, phản hồi quiz theo template cố định (Correct!/Not quite...) [19][20].
4. **enforce-paths.js là script xác định thật (không phải quy ước hội thoại)** ép ranh giới ghi file bằng string-match + whitelist field theo schema, đóng lại bằng `process.exit(2)` — có 27 test case cho hook này [17][15].

**Điểm phương pháp quan trọng**: mọi nội dung ở đây lấy qua WebFetch (xử lý qua model tóm lược trung gian với hầu hết file, curl thô với một số file) — trích dẫn cụm từ trong ngoặc kép có độ tin cao về nội dung nhưng chỉ trung bình về định dạng trình bày chính xác tuyệt đối (bảng vs heading). Xem ghi chú ở từng mục.

## 2. Theo từng chiều

### 2.1 Cấu trúc & kiến trúc plugin dạy học

`plugin.json` khai `hooks` ngay trong manifest (không phải file riêng): `PreToolUse` (matcher `Write|Edit`) gọi `enforce-paths.js`, `SessionStart` gọi `session-start.js` [1]. `marketplace.json` là manifest riêng theo schema Anthropic, khai `plugins[].source` trỏ repo GitHub — hai lớp tách biệt (plugin vs cách phân phối) [2].

Ranh giới 5 skill dựa trên **sở hữu dữ liệu**: `learn` ghi `plans/{slug}-{date}.json` (cấm lẫn field quiz — "Never add quiz fields... to plan files"), `quiz` ghi `progress/{slug}.json` (cấm ngược lại) [3][7]; `resources`/`review`/`dashboard` chỉ đọc, không ghi mới — mô hình "một nguồn ghi, nhiều nguồn đọc" qua `index.json` làm registry trung tâm [4][5][6]. Ranh giới không tuyệt đối: `learn` có cả "Phase 5: Teach" (dạy tương tác), không chỉ tạo plan [3].

**Lớp `commands/` là điểm khác biệt kiến trúc rõ nhất với BMAD** (BMAD chỉ có skill, không có lớp lệnh riêng). `commands/learn.md` là wrapper mỏng: frontmatter khai `allowed-tools` (whitelist công cụ) + `argument-hint`, thân chỉ nói "Follow the `learn` skill instructions to: [checklist]" — không lặp lại logic [8]. `commands/quiz.md` cùng khuôn, thêm cú pháp flag `--module N`/`--count N` — lớp command đảm nhận parse tham số CLI-style [9]. **Ngoại lệ:** `commands/dashboard.md` không trỏ về skill mà chứa trực tiếp 3 bước lệnh Bash khởi chạy server — command cho việc máy móc tự chứa logic, command cho việc hội thoại chỉ là pointer [10].

README khẳng định kiến trúc "all information remains local... nothing transmits to external services", yêu cầu Node.js 18+/Claude Code 2.0+, và nêu rõ có "hook systems for data validation, comprehensive testing frameworks, and evaluation suites for trigger and functional testing" — tức lớp eval là một phần kiến trúc công bố chính thức, không phải phụ trợ ẩn [11].

### 2.2 Eval & Known limitations (khoản nợ §17 của Vấn Đạo)

`evals/evals.json` có 3 khoá cấp cao: `skill_name`, `trigger_evals`, `functional_evals` [12]. Mỗi `trigger_evals` có `{id, prompt, should_trigger}` — ví dụ `{"prompt": "I want to learn kubernetes", "should_trigger": "learn"}` [12]. `run-trigger-eval.sh` gọi `claude -p "$prompt" --max-turns 1`, kiểm output JSON có `"name":"Skill"` và `"skill"` khớp `should_trigger` — **không cho skill chạy thật**, chỉ bắt bước routing [13].

`functional_evals` có thêm `setup_prompt`/`depends_on` tuỳ chọn và `expectations[]` [12]. `run-functional-eval.sh` sao lưu `~/.claude/learning/` trước khi chạy, rồi thực thi 5 test thật: `/learn DNS` (kiểm plan không lẫn field quiz), `/quiz dns` (kiểm progress không lẫn field plan), `/review` (kiểm output đề cập đúng chủ đề + điểm số), **test path-enforcement hook** (cố ý ghi sai chỗ, pass nếu hook chặn), và file-integrity (không có file rác) [14]. Cơ chế kiểm dùng `jq -e`/`grep -q`/`[ -f ]` thuần shell, không cần framework test riêng [14].

`tests/test-hooks.js` kiểm hook `enforce-paths.js` qua exit code (0=cho phép, 2=chặn), 27 test case chia 8 nhóm: chặn field quiz vào plans/, chặn field plan vào progress/, cho phép ghi đúng, bảo vệ thư mục root, bỏ qua enforcement ngoài `learning/`, hỗ trợ tool Edit qua `new_string`, phát hiện lỗi schema (tên field sai, `overallScore` phải là số nguyên phần trăm không phải thập phân), chặn đường dẫn tương đối/tuyệt đối sai [15].

**Known limitations (README, trích gần-nguyên-văn, xem ghi chú phương pháp):**
1. *Quiz formats* — "Dashboard supports MCQ and True/False only. Short answer and fill-in-blank are CLI-only."
2. *AskUserQuestion* — "CLI may fall back to plain text depending on Claude Code version."
3. *CLI schema drift* — "Claude occasionally invents field names. Dashboard normalizes on read; hook blocks common errors." [11]

*Ghi chú độ tin: nội dung 3 giới hạn trên có độ tin cao (câu chữ khớp qua nhiều lượt fetch), nhưng định dạng trình bày gốc (bảng markdown vs heading con) chỉ ở mức trung bình — WebFetch xử lý qua model tóm lược, chưa đối chiếu ký tự-cho-ký tự với file thô.*

### 2.3 Giữ trạng thái / tiến trình học

`hooks/session-start.js` chỉ chạy **due-check nhẹ**: đọc `index.json` + các file tiến trình, so `nextReview` với ngày hiện tại, đếm mục đến hạn, in nhắc nhở — **không nạp toàn bộ hồ sơ vào context** như `nap-ho-so.sh` của Vấn Đạo; nếu parse lỗi thì thoát êm, không gián đoạn phiên [16]. `hooks/enforce-paths.js` là validator ghi file: string-match ranh giới `plans/*` vs `progress/*`, whitelist field JSON theo loại file, vi phạm → `process.exit(2)` [17].

Dashboard (`skills/dashboard/server/`) dùng Express, API đọc trực tiếp file hệ thống (`index.json`, `plans/`, `progress/`, `profile.json`); endpoint `PUT /progress/:slug/spaced-repetition/:concept` cập nhật SM-2, `GET /calendar` cho lịch ôn tập [18]. **SSE không dựa trên file-watch/polling** — nó stream stdout của một subprocess `claude -p <prompt>` đang chạy; "real-time" ở đây là streaming tiến trình MỘT lệnh CLI, không phải live-sync dữ liệu học giữa nhiều client [18]. `validate.js` viết tay (không Zod/Ajv), whitelist field + bắt buộc 4 field SM-2 (`easeFactor`, `intervalDays`, `nextReview`, `repetitions`) trong `spacedRepetition`, trả `{valid, errors[]}` không throw — để `enforce-paths.js` xử lý graceful [18].

Thuật toán SM-2 đầy đủ nằm trong `skills/quiz/SKILL.md`/`review/SKILL.md`: quality 0-5 theo kết quả; đúng (quality≥3): lần 1 `intervalDays=1`, lần 2 `=6`, từ lần 3 `= round(interval_trước × easeFactor)`; sai: reset về 1; `easeFactor = max(1.3, easeFactor + 0.1 − (5−quality)×(0.08+(5−quality)×0.02))` [6][7].

### 2.4 Văn phong sư phạm

`learn/SKILL.md` tổ chức dạy thành 6 pha đánh số/tên rõ (Phase 0 Load Profile → 1 Clarify Scope → 1.5 Diagnostic → 2 Research → 3 Generate Plan → 4 Save → 5 Teach) — văn phong quy trình/checklist, không tường thuật [3]. Chỉ dẫn giọng dạy là mệnh lệnh trực tiếp ("Keep explanations conversational, not textbook-like") [3].

**Không tìm thấy persona/nhân vật nào cho "gia sư"** — không tên, không tính cách; CLAUDE.md chỉ mô tả "a personal tutor with spaced repetition" ở mức vai trò chức năng [19]. `quiz/SKILL.md` quy định template phản hồi cố định: đúng → "Correct! [1-2 câu giải thích]"; sai → "Not quite. The answer is [đáp án]. [2-3 câu giải thích]" — **không có điều khoản cấm khen sáo rỗng** tương đương FR33 của Vấn Đạo [7]. Mọi "Never/Always" tìm được thuộc phạm trù toàn vẹn dữ liệu/kỹ thuật (không lẫn field, luôn dùng đường dẫn tuyệt đối, luôn dùng tool AskUserQuestion, không quá 3-4 đoạn văn không có điểm tương tác), không thuộc phạm trù giọng điệu [3].

CLAUDE.md xác nhận kiến trúc 3 lớp tách biệt: Skills (chỉ là markdown hướng dẫn, không tự thực thi ràng buộc), Hooks (Node.js script ép toàn vẹn dữ liệu), Dashboard (Express server) — ràng buộc do hooks đảm nhiệm, skill chỉ ra lệnh bằng văn bản [19].

## 3. Phát hiện xuyên chiều

1. **Eval 2 tầng (trigger + functional) là mẫu hình chuyển-được gần nguyên trạng cho Vấn Đạo** — không chỉ là ý tưởng trừu tượng, mà có cấu trúc file cụ thể (`evals.json` schema, 2 script shell dùng `jq`/`claude -p --max-turns 1`) đóng đúng khoản nợ §17 mà không cần phát minh lại từ đầu.

2. **Lớp `commands/` tách biệt với `skills/` giải đúng vấn đề Vấn Đạo đã có nhưng chưa đặt tên nguyên tắc**: Vấn Đạo có `/vd:*` (đặc tả: "Cắt lệnh không cắt thành phần") — claude-tutor cho thấy nguyên tắc rõ ràng để quyết định "command nên là pointer mỏng hay tự chứa logic": pointer khi đích là skill hội thoại (LLM diễn giải), tự chứa khi đích là hành động máy móc thuần (khởi chạy server, không cần LLM).

3. **Domain "dạy học qua AI" không tự động cần rào chắn giọng điệu** — claude-tutor (cùng domain với Vấn Đạo) không có gì tương đương FR33. Đây không phải bằng chứng FR33 thừa (Vấn Đạo có lý do riêng: thế giới quan tu luyện, tránh sáo rỗng phá vỡ trải nghiệm), mà là xác nhận: FR33 là lựa chọn có chủ đích của Vấn Đạo, không phải "thông lệ ngành dạy-học-qua-AI".

## 4. Bằng chứng ngược

Không chạy red-team pass ở lượt nghiên cứu này (`red_team: off`) — không có mục nào ở phần này.

## 5. Khuyến nghị

1. **Áp dụng gần nguyên trạng mẫu hình eval 2 tầng (trigger_evals + functional_evals) cho Vấn Đạo** — đóng đúng khoản nợ đặc tả §17. Cấu trúc cụ thể: file JSON danh sách test case + 2 script shell (routing-only dùng `--max-turns 1`, và full-run có `expectations[]`). Độ tin: cao (mẫu hình cụ thể, đã chạy thật trong một plugin tương tự). *Feed vào: `bmad-create-epics-and-stories` — một epic riêng cho "Nền: eval suite", tham chiếu trực tiếp cấu trúc này.*

2. **Đặt tên tường minh nguyên tắc "command là pointer mỏng vs. tự chứa logic"** cho lớp `/vd:*` của Vấn Đạo, dựa theo tiêu chí quan sát được ở claude-tutor: đích là skill hội thoại (LLM diễn giải) → pointer mỏng chỉ khai `allowed-tools`/tham số; đích là hành động máy móc thuần (không cần LLM) → tự chứa logic. Độ tin: trung bình (nguyên tắc rút ra từ 1 ví dụ, chưa kiểm chứng rộng). *Feed vào: cách viết `commands/*.md` (nếu Vấn Đạo có lớp này riêng biệt khỏi skill) khi viết story.*

3. **Không cần thêm rào chắn giọng điệu học theo claude-tutor — FR33 của Vấn Đạo giữ nguyên, không phải thứ cần "chuẩn hoá theo ngành".** Xác nhận: domain dạy-học-qua-AI không có thông lệ chung về việc cấm khen sáo rỗng; đây là lựa chọn riêng của Vấn Đạo (thế giới quan tu luyện), tiếp tục giữ. Độ tin: cao. *Feed vào: không cần hành động.*

4. **Cân nhắc mẫu hook "string-match + field whitelist theo schema, exit code 2 khi vi phạm" của `enforce-paths.js`** cho các script kiểm tra ranh giới ghi của Vấn Đạo (đã có tinh thần tương tự ở `.pham-vi.json`/`kiem-thu.py`) — điểm khác: claude-tutor có bộ test riêng cho chính hook này (30 case, 8 nhóm), một kỷ luật kiểm-thử-cho-hook mà Vấn Đạo chưa xác nhận có tương đương. Độ tin: trung bình. *Feed vào: story cho `hooks/kiem-thu.sh`, cân nhắc thêm test suite riêng cho hook.*

## 6. Câu hỏi còn mở

1. Nội dung README dạng bảng "Known limitations" — chưa đối chiếu ký tự-cho-ký tự với file thô (WebFetch qua model tóm lược); nếu cần trích dẫn chính thức, cần đọc lại bằng curl trực tiếp.
2. `evals.json` đầy đủ (toàn bộ 17 trigger_evals + 3 functional_evals) chưa được dump nguyên văn — chỉ có cấu trúc + ví dụ; nếu Vấn Đạo muốn copy khuôn mẫu chính xác, nên đọc lại toàn văn file này qua công cụ không tóm lược.
3. Không rõ tần suất chạy eval suite thật trong quy trình phát triển của claude-tutor (mỗi commit? thủ công?) — README chỉ xác nhận sự tồn tại, không mô tả CI/cadence.
4. `commands/resources.md` và `commands/review.md` chưa được đọc trực tiếp (chỉ suy luận theo mẫu learn.md/quiz.md) — cần xác nhận có cùng khuôn "pointer mỏng" không.
5. Chưa xác nhận pub_date/ngày commit cuối của từng file (WebFetch không trả metadata Git).

## 7. Phụ lục nguồn

Mọi nguồn dưới đây: publisher "GitHub (kirilxd/claude-tutor)" · pub_date N/A · truy cập 2026-08-25 · độ tin Cao trừ khi ghi chú khác (nội dung qua WebFetch với model tóm lược trung gian cho phần lớn file — xem §2.2 về giới hạn trích dẫn nguyên văn).

| # | Nguồn | Hỗ trợ phát hiện |
|---|---|---|
| [1] | `.claude-plugin/plugin.json` | Manifest, khối hooks trong manifest |
| [2] | `.claude-plugin/marketplace.json` | Manifest phân phối riêng biệt |
| [3] | `skills/learn/SKILL.md` | Sở hữu dữ liệu plans/, cấm lẫn field, Phase 5 Teach |
| [4] | `skills/resources/SKILL.md` | Skill đọc-only, Data Schemas |
| [5] | `skills/dashboard/SKILL.md` | Đặc tả dashboard, local web server |
| [6] | `skills/review/SKILL.md` | Đọc index.json + progress, thuật toán SM-2 |
| [7] | `skills/quiz/SKILL.md` | Trigger description, format phản hồi, adaptive difficulty, SM-2 |
| [8] | `commands/learn.md` | Command pointer mỏng, allowed-tools |
| [9] | `commands/quiz.md` | Command + parse flag CLI-style |
| [10] | `commands/dashboard.md` | Command tự chứa logic Bash (ngoại lệ) |
| [11] | `README.md` | Kiến trúc local-only, Known limitations, yêu cầu hạ tầng |
| [12] | `evals/evals.json` | Cấu trúc trigger_evals/functional_evals |
| [13] | `evals/run-trigger-eval.sh` | Cơ chế trigger eval, --max-turns 1 |
| [14] | `evals/run-functional-eval.sh` | Cơ chế functional eval, 5 test thật |
| [15] | `tests/test-hooks.js` | 27 test case cho enforce-paths.js (không nhầm với dashboard.test.js — 30 scenario, file khác) |
| [16] | `hooks/session-start.js` | Due-check nhẹ, không nạp toàn bộ hồ sơ |
| [17] | `hooks/enforce-paths.js` | Validator ghi file, string-match + whitelist |
| [18] | `skills/dashboard/server/index.js`, `sse.js`, `validate.js` | Kiến trúc dashboard, SSE streaming CLI, validate thủ công |
| [19] | `CLAUDE.md` | Kiến trúc 3 lớp, không persona |
| [20] | `skills/dashboard/server/index.js`, `sse.js`, `validate.js` | Kiến trúc dashboard, SSE streaming CLI, validate thủ công |

## 8. Bản đồ độ mới

Repo hoạt động vừa phải (115 sao, push gần nhất 20/07/2026) — chậm hơn nhiều so với Superpowers nhưng vẫn đang duy trì. Rủi ro cao nhất không phải nội dung đổi mà là **độ chính xác trích dẫn nguyên văn** (WebFetch qua model tóm lược) — đã ghi rõ ở mỗi mục cần trích dẫn chính thức.

**Mốc tái xác minh:** nếu Vấn Đạo quyết định áp dụng Khuyến nghị #1 (eval 2 tầng) vào epic thật, đọc lại `evals/evals.json`, `run-trigger-eval.sh`, `run-functional-eval.sh` bằng công cụ đọc thô (curl, không qua WebFetch tóm lược) để lấy cấu trúc chính xác 100% trước khi viết story.
