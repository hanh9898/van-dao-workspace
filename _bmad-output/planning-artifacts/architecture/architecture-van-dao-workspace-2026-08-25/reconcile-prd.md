# Reconcile: ARCHITECTURE-SPINE.md ↔ PRD

Đối chiếu `ARCHITECTURE-SPINE.md` (draft, 2026-08-25) với `prd-van-dao-workspace-2026-08-24/prd.md` (status: final). Chỉ liệt kê những gì PRD nói mà spine không phản ánh được — không lặp lại phần đã khớp tốt.

## Khớp tốt (không cần nêu lại)

FR6/FR7 (AD-6), FR8 (AD-1/AD-4 fresh-subagent-never-fork), FR11a-c (info-hiding edges TL→NC/TL→PK), FR15 (AD-7), Non-Goal #6 (Stack: nền tảng bắt buộc Claude Code), FR31 (Deferred, đúng lý do Vòng 3), FR16-21/FR13-15/FR24/FR30 (đúng ngoài phạm vi spine vì thuộc Vòng 3/4, không bị lặp chi tiết).

## Khoảng trống tìm thấy (6)

### 1. FR29 — ranh giới riêng tư của Chú Giải Sứ không thành AD [QUAN TRỌNG]

PRD: "*không mang chi tiết tình huống thật của người học ra ngoài* (không tên người, công ty, dự án cụ thể) — **đây là vai duy nhất có đầu ra rời khỏi máy người học**." Đây là ranh giới dữ liệu nghiêm trọng nhất trong toàn hệ (khớp trực tiếp dòng Policy đầu tiên của AGENTS.md: "không bao giờ commit nội dung sách hoặc hồ sơ người học"). Spine chỉ nhắc Chú Giải Sứ qua cạnh `TL --> CG` trong diagram và một dòng trong cây thư mục dữ liệu — không có AD nào khoá lại "đầu ra của Chú Giải Sứ phải được lọc ẩn danh trước khi rời máy" hay chỉ rõ *đường nào* dữ liệu rời máy (khác với 4 vai chấm khác, tất cả đều ở lại cục bộ). Hai người dựng độc lập hoàn toàn có thể chọn khác nhau ở đây — một người coi Chú Giải Sứ là vai nội bộ như các subagent khác, một người mới nhận ra nó có đường ra ngoài. Nên là AD riêng.

### 2. FR33 — nhất quán giọng điệu (chống sáo rỗng) xuyên 8 skill không có cơ chế giữ [QUAN TRỌNG]

PRD: "Hệ không được khen ngợi mang tính xã giao/nịnh bợ... Áp dụng cho **mọi phản hồi của hệ** (Dạy, Soát, Nền), không riêng lúc gắn nghi thức." Đây là ràng buộc cross-cutting áp lên toàn bộ 8 SKILL.md độc lập. Spine không có AD hay dòng Consistency Convention nào nói *làm sao* giữ nhất quán — 8 tác giả skill khác nhau (hoặc cùng một agent viết ở các lượt khác nhau) hoàn toàn có thể diễn đạt luật này khác nhau hoặc quên. Đáng ít nhất một dòng convention (vd. một đoạn rule dùng chung mà mọi SKILL.md tham chiếu, hoặc một behavioral eval bắt buộc — PRD đã tự nói "kiểm bằng behavioral eval").

### 3. FR12a — quy tắc phá thế cân bằng ("nghiêng về người học") không có AD [VỪA]

PRD: "khi bằng chứng cân bằng, kết quả luôn nghiêng về hướng có lợi cho người học." Đây là một quy tắc hành vi cụ thể, kiểm được, và là loại quyết định hai đơn vị dựng độc lập dễ chọn khác nhau nhất (một bên mặc định an toàn/nghiêm khắc, bên kia nghiêng về người học như PRD yêu cầu). Spine chỉ nói tới cờ bất đồng ở AD-7 (khía cạnh "không dùng Hook"), không nói tới quy tắc phá thế này.

### 4. AD-3 "Binds" liệt kê thiếu vùng [NHẸ, cơ học]

AD-3 liệt kê `truong-mon/**, thu-linh/**, truong-lao/**, tang-kinh/**, chu-giai/**, ban-giao/**` nhưng bỏ sót `dao-tam` (đệ tử sở hữu — chính PRD FR22 nhấn mạnh đây là vùng ghi đặc biệt, disable-model-invocation) và `bi-kip/` (Tàng kinh trưởng lão sở hữu). Luật chung trong Rule text vẫn đúng ("mỗi thư mục... đúng một vai") nên đây không phải lỗi logic, chỉ là danh sách Binds không đầy đủ — dễ đọc nhầm thành "chỉ 6 vùng này có luật single-writer".

### 5. FR32 — hợp đồng "chưa hỗ trợ ở bản này" không có AD [VỪA]

PRD: bắt buộc từ MVP, áp dụng cho *mọi* ý định của `/vd:chi-duong` khi cơ chế đứng sau chưa dựng ở Vòng hiện tại — "không im lặng bỏ qua, không đoán liều thay." Đây là một cross-cutting behavior contract thật (giống FR33) nhưng không xuất hiện ở đâu trong spine — không AD, không dòng trong Capability→Architecture Map cho 4.7, dù bảng đó có ghi "4.7 | all | AD-1…AD-7 (tổng hợp)" một cách chung chung không trỏ đúng AD nào cho FR32 cụ thể.

### 6. FR9 — "Giám khảo cấm chấm" chỉ ngụ ý, không phải AD tường minh [NHẸ]

Được thể hiện gián tiếp qua bảng quyền §4.2 (trỏ tới qua AD-3's "bảng §4.2 là nguồn thật") và qua diagram (không có cạnh GK→người học chấm). Nhưng AD-1's danh sách "ba cạnh trọng yếu" không nhắc edge này — trong khi PRD gọi nó là FR9 riêng, có nguồn R20. Có thể đủ (đã có ở bảng quyền được trỏ tới), nhưng đáng cân nhắc thêm một dòng trong AD-1 nếu muốn tường minh ngang hàng ba cạnh kia.

## Không tìm thấy mà đáng ghi nhận thêm

FR10 (trích câu làm căn cứ) và FR23 (nghi thức gắn việc thật) đúng là không thuộc phạm vi spine (rubric/content-level, không phải kiến trúc) — không tính là gap.
