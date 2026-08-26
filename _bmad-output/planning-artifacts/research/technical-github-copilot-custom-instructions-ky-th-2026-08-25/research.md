---
title: 'technical research: GitHub Copilot custom instructions/chatmodes — quy ước viết'
type: 'technical'
topic: 'GitHub Copilot custom instructions/chatmodes — quy ước viết hướng dẫn, đối chiếu BMAD'
decision: 'Cách viết SKILL.md/agents/hooks của Vấn Đạo — kiểm tra kỹ thuật BMAD có chuyển được sang nền tảng khác'
source: 'Native run — web thật, tài liệu chính chủ docs.github.com/code.visualstudio.com/github.blog'
status: complete
preset: 'standard'
validation: 'normal'
claims_verified: 3
claims_unverified: 0
created: '2026-08-25'
updated: '2026-08-26'
---

# technical research: GitHub Copilot custom instructions/chatmodes — quy ước viết

**Decision this research serves:** Vòng thứ ba đối chiếu (sau BMAD-METHOD và Superpowers, cùng nền Claude Code) — lần này khác nền tảng hoàn toàn, để kiểm tra kỹ thuật viết skill của BMAD (biến `{skill-root}`, persona "You are X", numbered activation steps) có phải tri thức chuyển được hay chỉ đặc thù Claude Code. Không lặp lại phần permission/hooks đã khảo sát ở nghiên cứu HITL trước.

## 1. Tóm tắt điều hành

GitHub Copilot **không có tương đương trực tiếp** cho cú pháp biến `{skill-root}`/`{project-root}` của BMAD — chỉ có glob pattern (`applyTo`) và "nearest file wins" theo vị trí, không có prose-variable do tác giả tự định nghĩa [1][2][3]. Cũng **không tìm thấy** khuyến nghị persona "You are X" hay activation-steps đánh số ở bất kỳ tài liệu chính chủ nào đã khảo sát — Copilot xem agent như "teammate mới cần onboard bằng sự thật dự án", không đóng vai nhân vật [15][16].

Nhưng bốn phát hiện xác nhận **các nguyên lý tổ chức đa-bước/đa-vai của BMAD/Vấn Đạo là tri thức chuyển được, không phải đặc thù Claude Code**:

1. **Subagents chính thức của VS Code Copilot** ("clean context", stateless, chỉ trả tóm tắt cho agent chính) là tương đương rất sát "subagent tươi" — mô hình "coordinator and worker" [6].
2. **Custom agents + Handoffs** là tương đương gần nhất với "8 vai" — nhưng chuyển vai luôn cần xác nhận người dùng hiển thị (dropdown thủ công hoặc nút Handoff), không có auto-route ẩn [5].
3. **Copilot code review là reviewer-gate thật** (tự trigger qua repo ruleset, 2 mức Lite/Balanced) nhưng ở granularity **PR-level**, không phải step-level nội bộ trong một phiên [8].
4. **False-friend quan trọng cần tránh khi viết tài liệu**: "Checkpoint" trong Copilot CLI = snapshot nén context (compaction), KHÔNG phải trạng thái tiến độ nhiều bước — best-practice chính thức cho việc theo dõi tiến độ dài là **tự viết file checklist Markdown thủ công**, không có tính năng nền tảng có sẵn [9].

**Cũng đáng chú ý**: VS Code đã native đọc song song `.claude/agents` cùng `.github/agents` [3], và `.claude/rules` cùng `.github/instructions` [2] — nghĩa là layout gốc của Vấn Đạo (`.claude/`) đã được một nền tảng thứ ba nhận diện phần nào, dù nội dung field bên trong vẫn theo schema riêng khi Copilot parse.

## 2. Theo từng chiều

### 2.1 Cấu trúc file custom-instructions/chatmodes

`.github/copilot-instructions.md` (cấp repo) là **Markdown thuần, không frontmatter** — chỉ danh sách chỉ dẫn ngôn ngữ tự nhiên, khoảng trắng giữa các dòng bị bỏ qua [1]. Ngược lại, `.instructions.md` (path-scoped, đặt trong `.github/instructions/`) **có frontmatter YAML** với `name`, `description`, và `applyTo` — glob pattern relative workspace root, không hỗ trợ biến động `${...}` [2]. Custom agent files (`.agent.md`, đổi tên từ `.chatmode.md`) có frontmatter phong phú nhất: `description`, `tools`, `agents` (subagent allow-list), `model` (danh sách ưu tiên), `user-invocable`, `disable-model-invocation`, `handoffs`, `hooks` — rộng hơn cấu trúc `agents/*.md` hiện tại của Vấn Đạo [3].

