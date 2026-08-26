---
title: 'technical research: repository-harness (hoangnb24) — agent-ready workspace generator'
type: 'technical'
topic: 'repository-harness (hoangnb24) — agent-ready workspace generator'
decision: 'Hiểu tư duy/phương pháp thiết kế harness cho repo, soi lại thực hành AGENTS.md của Vấn Đạo/BMAD'
source: 'https://github.com/hoangnb24/repository-harness'
status: complete
preset: 'standard'
validation: 'normal'
created: '2026-08-26'
updated: '2026-08-26'
claims_verified: 8
claims_unverified: 1
---

# technical research: repository-harness (hoangnb24) — agent-ready workspace generator

**Decision this research serves:** Hiểu tư duy/phương pháp thiết kế harness cho repo, soi lại thực hành AGENTS.md của Vấn Đạo/BMAD

## Executive Summary

`repository-harness` là một Rust binary thật (1198 sao, pre-1.0, gần như một người vận hành) sinh và bảo trì `AGENTS.md`/`CLAUDE.md`/cấu trúc tài liệu cho repo bất kỳ, có installer/updater ba chiều (three-way merge). Bảy nguyên tắc thiết kế của nó (docs/HARNESS.md) đều xoay quanh một trục: **repo là nguồn sự thật, AGENTS.md chỉ là entrypoint gọn dẫn tới đó — không phải nơi nhồi nội dung, và mọi tuyên bố "xong" phải có bằng chứng chạy được, không phải tự báo cáo.**

Đối chiếu trực tiếp với `AGENTS.md` hiện tại của Vấn Đạo (workspace này), phần lớn khác biệt là **khác triết lý phù hợp quy mô riêng** (harness quản nhiều repo/nhiều agent, Vấn Đạo là 1 plugin/1 agent qua BMAD), không phải chỗ trống cần lấp. Có **đúng một điểm đáng học thật**: Vấn Đạo đã có tinh thần "luật bằng lời ⇄ check tự động" ở một cặp cụ thể (`bi-kip.schema.md` §6 ↔ `kiem-bi-kip.py`) nhưng chưa phát biểu thành quy ước chung, tái dùng được cho luật mới — harness làm điều này tường minh qua skill `$encode-invariant` (5 bước có tên, có tài liệu riêng).

**Caveat lớn nhất:** repo pre-1.0, đang đổi kiến trúc mạnh (vừa khai tử cả một dòng sản phẩm — SQLite `harness-cli`/protocol v1 — ngày 2026-08-10), và có một PR audit ngoài (chưa merge) tự báo phát hiện lỗ hổng path traversal thật — không ảnh hưởng tới việc học nguyên tắc thiết kế (nguyên tắc không phụ thuộc code có bug hay không), nhưng nếu ai định *dùng thật* công cụ này (không phải Vấn Đạo — Vấn Đạo chỉ học nguyên tắc) thì nên đợi audit đó merge trước.

## 1. Kiến trúc & tư duy thiết kế

**`.agents/`, `AGENTS.md`, `CLAUDE.md` — ba vai trò tách biệt rõ.** `AGENTS.md` (gốc, 1613 byte) là payload nội dung thật, bọc marker `<!-- HARNESS:BEGIN -->...END -->` cho phép updater merge ba chiều mà không mất chỉnh sửa cục bộ; là "entry map và authority boundary" quy định đọc `docs/WORKFLOW.md`, coi answer/review/diagnosis là read-only, dừng lại nếu chính sách sản phẩm chưa rõ, "Claim completion only with executable or observable evidence" [1]. `CLAUDE.md` (258 byte) hoàn toàn không có nội dung riêng — chỉ một dòng import bắt buộc để tương thích với việc Claude Code không tự nạp `AGENTS.md`: *"Claude Code does not auto-load AGENTS.md. Import that single canonical project instruction source... @AGENTS.md"* [1]. `.agents/skills/` chứa 5 skill (`audit-onboarding-proposal`, `encode-invariant`, `engineering-wisdom`, `improve-harness`, `onboard-repository`), kích hoạt qua slash-command tường minh (`$encode-invariant`...) — tách hẳn khỏi `AGENTS.md` (luôn nạp): *"No skill runs during installation. Onboarding and Harness improvement remain explicit-only"* [2].

