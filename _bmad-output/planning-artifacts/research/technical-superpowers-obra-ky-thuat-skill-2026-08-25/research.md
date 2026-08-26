---
title: 'technical research: Superpowers (obra) — kỹ thuật viết skill Claude Code'
type: 'technical'
topic: 'Superpowers (obra/superpowers) — kỹ thuật viết skill Claude Code, đối chiếu BMAD-METHOD'
decision: 'Cách viết SKILL.md/agents/hooks của Vấn Đạo — góc nhìn đa chiều, đối chiếu BMAD'
source: 'Native run — web thật, kéo trực tiếp file gốc github.com/obra/superpowers (branch main)'
status: complete
spot_check: '6/6 claims matched source (2026-08-26)'
preset: 'standard'
validation: 'normal'
claims_verified: 3
claims_unverified: 0
created: '2026-08-25'
updated: '2026-08-26'
---

# technical research: Superpowers (obra) — kỹ thuật viết skill Claude Code

**Decision this research serves:** Đối chiếu chéo kỹ thuật viết SKILL.md của BMAD-METHOD (đã nghiên cứu trước) với Superpowers — framework 277k sao trên GitHub, cùng nền tảng Claude Code nhưng triết lý thiết kế khác hẳn (TDD-driven, evidence-based, tự nhận lệch khỏi hướng dẫn chính thức của Anthropic) — để biết kỹ thuật nào của BMAD là "chuẩn ngành" và kỹ thuật nào chỉ là lựa chọn riêng.

## 1. Tóm tắt điều hành

Superpowers là "complete software development methodology" gồm 14 skill trong `skills/`, tổ chức thành 7-bước quy trình cơ bản (brainstorming → worktree → writing-plans → subagent-driven-development → TDD → code-review → finishing-branch) [4]. Bốn phát hiện thay đổi cách nhìn kỹ thuật viết skill so với lượt nghiên cứu BMAD:

1. **Viết skill là TDD thực nghiệm, có eval, có A/B test** — không phải chỉ prose có kinh nghiệm. `writing-skills/SKILL.md` (679 dòng, chính nó là skill dạy viết skill) quy định chu trình RED (baseline fail không skill) → GREEN (skill tối thiểu) → REFACTOR, với bằng chứng A/B test cụ thể rằng **prohibition-list guidance có thể tệ hơn không có hướng dẫn nào** khi loại lỗi là "output sai hình dạng" [3].
2. **"Description = khi nào dùng, KHÔNG BAO GIỜ tóm tắt workflow"** — có bằng chứng thực nghiệm trực tiếp: khi description tóm tắt quy trình, agent làm theo bản tóm tắt rút gọn thay vì đọc skill đầy đủ (case cụ thể: agent chỉ review 1 lần thay vì 2 vì description nói "code review between tasks") [3].
3. **Có quy tắc số-từ tường minh** BMAD không có: <150 từ (skill nạp mọi hội thoại), <200 từ (skill tải thường xuyên), <500 từ (skill khác); ngưỡng tách file 100+ dòng [3].
4. **Không có cơ chế resume/state xuyên phiên nào** tương đương memlog.py — plan là file markdown tĩnh, tiến độ task là nhị nguyên in_progress/completed không rõ nơi lưu bền vững, và tài liệu chỉ nói "dừng ngay khi gặp blocker" [11][12].
5. **Superpowers công khai tuyên bố lệch khỏi hướng dẫn chính thức của Anthropic** về viết skill, dựa trên eval thực nghiệm riêng — PR nào "compliance-hoá" theo tài liệu Anthropic sẽ bị từ chối nếu không có bằng chứng cải thiện outcome [5].

**Cảnh báo:** đây là quan sát MỘT framework nữa (cùng BMAD là hai), không phải "chuẩn ngành" — nhiều kỹ thuật ở đây (Iron Law viết hoa, thẻ giả-XML, bảng Red Flags) là lựa chọn thiết kế có chủ đích của Superpowers, được kiểm chứng bằng eval riêng của họ, không nhất thiết chuyển được nguyên trạng sang bối cảnh khác.

