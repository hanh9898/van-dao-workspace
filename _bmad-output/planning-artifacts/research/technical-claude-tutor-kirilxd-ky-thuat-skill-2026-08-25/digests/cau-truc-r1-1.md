# Digest: claude-tutor (kirilxd) — Cấu trúc & kiến trúc plugin dạy học

Chủ đề: kỹ thuật viết plugin dạy học "claude-tutor" trên Claude Code, chiều
"Cấu trúc & kiến trúc plugin dạy học". Phục vụ quyết định thiết kế cho plugin
"Vấn Đạo" (sách PDF/EPUB → lộ trình học, 8 vai/subagent).

Nguồn: repo GitHub `kirilxd/claude-tutor`, nhánh `main` (không có 404, không
cần thử `master`). Tất cả finding lấy trực tiếp từ raw.githubusercontent.com
qua WebFetch, không suy diễn từ kiến thức nền.

---

## Câu hỏi 1 — plugin.json và marketplace.json khai báo gì

**F1.1**
- claim: `.claude-plugin/plugin.json` khai báo plugin với `name: "claude-tutor"`, `version: "1.0.0"`, `description`, `author.name: "kirilxd"`, `license: "MIT"`, `keywords: ["learning","education","quiz","study","tutor"]` — không có trường `commands`, `skills`, hay `agents` liệt kê tường minh trong manifest (các thư mục này được nạp theo quy ước thư mục chuẩn của Claude Code, không cần khai báo path trong plugin.json).
- source: https://raw.githubusercontent.com/kirilxd/claude-tutor/main/.claude-plugin/plugin.json
- publisher: GitHub (kirilxd/claude-tutor)
- pub_date: N/A
- accessed: 2026-08-25
- confidence: high
- class: pattern

**F1.2**
- claim: `plugin.json` khai báo khối `hooks` ngay trong manifest (không phải file `hooks.json` riêng), gồm 2 hook: `PreToolUse` với `matcher: "Write|Edit"` gọi `node ${CLAUDE_PLUGIN_ROOT}/hooks/enforce-paths.js` (chặn/kiểm tra đường dẫn ghi file trước khi Write/Edit chạy), và `SessionStart` gọi `node ${CLAUDE_PLUGIN_ROOT}/hooks/session-start.js`. Biến `${CLAUDE_PLUGIN_ROOT}` được dùng để tham chiếu thư mục gốc plugin một cách portable.
- source: https://raw.githubusercontent.com/kirilxd/claude-tutor/main/.claude-plugin/plugin.json
- publisher: GitHub (kirilxd/claude-tutor)
- pub_date: N/A
- accessed: 2026-08-25
- confidence: high
- class: pattern

**F1.3**
- claim: `.claude-plugin/marketplace.json` là manifest marketplace riêng (khác plugin.json), theo schema `https://anthropic.com/claude-code/marketplace.schema.json`, khai báo `name: "kirilxd-plugins"`, `owner.name: "kirilxd"`, và mảng `plugins` với 1 entry `claude-tutor` có `source: {"source":"github","repo":"kirilxd/claude-tutor"}` và `description` riêng (ngắn hơn, khác câu chữ so với description trong plugin.json). Đây là cơ chế để người dùng cài qua `/plugin marketplace add kirilxd/claude-tutor` rồi `/plugin install claude-tutor@kirilxd-plugins`.
- source: https://raw.githubusercontent.com/kirilxd/claude-tutor/main/.claude-plugin/marketplace.json
- publisher: GitHub (kirilxd/claude-tutor)
- pub_date: N/A
- accessed: 2026-08-25
- confidence: high
- class: pattern

---

## Câu hỏi 2 — 5 skill (learn, quiz, resources, review, dashboard) chia việc thế nào

