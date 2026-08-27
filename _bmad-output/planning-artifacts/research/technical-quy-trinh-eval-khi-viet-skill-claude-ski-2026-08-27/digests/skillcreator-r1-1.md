# Digest — D1: quy trình chính thức skill-creator (round 1, assistant 1)

## Findings

**1. `platform.claude.com/.../best-practices` — "Evaluation and iteration"**
Claim: Anthropic khuyến nghị rõ ràng "Create evaluations BEFORE writing extensive documentation" cho MỘT skill, theo quy trình 5 bước: (1) chạy Claude không có skill để tìm gaps, (2) tạo evaluation cho các gaps đó, (3) đo baseline không-skill, (4) viết instructions tối thiểu để pass eval, (5) lặp lại. Checklist cuối bài yêu cầu "At least three evaluations created" trước khi coi skill là sẵn sàng chia sẻ.
Nguyên văn: "Create evaluations BEFORE writing extensive documentation. This ensures your Skill solves real problems rather than documenting imagined ones."
Source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
Publisher: Anthropic (docs chính thức) | pub_date: không rõ | accessed: 2026-08-27 | confidence: cao | class: chính sách chính thức
Lưu ý: khuyến nghị này nói về vòng đời của MỘT skill đơn (viết eval để định hình nội dung skill đó), KHÔNG bàn tình huống nhiều skill phối hợp / vertical slice.

**2. Repo `anthropics/skills`, skill `skill-creator`, file SKILL.md — quy trình thao tác thực tế**
Claim: Ngược với khuyến nghị "eval trước" ở best-practices, quy trình thao tác thực tế mà công cụ skill-creator làm là viết draft skill TRƯỚC, rồi mới tạo test prompts/eval SAU.
Nguyên văn (đúng thứ tự gốc): "Decide what you want the skill to do and roughly how it should do it" → "Write a draft of the skill" → "Create a few test prompts and run claude-with-access-to-the-skill on them" → "Help the user evaluate the results both qualitatively and quantitatively" → "Rewrite the skill based on feedback... Repeat until you're satisfied" → "Expand the test set and try again at larger scale."
Tiêu chí dừng: "Keep going until: The user says they're happy / The feedback is all empty / You're not making meaningful progress" — không có câu nào nói "phải có eval mới coi là hoàn thành".
Source: https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md (đọc qua mirror cdn.jsdelivr.net do GitHub trực tiếp lỗi SSL trong phiên)
Publisher: Anthropic (repo GitHub chính thức) | pub_date: không rõ | accessed: 2026-08-27 | confidence: cao (khớp giữa 2 lần fetch độc lập) | class: chính sách chính thức / công cụ chính thức

**3. `code.claude.com/docs/en/skills` — "Evaluate and iterate on a skill"**
Claim: Tài liệu Claude Code coi eval là bước xảy ra SAU KHI skill đã tồn tại và chạy được ("evaluate an existing skill"), không phải điều kiện tiên quyết để bắt đầu dùng skill. Giới thiệu plugin `skill-creator` chính thức để tự động hoá vòng lặp so sánh with/without-skill, lưu evals trong `evals/evals.json`.
Nguyên văn: "Seeing a skill trigger tells you Claude found it, not that it did what you intended. To know a skill is working, measure two things separately..." / "The plugin walks you through writing test cases and runs the loop."
Source: https://code.claude.com/docs/en/skills
Publisher: Anthropic (docs chính thức) | pub_date: không rõ | accessed: 2026-08-27 | confidence: cao | class: chính sách chính thức

**4. `agentskills.io/skill-creation/evaluating-skills` — quy trình eval chi tiết nhất, được code.claude.com dẫn làm nguồn tham chiếu**
Claim: Trang mở đầu bằng giả định skill ĐÃ VIẾT XONG rồi mới eval: "You wrote a skill, tried it on a prompt, and it seemed to work. But does it work reliably..." Khuyến nghị rõ: bắt đầu với 2-3 test case, "Don't over-invest before you've seen your first round of results", chưa cần định nghĩa assertion pass/fail chi tiết ngay.
Source: https://agentskills.io/skill-creation/evaluating-skills
Publisher: agentskills.io (chuẩn Agent Skills, khởi xướng bởi Anthropic, nay duy trì qua "Agentic AI Foundation"; được code.claude.com dẫn chiếu chính thức) | pub_date: không rõ | accessed: 2026-08-27 | confidence: trung bình-cao | class: chính sách chính thức (được dẫn chiếu chính thức)

**5. Blog Anthropic về skill-creator**
Claim: Nhấn mạnh giá trị testing nhưng KHÔNG tuyên bố dứt khoát về thời điểm (ngay sau skill đầu tiên hay dồn lại sau nhiều skill). Ví dụ Anthropic tự dùng eval sửa lỗi "PDF skill" (một skill đơn, không phải multi-skill).
Nguyên văn: "Testing turns a skill that seems to work into one you know works."
Source: https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills
Publisher: Anthropic (blog) | pub_date: chưa xác nhận độc lập (ghi nhận ~2026-03, cần đối chiếu) | accessed: 2026-08-27 | confidence: trung bình (tóm tắt qua fetch, chưa đọc verbatim toàn văn) | class: chính sách chính thức / quan sát thực tế của Anthropic

## Leads chưa theo kịp
- GitHub Issue #490 (`anthropics/skills`): "skill-creator: Create evals workspace outside skill directory to avoid confusion with skills" — tiêu đề gợi ý người dùng thực tế gặp vấn đề tổ chức evals khi có NHIỀU skill trong cùng repo. Không fetch được do lỗi SSL certificate với github.com trong phiên này.
- GitHub Issue #880 ("SOP_BUILDER_SKILL.md") và blog tessl.io "Anthropic brings evals to skill-creator. Here's why that's a big deal" — chưa fetch.
- Ngày xuất bản chính xác của các trang docs Anthropic — chưa xác nhận độc lập (docs Mintlify-style không hiển thị ngày công khai).
- Chưa kiểm tra trực tiếp mã nguồn plugin `skill-creator` (claude-plugins-official) để xem logic có ép buộc thứ tự nào không.

## Không tìm thấy
- Không tìm thấy tuyên bố chính thức nào của Anthropic áp dụng nhị phân "phải có eval trước khi coi 1 skill hoàn thành" CHO TÌNH HUỐNG NHIỀU SKILL PHỐI HỢP — mọi tài liệu đọc được chỉ bàn vòng đời một skill đơn lẻ.
- Không tìm thấy ví dụ thực tế mô tả một dự án nhiều-skill chủ động hoãn eval đến khi có vertical slice.
- Không tìm thấy Anthropic tự thừa nhận mâu thuẫn ngôn ngữ giữa best-practices ("eval trước") và skill-creator SKILL.md ("draft trước, eval sau") — hai tài liệu không đối chiếu lẫn nhau.
