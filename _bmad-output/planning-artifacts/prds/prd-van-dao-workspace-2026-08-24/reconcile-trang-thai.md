# Input Reconciliation — VAN-DAO-trang-thai-du-an.md vs prd.md

**Input:** `docs/VAN-DAO-trang-thai-du-an.md` (cập nhật 2026-08-24)
**Target:** `_bmad-output/planning-artifacts/prds/prd-van-dao-workspace-2026-08-24/prd.md`
**Method:** đọc toàn bộ hai file, đối chiếu §1-§10 của status doc với Vision/MVP Scope/Non-Goals/Success Metrics/Open Questions/Assumptions Index của PRD.

---

## Gap 1 — PRD không phản ánh trạng thái build/verify hiện tại (nền kỹ thuật xong, giá trị = 0%)

**Bằng chứng ở status doc:**
- §1: Implementation = "Nền kỹ thuật xong, vertical slice chưa bắt đầu" — chỉ có `kiem-bi-kip.py` + test + CI; `giam-dinh.py`, skill `thu-bi-kip`, `thu-linh` **chưa viết**.
- §1: Detailed design = "1/8" — 7/8 data contract cần cho Vòng 1-4 (kể cả `lo-do.schema.md` và `ho-so.schema.md`, cả hai đều Vòng 1, tức nằm trong MVP) **chưa có schema**.
- §10: "Bước 8 là lần đầu có người học thật, và là thứ duy nhất chạm được cột *giá trị* — cột duy nhất vẫn ở 0% sau tất cả những gì đã làm."
- §3: 31/34 requirement (91%) hiện chỉ verify được bằng người đọc transcript — tự gọi đây là "con số nghiêm trọng nhất trong tài liệu này."
- §4.2: Document review bắt được 0/11 defect; manual walkthrough bắt được 11/11 — bằng chứng thực nghiệm rằng soát tài liệu không đáng tin cho loại lỗi *thiếu ca* / *thiếu đường dữ liệu*.

**Trong PRD:** Không có mục nào nêu trạng thái triển khai hiện tại. §6 MVP Scope trình bày ranh giới Vòng 1-2 như một target, không kèm ghi chú là tính tới ngày PRD hoàn tất, **chưa có FR nào trong danh sách MVP được lập trình xong** — kể cả hai data contract (`lo-do`, `ho-so`) mà chính bảng MVP liệt kê (FR6, FR9a-c) đều còn thiếu schema.

**Vì sao đáng đưa vào PRD:** PRD là tài liệu sẽ dùng để cắt epic/story sau. Nếu không neo lại "MVP scope này hiện = 0% built, các data contract nền tảng còn thiếu 2/2 (Vòng 1)", người đọc PRD độc lập (không đọc kèm status doc) sẽ hiểu nhầm mức độ sẵn sàng.

**Đề xuất:** Thêm một dòng ngắn ở đầu §6 MVP Scope hoặc một entry Assumptions Index: "Tính tới ngày PRD này, MVP scope (Vòng 1-2) chưa có FR nào hoàn thiện — chỉ có hạ tầng validate (`kiem-bi-kip.py` + CI); `lo-do.schema.md`/`ho-so.schema.md` (cả hai chặn FR trong MVP) chưa viết." Không nhất thiết phải là Open Question (không phải câu hỏi cần quyết định) nhưng nên là một dòng trạng thái tường minh, hoặc ít nhất một câu dẫn ở §6.

---

## Gap 2 — Phụ thuộc ngoài "book-to-skill" (virgiliojr94) không xuất hiện ở đâu trong PRD

**Bằng chứng ở status doc:**
- §10 bước 2: "`bin/giam-dinh.py` + skill `thu-bi-kip` (Tàng kinh trưởng lão) — ba pha, dừng ở pha 2. **Phụ thuộc ngoài: `book-to-skill` (virgiliojr94)**."

**Trong PRD:** FR1 ("Hệ thống phải giải nghĩa được ý và nội dung cơ bản của một cuốn sách (PDF/EPUB)... đủ để làm nguồn cho việc dạy") nằm trong MVP (§6, bước 3) và là nền cho toàn bộ Vision ("biến bất kỳ cuốn sách PDF/EPUB nào... thành một lộ trình học"). Không có dòng nào trong Open Questions hay Assumptions Index nhắc tới việc FR1 phụ thuộc vào một plugin bên thứ ba cụ thể (`book-to-skill`, tác giả `virgiliojr94`).

**Vì sao đáng đưa vào PRD:** Đây là một phụ thuộc ngoài, cụ thể, đặt tên rõ, chặn thẳng vào FR1 — đúng loại rủi ro Assumptions Index đang dùng để ghi ("giả định phát sinh riêng trong PRD này"). Nếu plugin đó thay đổi API, ngừng bảo trì, hay không xử lý tốt định dạng sách có bảng/hình/công thức, FR1 vỡ mà PRD không có chỗ nào cảnh báo trước.

