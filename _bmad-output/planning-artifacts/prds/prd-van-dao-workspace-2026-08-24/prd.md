---
title: "PRD: Vấn Đạo"
status: "final"
created: "2026-08-24"
updated: "2026-08-26"
---

# PRD: Vấn Đạo

## 1. Vision

**Vấn Đạo là một plugin Claude Code biến sách PDF/EPUB bạn đã có sẵn (chủ yếu dạng văn bản) thành một lộ trình học có AI đồng hành sát sao — giải thích đủ để bạn nắm ý, rồi hỏi ngược từng bước tới khi bạn thật sự vận dụng được vào việc thật, không dừng ở "đọc xong".**

Người tự học đọc xong một chương và tưởng đã hiểu — cho tới khi phải dùng vào việc thật mới lộ ra chỗ chưa nắm chắc. Tóm tắt AI đọc nhanh nhưng không kiểm tra hiểu; tự học một mình không có ai hỏi ngược. Vấn Đạo lấp khoảng đó bằng một quy trình có cấu trúc: giải thích ngắn gọn trước, dạy từng ý một kèm câu hỏi, và **không công nhận đã hiểu chỉ vì trả lời đúng một câu** — phải qua một bài kiểm tra đòi vận dụng vào tình huống mới, được chấm độc lập bởi một AI tách biệt với AI vừa dạy. Nhưng đây không phải một cửa chặn giữ bạn lại — mọi kết quả là phản chiếu trả về cho chính bạn tự quyết định học tiếp thế nào; hệ không gác cổng ai, kể cả khi chưa đạt.

Khác biệt cốt lõi không nằm ở nội dung (sách là của người học, không phải của Vấn Đạo) mà ở **cấu trúc kiểm chứng**: nhiều vai AI chuyên trách — dạy, hỏi ngược, chấm, soát — được phân tách rõ ràng để một vai không thể vừa dạy vừa tự cho qua bài của chính mình. Đây là sản phẩm cho **chính tác giả trước tiên** (n=1), mã nguồn mở để ai muốn cũng tự dùng cá nhân được — không phải một dịch vụ nhắm số đông.

## 2. Đối tượng người dùng

**Ai:** Người tự học bằng sách PDF/EPUB đã có sẵn — có thể là sách theo nghề/vai cụ thể (lập trình, phân tích nghiệp vụ, kiểm thử, quản lý...) hoặc sách về năng lực nền dùng được ở mọi vai (tư duy, giao tiếp, dẫn dắt...) — không qua khoá học có người dạy trực tiếp. Người dùng được xác nhận duy nhất tính tới bản đầu là **chính tác giả** (n=1) — mọi giả định về người dùng khác đều suy ra từ nhu cầu của tác giả, chưa có xác nhận từ người dùng thứ hai nào. Mã nguồn mở nên người khác có thể tự cài dùng cho riêng mình, nhưng đó không phải mục tiêu thu hút người dùng của bản đầu.

**Job cần làm (JTBD):** "Khi tôi đọc một cuốn sách — dù để làm được việc theo một vai cụ thể hay để xây năng lực nền dùng chung mọi việc — tôi muốn biết chắc là mình đã thật sự nắm được nội dung, không phải chỉ nhớ được chữ, để tôi tự tin dùng được kiến thức đó khi cần."

**Vì sao việc này chưa được giải quyết tốt:**
- Tóm tắt AI (kiểu NotebookLM) đọc nhanh nhưng không kiểm tra hiểu — chỉ tự người học *cảm thấy* đã hiểu.
- Tự học một mình không có ai hỏi ngược khi hiểu sai.
- Ghi chú tay, gạch chân không ai đọc lại, không phản hồi.

**Điều kiện thật để dùng được:** đã có sẵn PDF/EPUB (Vấn Đạo không tìm hay cấp sách), đang chạy Claude Code, chấp nhận nhịp học chậm (giải thích ngắn → hỏi ngược → chấm) thay vì đọc lướt nhanh.

**Không phải người dùng mục tiêu ở bản đầu:** người cần chứng chỉ/bằng cấp chính thức; người chưa có sách cụ thể trong đầu; nhóm nhiều người cùng học một bí kíp.

## 3. Thuật ngữ

### Thế giới quan

| Từ | Nghĩa |
|---|---|
| **Bí kíp** | Một quyển sách nhiều chương, đã đưa vào kho riêng của người học |
| **Tàn quyển** | Bài lẻ (một bài web, một chương rời) — không có lộ trình |
| **Công pháp** | Bí kíp theo nghề/vai cụ thể — học được là dùng ngay |
| **Tâm pháp** | Bí kíp theo năng lực nền — chậm hơn, nhưng dùng được ở mọi vai |
| **Mạch** | Một trục năng lực xuyên nhiều bí kíp (ví dụ: tư duy phân tích) |
| **Cảnh giới** | Năm bậc năng lực trên một mạch, theo mô hình Dreyfus |
| **Chương / Quyển / Mạch** | Ba tầng đột phá — đột phá chương (qua một ý), đột phá quyển (qua khảo thí), đột phá cảnh giới (lên bậc trên mạch) |
| **Lộ đồ** | Kế hoạch học cả quyển, người học duyệt trước khi bắt đầu |
| **Giáo án** | Kế hoạch dạy một chương, do Thư linh soạn trước khi dạy |
| **Khảo thí** | Bài kiểm tra cuối quyển — điều kiện đột phá quyển |
| **Đạo tâm** | Sổ nhật ký con đường học của người học |
| **Tâm ma** | Cách làm cũ người học mang sẵn vào, có thể bẻ cong thứ học sau |
| **Xuất quan** | Bỏ học giữa chừng — tạm dừng hợp lệ, không phải kết thúc |
| **Chú giải** | Lớp ghi chú người học bồi thêm lên bí kíp gốc (bí kíp gốc không đổi) |
| **Cờ bất đồng** | Bản ghi khi hai AI chấm độc lập không khớp kết quả — không chặn người học, nhưng được lưu lại để xem xét |
| **Tám vai** | Trưởng môn (giữ bản đồ, chỉ đường) · Tàng kinh trưởng lão (giám định, thu sách) · Thư linh (dạy, hỏi ngược) · Giám khảo (ra đề, coi thi) · Sơn phong trưởng lão (định cảnh giới) · Nghiệm Công Sứ (chấm theo tiêu chí) · Phúc Khảo Sứ (soát độc lập ở khảo thí) · Chú Giải Sứ (bồi chú giải) |

### Kỹ thuật

