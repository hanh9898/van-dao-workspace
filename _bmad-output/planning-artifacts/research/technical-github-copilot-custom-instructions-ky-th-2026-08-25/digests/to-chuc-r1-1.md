# Digest — GitHub Copilot: tổ chức flow nhiều bước / nhiều mode

Chủ đề: chiều "đa-bước / đa-vai" của GitHub Copilot (không phải permission/hooks).
Phục vụ quyết định: kiểm tra kỹ thuật đa-bước/đa-vai của Vấn Đạo (8 vai, subagent tươi, reviewer gate) có tương ứng/chuyển được sang Copilot không.

---

## Q1. Custom chat modes (`.chatmode.md`) có phải "vai" riêng biệt không? Chuyển mode thế nào?

- **Finding**: Custom chat modes đã được đổi tên chính thức thành "custom agents"; file định dạng cũ `.chatmode.md` được đổi thành `.agent.md` (file cũ vẫn chạy được nếu đổi tên). Mỗi custom agent = "a set of instructions and tools that are applied when you switch to that agent" — tức có system-prompt riêng (phần thân Markdown) và tool-set riêng (trường `tools` trong frontmatter YAML).
  - source: https://code.visualstudio.com/docs/agent-customization/custom-agents
  - publisher: Visual Studio Code (Microsoft, tài liệu chính chủ Copilot trong VS Code)
  - pub_date: 2026-08-19 (trang ghi "8/19/2026")
  - accessed: 2026-08-25
  - confidence: high
  - class: pattern
  - Nhận định: về hình thức, mỗi custom agent giống "vai" (role) độc lập kiểu 8-vai Vấn Đạo hơn là giống "skill" tình huống của BMAD (mỗi custom agent chọn thủ công 1 lần, gắn 1 bộ system-prompt + tool cố định — không phải BMAD-style "một skill được match theo nội dung yêu cầu và tự kích hoạt giữa dòng hội thoại").

- **Finding**: Chuyển đổi giữa các mode có 2 cơ chế: (a) **thủ công** — người dùng chọn agent từ dropdown trong Chat view; (b) **"Handoffs"** — cơ chế bán-tự-động: sau khi 1 agent trả lời xong, nút "handoff" xuất hiện cho phép chuyển sang agent kế tiếp kèm theo context + prompt định sẵn. Cấu hình trong frontmatter của agent nguồn:
  ```yaml
  handoffs:
    - label: Start Implementation
      agent: implementation
      prompt: Now implement the plan outlined above.
      send: false
  ```
  `send: false` = người dùng phải bấm nút gửi thủ công; `send: true` = tự động gửi ngay. Nguyên văn: "Handoffs enable you to create guided sequential workflows that transition between agents with suggested next steps."
  - source: https://code.visualstudio.com/docs/agent-customization/custom-agents
  - publisher: Visual Studio Code (Microsoft)
  - pub_date: 2026-08-19
  - accessed: 2026-08-25
  - confidence: high
  - class: pattern
  - Nhận định: đây KHÔNG phải agent tự-route ẩn (agent tự quyết chuyển mode mà người dùng không biết) — luôn có bước gợi ý + nút bấm hiển thị (trừ khi cấu hình `send: true` thì tự gửi nhưng vẫn hiển thị đã chuyển). Là "guided workflow", gần giống cách Vấn Đạo gợi ý bước kế tiếp/vai kế tiếp cho người dùng xác nhận.

- **Finding**: Một custom agent có thể khai báo trường `agents` (danh sách agent con được phép gọi, hoặc `*` cho phép tất cả) để **gọi agent khác như subagent** — cơ chế riêng biệt với "handoffs" (handoffs chuyển hẳn quyền điều khiển; gọi subagent thì agent chính vẫn giữ quyền, chỉ mượn subagent làm việc phụ rồi lấy kết quả về).
  - source: https://code.visualstudio.com/docs/agent-customization/custom-agents
  - publisher: Visual Studio Code (Microsoft)
  - pub_date: 2026-08-19
  - accessed: 2026-08-25
  - confidence: high
  - class: pattern

