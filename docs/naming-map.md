# Naming map — Vietnamese to English

**Status:** danh pháp đã chốt đủ để bắt đầu đổi tên. Chưa qua vòng review — xem mốc trong `review-log.md`.

Chốt 2026-08-31: hệ thống chuyển sang tiếng Anh toàn bộ — mã, tên file, định danh, tài liệu, skill,
agent. Thế giới quan tiên hiệp giữ nguyên; chỉ ngôn ngữ diễn đạt đổi. Tiếng Việt còn lại đúng một
chỗ: `communication_language` trong config, tức thứ tiếng hệ *nói chuyện* với người dùng.

Tài liệu này tồn tại vì một lý do hẹp: **cùng một khái niệm phải ra cùng một từ ở mọi nơi.** Dịch
rải rác qua nhiều lượt thì `bí kíp` sẽ thành một từ ở chỗ này, một từ khác ở chỗ kia — và không có
cách nào sửa lại sau, vì lúc đó không ai còn biết hai từ ấy từng là một.

---

## 1 · Thuật ngữ hệ — thế giới quan tiên hiệp

Nguyên tắc chọn từ: dùng từ vựng **cultivation fiction** đã phổ biến trong bản dịch tiếng Anh, để
người đọc có tiếp xúc thể loại nhận ra ngay. Không dùng pinyin, không dùng từ trung tính vô sắc.

| Tiếng Việt | Hán tự | Tiếng Anh | Ghi chú |
|---|---|---|---|
| bí kíp | 秘笈 | **scripture** | Cuốn sách được nạp vào hệ. Không dùng `book` (bận nghĩa kỹ thuật) cũng không dùng `manual` — `manual` trong phần mềm nghĩa là sách hướng dẫn dùng sản phẩm, nên `manuals/` sẽ bị đọc thành docs của plugin. Đã tra: `scripture` không phải thuật ngữ kỹ thuật nào. Có mang liên tưởng tôn giáo (tra ra gần như toàn phần mềm Kinh Thánh) — chấp nhận, vì trong ngữ cảnh môn phái và Tàng kinh các thì nghĩa "kinh thư" là đúng thứ ta muốn |
| mạch | 脈 | **meridian** | Nhánh tri thức chạy xuyên nhiều bí kíp |
| chỉ điểm | 指點 | **counsel** | Lời chỉ của Trưởng môn cho đệ tử. Không dùng `pointer` — trong một dự án Python, `pointers.jsonl` đọc như con trỏ. `counsel` là danh từ không đếm được, dùng nguyên dạng cho cả số nhiều |
| Trưởng môn | 掌門 | **Sect Master** | Vai điều phối |
| trưởng lão | 長老 | **Elder** | Vai chấm bài |
| đệ tử | 弟子 | **disciple** | Người học |
| nhập môn | 入門 | **initiation** | Nghi thức gia nhập |
| tàng kinh (các) | 藏經閣 | **Scripture Hall** | Nơi cất bí kíp. Cùng gốc từ với `scripture` là cố ý, không phải trùng lặp — tàng kinh các đúng nghĩa là nơi chứa kinh thư |
| cảnh giới | 境界 | **realm** | Bậc tu vi |
| tâm pháp | 心法 | **heart method** | Nguyên lý cốt lõi của một chương |
| công pháp | 功法 | **technique** | Cách vận dụng |
| khảo thí | 考試 | **ordeal** | Bài kiểm tra. Không dùng `exam` (mất màu) cũng không dùng `trial` — "start a trial" trong phần mềm đọc như bản dùng thử |
| nghiệm công | 驗功 | **proving** | Chứng minh đã lĩnh hội |
| Phúc Khảo Sứ | 覆考使 | **Re-examiner** | Vai chấm lại độc lập |
| hạ sơn | 下山 | **descend the mountain** | Rời môn phái, hoàn thành |
| giám định | 鑑定 | **appraisal** | Thẩm định bản sách trước khi nhận |
| bế quan | 閉關 | **seclusion** | Vào kín học một bí kíp. Skill chưa dựng — đặt tên trước để lệnh `/wayfarer:seclusion` không phải đổi sau |