| Từ | Nghĩa | Vì sao PRD cần |
|---|---|---|
| **Subagent tươi / Fork** | Vai chấm chạy trên ngữ cảnh sạch, không kế thừa hội thoại vai dạy; **fork** (kế thừa hội thoại) bị cấm dùng cho việc chấm | Cơ chế đứng sau lời hứa "một AI khác, tách biệt, kiểm tra" — cần thành NFR kiểm được |
| **Nhãn vs dấu hiệu** | *Nhãn* là bậc cảnh giới (cần đủ bằng chứng); *dấu hiệu* là điều quan sát được, nói ngay được | Nền cho cam kết "không công bố bậc khi κ thấp — chỉ nêu dấu hiệu" |
| **κ (kappa)** | Mức khớp giữa nhãn người chấm và bậc model khi hiệu chuẩn | Ngưỡng κ < 0,6 → không công bố bậc là cam kết đã tuyên bố công khai — ứng viên Success Metric |
| **Ca đối chứng** | Chạy hai lần, một lần cố tình thêm ngữ cảnh bị cấm, để chứng minh ràng buộc "không đọc X" thật sự có tác dụng | Cách duy nhất kiểm được lời hứa "chấm độc lập" không chỉ là lời nói — NFR/quality-gate |
| **Tiêu chí không phân biệt** | Tiêu chí mà người chưa đọc chương cũng đạt — vô dụng dù chấm khớp | Điều kiện để lời hứa "chấm có căn cứ" có nghĩa, không chỉ là chấm khớp nhau |
| **Trigger eval / Behavioral eval** | Kiểm skill có được gọi đúng lúc, và có chạy ra đúng kết quả | Quality-gate cho *mọi* skill trong PRD (đã quyết định ở memlog) |

Phần thuần cơ chế xây dựng (harness, compaction, context rot, `pham_vi_doc`, `.pham-vi.json`, điểm neo, chỉ ghi thêm, loại 1·2·3) đã là nguồn sự thật đầy đủ ở `docs/VAN-DAO-dac-ta-v1.0.md` §0.2 — không chép lại ở đây hay ở addendum, chỉ trích dẫn khi cần.

## 4. Features

*Rút ra bằng brainstorm Round Robin theo nhóm năng lực, có research làm nền cho từng điểm (nguồn trích trong `.memlog.md`).*

### 4.1 Thu sách

- **FR1** — Hệ thống phải giải nghĩa được ý và nội dung cơ bản của một cuốn sách (PDF/EPUB) — không chỉ trích xuất chữ nguyên văn — đủ để làm nguồn cho việc dạy. Khi gặp nội dung có độ tin cậy giải nghĩa thấp (bảng, công thức, code dày đặc), hệ phải **tự đánh dấu** chỗ đó — không âm thầm coi như đã giải nghĩa đủ *("đủ để làm nguồn" tự nó không kiểm được — đánh dấu là ngưỡng tối thiểu kiểm được, không phải giải quyết trọn vẹn vấn đề)*.

- **FR37** — Pha thiết kế sư phạm (pha 2 của thu bí kíp) phải **dừng chờ người dùng sửa và duyệt** trước khi sinh cấp chương — máy chỉ đề xuất kèm lý do cho từng đề xuất, không tự quyết xương sống/tiêu chí đạt/điểm hạ sơn *(nguồn: đặc tả §6.2 — "người bắt buộc chen vào pha 2: xương sống, tiêu chí đạt và điểm hạ sơn chỉ người có nghề quyết được; model đoán ra thứ nghe hợp lý mà sai, và cái sai truyền xuống mọi chương". Phát hiện qua Input Reconciliation lần 2 (bmad-prd, 2026-08-26) — lần 1 bỏ sót vì nội dung nằm chủ yếu trong sơ đồ §6.2, không phải văn xuôi)*.
- **FR38** — Khi không rút được chữ từ file đưa vào, hệ phải **dừng ngay**, báo "bản này không rút được chữ, tìm bản khác" — không OCR, không tạo bí kíp rỗng hay đoán liều nội dung *(nguồn: đặc tả §6.1/§6.2. Phát hiện qua Input Reconciliation lần 2)*.
- **FR39** — Một bí kíp có hai mức hợp lệ: **đủ dùng** (vào kho, học được ngay — mục tiêu, giả định nền, tiêu chí đạt thô, ≥1 câu vận dụng) và **đủ chuẩn** (chia sẻ được — thêm tiêu chí chi tiết, sai lầm phổ biến, worked example, bồi dần **sau khi học chương đó**, không theo lịch). Khi dạy ở mức đủ dùng, Thư linh phải nói rõ đang chấm theo mục tiêu, chưa có tiêu chí chi tiết — không để người học tưởng đang được chấm chặt hơn thực tế *(nguồn: đặc tả §6.5 "Hai mức hợp lệ — thu rồi bồi dần"; ở n=1 người học luôn là người đầu tiên dùng bản chưa bồi — đây là hạn chế cấu trúc, không phải thiếu sót. Phát hiện qua Input Reconciliation lần 2)*.

### 4.2 Dạy

