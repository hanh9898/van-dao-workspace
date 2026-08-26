# Digest R1.1 — Cấu trúc & giao thức skill của Superpowers (obra)

**Chủ đề:** Kỹ thuật viết skill Claude Code của framework "Superpowers" (obra/superpowers), phục vụ quyết định viết SKILL.md cho Vấn Đạo.
**Phạm vi câu hỏi:** Cấu trúc & giao thức skill — plugin.json, using-superpowers (entry point), writing-skills (skill viết skill), triết lý README/CLAUDE.md.
**Phương pháp:** Kéo trực tiếp nội dung nguyên văn qua WebFetch từ raw.githubusercontent.com (branch `main`), không suy đoán, không dùng tóm tắt thứ cấp. Cả 5 URL đều fetch thành công ở lần thử đầu tiên (không cần fallback branch/URL khác).
**Ngày truy cập:** 2026-08-25

---

## 1. `.claude-plugin/plugin.json` — khai báo gì?

**Nội dung nguyên văn (toàn bộ file):**
```json
{
  "name": "superpowers",
  "description": "Core skills library for Claude Code: TDD, debugging, collaboration patterns, and proven techniques",
  "version": "6.3.0",
  "author": {
    "name": "Jesse Vincent",
    "email": "jesse@fsck.com"
  },
  "homepage": "https://github.com/obra/superpowers",
  "repository": "https://github.com/obra/superpowers",
  "license": "MIT",
  "keywords": [
    "skills",
    "tdd",
    "debugging",
    "collaboration",
    "best-practices",
    "workflows"
  ]
}
```

### Findings