**F2.1**
- claim: Mỗi skill có `SKILL.md` với frontmatter YAML `name` + `description` mô tả trigger ngôn ngữ tự nhiên cụ thể (ví dụ skill `quiz`: "Triggers on 'quiz me', 'test me', 'test my knowledge', 'practice questions', 'check my understanding'..."; skill `resources`: "Triggers on 'find me resources', 'what should I read about', 'best tutorials for'..."; skill `dashboard`: dùng "only when user explicitly asks to 'open dashboard'..."). Đây là cơ chế Claude Code tự chọn skill dựa trên mô tả, không chỉ qua slash command.
- source: https://raw.githubusercontent.com/kirilxd/claude-tutor/main/skills/quiz/SKILL.md ; https://raw.githubusercontent.com/kirilxd/claude-tutor/main/skills/resources/SKILL.md ; https://raw.githubusercontent.com/kirilxd/claude-tutor/main/skills/dashboard/SKILL.md
- publisher: GitHub (kirilxd/claude-tutor)
- pub_date: N/A
- accessed: 2026-08-25
- confidence: high
- class: pattern

**F2.2**
- claim: Ranh giới trách nhiệm rõ theo dữ liệu ghi/đọc: skill `learn` SỞ HỮU việc ghi `~/.claude/learning/plans/{slug}-{date}.json` (chỉ chứa modules/resources/goal/depth/timeCommitment, không được lẫn field quiz); skill `quiz` SỞ HỮU việc ghi `~/.claude/learning/progress/{slug}.json` (chỉ chứa quizzes/weakAreas/strongAreas/spacedRepetition, không được lẫn field plan). File `learn/SKILL.md` nêu tường minh quy tắc "Never add quiz fields... to plan files" và ngược lại — đây là ràng buộc kiến trúc cấp skill nhằm tránh xung đột ghi đè giữa các skill dùng chung một cây thư mục dữ liệu.
- source: https://raw.githubusercontent.com/kirilxd/claude-tutor/main/skills/learn/SKILL.md
- publisher: GitHub (kirilxd/claude-tutor)
- pub_date: N/A
- accessed: 2026-08-25
- confidence: high
- class: pattern

**F2.3**
- claim: Các skill đọc-only (`resources`, `review`) không tự sinh dữ liệu mới mà đọc lại schema do `learn` và `quiz` ghi ra — mỗi SKILL.md của chúng có mục riêng "Data Schemas" liệt kê tường minh cấu trúc `index.json`, plan files, progress files mà skill đó sẽ đọc. Đây là mô hình 1 nguồn ghi (learn/quiz) – nhiều nguồn đọc (resources/review/dashboard) trên cùng kho dữ liệu `~/.claude/learning/`.
- source: https://raw.githubusercontent.com/kirilxd/claude-tutor/main/skills/resources/SKILL.md ; https://raw.githubusercontent.com/kirilxd/claude-tutor/main/skills/review/SKILL.md
- publisher: GitHub (kirilxd/claude-tutor)
- pub_date: N/A
- accessed: 2026-08-25
- confidence: high
- class: pattern

**F2.4**
- claim: `~/.claude/learning/index.json` đóng vai trò registry trung tâm (master index) ánh xạ slug topic → `planFile`, `progressFile`, và các số liệu tổng hợp (`modulesCompleted`, `quizzesTaken`, `overallScore`...). Cả 5 skill đều tham chiếu file này làm điểm vào đầu tiên trước khi đọc/ghi file chi tiết — đây là pattern "chỉ mục trung tâm + file chi tiết theo entity" để tránh phải quét toàn bộ thư mục.
- source: https://raw.githubusercontent.com/kirilxd/claude-tutor/main/skills/review/SKILL.md ; https://raw.githubusercontent.com/kirilxd/claude-tutor/main/skills/learn/SKILL.md
- publisher: GitHub (kirilxd/claude-tutor)
- pub_date: N/A
- accessed: 2026-08-25
- confidence: high
- class: pattern

