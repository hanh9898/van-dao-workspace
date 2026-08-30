# Harness viết skill cho Vấn Đạo — phân tích hiện trạng, vấn đề, và kế hoạch

**Trạng thái:** bản phân tích, chưa phải quy chuẩn đã chốt
**Ngày:** 2026-08-30
**Phạm vi:** cách viết và kiểm skill trong `van-dao/skills/**`, và cơ chế của workspace bảo đảm việc đó

Tài liệu này là **đầu vào** cho hai thứ: một quyết định kiến trúc về ngân sách ngữ cảnh, và một bộ luật kiểm được mà agent tuân theo. Bản thân nó không phải luật — xem §7 để biết vì sao phân biệt này quan trọng.

---

## 1 · Vấn đề

**Hiện tượng quan sát được:**

> Skill của Vấn Đạo **hỏng âm thầm** khi chạy thật: chúng vẫn được gọi, vẫn trả lời trôi chảy, nhưng một phần chỉ dẫn đã biến mất khỏi ngữ cảnh — và không có gì báo cho ai biết.

**Nguyên nhân gốc:**

> **Người viết skill không có cách nào biết mình đang viết sai, tại thời điểm viết.** Cơ chế cắt cụt (§2, M3) vô hình; ngưỡng an toàn không hiển thị ở đâu; và phép kiểm duy nhất — lens `skill-quality` — chỉ chạy khi có người nhớ gọi, tức sau khi skill đã viết xong.

Hiện tượng là bằng chứng; nguyên nhân gốc là thứ các tiêu chí dưới đây đo. Sửa hiện tượng mà không chạm nguyên nhân thì skill thứ năm lặp lại y hệt.

Tiêu chí thành công, đo được:

| # | Tiêu chí | Cách đo | Ai xác nhận | Đo khi nào |
|---|---|---|---|---|
| TC-1 | Không skill nào mất nội dung sau khi ngữ cảnh bị nén | Đo token mỗi `SKILL.md`; phần vượt ngưỡng phải là phần mất đi không đổi hành vi | **CI** — đỏ hay xanh, không ai phán | Mỗi lần CI chạy |
| TC-2 | Lỗi thuộc loại đã biết bị bắt **trước** khi skill được dùng | Phép kiểm chạy được, không phụ thuộc ai nhớ chạy | **CI** | Mỗi lần CI chạy |
| TC-3 | Skill tiếp theo **không lặp lại lỗi thuộc các loại đã biết** | Đọc finding của vòng review skill đó: không finding nào rơi vào sáu loại ở bảng dưới | Chủ repo, đọc và phán | Tại bước đóng story của **skill thứ năm** |

Thời điểm đo gắn vào **sự kiện**, không vào lịch — dự án này chạy theo story chứ không theo tháng, nên một mốc lịch sẽ rơi vào lúc chưa có gì để đo.

**Sáu loại lỗi đã biết** — rút từ lỗi thật đã xảy ra, không phải danh sách lý thuyết:

1. Vượt ngân sách ngữ cảnh (Story 1.4: 7.967 token, vượt 60%)
2. Lời dặn đặt thay cho cơ chế (`**tuyệt đối không in text**` không ngăn được gì)
3. Lệnh bảo người dùng gõ mà chưa ai gõ thử (`pip install` hỏng trên Windows)
4. `description` mô tả chức năng thay vì điều kiện kích hoạt
5. Lược đồ dữ liệu hoặc luật ghi rơi xuống sau mốc cắt (`truong-mon`)
6. Mâu thuẫn số nội bộ giữa các mục trong cùng một tài liệu

**Khi nào tuyên bố thất bại và quay lại:** nếu skill thứ năm **vẫn lặp ≥ 2 trong sáu loại lỗi trên** dù toàn bộ cơ chế đã dựng xong, thì cơ chế không hiệu quả — dừng lại và xét lại cách tiếp cận, đừng bồi thêm tầng. Cùng thước với TC-3 nên không phải đo thêm gì.

> TC-3 đo **chất**, không đo lượng. Đếm tổng finding thì phụ thuộc chạy bao nhiêu lens và người review kỹ đến đâu — hai skill khác nhau sẽ không so được cùng thước. Còn "có lặp lại lỗi cũ không" đo đúng thứ cần biết: **cơ chế vừa dựng có chặn được lỗi cũ hay không.**

