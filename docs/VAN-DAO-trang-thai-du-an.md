# Vấn Đạo — Trạng thái dự án và kế hoạch triển khai

**Ngày:** 2026-08-21, cập nhật 2026-08-24 · **Tác giả:** hanhnt2 (hanhnt2@hblab.vn)
**Đi kèm:** `VAN-DAO-dac-ta-v1.0.md` (đặc tả) · `bi-kip.schema.md` (data contract) · `VAN-DAO-setup-du-an.md` (dựng môi trường)

Tài liệu này nói **đang ở đâu** và **làm gì tiếp**. Không nhắc lại thiết kế.

---

# 1 · TRẠNG THÁI PHA

| Pha | Trạng thái | Ghi chú |
|---|---|---|
| Requirements | **Đóng** | 34 requirement — `R1`–`R31` cộng `R13b`·`R32`·`R33`, không open issue |
| Architecture | **Đóng** | 8 role, 28 component, 13 model, ranh giới đọc/ghi đã khai |
| Detailed design | **1/8** | Một data contract đã đặc tả; bảy cái còn lại mới có tên |
| Implementation | **Nền kỹ thuật xong, vertical slice chưa bắt đầu** | `kiem-bi-kip.py` + test + CI đã trong repo (§6 Ưu tiên 1); `giam-dinh.py`/skill `thu-bi-kip`/`thu-linh` chưa viết |
| Verification | **9 regression test (script), còn lại manual** | `pytest` xanh, CI chạy cả `ubuntu-latest` và `windows-latest` |

**Pha đặc tả đóng được.** Không còn câu hỏi chặn việc dựng.

---

# 2 · ARTIFACT

## 2.1 Đã có

| Artifact | Cỡ | Trạng thái |
|---|---|---|
| `VAN-DAO-dac-ta-v1.0.md` | 2.112 dòng | Tự đủ, nhất quán nội bộ |
| `bi-kip.schema.md` | 308 dòng | Data contract, đã dùng để viết validator |
| `kiem-bi-kip.py` | 541 dòng | **Đã chạy**, có test data, bắt được lỗi thật |
| `VAN-DAO-setup-du-an.md` | — | Hướng dẫn dựng môi trường |

## 2.2 Data contract còn thiếu

Bảy cái, có tên và vai trò trong đặc tả nhưng chưa có schema:

| Contract | Chặn gì | Ghi chú |
|---|---|---|
| `canh-gioi.md` | Toàn bộ nhánh định vị | **Phải tra Dreyfus bản gốc trước** (§19 đặc tả) |
| `lo-do.schema.md` | Vòng 1 | |
| `ho-so.schema.md` | Vòng 1 | |
| `loai-cau-hoi.md` | Vòng 1 | Phần lớn đã nằm trong `bi-kip.schema.md` |
| `mach.schema.md` | Vòng 3 | |
| `catalog.schema.md` | Vòng 3 | |
| `thu.schema.md` | Vòng 4 | |

**Viết just-in-time theo vòng, không viết trước cả bảy.** Căn cứ: `bi-kip.schema.md` chỉ đúng **sau khi** validator chạy trên dữ liệu thật — ba trường (`do_tieu_chi`, `id` bất biến, phân biệt rỗng-với-vắng) phải thêm sau đó. Bảy cái kia gần như chắc chắn cũng vậy.

---

# 3 · VERIFICATION COVERAGE

| Loại | Số lượng |
|---|---|
| Static check (script) | **3 / 34 requirement** |
| Unit test | **0** |
| Integration test | **0** |
| Trigger / behavioral eval | **0** |
| Manual walkthrough | Toàn luồng |

**31/34 requirement hiện chỉ verify được bằng người đọc transcript** (29 cũ + R32/R33 mới thêm, chưa có script). Đây là con số nghiêm trọng nhất trong tài liệu này.

Không phải toàn bộ đều tự động hoá được — nhóm judgment vốn không. Nhưng tỉ lệ hiện tại nghĩa là **hệ chỉ đúng chừng nào có người ngồi soát**, và ở n=1 người đó sẽ chán.

---

# 4 · DEFECT PROFILE TỪ WALKTHROUGH

Walkthrough thủ công toàn luồng — từ bái sư tới định vị, cộng hai chế độ hỏng — tìm được **11 defect**.

## 4.1 Phân loại theo giai đoạn tiêm lỗi

| Giai đoạn | Số | Ví dụ |
|---|---|---|
| Requirements — thiếu ca | 6 | `ban_hong` khác `khong_thay`; nhánh `khong_ro` |
| Design — thiếu đường dữ liệu | 4 | Tàng kinh không có đường báo về trưởng môn; ứng viên tiêu chí không có nhà |
| Spec-internal inconsistency | 1 | Lược đồ khai 3 giá trị, bảng xử lý 2 |

## 4.2 Hiệu quả của hai phương pháp verify

| Phương pháp | Defect bắt được |
|---|---|
| Document review — bốn lần soát chéo | **0 / 11** |
| Manual walkthrough — đóng vai, chạy ca thật | **11 / 11** |

