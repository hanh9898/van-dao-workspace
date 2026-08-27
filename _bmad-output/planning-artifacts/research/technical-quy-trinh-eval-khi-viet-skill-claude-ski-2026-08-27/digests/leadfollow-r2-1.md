# Digest — lead-following round 2 (đóng 3 manh mối treo từ round 1)

## Findings

**1. GitHub Issue #490 (anthropics/skills) — KHÔNG bàn trình tự eval đa-skill**
Claim: Issue chỉ bàn vấn đề TỔ CHỨC THƯ MỤC (workspace eval bị tạo cùng cấp với skill trong `.claude/skills/`, gây nhầm lẫn và khó version-control), đề xuất tách workspace eval ra thư mục riêng. KHÔNG đề cập trình tự/thời điểm viết eval khi dự án có nhiều skill.
Source: https://github.com/anthropics/skills/issues/490 (tác giả `limerickgds`, mở 2026-03-02, comment `Chi-teck` 2026-03-17)
Publisher: GitHub (anthropics/skills) | pub_date: 2026-03-02 | accessed: 2026-08-27 | confidence: cao (đọc trực tiếp) | class: primary — negative finding cho câu hỏi trọng tâm

**2. Hamel Husain / Shreya Shankar — "evaluation is part of the development process rather than a distinct line item"**
Claim: Câu trích xác nhận nguyên văn trong "LLM Evals: Everything You Need to Know" (hamel.dev, đồng bản Substack). Đọc trọn ngữ cảnh: KHÔNG bàn trực tiếp câu hỏi đơn-lẻ-vs-nhiều-thành-phần. Nguyên tắc chính của bài là "Start with error analysis, not infrastructure" — bắt đầu phân tích lỗi ngay khi có output, không định nghĩa rõ phải hoàn thành nhiều component trước; với workflow nhiều bước chỉ khuyên "segment your error analysis by workflow stages".
Source: https://hamel.dev/blog/posts/evals-faq/ (+ https://hamelhusain.substack.com/p/evals-faq)
Publisher: hamel.dev / Hamel Husain (Substack) | pub_date: ~2025-05-28 (hamel.dev), bản Substack cập nhật ~2025-08 | accessed: 2026-08-27 | confidence: trung bình-cao (câu trích khớp 2 nguồn độc lập; phần "không bàn trực tiếp" là suy luận từ ngữ cảnh) | class: primary cho câu trích, secondary cho suy luận

**3. PwC — "Validating multi-agent AI systems: From modular testing to system-level governance" — bằng chứng trực tiếp, đi NGƯỢC hướng "hoãn eval"**
Claim: Khuyến nghị rõ ràng: validate từng agent riêng lẻ TRƯỚC ("Individual agents in MAS may require pre-deployment testing and validation..."), rồi mới validate hệ thống tích hợp SAU ("Once agents are validated individually, the assembled system should undergo additional testing to evaluate end-to-end interactions, emergent risks, and overall system reliability"). Đây là bằng chứng trực tiếp NGƯỢC với "hoãn eval hình thức hoá từng skill đến khi có vertical slice" — mô hình PwC là phân lớp: modular/per-agent validation đi trước, system-level validation đi sau.
Source: https://www.pwc.com/us/en/services/audit-assurance/library/validating-multi-agent-ai-systems.html (đọc qua proxy r.jina.ai do URL gốc trả HTTP 403)
Publisher: PwC US (Audit & Assurance) | pub_date: không xác định trên trang | accessed: 2026-08-27 | confidence: trung bình (đọc qua proxy trung gian, chưa xác minh chéo bằng nguồn thứ hai độc lập — CẦN LƯU Ý khi dùng làm claim quyết định) | class: primary (nội dung gốc qua proxy, không phải snippet)

## Không tìm thấy
- Không có nguồn nào bàn trực tiếp, tường minh câu hỏi "có nên HOÃN eval hình thức hoá từng skill riêng lẻ đến khi có vertical slice hay không" trong bối cảnh multi-skill/multi-agent. PwC là nguồn gần nhất nhưng nói về THỨ TỰ TEST (agent riêng trước → hệ thống sau), không nói về việc trì hoãn VIẾT eval.
- Hamel/Shankar không đưa khuyến nghị tường minh về thời điểm khi có nhiều component.
- PwC mới đọc qua 1 proxy, chưa xác minh chéo nguồn thứ hai độc lập (cache Google/PDF) — do ngân sách round đã dùng 6/8 lượt.
