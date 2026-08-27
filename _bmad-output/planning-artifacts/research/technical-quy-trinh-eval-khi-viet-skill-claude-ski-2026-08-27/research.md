---
title: 'technical research: Quy trình eval khi phát triển 1 skill Claude'
type: 'technical'
topic: 'Quy trình eval khi phát triển 1 skill Claude — eval ngay từ đầu hay sau vertical slice'
decision: 'Story 1.1 (skill nhap-mon) đã viết xong, chưa có eval — quyết định dừng viết eval ngay hay tiếp tục story kế tiếp trước, đối chiếu NFR4 vs kế hoạch thao tác thật'
source: 'native run — 2 dimension breadth-first + 1 round lead-following'
status: complete
preset: 'standard'
validation: 'normal'
created: '2026-08-27'
updated: '2026-08-27'
claims_verified: 11
claims_unverified: 1
---

# technical research: Quy trình eval khi phát triển 1 skill Claude

**Decision this research serves:** Story 1.1 (skill `nhap-mon`) đã viết xong SKILL.md, chưa có eval — quyết định dừng lại viết eval ngay hay tiếp tục sang skill/story kế tiếp trước, đối chiếu NFR4 (PRD: "mọi skill phải có eval trước khi hoàn thành") với kế hoạch thao tác thật của van-dao (Ưu tiên 2 = vertical slice chạy được trước, Ưu tiên 3 = hình thức hoá eval sau).

## Tóm tắt điều hành

**Bằng chứng không ủng hộ việc hoãn eval của một skill đã viết xong đến khi có vertical slice nhiều-skill.** Ba phát hiện dẫn tới kết luận này:

1. Công cụ chính thức `skill-creator` của Anthropic — đọc trực tiếp mã nguồn `SKILL.md` của nó, nội dung khớp qua 2 đường fetch khác nhau (GitHub trực tiếp lỗi SSL, xác nhận lại qua mirror jsdelivr) — thực hiện đúng trình tự: viết draft **một** skill → tạo vài test prompt/eval nhỏ ngay sau đó trong cùng phiên làm việc → lặp lại tới khi hài lòng → mở rộng bộ test sau [2]. Đây là quy trình cho một skill đơn lẻ, diễn ra ngay lập tức — không phải "dồn eval sang sau khi có nhiều skill phối hợp".
2. Không tài liệu chính thức nào (Anthropic best-practices [1], code.claude.com [3], agentskills.io [4]) hay bằng chứng thực tiễn nào (OpenAI [6], Minko Gechev [7], Paul Twist [8]) ủng hộ rõ ràng việc hoãn eval một skill đã viết xong. Nguồn duy nhất bàn trực tiếp bối cảnh nhiều-agent/nhiều-skill (PwC [15], độ tin cậy trung bình — chưa xác minh chéo) đi **ngược** hướng "hoãn tới vertical slice": khuyến nghị validate từng agent/skill riêng lẻ trước, rồi mới validate hệ thống tích hợp.
3. "Vertical slice trước" có tiền lệ kỹ nghệ phần mềm thật — Walking Skeleton [9], Architectural Spike [11] — nhưng phục vụ mục tiêu khác: giảm rủi ro **tích hợp/kiến trúc** ở cấp hệ thống, không phải lý do để bỏ qua xác minh đúng-sai của một component (skill) đã viết xong. Không nguồn nào trong số này bàn về AI skill eval cụ thể.

**Áp dụng cho Story 1.1:** khoảng cách giữa NFR4 và kế hoạch thao tác thật không lớn như nhìn ban đầu — nhưng bằng chứng nghiêng về phía NFR4 (eval bám sát mỗi skill), ở **mức độ nhẹ** đúng như quy trình chính thức mô tả: agentskills.io nói thẳng "bắt đầu với 2-3 test case, đừng đầu tư quá mức trước khi thấy kết quả vòng đầu" [4] — không phải bộ máy đầy đủ 20-câu/`evals.json`/60-40-train-test mà `van-dao/.claude/rules/eval.md` mô tả cho trạng thái "hoàn thiện". Tức: đúng lúc viết một vòng eval **nhẹ** (vài kịch bản khớp I/O matrix của Story 1.1) trước khi sang Story 1.2, nhưng không bắt buộc phải dựng ngay toàn bộ khung trigger-eval hình thức của Ưu tiên 3.