**Kết luận rút ra và áp cho phần còn lại của dự án:** với loại lỗi *thiếu ca* và *thiếu đường dữ liệu*, đọc lại tài liệu **không hiệu quả**. Chúng chỉ hiện ra khi có ca thật chạy qua.

Hệ quả: **không viết thêm design cho tới khi có executable spec.**

## 4.3 Điểm lợi tức giảm dần

Ba khúc walkthrough đầu tìm được defect nặng (thiếu cơ chế). Hai khúc cuối chỉ tìm được defect nhẹ (đặt sai hạng, thiếu một dòng mẹo).

Bốn cơ chế còn lại ở §17.1 đặc tả **không mô phỏng được** — chúng cần thời gian trôi hoặc lặp lại thật.

**Walkthrough nên dừng.** Tiếp tục là trả công cho lợi tức giảm.

---

# 5 · NỢ KỸ THUẬT

**Bốn nợ trước đó đã trả** — `kiem-bi-kip.py` vào `bin/`, test suite (`tests/` + fixture, 9/9 pass), CI (`.github/workflows/kiem.yml`, ubuntu+windows). Ba defect cần regression test đã có test khoá lại: **mảng rỗng bị coi là vắng mặt** (`test_mang_rong_khong_phai_thieu_truong`) · **bộ tham số thiếu khoá** (`test_bo_tham_so_thieu_khoa_la_loi`) · **enum sai giá trị** (`test_canh_gioi_ngoai_enum_la_loi`).

| Nợ còn lại | Rủi ro |
|---|---|
| Chưa có remote — cả `van-dao` và workspace chỉ tồn tại local | Máy hỏng là mất hết, kể cả lịch sử git |

---

# 6 · KẾ HOẠCH

## Nguyên tắc

**Không viết thêm design cho tới khi có executable spec.** Căn cứ ở §4.2.

## Ưu tiên 1 — nền kỹ thuật (xong, trừ 1.1)

| # | Việc | Xong khi | Trạng thái |
|---|---|---|---|
| 1.1 | `git init` repo `van-dao`, push remote | Người khác `clone` được | `git init` xong (cả `van-dao` và workspace) — **push: chưa**, chưa chọn nơi lưu |
| 1.2 | Chuyển `kiem-bi-kip.py` vào `bin/` | Nằm trong VCS | ✅ |
| 1.3 | `tests/` với pytest, ba regression test từ §5 | `pytest` xanh | ✅ — 9/9 pass |
| 1.4 | Test fixture: bí kíp sạch, bí kíp lỗi, tàn quyển | Tái tạo được | ✅ |
| 1.5 | CI tối thiểu — chạy pytest mỗi push | Vỡ thì biết ngay | ✅ — chạy cả `ubuntu-latest` và `windows-latest` |

Việc còn lại của ưu tiên này chỉ là **chọn nơi push** (GitHub cá nhân, nội bộ, hay khác) — quyết định của tác giả, không tự chọn được.

## Ưu tiên 2 — vertical slice

Vòng 1 của §16 đặc tả: **ingest → teach → assess**, một quyển, một chương, một người học.

Đây là **integration test đầu tiên**, và là lần đầu chạm nhóm requirement thuộc cột *giá trị*.

Data contract viết just-in-time: `lo-do` và `ho-so` khi tới bước cần chúng.

**Không áp dụng cho eval từng skill.** Đọc trước đây coi "vertical slice trước" là lý do hoãn cả
behavioral eval của từng skill sang Ưu tiên 3 — sai, đã sửa bằng nghiên cứu
`_bmad-output/planning-artifacts/research/technical-quy-trinh-eval-khi-viet-skill-claude-ski-2026-08-27/research.md`
(2026-08-27): "vertical slice trước" (Walking Skeleton) chỉ phục vụ rủi ro **kiến trúc/tích hợp**
giữa các skill — không phải lý do bỏ qua xác minh đúng-sai của một skill đã viết xong. Đặc tả §16
("ba thứ dựng xuyên suốt") đã yêu cầu `evals/` đi cùng từng skill ngay lúc viết; quy trình chính
thức `skill-creator` của Anthropic làm đúng vậy. Mỗi story viết skill mới (kể cả trong Vòng 1 này)
tự mang theo eval **nhẹ** của nó — xem `van-dao/.claude/rules/eval.md`.

## Ưu tiên 3 — kéo verification lên

| Nhóm requirement | Cách verify | Ước số |
|---|---|---|
| Schema / graph constraint | Script — đã có khung | ~8 |
| Message contract | `kiem-thu.py` | ~5 |
| Skill behavior — nâng lên mức đầy đủ (đã có bản nhẹ từ lúc viết, xem Ưu tiên 2) | Behavioral eval đầy đủ + trigger eval 20-câu/60-40 (`skill-creator`) | ~10 |
| Routing | Trigger eval | ~3 |
| Judgment quality | Manual + κ calibration | ~8 |

**Mục tiêu: kéo 31 requirement manual xuống dưới 10.** Không nhắm 100% — nhóm cuối vốn không tự động hoá được.

---

# 7 · RÀNG BUỘC LỊCH

## 7.1 Quality gate chặn nhánh định vị

