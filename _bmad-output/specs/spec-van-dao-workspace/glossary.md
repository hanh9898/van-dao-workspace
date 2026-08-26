# Thuật ngữ — Vấn Đạo

## Thế giới quan

| Từ | Nghĩa |
|---|---|
| **Bí kíp** | Một quyển sách nhiều chương, đã đưa vào kho riêng của người học |
| **Tàn quyển** | Bài lẻ (một bài web, một chương rời) — không có lộ trình |
| **Công pháp** | Bí kíp theo nghề/vai cụ thể — học được là dùng ngay |
| **Tâm pháp** | Bí kíp theo năng lực nền — chậm hơn, nhưng dùng được ở mọi vai |
| **Mạch** | Một trục năng lực xuyên nhiều bí kíp (ví dụ: tư duy phân tích) |
| **Cảnh giới** | Năm bậc năng lực trên một mạch, theo mô hình Dreyfus |
| **Chương / Quyển / Mạch** | Ba tầng đột phá — đột phá chương (qua một ý), đột phá quyển (qua khảo thí), đột phá cảnh giới (lên bậc trên mạch) |
| **Lộ đồ** | Kế hoạch học cả quyển, người học duyệt trước khi bắt đầu |
| **Giáo án** | Kế hoạch dạy một chương, do Thư linh soạn trước khi dạy |
| **Khảo thí** | Bài kiểm tra cuối quyển — điều kiện đột phá quyển |
| **Đạo tâm** | Sổ nhật ký con đường học của người học |
| **Tâm ma** | Cách làm cũ người học mang sẵn vào, có thể bẻ cong thứ học sau |
| **Xuất quan** | Bỏ học giữa chừng — tạm dừng hợp lệ, không phải kết thúc |
| **Chú giải** | Lớp ghi chú người học bồi thêm lên bí kíp gốc (bí kíp gốc không đổi) |
| **Cờ bất đồng** | Bản ghi khi hai AI chấm độc lập không khớp kết quả — không chặn người học, nhưng được lưu lại để xem xét |
| **Tám vai** | Trưởng môn (giữ bản đồ, chỉ đường) · Tàng kinh trưởng lão (giám định, thu sách) · Thư linh (dạy, hỏi ngược) · Giám khảo (ra đề, coi thi) · Sơn phong trưởng lão (định cảnh giới) · Nghiệm Công Sứ (chấm theo tiêu chí) · Phúc Khảo Sứ (soát độc lập ở khảo thí) · Chú Giải Sứ (bồi chú giải) |

## Kỹ thuật

| Từ | Nghĩa | Vì sao cần |
|---|---|---|
| **Subagent tươi / Fork** | Vai chấm chạy trên ngữ cảnh sạch, không kế thừa hội thoại vai dạy; **fork** (kế thừa hội thoại) bị cấm dùng cho việc chấm | Cơ chế đứng sau CAP-4 — "một AI khác, tách biệt, kiểm tra" |
| **Nhãn vs dấu hiệu** | *Nhãn* là bậc cảnh giới (cần đủ bằng chứng); *dấu hiệu* là điều quan sát được, nói ngay được | Nền cho CAP-6: không công bố bậc khi κ thấp — chỉ nêu dấu hiệu |
| **κ (kappa)** | Mức khớp giữa nhãn người chấm và bậc model khi hiệu chuẩn | Ngưỡng κ < 0,6 → không công bố bậc (CAP-6) |
| **Ca đối chứng** | Chạy hai lần, một lần cố tình thêm ngữ cảnh bị cấm, để chứng minh ràng buộc "không đọc X" thật sự có tác dụng | Cách kiểm "chấm độc lập" không chỉ là lời nói |
| **Tiêu chí không phân biệt** | Tiêu chí mà người chưa đọc chương cũng đạt — vô dụng dù chấm khớp | Điều kiện để "chấm có căn cứ" có nghĩa |
| **Trigger eval / Behavioral eval** | Kiểm skill có được gọi đúng lúc, và có chạy ra đúng kết quả | Quality-gate cho mọi skill trong spec này |
| **Supportive Information** | Thành phần thứ hai của mô hình 4C/ID (van Merriënboer & Kirschner, *Ten Steps to Complex Learning*, 3rd ed., Routledge 2018) — thông tin hỗ trợ (mental model, cách khái niệm liên hệ) trình bày TRƯỚC learning task, sẵn có suốt luyện tập | Căn cứ cho CAP-3 (FR1a) — tóm lược mở đầu chương trước khi hỏi ngược từng ý |

Phần thuần cơ chế xây dựng (harness, compaction, context rot, `pham_vi_doc`, `.pham-vi.json`, điểm neo, chỉ ghi thêm, Loại 1·2·3) nằm ở companion `docs/VAN-DAO-dac-ta-v1.0.md` §0.2 và `ARCHITECTURE-SPINE.md` — không lặp lại ở đây.
