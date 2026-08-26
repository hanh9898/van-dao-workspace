# Đối chiếu đặc tả (`docs/VAN-DAO-dac-ta-v1.0.md`, 2139 dòng) với PRD hiện tại (`prd.md`)

Đã đọc trọn cả hai file. Lượt này đặc biệt lần theo tường minh cả 13 sơ đồ mermaid trong đặc tả (không đọc lướt như văn xuôi), cộng với soát chéo phần văn xuôi/bảng còn lại (R1-R33, tám vai, hai nguyên tắc nền, §6, §10, §11...).

---

## Phần 1 — Sơ đồ đã lần theo (13/13)

| # | Dòng | Loại | Biểu diễn gì (đã lần từng node/cạnh) | Map FR nào trong PRD | Gap? |
|---|---|---|---|---|---|
| 1 | 131-158 | flowchart TD | §1.3 "Đạt khi" — vòng lặp học ý → nghiệm công chương → đột phá chương → hết chương trong lộ đồ → khảo thí quyển → Trưởng môn xử → **đột phá quyển** (tô vàng = tiêu chí đạt hệ) → có ≥2 nguồn mạch chưa? → bỏ qua định vị (chưa đủ) hoặc trưởng lão ×3 định vị → cao hơn lần trước? → giữ bậc hoặc **đột phá cảnh giới** (tô xanh) | FR5 (mastery gate chương), FR16/FR18 (≥2 nguồn + đa mẫu), FR23 (đột phá cảnh giới là nghi thức có việc thật), mốc MVP "đột phá quyển" ở §6 | Không phải gap chính — nhưng cơ chế "định vị chạy **tự động** sau mỗi đột phá quyển, có 2 chốt chặn chi phí (bỏ qua nếu <2 nguồn / đọc cache không gọi lại)" không có FR nào phản ánh. Vòng 4, ưu tiên thấp — xem Gap phụ #6 |
| 2 | 250-269 | flowchart LR | §3 Vòng đời học tập — 10 chặng: Bái sư→Chỉ điểm→**Thỉnh sách (NGOÀI HỆ, tô xám)**→Thu bí kíp→Lộ đồ→Bế quan→Nghiệm công (lặp về Bế quan)→**Khảo thí quyển (tô vàng)**→Định vị→Ghi đạo tâm (chấm dứt về Chỉ điểm cho mạch tiếp)→nhánh tuỳ chọn **Hạ sơn lịch luyện (NGOÀI HỆ, tô xám)** | Trải đều FR36, FR1, FR6/FR7, FR2-FR5, FR8-FR12, FR16-21, FR22, FR24, và §2 "Vấn Đạo không tìm hay cấp sách" cho chặng ngoài-hệ | Không gap — mọi chặng đều có FR neo, đúng cấu trúc MVP/Vòng3/Vòng4 |
| 3 | 285-337 | flowchart TD | §4.1 Tám vai và đường truyền tin — toàn bộ cạnh dữ liệu giữa NH/8 vai/TKC, đặc biệt 3 cạnh "mang tải nặng nhất" (TL→NC không mang giáo án, TL→PK không mang tiêu chí, TM→TLAO phạm vi hẹp) và luật "không cạnh nào từ subagent về thẳng người học" | FR8-FR12 (tách vai, không đọc chéo), FR30 (`tra-tang-kinh-cac` ≤3 bí kíp), FR4 (F5′ báo trưởng môn qua cạnh TL→TM) | Không gap ở tầng FR — đây là sơ đồ kiến trúc luồng dữ liệu, PRD đúng mức chỉ neo hành vi observable (không đọc X, không mang Y), không cần chép lại từng mũi tên |
| 4 | 384-428 | flowchart LR | §4.3 Luồng dữ liệu và quyền ghi — mỗi vùng riêng đúng một vai ghi, `ban-giao/` chỉ ghi thêm, không file token cầm lượt | — (kiến trúc/lưu trữ thuần) | Không gap — PRD §3 tự nói rõ "phần thuần cơ chế xây dựng (harness...) đã là nguồn sự thật đầy đủ ở đặc tả §0.2, không chép lại" — đây đúng loại đó |
| 5 | 449-497 | erDiagram | §5.0 Mô hình khái niệm — toàn bộ quan hệ thực thể (NGUOI_HOC, HO_SO, BI_KIP, CHUONG, TIEU_CHI, KHUON_CAU_HOI, BAI_NOP, DINH_VI, TAM_MA, DAO_TAM, CHI_DIEM, CHU_GIAI...) | — (data model) | Không gap — mô hình dữ liệu thuộc tầng kiến trúc/schema, không phải FR-level |
| 6 | 817-832 | flowchart TD | §5.11 Ghi neo mỗi ý → XẢ (loại 1 ra file) → hết chương? → CHƯNG (loại 2, trần ~600 ký tự) → Reset → TÁI DỰNG chương sau; nhánh auto-compact nền tảng → điểm neo phục hồi được | — (compaction/context-rot, thuần kỹ thuật) | Không gap — đúng loại "harness/compaction" mà PRD §3 tuyên bố không chép lại |
| 7 | 866-879 | stateDiagram-v2 | §5.12 Tâm ma — 4 trạng thái: `chua_go` →(người học thừa nhận)→ `dang_go` →(**bằng chứng** ở nghiệm công/khảo thí, LÀM khác đi)→ `da_go` →(dấu hiệu cũ lại)→ `tai_phat` →(thừa nhận lần nữa)→ `dang_go` hoặc (bằng chứng mới)→ `da_go`; nhánh thoát `chua_go`→[*] khi người học bảo cách cũ vẫn đúng; note "Thư linh KHÔNG tự tuyên bố (R18)" | FR3 (chỉ phủ bước đầu: nêu xung đột thành lời) | **GAP THẬT** — xem Phần 2, gap #2 |
| 8 | 948-968 | flowchart TD | §6.2 Ba pha thu bí kíp — GIÁM ĐỊNH (rút chữ? Không→dừng, không OCR) → ước lượng → **người duyệt?** → PHA 1 TRÍCH XUẤT → PHA 2 THIẾT KẾ SƯ PHẠM (**NGƯỜI SỬA VÀ DUYỆT**, tô vàng — nút bắt buộc) → PHA 3 SINH CẤP CHƯƠNG → `kiem-bi-kip.py` hợp lệ? → Thu vào kho | FR1 (giải nghĩa + đánh dấu độ tin cậy thấp) | **GAP THẬT** — xem Phần 2, gap #1 |
| 9 | 1061-1099 | stateDiagram-v2 | §6.6 Vòng đời một bí kíp — NgoaiHe→GiamDinh→TuChoi/ChoDuyetChiPhi→Pha1→Pha2 (có nhánh lưu nháp `NhapDangDo` để tiếp phiên sau)→Pha3→**DuDung**→TrongKho↔**DuChuan** (bồi dần)→DangBeQuan↔TamDung(F9)→HocXongChuong→DangKhaoThi→**DaDotPha** (giữ cả hai lần thi khi thi lại)→GayConTro (file dời chỗ, từ bất kỳ trạng thái nào sau khi thu)→`/vd:noi-lai`→TrongKho | FR1 (một phần: DuDung/DuChuan tương ứng "đánh dấu độ tin cậy thấp") | **GAP THẬT** (một phần) — cùng nhóm gap #1: hai mức hợp lệ (đủ dùng/đủ chuẩn), nháp pha 2 lưu được, và `/vd:noi-lai` (gãy con trỏ) hoàn toàn không có FR — xem Phần 2, gap #1 và gap phụ #7 |
| 10 | 1168-1202 | flowchart TD | §7.0 Bế quan một chương — Nhận bí kíp→F-1 lộ đồ (TRÌNH DUYỆT)→chương đầu?→F0′ dò tâm ma→F0 giáo án→F1 dạy 1 ý→câu hỏi→phản ứng: **Hỏi lại** (trùng câu nghiệm công treo?→F3 KHÔNG đáp, hỏi ngược / không trùng→F3 trả lời) / **Trả lời sai** (F4 chẩn đoán→sai lần mấy: 1→lặp lại, 2→F5 đổi biểu diễn, 3→F5′ báo trưởng môn) / **Thông** (còn ý?→lặp / hết→nộp nghiệm công? Không→`chua_nghiem_cong` đi tiếp KHÔNG chặn / Có→F2 chấm) | FR6/FR7 (F-1/F0), FR3 (F0′), FR1a/FR2 (F1), FR4 (F4/F5/F5′ giàn giáo tăng khi vấp) | **GAP THẬT (nhỏ)** — nhánh "Hỏi lại → trùng câu nghiệm công đang treo → F3 KHÔNG đáp, hỏi ngược lại" (R5) không có FR nào phủ. Xem Phần 2, gap #3 |
| 11 | 1322-1345 | sequenceDiagram | §9.3 Luồng khảo thí quyển — NH→KT `/vd:khao-thi`→KT sinh biến thể đề (khuôn+tham số, kèm dữ kiện thừa)→NH bài làm→KT→NC (bài+tiêu_chí_đạt)→KT→PK (bài+mục_tiêu, KHÔNG tiêu chí)→NC/PK-->>TM→TM xử (không dạy không chấm)→alt khớp: trả kết quả / else bất đồng: ghi `bat-dong.jsonl`, trả kết quả LUÔN có lợi cho người học | FR9 (giám khảo không chấm), FR8/FR10, FR11a-c (trực giao), FR12a/b (cờ bất đồng, có lợi cho người học) | Không gap ở mức FR-hành vi — cơ chế `bo_tham_so`/`du_thua` (sinh đề từ bộ tham số đã khớp sẵn, tránh tổ hợp vô nghĩa) không có FR riêng, nhưng đây là chi tiết thiết kế đề thi (mức story/architecture), không phải capability thiếu — ghi nhận như quan sát phụ, không tính là gap chính |
| 12 | 1408-1434 | flowchart TD | §10.0 Bái sư và chỉ điểm — `/vd:nhap-mon`→Bái sư (đặt tên môn phái, ghi nhập môn ký)→đã biết muốn luyện?→(Biết: khai vai+mạch / Chưa biết: hỏi VAI trước→gợi ý mạch kèm cờ nguồn→người học chọn)→CHỈ ĐIỂM (biết:3+2, chưa biết:1+1)→mỗi chỉ điểm 5 trường→ghi `chi-diem.jsonl` (`dang_treo`)→người học đi kiếm→4 nhánh kết quả: **kiếm được**→thu-bi-kip; **không thấy SÁCH**→`chi-diem-hong.jsonl`+chỉ điểm khác; **thấy sách, bản hỏng**→`ban_hong` GIỮ quyển, khuyên tìm bản khác; **chưa đụng tới**→phiên sau nhắc 1 câu, lô cũ hết hiệu lực | **FR36** (đã vá ở lượt trước — bao phủ: 5 trường, 3+2 vs 1+1, hỏi vai trước, cờ nguồn, tâm pháp kèm, không cộng dồn nhưng tra lại được) | **GAP THẬT (nhỏ)** — FR36 không phủ 2 nhánh outcome mà chính đặc tả gọi là "nhánh đáng chú ý": phân biệt `ban_hong` (sách đúng, bản lỗi → GIỮ quyển) khác `khong_thay` (đổi sang quyển khác) — hai remedy khác nhau cho hai lỗi khác nhau. Xem Phần 2, gap #4 |
| 13 | 1687-1725 | flowchart TD | §13.0 Phân rã theo năng lực — 28 thành phần nhóm theo 6 năng lực (THU SÁCH/DẠY/SOÁT/ĐỊNH HƯỚNG/ĐO/NỀN), tô xanh Soát+Đo, tô xám Nền | — (kiến trúc, phân rã thành phần) | Không gap — PRD §4 dùng đúng 6 nhóm này làm cấu trúc mục (4.1 Thu sách...4.6 Nền), khớp hoàn toàn |

