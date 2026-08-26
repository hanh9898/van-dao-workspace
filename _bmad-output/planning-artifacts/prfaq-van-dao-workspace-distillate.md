---
title: "PRFAQ Distillate: van-dao-workspace"
type: llm-distillate
source: "prfaq-van-dao-workspace.md"
created: "2026-08-24"
purpose: "Token-efficient context for downstream PRD creation"
---

## Sản phẩm là gì

- Vấn Đạo: **plugin** Claude Code (không phải một skill đơn — bundle nhiều skill/agent/hook/lệnh `/vd:*`, xem `van-dao/.claude-plugin/`) biến sách kỹ thuật PDF/EPUB người dùng đã có sẵn thành lộ trình học có AI đồng hành, dạy kiểu Socratic bám đúng một cuốn sách, không giảng cả cuốn, đòi vận dụng thật (không chỉ nhớ) mới tính là đã nắm. Sửa thuật ngữ ngày 24/8: bản trước của distillate này gọi nhầm là "skill" — lỗi phát sinh trong lúc làm PRFAQ, `dac-ta-v1.0.md` dòng 4 luôn đúng là "Plugin".
- Concept type: open-source, cài đặt cá nhân riêng lẻ, không cộng tác/multiplayer, không SaaS multi-tenant, không unit economics — đánh giá theo adoption path và giá trị per-user.

## Persona đã chốt

- Một người: dev đang chuyển hướng làm BA. Hai nhu cầu nối tiếp trên cùng một người (không phải hai persona): (1) nắm ý cơ bản nhanh, (2) đào sâu/áp dụng thật vào công việc mới. Áp lực đổi nghề, sai lầm lộ ra khi đã vào việc mới thì đắt.
- Persona do người tạo tự suy luận, CHƯA được một người thật xác nhận. Đây là unknown lớn nhất về nhu cầu.

## Requirements signal — thay đổi phát sinh từ PRFAQ, chưa vào đặc tả

- **Cần thêm pha Supportive Information** (giải thích/tóm lược khái niệm) TRƯỚC pha Socratic — hiện F-flow (F-1→F9) không có bước này, đi thẳng vào Socratic từ F0. Khung nền: 4C/ID (van Merriënboer), thành phần thứ 2/4, đã verify qua 4cid.org. Lượng Supportive Information nên co giãn theo cảnh giới người học (nhiều lúc mới, giảm khi lên cao) — khớp luật sẵn có "giàn giáo dày lên giữa chừng" (§7.1 luật 3 đặc tả). **Chưa thiết kế — việc cần làm trước khi đưa vào đặc tả, không phải trong 34 requirement hiện có.**
- Ban đầu định vị "không tóm tắt, không giảng — chỉ hỏi" bị chính persona bác bỏ (rủi ro làm người học bỏ chạy). Đã sửa hướng: giải thích đủ rồi mới hỏi sâu.

## Chưa giải quyết — cần quyết định kiến trúc riêng, không phải PRFAQ

- **Model-agnostic vs Claude-Code-only.** Người dùng muốn "cắm vào đâu cũng được" (đa nền tảng/đa hãng AI), nhưng kiến trúc hiện tại (subagent tươi không fork — R9, hook SessionStart/SubagentStop, `.pham-vi.json`) phụ thuộc sâu vào cơ chế riêng Claude Code — đa nền tảng đòi dựng lại tầng điều phối, không phải đổi config. Customer FAQ trả lời "giữ cửa mở, đang cân nhắc" (KHÔNG theo đề xuất ban đầu của coach là "thẳng, có chủ đích, không hứa") — tín hiệu người dùng nghiêng về đa nền tảng thật. **Đây là crack chưa vá, cần quyết định trước khi commit thêm.**
- Ví dụ đã sai rồi tự sửa: coach từng khẳng định sai rằng `book-to-skill`/BMAD khoá 1 hãng — thực tế cả hai đa nền tảng (book-to-skill: Copilot CLI/Amp/Claude Code; BMAD: hàng chục host). Không dùng lại ví dụ này để biện minh cho việc khoá Claude Code.

## Kỹ thuật / phụ thuộc