## 2 · Danh từ kỹ thuật — không mang màu

| Tiếng Việt | Tiếng Anh |
|---|---|
| khối sư phạm | pedagogy block |
| khuôn câu hỏi | question template |
| hồ sơ | profile |
| thư | letter |
| bàn giao | handover |
| sổ tay | journal |
| xương sống | spine |
| dấu hiệu | signal |
| trạng thái | status |
| đường dẫn | path |
| phạm vi đọc | read scope |
| ngân sách token | token budget |
| tiêu chí đạt | pass criteria |
| sai lầm phổ biến | common mistakes |
| mục tiêu | objective |
| phụ thuộc | depends_on |
| nhận định | assessment |
| suy đoán | inference |
| giả định nền | baseline assumption |
| hết hiệu lực | expired |
| dư thừa | redundant |
| độ phức tạp | complexity |

## 2.1 · Khoá data contract — `bi-kip.schema.md`

Đây là phần **rủi ro nhất** của cả đợt refactor: khoá ở đây xuất hiện trong file bí kíp mà người dùng
tạo ra, nên đổi khoá là đổi định dạng dữ liệu, không phải đổi tên biến. Khoá glossary ở đây trước khi
sửa dòng đầu tiên (§7.4).

**Cấp quyển — `manifest.yaml`**

| Cũ | Mới | | Cũ | Mới |
|---|---|---|---|---|
| `loai` | `kind` | | `tieu_de` | `title` |
| `cau_truc` | `structure` | | `tac_gia` | `author` |
| `mach` | `meridians` *(list)* | | `nam` | `year` |
| `vai` | `roles` *(list)* | | `nguon_file` | `source_file` |
| `xuong_song` | `spine` *(list)* | | `van_tay` | `fingerprint` |
| `chi_nhanh` | `branches` *(list)* | | `duong_dan` | `path` |
| `khao_thi_quyen` | `volume_ordeal` | | `ha_son_sau` | `descend_after` *(list số chương)* |
| `nguon` *(cấp quyển)* | `source` | | `chuong` | `chapter` *(số)* · `chapters` *(list)* |

**Cấp chương — `chuong/NN.yaml`**

| Cũ | Mới | | Cũ | Mới |
|---|---|---|---|---|
| `muc_tieu` | `objective` | | `tieu_chi_dat` | `pass_criteria` |
| `gia_dinh_nen` | `baseline_assumption` | | `khuon_cau_hoi` | `question_templates` *(list)* |
| `phu_thuoc` | `depends_on` | | `khuon` | `template` |
| `worked_example` | *(giữ)* | | `do_tieu_chi` | `covers_criteria` |
| `tro_toi` | `points_to` | | `bai_luyen_lap` | `drill` |
| `sai_lam_pho_bien` | `common_mistakes` | | `gian_giao` | `scaffold` |
| `dau_hieu` | `signal` | | `do_phuc_tap` | `complexity` |
| `quan_niem_sai` | `misconception` | | `lop_nhiem_vu` | `task_class` |
| `cach_chua` | `remedy` | | `du_thua` | `redundant` |
| `nguon` *(trong `common_mistakes`)* | `origin` | | `bo_tham_so` | `parameter_set` |
| `mo_ta` | `description` | | `canh_gioi_vao` / `canh_gioi_ra` | `realm_required` / `realm_granted` |

`do_tieu_chi` → `covers_criteria` chứ không dịch sát chữ: nó là danh sách id tiêu chí mà câu hỏi phủ,
và tên tiếng Anh phải nói ra quan hệ đó — nếu không thì `do_tieu_chi: []` ở câu khởi động trông như
một trường bỏ trống chứ không phải một tuyên bố "câu này cố ý không làm bằng chứng".

