# Digest R1.1 — Cấu trúc file custom-instructions/chatmodes của GitHub Copilot

Chủ đề: quy ước VIẾT (cấu trúc file, frontmatter, path-resolution) của GitHub Copilot custom instructions & custom chat modes/agents — so sánh với BMAD-METHOD SKILL.md, phục vụ quyết định kiểm tra tính chuyển-nền-tảng của cách viết SKILL.md/agents Vấn Đạo.

---

## Findings

### F1 — `.github/copilot-instructions.md` là plain Markdown, KHÔNG có frontmatter YAML
```
{
  "claim": "File custom instructions cấp repository .github/copilot-instructions.md chứa 'natural language instructions to the file, in Markdown format'; whitespace giữa các instruction bị bỏ qua, có thể viết thành 1 đoạn văn, mỗi dòng, hoặc tách bằng dòng trống — không có cơ chế frontmatter YAML cho file này.",
  "source": "https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide",
  "publisher": "GitHub Docs",
  "pub_date": "N/A",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```

### F2 — `.instructions.md` (path-specific) CÓ frontmatter YAML với field `applyTo` (+ `name`, `description`)
```
{
  "claim": "File .instructions.md đặt trong .github/instructions/ (workspace) có frontmatter YAML tùy chọn với 3 field: name (display name, mặc định = tên file), description (mô tả ngắn hiện khi hover trong Chat view), applyTo (glob pattern xác định file nào được tự động áp dụng, relative to workspace root; dùng ** để áp dụng mọi file; nếu không khai thì instructions không tự áp dụng nhưng vẫn add thủ công được).",
  "source": "https://code.visualstudio.com/docs/agent-customization/custom-instructions",
  "publisher": "Visual Studio Code Docs (Microsoft)",
  "pub_date": "N/A",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```

### F3 — `applyTo` dùng cú pháp glob thuần, hỗ trợ multi-pattern bằng dấu phẩy — không có ngôn ngữ biến (`${var}`)
```
{
  "claim": "applyTo dùng glob syntax (vd '**/*.ts,**/*.tsx', 'src/**/*.py', '**/subdir/**/*.py'); tài liệu không đề cập bất kỳ cơ chế biến động dạng ${workspaceFolder}/${fileBasename} nào cho path resolution — chỉ có glob pattern tuyệt đối/tương đối so với workspace root.",
  "source": "https://code.visualstudio.com/docs/agent-customization/custom-instructions",
  "publisher": "Visual Studio Code Docs (Microsoft)",
  "pub_date": "N/A",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```

### F4 — Custom agents (trước gọi là "custom chat modes") dùng file `.agent.md`, frontmatter phong phú hơn nhiều so với instructions — gần giống cấu trúc SKILL.md/agent của Claude Code
```
{
  "claim": "Custom agent files (định dạng mới, thay thế .chatmode.md) là file Markdown đuôi .agent.md, có phần Header YAML frontmatter với các field: description, name, argument-hint, tools, agents (danh sách subagent, '*' hoặc '[]'), model (một model hoặc danh sách ưu tiên — hệ thống thử lần lượt cho tới khi có model khả dụng), user-invocable, disable-model-invocation, handoffs, hooks; phần Body là Markdown hướng dẫn, có thể tham chiếu tool bằng cú pháp #tool:<tool-name>.",
  "source": "https://code.visualstudio.com/docs/copilot/customization/custom-chat-modes",
  "publisher": "Visual Studio Code Docs (Microsoft)",
  "pub_date": "N/A",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```

### F5 — VS Code Copilot đã bắt đầu hỗ trợ trực tiếp định dạng thư mục kiểu Claude Code (`.claude/agents`, `.claude/rules`) song song với định dạng gốc `.github/agents`, `.github/instructions`
```
{
  "claim": "VS Code tìm custom agent files mặc định tại workspace .github/agents, đồng thời hỗ trợ định dạng 'Claude format' tại .claude/agents (workspace) — và tương tự với instructions: .github/instructions song song .claude/rules; user profile dùng ~/.copilot/agents hoặc ~/.copilot/instructions / ~/.claude/rules. Với session chạy trên Agent Host, agent đọc user-level custom agents từ ~/.copilot/agents chứ không phải VS Code profile user data. Có thể cấu hình thêm đường dẫn qua setting chat.agentFilesLocations / chat.instructionsFilesLocations.",
  "source": "https://code.visualstudio.com/docs/copilot/customization/custom-chat-modes",
  "publisher": "Visual Studio Code Docs (Microsoft)",
  "pub_date": "N/A",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```

### F6 — GitHub cũng hỗ trợ `AGENTS.md`/`CLAUDE.md`/`GEMINI.md` như một lớp "agent instructions" riêng, với quy tắc "nearest file wins" theo cây thư mục
```
{
  "claim": "Ngoài copilot-instructions.md và .instructions.md, Copilot còn hỗ trợ AGENTS.md (và tương đương CLAUDE.md, GEMINI.md) đặt ở bất kỳ đâu trong repo; khi Copilot làm việc, file AGENTS.md gần nhất trong cây thư mục (nearest-in-directory-tree) sẽ được ưu tiên áp dụng — một dạng resolution theo vị trí file, không phải theo biến.",
  "source": "https://docs.github.com/en/copilot/reference/custom-instructions-support",
  "publisher": "GitHub Docs",
  "pub_date": "N/A",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```

