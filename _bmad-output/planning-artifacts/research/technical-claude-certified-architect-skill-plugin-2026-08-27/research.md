---
title: 'technical research: Claude Certified Architect (Foundations + Professional) — nội dung liên quan thiết kế skill/plugin'
type: 'technical'
topic: 'Claude Certified Architect (CCAR-F, CCAR-P) — khái niệm liên quan thiết kế skill trong plugin và thiết kế plugin, đem vào van-dao'
decision: 'Rút khái niệm/pattern kiến trúc từ 2 chứng chỉ Anthropic, giới hạn đúng phần liên quan thiết kế skill/plugin, để đối chiếu cải thiện kiến trúc van-dao'
source: 'https://anthropic.skilljar.com/claude-certified-architect-foundations-access-request ; https://www.pearsonvue.com/us/en/anthropic.html'
status: complete
preset: 'standard'
validation: 'normal'
created: '2026-08-27'
updated: '2026-08-27'
claims_verified: 13
claims_unverified: 0
claims_overturned: 0
---

# technical research: Claude Certified Architect (Foundations + Professional) — nội dung liên quan thiết kế skill/plugin

**Decision this research serves:** Rút khái niệm/pattern kiến trúc từ 2 chứng chỉ Anthropic (CCAR-F, CCAR-P), giới hạn đúng phần liên quan thiết kế skill trong plugin và thiết kế plugin, để đối chiếu cải thiện kiến trúc van-dao.

## Tóm tắt điều hành

Lấy được nguồn sơ cấp mạnh nhất có thể có: 2 bản **PDF Exam Guide chính thức Anthropic** (CCAR-F, CCAR-P, v1.0, hiệu lực 07/2026), đọc toàn văn, cộng docs.claude.com/platform.claude.com chính chủ. **Phát hiện khung quan trọng:** chỉ CCAR-F đào sâu thiết kế skill/plugin (Domain 3, 20%, có Task Statement riêng); CCAR-P chỉ nhắc "Skills" như một chiến thuật tái dùng prompt trong phạm vi kiến trúc/governance doanh nghiệp rộng hơn — **với đúng câu hỏi "thiết kế skill trong plugin", CCAR-P gần như không đóng góp gì mới ngoài CCAR-F.**

Đối chiếu với `ARCHITECTURE-SPINE.md` (đọc trọn) và đặc tả van-dao thật: **van-dao đã áp dụng đúng 3/8 khái niệm kiểm được** (userConfig, cấu trúc plugin.json/component-ở-root, `disable-model-invocation`) và **độc lập tự đến progressive-disclosure pattern** (§12.5 micro-file) trước khi biết CCAR-F gọi nó là gì. Tìm được **4 điểm đáng bổ sung** — không phải lỗi thiết kế, mà là thiếu con số cụ thể hoặc thiếu 1 dòng ghi lý do cho lựa chọn đã đúng: ngân sách token cụ thể (25k/5k), ngưỡng độ dài SKILL.md (500 dòng), lý do chọn `agents/*.md` thay vì `context: fork`, và đáng chú ý nhất — **`~/.vandao/` là một divergence có chủ đích khỏi quy ước `${CLAUDE_PLUGIN_DATA}` của Anthropic, chưa được ghi lại lý do ở đâu**. MCP — trọng tâm lớn của cả hai chứng chỉ — hoàn toàn không áp dụng cho van-dao (không dùng MCP server nào).

⚠️ **Lưu ý an toàn phát sinh trong lượt chạy:** một trong hai subagent nghiên cứu trả về digest bị hệ thống tự động gắn cờ chứa đoạn nội dung web fetch khớp mẫu "chỉ thị giả dạng settings-json" — đã được framework tự trung hoà trước khi vào ngữ cảnh của người điều phối. Toàn bộ nội dung được xử lý thuần làm dữ liệu nghiên cứu, không có chỉ thị nào được thực thi. Không ảnh hưởng tới độ tin cậy của các claim trong báo cáo này (đều bắt nguồn từ PDF/docs chính chủ, đối chiếu được).

## 1. Nội dung thật — CCAR-F vs CCAR-P cho thiết kế skill/plugin

**CCAR-F** (5 domain, 60 câu): Agentic Architecture 27% · Tool Design & MCP 18% · **Claude Code Configuration & Workflows 20%** · Prompt Engineering 20% · Context Management 15%. Task Statement 3.2 nói thẳng về `SKILL.md`, frontmatter `context: fork`/`allowed-tools`/`argument-hint`, phân biệt skill (gọi theo tình huống) vs CLAUDE.md (luôn nạp).

**CCAR-P** (7 domain, 63 câu): "Skills" chỉ xuất hiện ở Domain 2 như một chiến thuật tái dùng prompt; Domain 7 (Developer Productivity, liên quan Claude Code nhất) chỉ **7% — nhẹ nhất toàn bài**, không Task Statement chi tiết. Đã đọc toàn văn PDF, không phải thiếu sót tìm kiếm.