**Enum — giá trị, không phải khoá**

| Trường | Cũ | Mới |
|---|---|---|
| `kind` | `bi-kip` · `tan-quyen` | `scripture` · `fragment` |
| `structure` | `chuoi` · `mang` | `chain` · `web` |
| `realm_required` / `realm_granted` | `luyen-khi` · `truc-co` · `ket-dan` · `nguyen-anh` · `hoa-than` | `qi-refining` · `foundation` · `core-formation` · `nascent-soul` · `soul-transformation` |
| `complexity` | `thap` · `trung` · `cao` | `low` · `medium` · `high` |
| `scaffold` | `day` · `vua` · `mong` | `heavy` · `medium` · `light` |
| `loai` câu hỏi | `tai_hien` · `van_dung` · `phan_tich` | `recall` · `apply` · `analyze` |
| `bloom` | `nho` · `hieu` · `ap_dung` · `phan_tich` · `danh_gia` · `sang_tao` | `remember` · `understand` · `apply` · `analyze` · `evaluate` · `create` |
| `origin` | `nguoi` · `sach` · `suy_doan` | `person` · `book` · `inference` |

**Bốn khoá giữ nguyên, không dịch:** `id`, `schema`, `worked_example`, `bloom`. Nói ra vì im lặng ở
đây đọc như "chưa xét tới".

**Hai từ Việt mang hai nghĩa khác nhau — chỗ dễ dịch hỏng nhất, và bản đầu của bảng này đã mắc.**

- `nguon` cấp quyển là **object** metadata sách gốc (`title`/`author`/`year`) → `source`. `nguon` trong
  `common_mistakes` là **enum xuất xứ** của một sai lầm — ai nói ra điều đó → `origin`. Gộp cả hai
  thành `source` là đúng thứ bảng này tồn tại để chống.
- `loai` cấp quyển (`scripture`/`fragment`) và `loai` câu hỏi (`recall`/`apply`/`analyze`) đều thành
  `kind`. Dùng chung một từ được, vì chúng lồng trong hai object khác nhau nên không bao giờ va nhau —
  nhưng phải nói ra, chứ không để người dịch lô sau tự quyết.

Hai chỗ đáng nói:

- **Ngũ cảnh giới** dùng đúng bản dịch đã phổ biến trong cultivation fiction tiếng Anh (Luyện Khí ·
  Trúc Cơ · Kết Đan · Nguyên Anh · Hoá Thần). Đây là chỗ quyết định "cultivation fiction, không phải
  pinyin" ở §1 trả cổ tức: người đọc thể loại nhận ra thang bậc ngay mà không cần chú giải.
- **`bloom`** vốn là thang Bloom, gốc tiếng Anh. Sáu bậc trả về đúng tên gốc — đây là dịch *ngược lại*
  về nguyên bản, không phải đặt từ mới.

`source: book` là chỗ duy nhất `book` được dùng, và nó đúng: ở đây `sach` nghĩa là **cuốn sách vật lý
gốc**, không phải bí kíp trong hệ. Bí kíp vẫn là `scripture` (§1).

## 2.2 · Định danh nội bộ của script

Khác §2.1 ở một điểm quyết định: đây **không** phải data contract. Đổi chúng không đụng file người
dùng, nên rủi ro thấp hơn hẳn — nhưng vẫn phải vào bảng, vì hai script sẽ được dịch ở hai lô khác nhau.

**Hàm**

| Cũ | Mới | | Cũ | Mới |
|---|---|---|---|---|
| `doc_yaml` | `read_yaml` | | `kiem_mot` | `check_one` |
| `kiem_manifest` | `check_manifest` | | `kiem_enum` | `check_enum` |
| `kiem_khoi_su_pham` | `check_pedagogy_block` | | `kiem_do_thi` | `check_graph` |
| `kiem_truong_bat_buoc` | `check_required_fields` | | `kiem_khao_thi` | `check_ordeal` |
| `van_tay` | `fingerprint` | | `in_text` | `print_report` |
| `ra` | `emit` | | | |

