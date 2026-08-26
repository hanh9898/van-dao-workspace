# Digest — Đối chiếu ghost-writer với van-dao (round 1)

*Thực hiện trực tiếp bởi người điều phối (không qua subagent riêng) — tránh đúng lỗi placeholder-rỗng đã gặp ở lần đối chiếu trước (repository-harness). Nguồn phía van-dao: nội dung `AGENTS.md` đọc trực tiếp ngày 2026-08-27 (khối `<!-- bmad:context -->`, đã verify cùng ngày). Nguồn phía ghost-writer: `digests/co-che-r1-1.md` (đọc sơ cấp từ mã nguồn cục bộ). Một số điểm dưới đây cần đối chiếu thêm với đặc tả/skill thật của van-dao (`docs/VAN-DAO-dac-ta-v1.0.md`, `van-dao/skills/`) — không có trong AGENTS.md — được đánh dấu rõ "chưa xác minh, cần đối chiếu thêm" thay vì khẳng định.

## Đáng học — cụ thể, có thể áp dụng

**1. Thang leo escalation khi người học "bí", có trạng thái `deferred` chính thức (skill `demolish`)**
- ghost-writer: khi tác giả không phản hồi được một phê bình, hệ thống có đúng 4 bước cố định (diễn đạt lại đơn giản hơn → thu hẹp về 1 claim → hỏi trực giác → 3 lối thoát có cấu trúc: Modify/Narrow/Accept) trước khi park vấn đề vào trạng thái `deferred` — không ép tiếp, không bỏ rơi.
- van-dao: đã có khái niệm `sai_lam_pho_bien` (danh sách sai lầm phổ biến, R13 "rỗng ≠ vắng") nhưng AGENTS.md không cho thấy có quy trình leo thang tường minh khi đệ tử/vai chấm gặp bế tắc, cũng không có từ vựng trạng thái tương đương `deferred`/`accepted-limitation` cho một khúc mắc chưa giải được.
- Đánh giá: **đáng học** — mẫu leo thang 4 bước + từ vựng trạng thái tường minh là thứ cụ thể, nhỏ, cấy được vào vai chấm (Nghiệm Công Sứ/Phúc Khảo Sứ) mà không cần biết chi tiết cơ chế hiện tại của van-dao. Cần đối chiếu với đặc tả trước khi đề xuất chính thức — có thể van-dao đã có cơ chế tương đương chưa lộ trong AGENTS.md.

**2. Nâng cấp cấu trúc tường minh, có ngưỡng, cần xác nhận, không đổi nội dung (skill `longform-upgrade`)**
- ghost-writer: khi sách vượt ngưỡng 10 chương, có skill riêng tự đề xuất (không tự động áp), hỏi tác giả xác nhận cách chia trước khi đổi, và tuyên bố rõ "không đổi nội dung, chỉ đổi cách quản lý context" — sau đó chỉ 2/27 skill còn full-read, còn lại lazy-read theo phần.
- van-dao: AGENTS.md ghi nhận đúng vấn đề song sinh — "Bậc" (đặc tả §13.1) và "Vòng" (đặc tả §16) từng lệch nhau thật (`phuc-khao` bị gắn Bậc 3 dù cần dùng ở Vòng 2) — cho thấy quy mô/độ phức tạp tăng dần đã từng gây lỗi thiết kế. Van-dao cũng đã có nguyên tắc "ba đường truyền tin định nghĩa bằng thứ KHÔNG mang theo" — cùng tinh thần lazy-read nhưng áp theo VAI (role-to-role), chưa rõ có áp theo QUY MÔ bí kíp (bí kíp rất nhiều chương) hay không.
- Đánh giá: **đáng cân nhắc** — không phải sao chép nguyên xi (van-dao không phải sách viết tuần tự nên "ngưỡng 10 chương" không áp dụng thẳng), nhưng ý tưởng "một bước nâng cấp cấu trúc TƯỜNG MINH, có ngưỡng, cần xác nhận" khi bí kíp lớn dần là hướng đáng hỏi kiến trúc sư (Winston) khi bàn architecture, không phải thêm ngay.