**`crates/` chỉ có 1 crate** (`crates/harness`, workspace 1 thành viên — xác nhận trực tiếp từ `Cargo.toml`, không phải nhiều crate như tên "crates/" số nhiều có thể gợi ý) [3]. Kiến trúc hexagonal/clean: domain (paths, hashes, provenance, merge outcomes — không phụ thuộc filesystem/CLI) ← application (use case: install, update, status, doctor...) ← infrastructure (filesystem transaction, Git 3-way merge, download, checksum) ← interface (parse command, render report); *"Architecture tests reject outward dependencies from inner layers"* — kiểm bằng test tự động, không chỉ quy ước bằng lời [4].

**Bảy nguyên tắc thiết kế** (`docs/HARNESS.md`, "Principles", trích nguyên văn) [5]:
1. *Repository truth wins* — tài liệu sản phẩm, quyết định, kế hoạch, code, test, CI, bằng chứng runtime, và Git history là nguồn sự thật.
2. *Load the smallest useful context* — `AGENTS.md` là entrypoint, không phải bách khoa toàn thư.
3. *Process follows work shape* — việc nhỏ giữ nhỏ; việc phối hợp/nhiều-phiên mới cần 1 kế hoạch bền.
4. *Material choices stay human-owned* — thiếu chính sách sản phẩm thì dừng, không tự quyết.
5. *Behavior proves completion* — ghi chép quy trình và tự báo cáo không thay được bằng chứng chạy được/quan sát được.
6. *Consumer applications own application operation.*
7. *Harness maintains only its core* — chỉ cài/cập nhật hướng dẫn được quản lý, không biến thành task control plane.

README củng cố #2/#3 bằng câu trực tiếp: *"The repository remains the system of record... It is not a task database, story tracker, agent orchestrator, or application runtime"*; *"A typo does not need a plan. A migration spanning sessions does"* [6]. `docs/WORKFLOW.md` cụ thể hoá #4 bằng ví dụ: *"`Add rate limiting` without a quota, trusted key, enforcement topology, or response contract must stop. `Enforce the documented 20 requests per minute per authenticated tenant` may proceed"* [7].

## 2. Cơ chế vận hành thật

Không phải "quét code rồi tự sinh AGENTS.md" — payload cài đặt **khai báo tường minh** trong `scripts/harness-install-files.txt`, gồm `AGENTS.md` gọn, `docs/WORKFLOW.md`, cấu trúc `docs/plans/active|completed`, `docs/decisions/` [8]. Có cơ chế "block" chèn vào `CLAUDE.md`/`AGENTS.md` đích thay vì ghi đè toàn bộ (`scripts/agent-harness-block.md`, `scripts/claude-harness-block.md`, cờ `--merge`/`--override`/`--dry-run`) [8]. Lệnh bảo trì thật: `harness status`, `harness doctor`, `harness update [--dry-run|--continue|--abort]` — three-way merge, backup, transactional; conflict giữ nguyên BASE/LOCAL/UPSTREAM/RESOLVED cho người dùng tự resolve [9].

Repo thật, đang hoạt động: **1198 sao, 429 fork**, MIT license, tạo 2026-05-05, push cuối 2026-08-13 [10]. Pre-1.0 (`harness-v0.1.10`) — đang biến động kiến trúc mạnh: dòng sản phẩm cũ (SQLite `harness-cli` + "protocol v1") **end-of-life chính thức ngày 2026-08-10**, xác nhận chéo qua README và CHANGELOG PR #64 [11]. Có `scripts/validate-premerge.sh` chạy fmt/test/Clippy/installer-check/release-guard/doc-check — gate CI thật, không chỉ vibe [9].