**Hằng**

| Cũ | Mới | | Cũ | Mới |
|---|---|---|---|---|
| `TRUONG_QUYEN` | `VOLUME_FIELDS` | | `CANH_GIOI` | `REALMS` |
| `TRUONG_BI_KIP` | `SCRIPTURE_FIELDS` | | `DO_PHUC_TAP` | `COMPLEXITY` |
| `TRUONG_SU_PHAM` | `PEDAGOGY_FIELDS` | | `GIAN_GIAO` | `SCAFFOLD` |
| `CHO_PHEP_RONG` | `MAY_BE_EMPTY` | | `LOAI_CAU_HOI` | `QUESTION_KINDS` |
| `KHOA_SO_LIEU` | `METRIC_KEYS` | | `ORIGIN_MISTAKE` | `MISTAKE_ORIGINS` |
| `BIEU` | `LABELS` | | `BLOOM_TINH_BANG_CHUNG` | `BLOOM_COUNTS_AS_EVIDENCE` |
| `SO_TIEU_DE_MAU` | `SAMPLE_TITLE_COUNT` | | `API` · `SCHEMA` · `BLOOM` | *(giữ)* |

**Khoá đầu ra JSON** — script in ra cho skill đọc, nên đây là contract giữa script và skill

| Cũ | Mới | | Cũ | Mới |
|---|---|---|---|---|
| `trang_thai` | `status` | | `ket_qua` | `result` |
| `loi` | `errors` | | `canh_bao` | `warnings` |
| `ghi_chu` | `notes` | | `thong_diep` | `message` |
| `ma` | `code` | | `o` | `where` |
| `dat` | `passed` | | `so_lieu` | `metrics` |
| `bi_kip` | `scripture` | | `duoi_nhan_duoc` | `accepted_extensions` |

**Khoá đầu ra riêng của `giam-dinh.py`** — truyền vào `emit()` dưới dạng keyword argument rồi thành
khoá JSON qua `**kwargs`, nên chúng *trông như* biến nội bộ mà thật ra là contract.

| Cũ | Mới | | Cũ | Mới |
|---|---|---|---|---|
| `duong_dan` | `path` | | `cach_cai` | `install_command` |
| `so_lieu` | `metrics` | | `duoi` | `extension` |
| `thong_diep` | `message` | | `duoi_nhan_duoc` | `accepted_extensions` |

**Giá trị của `status`** — skill phân nhánh theo mã thoát, nhưng vẫn hiển thị và ghi lại giá trị này

| Cũ | Mới |
|---|---|
| `ok` | *(giữ)* |
| `thieu_tham_so` | `missing_argument` |
| `engine_chua_cai` | `engine_not_installed` |
| `khong_phai_file` | `not_a_file` |
| `duoi_khong_ho_tro` | `unsupported_extension` |
| `file_rong` | `empty_file` |
| `khong_rut_duoc_chu` | `extraction_failed` |

Khoá đầu ra là **contract giữa script và skill**, không phải biến nội bộ: SKILL.md đọc chúng theo tên.
Đổi ở đây thì mọi chỗ trong SKILL.md nhắc tới chúng phải đổi cùng lô — nếu không, skill đọc một khoá
không còn tồn tại và im lặng nhận `None`.

## 2.3 · Khoá `chi-diem.jsonl` — contract vùng Trưởng môn

Contract thứ ba, và là cái dễ bỏ sót nhất: nó **không có file schema riêng**. Định nghĩa nằm trong mục
"Định dạng file" của `truong-mon/SKILL.md`, nên quét schema không thấy nó. Áp cho cả
`chi-diem.jsonl` lẫn `chi-diem-hong.jsonl`.