---

## 2 · Cơ chế nền tảng — sự thật quyết định mọi thứ còn lại

Đo và trích từ tài liệu chính thức của Claude Code, không phải suy đoán.

| | Cơ chế | Hệ quả |
|---|---|---|
| **M1** | `description` **luôn** nằm trong ngữ cảnh; thân `SKILL.md` chỉ nạp khi skill được gọi | `description` là nút thắt duy nhất luôn tốn chỗ → nó phải là *điều kiện kích hoạt*, không phải bản tóm tắt |
| **M2** | Nạp rồi thì *"stays in context across turns"* | "Ít khi gọi" **không** đồng nghĩa "rẻ". Gọi một lần là trả suốt phiên |
| **M3** | Sau nén ngữ cảnh, mỗi skill được gắn lại **5.000 token đầu tiên** | Phần đuôi biến mất. **Thứ tự trong file là thiết kế, không phải thẩm mỹ** |
| **M4** | Tổng mọi skill được gắn lại chia chung **25.000 token**; skill gọi sớm bị **bỏ hẳn** nếu vượt | Một phiên chạm quá ~5 vai thì vai đầu chuỗi rơi khỏi ngữ cảnh hoàn toàn |
| **M5** | Văn bản trong skill là *gợi ý xác suất*, không phải lệnh được thực thi | Ràng buộc chỉ thành thật khi nằm **ngoài** model: script, mã thoát, schema, permission |

M3 và M4 là hai cơ chế chưa từng được tính đến khi bốn skill hiện tại được viết.

---

## 3 · Hiện trạng, đo trực tiếp

### 3.1 Bốn skill của Vấn Đạo

Đo bằng `tiktoken/cl100k_base`. Đây là tokenizer của một nhà cung cấp khác, nên con số là **xấp xỉ** — kết luận chỉ chắc chắn với skill vượt ngưỡng nhiều.

| Skill | Token | Mất sau khi nén | Phần mất là gì | Mức chắc chắn |
|---|---|---|---|---|
| `truong-mon` | 7.334 | **2.334** | Gần nửa Nhánh C (nhánh chính) · toàn bộ "Tra lại theo tên cũ" · toàn bộ **"Định dạng file"** — lược đồ `chi-diem.jsonl`, luật sinh `id`, giá trị hợp lệ | **Chắc** (vượt 47%) |
| `nhap-mon` | 6.018 | **1.018** | Gần trọn Bước 5 · toàn bộ **Bước 6 — Xác nhận bái sư** | Nhiều khả năng (vượt 20%) |
| `thu-bi-kip` | 5.054 | 54 | Đuôi Nhánh G | **Không kết luận được** (vượt 1%, nằm trong sai số tokenizer) |
| `nhap-mon-ky` | 2.397 | 0 | — | An toàn |

`truong-mon` là ca hỏng rõ nhất: sau khi nén, nó vẫn được gọi để ghi `chi-diem.jsonl` mà **không còn lược đồ nào để ghi theo**.

### 3.2 Đối chiếu với hai bộ skill trưởng thành

Đo cùng thước, trên mã nguồn tải về, không đọc qua tóm tắt.

| | Số skill | `SKILL.md` trung bình | Nội dung nằm ngoài `SKILL.md` |
|---|---|---|---|
| BMAD (loại các shim đã ngừng dùng) | 29 | 1.737 token | **68%** |
| Superpowers | 14 | 2.290 token | 50% |
| **Vấn Đạo** | 4 | **5.201 token** | **6%** |

Khác biệt không nằm ở "họ viết ngắn hơn" — mà ở **họ để phần lớn nội dung ngoài đường nạp mặc định**. Vấn Đạo đang để 94% nội dung nằm trong file luôn được nạp trọn.

Một quan sát đáng ghi vì nó định cỡ kỳ vọng: cả hai bộ trên đều **không đạt** ngưỡng kích thước mà tài liệu của chính họ đặt ra. Giữ skill nhỏ là việc khó đến mức người viết ra quy tắc cũng không giữ nổi bằng kỷ luật — đó là lý do §6 chọn cơ chế thay vì lời khuyên.