- **FR1a** — Trước khi dạy từng ý theo hỏi ngược (FR2), hệ phải trình bày một bản tóm lược/mô hình tổng quan của chương — khái niệm cốt lõi và cách chúng liên hệ với nhau, dựa trên lớp giải nghĩa đã có ở FR1 — để người học có khung tham chiếu trước khi đi vào từng ý chi tiết; bản tóm lược **không thay thế** việc hỏi ngược, chỉ là bước chuẩn bị nhận thức đứng trước nó *(đánh số theo FR1 vì tiêu thụ trực tiếp đầu ra giải nghĩa của FR1, nhưng đặt ở §4.2 vì là hành vi Dạy, không phải Thu sách — nguồn: "supportive information", thành phần thứ hai của mô hình 4C/ID — van Merriënboer & Kirschner, Ten Steps to Complex Learning: A Systematic Approach to Four-Component Instructional Design, 3rd ed., Routledge 2018; gốc từ van Merriënboer, Clark & de Croock 2002, Educational Technology Research and Development 50(2) — thông tin hỗ trợ phải trình bày TRƯỚC learning task và sẵn có suốt quá trình luyện tập, giúp người học xử lý khía cạnh phi thường quy của nhiệm vụ)*.
- **FR2** — Không dạy tiếp mà không hỏi ngược: mỗi ý phải chốt bằng một câu hỏi, chờ người học trả lời trước khi đi tiếp *(nguồn: retrieval practice — Roediger & Karpicke 2006)*.
- **FR2a** — Khi một câu nghiệm công đang treo (chưa chấm xong), Thư linh **không được đáp câu hỏi trùng với câu đang treo đó** — phải hỏi ngược lại người học, và nếu cần giảng lại thì dùng ví dụ khác, không dùng đúng ca đang được nghiệm công *(nguồn: đặc tả §7.0 "Bế quan một chương", quy tắc R5. Phát hiện qua Input Reconciliation lần 2 — cơ chế chống rò rỉ đáp án qua kênh hỏi-đáp trong lúc chờ chấm, nằm trong nhánh tô đỏ của sơ đồ §7.0, chưa có FR nào phủ)*.
- **FR3** — Quan niệm cũ (cách làm trước đây của người học) phải được nêu thành lời và đối chất trước khi dạy nội dung mới trái với nó — không lặng lẽ nhồi đè lên *(nguồn: conceptual change — Posner, Strike, Hewson & Gertzog 1982)*.
- **FR3a** — Sau khi quan niệm cũ được nêu thành lời (FR3, "tâm ma"), Thư linh **không được tự tuyên bố** quan niệm cũ đã gỡ — chỉ lời người học thừa nhận xung đột đưa trạng thái tới "đang gỡ" (`dang_go`); chuyển sang "đã gỡ" (`da_go`) đòi **bằng chứng trong bài** (nghiệm công/khảo thí, người học làm khác đi thật) — thừa nhận bằng lời KHÔNG bằng gỡ được. Nếu dấu hiệu cũ xuất hiện lại sau khi đã gỡ, chuyển "tái phát" (`tai_phat`) — trạng thái riêng, không gộp về "chưa gỡ" ban đầu, vì người học từng vượt qua được. Người học bảo cách cũ vẫn đúng trong hoàn cảnh của họ thì đóng, không ép *(nguồn: đặc tả §5.12 "Tâm ma", quy tắc R18 "thừa nhận ≠ gỡ". Phát hiện qua Input Reconciliation lần 2 — lần 1 bỏ sót vì vòng đời 4 trạng thái nằm trong sơ đồ state diagram §5.12, không phải văn xuôi; FR3 gốc chỉ phủ bước đầu "nêu thành lời", thiếu hẳn guardrail chống kết luận vội)*.
- **FR4** — Mức gợi ý/giàn giáo phải co giãn theo tình trạng thật của người học: đủ chi tiết khi mới, giảm dần khi vững, **tăng lại khi vấp** (sai lần hai ở cùng chỗ → đổi cách trình bày; sai lần ba cùng chỗ → báo lên, không giảng lại lần nữa) — không chỉ giảm một chiều *(nguồn: fading + worked examples — Sweller & Cooper 1985)*.
- **FR5** — Chỉ tính một ý/chương là "đạt" khi người học chứng minh vận dụng được vào tình huống cụ thể, không phải nhớ đúng chữ; chưa đạt thì được hỗ trợ thêm rồi thử lại *(nguồn: mastery learning — Bloom 1968)*.
- **FR6** — Lộ đồ (kế hoạch học cả quyển) phải được trình người học duyệt trước khi bắt đầu học, kèm số chương và ước lượng thời lượng (đánh dấu rõ đây là ước lượng thô, không phải cam kết) — không tự ý bắt đầu dạy khi chưa có sự đồng ý về lộ trình *(F-1 — §16 bước 5; khớp lời hứa Press Release "cho biết trước mất bao lâu, bao nhiêu chương"; nguồn: Backward Design — Wiggins & McTighe, Understanding by Design, 1998/2005 — xác định mục tiêu và bằng chứng đo được TRƯỚC khi thiết kế hoạt động dạy; đã khai ở đặc tả §2 "Thư linh: Backward design + retrieval practice — bằng chứng viết trước, nội dung sau", chưa từng truyền xuống PRD trước bản cập nhật này)*.
- **FR7** — Giáo án (kế hoạch dạy một chương) phải được soạn ra file trước khi dạy mỗi chương — không ứng biến không ghi lại *(F0 — §16 bước 5; cùng nguồn Backward Design ở FR6 — giáo án là "hoạt động dạy" của Stage 3, chỉ soạn sau khi lộ đồ/mục tiêu và bằng chứng khảo thí (FR9/FR10) đã có hướng)*.

### 4.3 Soát

- **FR8** — Vai dạy và vai chấm phải là hai tiến trình AI tách biệt; vai chấm không kế thừa hội thoại dạy (không dùng fork) *(lý do: tránh xung đột lợi ích của việc tự dạy tự công nhận — nguyên tắc tách vai instructor/assessor đã ghi nhận trong giáo dục, dù còn hiếm gặp trong thực tế)*.
- **FR9** — Giám khảo (sinh đề, coi thi) không được chấm — tách biệt khỏi vai chấm (Nghiệm Công Sứ, Phúc Khảo Sứ) *(căn cứ: NCME Position Statement on Test Security — giám khảo phải độc lập hoàn toàn khỏi bài làm mình chấm để tránh xung đột lợi ích; cụ thể hoá bằng quy tắc R20 của đặc tả, tự nó bắt nguồn từ đặc tả §2 "Giám khảo: Tách ra đề khỏi chấm — coi thi và chấm thi là hai người, cùng một vai thì nới đề cho vừa bài" — một nguyên tắc thiết kế tự đặt tên của dự án, không phải trích dẫn học thuật ngoài, nay có thêm NCME làm khung ngoài song song)*.
- **FR10** — Mọi phán quyết đạt/chưa đạt của Nghiệm Công Sứ phải trích được câu cụ thể trong bài làm để làm căn cứ trước khi khẳng định — không kết luận suông *(căn cứ: quy tắc R19 của đặc tả — "mẫu quan trọng nhất được mượn", tự nó bắt nguồn từ đặc tả §2 "Nghiệm Công Sứ: Rubric neo + bằng chứng trước khẳng định — chấm theo tiêu chí, mỗi phán quyết phải trích được câu làm căn cứ"; đây là nguyên tắc thiết kế tự đặt tên của dự án — chưa tìm được khung học thuật ngoài cụ thể sau 3 vòng tìm kiếm — xem Open Questions §8 mục 6)*.
- **FR11a** — Ở mức khảo thí (cuối quyển), phải có người soát thứ hai chấm độc lập theo mục tiêu gốc, không đọc tiêu chí chi tiết *(nguồn: Ofqual 2014, "Review of Double Marking Research" — soát mù, không thấy điểm/căn cứ của người trước, phát hiện chấm sai đáng tin hơn giám khảo biết trước kết quả)*.
- **FR11b** — Hai người soát **cố ý không bàn bạc với nhau**, giữ trực giao để bắt loại lỗi khác nhau *(cùng nguồn Ofqual 2014 ở trên — bàn bạc làm mất chính lợi thế của soát mù)*.
- **FR11c** — Chấp nhận đánh đổi có chủ đích: tần suất cờ bất đồng có thể cao hơn mức đạt được nếu cho thương lượng lại — đổi lấy khả năng bắt lỗi khác loại *(nguồn: Cannings, Hawthorne, Hood & Houston 2005, Medical Education 39:299-308 — double marking thực tế trong dữ liệu y khoa chỉ khớp 36,8-39,8% số bài, κ trọng số thấp 0,12; và Ofqual 2014 — double marking gần đây chỉ nhỉnh hơn single marking một chút, không phải khớp gần tuyệt đối. Hai nguồn cùng hậu thuẫn: kỳ vọng khớp cao là phi thực tế, "chấp nhận đánh đổi" là lựa chọn đúng, không phải hạ chuẩn)*.
- **FR12a** — Khi hai bên chấm không khớp (hoặc một bên không kết luận được), hệ phải ghi lại thành "cờ bất đồng" và không chặn người học ở bất kỳ nhánh bất thường nào; khi bằng chứng cân bằng, kết quả luôn nghiêng về hướng có lợi cho người học.
- **FR12b** — Cờ bất đồng **không bị giấu đi** — người học xem được nếu chủ động mở đạo tâm — nhưng hệ **không tự đẩy thông báo** giữa lúc đang học, tránh ngắt luồng. *(Ở MVP, "mở đạo tâm" là mở trực tiếp file nhật ký — không có lệnh `/vd:*` riêng để đọc lại; thêm lệnh chỉ để đọc là phình phạm vi không cần thiết ở bản đầu. Màn "tiến độ" tổng hợp thuộc Vòng 3 — §16 bước 17 — chưa có ở MVP, xem §6.)*

