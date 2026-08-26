# Digest — Độ trưởng thành / tín hiệu cộng đồng thật (round 1)

*Ngày truy cập mọi nguồn: 2026-08-27, qua GitHub REST API trực tiếp + web search.*

## 1. Repo `simonediroma/claude-ghost-writer`

- Tạo 2026-04-18, push cuối 2026-06-07 (~7 tuần hoạt động rồi im lặng ~11 tuần tính tới 2026-08-27). Nguồn: GitHub API, cao tin cậy.
- `stargazers_count`/`forks_count`/`watchers_count`/`subscribers_count`/`network_count`/`open_issues_count` đều **= 0**. Không có GitHub Release nào (kể cả v1.0.0) — version chỉ tồn tại trong CHANGELOG.md, không phải Release object.
- 4 "issue" trả về đều thực chất là PR đã tự-merge bởi chính chủ repo (`author_association: OWNER`) — không có issue/PR thật từ người ngoài.
- 16 commit (2026-04-18 → 2026-06-07), chỉ 2 "tác giả": `simonediroma` và bot "Claude" (Claude Code session commits) — không có contributor ngoài.
- Có mặt trong `anthropics/claude-plugins-community` marketplace, nhưng entry trỏ tới sha `7e59bee` (2026-05-10) — **cũ hơn** 3 commit "Sprint tối ưu token" cuối (2026-06-06/07) — bản trên marketplace chưa đồng bộ bản mới nhất.

## 2. Người dùng ngoài tác giả

Không tìm thấy: fork, sao, issue thật, thảo luận Reddit/HN/blog/Twitter về plugin này hay tác giả trong ngữ cảnh này. Đây là "không xác nhận được có ai dùng", không phải bằng chứng phủ định tuyệt đối — cài qua marketplace không để dấu vết công khai trên GitHub.

## 3. `quantum_fatalism` — dự án gốc của phương pháp

- Tạo và push toàn bộ trong **cùng một ngày** (2026-04-16, ~9.5 giờ làm việc).
- Có `essay.md` (en, 45KB) + `saggio.md` (it, 46KB) — văn bản **hoàn chỉnh**, có cấu trúc essay thật (đã đọc trực tiếp phần đầu/cuối). README tự thuật "đã qua 8 phiên bản" theo đúng chu trình hỏi-đáp→viết→demolition→tích hợp mà plugin quảng cáo.
- Cũng 0 sao/fork/issue — không tương tác cộng đồng. Claim "8 phiên bản" chỉ có nguồn là tự-thuật của tác giả, chưa đối chiếu độc lập (`ships_log.md`/`diario_di_bordo.md` chưa đọc sâu). Không tìm thấy essay được xuất bản ở đâu ngoài GitHub cá nhân.
- **Đây là bằng chứng sơ cấp tốt nhất hiện có** rằng phương pháp gốc từng ra được ít nhất 1 sản phẩm hoàn chỉnh — nhưng tự-xuất bản, chưa qua biên tập độc lập nào được xác minh.

## 4. Marketplace / review bên ngoài

Marketplace `anthropics/claude-plugins-community` chỉ yêu cầu qua "automated validation và safety screening" khi nộp — **không phải** biên tập thủ công của con người (khác `claude-plugins-official`). Có mặt trên marketplace ≠ đã được kiểm chứng chất lượng qua sử dụng thật. Không tìm thấy review/bài viết nào về plugin hay marketplace cộng đồng này.

## Lead chưa đào sâu

Vênh sha marketplace vs commit mới nhất (mô tả "constructive demolition protocol" trên marketplace có thể là bản mô tả cũ hơn "quantum_fatalism writing method" hiện tại trên GitHub) — chưa xác nhận có ảnh hưởng gì tới hành vi plugin thật đang cài hay không.

## Không xác nhận được

- Quantum_fatalism từng xuất bản ngoài GitHub cá nhân — không tìm ra.
- Claim "8 phiên bản" bằng nguồn độc lập với tác giả.
- Có/không người dùng thật ngoài tác giả đã cài plugin qua marketplace (không có kênh đo lượt cài công khai).
- Marketplace listing có bị Anthropic áp điều kiện/gỡ gì khác không — chỉ xác nhận entry hiện diện tại thời điểm truy cập.