**Caveat lớn nhất:** không có nguồn nào — kể cả tài liệu chính thức Anthropic — bàn thẳng vào đúng kịch bản "nhiều skill Claude phối hợp, có nên hoãn eval". Kết luận trên là suy luận có căn cứ từ việc ghép quy trình chính thức cho một skill đơn (bằng chứng mạnh) với bằng chứng multi-agent tổng quát ngoài hệ sinh thái Claude (PwC, bằng chứng vừa, chưa xác minh chéo) — không phải câu trả lời tường minh trực tiếp.

## D1 — Quy trình chính thức của `skill-creator`

Tài liệu chính thức Anthropic tự mâu thuẫn nhẹ về **thứ tự** khi phát triển một skill đơn lẻ, dù cả hai đều không bàn kịch bản nhiều-skill:

- **Best-practices** (`platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices`) khuyến nghị eval-trước: "Create evaluations BEFORE writing extensive documentation" — quy trình 5 bước (chạy baseline không skill → ghi gap → tạo eval cho gap → viết instruction tối thiểu để pass → lặp lại), yêu cầu "at least three evaluations created" trước khi coi skill sẵn sàng chia sẻ [1].
- Nhưng **mã nguồn thật của skill `skill-creator`** (`github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md`, đọc trực tiếp, nội dung khớp qua 2 đường fetch khác nhau) lại thực hiện **ngược lại**: "Decide what you want the skill to do" → "Write a draft of the skill" → "Create a few test prompts and run..." → đánh giá → viết lại → lặp tới khi hài lòng → mở rộng bộ test sau. Tiêu chí dừng là "user happy / feedback rỗng / không còn tiến bộ đáng kể" — không có điều kiện "phải có eval mới coi là xong" [2].
- `code.claude.com/docs/en/skills` coi eval là bước xảy ra **sau khi** skill đã tồn tại và chạy được ("evaluate an existing skill"), không phải điều kiện tiên quyết; giới thiệu plugin `skill-creator` để tự động hoá vòng lặp so sánh with/without-skill, lưu kết quả vào `evals/evals.json` [3].
- `agentskills.io/skill-creation/evaluating-skills` — trang mà `code.claude.com` dẫn làm nguồn tham chiếu chuẩn cho quy trình eval — mở đầu với giả định skill **đã viết xong**: "You wrote a skill, tried it on a prompt, and it seemed to work. But does it work reliably..." Khuyến nghị rõ: bắt đầu 2-3 test case, "don't over-invest before you've seen your first round of results", chưa cần định nghĩa assertion pass/fail chi tiết ngay [4].
- Blog Anthropic giới thiệu skill-creator nhấn mạnh giá trị testing ("Testing turns a skill that seems to work into one you know works") nhưng không tuyên bố dứt khoát về thời điểm; ví dụ minh hoạ (PDF skill) là một skill đơn, không phải multi-skill [5].

Cả bốn tài liệu chính thức (kể cả hai tài liệu tự mâu thuẫn về thứ tự viết-trước-hay-eval-trước) đều **thống nhất ở một điểm**: eval xảy ra ngay trong vòng đời của **một** skill, gần thời điểm skill đó được viết — không tài liệu nào hình dung một giai đoạn "dồn eval lại" sau khi nhiều skill khác đã được viết xong. Không tìm thấy Anthropic tự thừa nhận mâu thuẫn ngôn ngữ giữa hai tài liệu của chính họ.