**F2.5**
- claim: Skill `learn` không chỉ tạo plan mà còn có "Phase 5: Teach" — dạy trực tiếp nội dung module một cách tương tác (giải thích khái niệm, dùng analogy, hỏi kiểm tra hiểu nhanh sau mỗi 2-3 khái niệm) — nghĩa là ranh giới giữa `learn` và `quiz` không phải "học vs kiểm tra" tuyệt đối; `learn` có cả bước dạy, còn `quiz` chuyên biệt cho việc kiểm tra có tính điểm/theo dõi tiến bộ dài hạn (SM-2).
- source: https://raw.githubusercontent.com/kirilxd/claude-tutor/main/skills/learn/SKILL.md
- publisher: GitHub (kirilxd/claude-tutor)
- pub_date: N/A
- accessed: 2026-08-25
- confidence: high
- class: pattern

**F2.6**
- claim: Skill `dashboard` khác biệt về bản chất so với 4 skill còn lại: nó không xử lý logic nghiệp vụ bằng LLM mà khởi chạy một local web server (Node.js, `http://localhost:3847`) để người dùng xem/sửa dữ liệu học tập bằng giao diện web, bao gồm cả lịch (calendar) cho spaced repetition — tách hẳn khỏi luồng hội thoại text-based của 4 skill kia.
- source: https://raw.githubusercontent.com/kirilxd/claude-tutor/main/skills/dashboard/SKILL.md
- publisher: GitHub (kirilxd/claude-tutor)
- pub_date: N/A
- accessed: 2026-08-25
- confidence: high
- class: pattern

---

## Câu hỏi 3 — quan hệ command/ và skill/ (khác BMAD chỉ có skill)

**F3.1**
- claim: File `commands/learn.md` là một Markdown "thin wrapper" có frontmatter riêng (`description`, `argument-hint: <topic>`, `allowed-tools: AskUserQuestion, WebSearch, WebFetch, Read, Write, Bash(mkdir *)`) — khai báo whitelist công cụ được phép dùng cho lệnh này — và phần thân chỉ nói: "Follow the `learn` skill instructions to: [checklist 9 bước tóm tắt]". Command KHÔNG chứa logic chi tiết (không lặp lại nội dung SKILL.md), nó chỉ là điểm vào slash-command trỏ tới skill và giới hạn quyền công cụ + tham số đầu vào (`$ARGUMENTS`).
- source: https://raw.githubusercontent.com/kirilxd/claude-tutor/main/commands/learn.md
- publisher: GitHub (kirilxd/claude-tutor)
- pub_date: N/A
- accessed: 2026-08-25
- confidence: high
- class: pattern

**F3.2**
- claim: `commands/quiz.md` theo cùng pattern: có `allowed-tools` riêng (AskUserQuestion, Read, Write, Bash mkdir) và cú pháp tham số mở rộng `--module N`, `--count N` ngoài topic — cho thấy lớp command đảm nhận việc parse tham số CLI-style (flags) mà lớp skill không xử lý.
- source: https://raw.githubusercontent.com/kirilxd/claude-tutor/main/commands/quiz.md
- publisher: GitHub (kirilxd/claude-tutor)
- pub_date: N/A
- accessed: 2026-08-25
- confidence: medium
- class: pattern

**F3.3**
- claim: `commands/dashboard.md` là ngoại lệ trong nhóm 5 command: nó KHÔNG trỏ ngược về skill `dashboard` bằng câu "follow the X skill", mà chứa trực tiếp 3 bước lệnh Bash cụ thể (`cd ${CLAUDE_PLUGIN_ROOT}/skills/dashboard/server && npm install --silent`, rồi `node .../index.js`, rồi thông báo URL) với `allowed-tools: Bash(node *), Bash(npm *), Bash(cd *)`. Điều này cho thấy quan hệ command↔skill không đồng nhất 100%: với skill hội thoại (learn/quiz/resources/review) command là pointer mỏng; với skill có server thực thi (dashboard) command chứa luôn quy trình khởi chạy vì đó là hành động máy móc, không cần "instructions" cho LLM diễn giải.
- source: https://raw.githubusercontent.com/kirilxd/claude-tutor/main/commands/dashboard.md
- publisher: GitHub (kirilxd/claude-tutor)
- pub_date: N/A
- accessed: 2026-08-25
- confidence: high
- class: pattern