**3. Skill "resume" cho người dùng cuối: quét nhanh cố định, cấm đọc sâu, luôn đúng 1 khuyến nghị, không liệt kê menu**
- ghost-writer: `/ghost-writer:resume` là "lệnh duy nhất cần nhớ" — đọc 5 nguồn cố định, cấm đọc toàn văn, luôn trả về đúng 3 khối (LAST TIME/WAITING/NEXT) và đúng 1 khuyến nghị kế tiếp theo bảng if/else 8 nhánh cố định, giọng "welcome back" chứ không phải dashboard.
- van-dao: đối tượng tương đương là **đệ tử quay lại lộ trình học sau một thời gian** (không phải người vận hành workspace BMAD — `docs/VAN-DAO-trang-thai-du-an.md` là tài liệu cho người/AI vận hành dự án, không phải cho đệ tử). AGENTS.md không cho thấy van-dao có/không có một skill "chào lại, tóm tắt lần trước, đúng 1 việc kế tiếp" hướng tới đệ tử — **chưa xác minh được**, cần hỏi đặc tả (có thể vai "thư linh" đã làm việc này).
- Đánh giá: **câu hỏi để hỏi, không phải kết luận** — nếu van-dao CHƯA có, đây là mẫu nhỏ gọn, cụ thể, dễ cấy (khuôn 3 khối + luật "luôn 1 khuyến nghị, không liệt kê"); nếu ĐÃ có, không cần làm gì.

## Cảnh báo — phản-mẫu (đáng học kiểu "đừng làm vậy")

**4. Ghi đè state ngầm mâu thuẫn với nguyên tắc đã tuyên bố (skill `integrate`, bước silent-overwrite `voice-sample.md`)**
- ghost-writer tuyên bố "Memory is explicit — mọi thứ đều ghi rõ" nhưng chính `integrate` lại âm thầm ghi đè `voice-sample.md` mà "không nói cho tác giả biết" khi đủ điều kiện — tự mâu thuẫn với nguyên tắc gốc của chính nó.
- van-dao: NFR (đã có trong PRD/kiến trúc phiên trước, không nhắc lại chi tiết ở đây) quy định "mọi thay đổi trạng thái phải append-only" — đúng hướng ngược lại. Đây là bằng chứng cụ thể (không phải giả định) cho thấy kỷ luật append-only/explicit-state của van-dao là lựa chọn đúng, không phải quá thận trọng — một dự án tương tự vi phạm đúng chỗ này và tự phá vỡ lời hứa của mình.
- Đánh giá: **không cần thay đổi gì ở van-dao** — dùng làm bằng chứng củng cố quy ước đã có, không phải hành động mới.

## Không ưu tiên / không đủ tương đồng để học nguyên xi

**5. Vòng đời co-authoring qua Git (CONTRIBUTING.md: nhánh riêng, quy ước commit message, danh sách file "luôn commit cùng nhau")** — mô hình dành cho nhiều TÁC GIẢ SÁCH cùng cộng tác qua git; van-dao có mô hình khác hẳn (bí kíp là input người dùng đưa vào, không phải nhiều tác giả cộng tác qua nhánh git). Không áp dụng.

**6. Macro command gói atomic skill (`start`/`chapter`/`review`/`finish`) cho người dùng không muốn tự điều phối trình tự** — ý tưởng UX nhẹ, có thể hữu ích nếu van-dao có nhiều skill atomic mà thầy/đệ tử phải tự nhớ trình tự gọi, nhưng giá trị biên thấp so với 2 mục đã nêu — không ưu tiên.

**7. Field `language` đọc ở đầu mọi SKILL.md, luôn xuất theo ngôn ngữ cấu hình bất kể input ngôn ngữ gì** — ghost-writer hỗ trợ đa ngôn ngữ tác giả; van-dao nhắm đối tượng học tiếng Việt là chính, khả năng cần đa ngôn ngữ thấp hơn nhiều. Không ưu tiên.

## Tổng kết

**Đáng mang ra hỏi/đề xuất chính thức (theo đúng thứ tự ưu tiên):** (1) từ vựng trạng thái + thang leo thang khi vai chấm/đệ tử bế tắc — cụ thể nhất, rủi ro thấp nhất khi cấy. (3) skill "chào lại đệ tử" kiểu resume — cần hỏi trước xem đã có chưa. (2) nâng cấp cấu trúc tường minh theo ngưỡng quy mô — mức kiến trúc, để dành cho lúc bàn với Winston.

**Dùng làm bằng chứng, không phải hành động:** (4) phản-mẫu ghi đè ngầm — củng cố NFR append-only hiện có.

**Không đáng học:** (5) mô hình co-authoring git, (7) field ngôn ngữ đa dạng. **Giá trị biên thấp:** (6) macro command.

**Giới hạn của đối chiếu này:** chỉ dựa trên AGENTS.md (bản tóm tắt), chưa đọc trực tiếp đặc tả đầy đủ hay skill thật của van-dao (`van-dao/skills/`, `docs/VAN-DAO-dac-ta-v1.0.md`) — 3 mục "đáng học" ở trên đều cần xác minh lại có thể đã tồn tại rồi hay chưa trước khi coi là gap thật.
