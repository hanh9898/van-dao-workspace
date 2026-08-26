# Digest — Cơ chế vận hành thật (round 1)

*Ngày truy cập mọi nguồn: 2026-08-26 (GitHub API + raw.githubusercontent.com trực tiếp).*

## 1. Cơ chế vận hành thật

- Rust binary (`harness`), không phải script sinh file đơn giản. Cài qua `curl ... install-harness.sh | bash -s -- --yes` (hoặc PowerShell) — bootstrap tải binary đã versioned + checksum, verify release identity trước khi cài. Nguồn: README "Install"/"What Gets Installed".
- Payload KHÔNG phải "sinh AGENTS.md từ quét code" — cài bộ cố định: `AGENTS.md` gọn, `docs/WORKFLOW.md` + bản đồ tài liệu, `docs/plans/active|completed`, `docs/decisions/`, skill tuỳ chọn. Payload khai báo tường minh trong `scripts/harness-install-files.txt`. Nguồn: README; GitHub API `scripts/` listing.
- Cơ chế "block" chèn vào `CLAUDE.md`/`AGENTS.md` đích, không ghi đè toàn bộ — `scripts/agent-harness-block.md` (1591B), `scripts/claude-harness-block.md` (241B) tồn tại riêng, cờ `--merge`/`--override`/`--dry-run`. Nguồn: API scripts/; README.
- Lệnh bảo trì thật: `harness status`, `harness doctor`, `harness update [--dry-run|--continue|--abort]` — three-way merge, backup, transactional; conflict giữ BASE/LOCAL/UPSTREAM/RESOLVED cho người dùng tự resolve. Nguồn: README "Maintain An Installation".
- Dòng sản phẩm cũ (SQLite `harness-cli` + protocol v1) **end-of-life 2026-08-10**, release cuối `harness-cli-v0.1.22`; hướng hiện tại chỉ còn "repository protocol" + installer/updater. Nguồn: README "Protocol V1 End Of Life"; CHANGELOG PR #64 (2026-08-10).

## 2. Độ trưởng thành thật

- Metadata (API trực tiếp): **1198 sao**, **429 fork**, watchers 1198, subscribers 12, open_issues=1, ngôn ngữ chính Rust, license MIT, created 2026-05-05, pushed 2026-08-13.
- CHANGELOG.md thật (35,728 bytes), theo PR merge — PR gần nhất #66 (2026-08-13). Từ repo tạo (05-05) tới 08-13 đã ≥66 PR — nhịp merge dày, nhiều PR/ngày.
- Version nội bộ `harness-v0.1.5`…`v0.1.10` (chưa 1.0) — dự án **pre-1.0, đang biến động kiến trúc mạnh** (đổi cả protocol nền giữa chừng).
- Test suite thật: `tests/` có 5 thư mục con (docs/installer/maintenance/release/workflow) + Rust unit test (`crates/harness/tests/release_update.rs`). PR #63 tự báo "101 passed" — CHƯA verify độc lập (chỉ mô tả PR, chưa merge).
- `scripts/validate-premerge.sh` chạy fmt/test/Clippy/installer-check/release-guard/doc-check/shell-syntax/git-diff-check — gate CI thật.

## 3. Người dùng thật nói gì

- Gần như dự án một người vận hành: quét ~35 PR gần nhất (#34-66), tuyệt đại đa số `user.login=hoangnb24` (chính chủ).
- **Duy nhất 1 issue thật từ người ngoài**: #38, "[question]: Should we add karpathy-guidelines skill?", mở bởi `lxbachit03` (NONE), đóng 2026-07-09. Phản hồi tích cực: "this harness repo was so powerful... I was falling in love with this repo" (2026-07-07). Chủ repo trả lời kỹ thuật chi tiết.
- `open_issues_count=1` = PR #63 (draft, chưa merge): "fix: 17 bug audit (3 critical + 4 medium + 8 systemic)", từ contributor ngoài `paulpham157` (fork riêng). Tự báo sửa: exit code sai, git merge-file exit range, regex classifier thiếu extension (critical); path traversal trong `HARNESS_RUN_ID`, race condition, non-atomic schema init (systemic). **Chưa merge tính đến 2026-08-26** — lead đáng theo.
- Không tìm thấy complaint nào (repo hỏng, cài lỗi, agent hành xử sai) trong PR/issue #34 trở lên — CHƯA quét được trước #34 (hết ngân sách).
- Không WebSearch review ngoài GitHub — hết ngân sách trước bước đó.

## Lead cho người điều phối

3 điều Vấn Đạo có thể soi lại: (1) payload cài đặt khai báo tường minh 1 file danh sách, không để agent tự quyết sinh gì; (2) AGENTS.md ở đây là "compact entrypoint" trỏ sang docs/WORKFLOW.md, không nhồi nội dung — README tự làm rõ "đọc-only" / "bounded change" / "multi-session change" / "material ambiguity → dừng"; (3) updater ba chiều bảo toàn local edit thay vì overwrite.

## Không xác nhận được
- Không kiểm `/releases` API (hết ngân sách) — CHANGELOG tự ghi "publication requires platform proof", các version có thể chưa thực publish.
- Không xác nhận số contributor thật ngoài 3 người đã thấy (chưa gọi `/contributors`).
- Không có review/bài viết ngoài GitHub được kiểm.
- Chưa đọc trực tiếp nội dung đầy đủ AGENTS.md/CLAUDE.md mẫu của chính repo này qua raw (chỉ biết size/tên qua contents API).