## 2. Theo từng chiều

### 2.1 Cấu trúc & giao thức skill

`.claude-plugin/plugin.json` chỉ là metadata tối giản (name/version/author/license/keywords) — **không liệt kê danh sách skill** [1]; khám phá skill dựa vào cấu trúc thư mục `skills/<name>/SKILL.md` theo "flat namespace" [3]. Khác biệt lớn với BMAD: Superpowers có một skill "cổng vào hành vi" (`using-superpowers`) nạp vào **mọi hội thoại**, ép agent kiểm tra skill liên quan trước MỌI phản hồi — "if you think there is even a 1% chance a skill might apply... you ABSOLUTELY MUST invoke it" [2]. Cơ chế điều hướng không phải menu tường minh mà là bảng "Red Flags" — 12 lối ngụy biện phổ biến kèm phản bác, chặn agent bỏ qua bước kiểm tra skill [2]. Có quy tắc ưu tiên: process skills (brainstorming, systematic-debugging) đi trước implementation skills [2], và user instructions (CLAUDE.md/AGENTS.md) > skills > default behavior [2]. Đáng chú ý: có khối `<SUBAGENT-STOP>` tường minh nói rõ quy tắc bootstrap này **không áp dụng cho subagent được dispatch** — chỉ áp cho agent chính [2].

CLAUDE.md của repo (không phải hướng dẫn dùng skill, mà là contributor guidelines cho AI agent muốn gửi PR) mở đầu cảnh báo tỷ lệ từ chối PR 94% [5], và xác nhận tường minh: **triết lý viết skill của Superpowers khác hướng dẫn chính thức Anthropic**, "extensively tested and tuned for real-world agent behavior" — PR "compliance-hoá" theo Anthropic sẽ bị từ chối trừ khi có eval chứng minh cải thiện [5]. Cũng có quy tắc "skill đặc thù domain không thuộc core" — phép thử: "would this be useful to someone working on a completely different kind of project? If not, publish it separately" [5], và yêu cầu chứng minh tích hợp harness mới bằng acceptance test cụ thể (gửi đúng một câu, brainstorming phải tự trigger trước khi có code) [5].

### 2.2 Cơ chế "Evidence before claims" / TDD-driven (kỹ thuật chữ ký của Superpowers)

Đây là nguồn gốc thật của nguyên tắc Vấn Đạo đã trích dẫn cho R19 nhưng chưa đọc gốc. `verification-before-completion/SKILL.md` định nghĩa "evidence" là đầu ra thực tế đo được (kết quả test cụ thể, exit code, output linter, diff VCS) — không phải suy đoán [7]. Quy trình 5 bước bắt buộc trước khi báo cáo hoàn thành; bỏ bất kỳ bước nào là **"lying, not verifying"** — các cụm "should pass"/"probably works"/"seems correct" bị liệt vào FORBIDDEN, ăn mừng sớm ("Great!", "Done!") trước khi xác minh là red flag [7].

`test-driven-development/SKILL.md` có "Iron Law": **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST** — code viết trước test phải xoá sạch, không giữ "tham khảo" [6]. `systematic-debugging/SKILL.md` khoá cứng 4 pha tuần tự (Root Cause → Pattern Analysis → Hypothesis/Testing → Implementation), cấm đề xuất fix trước khi hoàn thành điều tra root cause, và nối trực tiếp với verification-before-completion ở pha cuối [8]. Hai vai review tách biệt: `receiving-code-review` cấm ngôn từ xu nịnh, bắt buộc verify-before-implement, nhưng cũng cho phép push back có lý do kỹ thuật [9]; `requesting-code-review` là vai điều phối — gửi việc cho subagent reviewer độc lập nhận ngữ cảnh chế tạo riêng (không phải lịch sử phiên), "review early, review often" [10].