Copilot cũng hỗ trợ `AGENTS.md`/`CLAUDE.md`/`GEMINI.md` như lớp "agent instructions" riêng, với quy tắc **"nearest file wins"** theo cây thư mục — resolution theo vị trí file, không phải theo biến [4]. Việc nạp instructions là **tự động và im lặng** (auto-inject vào request) — người dùng chỉ xác minh gián tiếp qua mục References của response; không có cú pháp biến kiểu `{skill-root}` để tác giả tự trỏ đường dẫn [1]. Ma trận hỗ trợ khác nhau theo client: GitHub.com, VS Code, Visual Studio, JetBrains, Eclipse, Xcode, Copilot CLI mỗi cái hỗ trợ một tập con khác nhau của 4 loại file [4].

**Điểm đáng chú ý nhất cho Vấn Đạo**: VS Code đã bắt đầu đọc trực tiếp `.claude/agents` (song song `.github/agents`) [3] và `.claude/rules` (song song `.github/instructions`) [2] — "format của Claude Code đang được một nền tảng thứ ba công nhận như input format song song", không phải ngược lại.

### 2.2 Tổ chức flow nhiều bước / nhiều mode

Custom chat modes đã đổi tên chính thức thành "custom agents" [5]. Mỗi custom agent = "a set of instructions and tools that are applied when you switch to that agent" — về hình thức giống "vai" độc lập (kiểu 8 vai Vấn Đạo) hơn là "skill" tự kích hoạt theo nội dung (kiểu BMAD) [5]. Chuyển đổi có 2 cơ chế: **thủ công** (dropdown) hoặc **Handoffs** — nút gợi ý chuyển agent kế tiếp kèm context/prompt định sẵn, cấu hình `send: false` (người dùng bấm gửi) hoặc `send: true` (tự gửi) — **luôn hiển thị bước chuyển, không có auto-route ẩn** [5]. Trường `agents` (allow-list, hoặc `*`) cho phép gọi agent khác như subagent — tách biệt với Handoffs (Handoffs chuyển hẳn quyền điều khiển; gọi subagent thì agent chính giữ quyền, chỉ mượn việc phụ) [5].

**Subagents chính thức** của VS Code Copilot: "an independent AI agent that performs focused work... and reports the results back to the main agent", chạy **"clean context"**, agent chính chỉ nhận tóm tắt — không nhận toàn bộ transcript; mỗi lần gọi **stateless** (không gửi tiếp được cho cùng instance đã chạy xong); mô hình "coordinator and worker" [6]. Đây là tương đương rất sát "subagent tươi" của Claude Code về mặt khái niệm. Riêng **Copilot coding agent** (cloud/async trên GitHub.com) cách ly ở cấp hạ tầng khác — "own ephemeral development environment, powered by GitHub Actions" — không phải cách ly ngữ cảnh hội thoại như Subagents [7].

**Copilot code review** là reviewer-gate thật: cấu hình tự động trigger qua repository ruleset, review cả push mới và PR draft, 2 mức Lite (mặc định, nhanh)/Balanced (sâu hơn, tốn credit hơn) [8] — nhưng ở **granularity PR-level** (soát diff cuối), không phải step-level nội bộ như reviewer gate của BMAD/Vấn Đạo.

**"Checkpoint" là false-friend quan trọng**: Copilot CLI định nghĩa "A checkpoint is created when session context is compacted" — snapshot của việc NÉN NGỮ CẢNH (giống compact/summary của Claude Code), không phải trạng thái tiến độ từng bước [9]. Best-practice chính thức cho theo dõi tiến độ task lớn: tự viết `migration-checklist.md`, tick dần thủ công — **không có framework built-in** [9]. Riêng có **Plan mode** (`/plan`) tách lập-kế-hoạch khỏi thực-thi trước khi code [10], và **`/fleet`** chia task lớn thành subtask chạy song song qua subagent theo mô hình orchestrator — nhưng đây là **fan-out song song**, không phải chuỗi tuần tự có trạng thái [11].