- {claim: "plugin.json của Superpowers KHÔNG liệt kê danh sách skill tường minh (không có field `skills` hay `commands` trỏ tới từng skill) — nó chỉ khai báo metadata cấp plugin: name, description, version (6.3.0), author, homepage, repository, license, keywords.", source: "https://raw.githubusercontent.com/obra/superpowers/main/.claude-plugin/plugin.json", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Việc khám phá skill không đến từ plugin.json mà ngụ ý đến từ cấu trúc thư mục `skills/<skill-name>/SKILL.md` theo namespace phẳng (flat namespace) — plugin.json chỉ đóng vai trò manifest nhận diện plugin (tên, version, license) cho hệ thống marketplace/registry.", source: "https://raw.githubusercontent.com/obra/superpowers/main/.claude-plugin/plugin.json", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "medium", class: "pattern"}

---

## 2. `skills/using-superpowers/SKILL.md` — có phải "cổng vào" (entry point)?

**Frontmatter nguyên văn:**
```yaml
---
name: using-superpowers
description: Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions
---
```

**Nội dung chính (trích nguyên văn các đoạn quan trọng):**

> "If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill. IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT. This is not negotiable. You cannot rationalize your way out of this."

> "**Invoke relevant or requested skills BEFORE any response or action** — including clarifying questions, exploring the codebase, or checking files."

> "Then announce \"Using [skill] to [purpose]\" and follow the skill exactly. If it has a checklist, create a todo per item."

Có bảng "Red Flags" liệt kê 12 lối suy nghĩ ngụy biện ("This is just a simple question", "I need more context first", "I can check git/files quickly", v.v.) kèm phản bác từng cái. Có phần "Skill Priority" (process skills đi trước implementation skills — vd. brainstorming/systematic-debugging trước). Có phần "Platform Adaptation" trỏ tới file tham chiếu riêng cho từng harness (Codex, Pi, Antigravity, Hermes Agent). Kết thúc bằng "User Instructions": CLAUDE.md/AGENTS.md/GEMINI.md và yêu cầu trực tiếp của người dùng có ưu tiên cao hơn skill, skill có ưu tiên cao hơn hành vi mặc định.

### Findings

- {claim: "using-superpowers là skill 'bootstrap/gatekeeper' được kích hoạt khi bắt đầu MỌI hội thoại (description: 'Use when starting any conversation'), có vai trò bắt buộc kiểm tra và gọi skill liên quan TRƯỚC bất kỳ phản hồi hay hành động nào, kể cả câu hỏi làm rõ — đây đúng là cơ chế 'cổng vào' (entry point) của framework.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/using-superpowers/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "using-superpowers không liệt kê danh sách các skill cụ thể để điều hướng — nó không phải một 'menu' trỏ tới từng skill theo tên, mà là một quy tắc hành vi (behavioral rule) buộc agent tự tìm và gọi skill phù hợp bất cứ khi nào có xác suất dù chỉ 1% là skill đó áp dụng được.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/using-superpowers/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Cơ chế điều hướng chính là bảng 'Red Flags' — 12 dòng suy nghĩ ngụy biện phổ biến (vd. 'This is just a simple question', 'I need more context first', 'This doesn't need a formal skill') mỗi dòng kèm phản bác ('Reality') để chặn agent bỏ qua bước kiểm tra skill.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/using-superpowers/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Có quy tắc thứ tự ưu tiên rõ ràang giữa các skill: 'process skills come first' (vd. brainstorming, systematic-debugging) rồi mới đến 'implementation skills' (vd. frontend-design) — ví dụ cụ thể: 'Let's build X' → brainstorming trước, rồi mới skill triển khai; 'Fix this bug' → systematic-debugging trước, rồi mới domain skills.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/using-superpowers/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Skill có cơ chế thích ứng đa nền tảng (Platform Adaptation): nếu harness là Codex/Pi/Antigravity/Hermes Agent thì đọc thêm file tham chiếu riêng trong `references/<harness>-tools.md`.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/using-superpowers/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Thứ tự ưu tiên tổng thể: user instructions (CLAUDE.md/AGENTS.md/GEMINI.md, yêu cầu trực tiếp) > skills > default behavior; chỉ được bỏ qua skill workflow khi 'human partner' đã nói rõ ràng.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/using-superpowers/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Có khối cảnh báo đặc biệt dành cho subagent: '<SUBAGENT-STOP> If you were dispatched as a subagent to execute a specific task, ignore this skill. </SUBAGENT-STOP>' — nghĩa là quy tắc bootstrap này chỉ áp dụng cho agent chính, không áp cho subagent được dispatch làm việc cụ thể.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/using-superpowers/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

---

## 3. `skills/writing-skills/SKILL.md` — quy định thế nào là SKILL.md tốt (quan trọng nhất)

**Frontmatter nguyên văn:**
```yaml
---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
---
```

### 3.1. Nguyên lý cốt lõi
> "**Writing skills IS Test-Driven Development applied to process documentation.**"
> "**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing."
> "**REQUIRED BACKGROUND:** You MUST understand superpowers:test-driven-development before using this skill."

Định nghĩa: "A **skill** is a reference guide for proven techniques, patterns, or tools." — "Skills are: Reusable techniques, patterns, tools, reference guides" / "Skills are NOT: Narratives about how you solved a problem once".

### 3.2. Bảng ánh xạ TDD → viết skill
| TDD Concept | Skill Creation |
|---|---|
| Test case | Pressure scenario với subagent |
| Production code | Skill document (SKILL.md) |
| Test fails (RED) | Agent vi phạm rule khi CHƯA có skill (baseline) |
| Test passes (GREEN) | Agent tuân thủ khi CÓ skill |
| Refactor | Đóng lỗ hổng (loopholes) trong khi vẫn giữ compliance |

### 3.3. Khi nào tạo skill / không tạo skill
Tạo khi: kỹ thuật không hiển nhiên trực giác; sẽ dùng lại xuyên project; pattern áp dụng rộng; người khác cũng hưởng lợi.
Không tạo cho: giải pháp một lần; thực hành chuẩn đã có tài liệu; quy ước riêng của project (đưa vào instructions file); ràng buộc cơ học có thể tự động hoá bằng regex/validation.

### 3.4. Ba loại skill
Technique (phương pháp cụ thể có bước), Pattern (cách tư duy về vấn đề), Reference (tài liệu API/cú pháp/tool).

### 3.5. Cấu trúc thư mục
```
skills/
  skill-name/
    SKILL.md              # Main reference (required)
    supporting-file.*     # Only if needed
```
"**Flat namespace** - all skills in one searchable namespace". File riêng chỉ cho: (1) heavy reference (100+ dòng), (2) reusable tools (scripts, templates). Mọi thứ khác (principles, code < 50 dòng) giữ inline.

### 3.6. Cấu trúc SKILL.md chuẩn (khung mẫu nguyên văn)
Frontmatter YAML bắt buộc 2 field `name` và `description` (tối đa 1024 ký tự tổng, theo agentskills.io/specification). `name`: chỉ chữ, số, gạch ngang (không ngoặc/ký tự đặc biệt). `description`: ngôi thứ ba, CHỈ mô tả điều kiện kích hoạt (KHÔNG mô tả skill làm gì), bắt đầu bằng "Use when...", nêu triệu chứng/tình huống cụ thể, dưới 500 ký tự nếu có thể, KHÔNG BAO GIỜ tóm tắt quy trình/workflow của skill.

Khung mẫu file:
```markdown
---
name: Skill-Name-With-Hyphens
description: Use when [specific triggering conditions and symptoms]
---

# Skill Name

## Overview
What is this? Core principle in 1-2 sentences.

## When to Use
[Small inline flowchart IF decision non-obvious]
Bullet list with SYMPTOMS and use cases
When NOT to use

## Core Pattern (for techniques/patterns)
Before/after code comparison

## Quick Reference
Table or bullets for scanning common operations

## Implementation
Inline code for simple patterns
Link to file for heavy reference or reusable tools

## Common Mistakes
What goes wrong + fixes

## Real-World Impact (optional)
Concrete results
```

### 3.7. Skill Discovery Optimization (SDO) — phần quan trọng nhất
**Quy tắc trọng tâm: Description = When to Use, KHÔNG PHẢI What the Skill Does.**

Bằng chứng thực nghiệm được nêu trực tiếp trong skill: "Testing revealed that when a description summarizes the skill's workflow, an agent may follow the description instead of reading the full skill content. A description saying 'code review between tasks' caused an agent to do ONE review, even though the skill's flowchart clearly showed TWO reviews... When the description was changed to just 'Use when executing implementation plans with independent tasks' (no workflow summary), the agent correctly read the flowchart and followed the two-stage review process."

"**The trap:** Descriptions that summarize workflow create a shortcut agents will take. The skill body becomes documentation agents skip."

Ví dụ đối chiếu Bad/Good nguyên văn:
```yaml
# ❌ BAD: Summarizes workflow - agents may follow this instead of reading skill
description: Use when executing plans - dispatches subagent per task with code review between tasks

# ✅ GOOD: Just triggering conditions, no workflow summary
description: Use when executing implementation plans with independent tasks in the current session
```

Nội dung description nên: dùng trigger/triệu chứng cụ thể; mô tả VẤN ĐỀ (race conditions) chứ không phải triệu chứng đặc thù ngôn ngữ (setTimeout); giữ trigger công nghệ-trung lập trừ khi skill vốn đặc thù công nghệ; viết ngôi thứ ba (vì bị nhúng vào system prompt).

**Keyword coverage**: dùng từ agent sẽ tìm kiếm — error message, triệu chứng, từ đồng nghĩa, tên tool/lệnh cụ thể.

**Đặt tên mô tả**: dùng active voice, verb-first, dạng gerund (-ing) cho quy trình — vd. `creating-skills`, `condition-based-waiting` thay vì `skill-creation`, `async-test-helpers`.

**Token efficiency (quan trọng)**: skill loại "getting-started"/thường xuyên tải phải < 150 từ mỗi cái; skill tải thường xuyên khác < 200 từ tổng; skill khác < 500 từ. Có kỹ thuật: trỏ chi tiết flag ra `--help` thay vì liệt kê hết trong SKILL.md; dùng cross-reference thay vì lặp lại workflow; nén ví dụ; loại bỏ trùng lặp.

**Cross-referencing skill khác**: dùng tên skill kèm marker rõ ràng, VD: `**REQUIRED SUB-SKILL:** Use superpowers:test-driven-development`. TUYỆT ĐỐI KHÔNG dùng `@` link vì "`@` syntax force-loads files immediately, consuming 200k+ context before you need them."

### 3.8. Flowchart
Chỉ dùng flowchart (dot/graphviz) inline khi: điểm quyết định không hiển nhiên, có vòng lặp quy trình dễ dừng sớm, hoặc quyết định "dùng A hay B". KHÔNG dùng flowchart cho: tài liệu tham chiếu (dùng bảng/list), code example (dùng markdown block), hướng dẫn tuyến tính (dùng numbered list), nhãn không có ý nghĩa ngữ nghĩa (step1, helper2).

### 3.9. "The Iron Law" (Luật sắt)
> "NO SKILL WITHOUT A FAILING TEST FIRST" — áp dụng cho cả skill MỚI và CHỈNH SỬA skill hiện có. "Write skill before testing? Delete it. Start over." Không có ngoại lệ cho "simple additions", "documentation updates".

### 3.10. "Match the Form to the Failure" — chọn đúng dạng hướng dẫn theo loại lỗi
Bảng đối chiếu (nguyên văn ý chính):
| Loại lỗi baseline | Dạng đúng | Dạng sai |
|---|---|---|
| Bỏ/vi phạm rule dưới áp lực (biết luật vẫn phá) | Prohibition + rationalization table + red flags | Hướng dẫn mềm ("prefer...", "consider...") |
| Tuân thủ nhưng output sai hình dạng | Recipe/contract tích cực: nói rõ output LÀ gì | Danh sách cấm ("don't restate", "never narrate") |
| Bỏ sót phần bắt buộc trong output đã có | Structural: field/slot REQUIRED trong template | Prose reminder gần template |
| Hành vi phụ thuộc điều kiện | Conditional theo predicate quan sát được | Rule vô điều kiện + exemption clause |

Bằng chứng dẫn: trong test A/B về dispatch-prompt guidance, "prohibition arm produced clearly more of the unwanted content than the recipe arm... and trended worse than even the no-guidance control." Quy tắc bổ sung: "No nuance clauses" (thêm 1 clause ngoại lệ làm suy giảm recipe từ consistent xuống noisy); "Exemption clauses don't scope" (loại trừ không thực sự cô lập được phần cần loại trừ).

### 3.11. Bulletproofing chống ngụy biện (rationalization)
Phạm vi: chỉ áp dụng cho "discipline failures" (agent biết luật nhưng vẫn phá dưới áp lực) — KHÔNG dùng prohibition cho lỗi sai-hình-dạng output.
Kỹ thuật: đóng từng lỗ hổng tường minh (không chỉ nói rule mà cấm cả workaround cụ thể, vd "Don't keep it as 'reference'"); thêm nguyên lý nền tảng sớm ("Violating the letter of the rules is violating the spirit of the rules."); xây bảng Rationalization (Excuse → Reality); tạo danh sách Red Flags để agent tự kiểm tra.

### 3.12. Micro-test wording trước khi chạy full pressure scenario
5 bước: 1 sample/lời gọi fresh-context; LUÔN có no-guidance control; 5+ reps mỗi biến thể; đọc thủ công từng match được gắn cờ (không chỉ đếm tự động); "Variance is a metric" — guidance tốt thì 5 reps hội tụ cùng shape, 5 cách hiểu khác nhau nghĩa là wording chưa chặt.

### 3.13. RED-GREEN-REFACTOR cho skill
RED: chạy pressure scenario với subagent KHÔNG có skill, ghi lại nguyên văn lựa chọn/ngụy biện. GREEN: viết skill tối thiểu giải quyết đúng những ngụy biện đó, chạy lại thấy compliance. REFACTOR: agent tìm ngụy biện mới → thêm counter → test lại tới khi bulletproof.

### 3.14. Testing theo loại skill
4 loại: Discipline-Enforcing (TDD, verification-before-completion) test bằng pressure scenario kết hợp nhiều áp lực; Technique Skills test bằng application/variation scenario; Pattern Skills test bằng recognition/counter-example; Reference Skills test bằng retrieval/gap testing.

### 3.15. Anti-patterns nguyên văn
"❌ Narrative Example" (quá cụ thể, không tái sử dụng được), "❌ Multi-Language Dilution" (chất lượng trung bình, gánh nặng bảo trì), "❌ Code in Flowcharts" (không copy-paste được), "❌ Generic Labels" (helper1, step3 thiếu ý nghĩa ngữ nghĩa).

### 3.16. Checklist triển khai (TDD Adapted) — đầy đủ các mục RED/GREEN/REFACTOR/Quality/Deployment, bao gồm: name chỉ chữ-số-gạch ngang; description bắt đầu "Use when..." ngôi thứ ba; guidance form khớp loại lỗi; wording micro-tested (N/A cho reference thuần); code inline hoặc link file riêng; một ví dụ xuất sắc (không đa ngôn ngữ); commit git + push fork; cân nhắc PR ngược.

### Findings

- {claim: "Nguyên lý cốt lõi của writing-skills: 'Writing skills IS Test-Driven Development applied to process documentation' — quy trình viết skill bắt buộc theo chu trình RED-GREEN-REFACTOR giống hệt TDD viết code, với 'Iron Law': NO SKILL WITHOUT A FAILING TEST FIRST, áp dụng cho cả skill mới lẫn chỉnh sửa skill cũ.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Quy tắc quan trọng nhất về field `description` trong frontmatter: nó CHỈ được mô tả điều kiện kích hoạt (khi nào dùng), TUYỆT ĐỐI KHÔNG được tóm tắt quy trình/workflow của skill — vì có bằng chứng thực nghiệm cho thấy khi description tóm tắt workflow, agent sẽ làm theo mô tả rút gọn đó thay vì đọc và tuân theo nội dung đầy đủ của skill (dẫn ví dụ cụ thể về việc agent chỉ review 1 lần thay vì 2 lần vì description tóm tắt sai).", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Frontmatter chỉ cần 2 field bắt buộc: `name` (chỉ chữ/số/gạch ngang) và `description` (bắt đầu bằng 'Use when...', ngôi thứ ba, dưới 500 ký tự nếu có thể), tổng frontmatter tối đa 1024 ký tự theo chuẩn agentskills.io/specification.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Cấu trúc thư mục dùng 'flat namespace' (`skills/skill-name/SKILL.md`), file phụ riêng chỉ khi cần heavy reference (100+ dòng) hoặc reusable tool (script/template) — mọi nguyên lý/pattern/code dưới 50 dòng thì giữ inline trong SKILL.md.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Cấm tuyệt đối dùng cú pháp `@` để cross-reference skill khác vì nó force-load toàn bộ file ngay lập tức, tốn 200k+ token context trước khi thực sự cần — thay vào đó dùng marker tường minh dạng '**REQUIRED SUB-SKILL:** Use superpowers:test-driven-development'.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Có quy tắc giới hạn độ dài nghiêm ngặt theo loại skill: skill 'getting-started'/tải mỗi conversation phải dưới 150 từ mỗi cái; skill tải thường xuyên khác dưới 200 từ tổng; skill khác dưới 500 từ — kèm kỹ thuật cụ thể để nén (trỏ ra --help, cross-reference thay vì lặp, nén ví dụ).", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Framework có nguyên tắc 'Match the Form to the Failure': dạng hướng dẫn (prohibition list vs. recipe/contract tích cực vs. structural required-field vs. conditional) phải khớp với LOẠI lỗi baseline quan sát được — dùng sai dạng có thể phản tác dụng, có bằng chứng A/B test cụ thể rằng prohibition-based guidance làm tệ hơn cả việc không có guidance nào khi vấn đề là 'output sai hình dạng' chứ không phải 'vi phạm rule dưới áp lực'.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Kỹ thuật 'bulletproofing' chống ngụy biện (rationalization) chỉ áp dụng cho discipline-enforcing skills (agent biết luật nhưng vẫn phá dưới áp lực), gồm: đóng lỗ hổng tường minh (cấm cả workaround, không chỉ nói rule), câu nguyên lý nền 'Violating the letter of the rules is violating the spirit of the rules', bảng Rationalization (Excuse→Reality), và danh sách Red Flags.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Trước khi chạy pressure-scenario testing tốn kém, framework khuyến nghị 'micro-test wording' trước: 1 sample/call fresh-context, luôn có no-guidance control, tối thiểu 5 reps mỗi biến thể, đọc thủ công từng kết quả (không chỉ đếm tự động vì template echo/counter-example giả mạo hit), và coi 'variance' (độ phân tán giữa các reps) như một chỉ số đánh giá độ chặt của wording.", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Flowchart (graphviz/dot) chỉ dùng inline cho điểm quyết định không hiển nhiên hoặc lựa chọn A-vs-B — KHÔNG dùng cho tài liệu tham chiếu, code example, hướng dẫn tuyến tính, hay nhãn vô nghĩa (step1, helper2).", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Quy trình tạo skill có checklist bắt buộc theo pha RED (viết pressure scenario, chạy baseline không có skill, ghi ngụy biện) → GREEN (viết skill tối thiểu giải quyết đúng ngụy biện đã ghi, chạy lại xác nhận compliance) → REFACTOR (tìm ngụy biện mới, thêm counter, re-test tới khi bulletproof) → Deployment (commit git, cân nhắc PR ngược).", source: "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

---

## 4. README.md và CLAUDE.md — triết lý tổng thể

### 4.1. README.md

**Mô tả framework (nguyên văn):**
> "Superpowers is a complete software development methodology for your coding agents, built on top of a set of composable skills and some initial instructions that make sure your agent uses them."

**Cách vận hành (nguyên văn tóm lược từ phần "How it works"):** Agent không nhảy vào viết code ngay — nó dừng lại hỏi người dùng thực sự muốn gì; sau khi có spec, trình bày theo từng phần ngắn để dễ đọc; sau khi thiết kế được duyệt, lập implementation plan đủ rõ ràng cho "an enthusiastic junior engineer with poor taste, no judgement, no project context, and an aversion to testing" có thể theo; nhấn mạnh TDD đỏ/xanh thật, YAGNI, DRY; khi người dùng nói "go", khởi động "subagent-driven-development" — agent làm việc tự động vài giờ không lệch khỏi kế hoạch.

**The Basic Workflow (7 bước, trích nguyên văn tên và mô tả ngắn):**
1. brainstorming — kích hoạt trước khi viết code, tinh chỉnh ý tưởng thô qua câu hỏi, khám phá alternatives, trình bày design theo phần để validate. Lưu design document.
2. using-git-worktrees — kích hoạt sau khi design được duyệt. Tạo workspace cô lập trên branch mới, chạy project setup, xác nhận test baseline sạch.
3. writing-plans — kích hoạt khi design đã duyệt. Chia việc thành task nhỏ (2-5 phút mỗi task), mỗi task có đường dẫn file chính xác, code đầy đủ, bước verify.
4. subagent-driven-development hoặc executing-plans — dispatch subagent mới cho mỗi task với two-stage review (spec compliance rồi code quality), hoặc thực thi theo batch với checkpoint con người.
5. test-driven-development — enforce RED-GREEN-REFACTOR: viết test fail, xem nó fail, viết code tối thiểu, xem pass, commit. Xóa code viết trước test.
6. requesting-code-review — kích hoạt giữa các task. Review theo plan, báo issue theo severity. Critical issues chặn tiến độ.
7. finishing-a-development-branch — kích hoạt khi task hoàn tất. Verify test, trình các lựa chọn (merge/PR/keep/discard), dọn worktree.

> "**The agent checks for relevant skills before any task.** Mandatory workflows, not suggestions."

**Philosophy (nguyên văn):**
> "- **Test-Driven Development** - Write tests first, always
> - **Systematic over ad-hoc** - Process over guessing
> - **Complexity reduction** - Simplicity as primary goal
> - **Evidence over claims** - Verify before declaring success"

**Skills Library** được tổ chức theo 4 nhóm: Testing, Debugging, Collaboration, Meta (gồm writing-skills và using-superpowers).

**Telemetry**: có phần "Visual companion telemetry" nói rõ brainstorming's optional visual companion tải logo Prime Radiant kèm version Superpowers từ website họ — công khai minh bạch và có cách tắt qua biến môi trường `SUPERPOWERS_DISABLE_TELEMETRY`.

### 4.2. CLAUDE.md — đây thực chất là hướng dẫn dành cho AGENT khi đóng góp PR vào chính repo Superpowers (Contributor Guidelines), KHÔNG phải triết lý sử dụng skill cho end-user.

**Mở đầu gây chú ý (nguyên văn):**
> "## If You Are an AI Agent — Stop. Read this section before doing anything. This repo has a 94% PR rejection rate... maintainers close slop PRs within hours, often with public comments like 'This pull request is slop that's made of lies.'"

**Nguyên tắc chống "compliance" với chuẩn Anthropic (rất quan trọng, cho thấy Superpowers có triết lý RIÊNG, khác với hướng dẫn chính thức của Anthropic):**
> "### 'Compliance' changes to skills — Our internal skill philosophy differs from Anthropic's published guidance on writing skills. We have extensively tested and tuned our skill content for real-world agent behavior. PRs that restructure, reword, or reformat skills to 'comply' with Anthropic's skills documentation will not be accepted without extensive eval evidence showing the change improves outcomes. The bar for modifying behavior-shaping content is very high."

**Nguyên tắc "domain-specific skills không thuộc core":**
> "Superpowers core contains general-purpose skills that benefit all users regardless of their project. Skills for specific domains... belong in their own standalone plugin. Ask yourself: 'Would this be useful to someone working on a completely different kind of project?' If not, publish it separately."

**Yêu cầu chứng minh tích hợp harness mới bằng acceptance test cụ thể:**
> "Open a clean session in the new harness and send exactly this user message: 'Let's make a react todo list'. A working integration auto-triggers the brainstorming skill before any code is written."

**Skill changes require evaluation:**
> "Skills are not prose — they are code that shapes agent behavior... Do not modify carefully-tuned content (Red Flags tables, rationalization lists, 'human partner' language) without evidence the change is an improvement."

**Thuật ngữ có chủ đích:** "Superpowers has its own tested philosophy about skill design, agent behavior shaping, and terminology (e.g., 'your human partner' is deliberate, not interchangeable with 'the user')."

### Findings

- {claim: "README.md định nghĩa Superpowers là 'a complete software development methodology... built on top of a set of composable skills and some initial instructions that make sure your agent uses them' — tức framework tự mô tả gồm hai lớp: (1) tập skill có thể kết hợp (composable), (2) instruction khởi động (using-superpowers) đảm bảo agent thực sự dùng chúng.", source: "https://raw.githubusercontent.com/obra/superpowers/main/README.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Quy trình cơ bản (Basic Workflow) của Superpowers gồm 7 skill tuần tự: brainstorming → using-git-worktrees → writing-plans → subagent-driven-development/executing-plans → test-driven-development → requesting-code-review → finishing-a-development-branch, và framework khẳng định 'The agent checks for relevant skills before any task. Mandatory workflows, not suggestions.'", source: "https://raw.githubusercontent.com/obra/superpowers/main/README.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Bốn trụ triết lý được README nêu tường minh: Test-Driven Development (write tests first, always), Systematic over ad-hoc (process over guessing), Complexity reduction (simplicity as primary goal), Evidence over claims (verify before declaring success).", source: "https://raw.githubusercontent.com/obra/superpowers/main/README.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "CLAUDE.md của repo Superpowers thực chất là Contributor Guidelines dành cho agent AI muốn gửi PR vào chính repo này (không phải tài liệu triết lý sử dụng skill cho end-user) — mở đầu bằng cảnh báo tỷ lệ từ chối PR 94% và yêu cầu agent tự kiểm tra 6 điều kiện trước khi mở PR.", source: "https://raw.githubusercontent.com/obra/superpowers/main/CLAUDE.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "CLAUDE.md xác nhận tường minh rằng triết lý viết skill của Superpowers KHÁC với hướng dẫn chính thức của Anthropic về writing skills, và PR nào cố 'compliance-hoá' skill theo tài liệu Anthropic sẽ bị từ chối trừ khi có bằng chứng eval cụ thể cho thấy cải thiện outcome — đây là điểm đối chiếu quan trọng khi so với BMAD-METHOD (BMAD tuân theo chuẩn khác, còn Superpowers cố tình lệch khỏi chuẩn Anthropic dựa trên eval thực nghiệm riêng).", source: "https://raw.githubusercontent.com/obra/superpowers/main/CLAUDE.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "CLAUDE.md coi skill là 'code that shapes agent behavior' chứ không phải văn xuôi (prose), và cấm sửa nội dung đã tinh chỉnh kỹ (Red Flags tables, rationalization lists, thuật ngữ 'your human partner') nếu không có bằng chứng cải thiện — củng cố nguyên tắc trong writing-skills rằng mọi thay đổi content định hình hành vi phải qua eval trước khi merge.", source: "https://raw.githubusercontent.com/obra/superpowers/main/CLAUDE.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "CLAUDE.md yêu cầu skill/domain cụ thể (không tổng quát cho mọi project) không được đưa vào core repo mà phải publish thành plugin riêng — phép thử: 'Would this be useful to someone working on a completely different kind of project? If not, publish it separately.'", source: "https://raw.githubusercontent.com/obra/superpowers/main/CLAUDE.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}
- {claim: "Việc tích hợp harness mới phải được chứng minh bằng bài test chấp nhận cụ thể: gửi đúng câu 'Let\\'s make a react todo list' vào session sạch và brainstorming skill phải tự kích hoạt trước khi có bất kỳ dòng code nào được viết — đây là tiêu chí khách quan để xác nhận cơ chế auto-trigger hoạt động thật (không phải chỉ có file skill nằm trên đĩa).", source: "https://raw.githubusercontent.com/obra/superpowers/main/CLAUDE.md", publisher: "GitHub (obra/superpowers)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

---

## Không tìm thấy / Giới hạn

- Không xác định được ngày commit cuối (pub_date) của từng file vì WebFetch trên raw.githubusercontent.com không trả về header/metadata Git; tất cả finding đánh dấu `pub_date: "N/A"`. (Có thể bổ sung sau bằng `gh api repos/obra/superpowers/commits?path=<file>` nếu cần độ chính xác cao hơn.)
- Cả 5 URL đều fetch thành công ngay lần đầu trên branch `main` — không cần thử fallback `master` hay `github.com/.../blob/...`.
- Không có mục nào trong 4 câu hỏi bị thiếu dữ liệu; toàn bộ nội dung được lấy trực tiếp nguyên văn từ nguồn gốc.

---

## Đối chiếu nhanh với BMAD-METHOD (ghi chú định hướng cho bước tổng hợp sau — KHÔNG phải finding có nguồn, chỉ là gợi ý điều hướng)

Các điểm sau đây là quan sát cấu trúc, cần được xác nhận lại bằng digest nghiên cứu BMAD trước đó, không tự suy diễn ở đây:
- Superpowers dùng plugin.json tối giản (chỉ metadata), không khai báo danh sách skill tường minh — khác cách BMAD tổ chức workflow/skill (cần đối chiếu với digest BMAD).
- Superpowers có 1 skill "entry point" hành vi (using-superpowers) ép buộc agent tự quét toàn bộ skill khả dụng theo % xác suất áp dụng, thay vì router tường minh.
- Superpowers coi việc viết skill là một quy trình TDD hoàn chỉnh với eval bằng subagent pressure-testing — đây là điểm đặc trưng mạnh, khác biệt rõ với cách tiếp cận "viết tài liệu rồi review thủ công" phổ biến.
- Superpowers công khai tuyên bố lệch khỏi chuẩn Anthropic chính thức về skill — cần lưu ý khi Vấn Đạo cân nhắc giữa "theo chuẩn chính thức" hay "tối ưu theo eval thực nghiệm riêng".
