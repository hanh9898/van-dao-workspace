# Phạm vi MVP và thứ tự dựng — Vấn Đạo

**Milestone MVP: "đột phá quyển đầu tiên"** (đặc tả §16 bước 13, cuối Vòng 2) — không dừng ở bước 8 (tự bế quan). Dừng ở bước 8 mới có Dạy chạy được, chưa có Soát — mà Soát độc lập chính là khác biệt cốt lõi của sản phẩm (xem SPEC.md § Why). MVP phải khép được vòng Dạy→Soát, không chỉ dạy được.

**Hai điều cần đọc trước bảng:**
- **"Vòng" (đặc tả §16 — chuỗi phụ thuộc kỹ thuật) khác "Bậc" (đặc tả §13.1 — độ hoàn thiện tính năng).** Một thành phần "Bậc 1" vẫn có thể nằm ở "Vòng 2" nếu nó phụ thuộc kỹ thuật vào bước dựng sau. Bảng dưới xếp theo Vòng — đây là trục đúng cho câu hỏi "dựng được lúc nào". Nhãn Bậc từng lệch với Vòng một lần (trường hợp `phuc-khao`), nên không dùng Bậc để cắt MVP.
- **Vòng là chuỗi phụ thuộc, không phải mốc thời gian.** MVP = Vòng 1+2 không phải cam kết "xong trong X tuần".

## Có trong MVP (Vòng 1-2, bước 1-13)

| Capability | Bước §16 | Ghi chú |
|---|---|---|
| CAP-1 (Thu bí kíp) | 3 | |
| CAP-2, CAP-3 phần lộ đồ/giáo án/hỏi ngược/đối chất | 5 (F-1→F2) | Gồm FR1a (tóm lược mở đầu chương — 4C/ID Supportive Information) trước khi hỏi ngược từng ý |
| CAP-3 phần giàn giáo co giãn/mastery gate | 5 + 11 (F3-F5′) | Phần chẩn đoán/giảng lại khi vấp thuộc bước 11 (Vòng 2) — chỉ trọn vẹn từ cuối Vòng 2 |
| CAP-4 (Soát — tách vai, bằng chứng, Giám khảo tách chấm, trực giao, cờ bất đồng) | 6, 10, 12, 13 | Cờ bất đồng: chỉ có kênh đạo tâm; chưa có màn "tiến độ" |
| CAP-7 (Đạo tâm tự ghi) | 7 | |
| CAP-8 (Nghi thức) | 3-4, 7 | Chỉ bái sư + thu bí kíp; đột phá cảnh giới chưa dùng được ở MVP |
| CAP-14 (Trả lời rõ khi thiếu cơ chế) | — | Không chặn bởi bước nào cụ thể; cần ngay từ MVP để `/vd:chi-duong` không im lặng/đoán liều với ý định thuộc Vòng 3-4 |
| CAP-15 (Không khen sáo rỗng) | — | Xuyên suốt, cần ngay từ MVP |

## Để Vòng 3 (nhiều quyển, nhiều mạch — bước 14-19)

| Capability | Bước §16 | Vì sao chưa vào MVP |
|---|---|---|
| CAP-5 (Định hướng) | 14 | Gợi ý "học gì tiếp" vô nghĩa khi kho chỉ có một quyển |
| CAP-9 (Hạ sơn/phục mệnh) | 16 | Cơ chế cho nhiều mạch, chưa cần khi mới có một quyển |
| CAP-10 phần nhắc lại/hệ thống hoá | 18 | F6/F7 trong thu-linh, chặn bởi bước 8 |
| CAP-10 phần nối lại mạch cũ/xuất quan | 18 | **Đánh đổi có ý thức, không phải thiếu sót:** F8/F9 hoãn tới Vòng 3 vì n=1 là ràng buộc thật (SPEC.md Assumptions) — core loop Dạy→Soát chưa chứng minh với chính tác giả thì chưa đầu tư retention cho người dùng thứ hai chưa tồn tại; AD-2 đã đảm bảo dữ liệu quay lại không mất, chỉ chưa có luồng "hỏi 1-2 câu mở đầu lại" thiết kế riêng. **Xem lại khi:** có người dùng thứ hai thật muốn dùng liên tục nhiều phiên, hoặc chính tác giả tự thấy khó chịu vì quay lại chương dở mà hệ im lặng — khi đó kéo F8/F9 lên đầu Epic 10 thay vì cuối Vòng 3. |
| CAP-12 (quét kho gợi sách) | 15 | Vô nghĩa khi kho chỉ có một quyển |
| CAP-13 (bản đồ trực quan) | 17 | Ở MVP chỉ có đạo tâm dạng text, chưa có bản đồ |

## Để Vòng 4 (đo và tự sửa — bước 20-25)

| Capability | Bước §16 | Vì sao chưa vào MVP |
|---|---|---|
| CAP-6 (Đo cảnh giới + hiệu chuẩn) | 20-21, 25 | Cần ≥2 nguồn — không dựng có nghĩa với một quyển; hiệu chuẩn cần đủ mẫu phủ nhiều mạch |
| CAP-11 (Chú Giải Sứ) | 23 | Chặn bởi bước 18 (CAP-10) — xa MVP hơn cả Định hướng/Đo |

Thứ tự dựng chi tiết (từng bước F-1 đến F10, script/hook/subagent cụ thể) nằm ở companion `ARCHITECTURE-SPINE.md` (Capability → Architecture Map) và đặc tả §16 gốc.
