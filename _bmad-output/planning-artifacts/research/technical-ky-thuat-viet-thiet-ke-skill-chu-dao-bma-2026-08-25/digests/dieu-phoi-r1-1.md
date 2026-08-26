# Digest — Dimension 3: Điều phối subagent

Nguồn đã đọc trực tiếp (toàn bộ nội dung, không phải trích đoạn):
- `.claude/skills/bmad-deep-recon/SKILL.md`
- `.claude/skills/bmad-deep-recon/references/run.md`
- `.claude/skills/bmad-prd/SKILL.md`
- `.claude/skills/bmad-architecture/references/reviewer-gate.md`
- `.claude/skills/bmad-review/SKILL.md`

---

## Câu hỏi 1 — "Research firewall": định nghĩa và ranh giới

{claim: "Đoạn văn định nghĩa chính xác nguyên tắc firewall: 'The research firewall. Project context — briefs, PRDs, code, memory, {workflow.persistent_facts} — shapes what to ask, never what is true. It is inadmissible as evidence: every claim in a research artifact traces to a digest or import file with a source. Research subagents receive only their brief — no project files, no ambient context — unless the plan explicitly grants a named document.'", source: ".claude/skills/bmad-deep-recon/SKILL.md:17", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Firewall được nêu là một trong hai 'standing rules' epistemics kế thừa nguyên văn (verbatim) bởi mọi subagent mà Deep Recon spawn ra.", source: ".claude/skills/bmad-deep-recon/SKILL.md:14", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Ở tầng thực thi (run.md), firewall được nhắc lại và cụ thể hoá cho fan-out: 'Each assistant runs behind the research firewall: it gets its brief and nothing else — no project files, no ambient context.'", source: ".claude/skills/bmad-deep-recon/references/run.md:45", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Brief gửi cho subagent nghiên cứu gồm các thành phần cố định: câu hỏi nó sở hữu + quyết định phục vụ + topic; search surfaces và nguồn ưu tiên/cấm; craft nguồn và ngưỡng freshness của pack; ngân sách nguồn và tool-call; craft truy vấn; và nguyên tắc epistemics nguyên văn cộng 'return contract'.", source: ".claude/skills/bmad-deep-recon/references/run.md:45-52", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prd không dùng cụm từ 'research firewall', nhưng áp dụng nguyên tắc cô lập context tương tự dưới tên 'extract, don't ingest' cho subagent trích xuất tài liệu nguồn — khác về tên gọi và phạm vi (không phải research web) so với deep-recon.", source: ".claude/skills/bmad-prd/SKILL.md:67", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "medium", class: "pattern"}