### 3.3 Bằng chứng rằng viết tài liệu là chưa đủ

Đây là dữ kiện quan trọng nhất của tài liệu này, vì nó nói về chính tài liệu này.

- **AD-8 đã tồn tại** trong `ARCHITECTURE-SPINE.md` từ trước, có ghi ngân sách token. Story 1.4 vẫn viết ra một `SKILL.md` **7.967 token**, vượt 60%.
- Người viết story đó (tác nhân AI, có đọc AD-8) còn **ước token bằng cách chia số ký tự** — sai 40% — rồi kết luận "đạt". Nguyên nhân: **tiếng Việt có dấu tốn token gấp 2,06 lần tiếng Anh trên cùng một lượng ký tự** (đo trên chính các file của ba dự án: van-dao 2,11 ký tự/token · BMAD 4,40 · Superpowers 4,30). Mọi trực giác về độ dài rút từ tài liệu tiếng Anh đều lệch khoảng đó.
- Lỗi chỉ bị bắt khi lens `skill-quality` chạy, tức **sau khi skill đã viết xong**.
- Trong cùng story, câu `**tuyệt đối không in khoá text**` viết in đậm **không ngăn được gì**; ràng buộc chỉ thành thật khi được bọc vào `bin/giam-dinh.py` — nội dung sách không còn đường ra khỏi script.

Kết luận rút từ đây, và nó áp lên chính bản thân tài liệu này: **một quy tắc không có cách kiểm thì không khác gì một lời khuyên**.

---

## 4 · Nhu cầu thật, tách khỏi giải pháp

**Được yêu cầu (nguyên văn):** *"viết 1 tài liệu chuẩn mực viết skill… phân tích hiện trạng và làm rõ các vấn đề cần giải quyết rồi lên kế hoạch"*

**Nhu cầu phía sau:** làm cho **viết skill sai trở nên khó hơn viết đúng**, để người viết skill tiếp theo không phải lặp lại 28 lỗi của Story 1.4, và để người học không nhận hành vi sai từ một skill đã mất nửa chỉ dẫn.

Bốn câu kiểm nhu cầu:

| Câu | Trả lời, có bằng chứng |
|---|---|
| **Ai đau** | Người viết skill tiếp theo · và người học, vì skill hỏng âm thầm thì họ là người nhận hậu quả |
| **Đau lúc nào** | Lúc viết (28 finding phải vá sau khi xong) · và lúc chạy thật (`truong-mon` mất lược đồ sau khi nén) |
| **Hiện sống với nó thế nào** | Viết theo trực giác rồi chạy review thủ công để bắt lỗi — tức **phát hiện muộn**, và chỉ khi có ai nhớ chạy |
| **Cái gì làm bài này biến mất** | Không phải "có tài liệu". Mà là: **lỗi loại đã biết bị chặn tự động, sớm** |

Các bên liên quan, và kỳ vọng khác nhau của họ:

| Bên | Cần gì từ việc này |
|---|---|
| **Người viết skill tiếp theo** (tác giả, hoặc chính tác giả sáu tháng sau) | Biết mình sai **lúc đang viết**, không phải lúc review |
| **Người học** | Không nhận hành vi sai từ một skill đã mất nửa chỉ dẫn — họ không có cách nào biết điều đó đang xảy ra |
| **Người ngoài đóng góp** (repo public) | Quy tắc đọc được mà **không cần biết** §12.4, AD-3 hay bất kỳ định danh nội bộ nào của Vấn Đạo |
| **Người vận hành phép kiểm tự động** | Phép kiểm không chặn nhầm việc đúng — một CI đỏ sai vài lần là bị tắt |
| **Người kế thừa repo** | Hiểu được vì sao mỗi ràng buộc tồn tại, để biết cái nào còn đúng khi hoàn cảnh đổi |

**Ai xác nhận vấn đề này đúng:** hiện tại chưa có ai ngoài tác giả — đây là khoảng hở đã biết, chưa xử lý.