### 2.3 Giữ trạng thái / quy trình nhiều bước

Đối lập mạnh với memlog.py của BMAD: **Superpowers không có state/log file tập trung nào cho tiến độ xuyên phiên**. Plan là một file markdown tĩnh tại `docs/superpowers/plans/YYYY-MM-DD-<feature>.md` với header chuẩn (Goal/Architecture/Tech Stack/Spec) và checklist `- [ ]` — bản thân file plan là "nguồn sự thật" duy nhất về tiến độ [11]. Thực thi task chỉ có trạng thái nhị nguyên in_progress→completed, không mô tả nơi lưu bền vững, và tài liệu không có cơ chế resume/checkpoint — chỉ có mục "When to Stop and Ask for Help" liệt kê tình huống phải dừng ngay [12].

Worktree (`using-git-worktrees`) đóng vai trò cách ly không gian làm việc (filesystem/branch), có bước detect/verify baseline sạch, nhưng **không** mô tả revert/rollback hay snapshot fine-grained — khác bản chất với "đảo ngược rẻ" per-action kiểu Cline [13]. Đóng nhánh (`finishing-a-development-branch`) có quy trình chặt: test xanh bắt buộc → xác nhận base branch đúng (vì merge sai base "expensive to undo") → menu merge/PR/giữ nguyên, discard đòi gõ "discard" xác nhận [14]. Hook `session-start` (trigger startup|clear|compact) chỉ **đọc tĩnh** `using-superpowers/SKILL.md` rồi bơm vào context — hoàn toàn không ghi/lưu trạng thái nào [15][16][17].

### 2.4 Điều phối subagent

Hai kỹ thuật dispatch khác cấp độ chặt: `dispatching-parallel-agents` — nguyên tắc "một agent mỗi domain độc lập" [18], nhưng **không có digest contract chuẩn hoá**, chỉ yêu cầu định tính "specific about output" [18]. `subagent-driven-development` chặt hơn nhiều: implementer ghi report đầy đủ vào file, chỉ trả về **status (1/4 giá trị cố định: DONE/DONE_WITH_CONCERNS/NEEDS_CONTEXT/BLOCKED) + commits + one-line test summary + concerns** [19] — cùng tinh thần "extract don't ingest" của BMAD nhưng contract cụ thể hơn digest contract của bmad-deep-recon.

Quy tắc chống ô nhiễm ngữ cảnh áp cho cả hai chiều: "everything you paste into a dispatch prompt — and everything a subagent prints back — stays resident in your context... hand artifacts over as files" [19]. Controller (agent điều phối) **bị cấm tự sửa code trực tiếp** — "controller fixes pollute your context and skip review" [19]. Có quy tắc cấm subagent tự dispatch subagent khác (kể cả reviewer): "every reviewer a worker spawned duplicated the task review the controller dispatched anyway" [19]. Và quy tắc chống phân mảnh: batch nhiều fix nhỏ đồng dạng vào MỘT dispatch thay vì một subagent mỗi fix, dẫn chứng "a real session's final-review fix wave cost more than all its tasks combined" [19]. Đáng chú ý: `brainstorming/SKILL.md` **hoàn toàn không đề cập** điều phối nhiều subagent — chốt bằng HARD-GATE phê duyệt của người dùng, không dispatch [20].

### 2.5 Văn phong hướng dẫn model

Khác biệt cấu trúc rõ với BMAD: Superpowers **không gán persona "You are X"** nào — thân skill dùng giọng mệnh lệnh ngôi hai trực tiếp ("Write the test first. Watch it fail.") [6], nhưng trường `description` trong frontmatter lại bị **ép ngôi ba tường minh** ("Write in third person") vì nó được nhúng vào system prompt [3][6]. Không dùng "user" mà nhất quán "your human partner" [6].