---

## Q2. Copilot có tương đương "subagent tươi" (fresh/isolated context) không?

- **Finding**: VS Code Copilot có tính năng **Subagents** chính thức, định nghĩa: "an independent AI agent that performs focused work, such as researching a topic, analyzing code, or reviewing changes, and reports the results back to the main agent." Tài liệu khẳng định subagent chạy với **ngữ cảnh cô lập/"clean context"** — agent chính chỉ nhận **tóm tắt kết quả**, không nhận toàn bộ transcript, giữ cho ngữ cảnh của agent chính "sạch cho công việc triển khai thực tế." Gọi qua công cụ `agent/runSubagent`. Mỗi lần gọi là **không có trạng thái** (stateless) — agent chính không thể gửi tiếp tin nhắn cho cùng một subagent instance đã chạy xong. Mô hình được gọi là "coordinator and worker", mỗi subagent có thể có tool-set riêng và model riêng (rẻ/nhanh hơn).
  - source: https://code.visualstudio.com/docs/copilot/agents/subagents
  - publisher: Visual Studio Code (Microsoft)
  - pub_date: 2026-08-19
  - accessed: 2026-08-25
  - confidence: high
  - class: pattern
  - Nhận định: đây là tương đương RẤT SÁT với "subagent tươi" của Claude Code (fresh context, trả về summary, không giữ state) — kỹ thuật này chuyển được sang Copilot gần như nguyên vẹn về mặt khái niệm.

- **Finding**: **Copilot coding agent** (cloud/async agent trên GitHub.com) không được tài liệu mô tả rõ là "fresh context" theo nghĩa hội thoại, nhưng có cách ly ở cấp hạ tầng: mỗi agent có "access to its own ephemeral development environment, powered by GitHub Actions" để khám phá code, sửa đổi, chạy test. Nhận task qua: giao issue, mention `@copilot` trong PR, agent panel trên GitHub.com, hoặc tích hợp Teams/Slack/Issues. Trả kết quả bằng cách tạo pull request và "when the agent finishes, it will request a review from you."
  - source: https://docs.github.com/copilot/concepts/agents/coding-agent/about-coding-agent
  - publisher: GitHub Docs (chính chủ)
  - pub_date: N/A (trang không ghi ngày cập nhật)
  - accessed: 2026-08-25
  - confidence: high
  - class: pattern
  - Nhận định: đây là cách ly ở mức "môi trường thực thi" (VM/sandbox ephemeral) chứ tài liệu không mô tả rõ cách ly "ngữ cảnh hội thoại" như Subagents ở trên — khác chiều với "subagent tươi" kiểu Claude Code, gần giống hơn với mô hình "giao việc cho một agent nền chạy độc lập rồi review PR."

---

## Q3. Copilot có "reviewer gate" (agent tự soát lại việc agent khác vừa làm) không?

- **Finding**: **Copilot code review** là tính năng tự động review PR chính thức, có thể cấu hình để **tự kích hoạt** (không cần request thủ công) qua repository ruleset: "Automatically request Copilot code review", với tùy chọn review cả các lần push mới ("Review new pushes") và cả PR ở dạng draft ("Review draft pull requests" — hữu ích để bắt lỗi sớm trước khi human review). Có 2 mức độ ("Review effort level"): **Lite** (mặc định, nhanh, bắt lỗi/bảo mật/style phổ biến) và **Balanced** (phân tích sâu hơn logic phức tạp, code nhạy cảm bảo mật, dùng model reasoning cao hơn, tốn nhiều credit hơn).
  - source: https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-automatic-review
  - publisher: GitHub Docs (chính chủ)
  - pub_date: N/A (trang không ghi ngày cập nhật)
  - accessed: 2026-08-25
  - confidence: high
  - class: pattern
  - Nhận định: đây đúng là mô hình "reviewer gate" — nhưng phạm vi review là **PR-level** (soát diff cuối cùng), không phải "step-level" (soát ngay sau mỗi bước nhỏ trong một phiên làm việc) như reviewer gate của Vấn Đạo có thể chạy giữa các bước nội bộ.