> Tài liệu là **cần**, nhưng nó không phải thứ giải quyết vấn đề. Nó là đầu vào để sinh ra thứ giải quyết: một quyết định kiến trúc, một bộ luật kiểm được, và vài phép kiểm chạy được.

### 4.1 · Cái giá của việc không làm gì

Đây là phương án mặc định nếu không ai làm gì cả, và nó phải được ước để mọi phương án khác có mốc so sánh.

| Khoản | Ước, dựa trên số đã đo |
|---|---|
| Lỗi phải vá cho mỗi skill mới | Story 1.4 sinh **28 finding** ở vòng review, trong đó **7** đòi đổi hành vi thật (viết thêm một script, dựng 11 test, chạy lại toàn bộ eval) |
| Số skill còn lại | Đặc tả dự kiến ~10 skill; đã có 4 → còn **~6** |
| Chi phí lặp lại | ~6 lần lặp lại cùng loại lỗi, mỗi lần tốn một vòng review đầy đủ cộng công vá |
| Hỏng khi chạy thật | **2 skill đang hỏng** (`truong-mon`, `nhap-mon`) mà không có gì báo. Số này chỉ tăng, vì mỗi skill mới viết theo cùng thói quen |
| Chi phí phát hiện | Mỗi lỗi bị bắt ở vòng review đắt hơn nhiều lần so với bị bắt lúc viết — và một số không bao giờ được bắt, vì review chỉ chạy khi có người nhớ gọi |

Con số đáng chú ý: **không phải chi phí lớn nhất là công vá, mà là hai skill đang hỏng âm thầm ngay lúc này**. Chúng không tự lộ ra, và người chịu là người học.

---

## 5 · Yêu cầu

Mỗi yêu cầu ghim đủ năm chỗ: **ID · điều phải đạt · actor (ai thi hành) · ưu tiên · cách kiểm pass/fail**. Yêu cầu nào không kiểm được thì không nằm ở đây.

Ưu tiên theo MoSCoW: **P** = phải có (bỏ thì mục tiêu §1 không đạt) · **N** = nên có · **T** = có thì tốt.

### Nhóm A — Ngân sách ngữ cảnh

| ID | Yêu cầu | Actor | Ưu tiên | Kiểm pass/fail |
|---|---|---|---|---|
| **A1** | Mỗi `SKILL.md` ≤ **4.500 token** | CI | **P** | Đo bằng `tiktoken/cl100k_base`; > 4.500 là fail. Ngưỡng nền tảng là 5.000; 4.500 là **biên an toàn 10%** vì đo bằng tokenizer của nhà cung cấp khác |
| **A2** | Skill được miễn trừ A1 thì phần nằm sau mốc 4.500 chỉ chứa nội dung mà **việc mất đi không đổi hành vi** | Người viết → Reviewer | N | Người viết khai phần đó là gì và vì sao mất được; reviewer đối chiếu với eval của skill — nếu không có kịch bản eval nào chạm phần đó thì lời khai đứng vững |
| **A3** | Lược đồ dữ liệu, luật ghi file, ràng buộc an toàn nằm **trước** mốc 4.500 | CI | **P** | Đo vị trí tích luỹ của mục đó trong file. Skill đạt A1 thì tự thoả |
| **A4** | Tổng token của các skill **được gọi trong một session** không vượt **25.000** | CI (đo tĩnh) · Người viết (khi thiết kế luồng) | N | **Tĩnh:** cộng token mọi `SKILL.md` trong repo, so với 25.000 — chặt hơn thực tế nên chỉ cảnh báo. **Động, khi điều tra:** đếm skill invoke trong transcript phiên rồi cộng token của chúng |

> `session` ở đây là **session Claude Code** — đơn vị runtime, có ranh giới rõ và đo được từ transcript. Không phải "buổi học" của người học.
>
> Hai loại session có profile khác nhau và **chưa được tách**: session người học (chỉ gọi skill van-dao) và session phát triển (gọi thêm skill BMAD). Đo thật trên phiên viết tài liệu này: **16 skill khác nhau** được gọi — tức harness tự nó đang vượt trần.

### Nhóm B — Ranh giới lời dặn / cơ chế