Ép trình tự bằng nhiều lớp: numbered steps, khối "Iron Law" viết hoa trong code-fence (TDD và writing-skills dùng cấu trúc giống hệt: "NO PRODUCTION CODE WITHOUT..." / "NO SKILL WITHOUT...") [3][6], và thẻ giả-XML tuỳ biến ngoài chuẩn Markdown (`<HARD-GATE>`, `<EXTREMELY-IMPORTANT>`, `<SUBAGENT-STOP>`) [20][2]. Bảng "Thought/Excuse | Reality" lặp lại ở cả 4 file khảo sát — device chuẩn hoá cấp framework chống ngụy biện, không phải ngẫu nhiên [2][20][6][3].

Có mẫu "một tiêu chí quyết định" tương đương chức năng "one test decides" của BMAD nhưng không trùng cụm từ: "would the user understand this better by seeing it than reading it?" quyết định browser/terminal [20]; bảng "Match the Form to the Failure" quy về 4 loại baseline failure ánh xạ 1-1 sang dạng hướng dẫn đúng [3]. Độ dài đo được: using-superpowers 63 dòng, brainstorming 250, TDD 320, writing-skills 679 (dài nhất — vì tự nó dạy viết skill) [6][20][3].

## 3. Phát hiện xuyên chiều

1. **Hai epistemology khác nhau cho "skill tốt là gì": prose-có-kinh-nghiệm (BMAD) vs. thực-nghiệm-có-eval (Superpowers).** BMAD's SKILL.md được viết và tinh chỉnh qua kinh nghiệm/coaching iteratively; Superpowers đòi hỏi mỗi skill phải qua RED-GREEN-REFACTOR với pressure-testing subagent, A/B test giữa các dạng hướng dẫn, và "variance giữa 5 reps" như thước đo độ chặt của wording [3]. Đây không phải "cách nào đúng hơn" — là hai cách đặt cược khác nhau về chi phí kiểm chứng.

2. **"Trạng thái xuyên phiên" là điểm BMAD mạnh hơn hẳn, không phải điểm yếu cần sửa.** Superpowers hoàn toàn không có cơ chế tương đương memlog — dựa vào file plan tĩnh + trạng thái tạm trong phiên hội thoại. Với Vấn Đạo (khoá học kéo dài nhiều tuần, nhiều phiên, nhiều vai), đây xác nhận: memlog-style append-only log (đã có ở AD-2 kiến trúc spine) là lựa chọn đúng cho bài toán của Vấn Đạo, không phải thứ cần "học thêm" từ Superpowers.

3. **Digest contract của subagent-driven-development (4 giá trị status cố định) chặt hơn mọi contract BMAD đã khảo sát** — đáng cân nhắc cho Vấn Đạo ở những chỗ dispatch subagent tươi có kết quả cần phân loại rõ (vd. Nghiệm Công Sứ trả `đạt`/`chưa`/`thiếu_du_kien` đã gần giống mẫu này).

## 4. Bằng chứng ngược

Không chạy red-team pass ở lượt nghiên cứu này (`red_team: off`) — không có mục nào ở phần này.

## 5. Khuyến nghị

1. **Cân nhắc thêm quy tắc số-từ tường minh cho SKILL.md của Vấn Đạo**, theo tầng tần suất nạp (giống Superpowers: skill nạp mọi phiên rất ngắn, skill ít tải có thể dài hơn) — BMAD không có quy tắc này, Superpowers có và giải thích rõ lý do (token budget). Độ tin: cao (quan sát trực tiếp, có công thức cụ thể `wc -w`). *Feed vào: cách viết SKILL.md cho `thu-linh` (nạp mỗi phiên) vs các skill ít tải hơn.*

2. **Cân nhắc quy tắc "description chỉ mô tả khi-nào-dùng, không tóm tắt workflow"** cho 8 vai của Vấn Đạo — có bằng chứng thực nghiệm cụ thể (không phải suy đoán) rằng tóm tắt workflow trong description khiến agent bỏ qua nội dung đầy đủ. Độ tin: cao (case cụ thể được dẫn). *Feed vào: cách viết frontmatter `description` cho `agents/*.md` của Vấn Đạo.*