| Cũ | Mới | | Cũ | Mới |
|---|---|---|---|---|
| `ten` | `title` | | `muc_chac_chan` | `confidence` |
| `tac_gia` | `author` | | `trang_thai` | `status` |
| `nam_an_ban` | `published_year` | | `ghi_luc` | `logged_at` |
| `loai` | `kind` | | `id` | *(giữ)* |
| `vi_sao` | `rationale` | | | |

**Enum**

| Trường | Cũ | Mới |
|---|---|---|
| `kind` | `cong_phap` · `tam_phap` | `technique` · `heart-method` |
| `status` | `dang_treo` · `khong_thay` · `het_hieu_luc` | `pending` · `not_found` · `expired` |
| `confidence` | `suy_doan` | `inference` |

**`trang_thai` xuất hiện ở hai contract khác nhau** — khoá đầu ra JSON của script giám định (§2.2) và
khoá của `chi-diem.jsonl` ở đây. Cả hai đều thành `status`, nên không va nhau; nhưng chúng là hai
contract độc lập và **đổi cái này không tự động đúng cho cái kia**. Ghi ra vì bản thân việc tưởng
chúng là một đã suýt làm lô 2b chạy sai.

`loai` giờ là từ thứ ba mang nghĩa khác nhau (loại quyển · loại câu hỏi · loại chỉ điểm), cả ba đều
thành `kind`. Vẫn không va nhau vì ba object khác nhau — nhưng đây là dấu hiệu `loai` là từ quá chung
trong bản gốc, chứ không phải bản dịch có vấn đề.

## 2.4 · Tên file và thư mục trong `van-dao/`

| Cũ | Mới |
|---|---|
| `skills/nhap-mon/` | `skills/initiation/` |
| `skills/nhap-mon-ky/` | `skills/initiation-record/` |
| `skills/thu-bi-kip/` | `skills/scripture-intake/` |
| `skills/truong-mon/` | `skills/sect-master/` |
| `skills/*/references/dinh-dang.md` | `skills/*/references/format.md` |
| `bin/giam-dinh.py` | `bin/appraise.py` |
| `bin/kiem-bi-kip.py` | `bin/validate-scripture.py` |
| `tham-chieu/` | `reference/` |
| `tham-chieu/bi-kip.schema.md` | `reference/scripture.schema.md` |
| `tests/test_giam_dinh.py` | `tests/test_appraise.py` |
| `tests/test_kiem_bi_kip.py` | `tests/test_validate_scripture.py` |
| `tests/fixtures/kiem-thu-dac-ta/` | `tests/fixtures/spec-based-testing/` |
| `tests/fixtures/sach-loi/` | `tests/fixtures/broken-scripture/` |
| `tests/fixtures/tan-quyen-mau/` | `tests/fixtures/fragment-sample/` |
| `tests/fixtures/sach-thu/` | `tests/fixtures/sample-books/` |
| `tests/fixtures/sach-gia.txt` | `tests/fixtures/fake-book.txt` |

Tên thư mục skill **là thứ người dùng gõ**: `/van-dao:thu-bi-kip` thành `/wayfarer:scripture-intake`.
Đây là chỗ đợt refactor chạm vào giao diện, không chỉ nội bộ — mọi eval nhắc lệnh cũ sẽ sai và phải
chạy lại, không sửa tay.

`kiem-thu-dac-ta` là tên một bí kíp **mẫu** ("kiểm thử dựa trên đặc tả"), không phải thuật ngữ hệ —
nên dịch theo nghĩa của nó, `spec-based-testing`.

## 3 · Quy tắc đặt tên định danh

