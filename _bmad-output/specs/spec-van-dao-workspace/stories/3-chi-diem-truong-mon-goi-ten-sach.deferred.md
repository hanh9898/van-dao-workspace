# Hồ sơ hoãn — Story 1.3 (Chỉ điểm)

File đồng hành của `3-chi-diem-truong-mon-goi-ten-sach.md`. Tách ra khỏi frontmatter story vì đây là
**hồ sơ quyết định**, không phải **chỉ dẫn thi công** — agent implement không cần đọc để làm đúng.
Người cần đọc: ai lên kế hoạch vòng sau, hoặc ai quay lại hỏi "vì sao chỗ này làm dở dang".

Mỗi mục bắt buộc có `revisit_when`. Hoãn mà không ghi mốc thì không phải hoãn, là quên.

---

## 1. Hành vi nhắc của `dang_treo` chưa chạy — `[medium]`

**Việc hoãn:** trạng thái `dang_treo` ghi được, nhưng hành vi định nghĩa của nó ("nhắc một câu ở phiên
sau") không chạy ở bản này.

**Vì sao:** cơ chế nhắc là hook `SessionStart` (`hooks/nap-ho-so.sh`, thành phần 17, §16 Vòng 3 bước
17) — không phải việc của skill `truong-mon`, vì skill chỉ chạy khi người học tự gõ lệnh nên không có
mặt ở đầu phiên để nhắc. Hook chưa tồn tại: `van-dao/hooks/` hiện chỉ có `.gitkeep`. AD-7 cho phép
hook này (SessionStart là ranh giới lifecycle thật, không phải tool-call giả).

**Phần đã làm được ngay ở story này:** nhắc `dang_treo` tại chỗ khi người học tự gọi
`/van-dao:truong-mon`, làm chốt xác nhận trước khi lô cũ chuyển `het_hieu_luc`.

**Xem lại khi:** ngay sau khi Epic 2 hoàn tất — lộ đồ tồn tại thì `nap-ho-so.sh` có 2/3 payload (hồ sơ
từ Story 1.2 + lộ đồ từ Epic 2; còn thiếu bản đồ/`ban-do.py`), đủ lý do dựng thật.

**Vị trí:** `van-dao/hooks/nap-ho-so.sh`

---

## 2. Tên `truong-mon` chỉ hai phạm vi khác nhau — `[low]`

**Việc hoãn:** §16 và `epics.md` chưa trỏ về nhau, người đọc sau dễ tưởng bước 14 đã xong.

**Vì sao:** §16 Vòng 3 bước 14 ghi "skill `truong-mon` — chỉ điểm, xếp lớp", đi kèm `mach.schema.md`
(bản đầy đủ, nhiều mạch). Story 1.3 ở Epic 1 giao bản mồi lửa (một mạch, kho rỗng, không xếp lớp).
Đã ghi rõ trong Design Notes của story, nhưng hai tài liệu vẫn im lặng về nhau.

**Xem lại khi:** bắt đầu bước 14 (§16 Vòng 3) — đối chiếu phần đã giao ở Story 1.3 trước khi làm tiếp;
hoặc sớm hơn nếu có người thứ hai đọc vào bộ tài liệu này.

---

## 3. Bảng §10.3 có phạm vi hẹp hơn kết luận rút ra từ nó — `[medium]`

**Việc hoãn:** bảng nói về mức chắc chắn của phần **gợi ý tâm pháp**, nhưng câu rào rút ra lại áp cho
cả danh sách; mức chắc chắn của phần **công pháp** không có nguồn nào định nghĩa.

**Vì sao:** tiêu đề bảng là "công pháp nào cần tâm pháp gì" (3 dòng: có số liệu / có khai từ bí kíp /
suy đoán). Nhưng §10.3 kết luận "câu rào là một bước bắt buộc trong luồng chỉ điểm" và câu mẫu nói
"những gì nói sau đây là suy đoán" — bao cả danh sách công pháp. Ở n=1 kho rỗng cả hai phần đều suy
đoán nên chưa cắn; cắn khi dòng hai bật (kho có bí kíp khai tâm pháp): phần tâm pháp lên "kèm nguồn",
phần công pháp không rõ có lên theo không.

**Xem lại khi:** dòng hai của bảng §10.3 sắp bật lần đầu — tức khi kho đã có bí kíp khai tâm pháp.
Trước đó chưa cắn, và sửa đặc tả lúc chưa ai chạm tới dòng hai là sửa mù.

**Vị trí:** `docs/VAN-DAO-dac-ta-v1.0.md` §10.3

---

## 4. Câu rào không nhích theo kho — `[low]`

**Việc hoãn:** người học không thấy hệ đang lớn lên; tới một hôm câu rào biến mất mà không ai giải
thích vì sao.

**Vì sao:** phần còn lại cần **đếm kho** và biết quyển nào khai tâm pháp gì — đọc kho là vùng của Tàng
kinh trưởng lão, Trưởng môn chạm vào là vi phạm AD-3. Đặc tả đưa câu rào sau dấu trích dẫn (ví dụ),
không phải chuỗi cố định, nên nới lời văn để mang tin thật là hợp lệ — chỉ thiếu đường lấy dữ liệu.

**Phần đã làm được ngay ở story này:** nói đúng trạng thái kho rỗng ("kho chưa có quyển nào") thay vì
công thức chung chung, đặt sẵn khuôn câu rào là thứ đo được chứ không phải câu than nghi thức.

**Xem lại khi:** cùng mốc với mục 3 (dòng hai §10.3 sắp bật) — hai việc chung một gốc, gỡ cùng lượt.