3. **KHÔNG cần học "cơ chế resume xuyên phiên" từ Superpowers — Vấn Đạo đã đúng hướng hơn.** Xác nhận AD-2 (event-sourced, memlog-style) của architecture spine là lựa chọn phù hợp cho một sản phẩm nhiều-tuần-nhiều-phiên; Superpowers giải bài toán khác (một phiên làm việc dev, ngắn hơn nhiều). Độ tin: cao. *Feed vào: không cần hành động, xác nhận hướng đã chọn.*

4. **Cân nhắc digest contract "status cố định 4 giá trị" cho những nơi Vấn Đạo dispatch subagent tươi cần phân loại kết quả rõ** (Nghiệm Công Sứ, Phúc Khảo Sứ, sơn phong trưởng lão) — hiện đã có mầm mống (`đạt`/`chưa`/`thieu_du_kien`) nhưng chưa chuẩn hoá tường minh thành một tập giá trị cố định trong architecture spine. Độ tin: trung bình (một gợi ý cấu trúc, chưa kiểm chứng ở build thật). *Feed vào: story cho FR-Soát, có thể là AD-10 nếu spine reopen.*

5. **Cân nhắc kỹ thuật "Match the Form to the Failure" khi viết luật cho Vấn Đạo** — chọn đúng dạng hướng dẫn (cấm đoán vs. recipe tích cực vs. structural required-field) theo LOẠI lỗi baseline quan sát được, thay vì mặc định dùng "Never X" cho mọi luật. Độ tin: trung bình (một khung tư duy viết luật, hữu ích nhưng chưa test trên chính Vấn Đạo). *Feed vào: cách viết luật trong SKILL.md cho mọi vai, đặc biệt các quy tắc chống ngụy biện.*

6. **Không cần copy "Iron Law" viết hoa/thẻ giả-XML** trực tiếp — đây là lựa chọn văn phong đặc thù được Superpowers tự eval, không có bằng chứng nó chuyển sang bối cảnh thế giới quan tu luyện của Vấn Đạo mà không phá vỡ giọng điệu đã chọn (FR33). Độ tin: trung bình (thận trọng, không phải phát hiện tích cực). *Feed vào: không áp dụng nguyên trạng, chỉ tham khảo nguyên lý.*

## 6. Câu hỏi còn mở

1. Superpowers thực sự chạy eval pressure-scenario với tần suất nào trong quá trình phát triển thật (liên tục mỗi PR, hay chỉ lúc viết skill mới)? — writing-skills.md mô tả quy trình nhưng không nêu tần suất vận hành thật trong CI.
2. `hooks-cursor.json` (file thứ hai trong `hooks/`, ngoài `hooks.json`) chưa được đọc — có khác biệt hành vi gì giữa Cursor và Claude Code không?
3. `references/codex-tools.md`, `references/pi-tools.md` và các file platform-adaptation khác chưa đọc — nội dung thích ứng đa nền tảng cụ thể là gì?
4. Chưa xác nhận được ngày commit cuối (pub_date) của từng file — WebFetch/curl trên raw.githubusercontent.com không trả metadata Git; cần `gh api repos/obra/superpowers/commits?path=<file>` nếu cần độ chính xác cao hơn cho staleness map.
5. `testing-skills-with-subagents.md`, `persuasion-principles.md`, `anthropic-best-practices.md` (trỏ từ writing-skills.md) chưa đọc — đặc biệt `anthropic-best-practices.md` có thể trực tiếp trả lời "Superpowers lệch Anthropic ở điểm cụ thể nào".

## 7. Phụ lục nguồn