**Khái niệm cụ thể tìm được** (đầy đủ ở digest `noi-dung-that-r1-1.md`): progressive disclosure 3 tầng (metadata ~100 token luôn nạp → body <5k token khi trigger → file phụ trợ khi cần, SKILL.md nên <500 dòng) [1]; `disable-model-invocation` (chỉ người dùng gọi, side-effect) vs `user-invocable: false` (chỉ Claude gọi, kiến thức nền) [2]; evaluation-driven skill development (baseline không skill → gap → 3 eval scenario → instruction tối thiểu → lặp; Anthropic tự nhận **chưa có** eval built-in) [3]; `context: fork` chạy skill trong subagent cô lập, mặc định chạy background [4]; `plugin.json` — component phải ở root plugin, field `skills/` luôn **cộng thêm** vào mặc định (khác các field path khác — thay thế) [5]; 3 biến môi trường đặc thù (`${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${CLAUDE_PROJECT_DIR}`) [5]; `userConfig` cho cấu hình nhạy cảm lúc enable plugin [6]; tránh "capability bloat" (18 tool thay vì 4-5 làm giảm độ tin cậy chọn tool) [7], cấu trúc lỗi MCP chuẩn (`isError`/`errorCategory`/`isRetryable`) [7].

## 2. Đối chiếu với van-dao thật

*Đối chiếu trực tiếp với `ARCHITECTURE-SPINE.md` (214 dòng, đọc trọn) và đặc tả §12.4-12.5/§13.1/§15.*

| # | Khái niệm CCAR-F | Đối chiếu van-dao | Đánh giá |
|---|---|---|---|
| A | `${CLAUDE_PLUGIN_DATA}` = `~/.claude/plugins/data/{id}/`, bền qua update [5] | Van-dao dùng `~/.vandao/` — khác quy ước, chưa ghi lý do tường minh [8] | **Đáng ghi lại lý do** — divergence hợp lý (ổn định qua reinstall, người dùng tự tìm được, khớp "dữ liệu không giấu"), nhưng chưa có dòng nào trong spine/AGENTS.md giải thích, dễ bị "sửa cho đúng chuẩn" sau này mà mất lý do gốc |
| B | Compact giữ tối đa 5k token/skill, tổng ngân sách skill toàn phiên 25k token [1] | AD-8 có đúng nguyên tắc "chặn trên cố định kích thước" nhưng không có số cụ thể; 8 skill × 5k có thể vượt 25k nếu nạp cùng lúc [9] | **Đáng thêm số cụ thể** khi viết SKILL.md thật — không phải gap thiết kế |
| C | SKILL.md nên <500 dòng, progressive disclosure 3 tầng [1] | §12.5 "Micro-file cho thư linh" (tách `buoc/`, SKILL.md chỉ định tuyến) **đã tự đến đúng pattern này độc lập** [10] | **Xác nhận đúng hướng** — chỉ thiếu ngưỡng số 500 dòng để tự kiểm |
| D | `context: fork` — cơ chế native tạo subagent cô lập từ 1 skill [4] | Van-dao dùng `agents/*.md` riêng (custom subagent bền, có tên) thay vì fork tạm thời [11] | Cả hai hợp lệ trong Claude Code, lựa chọn của van-dao hợp lý cho nhu cầu lặp lại nhiều nơi — đáng 1 dòng ghi lý do so với lựa chọn kia |
| E | `userConfig` với `sensitive: true` [6] | Đã dùng đúng cho `communication_language` (NFR8, verify chạy thật 2026-08-26) [12] | **Khớp 100%** — không cần hành động |
| F | Component phải ở root plugin, không trong `.claude-plugin/` [5] | Cây thư mục van-dao (đặc tả §15) đã đúng [12] | **Khớp** — không cần hành động |
| G | `disable-model-invocation` cho side-effect, chỉ người dùng gọi [2] | Đã dùng đúng cho `dao-tam` (đệ tử sở hữu, tự ghi) [12] | **Khớp** — không cần hành động |
| H | MCP (Domain 2 CCAR-F 18%, Domain 3 CCAR-P 19% — trọng tâm lớn cả 2 chứng chỉ) | Van-dao không dùng MCP server nào — mọi tool là script Python nội bộ hoặc subagent tự định nghĩa [13] | **Không áp dụng** — ngoài phạm vi kiến trúc hiện tại, không phải thiếu sót |

## Khuyến nghị

**Đã áp dụng (2026-08-27, cùng ngày với nghiên cứu này) — cả 4 khuyến nghị hành động được đều đã đưa vào `ARCHITECTURE-SPINE.md` thật, `updated` bump lên 2026-08-27, `sources:` đã trỏ về nghiên cứu này:**