Một manh mối tổ chức thực tế: GitHub Issue #490 trên `anthropics/skills` (mở 2026-03-02, có phản hồi) ghi nhận việc thư mục `evals/` sinh cùng cấp với skill trong `.claude/skills/` gây nhầm lẫn và khó đưa vào version control — một vấn đề vận hành có thật khi dự án có nhiều skill, nhưng bàn về **tổ chức thư mục**, không bàn **trình tự** viết eval [13].

## D2 — Bằng chứng thực tiễn rộng hơn về thời điểm eval

**Phía ủng hộ eval sớm, theo sát từng skill (không hoãn):**
- OpenAI (nhà cung cấp khác, cùng không gian agent skill): "Define success before you write the skill" [6].
- Minko Gechev, kỹ sư thật, blog cá nhân (26/02/2026): "Don't ship skills without evals" — eval phải tồn tại trước khi đưa vào sản xuất, dù không bàn riêng kịch bản vertical-slice [7].
- Paul Twist, DEV Community (13/07/2026): cảnh báo "eval debt" — nợ đánh giá "compounds every week", khuyến nghị coi hạ tầng eval "co-equal" với hạ tầng agent "from day one" [8].
- Hamel Husain & Shreya Shankar (chuyên gia eval AI có tên thật, hamel.dev): "evaluation is part of the development process rather than a distinct line item" — nguyên tắc chính của bài là bắt đầu phân tích lỗi ngay khi có output, không định nghĩa việc phải hoàn thành nhiều component trước mới eval; với workflow nhiều bước chỉ khuyên phân đoạn phân tích theo từng giai đoạn, không khuyên trì hoãn [14].
- PwC — nguồn multi-agent cụ thể duy nhất tìm được — khuyến nghị: validate từng agent/skill riêng lẻ **trước** ("Individual agents in MAS may require pre-deployment testing and validation"), rồi mới validate hệ thống tích hợp **sau** ("Once agents are validated individually, the assembled system should undergo additional testing..."). Đọc qua proxy (trang gốc trả HTTP 403), chưa xác minh chéo bằng nguồn thứ hai độc lập — giữ ở trạng thái `unverified` [15].

**Phía có tiền lệ lý thuyết cho "dựng luồng chạy được trước", nhưng không đặc thù AI eval:**
- Walking Skeleton (Alistair Cockburn, đồng tác giả Agile Manifesto, khái niệm gốc năm 2000, nhất quán qua nhiều nguồn thứ cấp độc lập): "cài đặt tối giản thực hiện một chức năng end-to-end nhỏ... kiến trúc và chức năng sau đó tiến hoá song song". Rủi ro của việc **không** làm điều này (xây riêng lẻ rồi mới tích hợp) được ghi nhận cụ thể: "data contracts, latency limits, output formats, and deployment constraints fail late... leads to rework" [9]. defmyfunc.com nêu cùng rủi ro bằng ngôn ngữ chung hơn: "failing to integrate can cause untold pain... disastrous consequences" [10].
- Architectural Spike (Vijay Anant): giai đoạn thử nghiệm giới hạn thời gian nơi chuẩn kiểm thử hình thức được nới lỏng để ưu tiên tốc độ chứng minh khái niệm [11].

Cả hai nguồn lý thuyết này nói về rủi ro **tích hợp kiến trúc** ở cấp hệ thống — không một nguồn nào áp dụng logic đó cho câu hỏi cụ thể "có nên bỏ qua/hoãn xác minh đúng-sai của một AI skill đã viết xong hay không". Không tìm thấy ai — kể cả tác giả gốc của Walking Skeleton hay các nguồn diễn giải nó — mở rộng khái niệm này sang bối cảnh AI agent eval.

**Kiểm tra phủ định (đã tìm nhưng không thấy):** Braintrust [12] — bài về khung eval agent thực hành, đọc trực tiếp — không hề bàn trình tự vertical-slice-trước-hay-eval-trước, chỉ mô tả vòng lặp eval khi agent đã ở production. Đây là bằng chứng phủ định có ý nghĩa: một nguồn eval-framework thực hành đương đại, khi có cơ hội bàn đúng câu hỏi này, đã im lặng — không có tiền lệ đủ phổ biến để nguồn này cần đề cập.

