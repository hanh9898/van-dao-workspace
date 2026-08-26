---
title: 'technical research: plugin ghost-writer (simonediroma/claude-ghost-writer) — học hỏi cải thiện van-dao'
type: 'technical'
topic: 'plugin ghost-writer (simonediroma/claude-ghost-writer) — học hỏi cải thiện van-dao'
decision: 'Tìm điểm thiết kế của ghost-writer (skill/persona/state/chu trình viết-phê-tích hợp) đáng mang vào cải thiện van-dao'
source: 'https://github.com/simonediroma/claude-ghost-writer'
status: complete
preset: 'standard'
validation: 'normal'
created: '2026-08-27'
updated: '2026-08-27'
claims_verified: 16
claims_unverified: 0
claims_overturned: 2
---

# technical research: plugin ghost-writer (simonediroma/claude-ghost-writer) — học hỏi cải thiện van-dao

**Decision this research serves:** Tìm điểm thiết kế của ghost-writer (skill/persona/state/chu trình viết-phê-tích hợp) đáng mang vào cải thiện van-dao.

## Tóm tắt điều hành

Ghost-writer là plugin Claude Code 27-skill của một tác giả duy nhất, thiết kế cơ chế rất chỉn chu ở 3 điểm: (1) thang leo thang 4 bước có từ vựng trạng thái tường minh khi tác giả "bí" trong phê bình, (2) một skill nâng cấp cấu trúc tường minh, có ngưỡng, cần xác nhận khi dự án lớn dần, (3) một lệnh "resume" tối giản luôn trả đúng 1 khuyến nghị. Cả ba đều đáng đối chiếu với van-dao. **Nhưng**: nhánh ecosystem xác nhận plugin này — và cả dự án gốc "quantum_fatalism" mà phương pháp dựa trên — có **0 sao, 0 fork, 0 issue/PR từ người ngoài, 0 tín hiệu cộng đồng công khai nào** [11][12][14], và việc lọt vào marketplace `anthropics/claude-plugins-community` chỉ là qua kiểm tra an toàn tự động, không phải biên tập chất lượng [15]. Kết luận: đây là các Ý TƯỞNG THIẾT KẾ được đặc tả tốt trên giấy, **chưa có bằng chứng đã qua thử lửa thực tế nào** ngoài tác giả tự dùng 1 lần. Nên học cách ĐẶC TẢ (cấu trúc quy tắc, từ vựng trạng thái), không nên học như một "pattern đã kiểm chứng". **Cập nhật sau khi đối chiếu trực tiếp với `docs/VAN-DAO-dac-ta-v1.0.md` thật** (mục Đối chiếu §2, bảng cập nhật): 0/3 ứng viên là gap thật — 2/3 (mã A, C) van-dao đã có cơ chế tương đương, kiến trúc chặt hơn ghost-writer ở một số điểm; mã B tiền đề không khớp hình dạng vấn đề của van-dao. `van-dao/skills/` và `van-dao/agents/` hiện còn rỗng (`.gitkeep`) — dự án ở giai đoạn tiền-triển khai, chỉ đặc tả đã tồn tại.

## 1. Cơ chế vận hành thật của ghost-writer

27 skill (khớp CHANGELOG), một tác giả, MIT — đúng với **bản đã pin cục bộ** (v1.0.0, 2026-05-10) [1]; GitHub HEAD thật đã tiến xa hơn nhưng bản marketplace người dùng cài chưa đồng bộ theo (chi tiết ở mục 3) [13]. Vòng đời 4 nhóm: Onboarding (1 lần) → Chu trình viết (lặp mỗi chương) → Consistency (định kỳ) → Closing (1 lần cuối), cộng lớp "macro command" gói sẵn.

Ba cơ chế được đặc tả chi tiết nhất:

- **`resume`** — "lệnh duy nhất cần nhớ": quét đúng 5 nguồn cố định, tường minh cấm đọc sâu, luôn xuất đúng 3 khối (LAST TIME/WAITING/NEXT) và đúng 1 khuyến nghị theo bảng if/else 8 nhánh — không bao giờ liệt kê menu [2].
- **`demolish`** — máy trạng thái phê bình một-lỗi-một-lúc; khi tác giả bí có chuỗi leo thang 4 bước cố định (diễn đạt lại → thu hẹp về 1 claim → hỏi trực giác → 3 lối thoát có cấu trúc: Modify/Narrow/Accept) trước khi park chính thức vào trạng thái `deferred`; không lặp lại vấn đề đã `resolved` [3].
- **`longform-upgrade`** — tự đề xuất ở ngưỡng 10 chương, hỏi xác nhận cách chia trước khi đổi, tuyên bố rõ "không đổi nội dung, chỉ đổi cách quản lý context"; sau nâng cấp chỉ 2/27 skill còn full-read, còn lại lazy-read theo phần [5].