- **Thư mục và tệp:** `kebab-case`, tiếng Anh. `thu-bi-kip/` → `scripture-intake/`
- **Hàm và biến Python:** `snake_case`, tiếng Anh. `kiem_manifest` → `check_manifest`
- **Khoá JSON/TOML:** `snake_case`, tiếng Anh. `tieu_chi_dat` → `pass_criteria`
- **Vai (agent/skill):** danh từ chỉ vai, `kebab-case`. `truong-mon/` → `sect-master/`
- **Không viết tắt.** Không có ngoại lệ nào đủ rẻ để đáng có: một định danh dài đọc chậm hơn vài giây, một định danh viết tắt sai nghĩa thì sai mãi. Bản trước của dòng này ghi "trừ khi dài hơn ba từ" mà không nói viết tắt *thành gì* — tức là một quy tắc không thi hành được.

Một khái niệm ra một từ. Nếu bảng này chưa có từ cho thứ đang cần, **thêm vào bảng trước**, rồi mới
dùng — chứ không dùng trước rồi ghi sau.

## 4 · Ánh xạ đường dẫn dữ liệu người dùng

Đổi hết, **không** kèm script migrate: plugin chưa phát hành, nên chưa có dữ liệu thật ngoài máy phát
triển. Quyết định này chỉ đúng khi thực hiện *trước* lần phát hành đầu; sau đó thì vĩnh viễn phải
migrate.

Nguồn cho "chưa phát hành", verify 2026-08-31: repo `van-dao` không có tag nào, không có remote nào,
và `CHANGELOG.md` ghi `## [0.1.0] — chưa phát hành`. Ba dấu hiệu độc lập cùng chỉ một hướng.

| Cũ | Mới |
|---|---|
| `.vandao/` | `.wayfarer/` |
| `.vandao/bi-kip/` | `.wayfarer/scriptures/` |
| `.vandao/truong-mon/chi-diem.jsonl` | `.wayfarer/sect-master/counsel.jsonl` |
| `.vandao/truong-mon/chi-diem-hong.jsonl` | `.wayfarer/sect-master/counsel-broken.jsonl` |
| `.vandao/truong-mon/ho-so.json` | `.wayfarer/sect-master/profile.json` |
| `.vandao/nhap-mon-ky.md` | `.wayfarer/initiation-record.md` |
| `.vandao/tang-kinh/nhap-dang-do/` | `.wayfarer/scripture-hall/drafts/` |
| `.vandao/ban-giao/thu/` | `.wayfarer/handover/letters/` |
| `.vandao/custom/thu-bi-kip.toml` | `.wayfarer/custom/scripture-intake.toml` |
| `.vandao/custom/truong-mon.toml` | `.wayfarer/custom/sect-master.toml` |

## 5 · Tên sản phẩm — **Wayfarer**

Chốt 2026-08-31, thay cho "Vấn Đạo" (問道).

Lý do chọn: "the Way" là cách tiếng Anh dịch Đạo đã hơn một thế kỷ, nên *wayfarer* — kẻ lữ hành trên
Đạo — dịch được cả nghĩa lẫn tinh thần của "Vấn Đạo" mà không phải dịch chữ nào. Nó cũng đặt trọng
tâm vào **người học**, không vào kho sách hay thứ bậc, đúng thứ sản phẩm này làm.

| Chỗ | Cũ | Mới |
|---|---|---|
| Thư mục plugin | `van-dao/` | `wayfarer/` |
| Tên plugin (`plugin.json`) | `van-dao` | `wayfarer` |
| Tiền tố lệnh | `/van-dao:*` | `/wayfarer:*` |
| Thư mục dữ liệu | `~/.vandao/` | `~/.wayfarer/` |
| Tiền tố tài liệu | `docs/VAN-DAO-*.md` | `docs/wayfarer-*.md` |

**Đã tra trùng tên, 2026-08-31.** Kết quả và lý do vẫn giữ:

- npm có package `wayfarer` (trie router, ~5.000 lượt tải/tuần, ngừng bảo trì). Khác registry — một
  plugin Claude Code không tranh chấp không gian tên với npm.