| ID | Yêu cầu | Actor | Ưu tiên | Kiểm pass/fail |
|---|---|---|---|---|
| **B1** | Ràng buộc **phải đúng mọi lần** phải là script, mã thoát, hoặc schema — không phải văn xuôi | Người viết | **P** | Phép thử: *"nếu ai sửa skill vi phạm điều này, có gì bắt được không?"* Không có → fail. Một ràng buộc thuộc loại "phải đúng mọi lần" khi vi phạm nó làm hỏng dữ liệu, rò nội dung, hoặc ghi sang vùng của vai khác |
| **B2** | Mọi lệnh mà skill bảo người dùng gõ phải **đã được gõ thử thật** | Người viết | **P** | `evals.json` có bằng chứng chạy, hoặc có test tự động chạy đúng lệnh đó |
| **B3** | Phép kiểm đầu vào tất định nằm trong script | Người viết | N | Skill được phép **mô tả** script trả về gì và phân nhánh theo mã thoát; không được **thực hiện** từng phép kiểm bằng lời |

### Nhóm C — Kích hoạt

| ID | Yêu cầu | Actor | Ưu tiên | Kiểm pass/fail |
|---|---|---|---|---|
| **C1** | `description` phát biểu **khi nào dùng**, bằng câu người dùng thật sẽ nói | Người viết → Reviewer | **P** | Đọc câu đầu: mô tả *tình huống* hay *chức năng*? |
| **C2** | Bỏ lỡ kích hoạt gây hậu quả thật thì phải có đường vào tường minh | Người viết | N | "Hậu quả thật" = hỏng dữ liệu, rò nội dung, hoặc người học nhận thông tin sai. Chỉ chậm hoặc phiền thì không tính |

### Nhóm D — Bằng chứng

> **Eval đi theo AD-10 trong `ARCHITECTURE-SPINE.md`, không nhắc lại ở đây.** AD-10 đã quy định eval nhẹ chạy thật đi cùng lúc viết skill, và lệnh tái tạo chạy được cả Windows lẫn Linux. Chép lại vào đây tạo hai nguồn cho cùng một luật — đúng rủi ro §9 nêu.

| ID | Yêu cầu | Actor | Ưu tiên | Kiểm pass/fail |
|---|---|---|---|---|
| **D1** | Mỗi skill mới phải qua vòng review đủ lens trước khi đóng story; Spec Change Log ghi **số finding và loại của chúng** | Người viết | N | Đọc Spec Change Log: có số, có ghi lens nào chạy, và **có đối chiếu với sáu loại lỗi đã biết ở §1** chưa. Thiếu phần đối chiếu → fail, vì đó mới là thứ TC-3 cần |

---

## 6 · Giải pháp — bốn tầng, xếp theo sức cưỡng chế

Nguyên tắc chọn: **đặt mỗi yêu cầu vào tầng thấp nhất mà nó chặn được**. Tầng càng thấp càng khó lách, nhưng càng đắt để dựng và càng cứng khi muốn đổi.

| Tầng | Cơ chế | Chặn được gì | Giá |
|---|---|---|---|
| **1 · Mã** | Script trong `bin/`, mã thoát phân biệt ca | *(không chứa yêu cầu nào)* — đây là **hệ quả** của B1: khi lens phán một ràng buộc thuộc loại phải-đúng-mọi-lần, script là thứ được viết ra | Phải viết và test; thêm thành phần |
| **2 · Kiểm tự động** | Test trong `tests/` | A1, A3, **A4**, D2 — mọi thứ đếm được | Rẻ. Chỉ áp được cho thứ đo được bằng số. **Hiện chỉ chạy tay được** — xem cảnh báo dưới bảng |
| **3 · Kiểm có người gọi** | Lens `skill-quality` trong `bmad-review`; và quy ước ghi chép ở bước đóng story | A2, B1, B2, B3, C1, C2, **D1** — thứ cần phán đoán hoặc cần người ghi | Chỉ chạy khi có người nhớ chạy |
| **4 · Ràng buộc kiến trúc** | Một AD trong `ARCHITECTURE-SPINE.md` | **Nguyên tắc**, không phải yêu cầu cụ thể: ngân sách ngữ cảnh là tài nguyên dùng chung giữa mọi skill | Đắt để đổi; chỉ dùng cho thứ ổn định |

