---
title: 'Chỉ điểm — Trưởng môn gọi tên sách'
type: 'feature'
created: '2026-08-27'
status: 'done'
baseline_commit: 'b42c19309f8586c2f14c515ef92a1a3efa78b76d'
review_loop_iteration: 0
context:
  - '{project-root}/AGENTS.md'
# Hồ sơ hoãn (4 mục, mỗi mục có mốc quay lại) tách sang file đồng hành — không cần đọc để implement:
deferred_log: '3-chi-diem-truong-mon-goi-ten-sach.deferred.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Sau khi bái sư xong (Story 1.2), `nhap-mon` chủ động chặn "chỉ điểm chưa hỗ trợ ở bản này" — người học có vai/mạch nhưng chưa có sách cụ thể nào để bắt đầu, và tàng kinh các ban đầu rỗng nên không có mạch nào tự khởi động được.

**Approach:** Skill mới `truong-mon` (đã quy hoạch ở Bậc 2, đặc tả §13.1) — sau bái sư, `nhap-mon` dẫn tường minh sang `/van-dao:truong-mon` (không tự động im lặng). Trưởng môn gọi 3 công pháp + 2 tâm pháp (đã biết muốn luyện) hoặc 1+1 (chưa biết), mỗi chỉ điểm đủ 5 trường (tên/tác giả/năm-ấn bản/loại/vì sao), câu rào mức chắc chắn nói TRƯỚC danh sách — rồi ghi `truong-mon/chi-diem.jsonl` trạng thái `dang_treo`.

## Boundaries & Constraints

**Always:** 5 trường bắt buộc mỗi chỉ điểm, ba dữ kiện đầu (tên/tác giả/năm-ấn bản) không được thiếu, không chắc thì nói không chắc — không đưa tên trần; câu rào mức chắc chắn (số liệu thật / nguồn khai báo / suy đoán) luôn nói TRƯỚC khi đưa danh sách, không phải sau, và phải **nói đúng trạng thái kho thật** ("kho chưa có quyển nào") thay vì công thức chung chung ("ta chưa có dữ liệu nào") — câu rào là thứ đo được, không phải câu than nghi thức; ở story này kho luôn rỗng nên luôn ở mức suy đoán, kèm mời tự nhập hướng khác; danh sách công pháp là **thực đơn để người học chọn một**, không phải danh sách phải đi kiếm hết — nói rõ điều đó khi trình, và luôn kèm lối tự nhập hướng khác (gợi ý, không ép); với tâm pháp, tách hai việc: **gọi tên thì luôn** (mỗi công pháp kèm tâm pháp đỡ trần cùng lượt, để người học biết nó tồn tại), **đẩy lên thì không** — chỉ đẩy khi có dấu hiệu (vấp lặp cùng chỗ / cảnh giới không nhích), mà ở story này dấu hiệu chưa thể tồn tại nên tuyệt đối không dựng logic đẩy; số lượng mặc định 3 công pháp + 2 tâm pháp (đã biết) / 1+1 (chưa biết) đọc qua `customize.toml` field `so_chi_diem` của `truong-mon`, hình dạng field chốt ở Design Notes (đặc tả khai đủ cả hai mặc định nhưng không khai hình dạng field — không được tự bịa thêm trường ngoài hình dạng đã chốt); chỉ điểm mới thay HẲN chỉ điểm `dang_treo` cũ (chuyển `het_hieu_luc`), không cộng dồn, nhưng vẫn tra lại được nếu hỏi tên cũ; người học tự báo "tìm không ra" một chỉ điểm `dang_treo` → ghi `khong_thay` vào `chi-diem-hong.jsonl`, chỉ điểm quyển khác thay ngay; đúng trình tự "Trình → xác nhận → ghi → kiểm" và đủ 4 quy ước §12.4 khác; behavioral eval nhẹ đi cùng ngay (AD-10); không trích FR/NFR/§ trong nội dung skill (AD-11); tự xác định lại home-dir hiện tại trước khi đọc/ghi bất kỳ đường dẫn `~/.vandao/...` nào trong phiên (bug đã gặp 2 lần).

