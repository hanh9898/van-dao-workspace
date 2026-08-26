# Đánh giá chéo: 4 nguồn kỹ thuật viết skill AI agent

**Loại:** Tổng hợp/phân tích (không phải một deep-recon run mới — đúc kết từ 4 báo cáo đã hoàn tất, không fetch nguồn mới).
**Ngày:** 2026-08-26.
**Phục vụ quyết định:** Cách viết SKILL.md/agents/hooks/customize.toml của Vấn Đạo.
**Nguồn gốc:** 4 báo cáo deep-recon đã Finalize (citation check + spot-check ngữ nghĩa đều sạch):

1. `research/technical-ky-thuat-viet-thiet-ke-skill-chu-dao-bma-2026-08-25/research.md` — BMAD-METHOD (đọc file cục bộ)
2. `research/technical-superpowers-obra-ky-thuat-skill-2026-08-25/research.md` — Superpowers, obra/superpowers (web)
3. `research/technical-claude-tutor-kirilxd-ky-thuat-skill-2026-08-25/research.md` — claude-tutor, kirilxd/claude-tutor (web)
4. `research/technical-github-copilot-custom-instructions-ky-th-2026-08-25/research.md` — GitHub Copilot custom instructions (web, tài liệu chính chủ)

## Khung đánh giá

5 trục kỹ thuật giữ nguyên xuyên cả 4 lượt nghiên cứu (để so sánh được trực tiếp): **(1) Cấu trúc & giao thức skill · (2) Giữ trạng thái/quy trình nhiều bước · (3) Điều phối subagent/đa vai · (4) Human-in-the-loop/gate · (5) Văn phong hướng dẫn model.** Với mỗi nguồn: bối cảnh, ưu điểm, nhược điểm, học được gì (có địa chỉ cụ thể trong Vấn Đạo), không nên học (và vì sao).

## Ma trận tổng hợp — ai mạnh nhất ở đâu

| Trục | BMAD-METHOD | Superpowers | claude-tutor | GitHub Copilot |
|---|---|---|---|---|
| Cấu trúc & giao thức | Khá — nhưng không đồng nhất nội bộ | **Mạnh nhất** — quy tắc số-từ, ngưỡng tách file tường minh | Khá — lớp `commands/` tách biệt có nguyên tắc rõ | Khá — chuẩn đa-nền, nhưng tự mâu thuẫn giới hạn độ dài |
| Giữ trạng thái xuyên phiên | **Mạnh nhất** — memlog append-only, atomic | **Yếu nhất** — không có gì tương đương | Trung bình — due-check nhẹ, đơn giản | Yếu — chỉ khuyến nghị checklist thủ công |
| Điều phối subagent | Khá — nhiều contract khác nhau tuỳ skill | **Mạnh nhất** — contract 4-status chặt, có quy tắc chống ô nhiễm | Không áp dụng (không có kiến trúc subagent) | Khá — Subagents chính thức, xác nhận độc lập nguyên lý |
| HITL/gate | **Mạnh nhất** — Plan Gate vs Reviewer Gate tách tên rõ | Khá — HARD-GATE phê duyệt, nhưng chỉ 1 loại | Không áp dụng | Khá — reviewer PR-level thật, nhưng khác granularity |
| Văn phong | Khá — persona rõ, nhưng thiếu quy tắc độ dài | **Mạnh nhất** — có phương pháp luận thực nghiệm (A/B test) | Yếu — không persona, không rào giọng điệu | Yếu nhất cho mục đích Vấn Đạo — chủ trương không persona |

## Phân tích từng nguồn

### BMAD-METHOD

**Bối cảnh:** Framework nội bộ đang dùng thật cho chính quy trình BMAD của Vấn Đạo (PRD, architecture, deep-recon...) — không phải nguồn ngoài, mà là công cụ đang vận hành.