**Vì sao A4 không ở tầng 4 dù nó là tài nguyên chung:** nguyên tắc thì thuộc spine, nhưng **ngưỡng cụ thể và phép đo** thì không — chúng còn đổi khi ta đo lại bằng tokenizer chính thức, và spine là lớp đắt nhất để sửa. Spine giữ câu *"ngân sách ngữ cảnh là tài nguyên chung, mỗi skill phải khai phần của mình"*; con số 25.000 và cách đếm nằm ở tầng 2, sửa được rẻ khi hiểu biết đổi.

> **Tầng 2 chưa thật sự tự động.** Không repo nào có remote, nên CI chưa từng chạy — `van-dao/.github/workflows/kiem.yml` đã cấu hình nhưng chưa kích hoạt lần nào. Test viết ra vẫn chạy tay được và vẫn bắt lỗi thật, nhưng tính chất *"không phụ thuộc ai nhớ chạy"* — thứ khiến tầng 2 mạnh hơn tầng 3 — hiện **chưa có**. Cho tới khi có remote, tầng 2 trên thực tế hoạt động như tầng 3. Đã ghi mốc quay lại ở `deferred-work.md`.

**Cái gì *không* vào tầng 4:** cách tổ chức file, phong cách viết, thứ tự mục. Phép thử của spine là *"hai đơn vị xây độc lập có thể chọn khác nhau đến mức **không tương thích** không?"* — hai skill viết theo hai phong cách vẫn chạy được cùng nhau. Không đồng đều không phải không tương thích. Chỉ **ngân sách ngữ cảnh** là tài nguyên chung thật, nên chỉ nó là invariant.

---

## 7 · Kế hoạch triển khai

Xếp theo *chắc chắn có ích* giảm dần, không theo dễ làm. Cột **Cỡ** là ước thô để so tương đối, không phải cam kết thời gian: **S** = một lượt làm việc · **M** = vài lượt · **L** = đáng mở một story riêng.

**Phụ thuộc giữa các giai đoạn.** Phép đo token chạy được ngay, không phụ thuộc ngôn ngữ — nên về mặt kỹ thuật GĐ2 làm trước được. Nhưng **bật cổng chặn khi biết chắc nó sẽ đỏ là cách nhanh nhất để cổng đó bị tắt**: hai skill đang vượt ngưỡng, CI sẽ đỏ liên tục cho tới khi GĐ1 xong, và một CI đỏ kéo dài thì người ta học cách bỏ qua nó.

Nên thứ tự là: **dựng phép đo ở GĐ1** (chỉ để báo cáo con số, chưa chặn) → **chuyển ngôn ngữ** → rồi mới **bật chặn ở GĐ2**. GĐ3 và GĐ4 độc lập với nhau và với hai giai đoạn trên.

Nếu chỉ làm được một việc: **GĐ2**, vì nó là cơ chế duy nhất chặn tự động — nhưng phải làm sau GĐ1, hoặc bật ở chế độ cảnh báo trước rồi mới chuyển sang chặn.

### Giai đoạn 1 — Chuyển skill sang tiếng Anh · **L**

Việc này **thay thế** phương án "sắp xếp lại thứ tự trong từng skill". Lý do: tiếng Việt có dấu tốn token gấp **2,06 lần** tiếng Anh trên cùng lượng ký tự, nên chuyển ngôn ngữ đưa `truong-mon` 7.334 → ~3.560 và `nhap-mon` 6.018 → ~2.920 — cả hai về dưới ngưỡng, và việc sắp xếp thứ tự thành thừa.

| Việc | Cỡ | Yêu cầu phục vụ | Xong khi |
|---|---|---|---|
| Dựng test đo token trước, để có thước xác nhận | S | A1 | Test chạy được, hiện đúng con số hiện tại của cả bốn skill |
| Chuyển bốn `SKILL.md` sang tiếng Anh — **kể cả tên skill**. Giữ nguyên: câu thoại mẫu người học nghe, và thuật ngữ định danh trong dữ liệu | L | A1, A3 | Cả bốn < 4.500 token; **eval của từng skill chạy lại và pass** |
| Cập nhật mọi tham chiếu tới tên skill cũ: `evals.json`, tài liệu, lối dẫn giữa các skill | M | — | `grep` tên cũ trong repo ra rỗng |