**Người dùng thật:** gần như một người vận hành (quét ~35 PR gần nhất, đại đa số tác giả `hoangnb24`). Duy nhất 1 issue từ người ngoài (`lxbachit03`, đóng 2026-07-09) với phản hồi tích cực rõ ràng — hai phát biểu riêng, cùng tác giả, cùng ngày, cách nhau ~8 giờ: mở issue lúc 07:45 UTC *"Based on my experience, this harness repo was so powerful for most projects, tasks,..."*, rồi comment lúc 15:29 UTC *"...after exploring all features, workflows, and the harness CLI; I was falling in love with this repo"* [12]. Một PR draft (chưa merge tính đến 2026-08-26) từ contributor ngoài (`paulpham157`) tự báo audit tìm 3 bug critical + 8 systemic, gồm path traversal trong `HARNESS_RUN_ID` — **chưa xác nhận độc lập**, chỉ là tự báo cáo trong PR chưa merge [ref=6, unverified] [13].

## 3. Đối chiếu với AGENTS.md của Vấn Đạo

Sáu khác biệt cụ thể được tìm thấy (chi tiết đầy đủ: `digests/doi-chieu-r1-1.md`); phần lớn là khác triết lý phù hợp quy mô, không phải lỗ hổng:

| # | Khác biệt | Đáng học? |
|---|---|---|
| 1 | `CLAUDE.md` tách riêng khỏi nội dung canonical (harness) vs khối nằm trong chính AGENTS.md (Vấn Đạo) | Chưa đủ bằng chứng — không xác nhận được Vấn Đạo có/không có CLAUDE.md riêng từ đoạn văn bản; **kiểm trực tiếp filesystem xác nhận: `van-dao/` không có CLAUDE.md**, khớp đúng tự khai của AGENTS.md |
| 2 | Vòng đời kế hoạch `docs/plans/active/`→`completed/` (harness) vs 1 status doc sống theo § (Vấn Đạo) | Không — hai triết lý khác nhau, Vấn Đạo đã có giải pháp hợp lý cho quy mô của nó |
| 3 | `.agents/skills/` phân tầng mặc-định-nạp vs explicit-only-gọi-`$lệnh` | Chưa áp dụng được — **kiểm trực tiếp: `van-dao/skills/` hiện RỖNG**, chưa tới giai đoạn implement để cần phân tầng |
| 4 | Quy trình có tên `$encode-invariant` (5 bước, tái dùng cho mọi luật mới) vs 1 cặp cụ thể `bi-kip.schema.md`§6↔`kiem-bi-kip.py` | **Có — đáng học một phần** (xem bên dưới) |
| 5 | CHANGELOG riêng cho tài liệu-agent (có PR, có lý do) vs 1 dòng "Verified {ngày}" | Thấp/trung bình — git log đã cho lịch sử thô, lợi ích thêm nhỏ cho dự án 1 agent |
| 6 | Installer/updater độc lập (cryptographic verify, 3-way merge) vs skill BMAD ghi đè marker | Không — đổi sẽ xung đột với hệ sinh thái BMAD đang dùng nhất quán toàn workspace |