**Ask First:** (không có — phạm vi đã rõ từ SPEC.md CAP-17 và đặc tả §10.0-10.3, không có quyết định cần người can thiệp giữa chừng)

**Never:** Không xây `thu-bi-kip` (Story 1.4) — không tự tải/thẩm định sách, không đọc/ghi trạng thái `da_thu`/`ban_hong` (hai trạng thái này chỉ tới từ thư của `thu-bi-kip` sau này qua `ban-giao/thu/`, chưa có consumer thật để test) — chỉ khai đủ 5 giá trị hợp lệ trong schema/văn xuôi để không đổi hình dạng file khi Story 1.4 tới; không tự động (im lặng) chuyển từ bái sư sang chỉ điểm mà không có lệnh tường minh; không chọn mạch hộ người học (đã khai/suy ở Story 1.2, không đổi ở đây); không vai nào khác ngoài `truong-mon` đọc/ghi trực tiếp `chi-diem.jsonl`/`chi-diem-hong.jsonl` (AD-3). **Không tự dựng cơ chế nhắc đầu phiên** cho `dang_treo` — việc đó thuộc hook `SessionStart` (`hooks/nap-ho-so.sh`, chưa có ở bản này); skill chỉ chạy khi người học gõ lệnh nên nhét vào đây là nhét vào đúng chỗ không chạy được. **Không đếm kho** để nhích mức chắc chắn — đọc kho là vùng của Tàng kinh trưởng lão (AD-3); ở story này kho luôn rỗng, nói thẳng "kho chưa có quyển nào" là đủ. **Không dựng logic "đẩy tâm pháp lên"** — điều kiện kích hoạt (vấp lặp / cảnh giới không nhích) chưa thể tồn tại ở story này vì người học chưa học quyển nào; dựng nó là dựng nhánh chết. **Không dựng bản đồ** để hiện tâm pháp — bản đồ là `bin/ban-do.py` + Artifact (chưa có ở bản này).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Đã biết muốn luyện gì, kho rỗng | Vai/mạch đã khai, chưa có chỉ điểm nào | Câu rào (kho chưa có quyển nào) TRƯỚC danh sách; 3 công pháp làm thực đơn chọn một + tâm pháp đỡ trần gọi tên kèm; đủ 5 trường mỗi cuốn; kèm lối tự nhập; xác nhận rồi ghi `dang_treo` | Không lỗi |
| Chưa biết muốn luyện gì | Như trên, `mach_nguon` = suy_tu_vai | 1 công pháp + 1 tâm pháp, cùng câu rào và cùng lối tự nhập — ít quyển hơn vì không chuyển gánh nặng chọn lựa sang người vừa nói mình chưa biết chọn | Không lỗi |
| Báo tìm không ra sách | Có chỉ điểm `dang_treo` | Ghi `khong_thay` vào `chi-diem-hong.jsonl`, chỉ điểm quyển khác thay ngay trong cùng lượt | Không lỗi |
| Xin chỉ điểm lại (không phải vì tìm không ra) | Chỉ điểm `dang_treo` hiện có | Nhắc số quyển còn treo TRƯỚC, hỏi có thay hết không; đồng ý thì chỉ điểm cũ chuyển `het_hieu_luc`, chỉ điểm mới ghi `dang_treo`; hỏi lại tên cũ vẫn tra được | Không lỗi — không tự xoá lô cũ khi chưa hỏi |
| Gọi khi bái sư chưa xong | Hồ sơ thiếu vai/mạch | Từ chối, dẫn quay lại `/van-dao:nhap-mon`, không tự suy mạch hộ | Không lỗi — chặn rõ |

</frozen-after-approval>

## Code Map