1. ~~Thêm 1 dòng giải thích lý do `~/.vandao/` khác `${CLAUDE_PLUGIN_DATA}`~~ → đã thêm vào mục "Cây thư mục — dữ liệu người học" (2 gạch đầu dòng: install-identity risk vs đường dẫn ổn định/khớp NFR5).
2. ~~Áp số cụ thể 500 dòng/5k token mỗi skill, 25k token tổng vào AD-8~~ → đã thêm nguyên văn con số + nguồn vào AD-8, nối với §12.5 micro-file đã có.
3. ~~Ghi lý do chọn `agents/*.md` thay vì `context: fork`~~ → đã thêm vào AD-4, giải thích theo đúng nhu cầu "tái dùng ổn định ở nhiều nơi gọi" của 4 vai chấm.
4. Không cần hành động cho userConfig, cấu trúc plugin.json, `disable-model-invocation` — đã khớp sẵn, không đổi.

CCAR-P không đáng nghiên cứu thêm cho đúng câu hỏi này — nội dung skill/plugin design của nó không vượt quá những gì CCAR-F đã cho.

## Câu hỏi còn mở

- §12.2 "Phạm vi đọc tài liệu" chưa đối chiếu với quy tắc "tránh nested reference sâu >1 cấp" của CCAR-F — chưa đủ thời gian trong lượt này, độ ưu tiên thấp.
- Chưa đọc toàn văn `anthropics/claude-code/plugins/plugin-dev/skills/skill-development/SKILL.md` (Anthropic tự "dogfood" quy tắc viết skill) — chỉ có digest qua WebFetch, có thể còn chi tiết chưa khai thác nếu cần đào sâu thêm.

## Nguồn

| # | Claim/phát hiện | Nguồn | Ngày | Truy cập | Độ tin cậy |
|---|---|---|---|---|---|
| 1 | Progressive disclosure 3 tầng, SKILL.md <500 dòng | CCAR-F Exam Guide PDF v1.0 (S3 Anthropic Partner Academy) + [platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | 2026-07 | 2026-08-27 | Cao (sơ cấp) |
| 2 | `disable-model-invocation` vs `user-invocable: false` | [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) | 2026-07 | 2026-08-27 | Cao (sơ cấp) |
| 3 | Evaluation-driven skill development | platform.claude.com best-practices | 2026-07 | 2026-08-27 | Cao (sơ cấp) |
| 4 | `context: fork` chạy subagent cô lập | code.claude.com/docs/en/skills | 2026-07 | 2026-08-27 | Cao (sơ cấp) |
| 5 | `plugin.json`, biến môi trường, path behavior `skills/` | [code.claude.com/docs/en/plugins-reference](https://code.claude.com/docs/en/plugins-reference) | 2026-07 | 2026-08-27 | Cao (sơ cấp) |
| 6 | `userConfig` với `sensitive: true` | plugins-reference | 2026-07 | 2026-08-27 | Cao (sơ cấp) |
| 7 | Capability bloat, envelope lỗi MCP | CCAR-F Exam Guide PDF, Domain 2 | 2026-07 | 2026-08-27 | Cao (sơ cấp) |
| 8 | `~/.vandao/` khác `${CLAUDE_PLUGIN_DATA}` | Tổng hợp bởi người điều phối từ [5] + `AGENTS.md`/`ARCHITECTURE-SPINE.md` van-dao | 2026-08-27 | 2026-08-27 | Cao (verified) |
| 9 | AD-8 thiếu số ngân sách token cụ thể | Tổng hợp từ [1] + `ARCHITECTURE-SPINE.md` AD-8 | 2026-08-27 | 2026-08-27 | Cao (verified) |
| 10 | §12.5 micro-file = progressive disclosure độc lập | Tổng hợp từ [1] + đặc tả §12.5 | 2026-08-27 | 2026-08-27 | Cao (verified) |
| 11 | `agents/*.md` thay vì `context: fork` | Tổng hợp từ [4] + `ARCHITECTURE-SPINE.md` AD-1/AD-4 | 2026-08-27 | 2026-08-27 | Cao (verified) |
| 12 | userConfig/plugin.json/disable-model-invocation khớp | Tổng hợp từ [2][5][6] + NFR8 (`epics.md`), đặc tả §13.1, §15 | 2026-08-27 | 2026-08-27 | Cao (verified) |
| 13 | MCP không áp dụng cho van-dao | Tổng hợp từ [5][7] + `ARCHITECTURE-SPINE.md` (không có `.mcp.json`/MCP server nào) | 2026-08-27 | 2026-08-27 | Cao (verified) |

## Bản đồ độ cũ (staleness)

13/13 claim verified, 0 unverified, 0 overturned. Mốc tái kiểm: exam guide v1.0 hiệu lực tới 07/2027 (chu kỳ 12 tháng theo lệ chứng chỉ) — claim nhóm `mechanism` (nội dung thi) tái kiểm **2027-07-01** nếu Anthropic ra bản exam guide mới. Claim nhóm `comparison` (đối chiếu van-dao) tái kiểm khi `ARCHITECTURE-SPINE.md` hoặc SKILL.md thật thay đổi — sớm nhất khi van-dao bắt đầu viết skill thật (van-dao/skills/ hiện còn rỗng).
