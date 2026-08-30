# Chuẩn mực viết skill — và tám góc độ đánh giá một skill là tốt

**Trạng thái:** bản thảo, chưa chốt
**Ngày:** 2026-08-31
**Đọc cùng:** `VAN-DAO-harness-viet-skill.md` — tài liệu đó phân tích *vì sao* cần chuẩn này và *cơ chế nào* cưỡng chế nó. Tài liệu này nói *viết thế nào* và *đánh giá thế nào*.

Tài liệu chia hai phần, phục vụ hai người khác nhau:

- **Phần A — Viết** cho người sắp tạo một skill mới.
- **Phần B — Đánh giá** cho người soi một skill đã có, dù mình không viết nó.

Mọi ràng buộc **bắt buộc** (ID dạng `A1`, `B2`…) sống ở `VAN-DAO-harness-viet-skill.md` §5, không chép lại đây — hai nguồn cho cùng một luật thì sớm muộn lệch nhau. Tài liệu này trỏ tới chúng.

---

# Phần A — Viết một skill

## A.0 · Ba câu trả lời trước khi gõ dòng đầu tiên

Không phải ba bước, mà là ba câu mà nếu chưa trả lời được thì viết ra sẽ phải viết lại.

**1. Skill này sống ở ô nào?**

Hai trục quyết định gần như mọi lựa chọn còn lại:

|  | **Hậu quả nhẹ** — sai thì phiền, sửa được | **Hậu quả nặng** — sai thì hỏng dữ liệu, rò nội dung, hoặc người học nhận thông tin sai |
|---|---|---|
| **Sống qua nén ngữ cảnh** (phiên dài, gọi nhiều lần) | Ngắn là ưu tiên số một; văn xuôi đủ dùng | **Ô khó nhất.** Vừa phải ngắn vừa phải có cơ chế → đẩy tối đa vào script |
| **Không sống qua nén** (gọi một lần rồi thôi) | Thoải mái nhất | Không cần ngắn, **nhưng bắt buộc có cơ chế** |

Ví dụ thật: `thu-bi-kip` nằm ở ô dưới-phải — gọi một lần mỗi cuốn sách, nhưng sai thì ghi bẩn vùng dữ liệu của vai khác. Nên thứ bắt buộc với nó là `bin/giam-dinh.py`, không phải việc ép xuống dưới 3.000 token.

**2. Ràng buộc nào phải đúng *mọi lần*?**

Liệt kê ra. Với mỗi cái, hỏi: *nếu ai sửa skill vi phạm điều này, có gì bắt được không?* Không có → nó chưa phải ràng buộc, mới là nguyện vọng. Xem A.2.

**3. Người học nói gì khi cần skill này?**

Viết ra 3–5 câu thật họ sẽ gõ. Đó là nguyên liệu cho `description`, và `description` là thứ duy nhất luôn nằm trong ngữ cảnh.

## A.1 · Thứ tự viết — thứ mất đi thì hỏng âm thầm phải nằm ở đầu

Sau khi ngữ cảnh bị nén, mỗi skill chỉ được gắn lại **phần đầu**. Phần đuôi biến mất, và nó biến mất **không báo gì** — skill vẫn được gọi, vẫn trả lời trôi chảy.

Nên thứ tự trong file là quyết định thiết kế:

| Đặt ở đầu | Đặt ở cuối |
|---|---|
| Điều kiện kết thúc ("Xong khi") | Nhánh hiếm |
| Ranh giới ("Khi nào skill này không giúp được") | Ví dụ minh hoạ |
| **Bước nạp `customize.toml`** — quy ước bắt buộc, và nó phải chạy *trước việc chính* nên vị trí đầu là ràng buộc, không phải lựa chọn | Lý lẽ thiết kế |
| **Lược đồ dữ liệu và luật ghi file** | Ghi chú lịch sử |
| Ràng buộc an toàn | |
| Đường chạy chính | |

Ca thật: `truong-mon` đặt "Định dạng file" ở cuối theo thói quen tài liệu (tổng quan → chi tiết → phụ lục). Sau khi nén, nó vẫn được gọi để ghi `chi-diem.jsonl` mà **không còn lược đồ nào để ghi theo**. Thói quen viết tài liệu đúng ngược với thứ tự sống sót.

## A.2 · Ranh giới lời dặn và cơ chế

Đây là nguyên tắc đắt nhất trong dự án này, vì nó được học bằng cách làm sai.