**Ưu điểm**
- Trạng thái xuyên phiên mạnh nhất trong 4 nguồn: memlog append-only, ghi atomic (temp→fsync→rename), không có lệnh sửa/xoá, "trạng thái là một event chứ không phải cờ" — đúng bài toán "dự án dài, nhiều tuần, nhiều phiên" của Vấn Đạo.
- Phân biệt tường minh hai triết lý HITL khác nhau: Plan Gate (một hard-stop trước khi làm) và Reviewer Gate (dispatch song song soát sau) — không gộp chung thành "điểm duyệt".
- Kỷ luật cô lập ngữ cảnh nhất quán dưới nhiều tên gọi (research firewall, extract-don't-ingest) — subagent luôn ghi file trước, trả tóm tắt sau.
- `customize.toml` 3 lớp override (base→team→user, merge-theo-khoá cho mảng bảng) — cơ chế tuỳ biến production-grade, không phải ý tưởng.

**Nhược điểm**
- Không đồng nhất nội bộ cao: `bmad-review` (không persona, không memlog, dùng `## Execution`) và `bmad-prfaq` (state hoàn toàn khác — frontmatter `stage`) lệch mẫu rõ so với `bmad-prd`/`bmad-architecture`/`bmad-deep-recon` — dễ nhầm tưởng có một khuôn chung khi thực ra BMAD tự phân hoá theo hình dạng công việc.
- Không có quy tắc số-từ/độ dài tường minh cho SKILL.md — độ dài 50-136 dòng chỉ là dữ liệu quan sát, không phải luật viết ra.
- Không có phương pháp luận thực nghiệm (eval/pressure-test) để tự kiểm chứng một SKILL.md có thực sự hiệu quả hay chỉ "đọc thấy hợp lý".
- Digest contract không thống nhất — ít nhất 4 hình dạng khác nhau tuỳ skill (deep-recon, prd/architecture reviewer, review lens, prd reconcile) — mỗi skill tự phát minh lại.

**Học được gì cho Vấn Đạo** *(đã áp dụng một phần trong architecture spine)*
- Mẫu memlog-style append-only đã đúng hướng ở AD-2 (kiến trúc spine) — giữ nguyên.
- Phân biệt Plan Gate (F-1 lộ đồ) / Reviewer Gate (Nghiệm Công Sứ/Phúc Khảo Sứ) — đã ghi thành khuyến nghị, cần đặt tên tường minh khi viết SKILL.md thật.

**Không nên học:** cố ép một khuôn "On Activation" cứng nhắc giống hệt nhau cho mọi vai — chính BMAD cũng không làm vậy (bmad-review là bằng chứng ngược ngay trong nhà).

### Superpowers (obra) — 277k sao, hoạt động rất tích cực

**Bối cảnh:** Cùng nền Claude Code, nhưng triết lý khác hẳn — TDD-driven, evidence-based, tự nhận lệch khỏi hướng dẫn chính thức Anthropic dựa trên eval riêng.

**Ưu điểm**
- Duy nhất trong 4 nguồn có phương pháp luận **thực nghiệm** để viết skill: RED (baseline fail không skill) → GREEN (skill tối thiểu) → REFACTOR, có A/B test thật giữa các dạng hướng dẫn (bằng chứng cụ thể: prohibition-list có thể TỆ HƠN không có hướng dẫn nào).
- Quy tắc số-từ tường minh theo tầng tần suất nạp (<150/<200/<500 từ) + ngưỡng tách file (100+ dòng), có công cụ đo cụ thể (`wc -w`).
- Digest contract chặt cho subagent-driven-development: đúng 4 giá trị status cố định (DONE/DONE_WITH_CONCERNS/NEEDS_CONTEXT/BLOCKED).
- Mỗi quy tắc lớn đều có bằng chứng thực nghiệm cụ thể đi kèm, không chỉ khẳng định suông (ví dụ case "agent chỉ review 1 lần thay vì 2" khi description tóm tắt workflow).

**Nhược điểm**
- **Không có cơ chế trạng thái xuyên phiên nào** — plan là file markdown tĩnh, tiến độ chỉ nhị nguyên in_progress/completed trong phiên, không giải được bài toán "dự án dài nhiều tuần" của Vấn Đạo.
- Ceremony nặng: Iron Law viết hoa, thẻ giả-XML (`<HARD-GATE>`, `<EXTREMELY-IMPORTANT>`), bảng Rationalization dày đặc — hiệu quả với Superpowers (đã eval) nhưng **chưa có bằng chứng nó chuyển sang giọng điệu tu luyện của Vấn Đạo** mà không phá vỡ FR33.
- Cố tình lệch chuẩn Anthropic — một lựa chọn có rủi ro riêng (tooling chính thức có thể ưu tiên skill "chuẩn" hơn về lâu dài).

**Học được gì cho Vấn Đạo**
- Quy tắc số-từ theo tầng tải — cân nhắc thêm cho SKILL.md của `thu-linh` (nạp mỗi phiên) vs skill ít tải hơn.
- "Description chỉ mô tả khi-nào-dùng, không tóm tắt workflow" — áp dụng khi viết `agents/*.md`.
- "Match the Form to the Failure" — chọn dạng luật (cấm đoán/recipe/structural) theo loại lỗi quan sát được, thay vì mặc định "Never X" cho mọi luật.

**Không nên học:** Iron Law viết hoa/thẻ giả-XML nguyên trạng — xung khắc giọng điệu đã chọn cho Vấn Đạo; nguyên lý ("chọn form đúng loại lỗi") thì học, hình thức chữ thì không.

### claude-tutor (kirilxd) — cùng domain thật (dạy học qua AI)

**Bối cảnh:** Plugin nhỏ (5 skill, 115 sao), giải đúng bài toán sản phẩm của Vấn Đạo — không phải chỉ đúng kỹ thuật viết skill.

**Ưu điểm**
- Duy nhất cùng domain thật — bằng chứng trực tiếp (not by-analogy) về cách một plugin dạy-học-qua-AI khác đã tổ chức dữ liệu/luồng.
- Eval 2 tầng (trigger_evals routing-only + functional_evals chạy thật) là mẫu hình **cụ thể, nhỏ gọn, chuyển được gần nguyên trạng** — đóng đúng khoản nợ đặc tả §17 của Vấn Đạo.
- Lớp `commands/` tách biệt `skills/` có nguyên tắc rõ: pointer mỏng cho việc hội thoại, tự chứa logic cho việc máy móc.
- Kiến trúc 100% local-first, không gửi dữ liệu ra ngoài — khớp triết lý riêng tư Vấn Đạo đã có.

**Nhược điểm**
- Quy mô nhỏ, một tác giả — chưa bị thử thách ở độ phức tạp gần bằng Vấn Đạo (8 vai, nhiều tầng subagent, nhiều mạch tri thức).
- Không có persona/giọng điệu đặc trưng nào — không có gì để học về "giữ nhân vật" (nhu cầu ngược lại của Vấn Đạo).
- Trạng thái xuyên phiên đơn giản (chỉ due-check nhẹ lúc SessionStart) — chưa cần giải bài toán phức tạp kiểu đạo tâm/tâm ma của Vấn Đạo.

**Học được gì cho Vấn Đạo**
- Cấu trúc eval 2 tầng gần như nguyên trạng — ưu tiên cao, đóng khoản nợ §17 có sẵn thiết kế tham khảo cụ thể.
- Nguyên tắc "command là pointer mỏng vs. tự chứa logic" theo đích đến (hội thoại vs máy móc) — áp cho lớp `/vd:*` của Vấn Đạo.

**Không nên học:** thiếu rào chắn giọng điệu — không phải bằng chứng FR33 thừa, chỉ xác nhận đây là lựa chọn riêng của Vấn Đạo (thế giới quan tu luyện), không phải thông lệ ngành.

### GitHub Copilot — chuẩn đa-nền tảng, đa-vendor thật

**Bối cảnh:** Không phải một plugin đơn lẻ mà là sản phẩm của một hãng lớn, nhiều client (VS Code, JetBrains, CLI, GitHub.com) — vai trò trong bộ 4 nguồn là **kiểm tra cái gì phổ quát vs. cái gì đặc thù Claude Code**.

**Ưu điểm**
- Xác nhận độc lập: Subagent cô lập (clean context, stateless) + Handoffs + reviewer-gate là **nguyên lý phổ quát**, không phải phát minh riêng của BMAD/Claude Code — một hãng khác hội tụ về cùng mô hình.
- Danh sách lỗi thường gặp khi viết custom instructions được công bố tường minh (mơ hồ, quá dài, xung đột personal/repo/org) — một checklist "known failure mode" đáng tham khảo trực tiếp.
- VS Code đã native đọc `.claude/agents`/`.claude/rules` song song định dạng gốc — layout của Vấn Đạo đã được nhận diện phần nào bởi nền tảng thứ ba.

**Nhược điểm**
- **Điểm yếu rõ nhất trong 4 nguồn** về trạng thái nhiều bước: không có tính năng nền tảng nào, chỉ khuyến nghị tự viết file checklist thủ công.
- Tài liệu tự mâu thuẫn nhẹ giữa các trang (giới hạn "2 trang" vs "~1000 dòng") — cho thấy ngay cả tài liệu chính chủ một hãng lớn cũng chưa hoàn toàn nhất quán nội bộ.
- Không có file mẫu `copilot-instructions.md` hoàn chỉnh nào được công bố chính thức — chỉ có snippet minh hoạ.

**Học được gì cho Vấn Đạo**
- Xác nhận kiến trúc subagent/reviewer-gate hiện tại (AD-1, AD-7 spine) đứng vững khi đối chiếu chéo nền tảng — không cần điều chỉnh, chỉ củng cố niềm tin.
- Cảnh giác thuật ngữ "checkpoint" đa nghĩa (nén-context vs. tiến-độ-nhiều-bước) khi viết tài liệu kỹ thuật của Vấn Đạo.

**Không nên học:** văn phong "liệt kê sự thật dự án, không đóng vai nhân vật" — đúng cho coding-assistant tổng quát, sai bối cảnh cho một plugin có thế giới quan riêng như Vấn Đạo.

## Tổng hợp khuyến nghị cho Vấn Đạo (ưu tiên cao trước)

1. **[Cao]** Áp cấu trúc eval 2 tầng của claude-tutor gần nguyên trạng — đóng khoản nợ đặc tả §17. *(nguồn: claude-tutor Khuyến nghị #1)*
2. **[Cao]** Đặt tên tường minh Plan Gate (F-1) vs Reviewer Gate (Nghiệm Công Sứ/Phúc Khảo Sứ) khi viết SKILL.md/story — đã được cả BMAD lẫn Copilot xác nhận là hai mô hình khác nhau thật. *(nguồn: BMAD, Superpowers Khuyến nghị #3, Copilot Khuyến nghị #2)*
3. **[Trung bình]** Thêm quy tắc số-từ theo tầng tải + "description chỉ mô tả khi-nào-dùng" khi viết `agents/*.md`. *(nguồn: Superpowers Khuyến nghị #1, #2)*
4. **[Trung bình]** Đặt tên nguyên tắc "command pointer-mỏng vs tự-chứa-logic" nếu Vấn Đạo tách lớp `/vd:*` riêng khỏi skill. *(nguồn: claude-tutor Khuyến nghị #2)*
5. **[Thấp — chỉ xác nhận, không cần hành động]** Giữ nguyên kiến trúc subagent/reviewer-gate/memlog hiện tại của Vấn Đạo — cả 4 nguồn đối chiếu đều củng cố, không phát hiện gì cần sửa.

## Giới hạn của bản tổng hợp này

Đây là đúc kết lại nội dung ĐÃ verify ở 4 báo cáo gốc — không có claim mới nào chưa qua citation-check/spot-check. Nếu cần trích dẫn chi tiết (câu nguyên văn, dòng cụ thể), quay lại đúng báo cáo gốc tương ứng theo đường dẫn ở đầu tài liệu này.