**Phản-mẫu phát hiện được**: `integrate` (Phase 5, bước 4) âm thầm ghi đè `voice-sample.md` khi ≥3 đoạn bị viết lại, "không nói cho tác giả biết" — mâu thuẫn trực tiếp với nguyên tắc chính mà README tuyên bố ("Memory is explicit") [4].

Nghi vấn ban đầu về dữ liệu mẫu (book-memory.md, chapters/, outline.md... trông như dữ liệu thật) đã **giải quyết dứt điểm**: đọc trực tiếp xác nhận toàn bộ là template rỗng theo cú pháp placeholder ngoặc vuông (`[term]`, `[date]`, "Your Book Title"...) — scaffold trạng thái-ban-đầu mà tác giả cố ý đóng gói, không phải rò rỉ dữ liệu [6].

## 2. Đối chiếu với van-dao

*Đối chiếu trực tiếp với `docs/VAN-DAO-dac-ta-v1.0.md` (2.136 dòng) và cây thư mục `van-dao/` thật — không còn chỉ dựa vào AGENTS.md. Xác nhận: `van-dao/skills/`, `van-dao/agents/`, `van-dao/hooks/` hiện chỉ có `.gitkeep` — dự án tiền-triển khai, chưa có skill/agent nào viết thật; chỉ `bin/kiem-bi-kip.py` và `tham-chieu/bi-kip.schema.md` là mã đã tồn tại. Vì vậy đối chiếu dưới đây là với **đặc tả**, không phải với code đang chạy.*

| Mã | Mẫu ghost-writer | Đối chiếu với đặc tả van-dao thật | Kết luận |
|---|---|---|---|
| A | Thang leo thang 4 bước + trạng thái `deferred`/`accepted-limitation` khi bế tắc [3] | **Đã có, cấu trúc hơn.** Hai cơ chế riêng: (1) §7.0 — F4 chẩn đoán quan niệm sai → F5 đổi biểu diễn → F5′ báo Trưởng Môn "có thể thiếu nền", đúng 3 bước leo thang khi học sinh bí trong lúc dạy. (2) §9.4–9.5 — đúng vai chấm candidate nêu (Nghiệm Công Sứ/Phúc Khảo Sứ): `khong_ro` là trạng thái thứ ba chính thức của Phúc Khảo Sứ, có bảng quyết định 6 nhánh, và mỗi bất đồng ghi vào `bat-dong.jsonl` với **taxonomy loại** (tiêu_chí_không_phân_biệt/quá_hẹp/đề_không_ép_khẳng_định) + lý do nguyên văn + đề xuất tiêu chí thay thế — giàu hơn 2-status vocab của ghost-writer, và có đường dẫn thẳng vào cải thiện bí kíp [16] | **Không phải gap** — không cần cấy gì (đánh giá ban đầu ở [7], nay lật lại) |
| B | Skill nâng cấp cấu trúc tường minh, có ngưỡng, cần xác nhận [5][8] | **Tiền đề không khớp.** "Bậc" (§13.1) là trục thứ tự **dựng plugin** (dev-time roadmap) — vô hình với người dùng sau khi ship đủ (§15: "không gắn nhãn bậc — đã chốt làm đầy đủ"), không phải trục runtime co giãn theo nội dung. Bí kíp van-dao được **nhập toàn bộ một lần** từ PDF/EPUB có sẵn (giám định + phân giải, §6.2) — không phình dần qua nhiều tuần như sách ghost-writer, nên "ngưỡng phình cần nâng cấp" không có đối tượng tương ứng ở cấp một bí kíp [17] | **Không áp dụng** — analogy yếu hơn nhìn ban đầu; câu hỏi thật còn treo: log cấp hành trình học (`lo-trinh.jsonl`, `so-tay.jsonl`, đạo tâm) tích luỹ không giới hạn qua nhiều năm/nhiều bí kíp — spec chưa thấy cơ chế nén/tái cấu trúc cho các log này (khác §5.11 chỉ nén trong một phiên một chương) |
| C | `resume`: quét nhanh, cấm đọc sâu, luôn 1 khuyến nghị, giọng "welcome back" [2] | **Đã có, kiến trúc chặt hơn.** Đặc tả §14 xác nhận tường minh: `/vd:be-quan [bí kíp]` **không tham số** = "liệt kê bí kíp và chỗ đang dở" — đây chính là hành vi thay thế cho lệnh `/vd:tiep` từng bị cắt (§14.2). Cộng thêm `/vd:chi-duong` ý định 3 ("ta đang ở đâu") trả về Bản đồ vấn đạo (Artifact). Trạng thái **luôn suy lại từ artifact thật trên đĩa** (§5.7 — cache `ban-do.json` xoá được, dựng lại được), chặt hơn cách `resume` của ghost-writer đọc `book-memory.md` — một bảng do LLM tự tay duy trì, có nguy cơ lệch (đúng kiểu rủi ro mà bug silent-overwrite ở `integrate` minh hoạ) [18] | **Không phải gap** — đã có, nguyên tắc state-derivation còn chặt hơn ghost-writer (câu hỏi ban đầu ở [9], nay xác nhận) |
| D | Phản-mẫu: silent-overwrite mâu thuẫn tuyên bố "Memory is explicit" [4] | NFR2 append-only đã có ở van-dao (`epics.md`) [10] | Không cần hành động — dùng làm bằng chứng củng cố quy ước hiện có |

