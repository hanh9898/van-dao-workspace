# Digest R1-1: Văn phong hướng dẫn model — Superpowers (obra) vs BMAD-METHOD

**Phạm vi:** 4 file SKILL.md gốc, đọc toàn văn qua tải trực tiếp (raw.githubusercontent.com, branch `main`, không cần thử `master`):
- `using-superpowers/SKILL.md` (63 dòng)
- `writing-skills/SKILL.md` (679 dòng)
- `brainstorming/SKILL.md` (250 dòng)
- `test-driven-development/SKILL.md` (320 dòng)

Khung đối chiếu: BMAD-METHOD (nghiên cứu trước) dùng ngôi thứ hai, persona tường minh "You are X", mẫu hình "one test decides", numbered activation steps.

---

## Câu 1 — Ngôi, giọng điệu, persona

- **Claim:** Không file nào trong 4 file gán persona kiểu "You are X" (không có "You are a senior TDD engineer" hay tương đương). Thay vào đó, `using-superpowers/SKILL.md` xưng hô trực tiếp ngôi hai với model qua khối `<EXTREMELY-IMPORTANT>`: "If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill... You cannot rationalize your way out of this."
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/using-superpowers/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

- **Claim:** Thân bài skill được viết ở giọng mệnh lệnh ngôi hai ẩn chủ ngữ (imperative), không phải tường thuật ngôi ba: ví dụ TDD mở đầu bằng "Write the test first. Watch it fail. Write minimal code to pass." — chuỗi câu mệnh lệnh liên tiếp, không có chủ ngữ "you" tường minh nhưng ngữ cảnh là ra lệnh trực tiếp cho agent.
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/test-driven-development/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

- **Claim:** Trái lại, trường `description` trong YAML frontmatter được `writing-skills/SKILL.md` quy định BẮT BUỘC viết ở ngôi thứ ba ("Write in third person (injected into system prompt)"), và checklist triển khai lặp lại yêu cầu này ("Description written in third person"). Đây là quy tắc phân tầng: ngôi ba chỉ áp cho phần metadata mô tả điều kiện kích hoạt, còn phần thân hướng dẫn hành vi dùng giọng mệnh lệnh ngôi hai.
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

- **Claim:** Không dùng "user"/"assistant" mà nhất quán dùng cụm "your human partner" để chỉ người dùng cộng tác (xuất hiện trong cả 4 file: using-superpowers, brainstorming, tdd, writing-skills), ví dụ TDD: "Exceptions (ask your human partner)"; brainstorming: "until you have told your human partner what you intend and they have approved it."
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/test-driven-development/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

- **So với BMAD:** BMAD gán persona tường minh ("You are X" — một nhân vật/vai trò cụ thể). Superpowers không gán persona nào — agent vẫn là chính nó (Claude/Codex/Gemini...), chỉ được ra lệnh hành vi trực tiếp. Đây là khác biệt cấu trúc rõ rệt, không phải chỉ khác giọng văn.

## Câu 2 — Kỹ thuật ép đúng thứ tự bước

- **Claim:** `brainstorming/SKILL.md` dùng numbered steps tường minh cho từng nhánh quy trình (Spike 1-5, Bounded 1-5, Architectural 1-9) trong mục "Checklist", ví dụ nhánh Architectural: "6. **Write design doc**... 7. **Spec self-review**... 8. **User reviews written spec**... 9. **Transition to implementation**".
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

- **Claim:** Từ "Never" xuất hiện lặp lại như một chỉ dấu cấm tuyệt đối: TDD "Never fix bugs without a test."; writing-skills "Never use flowcharts for: Reference material..."; writing-skills SDO "NEVER summarize the skill's process or workflow" (viết hoa toàn bộ, lặp lại 2 lần trong cùng file).
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