### 4.4 Định hướng

- **FR13** — Gợi ý (học gì tiếp, sách nào phù hợp) luôn kèm lối tự nhập; không ép người học theo một hướng duy nhất *(nguồn: autonomy support — Self-Determination Theory, Deci & Ryan; và Developmental Advising — O'Banion 1972, mô hình chuẩn của NACADA — cố vấn là đối tác cùng khám phá với người học, đối lập "prescriptive advising" chỉ định một chiều; khác khía cạnh 4C/ID đã khai cho Trưởng môn ở đặc tả §2 (xếp lớp nhiệm vụ theo độ phức tạp) — hai khung phủ hai mặt khác nhau của cùng vai, không trùng)*.
- **FR14** — Mọi gợi ý phải nói rõ nguồn: dựa trên dữ liệu thật (lịch sử học, hồ sơ) hay chỉ là suy đoán của model *(nguồn: minh bạch nguồn gợi ý — nghiên cứu explainable recommendation)*.
- **FR15** — Khi một gợi ý là suy đoán (không có dữ liệu xác nhận), hệ phải **bắt người học xác nhận thêm** trước khi coi gợi ý đó là đã chấp nhận — không dừng ở một nhãn thụ động dễ bị lướt qua *(nguồn: appropriate reliance — giải thích/dán nhãn không đủ để tránh quá-tin-tưởng)*.

### 4.5 Đo

- **FR16** — Tuyên bố "đang ở bậc X" trên một mạch chỉ được đưa ra khi có **≥2 nguồn bằng chứng độc lập** (bài nộp từ nhiều bí kíp khác nhau cùng mạch; nguồn: ≥2 nguồn cao hơn thực tế chuẩn ngành — khảo sát cho thấy 54% chứng chỉ thật chỉ dùng một nguồn bằng chứng).
- **FR17** — Không công bố bậc (nhãn) khi độ khớp hiệu chuẩn κ dưới ngưỡng 0,6 — chỉ nêu dấu hiệu quan sát được, không gắn tên bậc *(nguồn: thang diễn giải κ — Landis & Koch 1977, Biometrics 33(1), 159-174, quy ước 0,61-0,80 là "substantial agreement", 0,41-0,60 là "moderate"; lưu ý trung thực: hai tác giả tự thừa nhận thang này dựa trên ý kiến cá nhân, không có bằng chứng thực nghiệm hậu thuẫn — khớp đúng tinh thần FR19: khung cảnh giới là giả thuyết, không phải phép đo đã kiểm chứng)*.
- **FR18** — Việc định bậc chạy nhiều lần độc lập trên cùng bằng chứng; **độ tản mát giữa các lần chạy dùng làm thước đo độ tin** — gọi đúng tên là "đa mẫu, đo độ tản mát", **không gọi là "self-consistency"** *(lý do: kỹ thuật self-consistency gốc — Wang et al. 2022 — chỉ kiểm chứng cho bài toán có một đáp án đóng đúng/sai, không phải phán đoán chủ quan như định bậc — dùng lại tên đó là mượn uy tín của một kỹ thuật cho việc nó chưa từng được kiểm chứng)*.
- **FR19** — Mọi nội dung nói với người dùng về cảnh giới/bậc phải khung nó là **một giả thuyết đang được kiểm chứng**, không phải một phép đo đã được khoa học xác nhận *(nguồn: mô hình Dreyfus thiếu bằng chứng thực nghiệm mạnh — Gobet & Chassy 2009; cam kết này đã tuyên bố công khai ở PRFAQ Customer FAQ, cần giữ nhất quán)*.
- **FR20** — Trước khi dùng để công bố cảnh giới, hệ phải hiệu chuẩn: so khớp kết quả model với người chấm tay trên tối thiểu 20 mẫu (phủ nhiều mạch, nhiều mức), tính κ; κ < 0,6 thì không công bố kết luận, phải hiệu chuẩn lại. *(Chỉ gate việc công bố bậc — không gate FR8-FR12 ở Soát, vốn chạy độc lập với cơ chế đo cảnh giới này.)*
- **FR21** — Báo cáo hiệu chuẩn phải kèm **% khớp thô song song với κ**, không báo κ một mình *(lý do: tránh nghịch lý kappa khi một loại kết quả áp đảo; chuẩn phổ biến, chi phí thấp trong đo lường liên-người-chấm)*.

### 4.6 Nền

- **FR22** — Sổ đạo tâm phải do chính người học tự ghi; không vai nào (kể cả AI) được ghi hộ hoặc tự soạn sẵn để duyệt, dù bản AI viết có thể "tốt hơn" về hình thức *(nguồn: quyền sở hữu tâm lý từ tự-tác-giả quyết định cam kết hơn chất lượng khách quan của nội dung — Pierce, Kostova & Dirks 2003; xác nhận trực tiếp lý do quy tắc R32/R33 của đặc tả tắt model-invocation cho `dao-tam`)*.
- **FR23** — Nghi thức/cột mốc (bái sư, thu bí kíp, đột phá cảnh giới) chỉ được kích hoạt khi có việc thật đứng sau — không phát cho hành động không tốn công thật *(nguồn: tránh hiệu ứng crowding-out đã có bằng chứng trong nghiên cứu gamification — thưởng tách khỏi tiến bộ thật làm giảm động lực nội tại)*. Việc thật cụ thể cho từng nghi thức: **bái sư** kích hoạt khi đã khai xong vai/mạch và ghi nhập môn ký; **thu bí kíp** kích hoạt khi người học đã tự tìm và đưa được một quyển vào kho; **đột phá cảnh giới** kích hoạt khi Sơn phong trưởng lão định bậc cao hơn lần trước, có căn cứ. Ba nghi thức này sẵn sàng ở các mốc khác nhau: bái sư và thu bí kíp dùng được ngay ở MVP; đột phá cảnh giới cần cơ chế Đo (FR16-FR21), chưa có ở MVP — xem §6. **"Ghi nhập môn ký"** dùng chung hạ tầng tự-ghi/`disable-model-invocation` với đạo tâm (FR22) nhưng đứng trên **căn cứ khác**: Cialdini, *Influence* (1984/2006) — nguyên tắc Commitment and Consistency, cam kết tự viết tay chủ động (không phải xác nhận thụ động) làm tăng khả năng theo đuổi cam kết sau này. Khác FR22 (Pierce, Kostova & Dirks 2003 — sở hữu tâm lý với công sức ĐÃ bỏ ra): nhập môn ký là cam kết viết TRƯỚC khi có công sức nào, nên không dùng đúng lý do của FR22 dù dùng đúng cơ chế của nó.
- **FR24** — Nhánh hạ sơn/phục mệnh (mang kiến thức ra việc thật rồi báo lại) phải nhận cả báo cáo thất bại, không chỉ báo cáo thành công.
- **FR25** — Khi vào một chương mới phụ thuộc chương trước, hệ phải nhắc lại (không dạy lại từ đầu) nội dung liên quan đã học, trước khi dạy ý mới *(F6 — §16 bước 18; nguồn: Dunlosky, Rawson, Marsh, Nathan & Willingham 2013, Psychological Science in the Public Interest 14(1), 4-58 — distributed/spaced practice, kỹ thuật ích lợi cao nhất trong 10 kỹ thuật tổng hợp từ 242 nghiên cứu)*.
- **FR26** — Hết chương cuối một quyển, trước khi vào khảo thí, hệ phải hệ thống hoá lại các ý xuyên suốt các chương thành một cái nhìn toàn quyển *(F7 — §16 bước 18; nguồn: van Merriënboer & Kirschner, Ten Steps to Complex Learning, 3rd ed. 2018 — nguyên tắc xây lược đồ nhận thức (cognitive schema) xuyên suốt nhiệm vụ phức hợp trong 4C/ID, cùng khung đã dùng cho FR1a; KHÔNG dùng "summarization" của Dunlosky et al. 2013 — nghiên cứu đó xếp summarization đơn thuần vào nhóm ích lợi THẤP, còn FR26 là xây liên kết ý xuyên chương, không phải tóm tắt lại chữ)*.
- **FR27** — Khi người học quay lại một chương đang dở ở phiên mới, hệ phải hỏi lại một hai câu của chương trước để tự quyết định đi tiếp hay lùi lại ôn — không tự động coi như không có gì thay đổi, và không tính theo số ngày đã qua *(F8 — §16 bước 18)*.
- **FR28** — Bỏ giữa chừng là tạm dừng hợp lệ, không phải kết thúc: hệ phải giữ nguyên lộ đồ và giáo án khi người học dừng; quay lại thì vào thẳng FR27 (nối lại mạch cũ), không dựng lộ đồ mới *(F9 — §16 bước 18)*.
- **FR29** — Khi cùng một sai lầm lặp lại ở cùng một chỗ qua nhiều lần học, hệ phải bồi một ghi chú vào lớp chú giải riêng của chương đó — không sửa bí kíp gốc, và **không mang chi tiết tình huống thật của người học ra ngoài** (không tên người, công ty, dự án cụ thể) — đây là vai duy nhất có đầu ra rời khỏi máy người học *(Chú Giải Sứ — §16 bước 23, chặn bởi FR25-FR28; ràng buộc riêng tư theo quy tắc R12 của đặc tả)*.
- **FR30** — Khi cần gợi ý sách tiếp theo, một công cụ quét kho sách của người học phải trả về tối đa 3 lựa chọn kèm lý do — không phải cả danh sách kho *(`tra-tang-kinh-cac` — §16 bước 15)*.
- **FR31** — Tiến độ học (nhiều quyển, nhiều mạch) phải xem được dưới dạng bản đồ trực quan, dựng lại được bất cứ lúc nào từ file trạng thái — không phải nguồn lưu trữ chính của tiến độ *(`ban-do.py` + Artifact — §16 bước 17)*.
- **FR34** — Khi plugin được bật lần đầu, hệ phải giúp người học chọn ngôn ngữ giao tiếp qua `userConfig` — chọn đúng một lần, các phiên sau nạp lại, không hỏi lại *(số hiệu đặt ở cuối §4.6 dù không liền FR31 — phát hiện muộn hơn khi rà epic list; đánh số theo thứ tự phát hiện, không renumber toàn bộ, cùng cách đã làm với FR1a. Nguồn: cơ chế `userConfig` trong `.claude-plugin/plugin.json` của Claude Code, lưu vào `~/.claude/settings.json` phạm vi user; **verify chạy thật xong 2026-08-26** — field `communication_language` thêm vào `van-dao/.claude-plugin/plugin.json`, `claude plugin validate --strict` PASS, `claude plugin install --config` xác nhận lưu đúng vào `pluginConfigs["van-dao@van-dao"].options`. **Sửa lại một claim sai sau khi tự kiểm:** Claude Code KHÔNG tự động chặn/hỏi khi cài qua CLI không kèm `--config` — chỉ in cảnh báo và cài xong với field chưa đặt; đường cài tương tác thật (con người, không qua CLI headless) chưa verify được. Bước mở đầu (`nhap-mon`) phải tự kiểm tra field đã set chưa và chủ động hướng dẫn `/plugin configure` nếu chưa — không giả định Claude Code tự hỏi)*.
- **FR35** — Bái sư phải cho người học đặt tên riêng cho 4 vai trực tiếp nói chuyện với mình (Trưởng môn, Tàng kinh trưởng lão, Thư linh, Giám khảo) — gợi ý sẵn vài tên kèm cho phép tự nhập, không ép chọn trong danh sách; 4 vai không bao giờ nói với người học (Sơn phong trưởng lão, Nghiệm Công Sứ, Phúc Khảo Sứ, Chú Giải Sứ) không đặt tên vì không hiện ra với người học (đặc tả §3, bảng "Nói với người học") *(nguồn: schema tên/tước hiệu persona của BMAD `agents.*` (name/title/icon) dùng làm mẫu; đặt trong hội thoại `nhap-mon` chứ không phải `userConfig`, vì `userConfig` không có kiểu chọn-từ-danh-sách)*.
- **FR36** — Sau khi khai vai/mạch ở bái sư, Trưởng môn phải **chỉ điểm** — gọi tên sách cụ thể để người học tự đi tìm, không phải chọn mạch hộ; đây là mắt xích duy nhất giúp hệ khởi động được khi tàng kinh các còn rỗng. Mỗi chỉ điểm phải nêu đủ 5 trường (tên, tác giả, năm/ấn bản, công pháp hay tâm pháp, vì sao) — không đưa một cái tên trần dễ bịa; không chắc thì nói không chắc. Số chỉ điểm co giãn: 3 công pháp + 2 tâm pháp nếu người học đã biết muốn luyện gì, 1+1 kèm "thỉnh được rồi quay lại, ta chỉ tiếp" nếu chưa biết (nhánh chưa biết hỏi VAI trước, không hỏi mạch — suy mạch từ vai, kèm cờ nguồn gợi ý). Sách công pháp luôn kèm gợi ý tâm pháp đỡ trần; mức chắc chắn của gợi ý (kèm số liệu thật / kèm nguồn khai báo / chỉ là suy đoán) phải nói **trước khi** đưa danh sách, không phải sau. Chỉ điểm mới thay hẳn chỉ điểm cũ (không cộng dồn) nhưng vẫn tra lại được nếu người học hỏi lại tên cũ. **Nhánh đáng chú ý riêng** (đặc tả gọi đích danh, §10.2): "kiếm thấy sách nhưng bản này không rút được chữ" (`ban_hong`) khác hẳn "kiếm không ra sách" (`khong_thay`) ở chỗ quyết định — `ban_hong` là **sách đúng, bản in sai**, phải GIỮ NGUYÊN quyển trong chỉ điểm và khuyên tìm bản khác; `khong_thay` mới ghi vào `chi-diem-hong.jsonl` và chỉ quyển khác. Gộp hai nhánh làm một là mất một quyển hay vì một lỗi phân loại *(F0/F-1 tương đương — §10 đặc tả "Bái sư và chỉ điểm", phát hiện muộn khi rà story Epic 1, đặt cuối §4.6 không renumber toàn bộ, cùng cách FR1a/FR34/FR35. Luật epistemic-honesty của chỉ điểm — nói rõ mức chắc chắn trước khi đưa danh sách — là áp dụng cụ thể của FR14/FR15 (Định hướng) cho khoảnh khắc cold-start, trước khi CAP-5/CAP-12 (Vòng 3) có đủ kho mà gợi ý)*.

### 4.7 Nguyên tắc xuyên suốt (cross-cutting)

- **FR32** — Khi người học hỏi một ý định mà cơ chế đứng sau chưa được dựng ở bản đang chạy (ví dụ hỏi cảnh giới trước khi Sơn phong trưởng lão tồn tại — Vòng 4), hệ phải trả lời rõ **"chưa hỗ trợ ở bản này"** — không im lặng bỏ qua, không đoán liều thay. Áp dụng cho mọi ý định của `/vd:chi-duong`, không riêng cảnh giới; phải có ngay từ MVP vì bản đầu chưa dựng hết Vòng 3-4. *(Khớp nguyên tắc đã có ở FR14 — nói rõ khi thiếu dữ liệu; ở đây là thiếu cả cơ chế, không chỉ thiếu dữ liệu.)*
- **FR33** — Hệ không được khen ngợi mang tính xã giao/nịnh bợ (ví dụ "ngươi giỏi lắm") — mọi cảm giác tiến bộ phải đến từ nghi thức gắn với việc thật và kết quả thật, không từ lời khen. Áp dụng cho mọi phản hồi của hệ (Dạy, Soát, Nền), không riêng lúc gắn nghi thức *(nguồn: §1.4, §7 đặc tả — "vui đến từ nghi thức và tiến bộ có thật, không từ lời khen"; kiểm bằng behavioral eval — §3 — với ca thử: đưa câu trả lời tầm thường, xác nhận hệ không khen sáo rỗng)*.

## 5. Non-Goals

1. **Không cấp chứng chỉ/bằng cấp chính thức.** "Đột phá" là phản chiếu nội bộ cho người học, không phải văn bằng có giá trị dùng bên ngoài.
2. **Không đo tiến độ bằng số chương đã đọc.** Đối lập trực tiếp với JTBD ở §2 — đọc xong không đồng nghĩa hiểu; đếm chương là chỉ số dễ đo nhưng sai mục tiêu.
3. **Không thu telemetry từ người dùng mở nguồn khác.** Sách và câu trả lời ở lại máy người dùng; không có server riêng của Vấn Đạo thu dữ liệu học tập.
4. **Không phải chatbot hỏi-đáp tự do, không cấu trúc.** Luôn đi qua lộ đồ/giáo án; không trả lời "dạy tôi chương X" bằng một bài giảng bột phát không qua nghiệm công.
5. **Không phải chế độ lớp học / nhiều người cùng học một bí kíp.** Theo dõi tiến độ theo cá nhân, không theo nhóm.
6. **Chỉ chạy trên Claude Code, không cam kết mở rộng.** Không phải bản chạy trên Claude.ai chat hay nền tảng khác — cần subagent tươi, hook, tầng lưu trữ cục bộ, đều là điều kiện chỉ Claude Code CLI có. Đây là *chưa quyết mở rộng*, không phải *loại trừ vĩnh viễn* — giữ đúng mức PRFAQ đã nói ("đang cân nhắc"), không nói dứt khoát hơn bằng chứng cho phép.

## 6. MVP Scope

**Milestone MVP: "đột phá quyển đầu tiên"** (`docs/VAN-DAO-dac-ta-v1.0.md` §16 bước 13, cuối Vòng 2) — không dừng ở bước 8 (tự bế quan). Lý do: dừng ở bước 8 mới có Dạy chạy được, chưa có Soát — mà Soát độc lập chính là khác biệt cốt lõi đã nêu ở §1 Vision. MVP phải khép được vòng đó, không chỉ dạy được.

**Hai điều cần đọc trước bảng:**
- **"Vòng" (§16 — chuỗi phụ thuộc kỹ thuật) khác "Bậc" (§13.1 — độ hoàn thiện tính năng).** Một thành phần "Bậc 1" vẫn có thể nằm ở "Vòng 2" nếu nó phụ thuộc kỹ thuật vào bước dựng sau — ví dụ phần chẩn đoán/giảng lại của FR4/FR5 (F3-F5′) là Bậc 1 nhưng đúng bước 11, Vòng 2. Bảng dưới xếp theo Vòng, vì đây là trục đúng cho câu hỏi "dựng được lúc nào" — nhãn Bậc từng lệch với Vòng một lần (trường hợp `phuc-khao`), nên không dùng Bậc để cắt MVP.
- **Vòng là chuỗi phụ thuộc, không phải mốc thời gian** (§16 tự nói rõ điều này) — MVP = Vòng 1+2 không phải cam kết "xong trong X tuần".

**Có trong MVP (Vòng 1-2, bước 1-13):**

| FR | Bước §16 | Ghi chú |
|---|---|---|
| FR1, FR37, FR38, FR39 (Thu sách — giải nghĩa, người sửa-duyệt pha 2, dừng khi không rút được chữ, hai mức hợp lệ) | 3 | FR37-39 phát hiện muộn qua Input Reconciliation lần 2 — cùng bước 3 với FR1, cùng luồng thu bí kíp |
| FR6, FR7, FR1a, FR2, FR2a, FR3, FR3a (Dạy — lộ đồ trình duyệt, giáo án ra file, tóm lược trước khi hỏi ngược, hỏi ngược, không đáp câu trùng nghiệm công treo, đối chất quan niệm cũ, thừa nhận≠gỡ) | 5 (F-1→F2) | FR1a là bước mở đầu F0/F1, tiêu thụ trực tiếp đầu ra FR1. FR2a/FR3a phát hiện muộn qua Input Reconciliation lần 2 |
| FR4, FR5 (Dạy — giàn giáo co giãn, mastery gate) | 5 + 11 (F3-F5′) | Phần chẩn đoán/giảng lại khi vấp thuộc bước 11 (Vòng 2) — FR4/FR5 chỉ trọn vẹn từ cuối Vòng 2, không phải ngay từ đầu Vòng 1 |
| FR8, FR10 (Soát — tách vai, bằng chứng trước khẳng định) | 6 | |
| FR9, FR11a-c, FR12a-b (Soát — Giám khảo tách khỏi chấm, trực giao, cờ bất đồng) | 10, 12, 13 | FR12b: chỉ có kênh đạo tâm; chưa có màn "tiến độ" |
| FR22 (Nền — đạo tâm tự ghi) | 7 | |
| FR23 (Nền — nghi thức) | 3-4, 7 | Chỉ bái sư + thu bí kíp; đột phá cảnh giới chưa dùng được ở MVP |
| FR34, FR35 (Nền — chọn ngôn ngữ, đặt tên 4 vai) | 1 (mới, trước cả bái sư) | Chạy trước bái sư — FR34 qua `userConfig` lúc bật plugin (chưa verify chạy thật), FR35 trong hội thoại `nhap-mon`; phát hiện muộn khi rà epic list, không có bước §16 gốc |
| FR36 (Nền — chỉ điểm) | tương đương F-1, ngay sau bái sư | Trưởng môn chỉ sách trước khi đệ tử đi thỉnh — mắt xích bắt buộc để hệ khởi động từ kho rỗng; phát hiện muộn khi rà story Epic 1, không có bước §16 gốc |
| FR32 (cross-cutting — trả lời rõ khi thiếu cơ chế) | — | Không chặn bởi bước nào cụ thể; cần ngay từ MVP để `/vd:chi-duong` không im lặng/đoán liều với ý định thuộc Vòng 3-4 |

**Để Vòng 3 (nhiều quyển, nhiều mạch — bước 14-19):**

| FR | Bước §16 | Vì sao chưa vào MVP |
|---|---|---|
| FR13-FR15 (Định hướng) | 14 | Gợi ý "học gì tiếp" vô nghĩa khi kho chỉ có một quyển |
| FR24 (hạ sơn/phục mệnh) | 16 | Cơ chế cho nhiều mạch, chưa cần khi mới có một quyển |
| FR25, FR26 (Nền — nhắc lại, hệ thống hoá cuối quyển) | 18 | F6/F7 trong thu-linh, chặn bởi bước 8 |
| FR27, FR28 (Nền — nối lại mạch cũ, xuất quan) | 18 | F8/F9 — quay lại phiên mới chỉ mượt từ Vòng 3; ở MVP trạng thái vẫn còn trong file nhưng chưa có luồng nối lại thiết kế riêng |
| FR30 (quét kho gợi sách) | 15 | Vô nghĩa khi kho chỉ có một quyển, cùng lý do với Định hướng |
| FR31 (bản đồ trực quan) | 17 | Ở MVP chỉ có đạo tâm dạng text (FR22), chưa có bản đồ |

**Để Vòng 4 (đo và tự sửa — bước 20-25):**

| FR | Bước §16 | Vì sao chưa vào MVP |
|---|---|---|
| FR16-FR21 (Đo cảnh giới + hiệu chuẩn) | 20-21, 25 | Cần ≥2 nguồn theo R10 — không dựng có nghĩa với một quyển; hiệu chuẩn cần đủ mẫu phủ nhiều mạch |
| FR29 (Chú Giải Sứ — bồi sai lầm phổ biến) | 23 | Chặn bởi bước 18 (FR25-FR28) — xa MVP hơn cả Định hướng/Đo |

## 7. Success Metrics

**Đo bằng gì:** Không có telemetry (§5 Non-Goals #3) — mọi số liệu ở đây tác giả tự quan sát từ đạo tâm và trải nghiệm của chính mình, không phải dashboard tập trung. Mỗi metric ghép với một counter-metric theo kỹ thuật **paired metrics** (Andy Grove, *High Output Management*, 1983) — chống lại Goodhart's Law: một phép đo đứng một mình sẽ bị tối ưu hoá ngược, chệch khỏi mục tiêu thật.

| Metric | Counter-metric |
|---|---|
| **Hoàn thành đột phá quyển thật** — tự thu một quyển PDF/EPUB thật đang cần học và đi hết tới đột phá quyển (§16 bước 13) | Không tính "hoàn thành" nếu tỷ lệ chương bỏ qua nghiệm công quá cao — hoàn thành mà né chấm không phải bằng chứng thật |
| **Đạo tâm có bằng chứng vận dụng cụ thể** — dòng ghi kèm dẫn chứng từ nghiệm công/khảo thí, không chỉ log sự kiện nghi thức | Không tính là "dùng được" nếu đạo tâm chỉ toàn nghi thức (bái sư, thu sách) mà không có sự kiện gắn với vấp/sửa thật |
| **Quay lại học quyển thứ hai sau khi xong quyển đầu** — không bỏ cuộc vì ma sát UX | Phân biệt "xuất quan" hợp lệ (tạm dừng, §1.4) khỏi bỏ hẳn không quay lại; đo ở mốc xa (vài tuần sau), không chỉ ngay sau lần đầu — nghiên cứu gamification cảnh báo hiệu ứng nghi thức/thành tựu có thể chỉ là hiệu ứng mới lạ (novelty) phai theo thời gian, nên không lấy hài lòng tuần đầu làm bằng chứng duy trì thật |

**Sau Vòng 4 (không phải MVP):** κ hiệu chuẩn đạt ngưỡng ≥0,6 khi đủ 20 mẫu — điều kiện để bắt đầu công bố cảnh giới, không phải chỉ tiêu tăng trưởng.

## 8. Open Questions

1. **Chạy trên Claude Code hay mở rộng nền tảng khác?** PRFAQ nói "đang cân nhắc", Non-Goals §5 mục 6 giữ ở mức "chưa quyết" — nhưng kiến trúc hiện tại (subagent tươi, hook, nhiều vai AI tách biệt bên trong Claude Code) gắn khá sâu vào cách nền tảng này tổ chức, nên chuyển sang nơi khác gần như phải dựng lại phần điều phối. Chưa có quyết định thật, chỉ có hai câu trả lời khác nhau về mức độ cam kết, đang tồn tại song song ở hai tài liệu. **Owner:** tác giả. **Điều kiện xem lại:** khi có nhu cầu thật từ người dùng thứ hai, hoặc khi kiến trúc đủ ổn định để ước tính chi phí chuyển nền tảng.

2. **Việc chấm ở MVP (Vòng 1-2) chưa có hiệu chuẩn nào xác nhận đáng tin.** FR8, FR10-FR12 (Nghiệm Công Sứ, Phúc Khảo Sứ) chạy từ Vòng 1-2, nhưng hiệu chuẩn κ (FR20) chỉ chạy ở Vòng 4 — vì cần đủ mẫu và nhiều mạch. Suốt Vòng 1-3, không có cơ chế nào xác nhận model chấm đúng theo rubric — đúng giả định nền §17 đặc tả đã tự nêu ("Model chấm được bài vận dụng theo rubric có tiêu chí cụ thể — sai thì §11 phát hiện", nhưng §11 lại là Vòng 4). Tác giả phải tự đánh giá bằng cảm quan trong giai đoạn này, không có gì đỡ. **Owner:** tác giả. **Điều kiện xem lại:** khi tới Vòng 4 chạy được hiệu chuẩn thật; nếu phát hiện chấm sai có hệ thống ngay ở MVP thì cần cân nhắc đẩy một phần §11 lên sớm hơn Vòng 4.

3. **Chưa có ai ngoài tác giả đọc và phản hồi thật về ý tưởng này.** PRFAQ tự nhận đây là "crack in the foundation" hàng đầu — rủi ro "giải pháp đi tìm vấn đề" — và khuyến nghị nên có phản hồi từ người ngoài trước khi đầu tư tiếp. §2 chỉ có một câu vọng nhẹ ("chưa có xác nhận từ người dùng thứ hai") coi như đặc điểm persona, chưa phải rủi ro được theo dõi chủ động. **Owner:** tác giả. **Điều kiện xem lại:** trước khi đầu tư thêm công sức đáng kể vượt quá MVP, hoặc trước khi mời bất kỳ ai khác cài thử.

4. **Chưa có kế hoạch bảo trì/hỗ trợ nếu người khác thật sự cài dùng.** Mã nguồn mở (§1, §2) nhưng PRFAQ Internal FAQ tự nhận "chưa nghĩ tới" SLA hay kế hoạch phân phối. **Owner:** tác giả. **Điều kiện xem lại:** cùng mốc với mục 3 — khi có người dùng thứ hai thật sự.

5. **Phụ thuộc bên ngoài `book-to-skill` (virgiliojr94) chưa có phương án dự phòng.** FR1 — nền của toàn bộ Dạy/Soát phía sau — cần package này hoạt động đúng và tiếp tục được duy trì; đã verify chạy thật (không chỉ đọc tài liệu) nhưng chưa có kế hoạch nếu package đổi API hay ngừng bảo trì — rủi ro nền tảng này trước đó chỉ nằm trong Assumptions Index, nay nâng lên đây cho đúng mức theo dõi. **Owner:** tác giả. **Điều kiện xem lại:** nếu package ngừng bảo trì hoặc đổi API phá vỡ tương thích; trước khi phụ thuộc vào nó vượt quá MVP.

6. **FR10 ("trích câu cụ thể trước khi khẳng định") chưa đứng trên khung học thuật ngoài — đã có tên ở đặc tả §2 ("Rubric neo + bằng chứng trước khẳng định") nhưng đó là nguyên tắc tự đặt tên của dự án, không phải trích dẫn học thuật.** Rà soát grounding toàn bộ FR1-FR33 (Source Triangulation, 2026-08-26) phát hiện FR10 là claim hành vi chấm điểm duy nhất trong cụm Soát không tìm được nguồn học thuật ngoài sau 3 vòng tìm kiếm thật — khác FR9 (nay có NCME Test Security cạnh "Tách ra đề khỏi chấm" của §2) và FR11a-c (nay có Ofqual 2014 + Cannings et al. 2005). Có thể liên quan "evidence-centered design" (Mislevy et al.) nhưng chưa verify được liên hệ trực tiếp. **Owner:** tác giả. **Điều kiện xem lại:** trước khi viết story cho FR10 (Epic 4) ở step-03, nếu muốn nguyên tắc này có căn cứ học thuật ngoài thay vì chỉ là lựa chọn thiết kế tự đặt tên; hoặc chấp nhận đây là quyết định nội bộ hợp lý không cần khung ngoài (không phải mọi quyết định đều là claim hành vi cần khung).

## 9. Assumptions Index

**Giả định nền tảng đã có sẵn:** `docs/VAN-DAO-dac-ta-v1.0.md` §17 liệt kê đủ 7 giả định nền kèm "sai thì sao" — không chép lại ở đây. Mục 2 của bảng đó (model chấm theo rubric) đã lên Open Questions §8 mục 2. Mục 3 (model đọc cảnh giới) **chưa** có Open Question riêng — chỉ giảm nhẹ gián tiếp qua việc FR16-FR21 hoãn tới Vòng 4 và FR17/FR19 (không công bố khi chưa đủ căn cứ, khung là giả thuyết); bản thân giả định đúng hay không vẫn chưa kiểm được tới khi có dữ liệu thật.

**Giả định phát sinh riêng trong PRD này:**

| Giả định | Nếu sai thì sao |
|---|---|
| Model giải nghĩa đúng ý từ PDF/EPUB đa dạng định dạng (FR1) — chưa kiểm với sách có bảng/hình/công thức/code | Dạy/Soát sau đó build trên nguồn hiểu sai từ gốc; cơ chế hiện tại không kiểm nguồn có đúng với sách gốc, chỉ kiểm người học có làm đúng theo nguồn — lỗi gốc không bị bắt |
| Kỹ thuật sư phạm được kiểm chứng cho người dạy là con người (FR2-FR5) sẽ chuyển tốt sang AI dạy qua văn bản | Đúng quy trình lý thuyết nhưng hiệu quả học thực tế thấp hơn kỳ vọng — chưa có cách đo riêng cho hình thức AI-dạy này (PRFAQ Customer FAQ đã tự nhận câu hỏi học thuật này chưa ngã ngũ) |
Pha "giải thích trước khi hỏi ngược" nay đã có FR riêng với căn cứ (FR1a — 4C/ID Supportive Information, van Merriënboer & Kirschner 2018), nhưng **liều lượng cụ thể** (dài bao nhiêu, dạng văn bản/sơ đồ, có co giãn theo độ dày chương không) chưa được thiết kế chi tiết — khung lý thuyết chỉ nói TRÌNH BÀY TRƯỚC là đúng hướng, không nói trình bày dài/ngắn thế nào | FR1a có thể cần điều chỉnh đáng kể về hình thức khi thiết kế chi tiết xong (viết story) — căn cứ lý thuyết đã có, nhưng tham số cụ thể chưa chốt |
| Trực giao Nghiệm Công Sứ/Phúc Khảo Sứ (đọc tiêu chí khác đọc mục tiêu, FR11a-c) tạo phân kỳ thật, không chỉ khác biệt hình thức | Cờ bất đồng hiếm không phải vì chấm tốt mà vì cả hai cùng mù một điểm; chỉ ca đối chứng (Vòng 4) mới phát hiện — liên quan Open Questions mục 2 nhưng là câu hỏi khác (độc lập thật hay chỉ có vẻ độc lập) |
| Mastery learning (FR5) áp dụng tốt như nhau cho cả công pháp và tâm pháp | Tâm pháp khó đo "vận dụng đúng" hơn, dễ rơi vào tiêu chí không phân biệt nếu không tách riêng |
| Độ tản mát giữa nhiều lần chạy (FR18) là thước đo độ tin hợp lệ cho phán đoán chủ quan | Nếu không tương quan thật với độ chính xác, κ hiệu chuẩn (Vòng 4) là phép kiểm duy nhất — không có gì đỡ trước đó |
| n=1 là ràng buộc thật, không phải khiêm tốn (§2) | Người dùng thứ hai với nhu cầu khác có thể đòi điều chỉnh giả định "đủ dữ liệu" ở Định hướng/Đo |

*Phụ thuộc `book-to-skill` (virgiliojr94, chặn FR1) đã nâng thành Open Questions §8 mục 5 — có Owner + điều kiện xem lại, không để ở đây nữa.*
