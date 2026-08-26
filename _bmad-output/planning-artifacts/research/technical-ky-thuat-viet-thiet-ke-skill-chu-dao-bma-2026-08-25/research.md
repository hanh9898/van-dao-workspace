---
title: 'technical research: Kỹ thuật viết, thiết kế skill chủ đạo của BMAD-METHOD'
type: 'technical'
topic: 'Kỹ thuật viết/thiết kế skill chủ đạo của BMAD-METHOD, rút từ chính mã nguồn skill đang chạy trong workspace này'
decision: 'Cách viết SKILL.md/agents/hooks/customize.toml của Vấn Đạo — feed vào bmad-spec, epics/stories, và bmad-build'
source: 'Native run — đọc trực tiếp mã nguồn cục bộ (7 skill BMAD đại diện), không web fan-out'
status: complete
preset: 'standard'
validation: 'normal'
claims_verified: 7
claims_unverified: 0
created: '2026-08-25'
updated: '2026-08-25'
---

# technical research: Kỹ thuật viết, thiết kế skill chủ đạo của BMAD-METHOD

**Decision this research serves:** Vấn Đạo sắp viết SKILL.md/agents/hooks/customize.toml thật cho 8 vai của mình. Thay vì phát minh khuôn mẫu riêng, nghiên cứu này đọc trực tiếp mã nguồn của 7 skill BMAD-METHOD tiêu biểu — nhiều skill trong số đó đã được chính dự án này dùng để tạo ra PRD và architecture spine của Vấn Đạo — để rút ra kỹ thuật thiết kế đã được chứng minh là hiệu quả, có thể tái dùng.

## 1. Tóm tắt điều hành

BMAD-METHOD không có một khuôn SKILL.md cứng nhắc — độ dài dao động 50-136 dòng, tên section khác nhau giữa các skill (`## On Activation` vs `## Execution`; `## Conventions` vs `## Resolution rules`) [1][2][3][4][5][6]. Nhưng **năm kỹ thuật lặp lại nhất quán, có chủ đích**, đáng tái dùng cho Vấn Đạo:

1. **Bước 1 của activation luôn giống hệt nhau**: gọi `resolve_customization.py --skill {skill-root} --key workflow`, fallback đọc thẳng `customize.toml` nếu lỗi — xuất hiện gần nguyên văn ở 5/5 skill đọc được [1][2][3][5][4].
2. **"Extract, don't ingest"**: subagent ghi đầy đủ ra file, chỉ trả về tóm tắt gọn (verdict/2-5 finding/đường dẫn) — parent không bao giờ giữ full text; nguyên tắc này lặp lại xuyên nhiều skill dưới nhiều tên khác nhau (research firewall, extract-don't-ingest, lens isolation) [3][8][1][9].
3. **Memlog là bộ nhớ quá trình append-only, KHÔNG phải deliverable** — atomic write (temp→fsync→rename), không có lệnh sửa/xoá, không có field "status" (trạng thái là một event, không phải cờ) [10]. Nhưng đây **không phải cơ chế phổ quát**: bmad-prfaq dùng hẳn một cơ chế khác (frontmatter `stage` + comment nhúng trong tài liệu) [6][10].
4. **Reviewer Gate** (rubric walker + reviewer cấu hình, dispatch song song, trình bày tiered "verdict một câu rồi critical+high, medium/low gộp đuôi") chỉ có ở bmad-prd và bmad-architecture — bmad-deep-recon dùng cơ chế khác hẳn: "Plan Gate" (một hard-stop duy nhất trước khi chạy) [2][9][1][8].
5. **"One test decides what belongs"** — nén một quy tắc phức tạp thành một câu hỏi có/không thay vì liệt kê hết trường hợp — chỉ đúng nghĩa đen ở bmad-architecture, nhưng biến thể của mẫu hình này xuất hiện ở 4/5 skill khác dưới hình dạng riêng [2][1][4][3].

**Cảnh báo quan trọng nhất xuyên suốt báo cáo này**: BMAD-METHOD **không đồng nhất** — mọi khái quát hoá "BMAD luôn làm X" đã bị kiểm tra chéo và phần lớn **sai** khi soi vào bmad-review, bmad-prfaq, hoặc bmad-brainstorming. Đọc kỹ nhãn "chỉ thấy ở n/5" ở mỗi phát hiện dưới đây trước khi copy sang Vấn Đạo.

## 2. Theo từng chiều

### 2.1 Cấu trúc & giao thức skill

Mọi SKILL.md mở đầu bằng frontmatter YAML tối giản (chỉ `name`/`description`) rồi một H1 [1][2][3][4][5]. Ngay sau đó là một section khai quy ước path — tên heading không thống nhất (`## Conventions` ở bmad-prd/bmad-review/bmad-brainstorming; `## Resolution rules` ở bmad-architecture/bmad-deep-recon) nhưng nội dung tương đương: `{skill-root}` = thư mục cài skill (nơi `customize.toml` sống), `{project-root}` = thư mục làm việc dự án, `{workflow.<name>}` = field đã merge từ `customize.toml` [1][2][3][4][5]. Chỉ 2/5 file khai thêm cảnh báo chống double-prefix ("Config variables already contain `{project-root}`... never double-prefix") — đừng khái quát hoá đây là luật chung [2][3].

`{doc_workspace}` (thư mục làm việc riêng cho một lần chạy) chỉ được khai tường minh ở 3/5 file dù cũng được dùng ở bmad-brainstorming — một khoảng hở tài liệu quan sát được, không phải một quy tắc [1][2][3].

Cơ chế merge `customize.toml` thật (đọc trực tiếp `config_utils.py`, không đoán từ comment) là ba lớp base→team→user: `structural_merge()` đệ quy trên dict (scalar: override thắng; dict: merge lồng nhau); với mảng, nếu **mọi** phần tử của cả base lẫn override đều có field khoá `code` hoặc `id` thì merge-theo-khoá (khoá trùng → thay thế tại chỗ, khoá mới → append cuối); nếu không, mảng chỉ nối đuôi thuần tuý [12][11]. Đây chính là cơ chế cho phép Vấn Đạo sau này override đúng một lens/loại nghiên cứu bằng `code` trùng mà không phải viết lại cả mảng — ví dụ thật: `bmad-review/customize.toml` khai 5 bảng `[[workflow.lenses]]` mỗi bảng một `code` riêng [17][16].

**Lệch mẫu đáng chú ý**: bmad-prd đọc thẳng `_bmad/bmm/config.yaml` thay vì gọi `resolve_config.py` như 3 skill kia — không rõ lý do (chưa xác nhận được, để ở Câu hỏi mở) [1]. bmad-review lệch mẫu rõ nhất trong cả 5 dimension: dùng `## Execution` thay `## On Activation`, không chào người dùng, không có run-folder/memlog riêng — nó là một stateless review pass, không phải một quy trình nhiều bước có trạng thái [4].

### 2.2 Giữ trạng thái xuyên phiên

Memlog (`.memlog.md`) là "LLM-optimal working memory" — một log phẳng, chronological, append-only [10]. Ba bất biến tự khai trong `memlog.py`: (1) không bao giờ sửa/xoá/sắp lại — không có subcommand edit/delete; (2) write-only/blind — mỗi lệnh ghi atomic rồi echo JSON, caller không bao giờ đọc lại file *giữa* phiên; (3) không có field lifecycle "status" — việc xong/dở/bị chặn tự nó là một `event`, đọc được bằng cách đọc các entry cuối, giống mọi thứ khác [10]. Ghi file dùng temp-file → fsync → `os.replace` (atomic rename) để một crash không bao giờ để lại entry ghi dở [10].

`{doc_workspace}` bind theo công thức chung `{output_path}/{run_folder_pattern}/` ở cả 3 skill có memlog, nhưng khuôn tên folder khác nhau theo mục đích (`"{research_type}-{topic_slug}-{date}"` vs `"prd-{project_name}-{date}"` vs `"architecture-{project_name}-{date}"`) [8][1][2]. Riêng bmad-deep-recon KHÔNG để model tự sinh tên folder — nó gọi script `recon_kit.py slug` để tên folder deterministic theo topic, đảm bảo Draft→Run ngoài→Process luôn trỏ về đúng một chỗ [8][13].

Lý do "ghi file ngay" được viết thẳng ra (không phải suy luận): sống sót qua crash *và* tránh tràn context — "the conversation is a control channel, never the store" [3]. bmad-architecture áp cùng triết lý cho tài liệu cuối: spine được **chưng cất từ memlog ở cuối, không xây dần trong hội thoại** [2].

**Cảnh báo mạnh nhất của dimension này**: memlog **không phải cơ chế phổ quát**. bmad-prfaq hoàn toàn không dùng `memlog.py` — nó resume bằng cách đọc 20 dòng đầu của tài liệu đầu ra để lấy frontmatter `stage`, và lưu rationale/quyết định bằng comment HTML nhúng thẳng trong tài liệu (`<!-- coaching-notes-stage-1 -->`) [6]. Hai cơ chế trạng thái xuyên phiên khác nhau đang cùng tồn tại trong BMAD, chọn theo bản chất công việc: quy trình nghiên cứu/xây-dựng-quyết-định nhiều bước dùng memlog; quy trình có "giai đoạn tuyến tính rõ ràng, một tài liệu duy nhất" dùng frontmatter `stage`.

### 2.3 Điều phối subagent

"Research firewall" — định nghĩa chính xác nhất và duy nhất — chỉ có ở bmad-deep-recon: project context "shapes what to ask, never what is true", subagent "receive only their brief — no project files, no ambient context" [3][8]. Các skill khác dùng cơ chế **tương đương** (parent không giữ full text, mỗi subagent ghi file rồi trả tóm tắt) nhưng **không cùng tên gọi và không cùng contract trường dữ liệu**: bmad-deep-recon dùng `{claim, source, publisher, pub_date, accessed, confidence, class}` [8]; bmad-prd/bmad-architecture reviewer dùng `verdict + top 2-5 findings + file path` [1][9]; bmad-review dùng `{lens, location, trigger_condition, guard_snippet, potential_consequence}` [4]; bmad-prd reconcile-subagent dùng `input name + gaps 2-5 + file path` [1]. **Không có một digest-contract duy nhất xuyên BMAD** — mỗi skill tự định nghĩa contract khớp mục đích của nó.

Quy tắc thao tác lặp lại xuyên mọi skill có subagent: **ghi file trước khi làm bất cứ điều gì khác với kết quả** — "write the digest... before doing anything else with it" [8]; kể cả khi fallback chạy tuần tự (không có subagent), quy tắc vẫn là "write the file first, then flush it from context", không giữ lại trong working context [1][9]. bmad-architecture giải thích rõ lý do triết học: "an inline self-check does not count — the independent context is the point, because a fresh reviewer finds the divergences the author talks past" [9].

Mức song song và ngân sách được định lượng theo preset (quick=2, standard=3, deep=6, cap 10) và scale theo độ khó nhiệm vụ (dưới 5 lookup đơn giản, ~10 khó, 15 nhiều phần, 20 không bao giờ vượt) [8]. **Không tìm thấy cơ chế kỹ thuật (sandbox/permission) nào thực thi firewall** — toàn bộ là kỷ luật văn xuôi cho agent điều phối tự tuân thủ khi soạn brief [8][9][4] — đánh giá đầy đủ ở Khuyến nghị #4.

### 2.4 Human-in-the-loop / gate

Plan Gate của bmad-deep-recon là "the one hard stop, kept light" — đúng một điểm dừng cứng cho toàn bộ quy trình Run, không phải nhiều gate rải rác [8]. Nội dung bắt buộc: decision, dimensions đã prune theo decision, topology (breadth-first/depth-first/straightforward), knob đang áp dụng và nguồn gốc, search surfaces sẵn có, có chạy workflow hay không, và ước tính thời gian trung thực [8]. Sau gate, mọi checkpoint còn lại chỉ là "one or two lines in chat", không chờ duyệt — "keep moving unless the user speaks up" [8]. Đây khác hẳn Reviewer Gate của bmad-prd/bmad-architecture, vốn KHÔNG tồn tại trong bmad-deep-recon [8][1][2][9]: Reviewer Gate dispatch reviewer song song, lint deterministic trước (`lint_spine.py`, "so reviewers spend judgment on the semantic half") [9], rồi trình bày tiered — một câu verdict, critical+high, medium/low gộp đuôi "plus N more in {file}" [1][9].

Coaching path là mặc định tường minh ở cả bmad-prd và bmad-architecture, với quy tắc "elicit, don't quiz" gần như song sinh giữa hai file: mở câu hỏi ("how are you thinking about X?") thắng menu trắc nghiệm; chỉ dùng either/or cho "genuinely binary fork" [1][2]. bmad-prd đặt tên ngưỡng cụ thể cho lúc AI phạm luật: "When you find yourself naming wedges, picking MVP cuts, or proposing phases, stop — you have crossed from elicitation into authoring" [1]. bmad-architecture đi xa hơn: buộc các quyết định trọng yếu (paradigm, stack, ranh giới lớn) phải "shown, not silently made" — trình bày phương án đã cân nhắc, để người dùng chọn, rationale sống trong hội thoại + memlog chứ không phải trong tài liệu cuối [2]. Fast path là lối thoát chính danh duy nhất cho việc AI tự suy luận, luôn đi kèm tag `[ASSUMPTION]` được triage lại ở Finalize [1][2].

Quy tắc "đừng hỏi thứ scan tự trả lời được" được diễn đạt **tường minh và mạnh nhất** ở bmad-project-context — coi việc hỏi lại một claim đã path-check hoặc một config file đã nói là **defect**, không chỉ lãng phí [7]. Cụm từ đúng nghĩa đen này không xuất hiện ở bmad-prd hay bmad-deep-recon; bmad-architecture có tinh thần tương tự nhưng diễn đạt khác ("don't re-tell the user what the scan already shows", "inherit... silently") [2][7].

### 2.5 Văn phong hướng dẫn model

Cả 5 SKILL.md khảo sát xưng ngôi thứ hai ("you"); 4/5 mở đầu bằng persona tường minh dạng "You are..."/"Act as..." — riêng bmad-review là ngoại lệ, mở bằng mệnh lệnh trực tiếp không gán vai [1][2][3][6][4]. Kỹ thuật ép đúng thứ tự lặp lại nhất: numbered "On Activation" ở mọi file, và bmad-prd/bmad-prfaq dùng gần NGUYÊN VĂN cùng một câu chốt: "confirm every entry was executed in order before proceeding... Do not begin the main workflow until all activation steps have been completed" [1][6].

"One test decides what belongs" — đóng khung một quy tắc phức tạp (cái gì thuộc kiến trúc) thành một câu hỏi có/không duy nhất — chỉ xuất hiện đúng nghĩa đen ở bmad-architecture [2], nhưng mẫu hình "một tiêu chí thay liệt kê" lặp lại dưới hình dạng khác ở 4/5 file: ngưỡng elicitation→authoring của bmad-prd [1]; quy tắc zero-findings theo lens của bmad-review [4]; "A claim is a sentence with a source" của bmad-deep-recon [3].

Cả 5 file đẩy chi tiết ra `references/*.md`, nạp "just-in-time" — bmad-review nói thẳng "load only what runs" [4]; bmad-deep-recon có bảng ánh xạ intent→file tường minh [3]; ngay cả bmad-prfaq (136 dòng, dài nhất trong 5 file) vẫn chỉ giữ Stage 1 inline, đẩy 4 giai đoạn còn lại ra file riêng [6]. **Không tìm thấy quy tắc số-dòng-tối-đa bằng lời** cho SKILL.md ở bất kỳ file nào — nguyên tắc "ngắn gọn" chỉ thể hiện qua hành vi cấu trúc thực tế (50-136 dòng quan sát được), không phải luật viết ra [1][2][3][6][4].

## 3. Phát hiện xuyên chiều

1. **Ba lớp kỷ luật khác nhau đang hoạt động dưới cùng một triết lý "đừng để context/tài liệu trôi"**: memlog (bộ nhớ quá trình, xuyên phiên) [10], "extract, don't ingest" (cô lập ngữ cảnh giữa parent-subagent trong MỘT phiên) [3][1][9], và "distill at the end" (tài liệu cuối được tổng hợp một lần từ log, không xây dần trong hội thoại) [2][10]. Ba cơ chế phục vụ ba bài toán khác nhau — resume-được, không-tràn-context, và tài-liệu-cuối-gọn — nhưng dễ bị nhầm là một thứ. Vấn Đạo nên tách rõ ba lớp này khi thiết kế: memlog tương đương với `truong-mon/lo-trinh.jsonl` (đã có sẵn theo kiểu append-only, đúng tinh thần), "extract, don't ingest" tương đương với info-hiding giữa các vai (đã có, mạnh hơn BMAD vì có ranh giới file-system thật — xem 2.3), còn "distill at the end" là mẫu hình Vấn Đạo **chưa có tên** (xem Khuyến nghị #6) dù về bản chất giáo án/lộ đồ cũng được tổng hợp một lần chứ không viết dần.

2. **Reviewer Gate và Plan Gate là hai triết lý HITL khác nhau, chọn theo bản chất quyết định, không phải mức độ quan trọng.** Plan Gate (deep-recon) là một cổng TRƯỚC khi làm — dừng để duyệt kế hoạch, sau đó chạy liền mạch không hỏi lại [8]. Reviewer Gate (prd, architecture) là một cổng SAU khi có bản nháp — dispatch song song để tìm lỗi tác giả tự bỏ sót [1][9]. Vấn Đạo hiện có cả hai dạng rải rác trong đặc tả nhưng chưa đặt tên tường minh (xem Khuyến nghị #3).

3. **Sự KHÔNG đồng nhất giữa các skill BMAD (bmad-review, bmad-prfaq lệch mẫu rõ rệt) tự nó là một bài học thiết kế, không phải nhiễu.** Cả hai trường hợp lệch đều có lý do bản chất: bmad-review là stateless (một lần review, không có vòng đời nhiều bước) nên không cần memlog/run-folder; bmad-prfaq có 5 giai đoạn tuyến tính cố định nên frontmatter `stage` đơn giản hơn memlog chronological. Bài học cho Vấn Đạo: không phải mọi skill cần đủ bộ máy nặng — chọn cơ chế theo hình dạng công việc, không phải copy khuôn nặng nhất cho mọi vai (xem Khuyến nghị #2).

## 4. Bằng chứng ngược

Không chạy red-team pass ở lượt nghiên cứu này (`red_team: off`) — không có mục nào ở phần này.

## 5. Khuyến nghị

1. **Áp nguyên văn khuôn "bước 1 activation" của BMAD cho mọi skill mới của Vấn Đạo**: gọi script resolve customize/config trước, fallback đọc trực tiếp nếu lỗi, rồi mới vào việc chính — đây là mẫu hình ổn định nhất tìm thấy (5/5 skill, gần nguyên văn) [1][2][3][5][4]. Độ tin: cao. *Feed vào: cách viết `thu-linh/SKILL.md`, `truong-mon/SKILL.md` và các skill khác.*

2. **Không copy memlog.py cho mọi vai của Vấn Đạo một cách máy móc — chọn theo hình dạng công việc, như chính BMAD đã làm (bmad-prfaq lệch mẫu có chủ đích).** Vai có nhiều phiên, trạng thái tích luỹ (`thu-linh` dạy nhiều chương qua nhiều tuần) hợp với mẫu hình append-only-log gần giống memlog — Vấn Đạo *đã* có mẫu này ở `lo-trinh.jsonl`/`chi-diem.jsonl` (kiến trúc spine AD-2). Vai một-lượt, ít trạng thái (Giám khảo sinh đề, coi thi — `khao-thi`, gần giống bmad-review) không cần bộ máy nặng. Độ tin: trung bình (suy luận từ cách BMAD tự phân hoá, không phải một khuyến nghị BMAD viết thẳng ra). *Feed vào: architecture spine (đã đúng hướng ở AD-2), epics cho `khao-thi` vs `thu-linh`.*

3. **Đặt tên tường minh hai mẫu hình HITL của Vấn Đạo theo đúng phân biệt Plan Gate vs Reviewer Gate mà BMAD đã tách rõ**, thay vì gọi chung "điểm duyệt". F-1 (lộ đồ trình duyệt trước khi dạy) là Plan Gate — một hard-stop, không hỏi lại giữa chừng. Nghiệm Công Sứ/Phúc Khảo Sứ (chấm độc lập rồi so cờ bất đồng) là Reviewer Gate — dispatch song song, so sánh sau. Đặt tên tường minh sẽ giúp epics/stories sau này không lẫn lộn "khi nào cần dừng-trước" với "khi nào cần soát-sau". Độ tin: cao cho việc phân biệt là thật (quan sát trực tiếp từ 2 skill khác nhau của BMAD); trung bình cho việc đặt-tên-tường-minh có ích thật cho Vấn Đạo (chưa kiểm chứng ở build thật). *Feed vào: `bmad-spec`/epics khi viết story cho FR6 và FR12a-b.*

4. **Giữ nguyên — không hạ thấp — ranh giới file-system thật của Vấn Đạo (`.pham-vi.json`, `tools:` hẹp cho subagent tươi) thay vì chỉ dựa vào kỷ luật văn xuôi như "research firewall" của BMAD.** Nghiên cứu này xác nhận: **không tìm thấy** cơ chế kỹ thuật nào (sandbox/permission) thực thi firewall trong BMAD — toàn bộ dựa vào agent điều phối tự tuân thủ khi soạn brief [8][9][4]. Vấn Đạo đã đi xa hơn (đã ghi trong spine AD-3, AD-4) — đây là một điểm Vấn Đạo mạnh hơn nguồn tham khảo, không phải chỗ cần "học theo". Độ tin: cao. *Feed vào: không cần hành động, chỉ xác nhận hướng đã chọn.*

5. **Dùng đúng cụm "one test decides" hoặc biến thể một-câu-hỏi cho mọi luật phức tạp trong SKILL.md của Vấn Đạo**, thay vì liệt kê hết trường hợp — ví dụ: luật "khi nào một component thuộc Bậc 1 vs Bậc 3" hay "khi nào một field là Loại 1 vs Loại 2" (đã có sẵn trong spine AD-5 dưới dạng "phép kiểm 3 câu hỏi", đúng mẫu hình này) nên viết lại theo khuôn if-then một câu như `bmad-architecture` đã làm, thay vì bảng liệt kê dài. Độ tin: trung bình (một khuyến nghị về văn phong, không phải một fact có thể sai/đúng). *Feed vào: cách viết SKILL.md cho mọi vai.*

6. **Đặt tên tường minh cho mẫu hình "distill at the end"** — tài liệu cuối (giáo án đã dạy xong một chương, lộ đồ đã hoàn tất một quyển) được tổng hợp một lần từ log sự kiện đã ghi sẵn, không xây dần trong hội thoại (bmad-architecture: "The spine file itself is distilled from the memlog at the end, not written as you go"). Vấn Đạo hiện làm đúng điều này về bản chất (giáo án chỉ ghi sự kiện mỗi nước đi, không ghi lời giảng — đặc tả §5.9) nhưng chưa có tên gọi tường minh cho nguyên tắc, khiến nó dễ bị vi phạm khi viết SKILL.md mới (vd. một skill tương lai vô tình tích luỹ văn xuôi dần trong ngữ cảnh thay vì chưng cất từ log). Độ tin: trung bình (suy luận từ cách BMAD đặt tên nguyên tắc, áp dụng sang một mẫu hình Vấn Đạo đã có nhưng chưa gọi tên). *Feed vào: cách viết SKILL.md cho `thu-linh`, `truong-mon` — nơi có tài liệu tổng hợp cuối.*

## 6. Câu hỏi còn mở

1. Vì sao `bmad-prd` đọc thẳng `_bmad/bmm/config.yaml` thay vì gọi `resolve_config.py` như 3 skill kia — chưa xác nhận được lý do (hai cơ chế config trung tâm song song? cố ý hay tàn dư lịch sử?) [1].
2. Cơ chế Refresh/Deepen của bmad-deep-recon xử lý conflict thế nào khi nguồn đã đổi so với lần chạy trước — nằm trong `references/lifecycle.md`, chưa đọc trong lượt này (ngoài phạm vi 7 file đã chọn).
3. Hình dạng thật (một ví dụ render cụ thể) của "compact checklist" ở plan gate — `run.md` chỉ đặc tả các trường nội dung bắt buộc, không có mẫu văn bản thật [8].
4. Liệu mẫu hình "one test decides" có lặp lại ở các SKILL.md khác ngoài 7 file đã đọc (vd. `bmad-spec`, `bmad-build`) — chưa khảo sát, một lead từ dimension 5.
5. Cơ chế `references/headless.md`/`references/validate.md`/`references/verification.md` — được trỏ tới dày đặc nhưng nằm ngoài phạm vi 7 file đã chọn cho lượt này; có thể chứa thêm chi tiết về cách gate biến mất ở chế độ headless.

## 7. Phụ lục nguồn

Mọi nguồn dưới đây: publisher "BMAD-METHOD skill source (local)" · ngày xuất bản N/A (mã nguồn cục bộ, không phải xuất bản phẩm) · truy cập 2026-08-25 · độ tin Cao (đọc trực tiếp).

| # | Nguồn | Hỗ trợ phát hiện |
|---|---|---|
| [1] | `.claude/skills/bmad-prd/SKILL.md` | Cấu trúc activation, extract-don't-ingest, Reviewer Gate, Coaching/Fast path, văn phong |
| [2] | `.claude/skills/bmad-architecture/SKILL.md` | One-test-decides, Coaching path mặc định, shown-not-silently-made, cấu trúc activation |
| [3] | `.claude/skills/bmad-deep-recon/SKILL.md` | Research firewall, extract-don't-ingest, epistemics, "nothing exists until it is a file" |
| [4] | `.claude/skills/bmad-review/SKILL.md` | Lệch mẫu (Execution/không persona/không memlog), lens isolation, digest contract riêng |
| [5] | `.claude/skills/bmad-brainstorming/SKILL.md` | Cấu trúc activation, resume-scan trước khi tạo workspace mới |
| [6] | `.claude/skills/bmad-prfaq/SKILL.md` | Cơ chế state khác hẳn (frontmatter stage + comment nhúng), bảng Stages, persona "hardcore mode" |
| [7] | `.claude/skills/bmad-project-context/SKILL.md` | "Never ask what a scan could answer" tường minh nhất, Interview-the-gaps |
| [8] | `.claude/skills/bmad-deep-recon/references/run.md` | Plan Gate, fan-out, digest contract, stop-and-write valve |
| [9] | `.claude/skills/bmad-architecture/references/reviewer-gate.md` | Lint deterministic trước, subfolder reviews/, lý do "independent context is the point" |
| [10] | `_bmad/scripts/memlog.py` | Ba bất biến (append-only, write-only, no-lifecycle-status), atomic write, format file |
| [11] | `_bmad/scripts/resolve_customization.py` | `--key` dotted-path, exit code 1 khi lỗi (kích hoạt fallback), tìm project-root ngược cây |
| [12] | `_bmad/scripts/config_utils.py` | Cơ chế merge thật ba lớp, `structural_merge()`, `_merge_arrays()` theo khoá `code`/`id` |
| [13] | `.claude/skills/bmad-deep-recon/scripts/recon_kit.py` | `slug` sinh tên folder deterministic, `tally` đếm claim theo last-status-wins |
| [14] | `.claude/skills/bmad-prd/customize.toml` | Field lặp lại (activation_steps, persistent_facts, doc_standards...), cảnh báo DO NOT EDIT |
| [15] | `.claude/skills/bmad-architecture/customize.toml` | Cùng khuôn field với bmad-prd, `spine_output_path`, `run_folder_pattern` |
| [16] | `.claude/skills/bmad-deep-recon/customize.toml` | `persistent_facts = []` có chủ đích (research firewall), 6 bảng `[[workflow.research_types]]` khoá `code` |
| [17] | `.claude/skills/bmad-review/customize.toml` | 5 bảng `[[workflow.lenses]]` khoá `code` — ví dụ thật của merge-theo-khoá |
| [18] | `.claude/skills/bmad-brainstorming/customize.toml` | Field `persistent_facts` mặc định giống bmad-prd/bmad-architecture |

## 8. Bản đồ độ mới

Đây là điểm khác biệt quan trọng so với nghiên cứu web thông thường: mọi nguồn ở đây là **mã nguồn cục bộ của chính workspace này, đọc trực tiếp ngày 2026-08-25**, không phải xuất bản phẩm bên ngoài có ngày công bố riêng — nên `recon_kit.py staleness` (thiết kế cho `pub_date` dạng `YYYY-MM` của nguồn web) không áp dụng một cách có ý nghĩa ở đây.

"Độ mới" thật sự của báo cáo này là: **các file BMAD-METHOD này có thể tự đổi** nếu framework cập nhật (đúng như `customize.toml` tự cảnh báo "DO NOT EDIT -- overwritten on every update" [14][15][16][17][18]). Mốc tái xác minh hợp lý: **trước khi Vấn Đạo thật sự bắt đầu viết SKILL.md** (ở `bmad-create-epics-and-stories`/`bmad-build`), chạy lại một lượt đọc nhanh (không cần fan-out đầy đủ) để xác nhận 5 kỹ thuật ở §1 (Tóm tắt điều hành) chưa đổi — đặc biệt bước 1 activation và cơ chế merge `customize.toml`, vì đây là hai điểm Vấn Đạo dự định copy gần nguyên văn.
