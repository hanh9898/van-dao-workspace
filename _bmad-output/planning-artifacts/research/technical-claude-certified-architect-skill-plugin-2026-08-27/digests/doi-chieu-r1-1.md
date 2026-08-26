# Digest — Đối chiếu CCAR-F/CCAR-P với van-dao (round 1)

*Thực hiện trực tiếp bởi người điều phối (không qua subagent riêng) — tránh lỗi placeholder-rỗng đã gặp ở lần đối chiếu ghost-writer trước đó. Nguồn phía van-dao: `ARCHITECTURE-SPINE.md` đọc trọn (214 dòng) + đặc tả §12.4-12.5, §13.1, §15 đã đọc trong phiên. Nguồn phía CCAR: `digests/noi-dung-that-r1-1.md`.*

## Đáng hành động — cụ thể

**1. `~/.vandao/` khác `${CLAUDE_PLUGIN_DATA}` của Anthropic — divergence có chủ đích, chưa ghi lý do tường minh**
- CCAR-F: Anthropic quy ước dữ liệu bền vững của plugin nằm ở `${CLAUDE_PLUGIN_DATA}` = `~/.claude/plugins/data/{id}/`, sống sót qua update.
- van-dao: dữ liệu người học nằm ở `~/.vandao/` (home-relative, KHÔNG theo quy ước trên) — đã xác nhận qua AGENTS.md ("dữ liệu người học ở ~/.vandao/, cố định").
- Đánh giá: **đáng ghi lại lý do**, không phải lỗi. `${CLAUDE_PLUGIN_DATA}` gắn với *install-identity* của plugin (đường dẫn có `{id}` mờ) — nếu plugin cài lại/đổi tên/đổi marketplace có rủi ro mồ côi dữ liệu; `~/.vandao/` là đường dẫn ổn định, người dùng tự tìm/tự backup được — khớp đúng triết lý "dữ liệu ở lại máy người dùng, không giấu" (NFR5, Policy AGENTS.md). Nên thêm 1 dòng vào ARCHITECTURE-SPINE.md hoặc AGENTS.md giải thích đây là lựa chọn có ý thức khác quy ước mặc định, để người sau không "sửa cho đúng chuẩn" mà phá mất lý do gốc.

**2. Ngân sách token cụ thể của Anthropic (25k tổng compact / 5k mỗi skill) chưa vào AD-8**
- CCAR-F/docs Claude Code: compact giữ tối đa 5k token/skill, tổng ngân sách skill toàn phiên 25k token.
- van-dao: AD-8 có đúng NGUYÊN TẮC ("chặn trên cố định kích thước") nhưng không có SỐ cụ thể. Van-dao có 8 skill (nhap-mon, thu-bi-kip, thu-linh, truong-mon, ha-son, phuc-menh, khao-thi, dao-tam) — nếu nhiều skill cùng nạp một phiên, 8×5k=40k có thể vượt trần 25k thật của nền tảng.
- Đánh giá: **đáng thêm số cụ thể** khi viết SKILL.md thật — không phải gap thiết kế (AD-8 đã đúng hướng), chỉ thiếu con số để tự kiểm khi viết.

**3. Progressive disclosure — van-dao đã có tinh thần (AD-8 + §12.5 micro-file), thiếu ngưỡng số**
- CCAR-F: SKILL.md nên dưới 500 dòng, body dưới 5k token, tầng 3 (file phụ trợ) nạp khi cần.
- van-dao: §12.5 "Micro-file cho thư linh" (tách `buoc/`, mỗi bước một file, SKILL.md chỉ định tuyến) ĐÚNG LÀ progressive disclosure tầng 2→3 trong thực hành — **đã tự đến pattern này độc lập, không cần học thêm về nguyên tắc**. Chỉ thiếu ngưỡng số (500 dòng) làm tiêu chí tự kiểm khi viết.
- Đánh giá: **xác nhận đúng hướng**, chỉ bổ sung số khi cần.

**4. `context: fork` (skill-forked subagent) vs `agents/*.md` (custom subagent bền) — van-dao chọn cơ chế khác, hợp lý nhưng chưa nêu lý do so với lựa chọn kia**
- CCAR-F: `context: fork` trong frontmatter SKILL.md là cách Claude Code native tạo subagent cô lập từ MỘT skill.
- van-dao: dùng `agents/*.md` riêng (nghiem-cong.md, phuc-khao.md, truong-lao.md, chu-giai.md) — cơ chế custom-subagent-type có tên, bền, không phải fork tạm thời từ 1 skill.
- Đánh giá: **cả hai đều hợp lệ trong Claude Code**, van-dao chọn đúng cho nhu cầu (4 vai chấm cần định nghĩa `tools:`/`skills:` riêng, dùng lặp lại nhiều nơi — hợp với custom agent hơn fork một-lần). Không phải gap, nhưng đáng 1 dòng ghi lý do chọn `agents/*.md` thay vì `context: fork` để tránh câu hỏi "sao không dùng cơ chế mới hơn" sau này.

## Xác nhận đúng — không cần hành động

**5. `userConfig`** — CCAR-F mô tả field string/number/boolean với `sensitive: true`, prompt lúc enable plugin. Van-dao ĐÃ dùng đúng cơ chế này cho `communication_language` (NFR8, verify chạy thật 2026-08-26). Khớp 100%.

**6. Cấu trúc `plugin.json`/component ở root** — CCAR-F: mọi thư mục component phải ở ROOT plugin, không trong `.claude-plugin/`. Cây thư mục van-dao (đặc tả §15, ARCHITECTURE-SPINE.md Structural Seed) đã đúng: `.claude-plugin/plugin.json` tách riêng, `skills/`/`agents/`/`hooks/`/`bin/` đều ở root. Khớp.

**7. `disable-model-invocation`** — CCAR-F: dùng cho tác vụ có side-effect, chỉ người dùng gọi được. Van-dao dùng đúng cho `dao-tam` (đệ tử sở hữu, tự ghi — §13.1 Bậc 1 #11). Khớp.

## Không áp dụng

**8. MCP (Model Context Protocol)** — cả CCAR-F (Domain 2, 18%) lẫn CCAR-P (Domain 3, 19%) đều nặng về MCP. Van-dao KHÔNG dùng MCP ở đâu cả — mọi tool là script Python nội bộ (`bin/*.py`) hoặc subagent tự định nghĩa, không có `.mcp.json`/MCP server nào trong kiến trúc. Toàn bộ nội dung MCP của cả 2 chứng chỉ không áp dụng cho van-dao — không phải thiếu sót, chỉ là ngoài phạm vi kiến trúc hiện tại.

## Đánh giá khung: CCAR-F vs CCAR-P cho đúng nhu cầu này

CCAR-F (Domain 3, 20%, có Task Statement riêng cho skill/plugin) đóng góp gần như toàn bộ nội dung hữu ích ở trên. CCAR-P chỉ nhắc "Skills" như MỘT chiến thuật tái dùng prompt trong phạm vi kiến trúc/governance/stakeholder doanh nghiệp rộng hơn — không có Task Statement riêng cho thiết kế skill/plugin cụ thể (Domain 7, phần gần nhất, chỉ 7% và không chi tiết). Với đúng câu hỏi "thiết kế skill trong plugin, thiết kế plugin" — **CCAR-P gần như không đóng góp gì mới ngoài những gì CCAR-F đã có.**