**Điểm đáng học thật (#4):** Vấn Đạo đã thực hành đúng tinh thần "luật bằng lời ⇄ check tự động" ở đúng một chỗ — `bi-kip.schema.md` §6 là luật bằng lời của phép kiểm `kiem-bi-kip.py` thực thi, §7 là phần script không làm, "đổi một bên thì đổi bên kia trong cùng một thay đổi, kèm fixture và test". Đây chính là nguyên tắc `$encode-invariant` của harness, nhưng chưa được phát biểu thành quy ước CHUNG để áp dụng khi thêm luật mới ở chỗ khác. Không cần cả bộ máy 5-cổng của harness (tìm authority → xác nhận → thiết kế guard → cài kèm bằng chứng dương/âm → khảo sát enforcement có sẵn) — chỉ cần tổng quát hoá thành một dòng quy ước ngắn trong `AGENTS.md`.

## Cross-dimension insights

Kết hợp 3 chiều cho thấy một điều không chiều riêng lẻ nào thấy được: **"harness" của repo này không phải một công cụ generic áp dụng đâu cũng được — nó được thiết kế RÕ RÀNG cho bối cảnh nhiều-repo/nhiều-agent/nhiều-phiên cần một lớp cài đặt-cập-nhật độc lập (Cơ chế, mục 2)**, đúng như 7 nguyên tắc của nó tự thừa nhận ở nguyên tắc #6/#7 ("consumer applications own application operation", "harness maintains only its core" — mục 1). Vấn Đạo đã GIẢI QUYẾT đúng vấn đề đó bằng một cách khác phù hợp bối cảnh của mình hơn (BMAD skill quản lý AGENTS.md trong cùng một workspace, không cần installer riêng) — nên phần lớn khác biệt tìm được ở mục 3 là **kết quả tất yếu của bối cảnh khác nhau**, không phải Vấn Đạo thiếu sót. Điều thật sự đáng mang về không nằm ở tầng "cơ chế" (installer, changelog, thư mục plans) mà ở tầng "nguyên tắc" duy nhất — #4 — vì đó là nguyên tắc không phụ thuộc quy mô: "luật mới cần validate thì luôn đi kèm bằng chứng dương/âm và nguồn thẩm quyền" áp dụng được cho dự án 1 người lẫn dự án nhiều repo như nhau.

## Recommendations

1. **Thêm 1 dòng quy ước vào AGENTS.md** (mục "Conventions that differ from defaults" đã có): tổng quát hoá pattern `bi-kip.schema.md`↔`kiem-bi-kip.py` thành quy ước chung — "luật mới cần kiểm bằng script phải đi cặp: đoạn luật bằng lời trong tài liệu tham chiếu + test dương/test âm trong cùng một thay đổi, và luật đó bắt nguồn từ đâu (R-nào của đặc tả) phải nêu rõ". Độ tin cậy: cao — dựa trên pattern Vấn Đạo đã thực hành thật (không phải suy đoán), chỉ thiếu phát biểu tường minh.
2. **Không** áp dụng vòng đời `docs/plans/active/completed`, installer riêng, hay CHANGELOG riêng cho AGENTS.md — cả ba đều giải quyết vấn đề Vấn Đạo không có ở quy mô hiện tại, hoặc đã có giải pháp khác phù hợp hơn qua BMAD.
3. **Theo dõi, không hành động ngay:** nếu Vấn Đạo (hoặc BMAD nói chung) sau này cân nhắc một cơ chế "sinh/cập nhật AGENTS.md" tổng quát hơn cho nhiều dự án, PR #63 (audit bug chưa merge) và tình trạng pre-1.0/đổi kiến trúc mạnh của `repository-harness` là lý do để KHÔNG vội phụ thuộc trực tiếp vào công cụ này ngay bây giờ — độ tin cậy: trung bình (dựa trên 1 PR chưa merge, tự báo cáo).

## Open Questions

- Không có — 2 câu hỏi mở ban đầu (CLAUDE.md riêng? phân tầng skill?) đã đóng bằng kiểm tra filesystem trực tiếp (mục 3, bảng #1 và #3).

## Source Appendix

| # | Claim/finding | Publisher | Ngày xuất bản | Truy cập | Độ tin cậy |
|---|---|---|---|---|---|
| [1] | Vai trò AGENTS.md (entrypoint, marker 3-way) vs CLAUDE.md (shim import) | [raw AGENTS.md/CLAUDE.md, hoangnb24/repository-harness](https://raw.githubusercontent.com/hoangnb24/repository-harness/main/AGENTS.md) | 2026 (repo hiện hành) | 2026-08-26 | Cao — đọc trực tiếp file gốc |
| [2] | `.agents/skills/` — 5 skill, 3 explicit-only | [GitHub API listing `.agents/skills`](https://api.github.com/repos/hoangnb24/repository-harness/contents/.agents/skills) | 2026 | 2026-08-26 | Cao |
| [3] | `crates/` chỉ 1 crate `harness` | [raw Cargo.toml](https://raw.githubusercontent.com/hoangnb24/repository-harness/main/Cargo.toml) | 2026 | 2026-08-26 | Cao |
| [4] | Kiến trúc hexagonal, architecture test chặn dependency ngược | [raw docs/ARCHITECTURE.md](https://raw.githubusercontent.com/hoangnb24/repository-harness/main/docs/ARCHITECTURE.md) | 2026 | 2026-08-26 | Cao |
| [5] | 7 nguyên tắc thiết kế | [raw docs/HARNESS.md](https://raw.githubusercontent.com/hoangnb24/repository-harness/main/docs/HARNESS.md) | 2026 | 2026-08-26 | Cao |
| [6] | "Repository remains system of record", "typo does not need a plan" | [raw README.md](https://raw.githubusercontent.com/hoangnb24/repository-harness/main/README.md) | 2026 | 2026-08-26 | Cao |
| [7] | Ví dụ "material ambiguity → dừng" (rate limiting) | [raw docs/WORKFLOW.md](https://raw.githubusercontent.com/hoangnb24/repository-harness/main/docs/WORKFLOW.md) | 2026 | 2026-08-26 | Cao |
| [8] | Payload cài đặt khai báo tường minh, cơ chế block-merge | README.md; [GitHub API `scripts/`](https://api.github.com/repos/hoangnb24/repository-harness/contents/scripts) | 2026 | 2026-08-26 | Cao |
| [9] | Lệnh bảo trì (`status`/`doctor`/`update`), gate CI `validate-premerge.sh` | README.md, mục "Maintain An Installation"/"Development" | 2026 | 2026-08-26 | Cao |
| [10] | Metadata repo: 1198 sao, 429 fork, MIT, ngày tạo/push | [GitHub API repo metadata](https://api.github.com/repos/hoangnb24/repository-harness) | 2026-08-13 (pushed_at) | 2026-08-26 | Cao — số liệu trực tiếp từ API |
| [11] | Protocol v1/SQLite CLI end-of-life 2026-08-10 | README "Protocol V1 End Of Life"; CHANGELOG PR #64 | 2026-08-10 | 2026-08-26 | Cao — xác nhận chéo 2 nguồn |
| [12] | Testimonial người dùng thật (issue #38) — 2 phát biểu riêng cùng tác giả, cùng ngày, cách ~8h (issue body + comment), không phải 1 câu liên tục | [GitHub Issue #38 + comments](https://api.github.com/repos/hoangnb24/repository-harness/issues/38) | 2026-07-07 (issue body 07:45 UTC, comment 15:29 UTC) | 2026-08-26; spot-check độc lập 2026-08-27 | Cao — nội dung xác nhận thật qua spot-check, đã sửa cách trích cho đúng 2 nguồn tách biệt |
| [13] | PR #63 (draft) tự báo audit 3 critical + 8 systemic bug | [GitHub Issues API, PR #63 body](https://api.github.com/repos/hoangnb24/repository-harness/issues?state=open) | 2026 (chưa merge) | 2026-08-26 | **Thấp — chưa xác nhận độc lập, tự báo cáo trong PR chưa merge** |

## Staleness Map

Lớp claim dễ lỗi thời nhất: **metrics/số liệu repo (sao, fork, version, PR count)** — pack "technical" đặt cửa sổ tươi ≤1 tháng cho version/compatibility, ≤6 tháng cho tín hiệu ecosystem. Repo đang pre-1.0 và đổi kiến trúc mạnh (vừa end-of-life cả một dòng sản phẩm trong tháng 8/2026) — mọi số liệu ở đây có khả năng lỗi thời nhanh hơn mức trung bình một dự án ổn định. Claim [10]/[11]/[13] nên re-check trước tiên nếu dùng lại nghiên cứu này sau ~1 tháng; claim [1]-[9] (nguyên tắc thiết kế, kiến trúc code) bền hơn — pack đặt cửa sổ "architecture patterns" ở ≤2 năm, ít khả năng đổi trừ khi có breaking redesign khác.
