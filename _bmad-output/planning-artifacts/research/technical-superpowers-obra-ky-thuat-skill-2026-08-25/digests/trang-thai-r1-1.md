# Digest R1-1 — Superpowers (obra): Giữ trạng thái / quy trình nhiều bước

**Phạm vi:** skills/writing-plans, skills/executing-plans, skills/using-git-worktrees, skills/finishing-a-development-branch, hooks/
**Ngày truy cập:** 2026-08-25
**Publisher chung:** GitHub (obra/superpowers), pub_date: N/A

---

## 1. writing-plans/SKILL.md — nơi lưu và hình dạng plan

- {claim: "Plan mặc định được lưu tại đường dẫn `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`, người dùng có thể ghi đè vị trí này.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-plans/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Mọi plan phải mở đầu bằng header chuẩn gồm: tên feature làm H1 '... Implementation Plan', rồi các trường **Goal** (1 câu), **Architecture** (2-3 câu), **Tech Stack**, **Spec** (đường dẫn tới spec/design doc), cộng thêm phần 'Global Constraints' liệt kê yêu cầu toàn cục từ spec.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-plans/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Mỗi task trong plan theo mẫu cố định: '### Task N: [Component Name]' kèm mục **Files** (Create/Modify paths), **Interfaces** (Consumes/Produces với signature chính xác), và danh sách checkbox '- [ ] **Step:** [action kèm code block]'.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-plans/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Nguyên tắc thiết kế plan: cấm placeholder ('TBD', 'TODO', 'similar to Task N'), mỗi step phải bite-sized (2-5 phút: viết test → chạy → implement → commit), và phải ánh xạ cấu trúc file trước khi định nghĩa task theo nguyên tắc 'split by responsibility, not by technical layer'.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-plans/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Sau khi viết xong, skill yêu cầu tự kiểm tra plan: spec coverage (mỗi yêu cầu trong spec có task tương ứng), placeholder scan (quét các cụm từ cấm), và type consistency (tên hàm/signature khớp nhau xuyên plan).", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-plans/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

**Nhận xét đối chiếu (không phải claim từ nguồn, chỉ ghi chú phân tích):** Plan là một file markdown tĩnh nằm trong repo (`docs/superpowers/plans/...`), không phải một log/state-file động — khác về bản chất so với memlog.py (ghi log runtime có timestamp/append liên tục).

---

## 2. executing-plans/SKILL.md — theo dõi tiến độ / resume

- {claim: "Quy trình thực thi plan gồm 3 bước chính: (1) Load and Review Plan — tạo workspace, đọc kế hoạch, xác định mối lo ngại; (2) Execute Tasks — đánh dấu trạng thái, thực hiện từng bước, xác minh; (3) Complete Development — gọi skill finishing-a-development-branch.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/executing-plans/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Ở bước 'Execute Tasks', cơ chế theo dõi trạng thái từng task là: (1) Mark as in_progress, (2) Follow each step exactly, (3) Run verifications, (4) Mark as completed — tức trạng thái nhị nguyên in_progress → completed cho mỗi task, không thấy mô tả nơi lưu trạng thái này (có thể là TodoWrite/task list nội bộ của Claude Code chứ không phải file riêng).", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/executing-plans/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "medium", class: "pattern"}
- {claim: "SKILL.md không mô tả cơ chế resume/checkpoint nào; chỉ có một section 'When to Stop and Ask for Help' liệt kê các tình huống phải dừng ngay (gặp blocker, test fail, instruction không rõ ràng) — nghĩa là không có state file cho phép tiếp tục phiên làm việc dở dang.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/executing-plans/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "medium", class: "pattern"}

**Nhận xét đối chiếu:** Đây là khác biệt cốt lõi so với memlog.py — Superpowers dựa vào bản thân file plan markdown (đã có sẵn checklist `- [ ]`) làm "nguồn sự thật" duy nhất về tiến độ, cộng với trạng thái tác vụ tạm thời (todo list) trong phiên hội thoại; không có log trạng thái ghi liên tục ra đĩa để resume across sessions như memlog.py.

---

## 3. using-git-worktrees/SKILL.md — worktree như cơ chế cách ly/checkpoint

- {claim: "Overview của skill: 'Ensure work happens in an isolated workspace. Prefer your platform's native worktree tools.' — worktree được dùng để tạo một thư mục làm việc tách biệt, liên kết với cùng repo git, nhằm bảo vệ nhánh chính khỏi các thay đổi đang diễn ra.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/using-git-worktrees/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Step 0 (Detection): 'Before creating anything, check if you are already in an isolated workspace' — kiểm tra bằng cách so sánh GIT_DIR != GIT_COMMON (loại trừ submodule) để phát hiện đã ở trong worktree từ trước hay chưa.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/using-git-worktrees/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Step 1 tạo worktree theo 2 cơ chế ưu tiên: 1a) dùng native tool của platform nếu có (tự xử lý vị trí và cleanup); 1b) fallback thủ công bằng lệnh git: `git worktree add \"$path\" -b \"$BRANCH_NAME\"`.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/using-git-worktrees/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Step 3 yêu cầu chạy test suite ngay sau khi tạo worktree để xác nhận 'workspace starts clean' — thiết lập baseline trước khi bắt đầu implement.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/using-git-worktrees/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Tài liệu KHÔNG mô tả quy trình revert/rollback hay cơ chế phục hồi trạng thái tường minh nào; nguyên tắc nêu ra là 'Never fight the harness' và việc cleanup được 'owned' bởi native tools.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/using-git-worktrees/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "medium", class: "pattern"}

**Nhận xét đối chiếu (đã biết Cline "đảo ngược rẻ" từ nghiên cứu trước, không có trong brief này — chỉ ghi chú phân tích không phải claim mới):** Cơ chế của Superpowers khác về bản chất: worktree là cách ly không gian làm việc (workspace isolation, cấp thư mục/branch git) để tránh xung đột với nhánh chính, không phải checkpoint/snapshot từng bước cho phép "tua lại" một hành động cụ thể như snapshot-per-action của Cline. Không có bằng chứng trong skill này về undo tại mức fine-grained.

---

## 4. finishing-a-development-branch/SKILL.md — quy trình đóng nhánh

- {claim: "Step 1 (Verify Tests): phải chạy full test suite của dự án (npm test / cargo test / pytest / go test ./...); nếu test fail thì báo lỗi và dừng lại, chỉ tiếp tục khi test suite xanh.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/finishing-a-development-branch/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Step 2 (Detect Environment) phân biệt normal repo (GIT_DIR == GIT_COMMON) với worktree có named branch hoặc detached HEAD, để chọn nhánh xử lý phù hợp ở bước sau.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/finishing-a-development-branch/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Step 3 (Determine Base Branch): 'The base branch is whatever this work forked from — usually named in the plan, the conversation, or the branch's upstream', và phải xác nhận trước khi merge vì 'merging into the wrong base is expensive to undo'.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/finishing-a-development-branch/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Step 4 đưa ra menu tùy chọn khác nhau theo môi trường: với normal repo/named-branch worktree có 3 lựa chọn (merge locally về base branch, push + tạo PR, giữ nguyên nhánh xử lý sau); với detached HEAD có 2 lựa chọn (push thành nhánh mới + tạo PR, hoặc giữ nguyên).", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/finishing-a-development-branch/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Nếu chọn push PR, worktree được giữ lại nguyên văn: 'Keep the worktree — your human partner iterates on PR feedback there'; nếu merge locally thì test lại rồi cleanup worktree và xóa nhánh.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/finishing-a-development-branch/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Có lựa chọn Discard nhưng chỉ khi user yêu cầu rõ ràng, đòi hỏi xác nhận tường minh bằng cách gõ 'discard' trước khi xóa force.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/finishing-a-development-branch/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Nếu worktree bị git từ chối remove do có uncommitted files, skill yêu cầu hỏi user 3 lựa chọn (commit / move / delete) thay vì tự ý xử lý.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/finishing-a-development-branch/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

---

## 5. hooks/ — quản lý session/trạng thái

- {claim: "Thư mục hooks/ của obra/superpowers (nhánh main) chứa đúng 4 file: hooks-cursor.json, hooks.json, run-hook.cmd, session-start.", source: "https://api.github.com/repos/obra/superpowers/contents/hooks", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "hooks.json khai báo một hook loại 'SessionStart' với matcher pattern 'startup|clear|compact' (kích hoạt khi startup, clear, hoặc compact), gọi lệnh '${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd session-start' qua shell bash, chạy đồng bộ (async: false).", source: "https://raw.githubusercontent.com/obra/superpowers/main/hooks/hooks.json", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Script session-start chỉ đọc (read-only) nội dung file `skills/using-superpowers/SKILL.md` trong plugin, escape nó để nhúng vào JSON, rồi xuất ra dưới dạng context bổ sung ('EXTREMELY_IMPORTANT' message) cho model — định dạng output khác nhau tùy platform: Cursor dùng `additional_context`, Claude Code dùng `hookSpecificOutput.additionalContext`, Copilot CLI dùng `additionalContext`.", source: "https://raw.githubusercontent.com/obra/superpowers/main/hooks/session-start", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Hook session-start KHÔNG lưu hay ghi bất kỳ trạng thái/tiến độ nào ra đĩa — không có file I/O ghi (write), chỉ đọc một file skill tĩnh. Nói cách khác, hooks/ của Superpowers không đóng vai trò một cơ chế quản lý session/state như memlog.py; nó chỉ là cơ chế 'bơm' hướng dẫn skill vào context mỗi khi phiên khởi động/clear/compact.", source: "https://raw.githubusercontent.com/obra/superpowers/main/hooks/session-start", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

---

## Ghi chú tổng hợp (không phải claim, chỉ là khung phân tích cho bước đối chiếu sau)

Framework Superpowers không có một "state/log file" tập trung kiểu memlog.py để theo dõi tiến độ nhiều bước xuyên phiên. Thay vào đó, "trạng thái" được phân tán vào 3 chỗ có bản chất khác nhau:
1. Bản thân file plan markdown tĩnh (checklist `- [ ]` trong `docs/superpowers/plans/...`) — đóng vai trò nguồn sự thật cho tiến độ task, nhưng là artifact do người/agent viết tay và cập nhật thủ công, không phải log tự động.
2. Trạng thái task tạm thời trong phiên (in_progress/completed) — không rõ cơ chế lưu trữ bền vững, không có mô tả resume across session.
3. Worktree git — cách ly không gian làm việc ở cấp filesystem/branch, không phải checkpoint/snapshot hành vi.
Hook session-start chỉ bơm context tĩnh, không liên quan đến theo dõi tiến độ.