Không đáng học nguyên xi: mô hình co-authoring qua Git nhánh riêng (đối tượng khác hẳn — van-dao không có nhiều tác giả cộng tác qua git); field `language` đa dạng ở đầu mọi skill (van-dao nhắm người học tiếng Việt là chính). Giá trị biên thấp: macro-command gói skill atomic.

**Một điểm nhỏ còn đáng giữ lại** (không phải gap, chỉ là mức độ chi tiết): khi `be-quan`/`chi-duong` được viết SKILL.md thật (chưa tồn tại), có thể mượn **phong cách đặc tả chính xác** của `resume` — đúng N nguồn cố định, cấm đọc sâu, luôn đúng 1 khuyến nghị — làm tham khảo hành văn, không phải tính năng mới.

## 3. Độ trưởng thành / tín hiệu cộng đồng thật

`claude-ghost-writer`: tạo 2026-04-18, push cuối 2026-06-07 (~7 tuần rồi im lặng ~11 tuần tính tới hôm nay). **0** sao, fork, watcher, open-issue; không Release object nào; 4 "issue" thực chất là PR tự-merge bởi chính chủ repo; 16 commit chỉ 2 "tác giả" (chủ repo + bot Claude Code) [11][12]. Entry marketplace trỏ sha cũ hơn 3 commit sprint cuối — bản người dùng cài có thể lệch bản mới nhất trên GitHub [13].

Dự án gốc của phương pháp, `quantum_fatalism`: tạo và viết xong trong **1 ngày** (~9.5 giờ), có essay hoàn chỉnh thật (đã đọc trực tiếp, 45-46KB, cấu trúc rõ ràng) theo đúng chu trình mà ghost-writer quảng cáo — đây là bằng chứng sơ cấp tốt nhất rằng phương pháp từng ra được 1 sản phẩm hoàn chỉnh. Nhưng: tự-xuất bản, không qua biên tập độc lập nào xác minh được, claim "8 phiên bản" chỉ có nguồn là tự-thuật của tác giả, và cũng 0 sao/fork/issue [14].

Marketplace cộng đồng chỉ yêu cầu qua kiểm tra an toàn tự động khi nộp — không phải biên tập chất lượng thủ công (khác marketplace chính thức được tuyển chọn) [15]. Không tìm thấy review/thảo luận nào (Reddit/HN/blog) về plugin hay tác giả.

## Khuyến nghị

Ghép cơ chế (mục 1) với ecosystem (mục 3): không quy tắc nào trong đó từng được ai ngoài tác giả thử qua, kể cả tác giả cũng chỉ dùng thật đúng 1 lần (quantum_fatalism). "Có mặt trên marketplace Anthropic" chỉ là qua lọc an toàn tự động, không phải tín hiệu chất lượng. Đối chiếu trực tiếp với đặc tả thật (mục 2) xác nhận điều đó đúng theo hướng cụ thể nhất: **0/3 ứng viên là gap** — van-dao không cần copy pattern nào của ghost-writer để cải thiện.