Bước 25 của §16 — **κ calibration** — là điều kiện để R11 cho phép công bố cảnh giới.

Nó cần **20 mẫu chấm tay**, mà mẫu chỉ sinh ra sau khi có người học thật. Nên:

```
vòng 1 xong → có người học thật → mẫu tích dần → đủ 20 → calibration → mở nhánh định vị
```

**Không rút ngắn được.** Trước gate này, trưởng lão chạy được nhưng **im lặng về bậc** (R10 trả `null`, §5.10 vẫn nêu `dau_hieu[]`).

## 7.2 Phụ thuộc ngoài

`canh-gioi.md` chặn bởi việc **tra Dreyfus bản gốc**. Đây là phụ thuộc ngoài dự án, không lập trình được qua.

---

# 8 · RỦI RO

| Rủi ro | Mức | Ghi chú |
|---|---|---|
| **Đặc tả quá lớn so với bằng chứng** | **Cao** | 2.112 dòng, 34 requirement, 28 component — cho một người dùng chưa học xong chương nào |
| 31/34 requirement chỉ verify thủ công | Cao | Hệ chỉ đúng chừng nào có người ngồi soát |
| Hai giả định nền chưa kiểm | Cao | §17 đặc tả — sai thì dựng lại từ §1 |
| Bốn cơ chế không kiểm được ở giai đoạn này | Trung bình | §17.1 — đã ghi nhận, không phải việc bỏ sót |
| Dựng xong thì hết hứng | Trung bình | Rủi ro cố hữu của dự án n=1, đã chấp nhận khi chọn bậc 3 |

**Rủi ro số một đã đổi.** Trước walkthrough nó là *"đặc tả chưa đủ chín"*. Giờ là *"đặc tả quá chín so với thứ đã chạy"* — mỗi dòng thêm vào là một dòng phải dựng đúng.

---

# 9 · MẪU THIẾT KẾ RÚT RA

Ghi lại vì chúng sẽ dùng lại ở mọi component chưa viết.

## 9.1 Chuyển ràng buộc từ lời dặn sang cấu trúc dữ liệu

Lặp **ba lần** trong dự án này, mỗi lần đều làm ràng buộc kiểm được bằng script:

| Ràng buộc | Trước | Sau |
|---|---|---|
| Câu hỏi phủ hết tiêu chí | Soát bằng mắt | `do_tieu_chi` — liên kết tường minh |
| Tổ hợp tham số hợp lệ | Model tự lọc lúc chạy | `bo_tham_so` — bộ khớp sẵn, kiểm ở pha validate |
| Không lộ nhãn bậc khi chưa đủ dữ liệu | Vai cầm lượt tự biên tập | `dau_hieu[]` tách khỏi `nhan_dinh` — bóc bằng chọn trường |

**Đây là kỹ thuật dựng chính của dự án.** Khi gặp một ràng buộc chỉ tồn tại dưới dạng lời dặn, hỏi: *có cấu trúc dữ liệu nào làm nó kiểm được không?*

## 9.2 Ranh giới trách nhiệm: bí kíp vs hệ

Áp cho ba ca khác nhau, cùng một kết luận: **yếu ở đâu là lỗi của bí kíp, không phải lỗi của hệ.**

| Ca | Sửa ở |
|---|---|
| Tiêu chí không phân biệt | `tieu_chi_dat` của bí kíp |
| Đề không ép khẳng định | `khao_thi_quyen` của bí kíp |
| `du_thua` dùng cho cảnh giới cao | Thiết kế bí kíp |

Nó giữ cho hệ không phình mỗi lần một bí kíp viết kém.

## 9.3 Fail an toàn

`.pham-vi.json` thiếu → **không vai nào đọc được**, không phải mọi vai đọc được. Thêm thư mục mà quên khai thì nó im lặng vô hình, chứ không im lặng mở toang.

---

# 10 · VIỆC TIẾP THEO

Ưu tiên 1 xong trừ push (§6). Còn lại theo đúng thứ tự phụ thuộc ở §16 đặc tả, Vòng 1:

1. Push remote — **cần bạn chọn nơi lưu trước**, không chặn bởi gì khác
2. `bin/giam-dinh.py` + skill `thu-bi-kip` (Tàng kinh trưởng lão) — ba pha, dừng ở pha 2. Phụ thuộc ngoài: `book-to-skill` (virgiliojr94)
3. Thu một quyển thật, 3 chương
4. `tham-chieu/lo-do.schema.md` + skill `thu-linh` — F-1 · F0 · F0′ · F1 · F2
5. `.pham-vi.json` + `bin/kiem-thu.py` bản đầu (R26/R27) — chỉ phụ thuộc bước đã xong, làm song song với 2-4 được
6. `agents/nghiem-cong.md` — chấm chương
7. skill `nhap-mon` · `dao-tam` · `bin/tang-kinh-cac.py` — song song
8. **Tự bế quan quyển đó bằng plugin**

Bước 8 là lần đầu có người học thật, và là thứ duy nhất chạm được cột *giá trị* — cột duy nhất vẫn ở 0% sau tất cả những gì đã làm.
