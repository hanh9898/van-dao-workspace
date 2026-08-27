# Digest — D2: bằng chứng thực tiễn về thời điểm eval (round 1, assistant 2)

## Findings

**1. OpenAI Developers — "Testing Agent Skills Systematically with Evals"**
Claim: "Define success before you write the skill" — lập trường ngược với hoãn eval, áp dụng ngay cho một skill đơn lẻ, không đợi có nhiều skill phối hợp.
Source: https://developers.openai.com/blog/eval-skills
Publisher: OpenAI Developers | pub_date: không rõ | accessed: 2026-08-27 | confidence: trung bình (chỉ 1 câu trích, không lấy được đoạn nói rõ về hệ multi-skill) | class: chính sách chính thức (nhà cung cấp khác)

**2. Minko Gechev — "Unit Tests for AI Agent Skills" (26/02/2026)**
Claim: "Don't ship skills without evals" — eval phải tồn tại trước khi đưa skill vào sản xuất, kể cả một skill đơn lẻ; không bàn cụ thể việc có nên đợi vertical slice hay không.
Source: https://blog.mgechev.com/2026/02/26/skill-eval/
Publisher: blog.mgechev.com (tác giả thật, kỹ sư) | pub_date: 2026-02-26 | accessed: 2026-08-27 | confidence: trung bình-cao | class: quan sát thực tế / khuyến nghị cá nhân

**3. Paul Twist — "The Evaluation Debt You Don't Know You Have" (DEV Community, 13/07/2026)**
Claim: Cảnh báo "eval debt" trong agent LLM: "The eval debt you don't know you have? It compounds every week. Pay it early." Khuyến nghị coi eval infra "co-equal" với agent infra, log có cấu trúc "from day one".
Source: https://dev.to/paultwist/the-evaluation-debt-you-dont-know-you-have-why-agent-evals-fail-in-production-2md8
Publisher: DEV Community (Paul Twist) | pub_date: 2026-07-13 | accessed: 2026-08-27 | confidence: trung bình | class: quan sát thực tế — trả lời trực tiếp câu hỏi rủi ro trì hoãn

**4. Alistair Cockburn — "Walking Skeleton" (Writing Effective Use Cases, 2000), qua nhiều nguồn thứ cấp**
Claim: Walking Skeleton = "cài đặt tối giản của hệ thống thực hiện một chức năng end-to-end nhỏ... không cần kiến trúc cuối cùng nhưng phải nối các thành phần kiến trúc chính lại; kiến trúc và chức năng sau đó tiến hoá song song." Tiền lệ trực tiếp trong kỹ nghệ phần mềm cho ý tưởng "dựng luồng chạy được tối thiểu trước".
Source: https://distilledpatterns.org/patterns/walking-skeleton/ ; https://www.henricodolfing.ch/en/start-your-project-with-a-walking-skeleton/ ; https://www.forbes.com/councils/forbestechcouncil/2020/01/02/using-a-walking-skeleton-to-reduce-risk-in-software-innovation/
Publisher: nhiều nguồn thứ cấp, gốc Alistair Cockburn (đồng tác giả Agile Manifesto) | pub_date: khái niệm gốc 2000; Forbes 2020-01-02 | accessed: 2026-08-27 | confidence: cao (nhất quán qua nhiều nguồn độc lập) | class: lý thuyết phần mềm tổng quát

**5. defmyfunc.com — rủi ro khi KHÔNG làm walking skeleton**
Claim: "Building components in isolation pushes integration risk to the end of the project. Data contracts, latency limits, output formats, and deployment constraints fail late... This leads to rework and late system surprises." — rủi ro cụ thể khi trì hoãn tích hợp/kiểm thử hệ thống.
Source: https://www.defmyfunc.com/2019_10_18_walking_skeleton/
Publisher: defmyfunc blog | pub_date: 2019-10-18 | accessed: 2026-08-27 | confidence: trung bình | class: lý thuyết phần mềm tổng quát / kinh nghiệm

**6. Vijay Anant — "The Architectural Spike: De-Risking High-Stakes Technical Decisions"**
Claim: Spike là "thí nghiệm tập trung, giới hạn thời gian (1-2 tuần) nơi bạn dừng xây tính năng và bắt đầu xây bằng chứng" — trong spike, chuẩn kiểm thử hình thức được nới lỏng để ưu tiên tốc độ chứng minh khái niệm, tương tự logic "hoãn eval tới vertical slice".
Source: https://vijayanant.com/posts/from-patterns-to-practice/the-spike/
Publisher: blog cá nhân | pub_date: không rõ | accessed: 2026-08-27 | confidence: trung bình | class: lý thuyết phần mềm tổng quát

**7. Braintrust — "AI agent evaluation: A practical framework" (02/02/2026) — negative finding**
Đã fetch và đọc trực tiếp: KHÔNG bàn trình tự vertical-slice-trước-hay-eval-trước; chỉ mô tả vòng lặp eval sau khi agent đã ở production.
Source: https://www.braintrust.dev/articles/ai-agent-evaluation-framework
Publisher: Braintrust | pub_date: 2026-02-02 | accessed: 2026-08-27 | confidence: cao (đã đọc trực tiếp) | class: quan sát thực tế (không trả lời câu hỏi)

## Leads chưa theo kịp
- PwC — "Validating multi-agent AI systems: From modular testing to system-level governance" — snippet gợi ý PwC ủng hộ kiểm thử từng agent riêng lẻ TRƯỚC rồi mới kiểm thử cấp hệ thống (ngược hướng câu hỏi 4), nhưng fetch bị chặn (HTTP 403), chưa kiểm chứng được.
- arXiv 2606.08162 — "Silent Failure in LLM Agent Systems: The Entropy Principle..." — tiêu đề liên quan trực tiếp câu hỏi rủi ro trì hoãn, chưa fetch full-text.
- leehanchung.github.io "Hidden Technical Debt of AI Systems: Agent Runtime" (24/04/2026) và Port.io "The Hidden Technical Debt Of Agentic Engineering" — chỉ có snippet, chưa xác minh.
- Hacker News threads liên quan agent-evals — chưa đọc phần bình luận.
- Hamel Husain / Shreya Shankar "FAQs About AI Evals" (qua Simon Willison, 2025-07-03) — có câu "evaluation is part of the development process rather than a distinct line item" nhưng chưa lấy được đoạn gốc đầy đủ để trích chính xác ngữ cảnh.

## Không tìm thấy
- Câu hỏi trọng tâm: không tìm được nguồn có tên tác giả/tổ chức thật bàn TRỰC TIẾP và CỤ THỂ về trình tự "vertical slice trước → eval hình thức hoá sau" cho AI agent/skill, ngoài 3 nguồn đã biết trước trong dự án (Anthropic best-practices, Superpowers, claude-tutor).
- Không tìm được người ủng hộ RÕ RÀNG, có trích dẫn cụ thể, cho lập trường "dựng luồng nhiều-thành-phần chạy được trước, eval sau" trong bối cảnh multi-agent/multi-skill — các nguồn multi-agent testing tìm được (PwC — chưa xác minh do 403) đều nghiêng hướng ngược lại: kiểm từng agent/module trước, tích hợp sau.
- Không tìm thấy thread Reddit cụ thể bàn đúng câu hỏi trình tự này.
