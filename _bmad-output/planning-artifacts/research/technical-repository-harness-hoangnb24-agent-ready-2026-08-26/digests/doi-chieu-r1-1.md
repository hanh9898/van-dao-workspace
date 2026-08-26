# Digest — Đối chiếu với AGENTS.md Vấn Đạo (round 1)

*Lưu ý nguồn: brief ban đầu bị lỗi placeholder rỗng, điều phối viên đã gửi bù nội dung thật AGENTS.md — so sánh dưới đây dùng nội dung thật.*

## Khác biệt cụ thể (trích được cả hai phía)

**1. CLAUDE.md là file "trỏ" riêng tách khỏi nội dung canonical**
- harness: `CLAUDE.md` chỉ 1 dòng import `@AGENTS.md`, bọc marker `HARNESS:BEGIN/END`; nội dung thật nằm ở `AGENTS.md`.
- Vấn Đạo: khối `<!-- bmad:context -->` nằm trong chính AGENTS.md, không có `CLAUDE.md` riêng được xác nhận tồn tại trong đoạn được cấp.
- Đánh giá: chưa xác nhận được đây có phải khác biệt thật — không có bằng chứng dự án CÓ hay KHÔNG CÓ CLAUDE.md.

**2. Vòng đời kế hoạch `docs/plans/active/` → `docs/plans/completed/`**
- harness: mỗi kế hoạch 1 file, di chuyển thư mục khi validation xong.
- Vấn Đạo: 1 status doc sống (`docs/VAN-DAO-trang-thai-du-an.md`, tra theo §) + `_bmad-output/planning-artifacts` vs `implementation-artifacts` tách theo LOẠI, không theo trạng thái active/completed.
- Đánh giá: khác biệt thật nhưng KHÔNG đáng học nguyên xi — hai triết lý khác nhau, dự án đã có giải pháp hợp lý cho quy mô của nó.

**3. `.agents/skills/` — phân tầng "mặc định cài" vs "explicit-only, gọi `$lệnh`"**
- harness: 5 skill, 3 trong đó "explicit-only" (chỉ chạy khi gọi tường minh, không tự nạp).
- Vấn Đạo: đã có `van-dao/skills/` với quy ước SKILL.md bắt buộc ("Xong khi", "Khi nào không giúp được", "Trình→xác nhận→ghi→kiểm") — không phải chỗ trống.
- Điểm còn thiếu hẹp hơn: đoạn được cấp không nói rõ có phân tầng "tự nạp vs explicit-only" hay không. Chưa xác nhận được.

**4. Luật bằng lời ⇄ check tự động, có tên, tái dùng được — Vấn Đạo chỉ có 1 cặp cụ thể**
- harness: skill `$encode-invariant` — quy trình tổng quát 5 bước (tìm authority → xác nhận + cấm biến convention-chưa-duyệt thành policy → thiết kế guard tối thiểu → cài kèm bằng chứng dương/âm → khảo sát enforcement có sẵn), gắn `docs/patterns/encoding-invariants.md`.
- Vấn Đạo: đã có TINH THẦN này ở 1 cặp cụ thể — `bi-kip.schema.md` §6 (luật bằng lời của phép kiểm script) đi cặp `kiem-bi-kip.py`, "đổi một bên thì đổi bên kia trong cùng một thay đổi, kèm fixture và test" — nhưng CHỈ áp dụng cho 1 cặp file, không phải quy trình đặt tên tái dùng được cho luật mới bất kỳ, không có bước "trích nguồn authority" hay yêu cầu tường minh bằng chứng dương+âm.
- **Đánh giá: ĐÁNG HỌC MỘT PHẦN** — không cần cả bộ máy 5-cổng, nhưng tổng quát hoá thành 1 dòng quy ước lặp lại được ("luật mới cần validate → luôn viết cặp luật-bằng-lời + test dương/âm + ghi rõ ai/đâu cho phép luật này") sẽ hữu ích vì dự án đã thực hành đúng tinh thần ở 1 chỗ, chưa phát biểu thành quy ước chung.

**5. Changelog riêng cho tài liệu/harness của agent**
- harness: CHANGELOG.md root có nhóm "Documentation & Decision Records" (ADR) và "Agent Skills & AI Integration" — thay đổi tài liệu-cho-agent được log có PR, có mô tả LÝ DO.
- Vấn Đạo: chỉ 1 dòng mốc "Verified 2026-08-25..." — bản chụp mới nhất, không có lịch sử/lý do các lần đổi trước.
- Đánh giá: khác biệt thật, giá trị học THẤP/TRUNG BÌNH — git log đã cho lịch sử thô; cái harness thêm là lý do được tóm tắt/phân loại. Với nhóm nhỏ 1 agent đã có git blame, lợi ích thêm CHANGELOG riêng là nhỏ — không ưu tiên.

**6. Harness = gói cài đặt/cập nhật độc lập (installer + verify + merge 3-way) vs skill nội bộ bmad-project-context**
- harness: installer bash/PowerShell, xác thực cryptographic, cờ `--merge/--override/--dry-run`, `status/doctor/update` với 3-way merge.
- Vấn Đạo: "Managed by bmad-project-context; sửa trong khối này sẽ bị ghi đè ở lần refresh sau" — skill BMAD ghi đè khối marker.
- Đánh giá: khác biệt thật nhưng KHÔNG đáng học — dự án đã dùng BMAD nhất quán toàn workspace, đổi sang installer riêng sẽ xung đột công cụ.

## Tổng kết — đáng học thật

**Đáng cân nhắc học:** (4) Tổng quát hoá "luật bằng lời ⇄ check tự động, kèm bằng chứng dương/âm" thành 1 dòng quy ước lặp lại được trong AGENTS.md — dự án đã có tinh thần này ở 1 chỗ (bi-kip schema), chưa phát biểu thành quy ước chung.

**Không ưu tiên/khác bản chất:** (2) vòng đời plans active/completed — đã có giải pháp khác phù hợp quy mô. (6) installer/versioning riêng — sẽ xung đột BMAD. (5) changelog riêng cho AGENTS.md — lợi ích biên thấp.

**Chưa đủ bằng chứng kết luận:** (1) có/không CLAUDE.md riêng dạng pointer. (3) có/không phân tầng skill mặc-định vs explicit-only trong `van-dao/skills/`.

## Nguồn đã tra
raw.githubusercontent.com + api.github.com: AGENTS.md, CLAUDE.md, README.md, `.agents/skills/encode-invariant/SKILL.md`, CHANGELOG.md (qua WebFetch tóm tắt, không phải nguyên văn 100% — lưu ý mức tin cậy thấp hơn phần trích raw trực tiếp), listing API `.agents/`, `.agents/skills/`, root repo.