- Niantic từng có sản phẩm tên Wayfarer nhưng **đã đổi thành Niantic Recon**, tức tên đang được thả ra.
- Vài repo GitHub cùng tên, không cái nào cùng lĩnh vực.

Cái thật sự mất là **nhận diện tìm kiếm**: gõ "wayfarer" ra Niantic và một router JavaScript trước.
Chấp nhận, vì "wayfarer" là từ tiếng Anh phổ thông — không ai độc quyền được, và cũng không ai chặn
được ta dùng.

Hai tên từng cân nhắc, tra ra tệ hơn: **Ninefold** đã có một app *"therapist-built inner work"* tổ
chức quanh chín con đường — gần không gian sản phẩm này đến mức khó chịu; **Scriptorium** có game
Steam, text editor cho người viết, và eScriptorium.

Chưa tra: nhãn hiệu đăng ký (khác với trùng tên sản phẩm). Cần tra trước khi phát hành thương mại,
không cần trước khi công khai repo.

**Thư mục repo workspace** (`van-dao-workspace/`) để riêng, không đổi trong đợt này: đổi nó làm hỏng
mọi đường dẫn tuyệt đối đang có trong config và phiên làm việc, mà lợi ích thì chỉ là thẩm mỹ. Mốc:
cùng lúc với lần đặt remote đầu tiên.

*Ghi chú: `nhap-dang-do` = "nhập đang dở" — nháp pha 2 chưa xong, tiếp được ở phiên sau, vùng riêng
của Tàng kinh trưởng lão. Nên là `drafts/`, không phải `pending/`: "pending" nói thứ đang chờ ai đó
xử lý, còn đây là việc của chính người viết chưa làm xong.*

## 6 · Bảng này phủ đến đâu — và chỗ nó chưa cưỡng chế được

**Phủ:** thuật ngữ hệ (§1), danh từ kỹ thuật hay gặp (§2), đường dẫn dữ liệu người dùng (§4), tên sản
phẩm (§5). Đó là phần **quyết định** — chọn sai thì sai lan ra mọi chỗ.

**Chưa phủ:** hàng trăm khoá `snake_case` trong đặc tả (`dang_treo`, `lop_nhiem_vu`, `canh_gioi_ra`,
`khao_thi_quyen`, `ghi_luc`…). Chúng suy ra được từ §1 và §2 nên không cần liệt kê sẵn — nhưng **suy
ra rồi thì phải ghi vào §2**, để lần sau người khác gặp cùng khoá không suy ra một từ khác. Quy tắc:
gặp khoá chưa có từ → thêm dòng vào bảng → rồi mới đổi tên. Không làm ngược.

**Chỗ bảng này chưa cưỡng chế được gì.** Nguyên tắc "một khái niệm ra một từ" hiện chỉ là lời dặn —
đúng thứ dự án này liên tục chứng minh là không đủ. Phép kiểm rẻ nhất, dựng **sau khi refactor xong**:
một test quét mọi định danh trong mã và tên tệp, đỏ nếu còn ký tự có dấu tiếng Việt. Nó không bắt được
"dịch một khái niệm thành hai từ", nhưng bắt được "quên dịch", và đó là kiểu sót nhiều nhất. Mốc: cùng
lượt với lần refactor cuối.

## 7 · Chiến lược dịch tài liệu dài

Áp cho `docs/VAN-DAO-dac-ta-v1.0.md` (2.151 dòng, 1.224 dòng có tiếng Việt — 29% toàn bộ khối lượng
dịch của dự án) và mọi tài liệu cùng cỡ. Tách thành **đợt riêng**, không làm chung với đợt đổi tên mã.

**Vấn đề gốc:** "dịch có đúng nghĩa không" không có oracle. Nhưng phần lớn thiệt hại thật của một bản
dịch tài liệu đặc tả không nằm ở nghĩa — nó nằm ở **mất mát âm thầm**: rơi một hàng bảng, mất một mã
ràng buộc, gộp hai mục thành một. Thứ đó đếm được. Chiến lược này đổi câu hỏi không kiểm được lấy câu
kiểm được, và chấp nhận rõ ràng rằng phần nghĩa vẫn phải soi bằng mắt.

