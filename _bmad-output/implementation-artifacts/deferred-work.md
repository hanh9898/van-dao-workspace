# Deferred Work

Việc đã có quyết định hoãn, kèm mốc cụ thể để quay lại. Append-only — không sửa mục cũ.
Hoãn mà không ghi mốc thì không phải hoãn, là quên.

- source_spec: `_bmad-output/specs/spec-van-dao-workspace/stories/3-chi-diem-truong-mon-goi-ten-sach.md`
  summary: Dựng hook `SessionStart` (`van-dao/hooks/nap-ho-so.sh`) để hành vi "nhắc một câu ở phiên sau" của trạng thái `dang_treo` chạy thật.
  evidence: >-
    Story 1.3 ghi được `dang_treo` nhưng không dựng được cơ chế nhắc — skill `truong-mon` chỉ chạy
    khi người học tự gõ lệnh nên không có mặt ở đầu phiên. Cơ chế đúng là hook SessionStart
    (thành phần 17, §16 Vòng 3 bước 17), AD-7 cho phép vì SessionStart là ranh giới lifecycle thật.
    `van-dao/hooks/` hiện chỉ có `.gitkeep`. Story 1.3 đã làm phần làm được ngay: nhắc `dang_treo`
    tại chỗ khi người học tự gọi `/van-dao:truong-mon`, làm chốt trước khi lô cũ hết hiệu lực.
  revisit_when: >-
    Ngay sau khi Epic 2 hoàn tất — lộ đồ tồn tại thì hook có 2/3 payload (hồ sơ + lộ đồ; còn thiếu
    bản đồ/`ban-do.py`), đủ lý do dựng thật.

- source_spec: `_bmad-output/specs/spec-van-dao-workspace/stories/3-chi-diem-truong-mon-goi-ten-sach.md`
  summary: Gỡ phạm vi bảng quyết định §10.3 (bảng nói về tâm pháp, câu rào rút ra áp cho cả danh sách) và cho câu rào nhích theo kho.
  evidence: >-
    Hai việc chung một gốc. (1) Tiêu đề bảng §10.3 là "công pháp nào cần tâm pháp gì" nhưng kết luận
    rút ra ("câu rào là bước bắt buộc trong luồng chỉ điểm", câu mẫu "những gì nói sau đây là suy đoán")
    bao cả danh sách công pháp — mức chắc chắn của phần công pháp không nguồn nào định nghĩa.
    (2) Câu rào không nhích theo kho: cần đếm kho và biết quyển nào khai tâm pháp gì, mà đọc kho là
    vùng của Tàng kinh trưởng lão (AD-3). Story 1.3 chỉ làm phần rẻ: nói đúng trạng thái kho rỗng
    ("kho chưa có quyển nào") thay vì công thức chung chung, đặt sẵn khuôn câu rào là thứ đo được.
  revisit_when: >-
    Khi dòng hai của bảng §10.3 sắp bật lần đầu — tức khi kho đã có bí kíp khai tâm pháp. Trước đó
    cả hai đều chưa cắn, và sửa đặc tả lúc chưa ai chạm tới dòng hai là sửa mù.