**F3.4**
- claim: Có sự trùng lặp nội dung mô tả giữa command và skill (ví dụ cả `commands/quiz.md` và `skills/quiz/SKILL.md` đều mô tả "adaptive difficulty and mixed question formats") nhưng skill mới là nơi chứa toàn bộ quy trình chi tiết, schema dữ liệu và quy tắc; command chỉ tóm tắt lại ở mức tiêu đề/checklist — tức là command đóng vai "registration + entry point" còn skill đóng vai "spec hành vi đầy đủ", khác mô hình BMAD nơi chỉ có một lớp skill duy nhất làm cả hai việc.
- source: https://raw.githubusercontent.com/kirilxd/claude-tutor/main/commands/quiz.md ; https://raw.githubusercontent.com/kirilxd/claude-tutor/main/skills/quiz/SKILL.md
- publisher: GitHub (kirilxd/claude-tutor)
- pub_date: N/A
- accessed: 2026-08-25
- confidence: medium
- class: pattern

---

## Câu hỏi 4 — README.md nói gì về kiến trúc tổng thể

**F4.1**
- claim: README mô tả claude-tutor triển khai "a five-stage learning cycle: planning, studying, quizzing, reviewing, and repeating" — ánh xạ trực tiếp lên 5 skill (learn=planning/studying, quiz=quizzing, review=reviewing, dashboard=giao diện quản lý toàn cục, "repeating" ứng với spaced repetition SM-2 xuyên suốt quiz/review).
- source: https://raw.githubusercontent.com/kirilxd/claude-tutor/main/README.md
- publisher: GitHub (kirilxd/claude-tutor)
- pub_date: N/A
- accessed: 2026-08-25
- confidence: high
- class: pattern

**F4.2**
- claim: README khẳng định nguyên tắc kiến trúc dữ liệu: "All information remains local in `~/.claude/learning/`... Nothing transmits to external services" — toàn bộ state (plans, progress, profile, index) là file JSON cục bộ trên máy người dùng, không có backend/cloud sync, phù hợp với việc dashboard chỉ là local web server (localhost:3847) chứ không phải dịch vụ hosted.
- source: https://raw.githubusercontent.com/kirilxd/claude-tutor/main/README.md
- publisher: GitHub (kirilxd/claude-tutor)
- pub_date: N/A
- accessed: 2026-08-25
- confidence: high
- class: pattern

**F4.3**
- claim: README nêu yêu cầu kỹ thuật/hạ tầng đi kèm kiến trúc: "Node.js 18+ and Claude Code 2.0+", MIT license, và plugin "includes hook systems for data validation, comprehensive testing frameworks, and evaluation suites for trigger and functional testing" — cho thấy plugin có lớp kiểm thử/eval riêng ngoài 5 skill + hooks, không chỉ dừng ở logic hội thoại.
- source: https://raw.githubusercontent.com/kirilxd/claude-tutor/main/README.md
- publisher: GitHub (kirilxd/claude-tutor)
- pub_date: N/A
- accessed: 2026-08-25
- confidence: medium
- class: pattern

---

## Ghi chú phương pháp
- Không truy cập được README dưới dạng thô 100% nguyên văn (WebFetch trả về bản diễn giải/tóm tắt của model trung gian, không phải trích dẫn nguyên văn từng dòng) — các finding trên giữ nguyên câu chữ trong ngoặc kép khi WebFetch trích dẫn trực tiếp, phần còn lại là diễn giải có gắn nguồn.
- Không tìm thấy `CLAUDE.md` riêng ở root repo trong phạm vi các URL đã fetch (không được yêu cầu trong danh sách bắt buộc, không tự suy diễn có tồn tại hay không).
- Tất cả URL fetch thành công trên nhánh `main` — không cần fallback `master`.