### 2.3 Văn phong hướng dẫn model trong tài liệu chính chủ

GitHub quy định giới hạn độ dài nhưng **không nhất quán giữa các trang tài liệu**: trang repository-instructions nói "no longer than 2 pages" và "must not be task specific" [12], trong khi trang tutorial code-review nói "no longer than about 1,000 lines... beyond this, the quality of responses may deteriorate" [13] — hai con số khác nhau, không rõ do phạm vi khác nhau (repo-wide vs code-review) hay tài liệu chưa đồng bộ. Có danh sách "không hỗ trợ" tường minh: đổi UX/định dạng review comment, đổi chức năng lõi, theo dõi link ngoài, và yêu cầu mơ hồ (ví dụ "Be more accurate" bị liệt kê thẳng là không hỗ trợ) [13].

Văn phong khuyến nghị nhất quán: mệnh lệnh ngôi hai ("always...", "avoid...", "use..."), heading + bullet, "elevator pitch cho DỰ ÁN" ở phần mở đầu — không mô tả Copilot là ai [14]. 5 mục chính thức khuyến nghị đều là LOẠI THÔNG TIN DỰ ÁN (project overview, tech stack, coding guidelines, project structure, resources), không có mục nào yêu cầu định nghĩa "nhân vật" cho Copilot [14]. Cảnh báo giọng văn tường minh: "Don't be passive aggressive with Copilot" [14]. **Không có file mẫu `copilot-instructions.md` hoàn chỉnh nào được công bố** — chỉ có snippet minh hoạ (đoạn project-overview, và một file path-specific `typescript.instructions.md` đầy đủ về naming/style/error-handling/testing) [15][16].

**Đối chiếu trực tiếp với BMAD** (kết luận âm tính, đã kiểm nhiều trang, confidence trung bình vì phạm vi fetch có giới hạn): **không tìm thấy** persona "You are X", numbered activation steps, hay "one test decides" ở bất kỳ trang chính chủ GitHub nào đã khảo sát trong lượt này [17].

## 3. Phát hiện xuyên chiều

1. **Hai lớp kỹ thuật của BMAD tách biệt rõ khi soi qua Copilot: "cơ chế tổ chức" (chuyển được) vs. "văn phong hướng dẫn" (không chuyển được).** Subagent cô lập, reviewer-gate, plan-trước-thực-thi — đều có tương đương thật ở Copilot, xác nhận đây là nguyên lý phổ quát của việc điều phối AI agent, không phải phát minh riêng của BMAD/Claude Code. Ngược lại, persona/numbered-steps/"one test decides" — không tìm thấy dấu vết nào ở Copilot; đây có thể là lựa chọn văn phong đặc thù hệ sinh thái Claude Code (nơi cả BMAD lẫn Superpowers đều dùng mạnh mẽ) chứ không phải chuẩn ngành.

2. **"Checkpoint" là bẫy thuật ngữ xuyên nền tảng** — Claude Code, Copilot CLI, và (theo nghiên cứu HITL trước) nhiều công cụ khác đều dùng từ "checkpoint" nhưng với nghĩa khác nhau (nén context vs. snapshot hoàn tác vs. trạng thái tiến độ). Khi Vấn Đạo viết tài liệu kỹ thuật tham chiếu khái niệm này, nên định nghĩa lại tường minh trong ngữ cảnh riêng, không giả định người đọc hiểu đúng nghĩa nào.

3. **Điểm YẾU nhất của Copilot so với Vấn Đạo/BMAD: không có state/checkpoint đa bước nền tảng.** Best-practice chính thức là "tự viết file checklist" — đúng tinh thần memlog/lo-trinh.jsonl nhưng chưa được đóng gói thành tính năng có sẵn ở Copilot. Đây củng cố thêm phát hiện từ nghiên cứu Superpowers: cơ chế trạng thái xuyên phiên kiểu BMAD (đã áp dụng ở kiến trúc spine Vấn Đạo, AD-2) là lợi thế thật, không phải thứ "ai cũng có sẵn".

## 4. Bằng chứng ngược

