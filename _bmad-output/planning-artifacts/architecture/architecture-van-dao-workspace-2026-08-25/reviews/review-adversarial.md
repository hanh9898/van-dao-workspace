# Lens Đối kháng (Adversarial) — ARCHITECTURE-SPINE.md (Vấn Đạo)

Phương pháp: dựng hai đơn vị (component/story) một tầng dưới spine cho cùng một vùng chức năng, mỗi đơn
vị tuân thủ **đúng từng chữ** mọi AD hiện có (AD-1 → AD-7), rồi kiểm xem hai đơn vị đó có buộc phải ra
cùng một hình dạng dữ liệu / cùng một đường mutate hay không. Nếu spine cho phép hai lựa chọn hợp lệ mà
không tương thích nhau, đó là lỗ hổng của spine, không phải lỗi của người viết story sau này. Chỉ đọc trực
tiếp `ARCHITECTURE-SPINE.md` và `docs/VAN-DAO-dac-ta-v1.0.md` (§4, §5.7, §5.9, §13.1, §15); có đối chiếu
nhanh với code đã có (`van-dao/bin/kiem-bi-kip.py`) để lấy tiền lệ thật, không phải suy đoán.

Không sửa spine. Không lặp lại phát hiện của `review-rubric.md` (context-rot budget, AD-8) — đó là lỗ hổng
"chiều bị bỏ sót", còn lens này săn lỗ hổng "hai đơn vị cùng đúng luật nhưng lệch nhau".

---

## Finding 1 — Dấu vân tay lộ đồ: thuật toán, phạm vi hash, tên trường đều chưa fix — **BLOCKING**

**AD liên quan:** AD-6 (dòng 61-65), AD-7 (dòng 67-71), mục Deferred (dòng 194) tự thừa nhận đây là gap.

**Đơn vị A** — story hiện thực FR6 phần "trình duyệt lại": khi người học duyệt lộ đồ, script ghi lại một
"dấu vân tay" của lộ đồ vừa duyệt. A làm theo tiền lệ đã có trong repo — `kiem-bi-kip.py::van_tay()`
(`van-dao/bin/kiem-bi-kip.py:110-115`) băm **toàn bộ byte của file** bằng `sha256:<hex>`. A áp y hệt cách
đó cho `lo-do/<bí kíp>.json`: đọc file thô, sha256 nguyên văn, ghi vào một trường mới, ví dụ
`van_tay_duyet`.

