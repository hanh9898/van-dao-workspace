# Digest — Cơ chế vận hành thật của ghost-writer (round 1)

*Nguồn: đọc trực tiếp mã nguồn cục bộ plugin đã cài (`~/.claude/plugins/cache/claude-community/claude-ghost-writer/1.0.0/`) — bản clone git thật của `simonediroma/claude-ghost-writer`, độ tin cậy sơ cấp (không qua web fetch trung gian). File đã đọc: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `.claude-plugin/plugin.json`, `book.config.json`, `book-memory.md`, `outline.md`, `skills/resume/SKILL.md`, `skills/demolish/SKILL.md`, `skills/integrate/SKILL.md`, `skills/consistency-check/SKILL.md`, `skills/longform-upgrade/SKILL.md`, cây thư mục đầy đủ.*

## 1. Hình dạng tổng thể

27 skill (đúng số CHANGELOG khai, đếm khớp cây thư mục `skills/`), một tác giả (`simone di roma`), MIT license, version 1.0.0 phát hành **một lần** ngày 2026-05-10 — không có lịch sử iterate qua nhiều bản. `git log` cục bộ chỉ có 1 commit (merge PR publish) — bản clone nông, không phản ánh lịch sử thật của repo gốc trên GitHub.

4 nhóm skill theo vòng đời: **Onboarding** (chạy 1 lần: `session-start` → `setup-author` → `setup-book` → `setup-voice`) → **Chu trình viết** (lặp mỗi chương: `ask-before-writing`/`freeflow` → `write` → `demolish`/`demolish-persona` → `integrate`) → **Consistency định kỳ** (mỗi 3-4 chương) → **Closing** (1 lần cuối: `write-opening` → `write-closing` → `manuscript-final`). Có lớp "macro command" (`start`/`chapter`/`review`/`finish`) gói nhiều skill nguyên tử thành 1 lệnh cho tác giả không muốn tự điều phối trình tự.

## 2. Cơ chế đáng chú ý (trích nguyên văn logic, không diễn giải)

**`resume`** — "lệnh duy nhất cần nhớ". Đọc NHANH 5 nguồn cố định (book.config.json, outline.md, sessions/, file mới sửa nhất trong chapters/, chỉ phần Summary của demolition-history.md) — tường minh cấm đọc sâu ("Do not read full chapter files. Do not read full memory files."). Luôn xuất đúng 3 khối (LAST TIME / WAITING / NEXT), luôn đúng 1 khuyến nghị (không bao giờ liệt kê nhiều lựa chọn) theo một bảng quyết định if/else cố định 8 nhánh.

**`demolish`** — máy trạng thái phê bình một-lỗi-một-lúc, không cho gợi ý giải pháp trong pha phê bình. Đọc lịch sử phê bình cũ trước (Demolition Log của chương + demolition-history.md cấp sách) — không nêu lại vấn đề đã `resolved`/`integrated`, ưu tiên nêu lại vấn đề `deferred` trước vấn đề mới. Khi tác giả bí, có chuỗi leo thang 4 bước cố định: diễn đạt lại đơn giản hơn → thu hẹp về đúng 1 claim → hỏi trực giác (không cần biện luận) → đưa 3 lối thoát có cấu trúc (Modify/Narrow/Accept) — tác giả tự điền nội dung, hệ thống không bao giờ điền hộ. Hết 4 bước vẫn bí → ghi `deferred` chính thức vào log, không ép tiếp. Trạng thái mỗi vấn đề: `resolved` / `deferred` / `accepted-limitation`.

**`integrate`** — không bao giờ áp dụng thay đổi khi chưa xác nhận tường minh, một thay đổi một lúc, sau mỗi thay đổi tự hỏi "cascading effects" (ảnh hưởng dây chuyền sang phần khác của văn bản không). Có bước "Declarations" — với phê bình bị từ chối tích hợp (declared out of scope), đề xuất chính văn bản tự thừa nhận giới hạn đó để "phòng thủ trước" độc giả khó tính. **Điểm lệch với nguyên tắc đã tuyên bố**: README nêu "Memory is explicit — every term, promise, and demolition cycle is written down", nhưng Phase 5 bước 4 của `integrate` quy định: nếu ≥3 đoạn bị viết lại đáng kể trong vòng tích hợp, **âm thầm ghi đè `voice-sample.md`** bằng đoạn trích mới nhất — "Do not mention this to the author." Đây là bộ nhớ ngầm, mâu thuẫn với tuyên bố "mọi thứ đều ghi rõ ràng".

**`consistency-check`** — đọc `book-memory.md` như bảng dữ liệu có cấu trúc (Defined Terms/Central Claims/Open Promises/Examples/Chapter Summary Log), đối chiếu từng mục với toàn văn, tường minh "không lặp lại việc đã ghi trong demolition-history.md — chỉ xác minh còn hiệu lực hay đã giải". Output phân 3 tầng mức độ nghiêm trọng: CRITICAL / SIGNIFICANT / MINOR — mỗi phát hiện có khuôn cố định (định nghĩa gốc vs cách dùng lệch, hệ quả cụ thể).

**`longform-upgrade`** — tự động đề xuất kích hoạt khi đếm đủ 10 chương hoàn thành (skill `write`/`chapter` tự kiểm ngưỡng này sau mỗi lần integrate), có thể chạy tay bất kỳ lúc nào. Cam kết tường minh "không đổi nội dung, chỉ đổi cách quản lý context". Sau khi nâng cấp: các skill thường ngày chỉ đọc global index (`book-memory.md` rút gọn) + file memory của phần hiện tại + phần liền trước (chỉ đoạn bàn giao) + tóm tắt chương lân cận + toàn văn chương đang làm — **lazy reading**. Chỉ 2 skill (`consistency-check`, `manuscript-final`) còn đọc toàn bộ. Trước khi đổi cấu trúc phải hỏi tác giả xác nhận cách chia "Part" (không tự quyết).

## 3. Xác minh nghi vấn dữ liệu mẫu (đã nêu ở brief)

`book.config.json`, `book-memory.md`, `outline.md` ở gốc repo là **template rỗng có cú pháp placeholder ngoặc vuông** (`[term]`, `[claim]`, `Your Book Title`, `Describe your ideal reader in one sentence`, `[date]`...) — xác nhận là scaffold trạng thái-ban-đầu tác giả cố ý đóng gói làm schema, KHÔNG phải dữ liệu thật/riêng tư bị lẫn vào. `memory/part-template.md`, `sessions/session-template.md`, `chapters/example-chapter.md`, `personas/custom-template.md` cũng đúng quy ước đặt tên "-template"/"example". Kết luận: không có vấn đề rò rỉ dữ liệu.

## 4. Chưa xác nhận được (cần nhánh ecosystem)

- Không có tín hiệu cộng đồng thật (sao/fork/issue/PR, người dùng ngoài tác giả) — clone cục bộ chỉ có 1 commit, không phản ánh lịch sử GitHub thật.
- Chưa kiểm được project gốc `quantum_fatalism` (được README dẫn là nguồn phương pháp) có gì thêm không.
- Chưa có bằng chứng nào về việc phương pháp này đã dùng thật để hoàn thành 1 cuốn sách xuất bản — mọi nội dung đọc được đều là template rỗng.
