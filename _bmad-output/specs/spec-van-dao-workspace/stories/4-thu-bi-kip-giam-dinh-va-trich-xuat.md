---
title: 'Thu bí kíp — giám định và trích xuất'
type: 'feature'
created: '2026-08-28'
status: 'done'
baseline_commit: 'dbe11c22215026ec484f778cb0b2cd5ec3de3cce'
approved: '2026-08-28'
review_loop_iteration: 0
context:
  - '{project-root}/AGENTS.md'
# Phạm vi story 4 gốc đã tách tại step-01 (người dùng chọn [S]); 3 mục tiêu còn lại đã ghi kèm mốc
# quay lại ở _bmad-output/implementation-artifacts/deferred-work.md. Thư bao_ban_hong từng bị hoãn
# nhưng đã đưa lại vào phạm vi sau vòng elicitation — xem Design Notes.
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Người học đi tìm được sách theo chỉ điểm (Story 1.3) rồi mang về, nhưng chưa có đường nào đưa cuốn sách đó vào hệ — không ai giám định được sách dùng được hay không, không ai rút được chữ ra khỏi PDF/EPUB.

**Approach:** Skill mới `thu-bi-kip` nhận đường dẫn sách, gọi thẳng hàm `extract_single_file` của engine `book-to-skill` (đã cài, đã verify chạy thật), rồi làm bốn phép giám định trên số liệu trả về và trình cho người học kèm ước chi phí. Rút được chữ → ghi con trỏ tới file kèm kết quả giám định vào kho. Không rút được → dừng ngay, khuyên tìm bản khác, và gửi thư báo Trưởng môn để đánh dấu bản hỏng.

## Boundaries & Constraints

**Always:** **Kiểm engine có cài chưa trước mọi việc khác** — thử `import book_to_skill`; chưa có thì nói rõ và đưa đúng lệnh cài (`pip install -r requirements-dev.txt` từ gốc repo, nơi phiên bản đã được ghim), **không tự chạy lệnh cài hộ** (cài gói vào máy người dùng là việc phải hỏi), rồi dừng. **Kiểm ba điều trước khi gọi engine, đúng thứ tự:** (a) đường dẫn có trỏ tới **một file thật** không — hỏi bằng `Path.is_file()`, không phải `Path.exists()` (một thư mục tên `sach.epub` cho `exists()` đúng), (b) đuôi file **hạ chữ thường rồi** có nằm trong `book_to_skill.config.SUPPORTED_EXTENSIONS` không — hằng số đó chỉ chứa đuôi chữ thường, so thẳng thì một file `.EPUB` hợp lệ bị từ chối oan; đọc hằng số từ chính gói, không chép tay danh sách vào skill, (c) kích thước file có lớn hơn 0 không. Cả ba qua rồi mới gọi engine bằng **API Python** `book_to_skill.extract_single_file(Path, extraction_mode, install_mode)` — không qua CLI, không tự viết lại bộ phân giải, `install_mode` luôn là `"no"` (không tự cài gói khi đang chạy). **`ExtractionError` chỉ được hiểu là "bản hỏng" SAU KHI cả ba phép kiểm trên đã qua** — engine ném cùng một loại lỗi đó cho cả đường dẫn sai lẫn định dạng lạ, nên bắt nó mà không kiểm trước là gán nhầm tội cho một cuốn sách tốt; không phân loại lỗi bằng cách đọc chuỗi thông báo (chuỗi đó không phải hợp đồng ổn định giữa các phiên bản). **Giá trị trả về là một `dict` chứa khoá `text` giữ TOÀN BỘ nội dung sách — tuyệt đối không in, không giữ, không trích khoá đó vào ngữ cảnh** (ca tệ nhất đã đo: một sách kỹ thuật 514 trang cho 196K token / 1,37 triệu ký tự trong đúng khoá đó — gần 8 lần ngân sách skill của cả phiên); chỉ đọc các khoá số liệu (`filename`, `source_file`, `format`, `extraction_method`, `pages`, `pages_label`, `spine_items`, `words`, `chars`, `file_size_mb`, `estimated_tokens`, `chapters_detected`, `chapters_method`, `chapter_headings_sample`, `has_toc`, `images_dropped` — đúng 16 khoá, tức mọi khoá bản đã ghim trả về trừ `text`). Bản engine sau có thể thêm khoá mới: **khoá không nằm trong danh sách trên thì bỏ qua, không in** — không có gì bảo đảm một khoá lạ không lại là nội dung sách. Làm đủ **bốn phép giám định**: (1) rút được chữ không, (2) mục lục lấy được không — không lấy được thì **báo rồi vẫn đi tiếp**, không coi là hỏng, (3) cấu trúc `chuoi` hay `mang` — **hỏi người học bằng lời họ trả lời được, rồi hệ tự suy**: không bao giờ hỏi thẳng "sách này chuỗi hay mạng" (đó là từ vựng của hệ, người mới không trả lời được — cùng lý do nhánh chưa-biết hỏi vai chứ không hỏi mạch); hỏi kiểu *"cuốn này đọc từ đầu đến cuối, hay tra chỗ nào cần chỗ đó?"* rồi suy ra và **ghi kèm cờ nguồn** cho biết đây là suy từ câu trả lời của người học, không phải hệ tự đoán từ metadata (metadata không có trường nào cho biết điều này, và skill bị cấm đọc `text`). Ra `mang` thì nói rõ sẽ cần người học nêu vài tình huống thật ở bước sau — là xin thêm đầu vào, không phải chê sách, (4) bao nhiêu chương và **ước chi phí** — ước bằng `estimated_tokens` cho **các pha xử lý phía sau**, không phải thời gian rút chữ (rút chữ chỉ vài giây kể cả sách 500 trang, không đáng cảnh báo); trình rồi chờ duyệt. Khi trình số trang phải kèm `pages_label` để không nói "23 trang" cho một EPUB vốn không có trang; đúng trình tự "Trình → xác nhận → ghi → kiểm" và đủ 4 quy ước §12.4; behavioral eval nhẹ đi cùng ngay (AD-10); không trích FR/NFR/§ trong nội dung skill (AD-11); tự xác định lại home-dir hiện tại trước khi đọc/ghi bất kỳ đường dẫn `~/.vandao/...` nào trong phiên (bug đã gặp 2 lần).