- `van-dao/skills/truong-mon/SKILL.md` (mới) -- skill chỉ điểm, đủ 4 quy ước §12.4, đọc `customize.toml` riêng
- `van-dao/skills/truong-mon/customize.toml` (mới) -- lần đầu triển khai thật cơ chế §12.1 trong codebase, mặc định `so_chi_diem` 3+2/1+1
- `van-dao/skills/truong-mon/evals/evals.json` (mới) -- eval nhẹ AD-10, khớp I/O matrix trên
- `van-dao/skills/nhap-mon/SKILL.md` -- sửa 3 chỗ stub "chỉ điểm chưa hỗ trợ ở bản này" (dòng ~12, ~17, ~162) thành dẫn `/van-dao:truong-mon`
- `van-dao/skills/nhap-mon/SKILL.md` (đọc-only, mẫu tái dùng) -- logic 3-tier cờ nguồn gợi ý mạch (Story 1.2) là khuôn cho cờ mức-chắc-chắn chỉ điểm
- `docs/VAN-DAO-dac-ta-v1.0.md` §10.0-10.4 -- flowchart + bảng quyết định mức chắc chắn §10.3 (đọc); §10.2 heading + §12.1 hình dạng `so_chi_diem` (sửa, xem Tasks)
- `_bmad-output/specs/spec-van-dao-workspace/SPEC.md` CAP-17 (đọc-only) -- nguồn intent/success
- `ARCHITECTURE-SPINE.md` AD-3/AD-4/AD-5 (đọc-only) -- vùng ghi riêng, loại component, lớp dữ liệu

## Tasks & Acceptance

**Execution:**
- [x] `van-dao/skills/truong-mon/SKILL.md` -- viết skill mới, trình→xác nhận→ghi→kiểm cho chỉ điểm -- đúng luồng §10.0 node H, tách skill theo AD-4 (đối thoại, không tất định)
- [x] `van-dao/skills/truong-mon/customize.toml` -- khai `so_chi_diem` đúng hình dạng chốt ở Design Notes -- tránh hard-code số trong SKILL.md; lần đầu cơ chế §12.1 chạy thật trong codebase
- [x] `van-dao/skills/truong-mon/evals/evals.json` -- 3-4 kịch bản khớp I/O matrix + 1 kịch bản gộp 2 lớp `customize.toml`, evidence transcript chạy thật -- AD-10
- [x] `docs/VAN-DAO-dac-ta-v1.0.md` §12.1 -- bổ sung hình dạng `so_chi_diem` (bảng hai khoá); §10.2 sửa heading "Ba trạng thái" → "Năm trạng thái" (bảng dưới đã liệt kê 5) -- sửa nguồn sự thật trước khi mã bám theo
- [x] `van-dao/skills/nhap-mon/SKILL.md` -- đổi 3 chỗ stub sang dẫn `/van-dao:truong-mon` -- đóng vòng bái sư→chỉ điểm

**Acceptance Criteria:**
- Given vai/mạch đã khai và chưa có chỉ điểm nào, when gọi `/van-dao:truong-mon`, then nhận đủ số lượng theo nhánh đã biết/chưa biết, mỗi chỉ điểm đủ 5 trường, câu rào xuất hiện trước danh sách, và `chi-diem.jsonl` có dòng mới `dang_treo`
- Given một chỉ điểm đang `dang_treo`, when người học báo tìm không ra, then `chi-diem-hong.jsonl` có dòng `khong_thay` và một chỉ điểm thay thế được đưa ra trong cùng lượt
- Given một chỉ điểm đang `dang_treo`, when người học xin chỉ điểm lại (không phải tìm không ra), then Trưởng môn nhắc số quyển còn treo và hỏi trước khi thay, rồi chỉ điểm cũ mới chuyển `het_hieu_luc` và chỉ điểm mới ghi `dang_treo`; hỏi lại tên cũ vẫn tra được
- Given `truong-mon/SKILL.md` sau khi viết xong, when soát nội dung, then không có bước nào tự dựng cơ chế nhắc đầu phiên (thuộc hook `nap-ho-so.sh`), không có logic đẩy tâm pháp (điều kiện chưa thể tồn tại), và không có bước dựng bản đồ — cả ba đều chưa có ở bản này
- Given người học nhận danh sách chỉ điểm, when đọc lượt trình, then hiểu được đây là thực đơn để chọn một công pháp chứ không phải danh sách phải kiếm hết, và luôn có lối tự nhập hướng khác (gợi ý, không ép)
- Given mỗi công pháp trong danh sách, when trình ra, then có tâm pháp đỡ trần được gọi tên kèm theo, nhưng không có câu nào giục người học học tâm pháp ngay
- Given hồ sơ thiếu vai/mạch, when gọi `/van-dao:truong-mon`, then skill từ chối và dẫn quay lại `/van-dao:nhap-mon`, không tự suy mạch hộ
- Given `~/.vandao/custom/truong-mon.toml` đặt `so_chi_diem` khác mặc định, when gọi chỉ điểm, then số sách đưa ra theo lớp cá nhân — chứng minh bằng lượt chạy thật, không suy diễn từ việc đọc được file gốc