**Thế giới quan tu luyện không phụ thuộc ngôn ngữ chỉ dẫn** — nó nằm ở vai, ở cách xưng hô, ở câu thoại người học nghe. Phần đổi sang tiếng Anh là phần chỉ có model đọc.

### Giai đoạn 2 — Dựng phép kiểm tự động · **M**

| Việc | Cỡ | Yêu cầu phục vụ | Xong khi |
|---|---|---|---|
| Đưa test đo token vào CI, fail nếu > 4.500 | S | A1 | CI đỏ khi có skill vượt |
| Test kiểm vị trí các mục bắt buộc nằm trước mốc | M | A3 | CI đỏ khi lược đồ rơi xuống sau mốc |
| Test cộng token mọi `SKILL.md`, cảnh báo khi > 25.000 | S | A4 | CI cảnh báo (không chặn) khi tổng vượt trần |
| Đo lại chênh lệch tokenizer sau khi đã chuyển sang tiếng Anh | S | ứng phó rủi ro tokenizer | Có số đo mới; biên an toàn 10% được giữ hoặc bỏ có căn cứ |

Đây là tầng 2 — rẻ nhất và chặn sớm nhất. **Làm trước khi viết skill thứ năm.**

Lưu ý: cột "Xong khi" nói "CI đỏ" nhưng CI chưa chạy được (chưa có remote). Cho tới lúc đó, đọc là **"lệnh chạy tay báo đỏ"** — test vẫn viết như nhau, chỉ khác ai bấm nút.

Hai điều phải quyết khi làm: (a) thêm `tiktoken` vào `requirements-dev.txt` — CI hiện chưa có; (b) chấp nhận phép đo là **proxy**. Proxy vẫn có giá trị: nó nhất quán giữa các lần đo nên bắt được *xu hướng phình*, kể cả khi con số tuyệt đối lệch.

### Giai đoạn 3 — Đưa chuẩn mực vào cơ chế · **M**

Giai đoạn này biến `VAN-DAO-chuan-muc-skill.md` từ tài liệu thành thứ có hiệu lực. Không làm thì tài liệu đó rơi vào đúng kịch bản pre-mortem §9.

| Việc | Cỡ | Yêu cầu phục vụ | Xong khi |
|---|---|---|---|
| Viết lại lens `skill-quality` theo **tám góc độ** ở Phần B của tài liệu chuẩn mực, thay cho tám check hiện tại vốn ra đời rời rạc | M | A2, B1, B2, B3, C1, C2 | Lens có đúng tám mục khớp tên tám góc; chạy thử trên một skill có sẵn ra kết quả hợp lý |
| Thêm vào bước đóng story: ghi số finding **và loại** vào Spec Change Log | S | D1 | Một story đóng sau đó có đủ hai thông tin |
| Phân giải tài liệu chuẩn mực thành rules mà agent tuân theo — qua skill BMAD, đích đến là `AGENTS.md` hoặc tương đương | M | — | Người viết skill tiếp theo nhận được rules mà không phải mở tài liệu |

### Giai đoạn 4 — Chốt kiến trúc · **S**

| Việc | Cỡ | Yêu cầu phục vụ | Xong khi |
|---|---|---|---|
| Một AD mới **phát biểu nguyên tắc** ngân sách ngữ cảnh là tài nguyên chung — không ghim con số (qua `bmad-architecture`, intent update) | S | nền cho A1, A4 | AD tồn tại trong spine, không chứa con số nào sẽ đổi |
| Sửa AD-8: đổi đơn vị đo từ "kích thước file" sang "token đường nạp mặc định"; ghi rõ 5.000 là **điểm cắt cụt**, không phải mục tiêu mềm | S | A1 | AD-8 không còn nói "kích thước" |
| Đưa hai tài liệu này vào spine như tài liệu triển khai, và ghi rõ **quan hệ** giữa chúng | S | — | Spine trỏ tới cả hai, nói rõ cái nào là nguồn giải thích, cái nào là nguồn thi hành |

### Việc chạy suốt, không thuộc giai đoạn nào