- source_spec: `_bmad-output/specs/spec-van-dao-workspace/stories/3-chi-diem-truong-mon-goi-ten-sach.md`
  summary: Nhánh B (xin chỉ điểm lại) chỉ có hai lối ra — thay HẾT hoặc giữ hết; không có đường thay một phần danh sách treo.
  evidence: >-
    Chính transcript eval id 4 cho thấy skill tự ứng biến một lựa chọn thứ ba ("con chỉ không hợp gu
    với vài quyển cụ thể") không có trong SKILL.md lẫn đặc tả — tức có nhu cầu thật mà quy trình chưa
    định nghĩa (chọn id nào để thay, thay bao nhiêu, có chạy lại Nhánh C không). Gốc nằm ở thiết kế
    nhị phân của đặc tả ("xin chỉ điểm lần nữa → MỌI mục dang_treo chuyển het_hieu_luc"), không phải
    lỗi triển khai.
  revisit_when: >-
    Khi có người dùng thật (ngoài tác giả) báo bị ép thay cả lô, hoặc khi làm bước 14 §16 Vòng 3
    (truong-mon bản đầy đủ) — lúc đó xếp lớp nhiều mạch làm nhu cầu thay từng phần rõ hơn.

- source_spec: `_bmad-output/specs/spec-van-dao-workspace/stories/3-chi-diem-truong-mon-goi-ten-sach.md`
  summary: Nhóm ca biên đầu vào/hạ tầng chưa có hướng dẫn tường minh trong SKILL.md — gộp làm một mục vì cùng lớp rủi ro và cùng điều kiện quay lại.
  evidence: >-
    Edge Case Hunter + Blind Hunter cùng nêu: (1) so_chi_diem lớp cá nhân đặt 0/âm/quá lớn — không
    validate, tam_phap=0 mâu thuẫn với luật "mỗi công pháp kèm gọi tên một tâm pháp"; (2) ho-so.json
    hoặc chi-diem.jsonl hỏng/không parse được — chưa có xử lý; (3) hai phiên chạy đồng thời cùng ghi
    chi-diem.jsonl — không khoá file; (4) dòng cập nhật trạng thái chép đủ trường hay chỉ id+trạng
    thái — chưa chốt tường minh, "Định dạng file" chỉ có ví dụ cho dòng tạo mới; (5) luật hậu tố -2/-3
    khi id trùng chưa từng chạy thật; (6) Nhánh A khi người học báo nhiều sách cùng lúc, hoặc tên khớp
    nhiều mục treo, hoặc danh sách treo rỗng; (7) toàn bộ eval chỉ chạy communication_language=Vietnamese.
    Rủi ro thấp ở MVP một người dùng (n=1, tác giả tự sửa tay được), cùng lớp với ca biên đã defer ở
    Story 1.2.
  revisit_when: >-
    Khi có người dùng thứ hai, hoặc khi gặp ca thật đầu tiên trong nhóm này — lúc đó xử lý cả cụm một
    lượt thay vì vá lẻ.

- source_spec: `_bmad-output/specs/spec-van-dao-workspace/stories/3-chi-diem-truong-mon-goi-ten-sach.md`
  summary: Evidence trong evals.json cho phần "vì sao chọn quyển này" là diễn giải tóm tắt, không phải trích nguyên văn transcript.
  evidence: >-
    Lens skill-quality (check 6): evidence các eval id 2/4/5/6 tóm tắt danh sách dạng "Tên — Tác giả —
    Năm" do người soạn eval viết lại, không trích nguyên văn câu "vì sao" model thật sự đưa ra. Phần
    cấu trúc (đủ 5 trường) VẪN được chứng minh chắc chắn qua đọc file JSONL thật; chỗ chưa có bằng
    chứng độc lập là chất lượng nội dung trường vi_sao (có đủ cụ thể để người học tự đánh giá không).
  revisit_when: >-
    Khi nâng eval từ mức nhẹ lên mức đầy đủ (20 câu, 60/40) theo AD-10 — mốc đó là trước khi phát hành
    plugin ra ngoài.

- source_spec: `_bmad-output/specs/spec-van-dao-workspace/stories/4-*.md` (Story 1.4, tách phạm vi tại step-01)
  summary: Pha 3 — thiết kế sư phạm kèm cổng người-duyệt bắt buộc (FR37), và sinh cấp chương sau khi duyệt.
  evidence: >-
    Story 1.4 gốc gộp 5 mục tiêu độc lập. Người dùng chọn tách, làm mục tiêu 1 (giám định + trích xuất
    + từ chối sạch) trước. Pha 3 là mối quan tâm riêng có cổng riêng: máy CHỈ đề xuất xương sống/tiêu
    chí đạt/điểm hạ sơn kèm lý do, bắt buộc dừng chờ người dùng sửa-và-duyệt trước khi sinh chương.
    Đã verify chạy thật: engine book-to-skill KHÔNG làm phần này — nó chỉ trả full_text.txt +
    metadata.json, không cắt chương, không sinh cấu trúc sư phạm. Toàn bộ pha 3 là việc của van-dao.
  revisit_when: >-
    Ngay sau khi mục tiêu 1 (story này) đóng — đây là mắt xích còn thiếu để một bí kíp thật sự VÀO KHO,
    tức để Epic 1 đóng được và Epic 2 (lộ đồ) bắt đầu được.

- source_spec: `_bmad-output/specs/spec-van-dao-workspace/stories/4-*.md` (Story 1.4, tách phạm vi tại step-01)
  summary: Hai mức hợp lệ (đủ dùng / đủ chuẩn) và cơ chế bồi dần sau khi học.
  evidence: >-
    FR39, đặc tả §6.5-6.7. Mức "đủ chuẩn" bồi thêm tiêu chí chi tiết/sai lầm phổ biến/worked example
    SAU KHI người học học xong chương đó — tức cần Epic 3 (dạy) tồn tại mới có thời điểm kích hoạt.
    Làm bây giờ là dựng nhánh chết, đúng lớp lỗi đã cấm ở Story 1.3 (logic đẩy tâm pháp, cơ chế nhắc
    đầu phiên).
  revisit_when: >-
    Khi Epic 3 (dạy) có bước hoàn thành một chương — lúc đó mới có sự kiện để bồi.

- source_spec: `_bmad-output/specs/spec-van-dao-workspace/stories/4-*.md` (Story 1.4, tách phạm vi tại step-01)
  summary: Nghi thức thu bí kíp (skill riêng, disable-model-invocation) kích hoạt khi bí kíp vào kho.
  evidence: >-
    Cùng khuôn cơ chế với nhập môn ký (Story 1.2), khác thời điểm kích hoạt. Chưa làm được ở mục tiêu 1
    vì mục tiêu 1 dừng ở "chữ đã rút ra được", chưa tạo ra bí kíp trong kho — chưa có sự kiện để nghi
    thức bám vào.
  revisit_when: >-
    Cùng lượt với pha 3 (mục hoãn đầu tiên ở trên) — khi bí kíp thật sự vào kho thì nghi thức mới có
    thời điểm kích hoạt.

- source_spec: `_bmad-output/specs/spec-van-dao-workspace/stories/4-*.md` (Story 1.4, tách phạm vi tại step-01)
  summary: Cập nhật trạng thái chỉ điểm (da_thu / ban_hong) từ thu-bi-kip sang truong-mon qua thư ban-giao/thu/.
  evidence: >-
    Story 1.3 đã khai đủ 5 trạng thái nhưng da_thu/ban_hong chưa có đường nào tạo ra. AD-3 cấm
    thu-bi-kip ghi thẳng chi-diem.jsonl — phải gửi thư, mà hạ tầng ban-giao/thu/ chưa skill nào dựng.
    Nên đây không phải việc nhỏ ghép kèm được vào mục tiêu 1: nó là hạ tầng liên vai đầu tiên của hệ.
  revisit_when: >-
    Khi dựng hạ tầng thư ban-giao/thu/ (vai đầu tiên cần giao tiếp liên vai thật) — hoặc cùng lượt với
    pha 3 nếu lúc đó đã cần báo da_thu về cho Trưởng môn.

- source_spec: `_bmad-output/specs/spec-van-dao-workspace/stories/4-thu-bi-kip-giam-dinh-va-trich-xuat.md`
  summary: >-
    THAY THẾ mục hoãn "Cập nhật trạng thái chỉ điểm (da_thu / ban_hong) qua thư ban-giao/thu/" ở trên
    — phần `ban_hong` đã ĐƯA LẠI vào phạm vi Story 1.4, không còn hoãn. Chỉ còn `da_thu` là hoãn.
  evidence: >-
    Lý do hoãn ban đầu ("hạ tầng thư chưa dựng, đây là hạ tầng liên vai đầu tiên") sai — vòng
    elicitation Map Is Not the Territory đọc lại đặc tả §6.1 thấy ghi thẳng: hộp thư dùng được cho
    việc này KHÔNG CẦN cơ chế mới, vì nó vốn là chỗ mọi vai gửi và mọi vai đọc; đặc tả còn cho sẵn
    khuôn JSON của thư bao_ban_hong. Nên thư báo bản hỏng thuộc đúng phạm vi giám định và đã vào
    Story 1.4. Riêng `da_thu` vẫn hoãn vì nó chỉ phát sinh khi bí kíp thật sự vào kho — tức sau pha
    thiết kế sư phạm, vốn đã hoãn.
  revisit_when: >-
    Cùng lượt với pha 3 (thiết kế sư phạm) — khi bí kíp vào kho thì mới có sự kiện để báo `da_thu`.

- source_spec: `_bmad-output/specs/spec-van-dao-workspace/stories/4-thu-bi-kip-giam-dinh-va-trich-xuat.md`
  summary: Trưởng môn chưa có bước đọc hộp thư — thư `bao_ban_hong` gửi được nhưng không ai nhận, nên trạng thái `ban_hong` chưa bao giờ được đặt.
  evidence: >-
    Vòng Pre-mortem phát hiện: `truong-mon/SKILL.md` (Story 1.3) không có một dòng nào về hộp thư
    (grep chỉ ra "thư mục" và "Thư linh", không phải hộp thư). Story 1.4 thêm phía GỬI đúng khuôn
    đặc tả §6.1 nhưng phía NHẬN chưa tồn tại — nửa cơ chế. Story 1.4 vẫn gửi thư (bản ghi đúng chỗ,
    đúng khuôn) và nói thẳng với người học rằng phần cập nhật chỉ điểm chưa có, thay vì im lặng.
  revisit_when: >-
    Khi thêm bước đọc hộp thư vào `truong-mon` — hợp lý nhất là cùng lượt với pha 3 (thiết kế sư phạm),
    vì lúc đó `da_thu` cũng cần đường báo về, hai loại thư gộp một lần dựng.

- source_spec: `_bmad-output/specs/spec-van-dao-workspace/stories/4-thu-bi-kip-giam-dinh-va-trich-xuat.md`
  summary: Cơ chế nối lại đầy đủ khi file sách dời chỗ (đặc tả §6.9) — Story 1.4 chỉ làm phần tối thiểu.
  evidence: >-
    Story 1.4 lưu con trỏ tới file gốc (không lưu bản sao, đúng §6), nên con trỏ chết khi người học
    đổi tên hoặc chuyển thư mục sách. Đã làm phần rẻ: phát hiện file không còn ở đường dẫn cũ, hỏi
    đường dẫn mới, cập nhật đúng bản ghi. Chưa làm cơ chế nối lại đầy đủ của §6.9 (dò tìm tự động,
    khớp theo dấu vân tay nội dung...).
  revisit_when: >-
    Khi kho có nhiều sách và việc dò tay từng cuốn trở nên phiền — hoặc khi gặp ca thật đầu tiên
    người học không nhớ đã để sách ở đâu.

- source_spec: `_bmad-output/specs/spec-van-dao-workspace/stories/4-thu-bi-kip-giam-dinh-va-trich-xuat.md`
  summary: CI không kiểm phiên bản engine và cũng không chạy eval — hai lớp mù chồng lên nhau ở đúng phụ thuộc ngoài quan trọng nhất.
  evidence: >-
    Vòng Cascading Failure phát hiện: `book-to-skill` là đường DUY NHẤT đưa nội dung vào hệ, mà
    `.github/workflows/kiem.yml` chỉ chạy `pytest tests/` — không cài engine, không kiểm phiên bản,
    không chạy `evals.json` của skill nào (điểm sau đã defer từ Story 1.1, nay chồng thêm rủi ro mới).
    Story 1.4 đã vá phần rẻ nhất: ghim SHA trong requirements-dev.txt và ghi số hiệu bản vào bằng
    chứng. Nhưng nếu engine đổi hình dạng dict trả về, không có gì bắt được cho tới khi một người
    thật thử thêm sách.
  revisit_when: >-
    Khi thêm bất kỳ phép kiểm tự động nào cho skill (chạy eval trong CI, hoặc một smoke test gọi
    extract_single_file trên sách chung) — hai việc này nên làm cùng lượt vì cùng cần engine trong CI.

- source_spec: `_bmad-output/specs/spec-van-dao-workspace/stories/4-thu-bi-kip-giam-dinh-va-trich-xuat.md`
  summary: Thư `bao_ban_hong` của Story 1.4 ghi vào một hộp thư chưa tồn tại và chưa có file gác cửa — theo luật đặc tả thì coi như không vai nào đọc được.
  evidence: >-
    Vòng review trước khi duyệt Story 1.4 phát hiện: R26 (đặc tả dòng 1279) nói "Thiếu file
    `.pham-vi.json` → coi như **không vai nào đọc được**, fail an toàn", và §15.1 khai sẵn giá trị
    cho hộp thư chung: `{ "schema": 1, "ghi": "*", "doc": ["*"] }`. Nhưng `van-dao/` hiện **không có
    thư mục `ban-giao/` nào cả** — nên thư Story 1.4 gửi đi sẽ ghi thành công vào một nơi mà luật của
    chính đặc tả tuyên bố vô hình. Đây khác với mục "thư một chiều" đã ghi ở trên: mục kia là *chưa ai
    đọc*, mục này là *kể cả biết mở cũng bị luật chặn*. Việc này đặc tả đã lên lịch sẵn ở §16 Vòng 1
    bước 5b (`.pham-vi.json` cho từng thư mục `ban-giao/` + `bin/kiem-thu.py` bản đầu đối chiếu R27),
    chưa làm. Story 1.4 giữ nguyên phạm vi (người dùng chọn [V] tại cổng duyệt) vì tạo thư mục bàn
    giao + file gác cửa là mở rộng phạm vi, không phải vá lỗi diễn đạt.
  revisit_when: >-
    Lúc làm §16 Vòng 1 bước 5b — và **chậm nhất là cùng lượt với bước đọc hộp thư của `truong-mon`**
    (mục "thư một chiều" ở trên), vì tới lúc đó thiếu file gác cửa sẽ làm chính bước đọc đó vô nghĩa.

- source_spec: `_bmad-output/specs/spec-van-dao-workspace/stories/4-thu-bi-kip-giam-dinh-va-trich-xuat.md`
  summary: Trường `bi_kip_chi_diem` trong khuôn thư `bao_ban_hong` chưa có nguồn xác định để điền.
  evidence: >-
    Khuôn thư §6.1 (đặc tả dòng 935) có `"bi_kip_chi_diem": "software-requirements"` — Trưởng môn dùng
    nó để tìm đúng dòng trong `chi-diem.jsonl` mà đổi trạng thái sang `ban_hong` (§10.4). Nhưng đặc tả
    không định nghĩa trường định danh của một mục chỉ điểm, và `thu-bi-kip` nhận **một đường dẫn file**
    chứ không nhận một mục chỉ điểm: người học hoàn toàn có thể đưa cuốn sách chưa từng qua chỉ điểm.
    Không có luật nào nói điền gì trong ca đó. Story 1.4 không tự quyết vì việc này chạm vào lược đồ
    dữ liệu của vai khác (AD-3 — Trưởng môn là người ghi duy nhất của `chi-diem.jsonl`).
  revisit_when: >-
    Trước khi viết bước gửi thư ở step-03 của chính story này — đây là quyết định phải chốt để viết
    được `SKILL.md`, không dời xa hơn được. Nếu lúc đó chưa chốt được nguồn, lối ra rẻ nhất là hỏi
    người học tên sách đã được chỉ điểm, và bỏ trống trường khi họ nói sách này tự tìm.
  resolved: >-
    2026-08-28, tại step-03 đúng mốc đã ghi. Chốt: hỏi người học tên sách đã được chỉ điểm rồi rút
    định danh kebab-case từ chính tên đó; để TRỐNG khi họ tự tìm (thư mang định danh sai tệ hơn thư
    để trống — bên nhận sẽ sửa nhầm chỉ điểm khác); và luôn ghi thêm `ten_sach` làm đường khớp dự
    phòng, vì định danh sinh lại có thể lệch khi Trưởng môn đã thêm hậu tố số cho hai tên gần giống.
    Hướng "không gửi thư khi sách không đến từ chỉ điểm" có lập luận thiết kế mạnh hơn nhưng bị loại
    ở lượt này: nó đòi mở lại khối đã duyệt của spec, mà bên nhận chưa dựng nên chưa quan sát được gì
    để biết chắc. Xét lại khi `truong-mon` đọc hộp thư thật và thấy thư định danh trống là vô dụng.

- source_spec: `_bmad-output/specs/spec-van-dao-workspace/stories/4-thu-bi-kip-giam-dinh-va-trich-xuat.md`
  summary: Cả ba skill hiện có đều vượt trần ngân sách token của AD-8 — cần một lượt rà chung, và có thể cần xét lại chính con số trần.
  evidence: >-
    Vòng review step-04 của story 1.4 đo bằng `tiktoken/cl100k_base` (không phải ước bằng số ký tự —
    cách ước cũ sai 40% vì tiếng Việt có dấu tốn token gấp rưỡi): `thu-bi-kip` 7.967 → đã vá xuống
    5.054 bằng cách tách `references/dinh-dang.md` và cắt lý lẽ; nhưng `truong-mon` 7.334 và
    `nhap-mon` 6.018 vẫn nguyên. Trần AD-8 là ~5K/skill và ~25K/phiên. Ba skill hiện tại cộng lại
    ~18.4K, tức skill thứ tư gần như chắc chắn đẩy phiên vượt trần. Story 1.4 chỉ vá skill của
    chính nó — sửa hai skill kia là chạm vào phạm vi story khác đã đóng.
  revisit_when: >-
    Trước khi viết skill thứ tư (Epic 2, lộ đồ) — đó là lúc tổng phiên chạm trần thật, và cũng là
    lúc duy nhất còn rẻ để quyết định giữa hai hướng: rà gọn hai skill cũ theo cùng cách đã làm với
    `thu-bi-kip`, hay đo lại xem con số trần 5K/25K có còn đúng với mô hình hiện tại không.
