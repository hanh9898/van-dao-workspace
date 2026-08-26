# Digest — GitHub Copilot: văn phong hướng dẫn model trong tài liệu chính chủ (đối chiếu BMAD)

Round: r1-1
Chủ đề: cách GitHub Docs/GitHub Blog hướng dẫn viết `copilot-instructions.md` / custom instructions — cấu trúc, văn phong, ví dụ mẫu, cảnh báo lỗi.
Accessed: 2026-08-25 (fetch thực hiện 2026-08-26, ghi theo yêu cầu nhiệm vụ)

---

## Findings

### F1 — Vị trí file, định dạng, cú pháp cơ bản
```
{
  "claim": "Repository-wide custom instructions được đặt tại .github/copilot-instructions.md ở gốc repo, viết bằng ngôn ngữ tự nhiên định dạng Markdown; khoảng trắng giữa các chỉ dẫn bị bỏ qua nên có thể viết thành một đoạn liền, mỗi dòng một ý, hoặc tách đoạn.",
  "source": "https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions",
  "publisher": "GitHub Docs",
  "pub_date": "N/A (trang không hiển thị ngày cập nhật)",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```

### F2 — Giới hạn độ dài cứng + ràng buộc nội dung (docs chính thức, trang repository instructions)
```
{
  "claim": "Docs quy định: 'Instructions must be no longer than 2 pages' và 'Instructions must not be task specific'; đồng thời khuyến cáo tránh cung cấp các bộ chỉ dẫn xung đột nhau ('avoid providing conflicting sets of instructions'), với thứ tự ưu tiên khi xung đột là personal > repository > organization instructions.",
  "source": "https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions",
  "publisher": "GitHub Docs",
  "pub_date": "N/A",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```

### F3 — Giới hạn độ dài (bản khác, trang tutorial Copilot code review) — số dòng cụ thể + lý do chất lượng suy giảm
```
{
  "claim": "Trang tutorial 'Using custom instructions to unlock the power of Copilot code review' nêu nguyên văn: 'Limit any single instruction file to a maximum of about 1,000 lines. Beyond this, the quality of responses may deteriorate.' và 'Shorter instruction files are more likely to be fully processed by Copilot.'",
  "source": "https://docs.github.com/en/copilot/tutorials/use-custom-instructions",
  "publisher": "GitHub Docs",
  "pub_date": "N/A",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```
Ghi chú: hai con số giới hạn khác nhau xuất hiện ở hai trang khác nhau của cùng docs.github.com (2 trang vs ~1000 dòng) — có thể do ngữ cảnh khác nhau (repo-wide vs code-review instructions) hoặc do docs cập nhật không đồng bộ giữa các trang con. Không suy diễn thêm, chỉ ghi nhận cả hai.

### F4 — Danh sách "không hỗ trợ" tường minh cho Copilot code review instructions
```
{
  "claim": "Docs liệt kê tường minh các loại chỉ dẫn Copilot code review KHÔNG hỗ trợ: thay đổi UX/định dạng của review comments, sửa đổi PR overview comment, thay đổi chức năng lõi của Copilot, yêu cầu Copilot theo dõi external links, và các yêu cầu chất lượng mơ hồ (ví dụ liệt kê: 'Be more accurate').",
  "source": "https://docs.github.com/en/copilot/tutorials/use-custom-instructions",
  "publisher": "GitHub Docs",
  "pub_date": "N/A",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```

### F5 — Ví dụ mẫu chính thức: file path-specific instructions (TypeScript) trong GitHub Blog
```
{
  "claim": "GitHub Blog công bố ví dụ đầy đủ một file path-specific instructions (typescript.instructions.md) với frontmatter applyTo: '**/*.ts', gồm các mục: Naming Conventions, Code Style, Error Handling, Testing — mỗi mục là danh sách bullet mệnh lệnh ngắn (vd. 'Use camelCase for variables and functions.', 'Avoid using any type; specify more precise types whenever possible.'). Không có persona/nhân vật nào được gán cho Copilot trong ví dụ này — toàn bộ là quy tắc convention của project.",
  "source": "https://github.blog/ai-and-ml/github-copilot/unlocking-the-full-power-of-copilot-code-review-master-your-instructions-files/",
  "publisher": "GitHub Blog (chính chủ GitHub)",
  "pub_date": "Đăng 2025-11-14, cập nhật 2026-04-17",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```