## Cross-dimension: điểm chỉ có được khi ghép hai hướng lại

- D1 (quy trình chính thức, riêng cho AI skill) và D2 (bằng chứng thực tiễn rộng hơn, độc lập điều tra) **hội tụ về cùng một câu trả lời thực hành** dù được tra cứu tách biệt: eval nên diễn ra sớm, ngay sau khi một skill được viết, ở mức độ nhẹ ban đầu — không nguồn nào ở một trong hai hướng gợi ý hoãn nó tới một cột mốc tích hợp sau này. Sự hội tụ độc lập này củng cố độ tin cậy của kết luận hơn bất kỳ nguồn đơn lẻ nào.
- Ngược lại, "vertical slice trước" — cụm từ dùng trong kế hoạch thao tác thật của van-dao — hoá ra là một khái niệm mượn từ kỹ nghệ phần mềm tổng quát (D2), được áp cho một vấn đề (rủi ro tích hợp kiến trúc) khác với vấn đề mà AI skill eval giải quyết (đúng-sai hành vi của một component). Ghép hai dimension lại cho thấy: van-dao có thể đang dùng đúng từ vựng ("vertical slice") nhưng cho sai loại rủi ro — rủi ro kiến trúc (đáng dựng slice trước) khác với rủi ro hành vi-sai của skill (đáng eval ngay, không phụ thuộc slice).

## Bằng chứng trái chiều

- Nội bộ Anthropic tự mâu thuẫn về **thứ tự** (không phải về **có-nên-hoãn-hay-không**): best-practices nói "eval trước khi viết tài liệu mở rộng" [1], còn mã nguồn thật của skill-creator lại "viết draft trước, eval sau" [2]. Không tài liệu nào đối chiếu tài liệu kia. Với quyết định của van-dao, mâu thuẫn này không đổi kết luận — cả hai thứ tự đều diễn ra **trong cùng một skill, gần nhau về thời gian**, không đề xuất khoảng cách nhiều-story như kế hoạch thao tác thật giả định.
- PwC [15] là nguồn duy nhất bàn đúng bối cảnh nhiều-agent, và nó đi ngược hướng "hoãn eval" — nhưng độ tin cậy chỉ ở mức trung bình (đọc qua proxy, chưa xác minh chéo, không rõ ngày xuất bản). Không dùng một mình nguồn này để quyết định; nó chỉ củng cố thêm cho kết luận vốn đã được 6+ nguồn độc lập khác ủng hộ.
- Red-team pass không chạy (mặc định `off`, không có dấu hiệu cần bật ở mức rủi ro của quyết định này — một lựa chọn quy trình nội bộ, không phải cam kết không thể đảo ngược).

## Khuyến nghị

1. **[Tin cậy cao — dựa trên 4 nguồn chính thức Anthropic hội tụ [1][2][3][4], dù có mâu thuẫn thứ tự nội bộ]** Viết một vòng eval **nhẹ** cho `nhap-mon` (Story 1.1) trước khi chuyển sang Story 1.2 — không cần bộ máy đầy đủ 20-câu trigger-eval / `evals.json` 60-40 train-test mà `eval.md` mô tả cho trạng thái hoàn thiện; 2-3 kịch bản khớp đúng I/O matrix đã có trong story (3 dòng: chưa cấu hình / đã cấu hình / phiên mới giữ nguyên) là đủ theo đúng mức "start with 2-3 test cases" mà agentskills.io khuyến nghị [4].
2. **[Tin cậy trung bình — 1 nguồn multi-agent cụ thể, chưa xác minh chéo [15], nhưng không có nguồn nào mâu thuẫn]** Không áp dụng nguyên văn kế hoạch "Ưu tiên 2 = vertical slice trước, Ưu tiên 3 = eval sau" cho việc kiểm tra ĐÚNG-SAI hành vi từng skill — chỉ áp "vertical slice trước" cho các quyết định KIẾN TRÚC/TÍCH HỢP thật sự (ví dụ: cách 2 skill truyền trạng thái cho nhau), đúng phạm vi mà Walking Skeleton/Spike phục vụ [9][11].
3. **[Tin cậy cao, meta]** Cân nhắc sửa `van-dao/.claude/rules/eval.md` để phân biệt rõ hai mức: (a) eval NHẸ bắt buộc ngay khi một skill được coi là "viết xong nháp" — vài kịch bản, không assertion chi tiết; (b) bộ eval ĐẦY ĐỦ (trigger 20-câu + `evals.json` behavioral, 60/40 train/test) — có thể hoãn tới một cột mốc hợp lý (ví dụ trước khi phát hành/chia sẻ plugin), nhưng KHÔNG hoãn tới "sau khi có vertical slice" một cách vô thời hạn. Đây là cách hoà giải NFR4 và kế hoạch thao tác thật mà bằng chứng ủng hộ, khác với việc chọn hẳn một bên.