**Đề xuất:** Thêm một dòng vào Assumptions Index: "FR1 (giải nghĩa sách) phụ thuộc plugin bên thứ ba `book-to-skill` (virgiliojr94) cho bước trích xuất/giám định ban đầu — nếu plugin đổi hành vi hoặc ngừng bảo trì, `bin/giam-dinh.py` phải viết lại phần đó." Đây gần với dòng giả định đã có sẵn ("Model giải nghĩa đúng ý từ PDF/EPUB...") nhưng là một rủi ro khác: rủi ro *công cụ*, không phải rủi ro *chất lượng hiểu*.

---

## Gap 3 — Rủi ro "đặc tả quá lớn so với bằng chứng" (Cao, rủi ro #1 đã đổi) không có trong Open Questions/Assumptions Index

**Bằng chứng ở status doc §8 (bảng RỦI RO):**
- "**Đặc tả quá lớn so với bằng chứng** | **Cao** | 2.112 dòng, 34 requirement, 28 component — cho một người dùng chưa học xong chương nào"
- Và câu kết: "**Rủi ro số một đã đổi.** Trước walkthrough nó là 'đặc tả chưa đủ chín'. Giờ là 'đặc tả quá chín so với thứ đã chạy' — mỗi dòng thêm vào là một dòng phải dựng đúng."

**Trong PRD:** Không xuất hiện. Assumptions Index có 6 dòng giả định phát sinh riêng cho PRD (FR1 hiểu sách, FR2-FR5 sư phạm AI, FR9a-c trực giao, FR5 mastery cho tâm pháp, FR16 độ tản mát, n=1). Không dòng nào nói tới rủi ro *quy mô đặc tả vượt bằng chứng thực chạy* — đây là rủi ro ở tầng khác (tầng dự án/tiến độ, không phải tầng một FR cụ thể), nhưng chính status doc xếp nó là rủi ro Cao và là rủi ro đứng đầu.

**Vì sao đáng đưa vào PRD:** PRD đang mô tả một MVP khá lớn (Vòng 1-2, 16 FR) dựa trên một đặc tả 2.112 dòng — nếu PRD không neo lại rằng bản thân đặc tả nền đó còn "quá chín so với thứ đã chạy", MVP Scope có thể bị đọc là đã được kiểm chứng vững hơn thực tế.

**Đề xuất:** Thêm dòng vào Assumptions Index (không phải Open Question vì không có quyết định cụ thể cần treo — đây là tình trạng cần theo dõi): "Đặc tả nền (`VAN-DAO-dac-ta-v1.0.md`, 2.112 dòng / 34 requirement / 28 component) lớn hơn nhiều so với phần đã chạy thật (0 người học hoàn thành một chương). Nếu sai ở tầng thiết kế cơ bản, MVP Scope ở §6 có thể phải viết lại một phần — mỗi vòng đã hoàn thành hạ tầng (kiem-bi-kip.py) từng phải sửa 3 trường sau khi chạy thật, dấu hiệu các schema còn lại (7/8) nhiều khả năng cũng vậy."

---

## Gap 4 — "Bốn cơ chế không kiểm được ở giai đoạn này" (§17.1, Trung bình) không được PRD nhắc tới, dù có thể chạm MVP FR4/FR5

**Bằng chứng ở status doc:**
- §4.3: "Bốn cơ chế còn lại ở §17.1 đặc tả **không mô phỏng được** — chúng cần thời gian trôi hoặc lặp lại thật."
- §8 (bảng rủi ro): "Bốn cơ chế không kiểm được ở giai đoạn này | Trung bình | §17.1 — đã ghi nhận, không phải việc bỏ sót"

**Trong PRD:** Không nhắc tới §17.1 hay "bốn cơ chế không kiểm được" ở đâu. FR4/FR5 (MVP, §6: "giàn giáo co giãn... tăng lại khi vấp"; "mastery gate") là loại cơ chế phụ thuộc lặp lại/thời gian thật để lộ ra — đúng mô tả của nhóm "bốn cơ chế" này (dù status doc không nêu tên cụ thể bốn cơ chế đó, chỉ trỏ tới §17.1 đặc tả).

**Vì sao đáng đưa vào PRD:** Đây là một giới hạn đã biết trước của phương pháp verify (walkthrough thủ công không mô phỏng được) áp trực tiếp lên một phần cơ chế nằm trong MVP Scope (FR4/FR5, Vòng 2). Assumptions Index hiện có dòng cho FR5 ("Mastery learning áp dụng tốt như nhau cho công pháp và tâm pháp") nhưng không có dòng nói rằng **một số cơ chế trong MVP về nguyên tắc không kiểm được cho tới khi có người học thật lặp lại nhiều lần** — đây là giả định phương pháp khác, không trùng với giả định sư phạm đã ghi.