**Đơn vị B** — story hiện thực FR6/FR7 phần "gác trước F0" (script AD-7 dòng 71: "cùng khuôn với
`kiem-bi-kip.py`/`thoai-canh.py`"). B đọc đúng câu AD-5 (dòng 58): Loại 1 là **"lưu nguyên văn"** cấp
**phán quyết/cam kết**, không phải cấp byte-file — nên B băm **nội dung ngữ nghĩa đã canonicalize** (dump
JSON key đã sort, loại field không mang ý nghĩa cam kết như timestamp hiển thị) rồi mới sha256, và đặt tên
trường `dau_van_tay` (khớp thuật ngữ "dấu vân tay" dùng trong văn xuôi AD-7, không phải `van_tay` — tên đó
đã có nghĩa khác, "vân tay file nguồn" ở `bi-kip.schema.md`/`giam-dinh.py` theo §13.1 dòng 1785).

**Vì sao cả hai đều đúng luật:** AD-6 chỉ nói *phải* trình duyệt lại và *phải* có script đối chiếu; AD-7
chỉ nói script đó "cùng khuôn" với hai script kia — không nói khuôn đó gồm băm nguyên file hay băm nội
dung canonicalize, không nói tên trường. Cả A và B đều là "script xác định, không phải Hook, không phải
model tự giác" — đúng chữ AD-4 và AD-7.

**Xung đột thật:** nếu A ghi field lúc duyệt còn B đọc field lúc gác F0 (hai story khác nhau, rất có thể
hai người/hai đợt sprint khác nhau — đúng kịch bản "một tầng dưới spine"), B tìm `dau_van_tay` không thấy
(A ghi `van_tay_duyet`) → gác luôn báo "chưa từng duyệt" dù người học đã duyệt, hoặc ngược lại nếu field
trùng tên nhưng thuật toán khác (A băm byte-file, B băm nội dung canonicalize) thì cùng lộ đồ, cùng lần
duyệt, ra hai chuỗi hash khác nhau — cổng AD-6 sai dương tính ngay lần chạy đầu tiên, không phải edge case.

**AD cần siết:** AD-7 (hoặc một AD-8 riêng nếu muốn tách khỏi "hook boundary") phải cố định: (a) input của
hash là gì — nguyên file hay nội dung đã canonicalize và field nào bị loại trừ; (b) thuật toán + tiền tố
chuỗi (đã có tiền lệ `sha256:<hex>`, nên bắt buộc dùng lại, không để mỗi script tự chọn); (c) tên trường
chính xác trong `lo-do.schema.md`, dùng chung cho cả điểm ghi (lúc duyệt) và điểm đọc (lúc gác F0).

---

## Finding 2 — "Lộ đồ đang dùng" vs "lộ đồ đã duyệt": AD-2 và cây thư mục không nói chúng nằm ở đâu — **BLOCKING**

**AD liên quan:** AD-2 (dòng 37-41, "không sửa tại chỗ"), AD-5 (dòng 58, lộ đồ đã duyệt = Loại 1 bất
biến), AD-6 (dòng 65), AD-7 (dòng 71: đối chiếu "vân tay lộ đồ **đang dùng**" với "vân tay lộ đồ **đã
duyệt**" — hai đối tượng khác nhau). Cây thư mục chỉ khai một dòng: `thu-linh/ lo-do/ · giao-an/ ·
ghi-chep/` (dòng 173) — một file `.json` mỗi bí kíp, không phải `.jsonl`.

**Đơn vị A** — coi `lo-do/<bí kíp>.json` là artifact nội dung (giống `manifest.yaml` của bí kíp), được
ghi đè toàn bộ mỗi lần thư linh sửa lộ đồ; lúc duyệt, A **cập nhật tại chỗ** một trường con
`{"duyet": {"dau_van_tay": "...", "luc": "..."}}` ngay trong chính file đó. A tự cho là hợp luật AD-2 vì
đọc chữ "không có bảng/`.json` **trạng thái hiện tại**" — lo-do.json không phải "trạng thái", nó là nội
dung sư phạm (giáo án lộ đồ), nên sửa tại chỗ không phạm AD-2.

**Đơn vị B** — đọc đúng AD-2 theo tinh thần "mọi đổi trạng thái = thêm dòng vào log", và đọc AD-5 "lộ đồ đã
duyệt... không tái sinh" nghĩa đen là **không được ghi đè** bản đã duyệt. B giữ `lo-do/<bí kíp>.json` là
bản **đang soạn** (ghi đè tự do, không tính Loại 1), và tách một log riêng — ví dụ thêm dòng vào
`truong-mon/lo-trinh.jsonl` (đã có sẵn trong cây, do Trưởng môn ghi) hoặc một file mới
`thu-linh/lo-do-duyet.jsonl` — mỗi lần duyệt là một dòng bất biến `{"bi_kip": "...", "dau_van_tay": "...",
"luc": "..."}`. "Đã duyệt hiện tại" = dòng gần nhất, đúng chữ AD-2.

**Vì sao cả hai đều đúng luật:** spine không định nghĩa `lo-do/*.json` là "trạng thái" hay "nội dung" —
hai khái niệm AD-2 dùng để phân biệt "sửa tại chỗ được" và "không được" chưa có ranh giới rõ cho đúng
artifact này. AD-5 nói "lộ đồ đã duyệt" là Loại 1 nhưng không nói bản ghi Loại 1 đó sống trong cùng file
với bản đang soạn hay ở một chỗ tách biệt.

**Xung đột thật:** script gác F0 của AD-7 (Finding 1) phải biết đọc "vân tay đã duyệt" ở đâu. Nếu script
đó được viết theo giả định của B (tìm dòng gần nhất trong `lo-do-duyet.jsonl`) nhưng thư linh thực ra được
xây theo A (field lồng trong `lo-do/<bí kíp>.json`), cổng không đọc được gì — hoặc tệ hơn, đọc **nhầm**
bản đang soạn làm bản đã duyệt vì cả hai nằm chung một file, khiến AD-6 mất tác dụng hoàn toàn (script luôn
thấy "đang dùng" == "đã duyệt" vì chúng là cùng một trường vừa bị A ghi đè).

**AD cần siết:** AD-2 hoặc AD-6 phải nói rõ: bản "đã duyệt" của lộ đồ là một **artifact tách biệt và bất
biến** (không sống chung field/file với bản đang soạn), và chỉ rõ nó là snapshot (Loại 1 đúng nghĩa
"lưu nguyên văn") hay là dòng log append-only — chọn một, khai trong `lo-do.schema.md`.

---

## Finding 3 — Bảng "Consistency Conventions" hứa "error shapes, envelopes" nhưng không có nội dung nào cho nó — **CONCERN**

**AD liên quan:** bảng Consistency Conventions (dòng 116-120), hàng "Data & formats (ids, dates, **error
shapes, envelopes**)" (dòng 119); liên quan AD-4 (script) và AD-7 (script gác + hook).

**Bằng chứng:** đọc đúng nội dung hàng 119 — nó chỉ nói về *định dạng file* (`.jsonl` chỉ-ghi-thêm,
`.yaml`/`.json` theo schema, `thu.schema.md` + `kiem-thu.py`/hook `SubagentStop`). Không có một câu nào
định nghĩa hình dạng lỗi hay envelope chung cho **script** (không phải thư liên vai). Đối chiếu tiền lệ
thật đã có trong repo: `kiem-bi-kip.py` tự đặt ra quy ước riêng — ba mức `loi`/`canh_bao`/`ghi_chu`, mỗi
mục `{"ma", "thong_diep", "o"}`, thoát mã 0 = sạch, 1 = "có lỗi" (kể cả cảnh báo không chặn), 2 = "không
chạy được". Đây là quy ước **của riêng file đó**, không phải quy ước tầng spine — không AD nào bắt các
script khác (`thoai-canh.py`, hay script gác vân tay lộ đồ ở Finding 1) phải theo cùng khuôn.

**Đơn vị A** — story viết `thoai-canh.py` (hạ bậc khi định lại mà không có căn cứ mới, §13.1 #25). Hạ bậc
là kết quả **bình thường**, không phải lỗi — A cho thoát mã luôn là 0, và trả field
`{"ha_bac": true/false, "ly_do": "..."}` phẳng, không có `loi`/`canh_bao`.

**Đơn vị B** — story viết script gác F0 của Finding 1, sao chép nguyên khuôn `kiem-bi-kip.py` vì AD-7 dòng
71 nói "cùng khuôn với `kiem-bi-kip.py`/`thoai-canh.py`" — B hiểu "cùng khuôn" là cùng cấu trúc
`loi`/`canh_bao`/`ghi_chu` + thoát mã 1 khi vân tay lệch (xếp "lệch vân tay" vào `loi`, giống cách
`kiem-bi-kip.py` xếp "yaml hỏng" vào `loi`).

**Vì sao cả hai đều đúng luật:** "cùng khuôn" (AD-7 dòng 71) không định nghĩa được — không rõ là cùng
*giao diện CLI/thoát mã*, hay chỉ cùng *tinh thần script-xác-định-không-model*. Cả A và B đều tự nhận là
tuân thủ.

**Xung đột thật:** một wrapper gọi-script chung trong `thu-linh` SKILL.md (nếu có, để tránh lặp code gọi
script ở nhiều bước) sẽ phải case-by-case: thoát mã 1 của B nghĩa là "chặn F0, phải duyệt lại", còn thoát
mã 1 không tồn tại ở A (0 luôn là "đọc field mà biết") — hoặc nếu B học theo A và dùng thoát mã 0 cho
"lệch vân tay" (coi đó cũng là kết quả bình thường cần đọc field), thì bất kỳ đoạn gọi script generic nào
kiểm tra `if exit_code != 0: chặn` sẽ **bỏ lọt** đúng tình huống AD-6 cần chặn nhất.

**AD cần siết:** thêm một dòng cụ thể vào bảng Consistency Conventions (hoặc một AD mới nếu muốn tách khỏi
Data&Formats): cố định thoát mã cho *mọi* script Bậc 1-3 (ví dụ 0 = không cần hành động thêm, 1 = cần
hành động của người gọi — không phân biệt "lỗi" hay "cần duyệt lại", 2 = không chạy được), và cố định tên
ba mức severity + shape JSON dùng chung, không để mỗi script tự đặt lại như `kiem-bi-kip.py` đang làm.

---

## Finding 4 — AD-5 gộp 2 loại từ 3 loại của đặc tả §5.9, đánh rơi "Loại 2 — sinh tại chỗ, KHÔNG lưu" — **BLOCKING**

**AD liên quan:** AD-5 (dòng 55-59) đối chiếu đặc tả §5.9 "Ba loại" (docs/VAN-DAO-dac-ta-v1.0.md dòng
668-687).

**Bằng chứng đối chiếu trực tiếp:**

| | Đặc tả §5.9 | Spine AD-5 |
|---|---|---|
| Loại 1 | Phán quyết & cam kết — lưu nguyên văn | Loại 1 — lưu nguyên văn, không tái sinh (giữ nguyên) |
| Loại 2 | **Diễn giải — sinh tại chỗ, KHÔNG lưu** (lời giảng, ví dụ, câu hỏi dẫn dắt...) | **— không xuất hiện —** |
| Loại 3 | Dẫn xuất — cache, luôn dựng lại được | Đổi tên thành "**Loại 2**" — cache như `ban-do.json` |

Spine không nhắc một chữ nào tới nhóm "sinh tại chỗ, không lưu" — nhóm mà chính đặc tả nhấn mạnh "**lưu
chúng là có hại**, không chỉ thừa" (dòng 680). AD-5 chỉ còn hai nhãn "Loại 1" / "Loại 2", và "Loại 2" của
spine trùng số với "Loại 2" của đặc tả nhưng mang **nghĩa của Loại 3 đặc tả**.

**Đơn vị A** — story phân loại các trường ghi trong `thu-linh/giao-an/` và `thu-linh/ghi-chep/`, chỉ đọc
spine (đúng theo scope một-tầng-dưới, không bắt buộc đọc lại toàn đặc tả). Thấy AD-5 chỉ có hai loại: cam
kết (lưu nguyên văn) hoặc cache (xoá-dựng-lại-được). Sự kiện `{"buoc":3,"cach":"vi-du-A","ket_qua":
"van_vap"}` (đặc tả dòng 693, §5.9 "Giáo án tách làm hai") không có nguồn nào để "dựng lại" nếu xoá — A xếp
nó vào **Loại 1** (đúng), nhưng phần "lời giảng" thực tế thư linh sinh ra ở mỗi lượt, A không có nhãn nào
khác ngoài hai cái đã cho — vì "Loại 2 = cache dựng lại được" không khớp ("dựng lại từ đâu, không có
input"), A quyết định **không viết ra artifact nào cho lời giảng cả**, đúng may mắn — nhưng chỉ vì A tự suy
luận, không vì AD-5 nói rõ.

**Đơn vị B** — story khác (ví dụ viết `giam-dinh.py` phần trích worked example, hoặc F5 "giảng lại bằng
biểu diễn khác" §5.9) cũng chỉ đọc spine, cũng thấy hai loại, nhưng suy luận ngược: "không lưu nguyên văn,
không ai đối chiếu ngược field cụ thể này (nó là văn bản giảng)" → **không phải Loại 1** → theo tiêu chí
loại-trừ duy nhất còn lại trong AD-5, nó "phải là Loại 2 = cache". B viết cache file
`thu-linh/giao-an/<bí kíp>/<chương>-loi-giang.json` để "tránh sinh lại tốn token", có nút xoá/dựng-lại kiểu
`ban-do.py`. Đây trực tiếp là hành vi đặc tả cấm ("khoá thư linh vào cách giảng cũ và phá F5" — dòng 680),
nhưng B **tuân thủ đúng chữ AD-5** vì AD-5 không hề nói "loại thứ ba: đừng lưu gì cả".

**Vì sao cả hai đều đúng luật:** AD-5 chỉ cho hai nhãn và một phép loại trừ nhị phân ("cam kết" hoặc
"cache"); không có nhãn thứ ba cho "không lưu gì hết". Với đúng hai lựa chọn, hai người có quyền quyết
khác nhau cho cùng một loại artifact (nội dung diễn giải, sinh ra rồi biến mất).

**Xung đột thật:** A và B cùng đọc spine, cùng "đúng luật", nhưng ra hai hệ quả đối lập cho artifact giống
hệt nhau — một bên không ghi gì, một bên ghi một file cache. Nếu hai story này chạm cùng một vùng (ví dụ
cùng làm việc trên `thu-linh/giao-an/`), việc B tạo ra sẽ vi phạm AD-3 kiểu "artifact mồ côi" (ai chịu
trách nhiệm xoá cache lời giảng khi nó khoá style cũ?) mà không AD nào bắt phải xoá, vì AD-5 gọi nó là
"cache, xoá lúc nào cũng an toàn" — sai: xoá thì an toàn, nhưng **có nó** đã là hại, không phải chuyện
"xoá được hay không".

**AD cần siết:** khôi phục ba loại của đặc tả §5.9 vào AD-5 (không chỉ hai), đặt tên khớp với đặc tả để
tránh trùng số ("Loại 2" của spine hiện đang là "Loại 3" của đặc tả) — nêu rõ nhóm "sinh tại chỗ, không
lưu" là loại **bắt buộc không ghi artifact**, khác về chất với "cache có thể xoá". Nên cũng sửa Capability
Map dòng 184 (hàng "4.2 Dạy") — hiện chỉ ghi AD-1, AD-2, AD-6, AD-7, không có AD-5 — dù `thu-linh` chính là
nơi phân định giáo án/lời giảng theo Ba loại này.

---

## Finding 5 — `tang-kinh/**` được Bind ở AD-3 nhưng vắng mặt trong chính cây thư mục của spine — **CONCERN**

**AD liên quan:** AD-3 (dòng 43-47): "**Binds:** `truong-mon/**`, `thu-linh/**`, `truong-lao/**`,
`tang-kinh/**`, `chu-giai/**`, `ban-giao/**`". Đối chiếu Cây thư mục dữ liệu người học (dòng 167-177):
liệt kê `bi-kip/`, `truong-mon/`, `thu-linh/`, `truong-lao/`, `chu-giai/`, `ban-giao/` — **không có
`tang-kinh/`**. Sơ đồ hướng phụ thuộc của spine (dòng 75-110) cũng không vẽ cạnh ghi nào vào vùng
`tang-kinh` (chỉ có `TK -->|"bí kíp vào kho"| TM`). Đặc tả gốc thì có: §4.3 dòng 394
(`VTK2[("tang-kinh/<br/>nháp pha 2")]`, ghi bởi Tàng kinh trưởng lão) và §15 dòng 1923
(`tang-kinh/ nhap-dang-do/<id>.json — nháp pha 2, tiếp được ở phiên sau`).

**Đơn vị A** — story hiện thực "Pha 2 lưu được giữa các lượt" (đúng máy trạng thái ở spine dòng 137-138,
`Pha1 --> Pha2 --> Pha3`, ghi chú dòng 152 "nháp Pha 2 lưu được giữa các lượt"). A build **chỉ từ chính
spine** (đúng phạm vi "một tầng dưới spine" mà lens này giả định) — không thấy `tang-kinh/` trong cây thư
mục của spine, nên đặt nháp pha 2 ở nơi khác hợp lý theo chính cây spine đưa ra: một thư mục con dưới
`ban-giao/` (region đã biết, đa chủ theo `.pham-vi.json`) — ví dụ `ban-giao/tang-kinh/<id>.json` — hoặc
dưới `bi-kip/` (đã có trong cây spine, chủ là Tàng kinh trưởng lão). Cả hai lựa chọn đều **không mâu thuẫn
với bất kỳ dòng nào trong spine**, vì spine không hề nhắc "nháp pha 2 sống ở đâu".

**Đơn vị B** — story khác, viết bởi người có đọc chéo đặc tả §15 (rất hợp lý vì spine dòng 14 liệt kê
`docs/VAN-DAO-dac-ta-v1.0.md` là nguồn ràng buộc), đặt đúng theo đặc tả:
`~/.vandao/tang-kinh/nhap-dang-do/<id>.json`, một vùng **ngang hàng** với `truong-mon/`, `thu-linh/`, chủ
ghi là Tàng kinh trưởng lão — và trích đúng AD-3 dòng 45 để biện minh, vì `tang-kinh/**` **có tên trong
Binds**.

**Vì sao cả hai đều đúng luật:** AD-3's Binds line nói `tang-kinh/**` phải có "đúng một chủ ghi" — cả A và
B đều cho nó đúng một chủ (Tàng kinh trưởng lão). Xung đột không nằm ở *ai ghi* mà ở *ghi vào đâu* — spine
tự mâu thuẫn nội bộ giữa AD-3's Binds (nhắc tên `tang-kinh/**`) và Structural Seed (không vẽ nó ra), nên
"một tầng dưới spine, đọc đúng spine" không đủ để xác định vị trí thật của vùng này.

**Xung đột thật:** nếu A viết `giam-dinh.py`/`thu-bi-kip` skill ghi nháp vào `ban-giao/tang-kinh/`, còn
script/hook nào đó dò "nháp pha 2 còn dở" lúc `SessionStart` (`nap-ho-so.sh`, đã liệt trong Bậc 1-3, có
nhiệm vụ nạp "lộ đồ đang dở" — tương tự phải biết nháp pha 2 tồn tại để tiếp tục Pha 2) lại tìm ở
`~/.vandao/tang-kinh/` theo B, nó sẽ không thấy gì — người học mất nháp giữa các lượt, đúng thất bại mà
chính máy trạng thái ở spine (dòng 152) cam kết không được xảy ra ("nháp Pha 2 lưu được giữa các lượt").

**AD cần siết:** thêm `tang-kinh/` vào Cây thư mục dữ liệu người học ở Structural Seed (dòng 167-177) —
không cần đổi AD-3, chỉ cần Structural Seed không tự mâu thuẫn với Binds line của chính nó. Đây là fix rẻ
(một dòng), nhưng đáng nêu vì nó là bằng chứng "một tầng dưới spine" có thể lệch nhau mà không cần đọc sai
gì cả — chỉ cần một người dừng lại ở spine, một người đọc thêm đặc tả.

---

## Verdict

**BLOCKING.** Ba trong năm lỗ hổng (Finding 1, 2, 4) nằm ngay trên đường thực thi cốt lõi mà spine tự nhận
là quan trọng nhất — AD-6/AD-7 (lộ đồ là hợp đồng sống) và AD-5 (ranh giới lưu/không-lưu) — và cả ba đều
cho phép hai đơn vị "đúng luật" tạo ra dữ liệu không đọc được lẫn nhau hoặc hại đúng thứ AD-5/AD-6 muốn
ngăn. Finding 3 và 5 là CONCERN, rẻ để sửa nhưng không nên bỏ qua vì chúng lặp lại đúng khuôn mẫu: spine
đủ *nêu tên* các đối tượng cần đồng bộ (dấu vân tay, envelope lỗi, `tang-kinh/`) nhưng chưa *cố định hình
dạng* của chúng — đúng khoảng trống mà "đúng luật nhưng lệch nhau" sống trong đó. Khuyến nghị: khoá thuật
toán/tên trường dấu vân tay + vị trí bản "đã duyệt" (AD-7 hoặc AD-8 mới), khôi phục ba loại dữ liệu của
đặc tả §5.9 vào AD-5, thêm một dòng envelope-lỗi-chung vào bảng Consistency Conventions, và thêm
`tang-kinh/` vào Structural Seed — trước khi cho phép hai epic độc lập cùng bắt đầu viết story trên các
vùng này.