Không chạy red-team pass ở lượt nghiên cứu này (`red_team: off`) — không có mục nào ở phần này.

## 5. Khuyến nghị

1. **Không cần lo lắng về "tính di động" của cú pháp biến `{skill-root}`/`{project-root}` — đây vốn không phải mục tiêu của Vấn Đạo** (chỉ chạy Claude Code, Non-Goal đã ghi). Xác nhận: nếu sau này có nhu cầu port, sẽ phải bỏ cơ chế biến hoặc tự làm lớp tiền xử lý, không có sẵn native ở Copilot. Độ tin: cao. *Feed vào: không cần hành động — chỉ là kiến thức nền cho quyết định tương lai nếu multi-platform được cân nhắc lại.*

2. **Xác nhận: subagent cô lập + reviewer-gate PR-level + plan-trước-thực-thi là nguyên lý phổ quát, không phải rủi ro "chỉ Claude Code mới hiểu".** Kiến trúc 8-vai/subagent-tươi/Reviewer-Gate của Vấn Đạo (AD-1, AD-7 spine) đứng vững khi đối chiếu chéo nền tảng thứ ba — không cần điều chỉnh. Độ tin: cao. *Feed vào: không cần hành động, củng cố niềm tin vào kiến trúc đã chọn.*

3. **Khi viết tài liệu kỹ thuật (không phải SKILL.md người dùng cuối) có nhắc tới "checkpoint"**, định nghĩa rõ nghĩa dùng trong ngữ cảnh Vấn Đạo (nếu có) để tránh nhầm với nghĩa nén-context phổ biến ở công cụ khác. Độ tin: trung bình (một khuyến nghị viết-tài-liệu, phòng ngừa nhầm lẫn thuật ngữ). *Feed vào: bất kỳ tài liệu kỹ thuật/architecture nào của Vấn Đạo dùng từ "checkpoint".*

4. **Không cần bắt chước văn phong "liệt kê sự thật dự án, không persona" của Copilot** — đây là lựa chọn phù hợp cho công cụ coding-assistant tổng quát, không phải phản bác với cách BMAD/Superpowers dùng persona mạnh cho quy trình có tính kỷ luật cao. Vấn Đạo đã có lý do riêng cho thế giới quan/persona (trải nghiệm người học), tiếp tục giữ. Độ tin: trung bình. *Feed vào: không cần hành động.*

## 6. Câu hỏi còn mở

1. Hai URL docs.github.com khác nhau ([1] và [12]) đều tự nhận mô tả "repository instructions" cơ bản nhưng có đường dẫn khác nhau — chưa xác minh đây là hai trang thật khác nhau (redirect cũ/mới) hay một trong hai agent ghi nhầm URL; cần đối chiếu lại nếu trích dẫn chính thức.
2. Giới hạn độ dài "2 trang" vs "~1000 dòng" ([12] vs [13]) — chưa xác nhận có phải hai ngữ cảnh khác nhau (repo-wide vs code-review-specific) hay tài liệu GitHub chưa đồng bộ.
3. Claim về "feedback loop: Code Review identifies problems, Coding Agent solves them" — chỉ có qua WebSearch tóm tắt, chưa WebFetch xác minh trực tiếp trang github.blog nguồn; bị loại khỏi báo cáo chính vì chưa đạt ngưỡng xác minh.
4. `hooks-cursor.json`-tương-đương hoặc bất kỳ tài liệu nào về cách Copilot xử lý conflict giữa personal/repo/org instructions cụ thể hơn "personal > repository > organization" — chưa đọc chi tiết cơ chế merge.
5. Chưa khảo sát Copilot trên JetBrains/Eclipse/Xcode cụ thể — chỉ biết từ bảng ma trận hỗ trợ rằng chúng khác VS Code, chưa đọc tài liệu riêng từng IDE.

## 7. Phụ lục nguồn

Mọi nguồn dưới đây: publisher chính chủ GitHub (GitHub Docs / VS Code Docs / GitHub Blog) · truy cập 2026-08-25 · độ tin Cao trừ khi ghi chú khác.

