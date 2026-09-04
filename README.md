# Vấn Đạo — Workspace

Workspace tài liệu và điều phối cho plugin **`van-dao`**: biến sách PDF/EPUB người học đã có
thành lộ trình học có người kèm.

Hệ thống mượn ẩn dụ tông môn — *bái sư*, *tàng kinh các*, *công pháp*, *tâm pháp* — để đặt tên
cho các khái niệm học tập. Bảng tra từ vựng nằm ở §0 của đặc tả.

> **Repo này không chứa mã nguồn plugin.** Mã nguồn `van-dao/` nằm ở repo riêng.
> Ở đây là đặc tả, tài liệu thiết kế, và toàn bộ artifact của quy trình BMAD.

## Bắt đầu từ đâu

| Cần gì | Đọc file |
|---|---|
| Thiết kế đầy đủ | `docs/VAN-DAO-dac-ta-v1.0.md` — mở theo mục, đừng nạp cả file |
| Dự án đang ở đâu | `docs/VAN-DAO-trang-thai-du-an.md` §10 |
| Ngữ cảnh cho AI agent | `AGENTS.md` |

## Cấu trúc

```
docs/            Đặc tả, trạng thái, hướng dẫn setup
_bmad-output/    Artifact quy trình BMAD: PRD, architecture, epics, specs, research
_bmad/           Cấu hình BMAD
.claude/skills/  Skill dùng trong workspace (orca-help, work-state)
bin/             Script kiểm tra
tests/           Test suite, chạy tự động ở pre-commit
```

## Giấy phép

MIT
