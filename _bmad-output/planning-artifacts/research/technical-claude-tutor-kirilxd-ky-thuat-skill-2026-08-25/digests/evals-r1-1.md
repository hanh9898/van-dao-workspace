# Digest: claude-tutor (kirilxd) — evals/ và tests/test-hooks.js — R1.1

Nguồn: GitHub kirilxd/claude-tutor, branch `main` (mọi raw URL truy cập thành công ở lần thử đầu, không cần fallback `master`).
Ngày truy cập: 2026-08-25.

## 1. evals/evals.json — cấu trúc file

```json
findings = [
  {
    "claim": "evals.json có 3 key cấp cao nhất: skill_name (giá trị \"claude-tutor\"), trigger_evals (mảng test case cho định tuyến skill), functional_evals (mảng test case cho hành vi chức năng).",
    "source": "https://raw.githubusercontent.com/kirilxd/claude-tutor/main/evals/evals.json",
    "publisher": "GitHub (kirilxd/claude-tutor)",
    "pub_date": "N/A",
    "accessed": "2026-08-25",
    "confidence": "high",
    "class": "pattern"
  },
  {
    "claim": "Mỗi phần tử trong trigger_evals có 3 trường: id (số, quan sát thấy dải 1-17), prompt (chuỗi input người dùng), should_trigger (giá trị kỳ vọng: \"learn\", \"quiz\", \"review\", hoặc \"resources\"). Ví dụ: {\"id\": 1, \"prompt\": \"I want to learn kubernetes\", \"should_trigger\": \"learn\"}.",
    "source": "https://raw.githubusercontent.com/kirilxd/claude-tutor/main/evals/evals.json",
    "publisher": "GitHub (kirilxd/claude-tutor)",
    "pub_date": "N/A",
    "accessed": "2026-08-25",
    "confidence": "high",
    "class": "pattern"
  },
  {
    "claim": "Mỗi phần tử trong functional_evals có các trường: id (số, quan sát thấy dải 1-3), prompt (chuỗi lệnh, vd \"/learn DNS\"), setup_prompt (tuỳ chọn, hướng dẫn thiết lập ngữ cảnh test), depends_on (tuỳ chọn, tham chiếu phụ thuộc giữa các test), expectations (mảng chuỗi mô tả tiêu chí xác minh hành vi/đầu ra file kỳ vọng).",
    "source": "https://raw.githubusercontent.com/kirilxd/claude-tutor/main/evals/evals.json",
    "publisher": "GitHub (kirilxd/claude-tutor)",
    "pub_date": "N/A",
    "accessed": "2026-08-25",
    "confidence": "medium",
    "class": "pattern"
  }
]
```
Lưu ý: WebFetch trả về bản mô tả cấu trúc kèm ví dụ (đã qua một model trung gian tóm lược), không phải dump JSON thô đầy đủ 100% nguyên văn của toàn bộ mảng — vì vậy các trường được liệt kê ở mức tin cậy "high" cho khung cấu trúc, "medium" cho chi tiết functional_evals (setup_prompt/depends_on) vì có thể là optional field không xuất hiện ở mọi test case.

## 2. evals/run-trigger-eval.sh — trigger eval kiểm tra gì