| # | Nguồn | Publisher | Ngày | Hỗ trợ phát hiện |
|---|---|---|---|---|
| [1] | `docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide` | GitHub Docs | N/A | copilot-instructions.md plain Markdown, tự động nạp im lặng |
| [2] | `code.visualstudio.com/docs/agent-customization/custom-instructions` | VS Code Docs | N/A | `.instructions.md` frontmatter `applyTo`, không có biến `${...}`; `.claude/rules` song song `.github/instructions` |
| [3] | `code.visualstudio.com/docs/copilot/customization/custom-chat-modes` | VS Code Docs | N/A | `.agent.md` frontmatter phong phú, VS Code đọc `.claude/agents` song song |
| [4] | `docs.github.com/en/copilot/reference/custom-instructions-support` | GitHub Docs | N/A | AGENTS.md nearest-wins, ma trận hỗ trợ theo client |
| [5] | `code.visualstudio.com/docs/agent-customization/custom-agents` | VS Code Docs | 2026-08-19 | Custom agents, Handoffs, trường `agents` subagent allow-list |
| [6] | `code.visualstudio.com/docs/copilot/agents/subagents` | VS Code Docs | 2026-08-19 | Subagents chính thức, clean context, stateless |
| [7] | `docs.github.com/copilot/concepts/agents/coding-agent/about-coding-agent` | GitHub Docs | N/A | Coding agent, cách ly hạ tầng (ephemeral env) |
| [8] | `docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-automatic-review` | GitHub Docs | N/A | Copilot code review, auto-trigger, Lite/Balanced |
| [9] | `docs.github.com/en/copilot/how-tos/copilot-cli/cli-best-practices` | GitHub Docs | N/A | "Checkpoint" = context compaction, checklist thủ công |
| [10] | `github.blog/changelog/2026-01-21-github-copilot-cli-plan-before-you-build-steer-as-you-go/` | GitHub Blog | 2026-01-21 | Plan mode tách kế hoạch/thực thi |
| [11] | `docs.github.com/en/copilot/concepts/agents/copilot-cli/fleet` | GitHub Docs | N/A | `/fleet` fan-out song song |
| [12] | `docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions` | GitHub Docs | N/A | Giới hạn "2 trang", personal>repo>org |
| [13] | `docs.github.com/en/copilot/tutorials/use-custom-instructions` | GitHub Docs | N/A | Giới hạn "~1000 dòng", danh sách không hỗ trợ |
| [14] | `github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/` | GitHub Blog | Đăng 2025-09-03, cập nhật 2026-06-14 | 5 mục khuyến nghị, "elevator pitch", "don't be passive aggressive" |
| [15] | `github.blog/ai-and-ml/github-copilot/unlocking-the-full-power-of-copilot-code-review-master-your-instructions-files/` | GitHub Blog | Đăng 2025-11-14, cập nhật 2026-04-17 | Ví dụ file typescript.instructions.md đầy đủ |
| [16] | `docs.github.com/en/copilot/tutorials/customization-library/custom-instructions/your-first-custom-instructions` | GitHub Docs | N/A | Ví dụ ngôi 2 mệnh lệnh, trước/sau |
| [17] | `docs.github.com/copilot/how-tos/agents/copilot-coding-agent/best-practices-for-using-copilot-to-work-on-tasks` | GitHub Docs | N/A | 3 định dạng file + AGENTS/CLAUDE/GEMINI.md (confidence trung bình) |

## 8. Bản đồ độ mới

Nguồn là tài liệu chính chủ đang cập nhật tích cực (một số trang có ngày cập nhật tường minh gần đây: [5][6] 2026-08-19, [14] cập nhật 2026-06-14, [15] cập nhật 2026-04-17) — tính năng Copilot (Subagents, custom agents, Handoffs) đổi tên/API còn tương đối mới ("custom chat modes" → "custom agents" là một đổi tên gần đây) nên rủi ro đổi tiếp trong 3-6 tháng tới là thật.

**Mốc tái xác minh:** trước khi trích dẫn bất kỳ kết luận nào ở báo cáo này vào tài liệu chính thức của Vấn Đạo (đặc biệt phần "chuyển-nền-tảng-được"), re-check lại tên gọi/URL của tính năng Subagents và custom agents — do đổi tên gần đây, khả năng đường dẫn/thuật ngữ tiếp tục đổi trong ≤6 tháng là có thật.