## Câu hỏi còn mở

- Không có nguồn nào bàn trực tiếp, tường minh kịch bản "nhiều skill Claude phối hợp, hoãn eval tới khi có vertical slice" — nếu quyết định này có mức rủi ro cao hơn (vd. plugin đã phát hành công khai), nên tự thực nghiệm theo đúng mô hình RED→GREEN→REFACTOR / Claude-A-viết/Claude-B-test đã biết từ nghiên cứu trước trong dự án, thay vì tiếp tục suy luận từ tài liệu.
- PwC [15] cần xác minh chéo qua nguồn thứ hai độc lập (cache Google, bản PDF, hoặc bài tóm tắt khác) nếu khuyến nghị #2 ở trên trở thành căn cứ cho một quyết định kiến trúc lớn hơn — hiện tại nó chỉ đóng vai trò củng cố, không phải trụ cột.
- Ngày xuất bản chính xác của các trang docs Anthropic (best-practices, code.claude.com, agentskills.io) không xác nhận được — các trang dạng Mintlify không hiển thị ngày công khai; nếu cần mốc thời gian chính xác, phải tra qua Wayback Machine hoặc git history của repo docs (chưa làm ở lượt này).

## Nguồn

| # | Claim/phát hiện | Publisher | Ngày XB | Truy cập | Độ tin cậy |
|---|---|---|---|---|---|
| [1] | [platform.claude.com — best-practices, "eval trước khi viết docs mở rộng"](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Anthropic | không rõ | 2026-08-27 | Cao |
| [2] | [github.com/anthropics/skills — skill-creator SKILL.md, "draft trước, eval sau"](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | Anthropic | không rõ | 2026-08-27 | Cao |
| [3] | [code.claude.com/docs/en/skills — eval là bước sau khi skill tồn tại](https://code.claude.com/docs/en/skills) | Anthropic | không rõ | 2026-08-27 | Cao |
| [4] | [agentskills.io — evaluating-skills, bắt đầu nhỏ](https://agentskills.io/skill-creation/evaluating-skills) | Agent Skills spec (Anthropic-khởi-xướng) | không rõ | 2026-08-27 | Trung bình-cao |
| [5] | [claude.com/blog — improving skill-creator](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills) | Anthropic | ~2026-03 (chưa xác nhận độc lập) | 2026-08-27 | Trung bình |
| [6] | [developers.openai.com — Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | OpenAI | không rõ | 2026-08-27 | Trung bình |
| [7] | [blog.mgechev.com — Unit Tests for AI Agent Skills](https://blog.mgechev.com/2026/02/26/skill-eval/) | Minko Gechev (cá nhân) | 2026-02-26 | 2026-08-27 | Trung bình-cao |
| [8] | [dev.to/paultwist — The Evaluation Debt You Don't Know You Have](https://dev.to/paultwist/the-evaluation-debt-you-dont-know-you-have-why-agent-evals-fail-in-production-2md8) | DEV Community (Paul Twist) | 2026-07-13 | 2026-08-27 | Trung bình |
| [9] | [distilledpatterns.org / henricodolfing.ch / forbes.com — Walking Skeleton, kể cả câu trích rủi ro tích hợp trễ ("data contracts, latency limits... fail late")](https://distilledpatterns.org/patterns/walking-skeleton/) | Alistair Cockburn (qua 3 nguồn thứ cấp độc lập) | 2000 (khái niệm gốc) | 2026-08-27 | Cao |
| [10] | [defmyfunc.com — rủi ro không làm walking skeleton, diễn đạt chung hơn — không phải nguồn của câu trích cụ thể ở nguồn 9](https://www.defmyfunc.com/2019_10_18_walking_skeleton/) | defmyfunc (cá nhân) | 2019-10-18 | 2026-08-27 | Trung bình |
| [11] | [vijayanant.com — The Architectural Spike](https://vijayanant.com/posts/from-patterns-to-practice/the-spike/) | Vijay Anant (cá nhân) | không rõ | 2026-08-27 | Trung bình |
| [12] | [braintrust.dev — AI agent evaluation: A practical framework (negative finding)](https://www.braintrust.dev/articles/ai-agent-evaluation-framework) | Braintrust | 2026-02-02 | 2026-08-27 | Cao |
| [13] | [github.com/anthropics/skills/issues/490 — tổ chức thư mục evals](https://github.com/anthropics/skills/issues/490) | Anthropic (GitHub issue) | 2026-03-02 | 2026-08-27 | Cao |
| [14] | [hamel.dev — LLM Evals: Everything You Need to Know](https://hamel.dev/blog/posts/evals-faq/) | Hamel Husain & Shreya Shankar | ~2025-05-28 | 2026-08-27 | Trung bình-cao |
| [15] | [pwc.com — Validating multi-agent AI systems](https://www.pwc.com/us/en/services/audit-assurance/library/validating-multi-agent-ai-systems.html) | PwC US | không rõ | 2026-08-27 (qua proxy, HTTP 403 trực tiếp) | Trung bình (**unverified**) |

## Bản đồ độ cũ (staleness)

Tính bằng `recon_kit.py staleness`, cửa sổ theo lớp claim: tín hiệu AI-adjacent/landscape ≤3 tháng, tín hiệu hệ sinh thái/thực tiễn ≤6 tháng, pattern kỹ nghệ tổng quát ≤24 tháng.

- **Cần kiểm lại sớm nhất (≤ 2026-09-01):** [5] (claude.com blog), [13] (GitHub issue #490) — cửa sổ 6 tháng cho tín hiệu hệ sinh thái, đã gần nửa quãng.
- **Sắp tới hạn (≤ 2026-11-01):** [1][2][3][4][6][15] — nhóm tài liệu chính thức/vendor không rõ ngày xuất bản, đã tính bảo thủ theo ngày truy cập; nên tái xác nhận nếu quyết định trên bị trì hoãn quá 3 tháng.
- **Đã "quá hạn" theo cửa sổ máy tính nhưng KHÔNG cần tái kiểm** (dẫn chứng lịch sử/tiền lệ, không phải claim hiện trạng): [9] Walking Skeleton (2000), [10] defmyfunc (2019), [7] Gechev, [12] Braintrust, [14] Hamel/Shankar — các cửa sổ 6/24-tháng của pack được thiết kế cho claim về TRẠNG THÁI HIỆN TẠI của công nghệ, không phù hợp áp máy móc cho trích dẫn tiền lệ lịch sử hoặc quan sát đã kết luận xong; giữ nguyên, không cần re-fetch.
- Claim sớm nhất theo tính toán thô: 2002-01-01 ([9], vì pub_date gốc 2000 + cửa sổ pattern 24 tháng) — đây là hiện tượng máy móc của việc áp cửa sổ landscape cho một khái niệm nền tảng, không phải tín hiệu thật cần hành động.