### F7 — Việc nạp instructions là tự động & im lặng (auto-inject vào request), không qua cơ chế "resolve path lúc runtime" như BMAD
```
{
  "claim": "Instructions trong copilot-instructions.md khả dụng ngay khi lưu file và được tự động thêm ('automatically added') vào các request gửi tới Copilot; người dùng chỉ xác minh được việc này gián tiếp qua mục References của response trong Chat view liệt kê file .github/copilot-instructions.md làm nguồn tham chiếu — không có cú pháp biến kiểu {skill-root} để tác giả tự trỏ đường dẫn trong nội dung file.",
  "source": "https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide",
  "publisher": "GitHub Docs",
  "pub_date": "N/A",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```

### F8 — Hỗ trợ theo nền tảng (platform support matrix) khác nhau theo loại file — không phải mọi client đều đọc mọi loại
```
{
  "claim": "Bảng hỗ trợ nền tảng: GitHub.com hỗ trợ Repository/Personal/Organization instructions cho Chat và cả 4 loại cho Cloud Agent; VS Code hỗ trợ Repository/Path/Agent cho Chat, và Repository/Path/Agent(AGENTS/CLAUDE/GEMINI) cho Cloud Agent; Visual Studio, JetBrains, Eclipse, Xcode có ma trận hỗ trợ khác nhau (vd Eclipse không hỗ trợ custom instructions cho Code Review); Copilot CLI hỗ trợ cả 4 loại kể cả personal files.",
  "source": "https://docs.github.com/en/copilot/reference/custom-instructions-support",
  "publisher": "GitHub Docs",
  "pub_date": "N/A",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```

---

## So sánh trực tiếp với BMAD-METHOD (SKILL.md)

| Chiều | BMAD-METHOD SKILL.md | GitHub Copilot |
|---|---|---|
| Frontmatter cấp "root/repo-wide" | YAML bắt buộc (`name`, `description`) trên mọi SKILL.md | `.github/copilot-instructions.md` = plain Markdown, KHÔNG frontmatter (F1) |
| Frontmatter cấp "path-scoped" | Không có khái niệm tương đương trực tiếp — SKILL.md không tự giới hạn theo path glob | `.instructions.md` có frontmatter `applyTo` (glob) để scope theo path (F2) |
| Biến path-resolution | `{skill-root}`, `{project-root}` khai trong section `## Conventions`/`## Resolution rules`, tác giả tự resolve trong prose | KHÔNG có cú pháp biến (`${...}`) — chỉ glob pattern relative to workspace root; không có convention section tương đương (F3, F7) |
| File "agent" (persona/tool-scoped) | `agents/*.md` — cấu trúc do Vấn Đạo tự định nghĩa | `.agent.md` (trước là `.chatmode.md`) — frontmatter chuẩn hóa gồm `tools`, `agents` (subagent), `model` (list ưu tiên), `handoffs`, `hooks`, `user-invocable` — phong phú hơn, có khái niệm subagent/handoff/hook ngay trong frontmatter (F4) |
| Phát hiện/nạp file | Explicit invocation qua skill system của Claude Code | Tự động, im lặng, theo path cố định (`.github/instructions`, `.github/agents`) hoặc theo "semantic matching" của description với task hiện tại; có setting mở rộng đường dẫn (F5, F7) |
| Tương thích ngược "format khác" | N/A (Vấn Đạo chỉ chạy trên Claude Code) | VS Code đã bắt đầu đọc trực tiếp `.claude/agents` và `.claude/rules` — tức là **format của Claude Code đang được một nền tảng thứ ba công nhận như một "input format" song song**, không phải Copilot áp dụng convention của BMAD (F5) |

## Kết luận kỹ thuật cho quyết định "chuyển nền tảng"

- Cú pháp biến `{skill-root}`/`{project-root}` mà BMAD dùng trong SKILL.md **không có tương đương trực tiếp** trong hệ Copilot — Copilot resolve theo path tĩnh (glob `applyTo` hoặc vị trí file "nearest AGENTS.md") chứ không có prose-variable substitution do tác giả định nghĩa. Muốn mang quy ước SKILL.md của Vấn Đạo sang Copilot nguyên vẹn sẽ phải bỏ cơ chế biến hoặc tự làm lớp tiền xử lý (không có sẵn native).
- Frontmatter `.agent.md` của Copilot (F4) có bề mặt rộng hơn cấu trúc agent hiện tại của Vấn Đạo (thêm `handoffs`, `hooks`, `model` priority-list, `agents` allow-list) — đây là điểm để cân nhắc bổ sung nếu muốn agent Vấn Đạo "đọc được" bởi Copilot mà không mất field.
- Vì VS Code đã native-hỗ trợ đọc thư mục `.claude/agents`/`.claude/rules` (F5), **không phải mọi thứ cần "dịch"** — nếu Vấn Đạo giữ đúng layout `.claude/agents/*.md`, ít nhất phần discovery đã tương thích Copilot-trong-VS-Code sẵn (dù nội dung field bên trong vẫn theo schema riêng của Copilot khi nó parse).
