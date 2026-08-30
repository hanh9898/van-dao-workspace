# Lens — Truy vết (BABOK: Requirements Life Cycle Management · Trace Requirements)

**Mục tiêu:** kiểm chuỗi liên kết **vấn đề → nhu cầu → yêu cầu → giải pháp → kế hoạch → tiêu chí nghiệm thu** có liền mạch hai chiều không. Lens này không xét chất lượng nội dung từng mắt xích — nó chỉ tìm **mắt xích đứt** và **mắt xích thừa**.

## Stance

Đọc như người kiểm toán: đi từ mỗi đầu của chuỗi, lần theo, và ghi lại chỗ nào không lần được.

Đây là lens cơ học. Nó không cần hiểu lĩnh vực; nó cần đọc kỹ và không bỏ sót.

## Bốn phép lần

### 1. Xuôi — từ nhu cầu xuống

Mỗi nhu cầu phát biểu ở phần đầu có ít nhất một yêu cầu phục vụ nó không?

**Nhu cầu mồ côi**: được nêu ra, được nhấn mạnh, rồi không có yêu cầu nào thực hiện. Đây là kiểu hỏng êm nhất — tài liệu đọc rất thuyết phục mà phần thi hành lại bỏ qua đúng điều thuyết phục nhất.

### 2. Ngược — từ yêu cầu lên

Mỗi yêu cầu truy về được một nhu cầu cụ thể không?

**Yêu cầu mồ côi**: có ID, có cách kiểm, nhưng không phục vụ nhu cầu nào đã nêu. Thường là thứ tác giả thấy hay nên thêm vào — và nó làm phạm vi phình mà không ai nhận ra.

### 3. Xuôi tiếp — từ yêu cầu xuống kế hoạch

Mỗi yêu cầu có ít nhất một việc trong kế hoạch thực hiện nó không? Và ngược lại: mỗi việc trong kế hoạch phục vụ yêu cầu nào?

**Việc mồ côi trong kế hoạch** là dấu hiệu phạm vi đã phình sau khi danh sách yêu cầu được chốt.

### 4. Đối chiếu ranh giới

Mục "ngoài phạm vi" có mâu thuẫn với bất kỳ yêu cầu hay việc nào không? Một thứ bị tuyên bố ngoài phạm vi mà vẫn xuất hiện trong kế hoạch là mâu thuẫn phải báo.

## Ba chỗ đứt hay gặp

- **Tiêu chí thành công ở đầu tài liệu không nối được xuống bất kỳ yêu cầu nào** — nó thành khẩu hiệu.
- **Rủi ro nêu ra không có việc nào trong kế hoạch ứng phó**, dù mục rủi ro có cột "ứng phó".
- **Kế hoạch có thứ tự ưu tiên, nhưng thứ tự đó không suy ra được từ yêu cầu nào** — tức ưu tiên do cảm tính.

## Đầu ra

Canonical fields, thêm:

- `mat_xich` — cặp bị đứt, viết dạng `<nguồn> → <đích>` (ví dụ `TC-2 → (không có yêu cầu nào)`)
- `huong` — `xuôi` (nhu cầu→yêu cầu) · `ngược` (yêu cầu→nhu cầu) · `kế hoạch` (phép lần 3, cả hai chiều giữa yêu cầu và kế hoạch) · `ranh giới`

Kết quả rỗng hợp lệ khi cả bốn phép lần đều liền mạch — nhưng con số **đã lần bao nhiêu mắt xích** phải xuất hiện, và chỗ của nó là dòng tổng kết của lens trong báo cáo markdown, **không phải** trong mảng finding: mảng rỗng thì không đựng được gì.

Không có con số đó thì "lens chạy và sạch" trông y hệt "lens không chạy".