**Xác nhận: đã lần theo đủ 13/13 sơ đồ**, không thiếu sơ đồ nào.

---

## Phần 2 — Real gaps (xếp theo mức độ quan trọng)

### Gap #1 — QUAN TRỌNG NHẤT: Thu sách chỉ có 1 FR (FR1), thiếu cổng duyệt bắt buộc ở pha 2 và cơ chế "hai mức hợp lệ"

**Căn cứ đặc tả:** §6.2 (sơ đồ #8, dòng 948-968) + §6.5 + §6.6 (sơ đồ #9, dòng 1061-1099). Đặc tả dành nguyên §6 (9 tiểu mục: 6.1-6.9) cho việc thu bí kíp, và nhấn mạnh tường minh: *"Người bắt buộc chen vào pha 2. Xương sống, tiêu chí đạt và điểm hạ sơn chỉ người có nghề quyết được; model đoán ra thứ nghe hợp lý mà sai, và cái sai truyền xuống mọi chương."* (dòng 970). Sơ đồ #8 vẽ nút "NGƯỜI SỬA VÀ DUYỆT" tô vàng — cùng cấp nhấn mạnh với "ĐỘT PHÁ QUYỂN" ở sơ đồ #1. §6.5 định nghĩa "hai mức hợp lệ" (đủ dùng vs đủ chuẩn) cho phép sách vào kho sớm rồi bồi dần sau khi học — một cơ chế bồi thường (compensating control) cho việc pha 2 nặng. §6.1 quy định giám định dừng hẳn nếu không rút được chữ (không OCR).

**PRD đang thiếu gì:** FR1 (§4.1 Thu sách) chỉ có đúng một câu về "giải nghĩa ý + đánh dấu độ tin cậy thấp". Không có FR nào yêu cầu: (a) con người phải sửa-và-duyệt thiết kế sư phạm (tiêu chí đạt, xương sống, worked example) trước khi bí kíp vào kho — đây là gate chất lượng cốt lõi, không phải chi tiết vặt; (b) giám định dừng và báo rõ khi không rút được chữ, không tự ý OCR; (c) hai mức hợp lệ đủ dùng/đủ chuẩn cho phép bắt đầu học sớm rồi bồi trường chi tiết sau (R13, R13b, R15 trong đặc tả). So sánh: Dạy có 7 FR (FR1a, FR2-FR7), Soát có 6 FR (FR8-FR12), nhưng Thu sách — cũng là một trong ba năng lực cốt lõi theo chính cấu trúc §13.0 — chỉ có 1 FR. Sự bất cân xứng này không phải ngẫu nhiên: nó phản ánh việc pha 2 (thiết kế sư phạm có người duyệt) chưa được nhìn ra là một capability riêng cần FR.

**Vì sao quan trọng:** Đây là điểm rủi ro chất lượng lớn nhất của toàn hệ theo chính lời đặc tả — nếu model tự ý thiết kế xương sống/tiêu chí sai mà không ai duyệt, "cái sai truyền xuống mọi chương" và người học học sai từ gốc mà không ai biết. MVP scope hiện tại (§6 PRD) map FR1 vào bước 3 (§16 đặc tả) nhưng bước 3 đặc tả ghi rõ "dừng ở pha 2" — tức PRD đã ngầm chọn đúng phạm vi MVP (dừng ở pha 2, để người dựng tự duyệt bằng tay) nhưng chưa có FR nào ép buộc UI/luồng phải dừng lại chờ duyệt.

**Đề xuất:** Thêm 2-3 FR ở §4.1 Thu sách: (1) một FR bắt buộc dừng ở pha 2 chờ người học sửa-và-duyệt thiết kế sư phạm trước khi sinh chương (tương đương R6.5/§6.2 pha 2), có thể dùng chung logic "trình→xác nhận→ghi→kiểm" đã có ở §12.4; (2) một FR về giám định dừng nếu không rút được chữ, không OCR, báo rõ nguyên nhân; (3) cân nhắc thêm FR cho "hai mức hợp lệ" nếu muốn capability bồi dần nằm trong MVP, hoặc ghi rõ vào §6 MVP Scope là "chỉ mức đủ dùng, hoãn đủ chuẩn/bồi dần sang Vòng sau" nếu cố ý cắt.

---

### Gap #2 — QUAN TRỌNG: Tâm ma — thiếu cơ chế "thừa nhận ≠ gỡ" (R18) và vòng đời 4 trạng thái

**Căn cứ đặc tả:** §5.12 (sơ đồ #7, dòng 866-879) + R17/R18 (§8, dòng 1270-1271). Sơ đồ vẽ tường minh 4 trạng thái `chua_go → dang_go → da_go → tai_phat`, với ghi chú ngay trên sơ đồ: *"Thư linh KHÔNG tự tuyên bố (R18)"*. Văn xuôi ngay sau sơ đồ nhấn mạnh: *"Ranh giới giữa hai loại tín hiệu là chỗ dễ trượt nhất: thừa nhận không phải gỡ. Người học nói 'à đúng, tôi hay làm theo template' là bước một, không phải bước cuối. Trộn hai cái thì mọi tâm ma đều được gỡ ngay trong lượt phát hiện ra nó."* (dòng 889). Chuyển `dang_go → da_go` đòi bằng chứng LÀM khác đi ở nghiệm công/khảo thí, không phải lời nói.

**PRD đang thiếu gì:** FR3 (§4.2) chỉ phủ bước đầu của F0′ — "nêu thành lời và đối chất" — tương ứng chuyển `[*] → chua_go` và nhánh thoát. FR3 KHÔNG nói gì về: việc hệ phải theo dõi tâm ma qua nhiều trạng thái, và đặc biệt là luật chặn "không được tự tuyên bố đã gỡ chỉ vì người học thừa nhận bằng lời — phải có bằng chứng làm khác đi trong bài". Đây là một guardrail chống một chế độ hỏng cụ thể: hệ (hoặc Thư linh) vội kết luận "tâm ma đã gỡ" ngay khi người học nói "à tôi hiểu rồi", trong khi hành vi thật chưa đổi.

**Vì sao quan trọng:** Đây là một trong số ít nơi đặc tả tự đánh số thành yêu cầu riêng (R17 VÀ R18 — hai R khác nhau cho hai nửa của cùng cơ chế), cho thấy tác giả đặc tả coi đây là hai ràng buộc độc lập cần kiểm riêng. Thiếu R18 nghĩa là một điều kiện thất bại thầm lặng: hệ có thể sớm coi tâm ma đã xử lý xong dựa trên lời nói, làm hỏng đúng mục đích ban đầu của toàn cơ chế tâm ma (chống "tẩu hoả nhập ma" — nói trôi chảy, chưa từng làm — theo bảng thuật ngữ §0.1).

**Đề xuất:** Thêm một FR (hoặc mở rộng FR3) nêu rõ: chuyển trạng thái tâm ma sang "đã gỡ" chỉ được phép dựa trên bằng chứng quan sát được trong bài nộp/khảo thí (làm khác đi), không dựa trên lời thừa nhận của người học; và hệ phải phân biệt được tái phát (đã từng gỡ rồi vướng lại) với lần vướng đầu tiên.

---

### Gap #3 — TRUNG BÌNH: Thiếu luật "không đáp câu hỏi trùng câu nghiệm công đang treo" (R5)

**Căn cứ đặc tả:** Sơ đồ #10 (§7.0, dòng 1168-1202), nhánh "Hỏi lại → trùng câu nghiệm công treo? → Có → F3 KHÔNG đáp, hỏi ngược lại" — tô màu đỏ nhạt (`style H2 fill:#f8d7da`) trong sơ đồ, tức được tác giả xếp vào nhóm "ba nhánh dễ làm sai nhất" (dòng 1204). Cũng là R5 trong bảng yêu cầu §8 (dòng 1257) với cách kiểm cụ thể: "Nhật ký F3 ghi các câu đã né". Luật dạy số 4 ở §7.1 (dòng 1211) lặp lại nguyên tắc này.

**PRD đang thiếu gì:** Không có FR nào trong PRD nói tới việc Thư linh phải né/không trả lời trực tiếp khi người học hỏi đúng câu đang là đề nghiệm công treo (để tránh lộ đáp án qua kênh hỏi-đáp F3). FR2 chỉ nói về việc hỏi ngược sau mỗi ý dạy, không phải về việc từ chối trả lời câu hỏi trùng.

**Vì sao quan trọng:** Đây là một cơ chế chống rò rỉ đáp án — nếu thiếu, người học có thể "hỏi thẳng" thư linh chính câu hỏi nghiệm công đang treo và nhận được câu trả lời trực tiếp, làm vô hiệu hoá phép đo "vận dụng được" (FR5) ngay tại chỗ nó cần đo nhất.

**Đề xuất:** Thêm một FR ở §4.2 Dạy: khi người học hỏi trùng nội dung câu hỏi nghiệm công đang treo, hệ không đáp trực tiếp mà hỏi ngược lại (tương tự cách FR2 xử lý một-ý-một-câu-hỏi).

---

### Gap #4 — NHỎ: FR36 (chỉ điểm) chưa phân biệt `ban_hong` khác `khong_thay`

**Căn cứ đặc tả:** Sơ đồ #12 (§10.0, dòng 1408-1434) và bảng §10.2 (dòng 1471-1481, đặc biệt dòng 1481: *"`ban_hong` khác `khong_thay` ở chỗ quyết định. Bản scan không rút được chữ nghĩa là sách đúng, bản in sai — gạch tên quyển đó khỏi chỉ điểm là mất một quyển hay vì một lỗi phân loại."*).

**PRD đang thiếu gì:** FR36 (đã vá đúng gap trước, phủ tốt phần chỉ điểm ban đầu: 5 trường, 3+2/1+1, hỏi vai trước, cờ nguồn, tâm pháp kèm) không nhắc tới hai nhánh outcome khác nhau khi người học đi kiếm sách về: (a) `ban_hong` — kiếm thấy đúng sách nhưng bản không rút được chữ → GIỮ NGUYÊN quyển trong danh sách chỉ điểm, khuyên tìm bản khác; (b) `khong_thay` — không tìm ra sách → ghi vào `chi-diem-hong.jsonl`, chỉ điểm quyển KHÁC thay thế. Đây là hai remedy đối lập cho hai lỗi khác nhau (một là lỗi bản in, một là lỗi lựa chọn sách), và chính đặc tả gọi nhánh này là "đáng chú ý" trong tiêu đề mục ngay sau sơ đồ.

**Vì sao quan trọng (mức thấp):** Nếu không phân biệt, một cách hiện thực hoá cẩu thả có thể gộp hai lỗi làm một, khiến người học mất một quyển sách hợp lệ (chỉ vì bản scan họ tìm được đầu tiên bị lỗi OCR) thay vì được khuyên tìm bản khác của đúng quyển đó.

**Đề xuất:** Bổ sung một câu vào FR36 (hoặc câu riêng): khi người học báo "tìm thấy sách nhưng không đọc được" (giám định thất bại — liên hệ Gap #1), giữ nguyên quyển đó trong chỉ điểm và khuyên tìm bản khác, khác với trường hợp không tìm thấy sách (đổi sang chỉ điểm sách khác).

---

## Gap phụ (quan sát thêm, ưu tiên thấp — không bắt buộc sửa ngay)

5. **R2** (§8, dòng 1254) — "Không có tình huống thật thì vẫn dạy, nói rõ tầng nông hơn" — không có FR riêng, dù có cách kiểm cụ thể trong đặc tả ("chạy thử với người học không nêu tình huống"). Liên quan lỏng tới FR2/Non-Goal #4 nhưng chưa có FR trực tiếp.
6. **Định vị tự động sau đột phá quyển + 2 chốt chặn chi phí** (§1.3, dòng 176-183, một phần sơ đồ #1) — thuộc Vòng 4, đã hoãn hợp lý trong MVP Scope, nhưng khi tới lúc viết FR16-21 chi tiết hơn nên cân nhắc thêm cơ chế trigger này.
7. **`/vd:noi-lai`** (gãy con trỏ khi file dời chỗ, §6.9, một phần sơ đồ #9) — một trong 11 lệnh cấp Bậc 1 của đặc tả nhưng không xuất hiện trong PRD dưới bất kỳ hình thức nào.
8. **Giữ cả hai lần thi khi thi lại, không ghi đè** (§6.6, dòng 1107-1110) — quyết định giữ dữ liệu có lý do rõ (mẫu cho hiệu chuẩn/bat-dong), không có FR nào nhắc.
9. **R33** (tâm pháp chỉ đẩy lên ưu tiên học khi có dấu hiệu vấp lặp/đình trệ, khác với việc luôn gợi ý tâm pháp lúc chỉ điểm) — FR36 phủ đúng phần "luôn kèm gợi ý lúc chỉ điểm" nhưng không phủ phần "không đẩy ưu tiên học mặc định" — có thể là trùng lặp ý hoặc thiếu, cần đọc kỹ lại nếu viết story.

---

*Ghi chú: gap "§10 Bái sư và chỉ điểm bị bỏ sót hoàn toàn" từ lượt trước đã được xác nhận VÁ ĐÚNG bởi FR36 — không báo lại, chỉ báo phần chưa đủ (Gap #4) như trên.*
