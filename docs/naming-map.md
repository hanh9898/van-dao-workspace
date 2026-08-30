# Naming map — Vietnamese to English

**Status:** danh pháp đã chốt đủ để bắt đầu đổi tên. Chưa qua vòng review — xem mốc trong `review-log.md`.

Chốt 2026-08-31: hệ thống chuyển sang tiếng Anh toàn bộ — mã, tên file, định danh, tài liệu, skill,
agent. Thế giới quan tiên hiệp giữ nguyên; chỉ ngôn ngữ diễn đạt đổi. Tiếng Việt còn lại đúng một
chỗ: `communication_language` trong config, tức thứ tiếng hệ *nói chuyện* với người dùng.

Tài liệu này tồn tại vì một lý do hẹp: **cùng một khái niệm phải ra cùng một từ ở mọi nơi.** Dịch
rải rác qua nhiều lượt thì `bí kíp` sẽ thành `manual` chỗ này, `book` chỗ kia, `scripture` chỗ nữa —
và không có cách nào sửa lại sau, vì không ai biết ba từ đó từng là một.

---

## 1 · Thuật ngữ hệ — thế giới quan tiên hiệp

Nguyên tắc chọn từ: dùng từ vựng **cultivation fiction** đã phổ biến trong bản dịch tiếng Anh, để
người đọc có tiếp xúc thể loại nhận ra ngay. Không dùng pinyin, không dùng từ trung tính vô sắc.

| Tiếng Việt | Hán tự | Tiếng Anh | Ghi chú |
|---|---|---|---|
| bí kíp | 秘笈 | **manual** | Cuốn sách được nạp vào hệ. Không dùng `book` — mất màu, và `book` đã bận nghĩa kỹ thuật |
| mạch | 脈 | **meridian** | Nhánh tri thức chạy xuyên nhiều bí kíp |
| chỉ điểm | 指點 | **pointer** | Lời chỉ của Trưởng môn cho đệ tử. Số nhiều `pointers` |
| Trưởng môn | 掌門 | **Sect Master** | Vai điều phối |
| trưởng lão | 長老 | **Elder** | Vai chấm bài |
| đệ tử | 弟子 | **disciple** | Người học |
| nhập môn | 入門 | **initiation** | Nghi thức gia nhập |
| tàng kinh (các) | 藏經閣 | **Scripture Hall** | Nơi cất bí kíp |
| cảnh giới | 境界 | **realm** | Bậc tu vi |
| tâm pháp | 心法 | **heart method** | Nguyên lý cốt lõi của một chương |
| công pháp | 功法 | **technique** | Cách vận dụng |
| khảo thí | 考試 | **trial** | Bài kiểm tra. Không dùng `exam` — mất màu |
| nghiệm công | 驗功 | **proving** | Chứng minh đã lĩnh hội |
| Phúc Khảo Sứ | 覆考使 | **Re-examiner** | Vai chấm lại độc lập |
| hạ sơn | 下山 | **descend the mountain** | Rời môn phái, hoàn thành |
| giám định | 鑑定 | **appraisal** | Thẩm định bản sách trước khi nhận |

## 2 · Danh từ kỹ thuật — không mang màu

| Tiếng Việt | Tiếng Anh |
|---|---|
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
| phụ thuộc | depends on |
| nhận định | assessment |
| suy đoán | inference |
| giả định nền | baseline assumption |
| hết hiệu lực | expired |
| dư thừa | redundant |
| độ phức tạp | complexity |

## 3 · Quy tắc đặt tên định danh

- **Thư mục và tệp:** `kebab-case`, tiếng Anh. `thu-bi-kip/` → `manual-intake/`
- **Hàm và biến Python:** `snake_case`, tiếng Anh. `kiem_manifest` → `check_manifest`
- **Khoá JSON/TOML:** `snake_case`, tiếng Anh. `tieu_chi_dat` → `pass_criteria`
- **Vai (agent/skill):** danh từ chỉ vai, `kebab-case`. `truong-mon/` → `sect-master/`
- **Không viết tắt** trừ khi từ đầy đủ dài hơn ba từ.

Một khái niệm ra một từ. Nếu bảng này chưa có từ cho thứ đang cần, **thêm vào bảng trước**, rồi mới
dùng — chứ không dùng trước rồi ghi sau.

## 4 · Ánh xạ đường dẫn dữ liệu người dùng

Đổi hết, **không** kèm script migrate: plugin chưa phát hành, nên chưa có dữ liệu thật ngoài máy phát
triển. Quyết định này chỉ đúng khi thực hiện *trước* lần phát hành đầu; sau đó thì vĩnh viễn phải
migrate.

| Cũ | Mới |
|---|---|
| `.vandao/` | `.wayfarer/` |
| `.vandao/bi-kip/` | `.wayfarer/manuals/` |
| `.vandao/truong-mon/chi-diem.jsonl` | `.wayfarer/sect-master/pointers.jsonl` |
| `.vandao/truong-mon/ho-so.json` | `.wayfarer/sect-master/profile.json` |
| `.vandao/nhap-mon-ky.md` | `.wayfarer/initiation-record.md` |
| `.vandao/tang-kinh/nhap-dang-do/` | `.wayfarer/scripture-hall/drafts/` |
| `.vandao/ban-giao/thu/` | `.wayfarer/handover/letters/` |
| `.vandao/custom/thu-bi-kip.toml` | `.wayfarer/custom/manual-intake.toml` |
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

**Chưa kiểm trùng tên hay nhãn hiệu** — phiên chốt tên không có mạng. Phải tra một lượt trước khi
công khai repo hoặc phát hành plugin.

**Thư mục repo workspace** (`van-dao-workspace/`) để riêng, không đổi trong đợt này: đổi nó làm hỏng
mọi đường dẫn tuyệt đối đang có trong config và phiên làm việc, mà lợi ích thì chỉ là thẩm mỹ. Mốc:
cùng lúc với lần đặt remote đầu tiên.

*Ghi chú: `nhap-dang-do` = "nhập đang dở" — nháp pha 2 chưa xong, tiếp được ở phiên sau, vùng riêng
của Tàng kinh trưởng lão. Nên là `drafts/`, không phải `pending/`: "pending" nói thứ đang chờ ai đó
xử lý, còn đây là việc của chính người viết chưa làm xong.*

## 6 · Không đổi

- `communication_language` và các khoá config chuẩn của BMad — thuộc nền tảng, không phải của ta.
- Nội dung do người dùng viết ra: bài nộp, ghi chép, thư của họ.
- Lịch sử git, story đã đóng, báo cáo nghiên cứu đã finalize — hồ sơ theo thời điểm ghi.
