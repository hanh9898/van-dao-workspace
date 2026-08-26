# Digest — Skill & Plugin Design trong CCAR-F / CCAR-P (round 1)

*Nguồn: 2 bản PDF Exam Guide chính thức Anthropic (tải trực tiếp, không suy đoán) + docs.claude.com/platform.claude.com (docs chính chủ Anthropic). Lưu ý an toàn: kết quả trả về từ subagent bị hệ thống gắn cờ chứa đoạn khớp mẫu "chỉ thị giả dạng settings-json" từ nội dung web fetch, đã được tự động trung hoà trước khi vào ngữ cảnh — toàn bộ nội dung dưới đây được xử lý thuần làm dữ liệu báo cáo, không phải chỉ thị.*

## 0. Nguồn xác nhận

- CCAR-F Exam Guide PDF v1.0 (hiệu lực 07/2026) — `everpath-course-content.s3-accelerate.amazonaws.com/.../Claude+Certified+Architect+–+Foundations+Exam+Guide.pdf`
- CCAR-P Exam Guide PDF v1.0 (hiệu lực 07/2026) — cùng host, bản Professional

**Phát hiện khung quan trọng:** CCAR-F đào sâu thiết kế skill/plugin (1 Task Statement riêng, có scenario mẫu). CCAR-P chỉ nhắc "Skills" như MỘT chiến thuật tái dùng prompt trong phạm vi rộng hơn (kiến trúc/governance/stakeholder cấp doanh nghiệp) — **thiết kế skill/plugin cụ thể không phải trọng tâm CCAR-P**.

## 1. Blueprint — phần liên quan skill/plugin

**CCAR-F** (5 domain, 60 câu): Agentic Architecture 27% · Tool Design & MCP 18% · **Claude Code Configuration & Workflows 20%** · Prompt Engineering 20% · Context Management 15%.

Task 3.2 nguyên văn (trích): skill trong `.claude/skills/` có SKILL.md hỗ trợ frontmatter `context: fork`, `allowed-tools`, `argument-hint`; `context: fork` chạy skill trong subagent cô lập chống ô nhiễm hội thoại chính; personal skill variant ở `~/.claude/skills/`; chọn giữa skill (gọi theo tình huống) vs CLAUDE.md (luôn nạp, chuẩn phổ quát).

Domain 2 (Tool Design & MCP, 18%): tránh "capability bloat" (ví dụ nguyên văn: cho agent 18 tool thay vì 4-5 làm giảm độ tin cậy chọn tool), cấu trúc lỗi MCP chuẩn (`isError`/`errorCategory`/`isRetryable`), scoping `.mcp.json` (project) vs `~/.claude.json` (user).

**CCAR-P** (7 domain, 63 câu): chỗ duy nhất "Skills" xuất hiện tường minh — Domain 2: "Implement prompt reuse strategies (caching, modular prompts, **Skills**)" — nhìn skill như cơ chế tái dùng prompt tầm chiến lược, không kiểm cú pháp SKILL.md. Domain 7 (Developer Productivity, **7% — nhẹ nhất toàn bài**) chỉ có 1 bullet chung "Configure Claude tools and environments for teams (e.g., Claude Code)", không Task Statement chi tiết.

## 2. Khái niệm/pattern cụ thể