1. **Không hành động cho mã A, B, C, D.** A và C đã có cơ chế tương đương trong đặc tả (kiến trúc chặt hơn ở một số điểm — state-derivation của C, taxonomy bất đồng của A); B tiền đề không khớp hình dạng vấn đề của van-dao; D chỉ là bằng chứng củng cố NFR2 sẵn có.
2. **Câu hỏi thật duy nhất còn treo** (từ việc kiểm B, không phải một ứng viên ghost-writer): log cấp hành trình học (`lo-trinh.jsonl`, `so-tay.jsonl`, đạo tâm) tích luỹ không giới hạn qua nhiều năm — đặc tả chưa thấy cơ chế nén/tái cấu trúc cho log này. Đáng hỏi kiến trúc sư (bmad-architecture) khi có dịp, không phải nhập từ ghost-writer.
3. **Ghi chú hành văn cho tương lai** (không phải hành động bây giờ): khi viết `be-quan`/`chi-duong` SKILL.md thật, độ chính xác đặc tả của `resume` (N nguồn cố định, cấm đọc sâu, luôn 1 khuyến nghị) là tham khảo hành văn tốt — van-dao/skills/ hiện còn rỗng nên chưa tới lúc.

## Câu hỏi còn mở

- Log cấp hành trình học (`lo-trinh.jsonl`, `so-tay.jsonl`, đạo tâm) tích luỹ không giới hạn qua nhiều năm/nhiều bí kíp — đặc tả chưa thấy cơ chế nén/tái cấu trúc. Câu hỏi thật của van-dao, phát hiện phụ khi kiểm mã B — không phải câu hỏi về ghost-writer.
- `ships_log.md`/`diario_di_bordo.md` của quantum_fatalism chưa đọc sâu — nơi duy nhất có thể xác minh độc lập claim "8 phiên bản".
- Có người dùng thật nào cài ghost-writer qua marketplace không — không có kênh đo lượt cài công khai, nên "0 tín hiệu GitHub" không đồng nghĩa "0 người dùng".

## Nguồn