- **Claim:** Mẫu câu điều kiện nếu-thì ngắn, dạng "câu hỏi tự vấn → chỉ thị" được lặp lại có hệ thống trong toàn bộ chu trình RED-GREEN-REFACTOR của TDD: "Test passes? You're testing existing behavior. Fix test." / "Test errors? Fix error, re-run until it fails correctly." / "Test fails? Fix code, not test." / "Other tests fail? Fix now." — mỗi bước xác minh đều có cặp câu hỏi-hành động này.
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/test-driven-development/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

- **Claim:** Cả 4 file đều dùng bảng "Thought/Excuse | Reality" (bảng phản-biện-hoá lý do biện minh) như một cấu trúc lặp lại xuyên suốt framework: using-superpowers có bảng "Red Flags" 11 dòng; brainstorming có bảng "Red Flags" 7 dòng; TDD có bảng "Common Rationalizations" 10 dòng; writing-skills có 2 bảng riêng ("Common Rationalizations for Skipping Testing" và ví dụ bảng trong "Bulletproofing Skills"). Đây là một device chuẩn hoá cấp framework, không phải ngẫu nhiên từng file.
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/using-superpowers/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

- **Claim:** Có khối luật cấp cao đóng khung bằng code-fence in hoa gọi là "Iron Law", lặp lại cấu trúc giống nhau ở 2 file khác nhau: TDD — "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"; writing-skills — "NO SKILL WITHOUT A FAILING TEST FIRST" (được writing-skills gọi tên "The Iron Law (Same as TDD)"), đều kèm theo danh sách "No exceptions" liệt kê từng cách lách luật cụ thể ("Don't keep it as reference", "Don't 'adapt' it while writing tests", "Don't look at it", "Delete means delete").
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

- **Claim:** Dùng thẻ giả-XML tuỳ biến để đánh dấu khối bắt buộc/không thương lượng, không thấy trong markdown chuẩn: `<SUBAGENT-STOP>`, `<EXTREMELY-IMPORTANT>` (using-superpowers), `<HARD-GATE>` (brainstorming), `<Good>`/`<Bad>` (writing-skills, TDD dùng cho code example). Đây là kỹ thuật ép mức ưu tiên đọc/tuân thủ bằng markup ngoài chuẩn Markdown.
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

- **Claim:** brainstorming.md có "ratchet một chiều" tường minh ép thứ tự không thể đảo ngược: "The ratchet is one-way: hidden complexity discovered mid-task upgrades the path — stop, say so, and step up. Nothing downgrades mid-task." — một cơ chế ép trình tự dựa trên hướng, khác với numbered steps thuần tuý.
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

## Câu 3 — Mẫu hình "một tiêu chí/test quyết định"

- **Claim:** brainstorming.md dùng một câu hỏi độc nhất để quyết định nên dùng "browser" hay "terminal" khi trình bày, thay vì liệt kê hết mọi loại nội dung: "Per-question decision: Even after the user accepts, decide FOR EACH QUESTION whether to use the browser or the terminal. The test: **would the user understand this better by seeing it than reading it?**"
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

- **Claim:** brainstorming.md cũng dùng một phép thử đơn nhất để phân loại "bounded" thay vì liệt kê case: "bounded means the flow you are changing is already here to read. If there is no existing flow to change, the task is not bounded." — một tiêu chí nhị phân quyết định toàn bộ nhánh xử lý, đặt cạnh bảng Red Flags cảnh báo việc lạm dụng nhãn "bounded" để né quy trình.
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