**Ask First:** (không có — phạm vi đã thu hẹp còn một mục tiêu, không có quyết định cần người can thiệp giữa chừng)

**Never:** Không rút được chữ thì **dừng hẳn** — không OCR, không đoán nội dung, không tạo bản ghi rỗng để "có cho đủ". Không lưu bản sao nội dung sách vào kho — chỉ ghi **con trỏ tới file gốc** kèm kết quả giám định. Không ghi `chi-diem.jsonl` trực tiếp — đó là vùng ghi của Trưởng môn; báo bản hỏng bằng **thư** vào hộp thư chung. **Không gửi thư báo bản hỏng khi lỗi bắt nguồn từ đường dẫn sai hoặc định dạng lạ** — thư đi sang vai khác và ghi vào dữ liệu của Trưởng môn, nên báo sai ở đây làm bẩn dữ liệu chứ không chỉ làm phiền màn hình; gõ nhầm tên file thì hỏi lại người học, không đụng tới hộp thư. Không làm thiết kế sư phạm (xương sống, tiêu chí đạt, điểm hạ sơn), không sinh chương, không cắt text theo chương — đó là mục tiêu đã tách, và nó có cổng người-duyệt bắt buộc riêng. Không tạo bí kíp dạy được — bản này dừng ở "đã giám định, đã biết chữ rút ra được". Không kích hoạt nghi thức thu bí kíp — chưa có bí kíp để mừng. Không dùng `extraction_mode = "technical"` — gói `docling` chưa cài nên nó tự lùi về nhánh text, gọi vào chỉ tạo ảo giác đã xử lý bảng/công thức.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Engine chưa cài trên máy | `import book_to_skill` thất bại | Nói rõ engine chưa có kèm đúng lệnh cài từ gốc repo; **không tự chạy lệnh cài**; dừng tại đây | Không lỗi — chặn trước mọi việc khác |
| Sách rút được chữ, có mục lục | EPUB/PDF hợp lệ, `has_toc` đúng | Trình đủ bốn phép giám định kèm ước chi phí và số trang có nhãn; xác nhận rồi ghi con trỏ + giám định vào kho, đọc lại kiểm | Không lỗi |
| Rút được chữ nhưng không có mục lục | `chapters_detected = 0`, `has_toc` sai | **Báo rõ rồi vẫn đi tiếp** — nói người học sẽ tự xếp chương ở bước sau; không coi là sách hỏng, không dừng | Không lỗi |
| Sách cấu trúc mạng | Sách tra cứu, cùng kỹ thuật ở nhiều vùng | Báo là cấu trúc `mang`, nói rõ lộ đồ sau này dựng theo nhiệm vụ và cần người học nêu vài tình huống thật — là xin thêm đầu vào, không phải chê sách | Không lỗi |
| Không rút được chữ | File hỏng/đổi đuôi/bản chụp ảnh | `ExtractionError` → dừng ngay, nói rõ không rút được chữ từ bản này, khuyên tìm bản khác; gửi thư báo Trưởng môn đánh dấu bản hỏng; không ghi gì vào kho | Không lỗi — từ chối sạch |
| Đường dẫn không trỏ tới một file dùng được | File không tồn tại, **đường dẫn là thư mục** (kể cả khi tên mang đuôi `.epub`), đuôi ngoài danh sách engine nhận *sau khi hạ chữ thường*, hoặc kích thước 0 | Nói rõ lý do kèm danh sách định dạng nhận được nếu là ca định dạng; hỏi lại đường dẫn. **Không gọi engine, và tuyệt đối không gửi thư báo bản hỏng.** Đuôi viết hoa (`.EPUB`) **không** thuộc ca này — hạ chữ thường rồi so, nó là sách hợp lệ | Không lỗi — chặn sớm, không bẩn dữ liệu vai khác |
| Thu lại cuốn đã có trong kho | Kho đã có con trỏ tới đúng sách đó | Báo rõ đã có, không ghi đè bản cũ, hỏi người học muốn làm gì tiếp | Không lỗi — không tạo bản sao |
| Con trỏ trong kho trỏ tới file đã dời chỗ | Kho có bản ghi cũ, file gốc không còn ở đường dẫn đó | Báo rõ file không còn ở chỗ cũ, hỏi đường dẫn mới rồi cập nhật đúng bản ghi đó — không xoá bản ghi, không coi là sách hỏng | Không lỗi — không gửi thư báo bản hỏng |

