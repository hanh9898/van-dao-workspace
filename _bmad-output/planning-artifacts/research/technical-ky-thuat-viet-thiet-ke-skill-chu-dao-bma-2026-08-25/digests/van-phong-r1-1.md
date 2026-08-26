# Digest — Dimension 5: Văn phong hướng dẫn model (BMAD SKILL.md)

Nguồn đọc trực tiếp: bmad-architecture/SKILL.md, bmad-prd/SKILL.md, bmad-deep-recon/SKILL.md, bmad-prfaq/SKILL.md, bmad-review/SKILL.md (đường dẫn gốc `.claude\skills\<tên>\SKILL.md` dưới `C:\Users\HBLAB_OPMS\Projects\van-dao-workspace\`).

## Câu 1 — Ngôi, giọng điệu, persona

{claim: "SKILL.md của bmad-architecture mở đầu bằng câu ngôi thứ hai trực tiếp 'You produce an architecture spine...' — không đặt tên persona riêng, chỉ xưng 'you'", source: ".claude\\skills\\bmad-architecture\\SKILL.md:9", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-architecture tự mô tả vai trò kèm cam kết hành vi: 'You're a coach, and the Coaching path is the default'", source: ".claude\\skills\\bmad-architecture\\SKILL.md:21", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prd mở đầu bằng persona tường minh 'You are a master facilitator and coach helping the user create, edit, or validate a high quality PRD...'", source: ".claude\\skills\\bmad-prd\\SKILL.md:7", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prd dùng câu mệnh lệnh ức chế hành vi mặc định của model: 'Fight the urge to do the thinking for them unless they put you into Fast path'", source: ".claude\\skills\\bmad-prd\\SKILL.md:7", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-deep-recon gán persona bằng tên riêng: 'You are Deep Recon — a research director, not a search engine' — kèm phép đối lập tương phản để định hình vai trò", source: ".claude\\skills\\bmad-deep-recon\\SKILL.md:10", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prfaq ra lệnh đóng vai bằng động từ mệnh lệnh trực tiếp: 'Act as a relentless but constructive product coach who stress-tests every claim, challenges vague thinking, and refuses to let weak ideas pass unchallenged'", source: ".claude\\skills\\bmad-prfaq\\SKILL.md:10", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prfaq tự đặt tên chế độ giọng điệu bằng in đậm: 'This is hardcore mode. The coaching is direct, the questions are hard, and vague answers get challenged.'", source: ".claude\\skills\\bmad-prfaq\\SKILL.md:14", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prfaq chỉ đạo tông giọng cụ thể ở bước kích hoạt: 'Be warm but efficient — dream builder energy.'", source: ".claude\\skills\\bmad-prfaq\\SKILL.md:62", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Khác với 4 file kia, bmad-review KHÔNG mở đầu bằng câu 'You are X' gán persona — câu đầu là mệnh lệnh trực tiếp không nêu vai trò: 'Review content through lenses — each a distinct method and stance — and report findings in one canonical shape.' (chỉ thấy thiếu persona-framing ở file này trong số 5 file khảo sát)", source: ".claude\\skills\\bmad-review\\SKILL.md:7", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Cả 5 SKILL.md đều dùng ngôi thứ hai xưyên suốt (xưng 'you'/mệnh lệnh ngầm định 'you') để nói chuyện trực tiếp với agent, không dùng ngôi thứ ba mô tả agent", source: "tổng hợp .claude\\skills\\bmad-architecture\\SKILL.md, bmad-prd\\SKILL.md, bmad-deep-recon\\SKILL.md, bmad-prfaq\\SKILL.md, bmad-review\\SKILL.md", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "medium", class: "pattern"}

## Câu 2 — Kỹ thuật lặp lại buộc đúng thứ tự

{claim: "Cả 5 file đều có mục 'On Activation' đánh số bước tuần tự (bmad-architecture 1-8, bmad-prd 1-5 rồi Finalize 1-8, bmad-prfaq Step 1-6, bmad-review 1-7, bmad-deep-recon 1-5) — numbered steps là khuôn mẫu lặp lại xuyên suốt cả 5 file", source: ".claude\\skills\\bmad-architecture\\SKILL.md:49-58; .claude\\skills\\bmad-prd\\SKILL.md:16-28; .claude\\skills\\bmad-prfaq\\SKILL.md:29-68; .claude\\skills\\bmad-review\\SKILL.md:25-33; .claude\\skills\\bmad-deep-recon\\SKILL.md:36-44", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prd và bmad-prfaq dùng NGUYÊN VĂN GẦN GIỐNG HỆT NHAU một câu chốt sau bước activation để ép model xác nhận đã chạy đủ bước theo thứ tự trước khi làm việc chính: 'Activation is complete. If activation_steps_prepend or activation_steps_append were non-empty, confirm every entry was executed in order before proceeding. Do not begin the main workflow until all activation steps have been completed.'", source: ".claude\\skills\\bmad-prd\\SKILL.md:28; .claude\\skills\\bmad-prfaq\\SKILL.md:68", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-architecture dùng câu điều kiện lặp lại nhiều lần để rẽ nhánh sang skill khác thay vì tự làm sai việc: 'If the real ask is requirements / UX / a capability contract / epic breakdown / an agent, invoke the bmad-prd, bmad-ux, bmad-spec... skill instead.'", source: ".claude\\skills\\bmad-architecture\\SKILL.md:55", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prd dùng cấu trúc if-then để xử lý lệch hướng: 'scan for misroute on the first message: if the signal points elsewhere (game → BMad GDS; express build → bmad-build...) suggest they might want the other options before continuing.'", source: ".claude\\skills\\bmad-prd\\SKILL.md:23", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-review dùng câu điều kiện tường minh để xử lý input rỗng, phân theo 2 nhánh caller mong đợi format khác nhau: 'If it is empty or cannot be decoded as text: when the caller expects the raw findings JSON array... return [...] and stop; otherwise say what's wrong and ask for reviewable content.'", source: ".claude\\skills\\bmad-review\\SKILL.md:28", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "'Never' xuất hiện lặp lại như một khuôn cấm đoán ngắn gọn trong nhiều file: bmad-review 'No severity, priority, or ranking anywhere.'", source: ".claude\\skills\\bmad-review\\SKILL.md:45", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-architecture dùng 'never' để khoá hành vi bịa đặt và đánh số lại: 'No placeholders; never invent to fill a gap.' và '...never renumber or reuse a retired ID.'", source: ".claude\\skills\\bmad-architecture\\SKILL.md:70,81", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-deep-recon dùng 'never' liên tiếp hai lần trong phần Epistemics để khoá nguồn kết luận và ngăn agent con tiếp cận project context: 'Never conclude from training data alone.' và research firewall coi project context 'never what is true'", source: ".claude\\skills\\bmad-deep-recon\\SKILL.md:16-17", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-deep-recon cấm bịa nghiên cứu bằng câu ngắn cuối mục Overview: 'Web access is required for Run. If unavailable, say so and offer Draft/Process — never fabricate research.'", source: ".claude\\skills\\bmad-deep-recon\\SKILL.md:27", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Kỹ thuật ràng buộc thứ tự bằng giải thích lý do (rationale ngay trong câu lệnh) thay vì chỉ ra lệnh suông xuất hiện lặp lại: bmad-prd 'Polish goes last so it does not redo work after reviewer fixes.' và bmad-architecture 'Walk the sequence; reviewer fixes land before polish.'", source: ".claude\\skills\\bmad-prd\\SKILL.md:85; .claude\\skills\\bmad-architecture\\SKILL.md:68", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prfaq ép thứ tự bước qua bảng 'Stages' đánh số 1-5 kèm cột 'Location' chỉ định file tham chiếu tiếp theo, và cuối mỗi giai đoạn có câu route tường minh ví dụ 'When you have enough to draft a press release headline, route to ./references/press-release.md.'", source: ".claude\\skills\\bmad-prfaq\\SKILL.md:125,129-135", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

## Câu 3 — Mẫu hình "một test/tiêu chí" thay vì liệt kê hết trường hợp

{claim: "bmad-architecture có block quote tường minh gọi là 'One test decides what belongs': 'If two units one level down built this independently, could they choose incompatibly? Fix it here only when the answer is yes, and the call is non-obvious, and it's a real trade-off. Otherwise name it under Deferred and move on.'", source: ".claude\\skills\\bmad-architecture\\SKILL.md:11-13", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Nhãn 'One test decides...' theo đúng nghĩa đen chỉ xuất hiện ở bmad-architecture trong số 5 file khảo sát — 4 file còn lại không dùng cụm từ 'one test' này", source: "tổng hợp .claude\\skills\\bmad-prd\\SKILL.md, bmad-deep-recon\\SKILL.md, bmad-prfaq\\SKILL.md, bmad-review\\SKILL.md (không tìm thấy cụm 'one test')", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prd có mẫu hình tương tự (một tín hiệu duy nhất quyết định thay vì liệt kê) dưới dạng ngưỡng hành vi: 'When you find yourself naming wedges, picking MVP cuts, or proposing phases, stop — you have crossed from elicitation into authoring. Hand the pen back.'", source: ".claude\\skills\\bmad-prd\\SKILL.md:46", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "medium", class: "pattern"}

{claim: "bmad-review có tiêu chí một-câu để mỗi lens tự quyết định 'stance đối với zero-findings' thay vì liệt kê từng trường hợp: 'for most an empty result is valid; the adversarial lens requires at least ten concrete findings and treats an empty list as a signal to re-check'", source: ".claude\\skills\\bmad-review\\SKILL.md:8", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "medium", class: "pattern"}

{claim: "bmad-deep-recon nén định nghĩa 'claim hợp lệ' thành một tiêu chí một-câu duy nhất thay vì liệt kê loại claim: 'A claim is a sentence with a source.'", source: ".claude\\skills\\bmad-deep-recon\\SKILL.md:23", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "medium", class: "pattern"}

{claim: "bmad-prd dùng cặp câu phủ định song song để nén quy tắc chọn mục vào một nguyên tắc thay vì liệt kê danh sách mục cần có/không cần: 'Never include a section because it appears; never skip a concern because no template section covered it.'", source: ".claude\\skills\\bmad-prd\\SKILL.md:65", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "medium", class: "pattern"}

## Câu 4 — Độ dài/mật độ SKILL.md, đẩy chi tiết ra references/

{claim: "Số dòng thực đo của 5 SKILL.md: bmad-architecture 86 dòng, bmad-prd 95 dòng, bmad-deep-recon 83 dòng, bmad-prfaq 136 dòng, bmad-review 50 dòng (đo trực tiếp từ nội dung file đã đọc)", source: ".claude\\skills\\bmad-architecture\\SKILL.md (86 dòng); .claude\\skills\\bmad-prd\\SKILL.md (95 dòng); .claude\\skills\\bmad-deep-recon\\SKILL.md (83 dòng); .claude\\skills\\bmad-prfaq\\SKILL.md (136 dòng); .claude\\skills\\bmad-review\\SKILL.md (50 dòng)", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-deep-recon có bảng tường minh ánh xạ intent → file references/ với chỉ dẫn tải đúng lúc: 'Every intent shares the run-folder workspace shape... Route on the detected intent and load only what it names.' liệt kê Draft→references/draft.md, Process→references/process.md, Run→references/run.md + verification.md + synthesis.md, Refresh/Deepen→references/lifecycle.md", source: ".claude\\skills\\bmad-deep-recon\\SKILL.md:56,58-63", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-review nêu tường minh nguyên tắc tải-đúng-lúc cho chi tiết lens: 'the shipped lenses load their reference file just-in-time, so load only what runs'", source: ".claude\\skills\\bmad-review\\SKILL.md:31", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-architecture đẩy toàn bộ cơ chế review chi tiết ra file riêng và chỉ để lại con trỏ trong SKILL.md: 'The spine's pre-handoff review — full mechanics in references/reviewer-gate.md. Load it when finalizing or validating.'", source: ".claude\\skills\\bmad-architecture\\SKILL.md:64", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prd đẩy toàn bộ quy trình headless và validate ra references/ riêng, SKILL.md chỉ ra lệnh 'follow' hoặc 'Load': 'If headless... follow references/headless.md for the whole run.' và 'Validate (or analyze). Critique without changing. Load references/validate.md.'", source: ".claude\\skills\\bmad-prd\\SKILL.md:24,36", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "bmad-prfaq là file dài nhất (136 dòng) trong 5 file nhưng vẫn đẩy 4/5 giai đoạn (Stage 2-5) ra file references/ riêng, chỉ giữ Stage 1 (Ignition) inline trong SKILL.md — bảng Stages ghi rõ 'Location' cho từng giai đoạn", source: ".claude\\skills\\bmad-prfaq\\SKILL.md:88-135", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Nguyên tắc 'độ dài đẩy chi tiết ra file khác' cũng áp dụng cho TÀI LIỆU ĐẦU RA (không chỉ SKILL.md) trong bmad-prd: 'Length scales with stakes... detail that doesn't earn its place in the PRD's main narrative belongs in addendum.md — moving overflow there is correct; padding the PRD to look thorough is not.' (đây là quy tắc cho PRD sản phẩm, không phải cho chính SKILL.md, cần phân biệt rõ)", source: ".claude\\skills\\bmad-prd\\SKILL.md:69", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

{claim: "Cả 5 file đều có mục 'Conventions'/'Resolution rules' ngắn gọn (4-5 dòng) chuẩn hoá cách resolve path/biến thay vì lặp lại giải thích trong từng phần — dấu hiệu nén thông tin dùng chung lên đầu file", source: ".claude\\skills\\bmad-architecture\\SKILL.md:42-47; .claude\\skills\\bmad-prd\\SKILL.md:9-14; .claude\\skills\\bmad-deep-recon\\SKILL.md:29-34; .claude\\skills\\bmad-prfaq\\SKILL.md:22-27; .claude\\skills\\bmad-review\\SKILL.md:19-23", publisher: "BMAD-METHOD skill source (local)", pub_date: "N/A", accessed: "2026-08-25", confidence: "high", class: "pattern"}

## Leads worth chasing

- Chưa đọc nội dung thực tế của bất kỳ file `references/*.md` nào (vd. `reviewer-gate.md`, `validate.md`, `run.md`, `press-release.md`) — chỉ thấy con trỏ trong SKILL.md. Muốn xác nhận mật độ/độ dài thực tế của references/ so với SKILL.md thì cần đọc trực tiếp các file đó (không nằm trong phạm vi brief này).
- Chưa kiểm tra `customize.toml` của từng skill — các biến `{workflow.xxx}` được tham chiếu dày đặc nhưng cơ chế override/mặc định nằm ở file khác.
- Muốn xác nhận mẫu hình "one test" có lặp lại ở các SKILL.md khác ngoài 5 file được giao (vd. bmad-spec, bmad-build) — nằm ngoài phạm vi brief này, chỉ nêu làm lead.
- Bảng "Stages" của bmad-prfaq và bảng "Intents" của bmad-deep-recon là hai cách trình bày ánh xạ bước→file khác nhau (bảng markdown 3 cột vs 2 cột) — đáng so sánh sâu hơn nếu muốn chọn khuôn mẫu bảng cho Vấn Đạo.

## Không tìm thấy

- Không tìm thấy cụm "one test" hoặc cấu trúc "One test decides..." y hệt ở bmad-prd, bmad-deep-recon, bmad-prfaq, bmad-review — chỉ có các biến thể tương tự (xem Câu 3).
- Không tìm thấy trong bmad-review một câu "You are..." mở đầu gán persona như 4 file kia — file này thiếu phần persona-framing rõ rệt.
- Không tìm thấy quy tắc số-dòng-tối-đa tường minh cho SKILL.md (không có câu kiểu "keep this file under N lines") trong bất kỳ file nào trong 5 file khảo sát — nguyên tắc "ngắn gọn, đẩy ra references/" chỉ được thể hiện qua hành vi cấu trúc file, không phải quy tắc bằng lời.