Một câu in đậm trong `SKILL.md` là **gợi ý xác suất**, không phải lệnh. Model diễn giải nó, không thực thi nó. Muốn một điều chắc chắn xảy ra mọi lần, nó phải nằm **ngoài** model.

| Viết thế này | Thay bằng |
|---|---|
| `**Tuyệt đối không in nội dung sách**` | Script chỉ trả về các khoá số liệu; nội dung không có đường ra |
| `Kiểm file tồn tại, đuôi hợp lệ, kích thước > 0` | Script làm ba phép kiểm, trả **mã thoát khác nhau** cho từng ca |
| `Chỉ gửi thư khi đúng là bản hỏng` | Mã thoát 1 = chặn sớm, mã thoát 2 = bản hỏng. Ranh giới thành vật lý |

Phép thử một dòng: **nếu ai sửa skill vi phạm điều này, có gì bắt được không?**

Không phải mọi thứ đều đáng chuyển thành script. Chỉ những thứ mà vi phạm gây hỏng dữ liệu, rò nội dung, hoặc ghi sang vùng của vai khác. Phần còn lại viết bằng lời là hợp lý — và nên nói thẳng rằng đó là quy ước, đừng dùng chữ "tuyệt đối" cho thứ không có gì cưỡng chế.

## A.3 · `description` là điều kiện kích hoạt, không phải bản tóm tắt

`description` luôn nằm trong ngữ cảnh, kể cả khi skill không được gọi. Nó có đúng một việc: giúp quyết định *có nên gọi skill này không*.

| Sai kiểu | Đúng kiểu |
|---|---|
| "Giám định một cuốn sách, làm bốn phép kiểm, ghi con trỏ vào kho" | "Dùng khi người học nói *tôi tải được cuốn X rồi*, *đưa cuốn này vào kho*, hoặc đưa thẳng đường dẫn một file sách" |

Mô tả chức năng khiến model đọc `description` rồi tưởng mình đã biết đủ để tự làm — và không mở skill ra. Mô tả tình huống thì nó chỉ dùng để khớp, rồi mở skill.

Nếu bỏ lỡ kích hoạt gây hậu quả thật, đừng chỉ dựa vào `description`: thêm một đường vào tường minh từ skill khác trong cùng luồng.

## A.4 · Khi skill phình — bốn cách, xếp theo hiệu quả đã đo

| # | Cách | Hiệu quả đo được ở `thu-bi-kip` | Được thêm gì |
|---|---|---|---|
| 1 | **Việc tất định → script** | *(xem ghi chú)* | Ràng buộc thành cơ chế |
| 2 | **Lược đồ, khuôn file → `references/`** nạp lúc cần | **1.349** token | — |
| 3 | **Lý lẽ thiết kế → Design Notes của story** | *(xem ghi chú)* | Vẫn truy vết được |
| 4 | **Nhánh hiếm → file riêng** | **827** token (16%) — đo bằng cách cộng ba nhánh Đ/E/G | — |

Cách 1 và 3 làm cùng một lượt nên **không tách bạch được**: `thu-bi-kip` đi từ 7.967 → 5.054, giảm 2.913, trong đó 1.349 là cách 2 (đo riêng được), còn **1.564 token là của cách 1 và 3 cộng lại**. Ghi hai con số riêng cho chúng sẽ là bịa độ chính xác không có.

Luôn hỏi cách 1 trước khi nghĩ tới cách 4. Tách file chỉ dời chỗ; chuyển thành script vừa dời chỗ vừa biến lời dặn thành cơ chế.

**Một cách thứ năm, hiệu quả nhất mà ít ai nghĩ tới: viết bằng tiếng Anh.** Đo trên chính các file của ba dự án, tiếng Việt có dấu tốn **2,06 lần** token so với tiếng Anh trên cùng lượng ký tự. Phần chỉ dẫn (model đọc) viết tiếng Anh; câu thoại người học nghe thì giữ nguyên ngôn ngữ của họ.

## A.5 · Bốn mục bắt buộc

Mọi `SKILL.md` phải có, và lý do từng mục:

| Mục | Vì sao bắt buộc |
|---|---|
| **Xong khi** | Không có điều kiện kết thúc quan sát được thì không ai biết lúc nào ngừng tin skill. Nêu cả thứ **không được xảy ra** — "không có thư nào được ghi" cũng là một phần của "xong" |
| **Khi nào skill này không giúp được** | Ranh giới phải nằm trong công cụ, không chỉ trong tài liệu thiết kế. Mỗi mục kèm chỗ chuyển tiếp |
| **Trình → xác nhận → ghi → kiểm** | Không ghi đè im lặng; ghi xong đọc lại; lệch thì quay lại sửa, có giới hạn số vòng |
| **Nạp `customize.toml`** | Field phơi ra mà không có bước đọc thì nó là tài liệu, không phải hành vi. Không phơi field nào thì ghi rõ "không có tuỳ biến" |

## A.6 · Eval đi cùng lúc viết, không để sau

Viết xong nháp thì chạy eval ngay, mức nhẹ là đủ: 2–3 kịch bản khớp ma trận I/O, evidence trích **nguyên văn transcript chạy thật**.

Ba điều eval phải làm mà đọc lại mã không làm được:

- **Mọi lệnh skill bảo người dùng gõ đều đã được gõ thử.** Ca thật: `pip install -r requirements-dev.txt` hỏng trên Windows vì file có comment tiếng Việt có dấu — không ai đọc file mà thấy được.
- **Chạy trên bản đã cài, không phải bản trong repo.** Plugin cache là bản copy; sửa xong mà không cài lại là đang kiểm bản cũ.
- **Kiểm cả thứ không được xảy ra** — không có thư thừa, không có bản ghi thừa.

## A.7 · Review độc lập, và dấu vết của nó

Tự chấm theo tám góc ở Phần B **không thay thế được** một vòng `bmad-review`. Bằng chứng trong chính dự án này: cả `work-state` lẫn `orca-help` đều tự chấm 8/8 pass trước khi review; lens sau đó tìm ra 16 và 18 finding. Với `work-state`, ba lỗi nặng nhất — script im lặng khi không kết luận được — tự chấm bỏ sót hoàn toàn.

Lý do không phải người tự chấm cẩu thả. Tự chấm hỏi *"có làm đúng những gì tôi định làm không"*; lens hỏi *"nó hỏng bằng cách nào"*. Hai câu khác nhau, và câu thứ hai khó tự hỏi mình.

**Khi nào bắt buộc review.** Output trong luồng BMAD đã có cổng sẵn (`bmad-build` step-04). Output **ngoài luồng** thì không có cổng nào — nó phụ thuộc ai đó nhớ, và điều đó đã hỏng thật: `work-state` được review vì có người bảo, `orca-help` thì không cho tới khi có người để ý.

**Ranh giới cái gì cần một vòng review riêng** — và nó hẹp hơn ta tưởng:

| Cần | Không cần |
|---|---|
| Skill, lens, tài liệu quy tắc — **chuẩn để người khác làm theo** | **Bản ghi sự kiện** (sprint-status, deferred-work, sổ review) — ghi lại quyết định đã có, không tạo hành vi mới |
| Script chạy trong luồng thật | **Test** — có oracle riêng (chạy được, xanh/đỏ); review cùng lượt với code nó kiểm |
| | **Config** — review cùng lượt với thứ nó cấu hình |

Ba mục cột phải không phải là miễn trừ vì chúng kém quan trọng, mà vì chúng **đã được kiểm bằng đường khác**: bản ghi được kiểm bởi việc dùng, test bởi chính việc chạy, config bởi thứ nó cấu hình.

Cạm bẫy đã mắc phải một lần: khi bị hỏi *"cơ chế này có review chính nó chưa"*, phản ứng đầu tiên là nhét mọi thứ vào phạm vi — và tạo ra 12 món nợ, phần lớn không đáng. **Có mặt trong sổ và cần review là hai câu hỏi khác nhau.** Sổ trả lời câu đầu cho mọi artifact; chỉ câu thứ hai mới là cổng.

**Không cưỡng chế được hành động, nhưng cưỡng chế được bằng chứng.** Không có cách nào bắt ai chạy review — nó cần phán đoán, không đếm được. Đây đúng là bài toán AD-10 đã giải cho eval: không ép được ai chạy eval, nhưng ép được *"phải có `evals.json`"*.

Áp cùng hình dạng: mọi artifact harness được version control phải **có mặt** trong `_bmad-output/implementation-artifacts/review-log.md`, với một trong ba trạng thái — `da-review`, `no` (kèm mốc quay lại), `mien-tru` (kèm lý do). `tests/test_review_log.py` kiểm sự có mặt đó.