</frozen-after-approval>

## Code Map

- `van-dao/skills/thu-bi-kip/SKILL.md` (mới) -- skill giám định + trích xuất, đủ 4 quy ước §12.4
- `van-dao/skills/thu-bi-kip/references/dinh-dang.md` (mới) -- lược đồ bản ghi kho + thư, nạp khi tới bước ghi (tách khỏi SKILL.md để giữ ngân sách token)
- `van-dao/skills/thu-bi-kip/customize.toml` (mới) -- phơi `ngan_sach_token`, kèm ví dụ file cá nhân chép được
- `van-dao/bin/giam-dinh.py` (mới) -- bọc engine: làm ba phép kiểm đường dẫn rồi gọi `extract_single_file`, chỉ trả khoá số liệu; `text` không có đường ra stdout
- `van-dao/tests/test_giam_dinh.py` (mới) -- 11 test khoá lại từng lỗi tìm ra khi chạy thật; CI chạy trên cả ubuntu lẫn windows
- `van-dao/skills/thu-bi-kip/evals/evals.json` (mới) -- eval nhẹ AD-10, khớp I/O matrix, chạy thật trên sách chung
- `van-dao/tests/fixtures/sach-thu/README.md` -- công thức lấy sách chung (Art of War, Gutenberg #132); sách không vào repo vì `.gitignore` chặn `*.epub`, nên công thức là thứ được version control
- `van-dao/skills/truong-mon/SKILL.md` (đọc-only, mẫu tái dùng) -- khuôn trình→xác nhận→ghi→kiểm, bước tự tra home-dir, cách viết mục "khi nào skill này không giúp được"
- `docs/VAN-DAO-dac-ta-v1.0.md` §6.1-6.3, §6.9 (đọc-only) -- bảng bốn phép giám định, ba pha, chuỗi/mạng, nối lại khi file dời chỗ; §6.1 có sẵn schema JSON của thư báo bản hỏng
- `_bmad-output/implementation-artifacts/deferred-work.md` (đọc-only) -- 3 mục tiêu đã tách khỏi story này kèm mốc quay lại

## Tasks & Acceptance

**Execution:**
- [x] `van-dao/skills/thu-bi-kip/SKILL.md` -- viết skill mới: nhận đường dẫn, gọi API `extract_single_file`, làm đủ bốn phép giám định, hai nhánh rút-được / `ExtractionError` -- đúng luồng ba pha nhưng chỉ tới hết giám định
- [x] `van-dao/skills/thu-bi-kip/evals/evals.json` -- 8 kịch bản khớp I/O matrix, evidence trích nguyên văn transcript chạy thật trên sách chung -- AD-10

**Acceptance Criteria:**
- Given một EPUB rút được chữ, when người học đưa đường dẫn cho `/van-dao:thu-bi-kip`, then engine chạy thật qua API, bốn phép giám định trình ra khớp đúng số liệu dict trả về, số trang có kèm nhãn, và sau xác nhận thì con trỏ tới file + giám định được ghi vào kho, đọc lại kiểm khớp
- Given một file ném `ExtractionError`, when chạy skill, then dừng ngay với lời khuyên tìm bản khác, có một thư báo bản hỏng gửi cho Trưởng môn, và không có bản ghi nào trong kho — kiểm bằng cách đọc kho trước và sau
- Given dict trả về chứa khoá `text` cỡ ~78K token, when skill xử lý sách, then không có bước nào in hay giữ khoá đó — chỉ đọc các khoá số liệu
- Given một sách không có mục lục (`chapters_detected = 0`), when giám định, then skill báo rõ và **vẫn đi tiếp**, không coi là sách hỏng
- Given người học gõ sai đường dẫn, trỏ vào một thư mục, hoặc đưa file định dạng lạ, when chạy skill, then skill hỏi lại đường dẫn và **không có thư nào được gửi** — kiểm bằng cách đọc hộp thư trước và sau; engine không được gọi
- Given engine chưa cài trên máy, when chạy skill, then skill nói rõ và đưa đúng lệnh cài, không tự chạy lệnh cài, và dừng — không thử gọi engine rồi để lỗi import lộ ra thô
- Given `thu-bi-kip/SKILL.md` sau khi viết xong, when soát nội dung, then không có bước thiết kế sư phạm, không sinh chương, không kích hoạt nghi thức, không ghi `chi-diem.jsonl` trực tiếp, và không lưu bản sao nội dung sách
- Given người học hỏi bước tiếp theo sau khi giám định xong, when skill trả lời, then nói rõ phần thiết kế sư phạm chưa có ở bản này, không bịa lộ trình học

## Spec Change Log

**2026-08-28 — vòng Advanced Elicitation (Map Is Not the Territory), trước khi duyệt.** Bản nháp đầu mô tả engine qua **CLI**: mã thoát 0/1, kết quả ra thư mục tạm ngẫu nhiên, đọc `metadata.json`. Mọi số liệu đó đo đúng — nhưng đo sai giao diện: đặc tả §6.2 chỉ rõ phải gọi thẳng `book_to_skill.extract_single_file()`, không qua CLI. Chạy thật API cho thấy nó khác CLI ở ba chỗ quyết định: trả `dict` thay vì file, ném `ExtractionError` thay vì mã thoát, và **giữ toàn bộ nội dung sách ngay trong khoá `text` của giá trị trả về** — khiến ràng buộc chống-tràn-ngữ-cảnh mạnh hơn bản nháp mô tả. API cũng trả thêm `pages_label`/`spine_items` mà CLI giấu mất; nhờ đó kết luận trung gian "`pages` là số vô nghĩa" bị bác — nó có nhãn, chỉ là CLI không đưa ra. Cùng vòng này bổ sung ba phép giám định §6.1 bản nháp bỏ sót (mục lục → báo rồi đi tiếp; chuỗi hay mạng; ước chi phí), sửa "lưu bản trích xuất" thành "lưu con trỏ tới file" cho khớp §6 ("bí kíp lưu con trỏ tới file, không lưu bản sao"), và đưa thư `bao_ban_hong` trở lại phạm vi.

**2026-08-28 — vòng `bmad-review` trước khi duyệt (lens adversarial, edge-case-hunter, structure, prose).** Vá các mâu thuẫn nội bộ và hai lỗ kiểm được bằng lượt chạy thật; **không mở rộng phạm vi**. Đã vá: câu "kiểm ba điều" nhưng câu sau nói "hai phép kiểm trên"; phép kiểm đường dẫn dùng `exists()` nên một thư mục `.epub` lọt qua rồi bị vu là bản hỏng; phép kiểm định dạng so `suffix` thẳng nên `.EPUB` hợp lệ bị chặn oan; danh sách khoá số liệu thiếu 5 khoá engine thật trả về (`spine_items`, `chars`, `file_size_mb`, `filename`, `source_file`) và không có luật cho khoá lạ ở bản engine sau; số token của cùng một lượt chạy ghi hai nơi hai giá trị (`~77K` / `~78K` — đo lại: 77.852, nên `~78K`); Tasks và Verification hứa 6 kịch bản trong khi I/O matrix đã lên 8 dòng qua các vòng elicitation; Design Notes xếp "file hợp lệ" vào danh sách sáu kiểu cùng ném `ExtractionError` — file hợp lệ không ném, thực chỉ có năm kiểu.

**Cùng vòng đó, hai phát hiện KHÔNG vá vì là quyết định phạm vi, đã ghi mốc quay lại ở `deferred-work.md`:** thư `bao_ban_hong` ghi vào một thư mục bàn giao chưa tồn tại và chưa có file phạm vi đi kèm (luật đặc tả: thiếu file đó thì coi như không vai nào đọc được), và trường `bi_kip_chi_diem` trong khuôn thư chưa có nguồn để điền ở bản này.

**2026-08-28 — step-03, hai thay đổi hành vi phát hiện khi CHẠY eval thật (không phải khi đọc lại spec).** (1) Phép kiểm kho ban đầu nằm ở bước ghi, tức sau khi đã rút chữ và hỏi người học một câu về cấu trúc sách; lượt eval kịch bản "thu lại cuốn đã có" cho thấy người học phải trả lời một câu vô ích cho việc đằng nào cũng không ghi. Đã chuyển thành Bước 2b, chạy trước khi gọi engine — so `duong_dan`/`filename` chỉ cần đường dẫn. (2) Nhánh "đã có trong kho" và nhánh "file dời chỗ" chồng lấn: một bản ghi khớp tên file nhưng `duong_dan` đã chết sẽ rơi vào nhánh báo trùng, bỏ mặc con trỏ chết. Đã thêm phép kiểm `is_file()` trên đường dẫn cũ để tách hai nhánh. Cả hai đều có bằng chứng hai bản (trước/sau vá) trong `evals.json`.

**Cùng lượt đó, `bi_kip_chi_diem` được chốt đúng mốc đã ghi:** hỏi người học tên sách đã được chỉ điểm rồi rút định danh kebab-case; để trống khi sách tự tìm; luôn ghi thêm `ten_sach` làm đường khớp dự phòng. Chi tiết cân nhắc và hướng bị loại ghi ở trường `resolved` của mục tương ứng trong `deferred-work.md`.

**2026-08-28 — step-04 review (5 lens), bảy thay đổi hành vi.** Vòng review tìm ra 28 finding (skill-quality 6 · edge-case-hunter 6 · adversarial 10 · structure 4 · prose 2; một trong bốn mục structure là PRESERVE, tức đề nghị GIỮ nguyên, nên số chỗ cần động tới là 27). Bốn cái có trade-off thật được người dùng chọn hướng trước khi vá. **(1) `bin/giam-dinh.py`** — ràng buộc "không đưa nội dung sách vào ngữ cảnh" trước đó chỉ là lời dặn, eval chỉ quan sát model tuân thủ chứ không có cơ chế nào chặn. Nay engine được bọc sau một script chỉ in ra các khoá số liệu; `text` không còn đường tới stdout. **(2) Ba phép kiểm đường dẫn chuyển vào script**, và hai ca "đường dẫn sai" / "sách hỏng thật" ra hai **mã thoát** khác nhau — ranh giới quyết định có gửi thư sang vai khác hay không giờ là cơ chế, không phải lời dặn. **(3) Trùng tên file thì hỏi, không đoán** — đo được: `~/a/sach.txt` và `~/b/sach.txt` cùng `filename` nhưng khác nội dung, nên nhánh "file dời chỗ" cũ sẽ cập nhật con trỏ sang một cuốn khác rồi giữ nguyên số liệu giám định của cuốn cũ. **(4) Phép kiểm kho chuyển lên trước khi gọi script.** **(5) Nhánh "người học không biết cấu trúc"**: hỏi lại một lần, rồi mặc định `chuoi` với cờ `mac_dinh`. **(6) Tên file thư có hậu tố thời gian** — trước đó gửi lại cùng cuốn lần hai sẽ ghi đè thư cũ. **(7) SKILL.md 7.967 → 5.054 token** (đo bằng tiktoken, không ước bằng ký tự — cách ước cũ sai 40% vì tiếng Việt có dấu): tách `references/dinh-dang.md`, cắt lý lẽ thiết kế về đây.

**Một bug thật lộ ra vì lens skill-quality bắt phải chạy lệnh chứ không chỉ viết ra:** `pip install -r requirements-dev.txt` — lệnh chính skill bảo người dùng gõ — **hỏng trên Windows** với `UnicodeDecodeError`, vì file có comment tiếng Việt có dấu mà pip đọc requirements bằng codec mặc định của hệ (cp1252). Đã vá bằng cách giữ file thuần ASCII, và chạy lại thật trong venv sạch: mã thoát 0, engine import được.

**Cũng phát hiện `truong-mon/SKILL.md` đang nói một điều nay đã sai** — dòng "việc thu nhận/thẩm định sách chưa dựng ở bản này". Đã sửa thành lối dẫn sang `/van-dao:thu-bi-kip`, và thêm một bước cuối Nhánh C nói rõ bước kế tiếp sau khi chỉ điểm được ghi.

**Ba việc không vá, đã ghi mốc ở `deferred-work.md`:** cả ba skill vượt trần token AD-8 (chỉ vá được skill của story này); ràng buộc `text` vẫn không có cách bắt nếu ai đó sửa skill để gọi engine trực tiếp trở lại; và bỏ lỡ auto-trigger vẫn là thất bại im lặng — đã giảm rủi ro bằng description viết theo mẫu câu thật cộng lối dẫn tường minh từ `truong-mon`, chứ chưa chặn được.

## Design Notes

**Hành vi engine — đo bằng lượt chạy thật 2026-08-28 trên đúng API sẽ dùng, trên `book-to-skill 1.4.0 @ 8a2cae6`.** Số hiệu bản này quan trọng: engine là gói cài từ nhánh chính của một repo cá nhân, hình dạng `dict` trả về không phải hợp đồng ổn định. Bản đang dùng đã được **ghim theo commit SHA** trong `van-dao/requirements-dev.txt` (ghim SHA chứ không ghim tag — tag di chuyển được). Đổi bản thì chạy lại eval, đừng giả định bảng dưới còn đúng. Gọi `extract_single_file(Path('art-of-war.epub'), 'text', 'no')`:

| Điều | Giá trị thật |
|---|---|
| Trả về | `dict` — không phải file, không có thư mục tạm nào để đi tìm |
| Thất bại | ném `ExtractionError` (được export ở cấp gói) — bắt được, không phải đoán |
| Nội dung sách | nằm ở khoá **`text`**, 77.852 token cho một cuốn 226 KB |
| Khoá số liệu | `format`, `extraction_method`, `pages`, `pages_label`, `spine_items`, `words`, `estimated_tokens`, `chapters_detected`, `chapters_method`, `chapter_headings_sample`, `has_toc`, `images_dropped` |

**`pages` phải đi kèm `pages_label`.** Cùng cuốn Art of War, ba định dạng cho ba con số khác nhau: EPUB `pages = 23` (thực ra là `spine_items`), TXT `pages = 0`, PDF `pages = 12` (trang thật). Không có nhãn thì "23 trang" là một câu sai nói với người học. Đây cũng là lý do không đọc CLI: `metadata.json` của CLI **không có** `pages_label`.

**Số chương là kết quả của cách rút, không phải thuộc tính của sách.** Cùng cuốn Art of War: EPUB ra 13 chương, TXT ra 15 chương. Trình cho người học thì nói đúng bản chất — "bản này rút ra được ngần này chương" — chứ không phải "sách này có ngần này chương".

**Không có mục lục ≠ sách hỏng.** PDF thử nghiệm cho `chapters_detected = 0`, `has_toc = False`, `chapters_method = 'none'` — mà engine vẫn thành công, chữ vẫn rút ra đủ. Đặc tả đã trả lời sẵn ca này: báo rồi vẫn đi tiếp, người học tự xếp chương ở pha sau. Coi nó là lỗi là chặn nhầm một cuốn sách dùng được.

**Một loại lỗi cho năm kiểu hỏng — phải kiểm trước, không phân loại sau.** Phá thật năm kiểu (file 0 byte, thư mục đội lốt file, EPUB đổi đuôi thành `.pdf`, đuôi `.xyz`, đường dẫn không tồn tại) thì cả năm đều ném đúng một `ExtractionError`; lớp này không có lớp con, không thuộc tính, chỉ khác nhau ở chuỗi thông báo — mà chuỗi không phải hợp đồng ổn định. Nên thứ tự kiểm là phần *thiết kế*, không phải tiểu tiết: file tồn tại → đuôi hợp lệ → mới gọi engine. Bỏ thứ tự đó thì một cú gõ nhầm tên file biến thành một lá thư khai man rằng sách của người học là bản hỏng.

**Hai lỗ nằm trong chính ba phép kiểm đó — đã đo, không suy đoán.** Lỗ thứ nhất hỏng theo chiều buộc tội: `Path('thumuc.epub').exists()` trả `True` cho một **thư mục**, đuôi `.epub` cũng qua, nên nó tới thẳng engine và lĩnh một `ExtractionError` — tức bị gán là bản hỏng. Trên Windows `st_size` của thư mục đo được là 0 nên phép kiểm kích thước tình cờ chặn lại, nhưng đó là hành vi của hệ tệp chứ không phải của phép kiểm, và CI còn chạy trên ubuntu. Nên câu hỏi đúng là `is_file()`, không phải `exists()`. Lỗ thứ hai hỏng theo chiều ngược lại, từ chối oan: `SUPPORTED_EXTENSIONS` chỉ chứa đuôi chữ thường, `'.EPUB' in SUPPORTED_EXTENSIONS` là `False` — trong khi engine rút cuốn `ART.EPUB` ra đủ 58.389 từ, y hệt bản chữ thường. So thẳng `suffix` là đuổi một cuốn sách tốt về; phải `suffix.lower()`.

**Rút chữ nhanh; chi phí đáng lo nằm ở phía sau.** Sách kỹ thuật 514 trang (2,13 MB) rút xong trong **5,1 giây**. Nên câu trong đặc tả về việc "không để đệ tử đợi mười phút" không nói về khâu này — nó nói về các pha xử lý sau. Vì vậy ước chi phí ở giám định phải quy về **khối lượng phải nhai về sau**, lấy `estimated_tokens` làm thước, kèm mốc so sánh thật để con số có nghĩa với người học: sách phổ thông cỡ Art of War ~78K token, sách kỹ thuật 500 trang ~196K token.

**Phép kiểm chuỗi/mạng không có nguồn dữ liệu — nhưng hỏi thẳng cũng sai.** Metadata không có trường nào mô tả cấu trúc, và skill bị cấm đọc `text`, nên không còn đầu vào nào để tự suy. Bằng chứng cho thấy đếm chương không thay được: BABOK trả 11 chương và có mục lục — nhìn metadata thì y hệt một cuốn chuỗi — trong khi chính đặc tả lấy BABOK làm ví dụ điển hình của cấu trúc mạng.

Nhưng hỏi thẳng *"sách này chuỗi hay mạng?"* lại lặp đúng lỗi dự án đã nhận diện chỗ khác: đặc tả nói rõ mạch là **khái niệm của hệ**, người mới không trả lời được, nên nhánh chưa-biết hỏi **vai** trước rồi mới suy ra mạch kèm cờ nguồn. `chuoi`/`mang` cũng là khái niệm của hệ, không khá hơn. Áp đúng khuôn đã có: hỏi một câu người đang cầm cuốn sách trả lời được — *"đọc từ đầu đến cuối, hay tra chỗ nào cần chỗ đó?"* — rồi hệ suy ra và ghi kèm cờ nguồn. Cùng một khuôn ba tầng đã dùng cho gợi ý mạch và mức chắc chắn của chỉ điểm.

**Thư báo bản hỏng hiện là một chiều — gửi được, chưa ai đọc.** `truong-mon/SKILL.md` (Story 1.3) không có bước đọc hộp thư nào; phạm vi story đó không bao gồm. Nên thư `bao_ban_hong` gửi đi sẽ nằm trong hộp thư cho tới khi Trưởng môn biết mở, và **trạng thái `ban_hong` chưa được đặt ở bản này**. Vẫn gửi, vì thư là bản ghi đúng chỗ và đúng khuôn đặc tả — nhưng nói thẳng trong lời thoại với người học rằng phần cập nhật lại chỉ điểm chưa có, thay vì để họ tưởng đã xong.

**Story này không cho người học năng lực mới nào.** Sau giám định, thứ người học nhận được là một bản báo cáo về cuốn sách họ đang cầm — không phải một thứ mới dùng được. Đó là hệ quả có chủ ý của việc tách phạm vi, không phải thiếu sót: thứ story này thật sự giao là **bản ghi giám định + con trỏ tới file** để pha thiết kế sư phạm tiêu thụ. Nói rõ điều này với người học ở cuối luồng, đừng để họ chờ một lộ trình học không tới.

**Đường dẫn tiếng Việt có dấu chạy được — đã verify.** Chạy thật trên `Sách của tôi/Kiểm thử/Binh pháp Tôn Tử.epub` cho kết quả đầy đủ (58.389 từ, 13 chương), không lỗi mã hoá. Với dự án mà người dùng đặt tên thư mục bằng tiếng Việt, đây là điều phải biết chắc chứ không giả định — và cũng có nghĩa skill không cần bước chuẩn hoá hay thoát ký tự nào cho đường dẫn.

**Vì sao dừng ở giám định, chưa phải bí kíp.** Một bí kíp mức thấp nhất vẫn cần mục tiêu, giả định nền, tiêu chí đạt thô, và ít nhất một câu vận dụng — tức phải qua pha thiết kế sư phạm, mà pha đó bắt buộc dừng chờ người dùng sửa-và-duyệt. Không có cách nào tự sinh cho nhanh mà không phá đúng cổng đó.

**Hệ quả cần biết trước:** Epic 1 **chưa đóng** sau story này. Mắt xích "một bí kíp vào kho" — điều kiện để Epic 2 (lộ đồ) bắt đầu — nằm ở mục tiêu đã hoãn, mốc quay lại đã ghi là "ngay sau khi story này đóng".

**Thư báo bản hỏng nằm trong phạm vi, không hoãn.** Bản nháp đầu hoãn nó với lý do "hạ tầng thư chưa dựng". Lý do đó sai: đặc tả nói thẳng hộp thư dùng được cho việc này **không cần cơ chế mới** — nó vốn là chỗ mọi vai gửi và mọi vai đọc — và cho sẵn khuôn JSON của thư. Đây cũng là lý do bản hỏng khác hẳn "không tìm thấy sách": sách vẫn đúng, chỉ bản in sai, nên chỉ điểm giữ nguyên chứ không bị gạch.

**Sách thử là chung, công thức mới là thứ được commit.** `.gitignore` của `van-dao` chặn `*.pdf`/`*.epub` — đúng chủ ý, sách không bao giờ vào repo. Nên fixture chung là một file README ghi nguồn + lệnh lấy về cho cả Windows lẫn POSIX, không ghim checksum (Gutenberg thỉnh thoảng sinh lại file, hash đổi mà nội dung không đổi — ghim hash làm eval gãy vì lý do không liên quan).

## Verification

**Commands:**
- `claude plugin validate van-dao --strict` -- expected: PASS (thêm skill `thu-bi-kip`)
- `python -c "import book_to_skill as b; print(b.extract_single_file, b.ExtractionError)"` -- expected: in ra được cả hai, xác nhận API đặc tả yêu cầu có thật trong bản đã cài

**Manual checks (if no CLI):**
- Đọc `thu-bi-kip/SKILL.md` xác nhận đủ 4 quy ước §12.4, không trích FR/NFR/§ (AD-11), có bước tự tra home-dir
- Đọc `thu-bi-kip/SKILL.md` xác nhận **không có bước nào in hay giữ khoá `text`** — đây là ràng buộc dễ vi phạm nhất, và vi phạm thì nổ ngữ cảnh ngay
- Đọc `thu-bi-kip/SKILL.md` xác nhận đủ **bốn** phép giám định, và nhánh "không có mục lục" đi tiếp chứ không dừng
- Đọc `thu-bi-kip/SKILL.md` xác nhận phép kiểm đường dẫn hỏi `is_file()` (không phải `exists()`) và so đuôi sau khi `.lower()` — hai lỗ đã đo, mỗi lỗ hỏng một chiều: một để thư mục lọt vào rồi bị vu là bản hỏng, một chặn oan sách `.EPUB` hợp lệ
- Đọc `thu-bi-kip/evals/evals.json` xác nhận evidence trích nguyên văn transcript chạy thật trên sách chung, phủ đủ 8 dòng I/O matrix

## Suggested Review Order

**Ranh giới cơ chế — chỗ lời dặn được thay bằng thứ không lách được**

- Điểm vào: chỉ 16 khoá số liệu rời script; `text` không có đường ra
  [`giam-dinh.py:137`](../../../../van-dao/bin/giam-dinh.py#L137)

- Danh sách khoá cho phép, viết tường minh thay vì lọc ngầm
  [`giam-dinh.py:49`](../../../../van-dao/bin/giam-dinh.py#L49)

- Engine in log ra stdout; chuyển sang stderr để stdout chỉ còn JSON
  [`giam-dinh.py:129`](../../../../van-dao/bin/giam-dinh.py#L129)

- Mã thoát tách "đường dẫn sai" khỏi "sách hỏng thật" — quyết định có gửi thư sang vai khác
  [`giam-dinh.py:73`](../../../../van-dao/bin/giam-dinh.py#L73)

**Luồng skill**

- Gọi script, không gọi engine trực tiếp — ràng buộc nằm ở đây
  [`SKILL.md:63`](../../../../van-dao/skills/thu-bi-kip/SKILL.md#L63)

- Kiểm kho trước vì rẻ nhất; chuyển lên bước 1 sau khi chạy eval thật
  [`SKILL.md:54`](../../../../van-dao/skills/thu-bi-kip/SKILL.md#L54)

- Nhánh Đ: từ chối sạch, gửi thư báo, không ghi gì vào kho
  [`SKILL.md:120`](../../../../van-dao/skills/thu-bi-kip/SKILL.md#L120)

- Nhánh E và G tách bằng `is_file()` — hai ca trông giống nhau, xử lý ngược nhau
  [`SKILL.md:134`](../../../../van-dao/skills/thu-bi-kip/SKILL.md#L134)

**Bằng chứng**

- Khoá `text` không bao giờ ra stdout — test khoá lại ràng buộc cốt lõi
  [`test_giam_dinh.py:44`](../../../../van-dao/tests/test_giam_dinh.py#L44)

- Bản hỏng thật ra mã thoát riêng, không lẫn với đường dẫn sai
  [`test_giam_dinh.py:116`](../../../../van-dao/tests/test_giam_dinh.py#L116)

- Thư mục đội lốt file `.epub` không bị coi là sách hỏng
  [`test_giam_dinh.py:83`](../../../../van-dao/tests/test_giam_dinh.py#L83)

- Tám kịch bản chạy thật, phủ 1-1 tám hàng I/O matrix
  [`evals.json`](../../../../van-dao/skills/thu-bi-kip/evals/evals.json)

**Ngoại vi**

- Lược đồ bản ghi kho và thư, tách khỏi SKILL.md để giữ ngân sách token
  [`dinh-dang.md`](../../../../van-dao/skills/thu-bi-kip/references/dinh-dang.md)

- Phơi `ngan_sach_token` cho người dùng chỉnh
  [`customize.toml`](../../../../van-dao/skills/thu-bi-kip/customize.toml)