Mọi nguồn dưới đây: publisher "GitHub (obra/superpowers)" · pub_date N/A (không xác định được qua raw file, xem Câu hỏi mở #4) · truy cập 2026-08-25 · độ tin Cao (đọc trực tiếp file gốc qua WebFetch/curl, branch `main`, không cần fallback).

| # | Nguồn | Hỗ trợ phát hiện |
|---|---|---|
| [1] | `.claude-plugin/plugin.json` | Metadata tối giản, không liệt kê skill |
| [2] | `skills/using-superpowers/SKILL.md` | Skill cổng vào, bảng Red Flags, ưu tiên process-skill, SUBAGENT-STOP |
| [3] | `skills/writing-skills/SKILL.md` | TDD-cho-skill, SDO, quy tắc số-từ, Match Form to Failure, Iron Law |
| [4] | `README.md` | Basic Workflow 7 bước, 4 trụ triết lý |
| [5] | `CLAUDE.md` | Contributor guidelines, lệch chuẩn Anthropic có chủ đích, domain-skill tách plugin riêng |
| [6] | `skills/test-driven-development/SKILL.md` | Iron Law TDD, Red-Green-Refactor 5 bước, ngôi 2 mệnh lệnh, "your human partner" |
| [7] | `skills/verification-before-completion/SKILL.md` | Nguồn gốc "evidence before claims", quy trình 5 bước, FORBIDDEN phrases |
| [8] | `skills/systematic-debugging/SKILL.md` | 4 pha khoá cứng, root-cause-first |
| [9] | `skills/receiving-code-review/SKILL.md` | Verify-before-implement, cấm xu nịnh, cho phép push back |
| [10] | `skills/requesting-code-review/SKILL.md` | Vai điều phối review, ngữ cảnh chế tạo riêng cho reviewer |
| [11] | `skills/writing-plans/SKILL.md` | Plan là file markdown tĩnh, header chuẩn, cấm placeholder |
| [12] | `skills/executing-plans/SKILL.md` | Trạng thái nhị nguyên, không có resume/checkpoint |
| [13] | `skills/using-git-worktrees/SKILL.md` | Cách ly workspace, không phải checkpoint fine-grained |
| [14] | `skills/finishing-a-development-branch/SKILL.md` | Quy trình đóng nhánh, xác nhận base branch, discard có gate |
| [15] | `api.github.com/repos/obra/superpowers/contents/hooks` | Danh sách file trong hooks/ |
| [16] | `hooks/hooks.json` | SessionStart matcher startup|clear|compact |
| [17] | `hooks/session-start` | Chỉ đọc tĩnh, không ghi trạng thái |
| [18] | `skills/dispatching-parallel-agents/SKILL.md` | Một agent/domain, không có digest contract chuẩn hoá |
| [19] | `skills/subagent-driven-development/SKILL.md` | Contract 4-giá-trị status, cấm controller tự sửa code, chống phân mảnh dispatch |
| [20] | `skills/brainstorming/SKILL.md` | Không điều phối subagent, HARD-GATE phê duyệt, thẻ giả-XML |

## 8. Bản đồ độ mới

Nguồn là mã nguồn của một repo đang hoạt động tích cực (277k sao, push gần nhất 19/08/2026, 24.815 fork) — khác hẳn BMAD (đọc từ chính workspace, không đổi ngoài ý muốn) hay tài liệu chính chủ tĩnh. **Rủi ro độ mới cao hơn hai nguồn kia**: nội dung SKILL.md có thể đổi bất cứ lúc nào theo PR mới (dù CLAUDE.md nói rõ nội dung định hình hành vi cần eval mới được merge, nên tốc độ đổi có kiểm soát). Chưa xác định được pub_date từng file (Câu hỏi mở #4).

**Mốc tái xác minh:** trước khi Vấn Đạo áp dụng bất kỳ khuyến nghị nào ở §5 vào SKILL.md thật, kiểm tra lại phiên bản hiện tại của `writing-skills/SKILL.md` (nguồn của phần lớn khuyến nghị) — đặc biệt các con số cụ thể (150/200/500 từ, ngưỡng 100 dòng) vì đây là quy tắc nội bộ có thể được điều chỉnh qua các lần eval tiếp theo của chính Superpowers.