- **Claim:** writing-skills.md có bảng "Match the Form to the Failure" — thay vì liệt kê hết loại thất bại, quy về đúng 4 loại baseline failure ánh xạ 1-1 sang "right form"/"wrong form", và nói rõ nguyên tắc chọn form phải dựa trên phân loại failure trước khi viết hướng dẫn ("Before writing guidance, classify the baseline failure. The form that bulletproofs one failure type measurably backfires on another.") — đây là mẫu "một tiêu chí phân loại quyết định form" áp dụng ở cấp meta (cách viết skill), không chỉ cấp nội dung skill.
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "medium"`, `class: "pattern"`

- **Nhận định đối chiếu (confidence: medium):** Không thấy cụm từ hay cấu trúc trùng khớp chính xác với "one test decides" của BMAD, nhưng có mẫu hình tương đương về chức năng — một câu hỏi/tiêu chí nhị phân độc nhất thay cho danh sách case. Điểm khác: Superpowers áp dụng mẫu này ở cấp ra-quyết-định-hành-vi cục bộ (chọn browser/terminal, phân loại bounded), trong khi vẫn dùng bảng liệt kê đầy đủ (rationalization tables) ở cấp chống-biện-minh — tức là hai kỹ thuật song song, không thay thế nhau hoàn toàn như câu hỏi giả định.

## Câu 4 — Độ dài / mật độ SKILL.md

- **Claim:** Độ dài đo được: `using-superpowers/SKILL.md` = 63 dòng (skill điều phối, nạp vào mọi hội thoại); `brainstorming/SKILL.md` = 250 dòng; `test-driven-development/SKILL.md` = 320 dòng; `writing-skills/SKILL.md` = 679 dòng (dài nhất trong 4 file, bản thân nó là skill dạy cách viết skill).
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

- **Claim:** writing-skills.md quy định target độ dài bằng số từ cụ thể, phân tầng theo tần suất nạp: "getting-started workflows: <150 words each", "Frequently-loaded skills: <200 words total", "Other skills: <500 words (still be concise)", và hướng dẫn xác minh bằng lệnh `wc -w skills/path/SKILL.md`.
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

- **Claim:** Cả 3 skill nội dung (writing-skills, brainstorming, TDD) đều đẩy phần chi tiết nặng ra file riêng và chỉ trỏ tới bằng liên kết tường minh, không nhúng: TDD trỏ tới `writing-good-tests.md` ("read writing-good-tests.md for the rules that keep tests honest"); brainstorming trỏ tới `visual-companion.md` ("read the detailed guide before proceeding: skills/brainstorming/visual-companion.md"); writing-skills trỏ tới `testing-skills-with-subagents.md`, `persuasion-principles.md`, `anthropic-best-practices.md`, `graphviz-conventions.dot`, `render-graphs.js`.
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/test-driven-development/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

- **Claim:** writing-skills.md quy tắc hoá ngưỡng tách file: "Separate files for: 1. Heavy reference (100+ lines)... 2. Reusable tools..." và "Keep inline: Principles and concepts; Code patterns (< 50 lines); Everything else." — tức có ngưỡng số dòng cụ thể (100+ dòng → tách file; <50 dòng code → giữ inline) chứ không phải quyết định tuỳ ý.
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

- **Claim:** using-superpowers.md (skill nạp vào MỌI hội thoại) đẩy toàn bộ phần đặc thù nền tảng ra 4 file reference riêng theo từng harness, giữ thân file gốc rất mỏng: "If your harness appears here, read its reference file for special instructions: Codex: `references/codex-tools.md`; Pi: `references/pi-tools.md`; Antigravity: `references/antigravity-tools.md`; Hermes Agent: `references/hermes-tools.md`."
  `source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/using-superpowers/SKILL.md"`, `publisher: "GitHub (obra/superpowers)"`, `pub_date: "N/A"`, `accessed: "2026-08-25"`, `confidence: "high"`, `class: "pattern"`

---

## Ghi chú phương pháp

- Cả 4 URL đều tồn tại trên branch `main`; không cần fallback `master`.
- Nội dung được tải trực tiếp bằng `curl` (raw.githubusercontent.com) để đảm bảo văn bản verbatim, do lần gọi WebFetch đầu tiên trả về bản tóm tắt qua model trung gian (không phải nguyên văn) cho 3/4 file — không dùng bản tóm tắt đó làm bằng chứng cho phân tích văn phong chi tiết (từ ngữ, dấu câu, cấu trúc bảng).
- Toàn bộ finding trên trích trực tiếp từ văn bản gốc đã đọc toàn văn; không suy diễn từ kiến thức nền về Superpowers.