- **Finding**: Có mô tả vòng lặp phản hồi kết hợp Copilot code review + coding agent: "a powerful feedback loop exists where Code Review identifies problems, Coding Agent solves them, and humans validate the results at every checkpoint" — tức Code Review (reviewer) phát hiện lỗi trên PR do Coding Agent (tác giả) tạo ra, và con người xác nhận ở mỗi "checkpoint" (ở đây "checkpoint" mang nghĩa mốc bàn giao/PR, không phải state kỹ thuật — xem thêm Q4).
  - source: (không fetch trực tiếp được URL gốc; nội dung này lấy từ kết quả WebSearch tổng hợp trỏ tới github.blog, chưa xác minh trực tiếp trang) — **hạ confidence vì chưa WebFetch xác minh nguyên văn từ chính trang github.blog**
  - publisher suy đoán: GitHub Blog (github.blog) — cần xác minh
  - pub_date: N/A
  - accessed: 2026-08-25
  - confidence: medium
  - class: pattern

---

## Q4. Tài liệu chính chủ nào mô tả việc chia 1 task dài thành nhiều bước có trạng thái/checkpoint?

- **Finding**: Copilot CLI có khái niệm "checkpoint" chính thức nhưng **ý nghĩa khác với "checkpoint tiến độ task"** — nguyên văn: "A checkpoint is created when session context is compacted, and allows you to view the summary context that Copilot created." Đây là **snapshot của việc nén ngữ cảnh hội thoại** (context compaction), không phải trạng thái tiến độ từng bước của công việc. Lệnh liên quan: `/session checkpoints` (xem danh sách), `/session checkpoints NUMBER` (xem chi tiết 1 checkpoint), `/compact` (kích hoạt nén thủ công). Lưu tại `~/.copilot/session-state/{session-id}/checkpoints/`.
  - source: https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-best-practices
  - publisher: GitHub Docs (chính chủ)
  - pub_date: N/A (trang không ghi ngày cập nhật)
  - accessed: 2026-08-25
  - confidence: high
  - class: pattern
  - Nhận định quan trọng: đây là điểm dễ hiểu lầm — "checkpoint" trong Copilot là cơ chế quản lý context-window (giống compact/summary của Claude Code), KHÔNG phải cơ chế lưu trạng thái nhiều bước của một kế hoạch dài như "story/step tracking" của Vấn Đạo.

- **Finding**: Tài liệu chính thức khuyến nghị pattern thủ công để theo dõi tiến độ task lớn: "For large-scale changes: Run the linter and write all errors to `migration-checklist.md` as a checklist. Then fix each issue one by one, checking them off as you go." — tức Copilot **không có framework built-in** để track trạng thái nhiều bước của 1 kế hoạch; best-practice chính chủ là tự tạo file checklist Markdown và tick dần — về bản chất là kỹ thuật thủ công, gần giống cách Vấn Đạo dùng story-file/status-file nhưng không được đóng gói thành cơ chế nền tảng.
  - source: https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-best-practices
  - publisher: GitHub Docs (chính chủ)
  - pub_date: N/A
  - accessed: 2026-08-25
  - confidence: high
  - class: pattern

- **Finding**: Copilot CLI có **Plan mode** (Shift+Tab hoặc gõ `/plan`) — "gives you a collaborative planning experience before Copilot starts implementing": Copilot phân tích yêu cầu, đặt câu hỏi làm rõ qua tool `ask_user`, xây dựng kế hoạch thực hiện có cấu trúc trước khi viết code; người dùng review/chỉnh kế hoạch rồi prompt "Implement this plan" để bắt đầu — đây là bước tách "lập kế hoạch" khỏi "thực thi", nhưng theo tài liệu đã fetch, không thấy mô tả cơ chế lưu trạng thái/checkpoint giữa các bước thực thi sau khi plan được duyệt.
  - source: https://github.blog/changelog/2026-01-21-github-copilot-cli-plan-before-you-build-steer-as-you-go/
  - publisher: GitHub Blog / Changelog (chính chủ, github.blog)
  - pub_date: 2026-01-21
  - accessed: 2026-08-25
  - confidence: high
  - class: pattern