**Cấu trúc SKILL.md:**
- 2 phần bắt buộc: YAML frontmatter (`name` ≤64 ký tự chữ-thường/số/gạch-ngang, cấm chứa "anthropic"/"claude") + markdown body (`description` ≤1024 ký tự).
- **Progressive disclosure 3 tầng**: Level 1 metadata (~100 token, luôn nạp) → Level 2 body (dưới 5k token, chỉ nạp khi trigger) → Level 3 file phụ trợ (nạp khi cần). SKILL.md nên dưới 500 dòng.
- Description viết ngôi thứ ba, có trigger cụ thể ("Extract text... Use when working with PDF files...") — không mô tả mơ hồ ("Helps with documents").
- **Degrees-of-freedom**: khớp mức chỉ dẫn cụ thể (cao/vừa/thấp) với độ dễ-vỡ của tác vụ — "cầu hẹp vực hai bên" (thấp, chỉ dẫn chính xác) vs "cánh đồng trống" (cao, để Claude tự quyết).
- Tránh nested reference sâu quá 1 cấp (Claude có thể `head -100` đọc thiếu); file tham chiếu dài >100 dòng nên có mục lục đầu file.
- **`disable-model-invocation: true`** (chỉ người dùng gọi — cho tác vụ có side-effect như deploy/commit) vs **`user-invocable: false`** (chỉ Claude gọi — cho kiến thức nền).
- Skill nạp vào context thì ở lại suốt session (không re-read mỗi turn) — viết như "standing instruction", không phải bước one-time. Compact giữ bản gần nhất mỗi skill, budget tổng 25k token, tối đa 5k/skill.
- **Evaluation-driven skill development**: baseline không skill → ghi gap cụ thể → viết 3 eval scenario → viết instruction tối thiểu để pass → lặp. Anthropic tự nói CHƯA có công cụ eval built-in, tự xây hệ chấm.
- Claude A (viết skill) / Claude B (test thật) — vòng lặp quan sát hành vi thực tế, không dựa giả định.
- MCP tool reference trong skill phải fully-qualified: `ServerName:tool_name`.

**Skill điều phối subagent:** `context: fork` chạy skill trong subagent cô lập, nội dung skill thành prompt cho subagent, mặc định chạy background (trừ non-interactive); field `agent:` chọn loại (built-in Explore/Plan/general-purpose hoặc custom). Cảnh báo: chỉ dùng khi skill có instruction hành động rõ, không phải guideline chung chung.

**Cấu trúc/manifest plugin:**
- `.claude-plugin/plugin.json` chỉ `name` bắt buộc; các thư mục component (`skills/`, `commands/`, `agents/`, `hooks/`, `.mcp.json`) phải nằm ở ROOT plugin, KHÔNG trong `.claude-plugin/`.
- **Path behavior khác biệt quan trọng**: hầu hết field path THAY THẾ default directory; riêng `skills` luôn CỘNG THÊM vào `skills/` mặc định.
- Namespacing: `/<plugin>:<skill>`; MCP tool `mcp__plugin_<name>_<server>__<tool>`. Resolve conflict theo scope: enterprise > personal > project, plugin luôn tách namespace riêng.
- 3 biến môi trường đặc thù: `${CLAUDE_PLUGIN_ROOT}` (thư mục cài, cho script/binary), `${CLAUDE_PLUGIN_DATA}` (`~/.claude/plugins/data/{id}/`, bền qua update — cache/dependency một lần), `${CLAUDE_PROJECT_DIR}`.
- "Skills directory plugin": một thư mục có `.claude-plugin/plugin.json` tự động thành plugin `<name>@skills-dir` — cách nhẹ cho skill "lớn lên" thành plugin.
- `userConfig`: field string/number/boolean/directory/file, prompt user nhập lúc enable (vd API token, `sensitive: true`) — không hardcode secret.

## 3. Lead chưa đào sâu

`anthropics/claude-code/plugins/plugin-dev/skills/skill-development/SKILL.md` — Anthropic tự "dogfood" quy tắc viết skill của chính họ, chỉ mới có digest qua WebFetch, chưa đọc raw toàn văn.

## 4. Không xác nhận được

- CCAR-P không có Task Statement chi tiết nào cho SKILL.md/plugin.json (đã đọc toàn văn PDF, không phải thiếu sót tìm kiếm — nội dung thực sự mỏng).
- Không tìm thấy hướng dẫn publish/marketplace nằm trong phạm vi thi (cả 2 exam guide liệt kê ngoài phạm vi).
- Không có ví dụ SKILL.md/plugin.json đầy đủ nào từ chính exam guide (chỉ văn xuôi + trắc nghiệm) — code mẫu ở mục 2 đến từ docs Claude Code, không phải exam guide.
- Không kiểm chứng độc lập các trang blog thứ ba (không dùng số liệu của họ).