| Việc | Vì sao không xếp giai đoạn |
|---|---|
| Giữ hai tài liệu đồng bộ: `harness-viet-skill` (vì sao + cơ chế) và `chuan-muc-skill` (viết thế nào + đánh giá thế nào) | Rủi ro §9 đã nêu. Luật là nguồn thi hành, tài liệu là nguồn giải thích — khi lệch, sửa tài liệu theo luật |

---

## 8 · Ngoài phạm vi

- **Viết lại nội dung bốn skill theo một chuẩn thống nhất.** Giai đoạn 1 *dịch* chúng sang tiếng Anh — giữ nguyên cấu trúc, nhánh, và hành vi. Sắp xếp lại nội dung hay đổi cách tổ chức file là việc khác, không nằm ở đây.
- **Áp mô hình router** (SKILL.md chỉ chứa lệnh nạp, nội dung ở file khác). Đo được: tách ba nhánh hiếm của `thu-bi-kip` chỉ giảm **16%** — không giải được bài, mà đánh đổi khả năng đọc hiểu của người.
- **Đặt ngưỡng số từ** kiểu `<500 từ`. Không đo được ổn định giữa các ngôn ngữ, và không bộ skill trưởng thành nào đạt được ngưỡng của chính mình.
- **Sắp xếp lại thứ tự trong `thu-bi-kip`** vì con số 5.054 — nằm trong sai số đo, và việc chuyển ngôn ngữ ở Giai đoạn 1 đưa nó xuống ~2.450 nên vấn đề tự hết. (Skill này vẫn được dịch cùng ba skill kia — dịch khác với sắp xếp lại.)

---

## 9 · Rủi ro

| Rủi ro | Dấu hiệu sớm | Ứng phó |
|---|---|---|
| **Ngưỡng 5.000 sai vì tokenizer khác** | Skill "đạt" theo đo của ta nhưng vẫn mất nội dung khi chạy thật | Biên an toàn 10%, và **đo lại sau khi chuyển skill sang tiếng Anh** — các tokenizer lệch nhau nhiều nhất ở chữ có dấu, với tiếng Anh chúng hội tụ gần nhau, nên rủi ro này tự nhỏ đi. Việc đo lại nằm ở Giai đoạn 2 |
| **Kiểm tự động thành nghi thức** | CI xanh mà skill vẫn hỏng theo kiểu khác | Mỗi lần một lỗi mới lọt qua, thêm test cho đúng lỗi đó — như `tests/test_giam_dinh.py` đang làm |
| **Tài liệu này lệch khỏi luật được sinh ra từ nó** | Luật nói một đằng, tài liệu nói một nẻo | Luật là nguồn thi hành; tài liệu là nguồn giải thích. Khi lệch, sửa tài liệu theo luật, không ngược lại |
| **Phép kiểm tự động chặn nhầm** | Test đỏ với một skill mà người viết tin là vẫn ổn — vài lần như vậy là test bị tắt | Đã tính sẵn trong thiết kế, nói ra để thấy là chủ ý: **A4 chỉ cảnh báo, không chặn**; A1/A3 chặn nhưng có **đường miễn trừ tường minh qua A2** (khai phần nào mất được và vì sao). Một phép kiểm không có đường miễn trừ hợp lệ là phép kiểm sẽ bị vô hiệu hoá |
| **Sửa thứ tự làm hỏng skill đang chạy đúng** | Eval của skill đó fail sau khi sắp xếp lại | Chạy lại eval sau mỗi lần đổi thứ tự — bắt buộc, không phải tuỳ chọn |

### Pre-mortem

*Sáu tháng sau, tài liệu này thất bại. Vì sao?*

Khả năng cao nhất: **nó được viết, được đọc một lần, rồi không ai mở lại** — đúng số phận của `van-dao/.claude/rules/eval.md` trước đây. Skill thứ năm được viết theo trực giác, vượt ngưỡng, và không ai biết cho tới khi có người chạy review.

Điều ngăn kịch bản đó **không phải chất lượng của tài liệu này**, mà là Giai đoạn 2 có được làm hay không. Nếu chỉ làm được một việc trong bốn giai đoạn, làm Giai đoạn 2.