```json
findings = [
  {
    "claim": "run-trigger-eval.sh kiểm tra đúng như giả thuyết: với mỗi prompt trong trigger_evals, script gọi `claude -p \"$prompt\" --plugin-dir ... --output-format stream-json --verbose --max-turns 1` (max-turns=1 để chỉ bắt bước định tuyến, không cho skill thực thi đầy đủ), sau đó tìm trong output JSON xem có \"name\":\"Skill\" và trường \"skill\" có khớp giá trị should_trigger hay không (dạng \"claude-tutor:learn\" hoặc \"learn\"); có fallback kiểm tra permission_denials nếu skill bị từ chối gọi. Đây chính là kiểm tra \"đúng input thì skill có được kích hoạt/route đúng không\".",
    "source": "https://raw.githubusercontent.com/kirilxd/claude-tutor/main/evals/run-trigger-eval.sh",
    "publisher": "GitHub (kirilxd/claude-tutor)",
    "pub_date": "N/A",
    "accessed": "2026-08-25",
    "confidence": "high",
    "class": "pattern"
  },
  {
    "claim": "Script khởi tạo bằng kiểm tra sự tồn tại của CLI `claude` và `jq`, đọc test case (id, prompt, should_trigger) trực tiếp từ evals.json, đếm PASS/FAIL/TOTAL, in tổng kết cuối cùng và trả về exit code 1 nếu có test fail.",
    "source": "https://raw.githubusercontent.com/kirilxd/claude-tutor/main/evals/run-trigger-eval.sh",
    "publisher": "GitHub (kirilxd/claude-tutor)",
    "pub_date": "N/A",
    "accessed": "2026-08-25",
    "confidence": "high",
    "class": "pattern"
  }
]
```

## 3. evals/run-functional-eval.sh — functional eval kiểm tra gì

```json
findings = [
  {
    "claim": "run-functional-eval.sh kiểm tra hành vi chức năng end-to-end (không chỉ routing): trước khi chạy, sao lưu ~/.claude/learning/ để bảo toàn dữ liệu hiện có. Gồm 5 test: (1) /learn DNS — tạo plan/index/profile, kiểm tra có modules[] và keyConcepts, fail nếu có field quizzes/weakAreas/spacedRepetition lẫn vào plan; (2) /quiz dns — gọi `claude -p` sinh 3 câu hỏi, mô phỏng trả lời, lưu tiến độ, kiểm tra progress file có quizzes[] và spacedRepetition, fail nếu dữ liệu quiz rò rỉ vào plans/; (3) /review — đọc index.json và progress/dns.json, kiểm tra output có đề cập DNS và hiển thị điểm số; (4) test path-enforcement hook — cố tình yêu cầu ghi quiz data vào plans/ (sai chỗ), pass nếu hook enforce-paths.js chặn thành công; (5) file integrity — xác nhận chỉ có file .json, không có file rác trong thư mục learning/.",
    "source": "https://raw.githubusercontent.com/kirilxd/claude-tutor/main/evals/run-functional-eval.sh",
    "publisher": "GitHub (kirilxd/claude-tutor)",
    "pub_date": "N/A",
    "accessed": "2026-08-25",
    "confidence": "high",
    "class": "pattern"
  },
  {
    "claim": "Cơ chế kiểm tra dùng jq -e (parse/assert JSON), grep -q/-l (tìm chuỗi trong output), ls và [ -f ] (kiểm tra tồn tại file). Điểm khác biệt với trigger eval: trigger eval chỉ kiểm tra skill có được gọi đúng tên (routing/pattern-matching), còn functional eval kiểm tra kết quả thật sau khi skill chạy xong — đúng file I/O, đúng vị trí thư mục, đúng schema dữ liệu, và đúng enforcement rule (hook chặn ghi sai chỗ) — khớp với giả thuyết \"skill chạy xong có đúng kết quả mong đợi không\".",
    "source": "https://raw.githubusercontent.com/kirilxd/claude-tutor/main/evals/run-functional-eval.sh",
    "publisher": "GitHub (kirilxd/claude-tutor)",
    "pub_date": "N/A",
    "accessed": "2026-08-25",
    "confidence": "high",
    "class": "pattern"
  }
]
```

## 4. README.md — mục "Known limitations" (trích NGUYÊN VĂN)

```json
findings = [
  {
    "claim": "README.md có mục cấp heading '##' tên 'Known limitations', nằm gần cuối README, ngay trước mục 'Uninstalling'. Nội dung nguyên văn dạng bảng gồm 3 dòng:\n1) 'Quiz formats' — 'Dashboard supports MCQ and True/False only. Short answer and fill-in-blank are CLI-only.'\n2) 'AskUserQuestion' — 'CLI may fall back to plain text depending on Claude Code version.'\n3) 'CLI schema drift' — 'Claude occasionally invents field names. Dashboard normalizes on read; hook blocks common errors.'",
    "source": "https://raw.githubusercontent.com/kirilxd/claude-tutor/main/README.md",
    "publisher": "GitHub (kirilxd/claude-tutor)",
    "pub_date": "N/A",
    "accessed": "2026-08-25",
    "confidence": "high",
    "class": "pattern"
  }
]
```
Lưu ý kỷ luật trích dẫn: nội dung trên do WebFetch (qua model trung gian) trả về đã ở dạng bảng tổng hợp cột "Limitation | Details" — có khả năng README gốc trình bày dạng bullet/heading phụ thay vì bảng markdown thật; cần đối chiếu lại bằng cách đọc trực tiếp file thô (không qua model tóm lược) nếu cần trích dẫn ký tự-cho-ký tự tuyệt đối (ví dụ để paste chính xác vào tài liệu chính thức). Độ tin cậy nội dung: high (3 giới hạn được liệt kê khớp nhau ở câu chữ cụ thể), nhưng định dạng trình bày (bảng vs heading con) ở mức medium.

## 5. tests/test-hooks.js — kiểm gì cho hooks

```json
findings = [
  {
    "claim": "test-hooks.js kiểm thử hook enforce-paths.js (path/schema enforcement cho thư mục học tập), bằng cách chạy hook qua execSync, truyền JSON vào stdin, và kiểm tra exit code (0 = cho phép ghi, 2 = chặn ghi) cùng nội dung stderr.",
    "source": "https://raw.githubusercontent.com/kirilxd/claude-tutor/main/tests/test-hooks.js",
    "publisher": "GitHub (kirilxd/claude-tutor)",
    "pub_date": "N/A",
    "accessed": "2026-08-25",
    "confidence": "high",
    "class": "pattern"
  },
  {
    "claim": "Các nhóm test case quan sát được: (1) 7 test chặn dữ liệu quiz/progress (field quizzes/weakAreas/spacedRepetition/overallScore) khi ghi vào plans/, kèm gợi ý đường dẫn progress/ đúng; (2) 3 test chặn dữ liệu plan (modules/resources/timeCommitment) khi ghi vào progress/; (3) 4 test cho phép ghi đúng chỗ (plan hợp lệ vào plans/, quiz/progress hợp lệ vào progress/, index.json và profile.json ở thư mục root); (4) 1 test bảo vệ thư mục root chặn file JSON ngẫu nhiên không nằm trong danh sách cho phép; (5) 2 test bỏ qua enforcement với đường dẫn ngoài learning/ (vd /tmp/, ~/.claude/settings.json); (6) 1 test hỗ trợ tool Edit qua field new_string thay vì content; (7) 8 test phát hiện lỗi schema (tên field sai như quiz_history/results/history, và overallScore phải là số phần trăm như 80 chứ không phải số thập phân như 0.8); (8) 4 test chặn đường dẫn tương đối/tuyệt đối sai vị trí dự án (learning/plans/, ./learning/progress/, đường dẫn tuyệt đối ngoài ~/.claude/), chỉ cho phép ghi trong ~/.claude/learning/.",
    "source": "https://raw.githubusercontent.com/kirilxd/claude-tutor/main/tests/test-hooks.js",
    "publisher": "GitHub (kirilxd/claude-tutor)",
    "pub_date": "N/A",
    "accessed": "2026-08-25",
    "confidence": "high",
    "class": "pattern"
  }
]
```

## Ghi chú phương pháp
- Tất cả 5 URL đều truy cập thành công trên branch `main` ngay lần thử đầu tiên — không cần fallback sang `master`.
- WebFetch xử lý nội dung qua một model tóm lược trung gian trước khi trả về cho agent này; với evals.json và README "Known limitations" nơi cần độ chính xác câu chữ tuyệt đối, nội dung trả về là bản diễn giải có trích dẫn cụm câu — không phải dump thô 1:1. Khuyến nghị: nếu bước downstream (vd viết vào đặc tả chính thức của Vấn Đạo) cần trích dẫn README nguyên văn ký tự-cho-ký tự, nên đọc lại raw file một lần nữa bằng công cụ không qua tóm lược (curl/Bash) để đối chiếu.
