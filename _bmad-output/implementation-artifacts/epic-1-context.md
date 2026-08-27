# Epic 1 Context: Nhập môn, chỉ điểm & nạp bí kíp

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Epic 1 dựng luồng khởi động bắt buộc của toàn hệ thống: người học chọn ngôn ngữ giao tiếp, bái sư (đặt tên môn phái, khai vai/mạch muốn luyện, đặt tên riêng cho 4 vai đồng hành), được Trưởng môn chỉ điểm tên sách cụ thể để tự đi tìm — vì tàng kinh các ban đầu rỗng — rồi nạp cuốn sách tìm được (PDF/EPUB) vào kho, với hệ giải nghĩa được ý sách chứ không chỉ trích chữ nguyên văn. Đúng thứ tự: Bái sư → Chỉ điểm → *(Thỉnh sách, ngoài hệ thống)* → Thu bí kíp. Không epic phía sau (lộ đồ, dạy, soát) chạy được trước khi một bí kíp đã vào kho qua epic này.

## Stories

- Story 1.1: Thiết lập ban đầu — ngôn ngữ giao tiếp
- Story 1.2: Bái sư — đặt tên môn phái, khai vai/mạch, đặt tên 4 vai
- Story 1.3: Chỉ điểm — Trưởng môn gọi tên sách
- Story 1.4: Thu bí kíp

## Requirements & Constraints

- Ngôn ngữ giao tiếp chỉ hỏi đúng một lần lúc bật plugin lần đầu; phiên sau nạp lại lựa chọn đã lưu.
- Nghi thức (bái sư, thu bí kíp) chỉ kích hoạt khi có việc thật đứng sau (khai vai/mạch xong; sách đã thật sự vào kho) — không phát cho hành động chưa tốn công, và gọi lại lệnh nhập môn khi đã có hồ sơ không được tạo hồ sơ mới đè lên hay kích hoạt lại nghi thức vô cớ.
- Bái sư cho người học đặt tên riêng cho 4 vai trực tiếp nói chuyện với mình — gợi ý sẵn kèm tự nhập, không ép chọn từ danh sách; vai không nói với người học thì không hỏi tên. Người chưa biết muốn luyện gì thì hỏi VAI trước, không hỏi mạch trước.
- Mỗi chỉ điểm sách nêu đủ 5 trường (tên, tác giả, năm/ấn bản, công pháp hay tâm pháp, vì sao) — không đưa tên trần; số lượng co giãn theo đã biết/chưa biết muốn luyện; mức chắc chắn của gợi ý phải nói trước khi đưa danh sách, không phải sau; sách công pháp luôn kèm gợi ý tâm pháp đỡ trần.
- "Bản hỏng" (sách đúng, bản không rút được chữ — giữ nguyên trong chỉ điểm, khuyên tìm bản khác) xử lý khác hẳn "không thấy" (chỉ điểm quyển khác) — gộp hai nhánh là mất một quyển vì lỗi phân loại.
- Hệ phải giải nghĩa được ý và nội dung cơ bản của sách — không chỉ trích chữ nguyên văn — và tự đánh dấu chỗ có độ tin cậy giải nghĩa thấp.
- Khi không rút được chữ, hoặc rút được nhưng không thành câu có nghĩa, hệ dừng ngay, báo tìm bản khác — không OCR, không tạo bí kíp rỗng, không đoán liều.
- Pha thiết kế sư phạm (xương sống, tiêu chí đạt, điểm hạ sơn) dừng chờ người dùng tự sửa và duyệt — máy chỉ đề xuất kèm lý do, không tự quyết; pha sinh chương không chạy nếu chưa duyệt.
- Bí kíp có hai mức hợp lệ: đủ dùng (vào kho ngay) và đủ chuẩn (chia sẻ được, bồi thêm sau khi học chương đó); dạy ở mức đủ dùng phải nói rõ đang chấm theo mục tiêu, chưa có tiêu chí chi tiết.
- Thu trùng một cuốn sách đã có trong kho không tạo bản sao hay ghi đè bản gốc (bí kíp gốc bất biến) — báo rõ đã có, hỏi người học muốn làm gì tiếp.

## Technical Decisions

- Cơ chế chọn ngôn ngữ đã verify chạy thật: cài plugin không kèm cấu hình tường minh thì nền tảng KHÔNG tự chặn/hỏi, chỉ cảnh báo — skill nhập môn phải tự kiểm giá trị đã đặt chưa và chủ động hướng dẫn cấu hình lại. Đọc cấu hình này phải qua cơ chế thế chỗ runtime, không đọc thẳng từ file plugin tĩnh — bug dạng này từng lọt bản nháp, chỉ lộ khi chạy eval hành vi thật.
- Cơ chế chặn AI ghi hộ nội dung tự-viết (cho "nhập môn ký") phải xây ở tầng skill/tool thật, không chỉ quy ước lời nói trong prompt — một ca thử "AI cố ghi hộ" phải thất bại rõ ràng. Đạo tâm (Epic 5) tái dùng nguyên vẹn cơ chế này sau này, không xây lại.
- Phụ thuộc ngoài cho trích xuất PDF/EPUB: lớp engine đã verify chạy thật trên PDF và EPUB thật; lớp skill hội thoại đi kèm CHƯA verify, phải verify khi triển khai thật. Độ phủ verify hiện còn hẹp (2 mẫu).
- Mỗi vùng dữ liệu học tập (con trỏ sách, nháp thiết kế sư phạm dở dang, nhật ký chỉ điểm) chỉ đúng một vai được ghi; vai khác chỉ đọc qua cơ chế lọc phạm vi theo mạch.
- Mọi đổi trạng thái là ghi thêm dòng mới vào log, không sửa tại chỗ; trạng thái hiện tại suy từ dòng gần nhất, kể cả khi dòng cuối ghi dở dang do crash.
- Nội dung skill/agent/command không trích số hiệu requirement hay số mục tài liệu kế hoạch — viết lại bằng lời tự nhiên, tự đủ nghĩa.
- Script mới dùng chung một envelope lỗi (ba mức lỗi chặn/cảnh báo/ghi chú, mã thoát cố định).

## Cross-Story Dependencies

- Thứ tự bắt buộc: Story 1.1 (ngôn ngữ) → Story 1.2 (bái sư, đồng thời xây cơ chế chặn-AI-ghi-hộ) → Story 1.3 (chỉ điểm) → Story 1.4 (thu bí kíp).
- Story 1.2 xây cơ chế tự-ghi/chặn-AI-ghi-hộ mà Story 5.1 (Epic 5 — đạo tâm) tái dùng nguyên vẹn, không xây lại.
- Epic 2 (lộ đồ trình duyệt) chỉ bắt đầu được sau khi Story 1.4 hoàn tất — lộ đồ sinh ngay khi một bí kíp vào kho thành công.
- Bước "thỉnh sách" (người học tự tìm sách ngoài đời thật), giữa Story 1.3 và 1.4, nằm ngoài phạm vi hệ thống.
