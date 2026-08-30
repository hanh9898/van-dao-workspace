# Lens — Nghiệm thu và đánh giá giải pháp (BABOK: Solution Evaluation · Acceptance and Evaluation Criteria)

**Mục tiêu:** kiểm xem sau khi mọi việc trong kế hoạch làm xong, có **cách nào biết vấn đề ban đầu đã được giải hay chưa** — và ai là người có quyền nói câu đó.

Verification hỏi *"có đúng đặc tả không"*. Lens này hỏi *"có đúng vấn đề không"*. Qua cái đầu mà trượt cái sau là giao xong một thứ không ai cần.

## Stance

Đọc như người sẽ phải **ký nghiệm thu** và chịu trách nhiệm nếu ký sai. Câu hỏi thường trực: *"tôi lấy gì để nói cái này đạt?"*

## Sáu phép kiểm

### 1. Tiêu chí thành công đo được từ ngoài

Mỗi tiêu chí phải quan sát được mà **không cần tin lời người làm**. "Chất lượng tốt hơn" không đo được; "số lỗi ở vòng review giảm so với mốc N" thì đo được.

Chỉ ra tiêu chí nào đang phải tin lời.

### 2. Có mốc so sánh (baseline)

Tiêu chí dạng "giảm", "tăng", "ít hơn" chỉ có nghĩa khi có con số gốc. Thiếu baseline thì mọi kết quả đều có thể tuyên bố là cải thiện.

### 3. Ai xác nhận — và người đó khác người làm

BABOK đặt gate ở đây: **người yêu cầu công nhận, không phải người làm tự chấm**. Tài liệu có nêu ai ký không? Nếu tác giả vừa đặt tiêu chí vừa tự đánh giá, đó là finding.

### 4. Đo lúc nào

Ngay sau khi giao, hay sau một khoảng dùng thật? Nhiều giải pháp chỉ lộ ra là không giải được vấn đề sau vài tuần dùng. Tài liệu không hẹn thời điểm đo thì việc đo sẽ không xảy ra.

### 5. Điều gì cho biết giải pháp đã **thất bại**

Tiêu chí chỉ nói khi nào thành công là tiêu chí một chiều. Phải có ngưỡng để tuyên bố *không đạt* và quay lại — nếu không, mọi kết quả đều được diễn giải thành thành công một phần.

### 6. Giải pháp có tạo ra vấn đề mới không

Mỗi cơ chế được đề xuất đều có chi phí vận hành: thêm phụ thuộc, thêm bước, thêm thứ phải bảo trì. Tài liệu có nêu cái giá đó không, hay chỉ nêu lợi ích?

Đặc biệt chú ý cơ chế tự động: một phép kiểm tự động sai sẽ chặn nhầm việc đúng, và cái giá đó thường không được tính.

## Kiểm ngược

Giả sử toàn bộ kế hoạch được thực hiện đúng, đủ, đúng hạn — **vẫn có kịch bản nào mà vấn đề ban đầu không hề giảm không?** Nếu có, chuỗi tiêu chí đang thiếu một mắt.

## Đầu ra

Canonical fields, thêm:

- `tieu_chi` — tiêu chí hoặc mục bị soi (hoặc `(thiếu)` khi finding là về một thứ đáng lẽ phải có mà không có)
- `ai_xac_nhan` — người/vai có quyền công nhận, hoặc `(chưa nêu)`