Ba điều về thiết kế này, nói thẳng vì chúng là giới hạn chứ không phải chi tiết:

- **Test kiểm sự có mặt, không kiểm chất lượng.** Một dòng ghi bừa vẫn qua. Nhưng nó nâng chi phí nói dối từ *im lặng* lên *phải chủ động viết một câu sai* — cùng ranh giới AD-10 đã chấp nhận.
- **`no` không làm test đỏ.** Quy tắc mới áp lên artifact có sẵn sẽ đỏ hàng loạt, và phép kiểm đỏ kéo dài thì bị tắt. Nợ hiện ra trong sổ, không biến mất, nhưng không chặn việc khác.
- **Thứ test thật sự bắt** là một artifact mới xuất hiện mà không ai ghi nhận. Đó chính là ca đã xảy ra với `orca-help`.

Phạm vi tính theo `git ls-files`, nên thứ bị gitignore — 49 skill BMAD cài từ ngoài chẳng hạn — tự động nằm ngoài, không cần danh sách loại trừ tự bịa.

---

# Phần B — Tám góc độ đánh giá một skill

Dùng khi soi một skill đã viết, kể cả không phải mình viết. Mỗi góc độ có **câu hỏi chấm** và **cách kiểm**; không có điểm số, vì điểm số khuyến khích tối ưu cho thước đo thay vì cho chất lượng.

Thứ tự dưới đây theo *hậu quả khi hỏng*, không theo dễ kiểm.

### 1 · Sống sót — nội dung quan trọng còn nguyên sau khi ngữ cảnh bị nén

> Nếu chỉ phần đầu của file này sống sót, skill còn làm đúng không?

**Kiểm:** đo token tích luỹ; xem mục nào rơi sau **mốc 5.000 token** — sau khi ngữ cảnh bị nén, mỗi skill chỉ được gắn lại đúng chừng ấy token đầu file. Lược đồ dữ liệu, luật ghi, ràng buộc an toàn nằm sau mốc là hỏng.
**Mốc thứ hai:** mọi skill được gắn lại chia chung **25.000 token**. Skill gọi sớm trong phiên bị bỏ *hẳn* khi ngân sách đó cạn — không phải cắt bớt phần đuôi, mà mất cả file.
**Hỏng thế nào:** âm thầm nhất trong tám góc. Skill vẫn chạy, vẫn tự tin, chỉ thiếu một nửa chỉ dẫn.

### 2 · Cưỡng chế — ràng buộc quan trọng là cơ chế, không phải chữ

> Với mỗi điều skill nói "tuyệt đối/không bao giờ/phải luôn": có gì bắt được nếu vi phạm?

**Kiểm:** đọc từng ràng buộc mạnh, tìm script/mã thoát/schema tương ứng. Không có → hoặc chuyển thành cơ chế, hoặc hạ giọng cho trung thực.
**Hỏng thế nào:** vi phạm không bị phát hiện cho tới khi hậu quả đã xảy ra.

### 3 · Đúng việc — làm đúng thứ hứa, từ chối rõ thứ ngoài phạm vi

> Skill có nêu điều kiện kết thúc quan sát được không? Có nói rõ thứ nó **không** làm, kèm chỗ chuyển tiếp không?

**Kiểm:** đọc "Xong khi" và "Khi nào không giúp được". Ranh giới chỉ nằm trong tài liệu thiết kế mà không nằm trong skill thì không tính.
**Hỏng thế nào:** skill lấn sang việc của vai khác, hoặc bịa ra thứ chưa dựng.

### 4 · Kích hoạt — được gọi đúng lúc

> `description` mô tả *tình huống* hay *chức năng*? Nếu bỏ lỡ thì hậu quả có thật không?

**Kiểm:** đọc câu đầu của `description`. Với skill mà bỏ lỡ gây hậu quả thật, tìm đường vào tường minh từ skill khác.
**Hỏng thế nào:** thất bại im lặng — không ai biết skill đã không được gọi.

### 5 · Bằng chứng — có eval chạy thật, còn dùng được sau này

> Evidence là transcript nguyên văn hay là mô tả hành vi mong đợi? Có tái tạo được không?

**Kiểm:** mở `evals/evals.json`. Đường dẫn trỏ vào thư mục tạm của một phiên là không tái tạo được. Không có lệnh cài/chạy là không tái tạo được.
**Hỏng thế nào:** cho cảm giác an tâm không phân biệt được với không có eval.

### 6 · Tự đủ — chạy được khi chỉ có một mình nó