### F6 — Khuyến nghị văn phong tường minh từ GitHub Blog: "5 tips"
```
{
  "claim": "Bài 'Give GitHub Copilot a project overview' (một trong 5 mục chính của bài) nêu nguyên văn: 'The header for your instructions file should be the elevator pitch for your app.' — tức phần mở đầu file nên mô tả súc tích DỰ ÁN đang làm gì, không phải mô tả Copilot là ai.",
  "source": "https://github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/",
  "publisher": "GitHub Blog (chính chủ GitHub)",
  "pub_date": "Đăng 2025-09-03, cập nhật 2026-06-14",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```

### F7 — Cấu trúc 5 phần được khuyến nghị (không phải persona, mà là 5 loại thông tin dự án)
```
{
  "claim": "5 tiêu đề chính (verbatim, theo đúng thứ tự) của bài blog: 'Give GitHub Copilot a project overview', 'Identify the tech stack you're using in your project', 'Spell out your coding guidelines', 'Explain your project structure', 'Point GitHub Copilot to available resources'. Cả 5 đều là các LOẠI THÔNG TIN VỀ DỰ ÁN cần liệt kê, không có mục nào yêu cầu định nghĩa 'nhân vật'/persona hay vai trò ('You are a senior X engineer...') cho Copilot.",
  "source": "https://github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/",
  "publisher": "GitHub Blog (chính chủ GitHub)",
  "pub_date": "Đăng 2025-09-03, cập nhật 2026-06-14",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```

### F8 — Cảnh báo văn phong tường minh: tránh giọng thụ động-hung hăng
```
{
  "claim": "GitHub Blog nêu nguyên văn cảnh báo về giọng văn: 'Don't be passive aggressive with Copilot.' — khuyến nghị giọng trực tiếp, mệnh lệnh, không mỉa mai/vòng vo.",
  "source": "https://github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/",
  "publisher": "GitHub Blog (chính chủ GitHub)",
  "pub_date": "Đăng 2025-09-03, cập nhật 2026-06-14",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```

### F9 — Ví dụ ngôi thứ 2 / mệnh lệnh trong tutorial "Your first custom instructions"
```
{
  "claim": "Trang tutorial minh hoạ custom instructions bằng ví dụ ngôi thứ 2, mệnh lệnh, liệt kê hành động cụ thể — không phải câu chuyện/persona: 'When writing functions, always: Add descriptive JSDoc comments; Include input validation; Use early returns for error conditions; Add meaningful variable names; Include at least one example usage in comments.' Trang minh hoạ kết quả trước/sau (không có custom instructions vs có custom instructions) để cho thấy tác động.",
  "source": "https://docs.github.com/en/copilot/tutorials/customization-library/custom-instructions/your-first-custom-instructions",
  "publisher": "GitHub Docs",
  "pub_date": "N/A",
  "accessed": "2026-08-25",
  "confidence": "high",
  "class": "pattern"
}
```

### F10 — Ba loại file custom instructions + hỗ trợ liên thông với AGENTS.md/CLAUDE.md/GEMINI.md
```
{
  "claim": "Docs về best practices cho Copilot coding agent liệt kê các định dạng file hỗ trợ: /.github/copilot-instructions.md (toàn repo), /.github/instructions/**/*.instructions.md (theo path, dùng frontmatter applyTo để chỉ định glob pattern loại file áp dụng), và cũng nhận diện **/AGENTS.md, /CLAUDE.md, /GEMINI.md như các định dạng agent-instructions khác được hỗ trợ.",
  "source": "https://docs.github.com/copilot/how-tos/agents/copilot-coding-agent/best-practices-for-using-copilot-to-work-on-tasks",
  "publisher": "GitHub Docs",
  "pub_date": "N/A",
  "accessed": "2026-08-25",
  "confidence": "medium",
  "class": "pattern"
}
```
Ghi chú confidence=medium: chi tiết này đến từ tóm tắt của WebFetch (model phụ), chưa được tôi tự đối chiếu verbatim bằng lượt fetch xác minh riêng như các finding khác.

### F11 — Không tìm thấy: không có sample copilot-instructions.md HOÀN CHỈNH nào được docs.github.com công bố dưới dạng "đây là file mẫu đầy đủ, sao chép nguyên"
```
{
  "claim": "Không tìm thấy trên docs.github.com một file copilot-instructions.md mẫu ĐẦY ĐỦ (full, sẵn sao chép) nào được công bố là 'ví dụ chính thức'. Các ví dụ chính thức tìm được đều là SNIPPET minh hoạ (đoạn Project Overview, đoạn TypeScript path-specific instructions) nằm trong GitHub Blog, không phải một file copilot-instructions.md hoàn chỉnh cho một repo thật.",
  "source": "https://github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/ ; https://github.blog/ai-and-ml/github-copilot/unlocking-the-full-power-of-copilot-code-review-master-your-instructions-files/",
  "publisher": "GitHub Blog (chính chủ GitHub)",
  "pub_date": "N/A (kết luận âm tính, tổng hợp từ các lượt fetch trên)",
  "accessed": "2026-08-25",
  "confidence": "medium",
  "class": "pattern"
}
```