## Spec Change Log

## Design Notes

**Phạm vi `truong-mon` ở story này là bản mồi lửa, không phải bản đầy đủ.** §16 xếp skill `truong-mon` ở Vòng 3 bước 14 — nhưng đó là bản đầy đủ, đi kèm `mach.schema.md` và việc *xếp lớp nhiều mạch*. Story này giao phần mồi lửa: một mạch, kho rỗng, chỉ điểm để khởi động hệ — không xếp lớp, không `mach.schema.md`. Hai phạm vi dùng chung một cái tên, nên nói rõ ở đây để người đọc sau không tưởng bước 14 đã xong.

**`dang_treo` ghi được, nhưng hành vi nhắc chưa chạy ở bản này.** Đặc tả gán cho `dang_treo` hành vi "nhắc một câu ở phiên sau", và cơ chế nhắc đó là hook `SessionStart` (`hooks/nap-ho-so.sh`, thành phần 17, §16 Vòng 3 bước 17) — **không phải việc của `truong-mon`**, vì skill chỉ chạy khi người học tự gõ lệnh. Hook chưa tồn tại (`van-dao/hooks/` hiện chỉ có `.gitkeep`). `truong-mon` **cấm tự dựng cơ chế nhắc đầu phiên** — nhét vào đây là nhét vào đúng chỗ nó không chạy được.

Phần làm được ngay và story này PHẢI làm: khi người học tự gọi `/van-dao:truong-mon` mà đang có mục `dang_treo`, Trưởng môn nhắc ngay trong lượt đó **trước khi** chỉ điểm mới — làm chốt xác nhận trước khi lô cũ chuyển `het_hieu_luc`, để người học kịp nói "khoan, quyển kia tôi đang tìm dở". Đây là một ca của hành vi nhắc, không phải bản thay thế cho hook.

Mốc xử lý phần còn lại: **ngay sau khi Epic 2 hoàn tất**. Lúc đó lộ đồ đã tồn tại nên `nap-ho-so.sh` có hai trong ba payload (hồ sơ từ Story 1.2, lộ đồ từ Epic 2 — còn thiếu bản đồ/`ban-do.py`), đủ lý do dựng thật; nhắc `dang_treo` đi kèm chuyến đó. Không hoãn quá mốc này mà không ghi lại lý do.

**Tâm pháp: gọi tên thì luôn, đẩy lên thì không.** Đặc tả phân biệt hai động từ mà một câu spec dễ gộp làm một. *Gọi tên*: mỗi công pháp kèm một tâm pháp đỡ trần, để người học biết nó tồn tại — luôn làm. *Đẩy lên* ("chiêu thức ngươi đủ rồi, thiếu là ở nội công"): chỉ khi có dấu hiệu thật (vấp lặp cùng chỗ, cảnh giới không nhích) — ở story này người học chưa học quyển nào nên dấu hiệu **không thể tồn tại**, dựng logic đẩy là dựng nhánh chết. Đặc tả cũng nói tâm pháp "mở sẵn trong bản đồ", nhưng bản đồ (`bin/ban-do.py` + Artifact) chưa có — nên ở bản này tâm pháp chỉ nằm trong `chi-diem.jsonl` và hiện ra khi người học hỏi.

