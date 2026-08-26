# Digest — Kiến trúc & tư duy thiết kế (round 1)

## Q1 — `.agents/`, `AGENTS.md`, `CLAUDE.md`: vai trò khác nhau

**`AGENTS.md`** (gốc, 1613 bytes) — là payload nội dung thật, bọc trong marker `<!-- HARNESS:BEGIN -->...END -->` (cho phép updater merge 3-way). Là "entry map và authority boundary" — quy định: đọc `docs/WORKFLOW.md`, coi answer/review/diagnosis là read-only, chỉ dùng `docs/plans/active/` khi việc trải nhiều phiên, dừng lại trước khi sửa nếu chính sách sản phẩm chưa rõ, "Claim completion only with executable or observable evidence."
Nguồn: https://raw.githubusercontent.com/hoangnb24/repository-harness/main/AGENTS.md (truy cập 2026-08-26)

**`CLAUDE.md`** (gốc, 258 bytes) — CHỈ là shim import, không chứa nội dung riêng:
> "Claude Code does not auto-load `AGENTS.md`. Import that single canonical project instruction source. Keep this bare `@` line outside backticks so the import remains active.
> @AGENTS.md"

Tồn tại thuần vì lý do kỹ thuật (Claude Code không tự đọc `AGENTS.md`) — một nguồn sự thật duy nhất (`AGENTS.md`), file agent-specific khác chỉ trỏ vào nó.
Nguồn: https://raw.githubusercontent.com/hoangnb24/repository-harness/main/CLAUDE.md

**`.agents/`** — chỉ có 1 thư mục con `skills/`, gồm 5 skill: `audit-onboarding-proposal`, `encode-invariant`, `engineering-wisdom`, `improve-harness`, `onboard-repository`. Skill triggers dạng slash-command (`$encode-invariant`...) — tách biệt `AGENTS.md` (luôn load) vs skill (opt-in, chỉ chạy khi gọi tường minh): "No skill runs during installation. Onboarding and Harness improvement remain explicit-only."
Nguồn: GitHub API `.agents` và `.agents/skills` listing (2026-08-26). *Chưa đọc nội dung SKILL.md từng skill — lead.*

## Q2 — `crates/` Rust workspace

Root `Cargo.toml`: `[workspace] resolver = "3" members = ["crates/harness"]` — chỉ 1 crate: `crates/harness` (package `harness`, v0.1.10).
Nguồn: raw Cargo.toml (gốc + crates/harness).

Một binary Rust ("repository-harness has one Rust binary, `harness`, plus thin Bash and PowerShell bootstraps" — docs/ARCHITECTURE.md), hexagonal/clean-architecture:
> "domain <- application <- infrastructure / <- interface / main.rs composes interface and infrastructure"
- domain: paths, hashes, provenance, merge outcomes, reports (không phụ thuộc filesystem/CLI)
- application: use case — install, update, status, doctor, self-update, version, conflict, recovery
- infrastructure: embedded release content, hashing, locks, filesystem transaction, Git 3-way merge, download, checksum, executable replacement
- interface: parse command, render report
- "Architecture tests reject outward dependencies from inner layers." (kiểm bằng test, không chỉ quy ước)
Nguồn: https://raw.githubusercontent.com/hoangnb24/repository-harness/main/docs/ARCHITECTURE.md

## Q3 — Nguyên tắc thiết kế (trích nguyên văn, docs/HARNESS.md, "Principles")

> 1. Repository truth wins. Product documents, decisions, plans, code, tests, CI, runtime evidence, and Git history are authoritative.
> 2. Load the smallest useful context. `AGENTS.md` is an entrypoint, not an encyclopedia.
> 3. Process follows work shape. Bounded work stays bounded; coordinated or recoverable work gets one durable plan.
> 4. Material choices stay human-owned. Missing product policy stops mutation.
> 5. Behavior proves completion. Workflow records and self-reports do not replace executable or observable evidence.
> 6. Consumer applications own application operation.
> 7. Harness maintains only its core. `harness` safely installs and updates managed guidance without becoming a task control plane.

Nguồn: https://raw.githubusercontent.com/hoangnb24/repository-harness/main/docs/HARNESS.md

README củng cố #2/#3:
> "The repository remains the system of record... It is not a task database, story tracker, agent orchestrator, or application runtime."
> "A typo does not need a plan. A migration spanning sessions does."
Nguồn: README.md

`docs/WORKFLOW.md` cụ thể hoá nguyên tắc #4:
> "`Add rate limiting` without a quota, trusted key, enforcement topology, or response contract must stop. `Enforce the documented 20 requests per minute per authenticated tenant` may proceed."
"Completion Standard": "A change is complete when the outcome exists or its blocker is explicit, repository truth remains current, behavior-appropriate proof passed or its gap is disclosed... Descriptions do not replace observed proof."
Nguồn: docs/WORKFLOW.md

## Lead chưa theo
- Nội dung từng SKILL.md trong `.agents/skills/*` (5 thư mục).
- `docs/patterns/encoding-invariants.md` — "complete method" cho invariant encoding (dẫn chiếu từ WORKFLOW.md).
- `docs/decisions/0027-end-protocol-v1-and-focus-repository-protocol.md` — quyết định khai tử SQLite `harness-cli` (protocol v1).
- `docs/README.md` (map file), `docs/product/`, `docs/research/`, `docs/demo/`.
- `scripts/harness-install-files.txt` — danh sách payload cài đặt.

## Không tìm thấy
- Không có blog tác giả/bài viết ngoài repo (không dùng WebSearch, ưu tiên đọc file trực tiếp).
- Chưa xác nhận nội dung chi tiết từng skill.
