# Đối chiếu ARCHITECTURE-SPINE.md ↔ đặc tả (docs/VAN-DAO-dac-ta-v1.0.md)

Chạy lại sau khi lần trước rớt kết nối. Phạm vi: §4 (Tám vai), §5.7, §5.9, §6.6, §13.1, §15, §16.

## Finding 1 — AD-5 gộp sai hai loại dữ liệu của đặc tả, bỏ sót "Loại 2 thật" (mức: cao)

Đặc tả §5.9 định nghĩa **BA** loại, không phải hai:

- **Loại 1** — Phán quyết & cam kết, lưu nguyên văn (`tieu_chi_dat`, lộ đồ đã duyệt, bài nghiệm công, `dinh-vi`, đạo tâm, `phu_thuoc`/`xuong_song`).
- **Loại 2** — Diễn giải, **sinh tại chỗ, KHÔNG lưu** (lời giảng, cách trình bày một ý, ví dụ minh hoạ, câu hỏi dẫn dắt, cách diễn đạt phản hồi). Đặc tả nói rõ: *"Lưu chúng là có hại, không chỉ thừa: khoá thư linh vào cách giảng cũ và phá F5 (giảng lại bằng biểu diễn khác)."*
- **Loại 3** — Dẫn xuất, cache luôn dựng lại được (`ban-do.json`, hai khung nhìn tàng kinh các, bậc cảnh giới hiện tại). Luật: *"xoá đi phải dựng lại y nguyên; không dựng lại được nghĩa là nó thuộc loại 1 và đang bị xếp nhầm."*

Spine's AD-5 chỉ có "Loại 1" (khớp đúng) và "Loại 2 — tái sinh được... cache như `ban-do.json`" — **đây thực ra là Loại 3 của đặc tả, bị gán nhầm số**. Loại 2 thật (nội dung diễn giải cấm lưu) **hoàn toàn vắng mặt** trong spine.

Đây là khoảng trống tải nặng thật, không phải chỉ đặt sai tên: nếu một epic sau này quyết định "log lại lời giảng để debug/replay", nó không vi phạm AD nào hiện có trong spine — nhưng vi phạm thẳng đặc tả (§5.9, và cơ chế "giáo án tách làm hai" §5.9 — `ghi-chep/` chỉ ghi *sự kiện* (`{buoc, cach, ket_qua}`), không ghi nội dung). Hai epic độc lập (một lưu transcript "cho chắc", một không lưu) đều "tuân thủ" spine hiện tại nhưng lệch nhau thật.

**Đề xuất sửa:** đổi AD-5 thành ba loại đúng số của đặc tả, thêm rule "Loại 2 cấm lưu nguyên văn — chỉ ghi sự kiện kết quả (`{buoc, cach, ket_qua}`), không ghi nội dung diễn giải" — trực tiếp cứu cơ chế `ghi-chep/` đã có.

## Finding 2 — AD-1's cạnh "TL → PK không mang tiêu chí" khả năng SAI cạnh, spine kế thừa nguyên văn lỗi tiềm ẩn của đặc tả (mức: cao)

Spine AD-1 viết: *"Thư linh → Phúc Khảo Sứ không mang tiêu chí"* — trích đúng nguyên văn dòng 342 đặc tả ("TL → PK không mang tiêu chí — thấy tiêu chí thì Phúc Khảo Sứ chấm lại đúng thứ Nghiệm Công Sứ vừa chấm, trực giao mất").

Nhưng dòng này **mâu thuẫn với chính đặc tả ở hai chỗ khác trong cùng §4.1**:

1. **Diagram mermaid §4.1** (dòng ~317-319): cạnh thật là `GK -->|"bài thi + mục tiêu KHÔNG tiêu chí"| PK` — Giám khảo gửi cho Phúc Khảo Sứ, không phải Thư linh.
2. **Bảng thành phần §13.1 #11d**: Phúc Khảo Sứ là *"Người soát thứ hai ở **khảo thí quyển**"* — chấm bài thi cấp quyển do Giám khảo coi thi, không phải bài Thư linh dạy từng chương. Thư linh không hề gửi thư cho Phúc Khảo Sứ ở đâu trong toàn bộ đặc tả đã đọc.