- `book-to-skill` (virgiliojr94) là dependency thật, đã cài và verify chạy được — 2 lớp: pip engine (`book_to_skill.extract_single_file()`, dùng trong `giam-dinh.py`) + skill hội thoại (`npx skills add virgiliojr94/book-to-skill`, dùng ở Pha 1 chế độ "Analyze Only" — kích hoạt bằng câu trong hội thoại, KHÔNG phải cờ CLI `--analyze-only`). MIT license, rủi ro thấp nếu ngừng bảo trì (fork được), chưa pin version.
- Hai giả định nền chưa kiểm (rủi ro cao nhất, không đổi suốt PRFAQ): (1) model chấm đúng bài vận dụng theo rubric, (2) model đọc đúng cảnh giới từ văn bản người học. Sai một trong hai → dựng lại từ §1 đặc tả. Chỉ kiểm được bằng chạy thật (bước 8), không kiểm trước được.
- Nền kỹ thuật (Ưu tiên 1, §6 trang-thai-du-an) đã xong: `kiem-bi-kip.py` trong repo, 9/9 test pass, CI chạy 2 OS. Còn thiếu: push remote (chưa chọn nơi lưu).

## Cạnh tranh (đã research, thời điểm 8/2026)

- Baseline thị trường thật là **NotebookLM** (Google, miễn phí, đại chúng) — có Quizzes/Flashcards/Learning Guide bám nguồn tải lên (9/2025), không phải các skill Claude Code nhỏ lẻ.
- `book-to-skill` xác nhận qua đọc README thật: hệ tra cứu thuần, không quiz/Socratic/đo năng lực — khác biệt Vấn Đạo tuyên bố với riêng nó là thật.
- `claude-tutor`, `AI-learning-skill` gần nhất về chức năng nhưng tổng quát theo chủ đề, không khoá 1 cuốn sách.
- `Book2Course V2` (web app, không phải Claude Code skill) — đối thủ ý tưởng gần nhất, ra mắt thật, phản hồi HN: "template-like", "quiz hời hợt", "thiếu chiều sâu" — bằng chứng bài toán này khó làm tốt.
- Khoảng trống thời cơ: chưa ai gộp (a) chỉ 1 sách + (b) từ chối tóm tắt/giảng + (c) Dreyfus 5 bậc tường minh cùng lúc — nhưng khoảng trống **hẹp**, không rộng.
- Rủi ro tự nêu bởi research: chưa có bằng chứng nhu cầu thật cho tự-đánh-giá Dreyfus ở dev tự học — "risk of being a solution in search of a problem". Hiệu quả Socratic AI tutoring vẫn là câu hỏi học thuật chưa ngã ngũ.

## Scope — trong/ngoài cho tới bước 8 (giá trị đầu tiên)