### 7.1 Hai loại dịch, làm theo thứ tự

| Loại | Bản chất | Công cụ | Oracle |
|---|---|---|---|
| **Định danh** — tên, khoá, đường dẫn | Tất định, có bảng §1–§4 | script thay chuỗi | `grep` từ cũ ra 0 |
| **Văn xuôi** | Phán đoán, không oracle tuyệt đối | dịch từng lô | bất biến §7.2 |

Định danh **trước**. Làm ngược thì mọi định danh nằm trong văn xuôi phải sửa lần hai — và lần hai là
lần người ta bỏ sót.

### 7.2 Bất biến — chạy `bin/check-invariants.py`

    python bin/check-invariants.py <file> --luu moc.json    trước khi đổi chữ đầu tiên
    python bin/check-invariants.py <file> --so moc.json     sau mỗi lô

Số phải khớp: heading H1/H2/H3 · số bảng và số cột mỗi bảng · tổng số hàng bảng · số khối mã · tập
hợp mã `R<n>`, `AD-n`, `FR/NFR` · tập hợp tham chiếu `§`.

Chú ý: script kiểm **tập hợp mã**, không kiểm số lượt xuất hiện — dịch được phép gộp câu làm đổi số
lượt, nhưng làm mất hẳn một mã thì luôn là lỗi.

Nó **không** kiểm nghĩa. Một bản dịch sai hoàn toàn mà giữ nguyên cấu trúc vẫn qua. Biết giới hạn đó
thì nó hữu ích; quên thì nó nguy hiểm hơn không có.

### 7.3 Chia lô theo H1, mỗi lô một commit

Đặc tả có 21 mục H1. Không bao giờ dịch nửa mục: chỗ dịch dở là nơi hai cách gọi cùng một khái niệm
gặp nhau, và nó lọt qua mọi phép kiểm cấu trúc.

### 7.4 Khoá glossary trước khi dịch dòng đầu tiên

Quét tài liệu lấy mọi thuật ngữ chưa có trong §1/§2, bổ sung hết **trước**. Không làm thì lô 3 sẽ tự
nghĩ ra từ mà lô 1 đã đặt khác — đúng thứ tài liệu này tồn tại để chống.

### 7.5 Không tạo bản copy tiếng Việt

Git đã giữ. Thêm một file copy là tạo nguồn thật thứ hai. Thay vào đó, ghi SHA của bản tiếng Việt
cuối cùng vào frontmatter bản tiếng Anh, để tra được bằng `git show <sha>:<path>`.

### 7.6 Cái không dịch

- Nội dung bên trong khối mã, trừ comment.
- Ví dụ hội thoại với người dùng (đặc tả có 2). Chúng minh hoạ hành vi khi `communication_language`
  là tiếng Việt, nên tiếng Việt ở đó là **nội dung đúng**, không phải sót. Thêm nhãn nói rõ.
- Trích dẫn nguyên văn từ nguồn tiếng Việt.

### 7.7 Spot-check nghĩa, không dịch ngược cả file

Chọn các mục mà hiểu sai thì mọi story sau sai — định nghĩa thuật ngữ, 33 ràng buộc `R<n>`, bảng tiêu
chí — dịch ngược và so nghĩa. Dịch ngược toàn bộ tốn gấp đôi mà bắt thêm rất ít.

## 8 · Không đổi

- `communication_language` và các khoá config chuẩn của BMad — thuộc nền tảng, không phải của ta.
- Nội dung do người dùng viết ra: bài nộp, ghi chép, thư của họ.
- Lịch sử git, story đã đóng, báo cáo nghiên cứu đã finalize — hồ sơ theo thời điểm ghi.
