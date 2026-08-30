# Lens — Tính chính đáng của vấn đề (BABOK: Strategy Analysis · Root Cause Analysis)

**Mục tiêu:** kiểm xem tài liệu có đang giải **đúng bài** không — trước khi ai quan tâm nó giải hay đến đâu. Một tài liệu yêu cầu hoàn hảo cho một vấn đề sai vẫn là thất bại, và đó là thất bại của vai BA chứ không phải của người triển khai.

Lens này **không** xét chất lượng từng yêu cầu (việc của `ba-requirements-quality`), **không** xét truy vết (việc của `ba-traceability`).

## Stance

Đọc như một người sắp phải bỏ tiền cho việc này và chưa tin nó đáng làm. Kết quả rỗng là hợp lệ, nhưng chỉ khi cả sáu phép kiểm dưới đây đều qua.

## Các phép kiểm

### 1. Vấn đề là nguyên nhân gốc hay triệu chứng

Áp *5 Whys* lên câu phát biểu vấn đề. Nếu hỏi "vì sao điều này xảy ra" thêm một lần nữa mà ra một câu **cụ thể hơn và vẫn nằm trong tầm kiểm soát**, thì tài liệu đang dừng ở triệu chứng.

Dấu hiệu triệu chứng: phát biểu vấn đề mô tả *hiện tượng quan sát được* mà không nêu *cơ chế sinh ra nó*.

### 2. Nhu cầu tách khỏi giải pháp

Tài liệu có phân biệt rõ **cái người yêu cầu xin** với **cái họ thật sự cần** không? Nếu phát biểu nhu cầu chỉ là bản diễn đạt lại của giải pháp được xin (động từ + đối tượng), thì bước tách chưa xảy ra.

Kiểm ngược: bỏ giải pháp đề xuất đi, phát biểu nhu cầu còn đứng được không?

### 3. Đã xét phương án "không làm gì"

BABOK xếp đây vào Strategy Analysis và ghi nhận nó là mục hay bị bỏ nhất. Tài liệu có nói **cái giá của việc không làm** không, và cái giá đó có được ước lượng bằng thứ quan sát được không?

Thiếu mục này thì mọi kế hoạch đều "đáng làm" một cách mặc định.

### 4. Bên liên quan — ai bị bỏ sót

Liệt kê các bên chịu ảnh hưởng. Ba nhóm hay bị quên: **người vận hành** thứ sẽ được xây, **người kế thừa** nó sau khi tác giả rời đi, và **người chịu hậu quả gián tiếp** khi nó hỏng.

### 5. Ai xác nhận vấn đề này là đúng

Tài liệu có nêu ai xác nhận không? Tác giả tự phát biểu vấn đề rồi tự xác nhận là một finding.

**Trừ khi tài liệu đã tự nhận điều đó.** Ở dự án một tác giả, "người xác nhận khác người viết" không tồn tại, và báo đi báo lại mỗi lượt chỉ tạo tiếng ồn nền. Khi tài liệu **nêu thẳng** rằng chưa có người xác nhận độc lập và ghi mốc sẽ có, phép này qua. Khi tài liệu **im lặng** về chuyện đó — vẫn là finding, vì im lặng đọc như đã có người duyệt.

### 6. Bằng chứng cho phát biểu vấn đề

Mỗi khẳng định về hiện trạng phải truy về: dữ liệu đo được · tài liệu/chính sách viết ra · hoặc lời của người có quyền quyết. Trực giác và "ai cũng biết" không tính.

Chỉ ra cụ thể khẳng định nào đang không có nguồn.

## Đầu ra

Canonical fields (`location`, `trigger_condition`, `guard_snippet`, `potential_consequence`), thêm:

- `babok_area` — knowledge area liên quan (ví dụ `Strategy Analysis`)
- `neu_sai_thi` — điều gì đổ theo nếu finding này đúng: một yêu cầu, cả nhóm yêu cầu, hay toàn bộ kế hoạch

Không xếp hạng, không gán mức nghiêm trọng.