| # | Claim/phát hiện | Nguồn | Ngày | Truy cập | Độ tin cậy |
|---|---|---|---|---|---|
| 1 | 27 skill, 1 tác giả, MIT, v1.0.0 một lần | [plugin.json / CHANGELOG.md](https://github.com/simonediroma/claude-ghost-writer) (đọc cục bộ, bản clone git thật) | 2026-05-10 | 2026-08-27 | Cao (sơ cấp) |
| 2 | Cơ chế `resume` | [skills/resume/SKILL.md](https://github.com/simonediroma/claude-ghost-writer/blob/main/skills/resume/SKILL.md) | 2026-05 | 2026-08-27 | Cao (sơ cấp) |
| 3 | Cơ chế `demolish` + thang leo thang | [skills/demolish/SKILL.md](https://github.com/simonediroma/claude-ghost-writer/blob/main/skills/demolish/SKILL.md) | 2026-05 | 2026-08-27 | Cao (sơ cấp) |
| 4 | `integrate` silent-overwrite + nguyên tắc "Memory is explicit" (README § Core Principles) bị mâu thuẫn | [skills/integrate/SKILL.md](https://github.com/simonediroma/claude-ghost-writer/blob/main/skills/integrate/SKILL.md) | 2026-05 | 2026-08-27 | Cao (sơ cấp, đã đối chiếu cả `integrate/SKILL.md` lẫn `README.md`) |
| 5 | Cơ chế `longform-upgrade` | [skills/longform-upgrade/SKILL.md](https://github.com/simonediroma/claude-ghost-writer/blob/main/skills/longform-upgrade/SKILL.md) | 2026-05 | 2026-08-27 | Cao (sơ cấp) |
| 6 | Template rỗng, không rò rỉ dữ liệu | book.config.json / book-memory.md / outline.md (đọc cục bộ) | 2026-05 | 2026-08-27 | Cao (sơ cấp) |
| 7 | Đối chiếu ban đầu (mã A "đáng học nhất") — **bị lật lại bởi [16]** sau khi đọc đặc tả thật | Tổng hợp bởi người điều phối từ [3] + `AGENTS.md` van-dao (bản tóm tắt, chưa đủ) | 2026-08-27 | 2026-08-27 | Overturned — xem [16] |
| 8 | Đối chiếu ban đầu (mã B "đáng cân nhắc") — **bị lật lại bởi [17]**, tiền đề không khớp | Tổng hợp bởi người điều phối từ [5] + `AGENTS.md` van-dao (bản tóm tắt, chưa đủ) | 2026-08-27 | 2026-08-27 | Overturned — xem [17] |
| 9 | Đối chiếu: van-dao đã có skill resume-cho-đệ tử — xác nhận bởi [18] | Tổng hợp bởi người điều phối từ [2] + `AGENTS.md` van-dao | 2026-08-27 | 2026-08-27 | Cao (verified — xem [18]) |
| 10 | Đối chiếu: phản-mẫu silent-overwrite củng cố NFR append-only | Tổng hợp bởi người điều phối từ [4] + **NFR2** (`epics.md`, mục NonFunctional Requirements) | 2026-08-27 | 2026-08-27 | Cao (verified) |
| 11 | 0 sao/fork/issue thật; PR tự-merge | [api.github.com/repos/simonediroma/claude-ghost-writer](https://github.com/simonediroma/claude-ghost-writer) | 2026-08-27 (live) | 2026-08-27 | Cao (sơ cấp) |
| 12 | 16 commit, 2 tác giả, cửa sổ hoạt động | GitHub API `/commits` | 2026-08-27 (live) | 2026-08-27 | Cao (sơ cấp) |
| 13 | Marketplace sha lệch bản mới nhất | [marketplace.json](https://github.com/anthropics/claude-plugins-community/blob/main/.claude-plugin/marketplace.json) | 2026-08-27 (live) | 2026-08-27 | Cao (sơ cấp) |
| 14 | `quantum_fatalism` — essay hoàn chỉnh, tự-xuất bản, 0 tín hiệu | [github.com/simonediroma/quantum_fatalism](https://github.com/simonediroma/quantum_fatalism) | 2026-04-16 | 2026-08-27 | Cao (tồn tại) / Trung bình (claim "8 phiên bản") |
| 15 | Marketplace community = chỉ automated screening | [code.claude.com/docs/en/discover-plugins](https://code.claude.com/docs/en/discover-plugins) | — | 2026-08-27 | Cao (sơ cấp) |
| 16 | Mã A không phải gap — §7.0 (F4→F5→F5′) + §9.4–9.5 (`khong_ro`, taxonomy bất đồng) đã giải quyết | `docs/VAN-DAO-dac-ta-v1.0.md` §7.0, §9.4, §9.5 (đọc trực tiếp) | 2026-08-27 | 2026-08-27 | Cao (sơ cấp, đọc trực tiếp đặc tả) |
| 17 | Mã B tiền đề không khớp — "Bậc" là dev-roadmap, bí kíp nhập toàn bộ một lần | `docs/VAN-DAO-dac-ta-v1.0.md` §13.1, §15, §6.2 (đọc trực tiếp) | 2026-08-27 | 2026-08-27 | Cao (sơ cấp, đọc trực tiếp đặc tả) |
| 18 | Mã C đã có — `/vd:be-quan` không tham số, `/vd:chi-duong` ý định 3, state luôn suy từ artifact | `docs/VAN-DAO-dac-ta-v1.0.md` §5.7, §14, §14.1, §14.2 (đọc trực tiếp) | 2026-08-27 | 2026-08-27 | Cao (sơ cấp, đọc trực tiếp đặc tả) |

## Bản đồ độ cũ (staleness)

16/18 claim verified, 2/18 overturned (mã A, B — đã lật lại bằng bằng chứng mới [16][17], xem bảng Nguồn), 0 unverified. Không claim nào đã stale tại thời điểm viết. Mốc tái kiểm sớm nhất: **2027-02-01** (nhóm `community`/`provenance`/`metadata` — cửa sổ 6 tháng, vì đây là số liệu GitHub sống, có thể đổi: sao/fork/issue tăng, marketplace đồng bộ lại). Nhóm `comparison` tái kiểm 2027-08-01 (12 tháng — phụ thuộc cả hai dự án tiến hoá, kể cả [16][17][18] vì đặc tả van-dao còn có thể đổi trước khi build). Nhóm `mechanism`/`data-provenance` tái kiểm 2028-05-01 (24 tháng — chỉ đổi nếu ghost-writer ra bản mới, hiện chưa có dấu hiệu sẽ ra).
