# Digest R1-1 — Giữ trạng thái xuyên phiên (memlog, doc_workspace, resume, "file ngay lập tức")

Nguồn đọc trực tiếp:
- `_bmad/scripts/memlog.py` (toàn bộ, 225 dòng)
- `.claude/skills/bmad-deep-recon/SKILL.md`
- `.claude/skills/bmad-deep-recon/references/run.md`
- `.claude/skills/bmad-deep-recon/customize.toml`
- `.claude/skills/bmad-deep-recon/scripts/recon_kit.py`
- `.claude/skills/bmad-prd/SKILL.md`
- `.claude/skills/bmad-prd/customize.toml` (chỉ grep dòng liên quan)
- `.claude/skills/bmad-architecture/SKILL.md`
- `.claude/skills/bmad-architecture/customize.toml` (chỉ grep dòng liên quan)
- `.claude/skills/bmad-prfaq/SKILL.md`

---

## Q1 — Cơ chế memlog (`.memlog.md`)

{claim: "memlog.py định nghĩa memlog là 'an append-only memory log: LLM-optimal working memory for a skill' — bản ghi dày đặc, theo thời gian, của mọi thứ quan trọng trong một phiên làm việc, tồn tại XUYÊN PHIÊN để một phiên mới có thể nạp lại và tiếp tục; nó KHÔNG phải deliverable — tài liệu đầu ra (brief, PRD, report...) được suy ra từ nó khi cần.", source: "_bmad/scripts/memlog.py:5-12", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "memlog là một log PHẲNG (flat) — không có section hay nhóm; mỗi entry là một dòng, được ghi ở CUỐI theo đúng thứ tự xảy ra; chính trình tự thời gian là cấu trúc — một sự kiện như 'started technique X' chỉ là một entry khác, ngang hàng với một ý tưởng hay insight.", source: "_bmad/scripts/memlog.py:14-16", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "memlog.py tự khai báo ba bất biến (invariants) làm cho nó đáng tin cậy: (1) Append-only/chronological — không bao giờ chèn lùi, sắp lại thứ tự, sửa hay xoá; script cố ý KHÔNG có subcommand edit/delete; lịch sử không bao giờ bị viết lại. (2) Write-only/blind — mỗi lệnh là một ghi atomic, phi ngữ-cảnh, và echo lại trạng thái mới dưới dạng một dòng JSON, để caller không bao giờ phải đọc lại file giữa phiên; lần duy nhất file được đọc là lúc resume — và chính caller đọc, không qua script. (3) No lifecycle status — memlog không có cờ 'complete'; việc công việc đã xong/bị chặn/tạm dừng tự nó là một sự kiện đã xảy ra nên được ghi như một entry (vd. `append --type event --text \"session complete\"`), không bao giờ là frontmatter phải mutate; resume học trạng thái bằng cách đọc các entry cuối — giống hệt cách nó học mọi thứ khác.", source: "_bmad/scripts/memlog.py:18-32", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Tính atomic của ghi file: mỗi lần ghi đi qua file tạm (`path.with_suffix(path.suffix + '.tmp')`), được flush và fsync, rồi `os.replace` (atomic rename) đè lên file đích — để một crash không bao giờ để lại một entry ghi dở.", source: "_bmad/scripts/memlog.py:34-35,122-129", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Định dạng file `.memlog.md`: frontmatter YAML-giống (`---` mở, các dòng `key: value`, `---` đóng) — ví dụ có `topic`, `goal`, `updated` — theo sau là thân log gồm các dòng bắt đầu bằng `- (type) text` hoặc `- (type by who) text` hoặc `- text` (không tag).", source: "_bmad/scripts/memlog.py:37-53", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Parser frontmatter (`split()`) coi dòng '---' ĐẦU TIÊN xuất hiện đúng nguyên văn là fence đóng, để một giá trị field (vd. topic/goal là free text người dùng) chứa chuỗi '---' bên trong không làm gãy việc parse frontmatter.", source: "_bmad/scripts/memlog.py:93-101", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Mỗi entry có thể mang `--type` tuỳ chọn (kind: idea, insight, question, decision, direction, assumption, gap, note, event, …) và `--by` tuỳ chọn (ai là nguồn, vd. user, coach); cả hai render vào MỘT tag inline ngắn gọn: `(idea)`, `(idea by user)`, `(by coach)`. Bỏ trống cả hai cho một note thường. Bản thân memlog.py không ép buộc một bộ vocabulary cố định — skill gọi nó mới quyết định vocabulary.", source: "_bmad/scripts/memlog.py:55-59", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "memlog.py có đúng 3 lệnh: `init` (tạo memlog mới, lỗi nếu đã tồn tại), `append` (thêm một entry ở cuối), `set` (set/thay một field frontmatter mô tả). Không có lệnh sửa/xoá entry.", source: "_bmad/scripts/memlog.py:61-68,145-187", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Cách địa chỉ hoá file: `--workspace DIR` (memlog luôn là `{workspace}/.memlog.md`) hoặc `--path FILE` (trỏ thẳng vào file cho caller đã sẵn có đường dẫn) — hai chế độ loại trừ lẫn nhau (mutually exclusive group, required).", source: "_bmad/scripts/memlog.py:66,190-194", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "`cmd_append` gộp mọi newline/khoảng trắng thừa trong `--text` thành một dòng đơn (`' '.join(args.text.split())`) — chủ đích là 'no prose bloat', ép mỗi entry là một dòng.", source: "_bmad/scripts/memlog.py:167", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Mỗi lần ghi (`touch()`) đều xoá field `updated` cũ rồi thêm lại ở cuối dict, để field `updated` luôn xuất hiện cuối cùng trong frontmatter một cách nhất quán ('keep it last so the field order stays predictable').", source: "_bmad/scripts/memlog.py:116-119", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Mỗi lệnh của memlog.py echo lại trạng thái mới dưới dạng một dòng JSON (`{\"ok\": true, \"memlog\": path, \"entries\": N}`) để 'caller never re-reads the file to know where it stands' — đúng invariant #2 (write-only/blind).", source: "_bmad/scripts/memlog.py:136-142", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Các skill khác nhau dùng bộ `--type` khác nhau cho memlog, do skill gọi quyết định (không phải memlog.py ép buộc): bmad-deep-recon dùng `decision|source|claim|assumption|question|event`; bmad-prd dùng `decision|change|override|assumption|event`; bmad-architecture dùng `decision|constraint|version|assumption|question|direction|event`.", source: ".claude/skills/bmad-deep-recon/SKILL.md:26; .claude/skills/bmad-prd/SKILL.md:14; .claude/skills/bmad-architecture/SKILL.md:40", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Trong bmad-deep-recon, mỗi claim được log qua memlog dùng `--type claim` với text theo một shape máy-đọc-được cố định: `ref=[n] status=<verified|unverified|disputed|overturned> class=<class> pub=<YYYY-MM> — <claim>`, để script `recon_kit.py tally`/`staleness` đọc được ledger; một thay đổi status sau này là MỘT dòng claim mới cùng `ref=` (status cuối cùng thắng — 'last status wins').", source: ".claude/skills/bmad-deep-recon/references/run.md:70", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Script `recon_kit.py` (nằm ở `.claude/skills/bmad-deep-recon/scripts/`, không phải `_bmad/scripts/`) có subcommand `tally MEMLOG_MD` đếm entries theo type, và với entry `--type claim` áp đúng quy tắc 'last status wins per ref' (dùng regex `status=` và `ref=\\[?(\\d+)\\]?` để parse dòng do memlog.py ghi).", source: ".claude/skills/bmad-deep-recon/scripts/recon_kit.py:16-19,122-152", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prd log override qua memlog kể cả 'headless overrides' — mọi quyết định, thay đổi, override đều thành một dòng append-only khi hội thoại diễn ra: `memlog.py append --workspace {doc_workspace} --type <decision|change|override|assumption|event> --text \"<one-line gist, reason included>\"`.", source: ".claude/skills/bmad-prd/SKILL.md:14", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-architecture nói rõ: 'Record decisions, not rationale (rationale lives in the memlog)' — memlog log cả RATIONALE của các quyết định (không chỉ bản thân quyết định), khác với file tài liệu cuối (spine) vốn chỉ giữ quyết định cô đọng.", source: ".claude/skills/bmad-architecture/SKILL.md:17", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-architecture: với một decision chỉ tồn tại trong một diagram (không phải văn xuôi), nó vẫn phải được log vào memlog ('a decision that lives only in a diagram still gets logged') — cho thấy memlog là nguồn sự thật đầy đủ hơn bất kỳ artifact hiển thị nào (kể cả diagram).", source: ".claude/skills/bmad-architecture/SKILL.md:35", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

---

## Q2 — `doc_workspace` được bind/đặt tên thế nào

{claim: "`{doc_workspace}` được định nghĩa nhất quán trong cả 3 skill (deep-recon, prd, architecture) là 'the bound run folder' — một biến resolution giống `{project-root}`, `{skill-root}`.", source: ".claude/skills/bmad-deep-recon/SKILL.md:33; .claude/skills/bmad-prd/SKILL.md:13; .claude/skills/bmad-architecture/SKILL.md:46", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Cả 3 skill dùng CÙNG một công thức bind: `{doc_workspace}` = `{<output_path>}/{workflow.run_folder_pattern}/` — deep-recon: `research_output_path`; prd: `prd_output_path`; architecture: `spine_output_path`.", source: ".claude/skills/bmad-deep-recon/references/run.md:26; .claude/skills/bmad-prd/SKILL.md:32; .claude/skills/bmad-architecture/SKILL.md:60", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Giá trị thực của `run_folder_pattern` khác nhau theo skill nhưng cùng khuôn mẫu <loại>-<định danh>-<ngày>: bmad-deep-recon = `\"{research_type}-{topic_slug}-{date}\"`; bmad-prd = `\"prd-{project_name}-{date}\"`; bmad-architecture = `\"architecture-{project_name}-{date}\"`.", source: ".claude/skills/bmad-deep-recon/customize.toml:34; .claude/skills/bmad-prd/customize.toml:67; .claude/skills/bmad-architecture/customize.toml:55", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Với bmad-deep-recon, tên thư mục KHÔNG được LLM tự do sinh ra — nó được mở rộng deterministic qua script: `uv run scripts/recon_kit.py slug \"<topic>\" --type <type> --pattern \"{workflow.run_folder_pattern}\"`, mục đích rõ ràng nêu trong run.md: 'so the same topic always resolves to the same folder' (idempotent theo topic, để draft → run bên ngoài → process cùng trỏ vào một folder).", source: ".claude/skills/bmad-deep-recon/references/run.md:26", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "`recon_kit.py slug` chuẩn hoá topic thành ascii-lowercase, thay ký tự không phải [a-z0-9] bằng '-', gộp '-' liên tiếp, cắt tối đa 40 ký tự, rồi thay 3 placeholder `{research_type}`, `{topic_slug}`, `{date}` (mặc định `date.today()` nếu không truyền `--date`) vào pattern để ra tên folder cuối cùng.", source: ".claude/skills/bmad-deep-recon/scripts/recon_kit.py:212-227", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Mỗi run-folder có cùng một 'shape' cố định bất kể intent (Draft/Process/Run/Refresh) trong deep-recon: `brief.md`, `imports/`, `digests/`, `research.md`, `.memlog.md` — nêu rõ 'Every intent shares the run-folder workspace shape'.", source: ".claude/skills/bmad-deep-recon/SKILL.md:56", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-architecture có một quy tắc đặt tên đặc biệt cho altitude 'epic': 'At epic altitude, scope the folder to the epic (set run_folder_pattern per customize.toml) so per-epic runs don't collide' — tức override pattern để nhúng epic identity, tránh nhiều epic-run ghi đè lẫn nhau.", source: ".claude/skills/bmad-architecture/SKILL.md:60", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Cả 3 skill đều quét thư mục output TRƯỚC KHI bind workspace mới, để phát hiện run dở dang và đề nghị resume thay vì tạo trùng: bmad-prd quét `{workflow.prd_output_path}` tìm folder theo `run_folder_pattern` có `prd.md` frontmatter `status` khác `final`; bmad-architecture 'If a run folder for this target already exists under {workflow.spine_output_path}, offer to resume'; bmad-deep-recon 'If a run folder for this topic already exists under {workflow.research_output_path}, offer to resume or extend it'.", source: ".claude/skills/bmad-prd/SKILL.md:24; .claude/skills/bmad-architecture/SKILL.md:56; .claude/skills/bmad-deep-recon/SKILL.md:45", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-deep-recon comment trong customize.toml nói rõ dụng ý thiết kế shape workspace: 'Draft, Process, and Run all use the same folder shape' — cho thấy shape không phụ thuộc intent, chỉ phụ thuộc topic/run.", source: ".claude/skills/bmad-deep-recon/customize.toml:29-34", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

---

## Q3 — Resume/refresh một phiên dở dang hoạt động thế nào

{claim: "memlog.py tự mô tả cơ chế resume ở mức nguyên lý: 'A resume learns the state by reading the last entries — the same way it learns everything else' — tức không có cờ trạng thái riêng, resume chỉ là đọc lại chronology và diễn giải các entry cuối.", source: "_bmad/scripts/memlog.py:31-32", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "memlog.py nói rõ: 'The one time the file is read is on resume — and the caller reads it itself, not via this script' — script không có subcommand đọc/list; việc đọc lại (Read tool trong skill) hoàn toàn nằm ở phía skill gọi, không phải trách nhiệm của memlog.py.", source: "_bmad/scripts/memlog.py:24-26", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-architecture nêu thẳng: 'Resume a prior run by reloading its memlog' — và ở phần Update: 'Resume from its .memlog.md (the authority on what was decided), not the rendered spine' — memlog được ưu tiên hơn cả file tài liệu đầu ra (spine) làm nguồn sự thật khi resume.", source: ".claude/skills/bmad-architecture/SKILL.md:35,81", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prd khi Update mà `.memlog.md` bị thiếu (tình huống PRD cũ có trước khi memlog tồn tại), nó không bỏ qua mà spawn một subagent bootstrap 'reverse-engineer a thin log from the PRD' — mỗi decision được suy ngược ra thành một dòng `memlog.py append --type decision` — TRƯỚC khi tiếp tục, cho thấy memlog được coi là điều kiện tiên quyết bắt buộc để làm việc, kể cả phải tái tạo giả lập.", source: ".claude/skills/bmad-prd/SKILL.md:34", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prd bước Finalize có 'Memlog audit' là bước đầu tiên: 'Walk .memlog.md with the user; each entry captured in PRD, in addendum, or set aside' — nghĩa là mọi entry memlog phải có một 'số phận' rõ ràng (vào tài liệu chính, vào addendum, hoặc chủ động bỏ) trước khi đóng phiên, không có entry nào bị lãng quên âm thầm.", source: ".claude/skills/bmad-prd/SKILL.md:87", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-deep-recon: khi phát hiện run-folder cùng topic đã tồn tại, offer resume phân biệt theo trạng thái nội dung cụ thể chứ không chỉ 'có tồn tại hay không' — ví dụ 'a drafted brief awaiting its report, a report awaiting refresh' — hàm ý skill đọc nội dung thư mục (brief.md có/không, research.md có/không) để suy ra đang ở giai đoạn nào của vòng đời (chỉ thấy mô tả này ở bmad-deep-recon).", source: ".claude/skills/bmad-deep-recon/SKILL.md:45", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "medium", class: "pattern"}

{claim: "bmad-prd resume-check cụ thể đọc FRONTMATTER của file tài liệu (không phải chỉ memlog) để lọc: quét các folder khớp `run_folder_pattern` mà `prd.md` frontmatter `status` KHÁC `final` — tức trạng thái 'dở dang' được xác định qua field `status` trong frontmatter của tài liệu đầu ra, song song với memlog.", source: ".claude/skills/bmad-prd/SKILL.md:24", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prfaq (không dùng memlog.py chút nào — pattern hoàn toàn khác) resume bằng cách đọc CHỈ 20 DÒNG ĐẦU của file `prfaq-{project_name}.md` để lấy frontmatter field `stage`, rồi route thẳng tới reference file của stage đó — chủ đích ghi rõ 'Do not read the full document.'. Đây là cơ chế resume nhẹ dựa trên frontmatter field đơn, không phải memlog chronological.", source: ".claude/skills/bmad-prfaq/SKILL.md:72", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prfaq lưu trạng thái tiến trình bằng các block comment HTML nhúng thẳng trong tài liệu đầu ra (`<!-- coaching-notes-stage-1 -->`) chứa rationale, assumption đã thách thức, lý do chọn hướng này thay vì hướng khác, và context người dùng không khớp khuôn PRFAQ — đây là một cơ chế 'process memory' khác hẳn memlog append-only: nhúng trực tiếp vào tài liệu thay vì một file log riêng. Pattern này CHỈ thấy ở bmad-prfaq trong số các file đã đọc.", source: ".claude/skills/bmad-prfaq/SKILL.md:123", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-deep-recon Headless Mode trả về JSON kết thúc có field `memlog` (đường dẫn) như một phần hợp đồng máy-đọc-được, cho thấy vị trí memlog được coi là output chính thức, không chỉ phụ trợ nội bộ.", source: ".claude/skills/bmad-deep-recon/SKILL.md:69-80", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

---

## Q4 — Vì sao "mọi thứ ra file ngay lập tức" thay vì giữ trong ngữ cảnh hội thoại

{claim: "bmad-deep-recon nêu trực tiếp lý do dưới heading 'How you work': 'Nothing exists until it is a file. Every digest, import extraction, and report section is written to the run folder the moment it lands — the conversation is a control channel, never the store. A run that dies mid-flight resumes from disk with nothing lost.' — đây là câu trả lời rõ ràng nhất, viết thẳng ra, cho câu hỏi 4.", source: ".claude/skills/bmad-deep-recon/SKILL.md:21", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Lý do thứ hai viết thẳng ra (bổ sung cho lý do 'sống sót qua crash'): quản lý context window — 'Extract, don't ingest. Raw reports and search results never enter the parent context whole; subagents return relevance-filtered digests, and the parent reads digest files JIT [just-in-time].' — ghi file ngay còn để TRÁNH việc raw content tràn ngập context của agent chính.", source: ".claude/skills/bmad-deep-recon/SKILL.md:22", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "run.md củng cố lý do JIT/extract bằng chỉ dẫn thao tác cụ thể: 'On each return, write the digest to {doc_workspace}/digests/ before doing anything else with it' — quy tắc thao tác literally là ghi file TRƯỚC, xử lý sau, không phải ngược lại.", source: ".claude/skills/bmad-deep-recon/references/run.md:54", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prd áp cùng nguyên tắc 'extract, don't ingest' cho tài liệu nguồn: 'Source documents go to subagents for extraction; the parent assembles from extracts. Only load source documents into the parent context wholesale when no subagents are available' — xác nhận đây là pattern lặp lại xuyên nhiều skill, không phải đặc thù riêng của deep-recon (dù câu giải thích 'why' tường minh nhất chỉ xuất hiện ở bmad-deep-recon).", source: ".claude/skills/bmad-prd/SKILL.md:67", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Lý do thứ ba (ngầm, suy ra từ nhiều chỗ, không phải một câu 'why' tường minh riêng): tách bạch việc GHI (write-only/blind) khỏi việc ĐỌC LẠI (chỉ khi resume) giúp mỗi thao tác ghi là atomic và không tốn context — memlog.py invariant #2 'the caller never re-reads the file mid-session' đúng với lý do context-budget hơn là chỉ crash-safety.", source: "_bmad/scripts/memlog.py:23-26", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "medium", class: "pattern"}

{claim: "bmad-architecture áp cùng triết lý 'distill từ file lưu trữ, không tích luỹ trong hội thoại' cho tài liệu cuối: 'The spine file itself is distilled from the memlog at the end, not written as you go' — tài liệu chính thức KHÔNG được xây dần trong ngữ cảnh hội thoại qua nhiều lượt, mà được tổng hợp một lần từ file log đã ghi sẵn.", source: ".claude/skills/bmad-architecture/SKILL.md:35", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

---

## Leads worth chasing

- `.claude/skills/bmad-deep-recon/references/lifecycle.md` — file này tồn tại (xác nhận qua `find`) và được SKILL.md trỏ tới cho intent "Refresh / Deepen" (cập nhật/mở rộng một run-folder có sẵn). Nằm NGOÀI danh sách nguồn được giao cho phiên này nên chưa đọc — đây là nơi nhiều khả năng có chi tiết cụ thể nhất về cơ chế refresh (câu hỏi 3), gồm cách phát hiện phần nào đã stale và cần chạy lại.
- `.claude/skills/bmad-deep-recon/references/headless.md` không tồn tại theo tên đó trong deep-recon (deep-recon xử lý headless ngay trong SKILL.md, phần "Headless Mode") nhưng bmad-prd và bmad-architecture đều trỏ tới `references/headless.md` riêng của chúng — chưa đọc; có thể có thêm chi tiết về cách log override khi headless.
- Chưa đọc `resolve_customization.py` và `resolve_config.py` (được gọi ở bước Activation của mọi skill) — có thể làm rõ thêm cơ chế merge `customize.toml` ảnh hưởng tới `run_folder_pattern`, nhưng nằm ngoài phạm vi câu hỏi được giao (đây là cấu hình, không phải state xuyên phiên).
- Chưa kiểm tra xem có một `.memlog.md` THẬT (đã sinh ra từ một lần chạy skill thật) nằm đâu đó trong repo `van-dao-workspace` để đối chiếu format lý thuyết (trong docstring memlog.py) với một file thực tế — nếu có, đáng đọc để xác nhận không có drift giữa spec và thực thi.

## Không tìm thấy

- Không tìm thấy bằng chứng trực tiếp nào cho thấy `bmad-prfaq` dùng `memlog.py` — grep/đọc SKILL.md của nó không có bất kỳ tham chiếu nào tới `memlog.py` hay `.memlog.md`; cơ chế trạng thái của nó (frontmatter `stage` + coaching-notes comment nhúng trong tài liệu) là một pattern KHÁC hẳn, không nên khái quát hoá memlog là cơ chế phổ quát cho MỌI skill BMAD — chỉ xác nhận được ở 3/4 skill đã đọc (deep-recon, prd, architecture).
- Không tìm thấy trong các file đã đọc một câu giải thích "why" tường minh, độc lập, cho riêng nguyên tắc "no lifecycle status / mọi trạng thái là một event" (invariant #3 trong memlog.py) — chỉ có mô tả CƠ CHẾ, không có đoạn văn nói rõ TẠI SAO chọn thiết kế này thay vì một field status đơn giản.
- Không tìm thấy con số/quy tắc cụ thể nào giới hạn ĐỘ DÀI hay số lượng entry tối đa của một memlog trong các file đã đọc — memlog.py không áp giới hạn kỹ thuật nào (không cap dòng, không rotate file).
- Chưa xác nhận được (vì chưa đọc lifecycle.md) cơ chế refresh xử lý CONFLICT thế nào khi nội dung nguồn đã đổi so với lần chạy trước — SKILL.md deep-recon chỉ nhắc tên intent, không mô tả cơ chế.
