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