### F12 — Đối chiếu trực tiếp với BMAD: không tìm thấy pattern "persona/You are X" hay "numbered activation steps" trong bất kỳ tài liệu chính chủ GitHub nào đã fetch
```
{
  "claim": "Trong toàn bộ nội dung đã fetch từ docs.github.com và github.blog (các trang trên), KHÔNG xuất hiện khuyến nghị gán persona/nhân vật kiểu 'You are X, a senior engineer...' cho Copilot, và KHÔNG xuất hiện mẫu 'numbered activation steps' hay 'one test decides' kiểu BMAD-METHOD. Văn phong khuyến nghị nhất quán qua các trang là: mô tả SỰ THẬT về dự án (tech stack, cấu trúc thư mục, coding convention) bằng câu mệnh lệnh ngắn, ngôi thứ 2 khi ra lệnh hành động ('always...', 'avoid...', 'use...'), tổ chức theo heading + bullet, không đóng vai nhân vật.",
  "source": "Tổng hợp từ: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions ; https://docs.github.com/en/copilot/tutorials/customization-library/custom-instructions/your-first-custom-instructions ; https://docs.github.com/en/copilot/tutorials/use-custom-instructions ; https://github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/ ; https://github.blog/ai-and-ml/github-copilot/unlocking-the-full-power-of-copilot-code-review-master-your-instructions-files/",
  "publisher": "GitHub Docs / GitHub Blog (chính chủ GitHub)",
  "pub_date": "N/A (kết luận âm tính tổng hợp)",
  "accessed": "2026-08-25",
  "confidence": "medium",
  "class": "pattern"
}
```
Ghi chú: đây là kết luận âm tính (absence of evidence) dựa trên tập trang đã fetch được trong phiên này, KHÔNG phải khảo sát toàn bộ docs.github.com/copilot. Hạ xuống confidence=medium vì phạm vi fetch có giới hạn.

---

## Trả lời trực tiếp 4 câu hỏi nhiệm vụ

1. **Văn phong/cấu trúc GitHub khuyến nghị:** Ngắn gọn (giới hạn cứng: "2 trang" theo trang repo-instructions, "~1000 dòng" theo trang code-review tutorial), viết bằng ngôn ngữ tự nhiên Markdown, heading + bullet, câu mệnh lệnh trực tiếp ngôi thứ 2 ("always", "avoid", "use"), không mơ hồ, không thụ động-hung hăng. Xem F1–F3, F6, F8, F9.

2. **Sample chính thức:** Không có 1 file copilot-instructions.md hoàn chỉnh "mẫu chuẩn" nào trên docs.github.com. Có 2 nguồn GitHub Blog với ví dụ SNIPPET thật: (a) đoạn "Project Overview" kiểu elevator-pitch trong bài 5-tips; (b) file typescript.instructions.md đầy đủ (naming/style/error-handling/testing) trong bài về code review. Xem F5, F7, F11.

3. **Cảnh báo lỗi thường gặp:** quá dài (giảm chất lượng phản hồi, có thể bị bỏ qua một phần), chỉ dẫn mơ hồ ("Be more accurate" bị liệt kê là không hỗ trợ), chỉ dẫn xung đột giữa personal/repo/org, yêu cầu vượt phạm vi cho phép (đổi UX/định dạng, đổi chức năng lõi, theo link ngoài), viết theo kiểu nhiệm vụ cụ thể thay vì hướng dẫn lâu dài ("must not be task specific"). Xem F2–F4.

4. **So với BMAD:** Không tìm thấy khuyến nghị persona ("You are X") hay activation-steps đánh số hay "one test decides" trong tài liệu chính chủ GitHub đã khảo sát. Khuyến nghị GitHub hoàn toàn khác kiểu: liệt kê SỰ THẬT/CONVENTION cụ thể của project (tech stack, cấu trúc thư mục, coding style) dưới dạng heading+bullet mệnh lệnh, xem Copilot như một "teammate mới cần onboard" bằng thông tin dự án — không đóng vai nhân vật. Đây là kết luận âm tính (absence pattern), confidence=medium, xem F12.