**Thành phần 17 là nút thắt ngầm.** Ba thứ khác nhau trong phạm vi chỉ điểm đều đổ về cùng một thành phần chưa tồn tại (`hooks/nap-ho-so.sh` · `bin/ban-do.py` + Artifact, §16 Vòng 3 bước 17): nhắc `dang_treo` đầu phiên, nạp lộ đồ đang dở, và chỗ hiện bản đồ tâm pháp. Không tài liệu nào hiện gọi nó là nút thắt. Ghi lại đây để lúc lên kế hoạch Vòng 3 biết bước 17 gánh nhiều hơn vẻ ngoài của nó.

**Hình dạng `so_chi_diem` — chốt ở story này.** Đặc tả khai đủ **cả hai** mặc định ở §10.1 (bảng nhánh đã-biết 3+2 / chưa-biết 1+1, kèm câu "cả hai là mặc định, chỉnh được qua `so_chi_diem`"), nhưng §12.1 chỉ nhắc lại một ("3 công pháp + 2 tâm pháp") và **không chỗ nào khai hình dạng field**. Story này chốt hình dạng bảng hai khoá và bổ sung lại vào đặc tả §12.1 cho khớp (sửa nguồn sự thật trước, đúng Policy):

```toml
[so_chi_diem]
da_biet  = { cong_phap = 3, tam_phap = 2 }
chua_biet = { cong_phap = 1, tam_phap = 1 }
```

Cố ý chỉ phơi `so_chi_diem` ở bản này. Hai field còn lại đặc tả gán cho `truong-mon` để trống có lý do: `persistent_facts` là khoảng hở đã biết (§12.4 tự nhận chưa skill nào có bước đọc nó), `catalog_them` chưa có catalog nào để thêm vào. Người dùng hỏi tới thì nói thẳng chưa phơi, không bịa trường.

**Luật 5 trường là mitigation tầng phát hiện, không phải ngăn chặn.** Đặc tả nói rõ ba dữ kiện cụ thể "khó bịa *trót lọt*" hơn tên trần — tức làm cho việc bịa dễ bị bắt, không làm model ngừng bịa. Sách không tồn tại là ca đã được lường trước, và `khong_thay` chính là đường phục hồi có chủ đích cho nó (người học tìm không ra — dù vì sách không có thật hay vì lý do khác — thì cách xử lý như nhau). Đừng đọc luật 5 trường như thể đã đóng được rủi ro bịa sách.

Cờ mức-chắc-chắn (số liệu thật/nguồn khai báo/suy đoán) tái dùng nguyên khuôn 3-tier đã dựng cho gợi ý mạch ở Story 1.2 (`nhap-mon/SKILL.md`) — chỉ đổi đối tượng (sách thay mạch) và vị trí câu rào (trước danh sách). Không dựng logic mới.

Dẫn từ bái sư sang chỉ điểm dùng lệnh tường minh `/van-dao:truong-mon`, không tự động im lặng dù sơ đồ §10.0 vẽ liền một luồng — auto-trigger dựa hoàn toàn vào `description` là rủi ro thật đã ghi nhận (lens `skill-quality` check 7), và đúng khuôn tiền lệ `nhap-mon` → `nhap-mon-ky`.

`da_thu`/`ban_hong` là 2 trong 5 giá trị hợp lệ nhưng KHÔNG có luồng nào trong story này tạo ra chúng — chỉ tới từ thư của `thu-bi-kip` (Story 1.4, chưa xây) theo AD-3. Khai đủ 5 giá trị trong schema/văn xuôi ngay từ đầu để không đổi hình dạng file sau này, nhưng không viết logic nhận thư ở story này — chưa có consumer thật để test.

## Verification

**Commands:**
- `claude plugin validate van-dao --strict` -- expected: PASS (thêm skill `truong-mon`, sửa `nhap-mon`)