- **Finding**: Copilot CLI có lệnh `/fleet` để **chia 1 task lớn thành nhiều subtask chạy song song qua subagent**: "the main Copilot agent analyzes the prompt and determines whether it can be divided into smaller subtasks", đánh giá "nature of the subtasks and their dependencies", rồi agent chính đóng vai **orchestrator**, "managing the workflow and dependencies between the subtasks." Tài liệu best-practices bổ sung: dùng `/fleet` ở đầu prompt để tăng tốc task lớn.
  - source: https://docs.github.com/en/copilot/concepts/agents/copilot-cli/fleet
  - publisher: GitHub Docs (chính chủ)
  - pub_date: N/A (trang không ghi ngày cập nhật)
  - accessed: 2026-08-25
  - confidence: high
  - class: pattern
  - Nhận định: `/fleet` là cơ chế "phân rã + điều phối dependency" gần với ý tưởng multi-step orchestration, nhưng là **song song hóa (fan-out)** chứ không phải **tuần tự có trạng thái/checkpoint** như một "story" nhiều bước của Vấn Đạo.

---

## Không tìm thấy

- Không tìm thấy tài liệu chính chủ nào mô tả Copilot (VS Code custom agents, Copilot CLI, hay Copilot coding agent) có cơ chế **agent tự động route** giữa các "vai" mà không cần người dùng xác nhận/bấm nút — mọi cơ chế chuyển vai tìm được (dropdown thủ công, Handoffs) đều yêu cầu hiển thị bước chuyển cho người dùng thấy (trừ khi handoff cấu hình `send:true`, nhưng vẫn có bước hiển thị/log).
- Không tìm thấy tài liệu chính chủ mô tả cơ chế "checkpoint tiến độ nhiều bước" (kiểu resume một kế hoạch dài dang dở, biết đang ở bước nào) tách biệt khỏi cơ chế nén context — Copilot dùng chữ "checkpoint" cho một khái niệm khác (context compaction snapshot), và pattern chính thức để track tiến độ nhiều bước là **tự viết checklist file thủ công**, không phải tính năng nền tảng có sẵn.
- Không xác minh trực tiếp được (chưa WebFetch nguyên trang) nguồn cho câu "Code Review identifies problems, Coding Agent solves them, and humans validate... at every checkpoint" — chỉ có qua tóm tắt WebSearch, đã hạ confidence xuống medium ở Q3.

---

## Tổng hợp nhanh cho quyết định (không phải finding riêng, chỉ là gợi ý đọc)

- Cơ chế **Subagents** của Copilot (Q2) là tương đương gần nhất, sát nhất về khái niệm với "subagent tươi" của Claude Code/Vấn Đạo — có thể dùng làm bằng chứng "kỹ thuật này portable sang nền tảng khác."
- Cơ chế **custom agents + Handoffs** (Q1) là tương đương gần nhất với "8 vai" — nhưng chuyển vai luôn cần xác nhận người dùng (không có auto-route ẩn), khác với cách Vấn Đạo có thể tự chuyển vai trong một phiên.
- **Reviewer gate** (Q3) tồn tại nhưng ở granularity PR-level, không phải step-level nội bộ trong 1 phiên.
- **State/checkpoint đa bước** (Q4) là điểm YẾU nhất của Copilot so với Vấn Đạo: không có tính năng nền tảng, chỉ có best-practice thủ công (viết checklist file) — đây có thể là điểm khác biệt/lợi thế đáng nêu khi viết SKILL.md/agents của Vấn Đạo.