- **Trong (cần):** Bậc 1 toàn bộ, bao gồm `phuc-khao` (giam-dinh.py, thu-bi-kip, thu-linh, nghiem-cong, phuc-khao, nhap-mon, dao-tam, tang-kinh-cac.py, `.pham-vi.json` + kiem-thu.py bản đầu ở bước 5b). Không cần Bậc 2.
- **`phuc-khao` (#20b/#11d) — SỬA LẠI, khác bản trước của distillate này:** từng bị đặc tả gắn nhầm mác "Bậc 3" (§13.1), đã sửa dời sang Bậc 1. Nó cần cho lời hứa "cờ bất đồng" ở Customer FAQ — không có nó thì không có gì để so sánh khi có bất đồng. §16 (thứ tự dựng thật) vốn đã đặt nó ở Vòng 2, chưa bao giờ thật sự ở Vòng 4 — lỗi chỉ nằm ở nhãn Bậc trong §13.1, không phải ở build order.
- **Ngoài (chưa cần, có lý do kỹ thuật thật, không phải cắt tuỳ tiện):** `truong-lao`/κ-calibration/`thoai-canh.py`/`canh-gioi.md` (định vị cảnh giới Dreyfus) — R10 đòi ≥2 nguồn (bài nộp từ ≥2 quyển cùng mạch), không dựng có ý nghĩa được với một quyển. Toàn bộ Bậc 2 (`ha-son`, `phuc-menh`, đạo tâm, `mach.schema.md`, `tra-tang-kinh-cac`, `ban-do.py`) — cơ chế đa quyển/đa mạch, chưa cần khi mới có một quyển.
- R11 tự nhiên giữ trưởng lão im lặng về bậc cho tới đủ mẫu — không cần cấm gì thêm bằng lời cho phần cảnh giới.
- Pha Supportive Information mới (xem trên) — chưa scope hoá, cần thiết kế trước khi đưa vào build order.

## Timeline / resource — không ước lượng số, chỉ chuỗi phụ thuộc

- Không nêu số ngày/tuần (luật tự đặt ở AGENTS.md: không ước lượng thời gian).
- Chuỗi: bước 3 (giam-dinh.py + thu-bi-kip) → bước 4 (thu 1 quyển thật) → bước 5+5b (thu-linh + kiem-thu.py bản đầu) → bước 6 (nghiem-cong) → bước 7 (nhap-mon/dao-tam song song) → bước 8 (tự bế quan — giá trị thật đầu tiên).
- Bảo trì: không hứa SLA, best-effort, mã nguồn mở cá nhân.
- Phân phối/người dùng đầu: chưa có kế hoạch — thành thật, chưa nghĩ tới.

## The Verdict — findings hành động được

**Forged in steel** (giữ nguyên, không cần sửa):
- Khác biệt với NotebookLM/book-to-skill là thật, verify được, không phải marketing.
- Trả lời dữ liệu/quyền riêng tư có cơ sở kiến trúc thật.
- Xử lý câu hỏi bằng chứng Dreyfus biến điểm yếu thành kỷ luật đáng tin (nối R11 có sẵn).

**Needs more heat** (việc cần làm trước PRD):
1. Thiết kế thật pha Supportive Information — vị trí trong F-flow, quy tắc co giãn theo cảnh giới.
2. Kế hoạch tối thiểu cho người dùng đầu tiên/bảo trì, nếu thật sự mở cho người khác như đã chốt.
3. Kiểm persona với ít nhất một người thật ngoài tác giả trước khi coi là đã xác nhận.

**Cracks in the foundation** (phải quyết định trước khi commit thêm):
1. **Model-agnostic vs Claude-Code-only** — chưa chốt, mâu thuẫn giữa Customer FAQ ("giữ cửa mở") và kiến trúc thật. Quyết định kiến trúc lớn, cần bàn riêng.
2. Hai giả định nền chưa kiểm — chỉ kiểm được ở bước 8, rủi ro cao nhất không đổi suốt quá trình.
3. Chưa có người thật (không phải tác giả) đọc thông cáo và phản ứng — toàn bộ Customer FAQ là tự vấn tự đáp.

**Khuyến nghị cuối:** Đi bước 3 — đủ cứng để bắt đầu. Song song, đừng đợi tới bước 8 mới cho một người thật đọc thông cáo và hỏi phản ứng — càng sớm càng rẻ.

## Review lens `naive-reader` (sau Verdict) — findings hành động được

- Lens tự tạo, không có sẵn trong bmad-review (không lens shipped nào kiểm "đọc lần đầu, chưa biết gì"). Chạy bằng subagent hoàn toàn mới, chỉ đọc đúng file PRFAQ, không đọc gì khác — để mô phỏng đúng độc giả lần đầu, không kế thừa ngữ cảnh người viết.
- 9 finding mechanical đã sửa trực tiếp trong PRFAQ: giải thích Claude Code/skill lần đầu nhắc, dịch epigraph Feynman, gỡ mâu thuẫn "không gửi đi đâu" vs "qua API Claude", sửa "tài khoản riêng" mơ hồ, gỡ jargon subagent/hook khỏi câu khách hàng, chú thích BABOK, làm rõ "20 mẫu".
- **Quyết định ngôn ngữ:** toàn bộ "người dạy"/"người chấm" trong Press Release + Customer FAQ đổi thành "AI"/"AI agent" — chọn trung thực tuyệt đối, không giữ giọng ấm áp mơ hồ dễ gây hiểu lầm có nhân sự con người tham gia.
- **Phát hiện lớn nhất, dẫn tới sửa đặc tả thật:** câu hỏi Dreyfus xuất hiện ở FAQ mà Press Release chưa từng giới thiệu → dẫn tới soát lại Bậc 1/2/3 có còn hợp lý cho phạm vi bước 8 → phát hiện `phuc-khao` bị gắn nhầm mác Bậc 3 trong §13.1 trong khi §16 đã đặt nó ở Vòng 2 từ trước (đúng lỗi lens `adversarial` từng nêu ở lần review kiến trúc trước đó, lúc đó bỏ qua vì ngoài phạm vi lúc ấy). Đã sửa thật trong `docs/VAN-DAO-dac-ta-v1.0.md` §13.1 — xem mục Scope ở trên.