> Người cài plugin, không có repo phát triển, đọc file này có làm đúng được không?

**Kiểm:** tìm trích dẫn số hiệu requirement, số mục đặc tả, đường dẫn chỉ tồn tại trong workspace. Mọi thứ skill cần phải nằm trong thứ được ship.
**Hỏng thế nào:** người dùng thật gặp một tham chiếu không tra được.

### 7 · Chi phí — ngân sách tương xứng tần suất

> Skill này tốn bao nhiêu, và nó được gọi bao lâu một lần?

**Kiểm:** đo token; đối chiếu với ô trong bảng A.0. Một skill 5.000 token gọi mỗi chương đắt hơn nhiều một skill 5.000 token gọi mỗi cuốn sách.
**Hỏng thế nào:** đẩy skill khác ra khỏi ngữ cảnh — hỏng ở chỗ khác chứ không ở chính nó.

### 8 · Đọc được — người bảo trì hiểu và sửa được

> Người kế thừa mở file này ra, trong bao lâu thì biết nó làm gì?

**Kiểm:** đọc một lượt. Nội dung bị đẩy ra sau một lệnh render (router pattern) thì rất rẻ cho model nhưng đắt cho người: không diff được trong PR, không review được.
**Hỏng thế nào:** không ai dám sửa; skill đóng băng rồi bị viết lại từ đầu.

## Bảng tóm — dùng khi soi nhanh

| # | Góc độ | Một câu để hỏi |
|---|---|---|
| 1 | Sống sót | Chỉ 5.000 token đầu sống sót thì còn đúng không? |
| 2 | Cưỡng chế | Vi phạm thì có gì bắt được? |
| 3 | Đúng việc | Xong khi nào, và không làm gì? |
| 4 | Kích hoạt | `description` tả tình huống hay chức năng? |
| 5 | Bằng chứng | Transcript thật hay mô tả mong đợi? |
| 6 | Tự đủ | Chỉ có file này thì làm đúng được không? |
| 7 | Chi phí | Tốn bao nhiêu, gọi bao lâu một lần? |
| 8 | Đọc được | Người kế thừa hiểu trong bao lâu? |

**Năm góc đã cắn thật trong dự án này**, mỗi góc kèm ca cụ thể:

| Góc | Ca thật |
|---|---|
| 1 · Sống sót | `truong-mon` mất trọn lược đồ `chi-diem.jsonl` sau khi nén |
| 2 · Cưỡng chế | `**tuyệt đối không in text**` không ngăn được gì cho tới khi bọc thành script |
| 3 · Đúng việc | `truong-mon` khai "việc thu nhận sách chưa dựng ở bản này" trong khi nó đã dựng |
| 5 · Bằng chứng | Eval của `nhap-mon` dẫn lệnh `/vd:` đã bị đổi tên; `pip install` chưa từng ai gõ thử |
| 6 · Tự đủ | `nhap-mon/SKILL.md` từng trích "(FR32)"/"§12.4" — vô nghĩa với người chỉ cài plugin |

Góc **4 · Kích hoạt** và **7 · Chi phí** và **8 · Đọc được** chưa cắn lần nào. Chúng có mặt vì hỏng theo kiểu chậm: không lộ ở một lần chạy, mà lộ sau vài tháng — hoặc lộ ở chỗ khác chứ không ở chính skill đó.

---

## Phần nào phổ quát, phần nào riêng Vấn Đạo

Phép thử: **bỏ hết danh từ riêng của Vấn Đạo đi, câu đó còn đúng không?**

| Phổ quát — áp được cho mọi dự án dùng Claude Code | Riêng Vấn Đạo |
|---|---|
| Hai trục phân loại skill (A.0) | Bốn mục bắt buộc (A.5) |
| Thứ tự sống sót (A.1) | Vai nào ghi vùng dữ liệu nào |
| Ranh giới lời dặn / cơ chế (A.2) | Ngưỡng token cụ thể của dự án |
| `description` là điều kiện kích hoạt (A.3) | Thuật ngữ hệ (bí kíp, mạch, chỉ điểm) |
| Bốn cách xử lý khi skill phình (A.4) | |
| Tám góc độ đánh giá (Phần B) | |
| Eval đi cùng lúc viết (A.6) | |

Cột trái tách ra dùng lại được ngoài Vấn Đạo. Cột phải thì không, và cũng không nên cố làm cho nó phổ quát.