**Manual checks (if no CLI):**
- Đọc `truong-mon/SKILL.md` xác nhận đủ 4 quy ước §12.4, không trích FR/NFR/§ (AD-11), có bước xác định lại home-dir
- Đọc `truong-mon/evals/evals.json` xác nhận evidence trích nguyên văn transcript chạy thật, khớp I/O matrix (AD-10)
- Đọc 3 chỗ sửa trong `nhap-mon/SKILL.md` xác nhận dẫn đúng `/van-dao:truong-mon`, không còn "chưa hỗ trợ ở bản này" cho chỉ điểm
- **Kiểm gộp 2 lớp `customize.toml` bằng một lượt chạy thật:** dựng `~/.vandao/custom/truong-mon.toml` (trong home cô lập) đặt `so_chi_diem` khác mặc định, gọi chỉ điểm, xác nhận số sách đưa ra theo lớp cá nhân chứ không theo lớp gốc — không có script nào gộp hộ, skill tự gộp bằng lời nên phải chứng minh bằng lượt chạy, không suy diễn từ việc file gốc đọc được

## Suggested Review Order

**Hợp đồng skill — đọc trước để nắm ý đồ**

- Điểm vào: `description` khai cả 3 đường kích hoạt (lệnh tường minh + 2 đường tự nhiên)
  [`SKILL.md:3`](../../../../van-dao/skills/truong-mon/SKILL.md#L3)

- Điều kiện xong của từng nhánh — chỗ duy nhất định nghĩa "thế nào là hoàn tất"
  [`SKILL.md:8`](../../../../van-dao/skills/truong-mon/SKILL.md#L8)

- Ba ranh giới cấm: nhắc đầu phiên, đẩy tâm pháp, dựng bản đồ — đều là nhánh chết ở bản này
  [`SKILL.md:18`](../../../../van-dao/skills/truong-mon/SKILL.md#L18)

**Cơ chế hai lớp `customize.toml` — lần đầu chạy thật trong codebase**

- Luật gộp theo từng trường con, không thay nguyên object — chỗ dễ hiểu sai nhất
  [`SKILL.md:29`](../../../../van-dao/skills/truong-mon/SKILL.md#L29)

- Lớp gốc, hình dạng bảng hai khoá đã chốt ở Design Notes
  [`customize.toml:8`](../../../../van-dao/skills/truong-mon/customize.toml#L8)

**Luồng chỉ điểm và máy trạng thái**

- Chọn nhánh A/B/C dựa trên trạng thái chỉ điểm đang treo
  [`SKILL.md:54`](../../../../van-dao/skills/truong-mon/SKILL.md#L54)

- Nhánh C bước 3: luật chống bịa (5 trường) + loại sách đã báo tìm không ra (patch review)
  [`SKILL.md:99`](../../../../van-dao/skills/truong-mon/SKILL.md#L99)

- Nhánh A: `khong_thay` ghi cả hai file, đưa quyển thay thế ngay trong cùng lượt
  [`SKILL.md:62`](../../../../van-dao/skills/truong-mon/SKILL.md#L62)

- Nhánh B: nhắc số quyển treo TRƯỚC khi hỏi thay — chốt trước khi lô cũ hết hiệu lực
  [`SKILL.md:71`](../../../../van-dao/skills/truong-mon/SKILL.md#L71)

**Đóng vòng bái sư → chỉ điểm**

- Bước cuối bái sư giờ mời tường minh sang `/van-dao:truong-mon`, không tự chuyển
  [`nhap-mon/SKILL.md:162`](../../../../van-dao/skills/nhap-mon/SKILL.md#L162)

**Nguồn sự thật — sửa đặc tả trước khi mã bám theo**

- Hình dạng `so_chi_diem` bổ sung vào §12.1; §10.2 sửa "Ba trạng thái" → "Năm trạng thái"
  [`dac-ta:1629`](../../../../docs/VAN-DAO-dac-ta-v1.0.md#L1629)

**Bằng chứng hành vi (đọc sau cùng)**

- 9 kịch bản chạy thật; id 7-9 là patch review: override thưa, auto-trigger, nhánh không-đồng-ý
  [`truong-mon/evals.json:1`](../../../../van-dao/skills/truong-mon/evals/evals.json#L1)

- Eval `nhap-mon` id 6/7 chạy lại sau khi Story 3 đổi hành vi — evidence cũ đã lỗi thời
  [`nhap-mon/evals.json:165`](../../../../van-dao/skills/nhap-mon/evals/evals.json#L165)