Kết luận: cạnh đúng phải là **Giám khảo → Phúc Khảo Sứ**, không phải Thư linh → Phúc Khảo Sứ. Dòng 342 của đặc tả nhiều khả năng là lỗi đánh máy còn sót (TL/GK), và spine đã sao chép nguyên văn lỗi đó vào AD-1 thay vì đối chiếu chéo với diagram cùng mục.

**Đề xuất sửa:** AD-1 sửa thành "Giám khảo → Phúc Khảo Sứ không mang tiêu chí" (khớp diagram + vai trò thật); cân nhắc gắn cờ dòng 342 đặc tả để người dùng tự quyết có sửa nguồn hay không (ngoài phạm vi việc của spine).

## Finding 3 — "Ba luật chống context rot" (§5.9) chưa thành AD nào (mức: trung bình, trùng với phát hiện độc lập của rubric walker)

Ba luật (cỡ nạp mỗi phiên có chặn trên cố định · log lớn theo thời gian chỉ qua truy vấn lọc, không nạp toàn bộ · việc dùng-một-lần nằm trong subagent) là quyết định load-bearing thật — chính là lý do `tra-tang-kinh-cac` và `truong-lao` phải là subagent thay vì bước trong skill. Không AD nào trong spine hiện tại nói tới giới hạn kích thước nạp hay quy tắc "subagent cho việc dùng một lần" một cách tường minh — chỉ ngụ ý rải rác qua AD-4. Xác nhận độc lập: đây là gap thật, nên thêm AD riêng.

## Finding 4 — AD-3 Binds: xác nhận thiếu `bi-kip/**`, nhưng KHÔNG xác nhận được `dao-tam/**` như một vùng riêng (mức: thấp, lưu ý thận trọng)

Đối chiếu §4.3 (luồng dữ liệu): `bi-kip/` đúng là một vùng ghi riêng (Tàng kinh trưởng lão ghi 1 lần) không có trong Binds hiện tại của AD-3 — nên thêm.

Nhưng **không tìm thấy một thư mục top-level `dao-tam/` nào trong cây thư mục `~/.vandao/` ở §15** đã đọc (bi-kip/, custom/, tang-kinh/, truong-mon/, thu-linh/, truong-lao/, chu-giai/, ban-giao/, so-tay.jsonl, thuat-ngu.json — không có `dao-tam/`). "Đệ tử sở hữu sổ đạo tâm" (§4.2) là đúng, nhưng đường dẫn ghi cụ thể chưa xác định được từ các phần đã đọc — có thể nó nằm trong một vùng khác (vd. dưới `truong-mon/` hoặc một field trong `ho-so`). **Đừng thêm `dao-tam/**` vào Binds của AD-3 mà không xác minh đường dẫn thật trước** — tránh đưa vào spine một đường dẫn không tồn tại.

## Finding 5 — Citation AD-6 lệch nhẹ, nhưng bằng chứng thật ra mạnh hơn spine đang trình bày (mức: thấp/cosmetic)

AD-6 trích "đặc tả §16 bước 5, F-1→F0" — bước 5 thật ra bao **F-1 · F0 · F0′ · F1 · F2** (5 chặng, không chỉ F-1→F0). Đáng chú ý: **F0′ chính là chặng "phát hiện tâm ma xung đột"** (§5.12: *"F0′ phát hiện cách cũ xung đột"*) — đúng là điểm cụ thể trong đặc tả nơi thông tin mới (tâm ma) có thể phát sinh nhu cầu sửa lộ đồ giữa khoá, kịch bản AD-6 dùng làm lý do. Nên trích rõ F0′ thay vì gộp mờ "F-1→F0" — làm bằng chứng cho AD-6 mạnh hơn, không phải yếu đi.

## Không tìm thấy mâu thuẫn nào khác cho AD-2, AD-4, AD-7

Đối chiếu riêng: AD-2 (trạng thái suy từ artifact) khớp đúng §5.7. AD-4 (luật chọn loại thành phần) khớp đúng §13.1 dòng mở đầu. AD-7 (Hook chỉ gác lifecycle/tool-call thật) — không tìm thấy cơ chế duyệt-lại nào khác đã có sẵn trong đặc tả mà spine bỏ sót; đặc tả không giả định lộ đồ bất biến giữa khoá ở đâu cả — AD-6/AD-7 không mâu thuẫn với đặc tả, chỉ đơn thuần là khoảng trống đặc tả chưa lấp (đúng như phiên coaching đã xác định).