**Đề xuất:** Thêm dòng Assumptions Index: "Một số cơ chế trong Dạy (đặc biệt phần giàn giáo co giãn theo thời gian ở FR4) không kiểm chứng được bằng walkthrough một lần hay đọc lại đặc tả — chỉ lộ ra qua lặp lại thật (§17.1, §4.3 status doc). MVP có thể ra mắt với các cơ chế này *chưa* được xác nhận hoạt động đúng như thiết kế."

---

## Gap 5 — Rủi ro "dựng xong thì hết hứng" (n=1 continuity risk) không trùng với Success Metric #3 hiện có

**Bằng chứng ở status doc §8:** "Dựng xong thì hết hứng | Trung bình | Rủi ro cố hữu của dự án n=1, đã chấp nhận khi chọn bậc 3" — đây là rủi ro tác giả (người xây) mất hứng thú *trước khi* sản phẩm chạm tới giá trị thật, không phải rủi ro người dùng bỏ cuộc sau khi đã dùng xong.

**Trong PRD:** Success Metric #3 ("Quay lại học quyển thứ hai sau khi xong quyển đầu — không bỏ cuộc vì ma sát UX") đo hành vi *người dùng sau khi sản phẩm đã hoạt động* — khác đối tượng và khác thời điểm với rủi ro "dựng xong thì hết hứng" của status doc, vốn nói về khả năng dự án bị bỏ dở *trong lúc xây*, trước khi có ai học xong quyển nào.

**Vì sao đáng đưa vào PRD (nhẹ hơn 4 gap trên):** Không bắt buộc — đây là rủi ro vận hành/dự án hơn là rủi ro sản phẩm, và PRD không nhất thiết phải ghi rủi ro về ý chí cá nhân của tác giả. Nêu ra để cân nhắc: nếu PRD muốn Assumptions Index đầy đủ theo tinh thần "n=1 là ràng buộc thật" (đã có dòng riêng), có thể đáng thêm một câu ngắn phân biệt hai rủi ro n=1 khác nhau (rủi ro về giả định người dùng thứ 2 vs. rủi ro về việc tác giả bỏ dở dự án).

---

## Điểm đã kiểm và thấy PRD phủ đủ (không phải gap)

- **κ calibration schedule constraint (§7.1 status doc)** — đã khớp với PRD FR18 và Open Question #2 ("Việc chấm ở MVP chưa có hiệu chuẩn nào xác nhận đáng tin"). Không cần thêm.
- **"Hai giả định nền chưa kiểm" (§8 status doc, trỏ §17 đặc tả)** — khớp với câu PRD Assumptions Index: "Mục 2 và 3 của bảng đó (model chấm theo rubric, model đọc cảnh giới) đã lên Open Questions §8." Coi như đã phản ánh, dù PRD Open Question #2 chỉ viết rõ phần "model chấm theo rubric" — phần "model đọc cảnh giới" (mục 3) chưa có câu riêng trong nội dung Open Question #2, chỉ được nêu tên trong ngoặc. Nhẹ, không tách thành gap riêng vì đã được trỏ tới.
- **`canh-gioi.md` chặn bởi tra Dreyfus bản gốc (§7.2, §2.2 status doc)** — một phần đã phản ánh gián tiếp qua FR17 (trích Gobet & Chassy 2009 về việc mô hình Dreyfus thiếu bằng chứng thực nghiệm mạnh) và qua việc FR14-19 đã bị đẩy hết ra khỏi MVP (Để Vòng 4). Không tách thành gap riêng.
- **Nợ kỹ thuật "chưa có remote git" (§5 status doc)** — rủi ro vận hành thuần túy (mất code nếu hỏng máy), không phải rủi ro sản phẩm/yêu cầu. Hợp lý để ở ngoài PRD; không đề xuất thêm.

---

## Tóm tắt cho việc tiếp bước Finalize

5 gap tìm được, xếp theo mức nên ưu tiên xử lý:
1. Trạng thái build/verify hiện tại vắng mặt trong PRD (Gap 1) — nên thêm.
2. Phụ thuộc ngoài `book-to-skill` chưa ghi nhận (Gap 2) — nên thêm vào Assumptions Index.
3. Rủi ro "đặc tả quá lớn so với bằng chứng" (Gap 3) — nên thêm vào Assumptions Index.
4. "Bốn cơ chế không kiểm được" chạm FR4/FR5 MVP (Gap 4) — nên thêm vào Assumptions Index.
5. Rủi ro "dựng xong thì hết hứng" khác Success Metric #3 (Gap 5) — tuỳ chọn, mức độ thấp.