{claim: "bmad-architecture/reviewer-gate.md và bmad-review/SKILL.md không dùng thuật ngữ 'research firewall' hay định nghĩa ranh giới project-context tương tự cho subagent reviewer — cụm từ và định nghĩa này chỉ thấy ở bmad-deep-recon.", source: ".claude/skills/bmad-architecture/references/reviewer-gate.md (toàn file); .claude/skills/bmad-review/SKILL.md (toàn file)", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

---

## Câu hỏi 2 — "Digest contract": hình dạng cố định, trường bắt buộc

{claim: "Digest contract của Deep Recon có hình dạng cố định theo trường: mỗi finding là một claim với các trường bắt buộc {claim, source, publisher, pub_date, accessed, confidence, class}, cộng thêm 'leads worth chasing' và 'what it looked for and could not find' như một phần của return contract cho mỗi subagent.", source: ".claude/skills/bmad-deep-recon/references/run.md:52", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Nguyên tắc nền cho digest: 'A claim is a sentence with a source. Publisher, publication date, access date. No naked numbers.' — giải thích lý do các trường publisher/pub_date/accessed là bắt buộc, không phải tùy chọn.", source: ".claude/skills/bmad-deep-recon/SKILL.md:23", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Digest phải được ghi ra file ngay khi trả về, trước khi làm bất cứ điều gì khác với nó: 'On each return, write the digest to {doc_workspace}/digests/ before doing anything else with it.' — quy tắc thứ tự thao tác, không chỉ vị trí lưu.", source: ".claude/skills/bmad-deep-recon/references/run.md:54", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Quy ước đặt tên file digest cố định: 'one file per assistant per round (<dimension>-r<round>-<n>.md)', và digest phải 'raw enough to re-derive from' (đủ thô để tái suy luận lại được).", source: ".claude/skills/bmad-deep-recon/references/run.md:28", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Ở các skill khác (bmad-prd Reviewer Gate, bmad-architecture reviewer-gate.md, bmad-review), 'return contract' của subagent có hình dạng KHÁC digest contract của deep-recon: không phải {claim, source, publisher, pub_date, accessed, confidence, class} mà là 'verdict, top 2-5 findings, file path' cho reviewer subagent — tức digest contract theo trường claim/source cụ thể chỉ thấy ở bmad-deep-recon, không phải một khuôn cố định xuyên toàn bộ BMAD.", source: ".claude/skills/bmad-prd/SKILL.md:77; .claude/skills/bmad-architecture/references/reviewer-gate.md:9", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-review định nghĩa một 'return contract' thứ ba, khác cả hai trên: mỗi finding từ lens mang các trường {lens, location, trigger_condition, guard_snippet, potential_consequence}, và subagent lens được ra lệnh 'Return ONLY your findings — no other output.'", source: ".claude/skills/bmad-review/SKILL.md:31,37-43", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Reconciliation subagent trong bmad-prd Finalize có contract riêng thứ tư: 'Each writes its extract to {doc_workspace}/reconcile-{slug}.md and returns ONLY a compact summary (input name, gaps 2-5, file path).'", source: ".claude/skills/bmad-prd/SKILL.md:88", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

---

## Câu hỏi 3 — "Extract, don't ingest": áp dụng cụ thể, parent tránh nạp gì

{claim: "Nguyên tắc nêu trực tiếp trong deep-recon: 'Extract, don't ingest. Raw reports and search results never enter the parent context whole; subagents return relevance-filtered digests, and the parent reads digest files JIT (just-in-time).'", source: ".claude/skills/bmad-deep-recon/SKILL.md:22", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prd nêu cùng tên nguyên tắc, áp dụng cho tài liệu nguồn thay vì kết quả web: 'Extract, don't ingest. Source documents go to subagents for extraction; the parent assembles from extracts. Only load source documents into the parent context wholesale when no subagents are available.' — đây là điều kiện dự phòng duy nhất được ghi nhận cho việc parent nạp toàn văn.", source: ".claude/skills/bmad-prd/SKILL.md:67", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Trong Update intent của bmad-prd, cùng cụm 'extract, don't ingest' được áp dụng cho việc đối chiếu tín hiệu thay đổi với PRD/addendum/.memlog.md/input gốc: 'Source-extract against PRD, addendum, .memlog.md, and original inputs (extract, don't ingest).'", source: ".claude/skills/bmad-prd/SKILL.md:34", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Cơ chế cụ thể parent tránh nạp: subagent reviewer 'writes its full review to {doc_workspace}/review-{slug}.md and returns ONLY a compact summary (verdict, top 2-5 findings, file path) — the parent never holds full review text.' Full text ở lại trên đĩa; chỉ tóm tắt vào context của parent.", source: ".claude/skills/bmad-prd/SKILL.md:77", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Cùng cơ chế lặp lại nguyên văn ở bmad-architecture reviewer-gate.md: '...returns ONLY a compact summary (verdict, top 2–5 findings, file path) — the parent never holds full review text. An inline self-check does not count: the independent context is the point, because a fresh reviewer finds the divergences the author talks past.' — câu sau giải thích LÝ DO triết học của việc không để parent tự review.", source: ".claude/skills/bmad-architecture/references/reviewer-gate.md:9", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Khi không có subagent khả dụng (fallback), quy tắc vẫn giữ kỷ luật thứ tự: 'run sequentially: write the file before anything else, then flush the review from working context' (bmad-prd) / 'run sequentially — write the file first, then flush it from context' (bmad-architecture) — tức ngay cả chạy tuần tự trong chính parent, parent vẫn phải ghi file rồi CHỦ ĐỘNG xoá khỏi working context thay vì giữ lại.", source: ".claude/skills/bmad-prd/SKILL.md:77; .claude/skills/bmad-architecture/references/reviewer-gate.md:9", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Nguyên tắc tổng quát bao trùm ở deep-recon: 'Nothing exists until it is a file. Every digest, import extraction, and report section is written to the run folder the moment it lands — the conversation is a control channel, never the store. A run that dies mid-flight resumes from disk with nothing lost.' — đây là lý do hệ thống của việc ghi-file-trước-rồi-mới-dùng.", source: ".claude/skills/bmad-deep-recon/SKILL.md:21", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-review áp dụng một biến thể khác của cô lập context không phải giữa parent-subagent mà giữa các lens với nhau: 'Run the independent lenses... Each sees the content and also_consider, never another lens's findings.' — các lens độc lập không được thấy kết quả của nhau, chỉ lens có 'after' mới nhận findings của lens trước.", source: ".claude/skills/bmad-review/SKILL.md:31-32", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "medium", class: "pattern"}

---

## Câu hỏi 4 — Dispatch song song nhiều subagent: quy tắc nhận/trả/ghi file

{claim: "Quy tắc fan-out của Deep Recon: 'Fan out researcher assistants for the round — concurrency per the resolved subagents level, split by the plan's topology: breadth-first gives each assistant independent sub-questions; depth-first gives each a distinct perspective or methodology on the same question; straightforward is one assistant with a small budget — never fan out what one focused assistant answers.'", source: ".claude/skills/bmad-deep-recon/references/run.md:45", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Mức độ song song (subagents) được định lượng theo preset: quick=2, standard=3 (mặc định), deep=6 (trần 10), và 'none'=0 (chạy tuần tự trong chính lead) khi không có subagent-harness.", source: ".claude/skills/bmad-deep-recon/references/run.md:9-15", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Ngân sách mỗi subagent được scale theo độ khó tác vụ, không đồng nhất: 'under 5 for a simple lookup, ~5 medium, ~10 hard, 15 for genuinely multi-part, 20 never exceeded. Either budget spent → synthesize what it has.'", source: ".claude/skills/bmad-deep-recon/references/run.md:50", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Model được chọn cho subagent theo thứ tự ưu tiên đã cấu hình: 'Spawn assistants on {workflow.subagent_models} when set (first available wins); otherwise the harness default — judgment work never drops to the smallest tier.'", source: ".claude/skills/bmad-deep-recon/references/run.md:56", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Quy tắc ghi file TRƯỚC khi làm gì khác với kết quả trả về là hằng số lặp lại xuyên các skill: deep-recon 'write the digest... before doing anything else with it' (run.md:54); bmad-prd fallback 'write the file before anything else' (SKILL.md:77); bmad-architecture fallback 'write the file first' (reviewer-gate.md:9).", source: ".claude/skills/bmad-deep-recon/references/run.md:54; .claude/skills/bmad-prd/SKILL.md:77; .claude/skills/bmad-architecture/references/reviewer-gate.md:9", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Vị trí ghi file được phân biệt có chủ đích giữa deliverable và scratch: bmad-architecture ghi review vào subfolder riêng '{doc_workspace}/reviews/review-{slug}.md — a subfolder, so the gate's scratch stays out of the deliverable folder', trong khi bmad-prd ghi trực tiếp '{doc_workspace}/review-{slug}.md' (không subfolder) — khác nhau về cấu trúc thư mục dù cùng pattern.", source: ".claude/skills/bmad-architecture/references/reviewer-gate.md:9; .claude/skills/bmad-prd/SKILL.md:77", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Trong bmad-review, dispatch song song từng lens là quy tắc rõ: 'When subagents are available, spawn one per lens in parallel: give it the lens instruction with {skill-root} and paths resolved absolute, the content or where to read it, any also_consider areas, the standing review directives, and the constraint \"Return ONLY your findings — no other output.\" Otherwise run the lenses sequentially yourself, completing one before starting the next.'", source: ".claude/skills/bmad-review/SKILL.md:31", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Findings được trình bày phân tầng, không đổ hết ra: 'Surface findings tiered, never dumped. Lead with a one-sentence gate verdict, then walk critical + high findings; medium/low roll into a single tail (\"plus N more in {file}\").' — lặp lại gần như nguyên văn ở cả bmad-prd và bmad-architecture, cho thấy đây là quy tắc trình bày chuẩn sau khi dispatch song song trả về.", source: ".claude/skills/bmad-prd/SKILL.md:79; .claude/skills/bmad-architecture/references/reviewer-gate.md:13", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Dispatch reviewer dùng 'standard prefix convention' để chỉ định lens/reviewer: bmad-prd và bmad-architecture đều nói 'using the standard prefix convention (skill: / file: / plain text)' cho các mục trong {workflow.finalize_reviewers}, và bmad-review dùng cùng quy ước prefix cho persistent_facts/review_guidance/style_guide.", source: ".claude/skills/bmad-prd/SKILL.md:77; .claude/skills/bmad-architecture/references/reviewer-gate.md:8; .claude/skills/bmad-review/SKILL.md:23,27", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Deep Recon cho phép chạy fan-out như một 'workflow' của harness khi có orchestration, nhưng khẳng định các quy tắc không đổi: 'The budgets, digest contract, firewall, and stopping rules apply unchanged — and however the acquisition parallelizes, digests land as files and the lead alone writes research.md, committing sections in plan order.' — chỉ LEAD được ghi báo cáo tổng hợp cuối, không phải subagent nào cũng ghi.", source: ".claude/skills/bmad-deep-recon/references/run.md:58", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

---

## Leads worth chasing

- `references/finalize.md`, `references/synthesis.md`, `references/verification.md`, `references/selection.md`, `references/draft.md`, `references/process.md`, `references/lifecycle.md` (đều được `.claude/skills/bmad-deep-recon/SKILL.md` trỏ tới nhưng CHƯA đọc trong lượt này) — có thể chứa thêm chi tiết về digest contract, verification level, và cách lead tổng hợp digest thành `research.md`.
- `.claude/skills/bmad-prd/references/validate.md` (được `SKILL.md:77,81` trỏ tới cho "prompt and output format" của rubric walker và pipeline tổng hợp HTML) — chưa đọc, có thể làm rõ thêm digest/summary contract của reviewer subagent.
- `customize.toml` của từng skill (deep-recon, prd, architecture, review) — chứa `finalize_reviewers`, `lenses`, `subagent_models`, `research_types` cụ thể; chưa đọc, cần để biết giá trị mặc định thực tế thay vì chỉ biến `{workflow.*}`.
- `_bmad/scripts/memlog.py` và `_bmad/scripts/recon_kit.py` — được gọi nhiều lần (`init`, `append`, `tally`, `slug`, `staleness`) nhưng chưa đọc mã nguồn; có thể có định nghĩa kỹ thuật hơn về việc parent/subagent ghi log ra sao.
- `.claude/skills/bmad-architecture/SKILL.md` (chưa đọc toàn văn, chỉ đọc `references/reviewer-gate.md`) — có thể có thêm ngữ cảnh về khi nào reviewer-gate được gọi và luồng dispatch subagent khác trong toàn bộ vòng đời skill.
- Các lens file riêng của bmad-review (`references/lens-*.md`) — chưa đọc; có thể có thêm chi tiết về "return ONLY your findings" và cấu trúc brief gửi cho từng lens.

## Không tìm thấy

- Không tìm thấy đoạn code/pseudo-code runtime nào thực sự "enforce" (thực thi kỹ thuật) research firewall — toàn bộ là hướng dẫn văn xuôi cho AI agent tự tuân thủ (prompt-level discipline), không phải cơ chế kỹ thuật (ví dụ sandbox, permission check) chặn subagent đọc project context.
- Không tìm thấy cụm "research firewall" hay "extract, don't ingest" xuất hiện trong `bmad-architecture/references/reviewer-gate.md` hay `bmad-review/SKILL.md` — hai file này dùng cơ chế tương đương ("parent never holds full review text", lens isolation) nhưng không đặt tên nguyên tắc giống deep-recon/prd.
- Không tìm thấy một "digest contract" DUY NHẤT áp dụng xuyên suốt toàn bộ BMAD — mỗi skill định nghĩa contract riêng cho mục đích của nó (deep-recon: {claim,source,publisher,pub_date,accessed,confidence,class} + leads + gaps; prd/architecture reviewer: verdict + top 2-5 findings + file path; review: {lens,location,trigger_condition,guard_snippet,potential_consequence}; prd reconcile: input name + gaps 2-5 + file path). Không nên khái quát hoá thành một khuôn chung.
- Không tìm thấy trong 5 file đã đọc mô tả cụ thể việc subagent bị CHẶN kỹ thuật (permission, sandbox) không cho đọc file dự án — chỉ có chỉ dẫn "it gets its brief and nothing else" như một quy tắc soạn brief, dựa trên kỷ luật của agent điều phối (lead) khi soạn prompt cho subagent.
