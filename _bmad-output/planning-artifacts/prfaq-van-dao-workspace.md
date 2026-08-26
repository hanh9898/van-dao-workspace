---
title: "PRFAQ: Vấn Đạo"
status: "complete"
created: "2026-08-24"
updated: "2026-08-24"
stage: "5-verdict"
inputs: ["docs/VAN-DAO-dac-ta-v1.0.md", "docs/VAN-DAO-trang-thai-du-an.md", "AGENTS.md"]
---

# Vấn Đạo không dừng ở tóm tắt: giải thích đủ để bạn nắm ý, rồi hỏi ngược tới khi bạn dùng được thật

> *"What I cannot create, I do not understand."* — Richard Feynman
> *("Điều tôi không tự tạo ra được, tôi không thực sự hiểu nó.")* (trên bảng đen lúc mất, Caltech Archives — đã verify, không phải câu bị gán sai thường thấy trên mạng)

## Cho người tự học kỹ thuật cần hiểu đủ sâu để dùng thật ngay khi bước vào việc mới — không chỉ đọc lướt rồi quên.

**{City, Date}** — Vấn Đạo hôm nay có mặt dưới dạng một plugin cài vào Claude Code — công cụ dòng lệnh dùng AI Claude của Anthropic — biến bất kỳ cuốn sách kỹ thuật PDF hay EPUB nào bạn đã có sẵn thành một lộ trình học có AI đồng hành sát. Không cần tìm khoá học, không cần sách mới — Vấn Đạo đọc đúng cuốn sách của bạn, giải thích đủ để bạn nắm được ý chính, rồi hỏi ngược lại từng bước tới khi bạn tự áp dụng được kiến thức đó vào việc thật.

Người tự học kỹ thuật thường đọc xong một chương và thấy như đã hiểu — cho tới khi phải dùng nó vào việc thật thì mới lộ ra chỗ chưa nắm chắc. Tóm tắt AI đọc nhanh nhưng không kiểm tra bạn có hiểu hay không; gạch chân, ghi chú tay thì không ai đọc lại và phản hồi. Với người đang đổi nghề, một lỗ hổng kiến thức chỉ lộ ra khi đã ở trong công việc mới thì cái giá phải trả không hề nhỏ — và không có ai đứng cạnh để hỏi "vậy trong tình huống này thì làm sao".

Với Vấn Đạo, bạn không tự học một mình nữa. Mở sách, Vấn Đạo giải thích đủ để bạn nắm được khung ý chính của chương — không dài dòng, không giảng lại cả cuốn. Rồi thay vì chuyển sang chương tiếp theo, nó hỏi ngược lại đúng một điều tại một thời điểm, đợi bạn trả lời, chỉ ra chỗ bạn hiểu sai nếu có, và không cho bạn "qua" một chương chỉ vì bạn nhớ đúng chữ. Chỉ khi bạn thật sự làm được một bài kiểm tra đòi vận dụng vào tình huống mới — không phải nhắc lại định nghĩa — Vấn Đạo mới coi là bạn đã nắm.

### Cách hoạt động

Bạn cài Vấn Đạo vào Claude Code, rồi đưa vào một cuốn sách PDF hay EPUB bạn đã có sẵn — không cần đi tìm khoá học hay tài liệu mới. Vấn Đạo cho bạn biết trước sẽ mất khoảng bao lâu, bao nhiêu chương, trước khi thật sự bắt đầu.

Vào từng chương, Vấn Đạo giải thích đủ để bạn nắm được khung ý chính — ngắn gọn, không giảng lại cả chương. Sau đó, mỗi lượt nó chỉ đưa ra đúng một ý, hỏi bạn một câu, và đợi bạn trả lời trước khi đi tiếp. Trả lời sai hay mơ hồ, nó không chỉnh ngay đáp án — nó đổi cách giải thích khác và hỏi lại. Sau vài lượt như vậy, một AI khác — tách biệt với AI vừa dạy bạn — kiểm tra bạn có thật sự làm được không.

Hết một quyển, bạn làm một bài khảo thí đòi bạn vận dụng vào tình huống mới, không phải nhắc lại định nghĩa. Qua được, Vấn Đạo ghi nhận đây là lần đầu bạn thật sự nắm được cuốn sách đó — không phải "đã đọc xong", mà là "đã dùng được".

### Bắt đầu

Thêm marketplace của Vấn Đạo rồi cài plugin (`/plugin marketplace add ...` · `/plugin install van-dao@van-dao`), trỏ tới cuốn sách PDF/EPUB bạn đã có sẵn, và bắt đầu chương đầu tiên ngay trong phiên đó — đúng cách cài một plugin Claude Code thông thường. Mã nguồn mở, dùng chung tài khoản Claude Code bạn đã có — không cần đăng ký thêm gì. Sách và hồ sơ học tập không lưu trên server riêng nào của Vấn Đạo, chỉ ở lại trên máy bạn; nội dung được xử lý qua API Claude như mọi phiên Claude Code khác.

---

## Customer FAQ

### Q: NotebookLM đã làm quiz bám tài liệu, miễn phí, của Google. Vì sao tôi không dùng cái đó cho xong?

A: NotebookLM dừng lại ở quiz đúng/sai bám tài liệu. Vấn Đạo không cho bạn "qua" một chương chỉ vì trả lời đúng — nó đòi bạn vận dụng vào một tình huống mới, và một AI khác (tách biệt với AI vừa dạy bạn) kiểm tra độc lập, không tự dạy tự chấm cho qua. Nếu bạn chỉ cần ôn nhanh trước một cuộc họp, NotebookLM có thể đủ. Nếu bạn cần chắc chắn mình dùng được kiến thức đó trong công việc thật, đó là chỗ khác biệt.

### Q: "Hỏi ngược tới khi hiểu" nghe giống chatbot vặn vẹo khó chịu — nghiên cứu học thuật còn chưa chứng minh Socratic AI tutoring hiệu quả. Sao tôi tin đây không phải gimmick?

A: Thẳng thắn: hiệu quả của việc AI dạy kiểu Socratic vẫn là câu hỏi học thuật chưa ngã ngũ — chúng tôi không hứa nó "tốt hơn" cách khác. Điều chúng tôi hứa được và kiểm được: Vấn Đạo không công nhận bạn đã hiểu chỉ vì bạn trả lời đúng một câu — nó đòi một bài kiểm tra vận dụng, chấm bởi một AI độc lập với AI vừa dạy bạn. Đó là cam kết về cổng kiểm chứng, không phải cam kết phương pháp dạy là tối ưu.

### Q: Nếu tôi dùng ChatGPT/Cursor thay vì Claude Code thì sao?

A: Hiện tại Vấn Đạo chỉ chạy trên Claude Code. Chúng tôi đang cân nhắc mở rộng sang các nền tảng agent khác, nhưng chưa có cam kết thời điểm cụ thể — kiến trúc hiện tại gắn khá sâu vào cách Claude Code tổ chức nhiều AI thành các vai riêng biệt bên trong nó, nên chuyển sang nền tảng khác gần như phải dựng lại phần điều phối, không phải chỉ đổi cấu hình.

### Q: Cái "định vị cảnh giới 5 bậc theo Dreyfus" đó — có bằng chứng nào nó thật sự đúng, hay chỉ là con số nghe có vẻ khoa học?

A: Chưa có bằng chứng — đây là giả định đang kiểm chứng, không phải điều đã chứng minh. Tính năng này cũng **chưa có trong bản đầu**: nó cần dữ liệu từ ít nhất hai cuốn sách trên cùng một mạch kiến thức để so sánh, nên không thể hoạt động có ý nghĩa ngay ở cuốn sách đầu tiên bạn học — bạn sẽ không thấy nó khi mới bắt đầu dùng Vấn Đạo.

Khi tính năng này ra mắt: trước khi có đủ 20 mẫu chấm tay — 20 bài làm thật được cả AI và một người có chuyên môn chấm độc lập rồi so khớp kết quả — đạt mức đồng thuận đủ cao, Vấn Đạo sẽ không công bố bậc năng lực nào cả. Nó chỉ nêu dấu hiệu quan sát được ("bạn làm tốt ở chỗ này, còn yếu ở chỗ kia"), không gắn nhãn "bạn đang ở trình độ nào". Gắn nhãn sai còn tệ hơn không gắn nhãn.

### Q: Đây là dự án cá nhân một người. Ai đảm bảo còn được duy trì 6 tháng nữa, hay tôi bỏ công thu sách rồi nó chết?

A: Không có gì đảm bảo cả — đây là dự án cá nhân, mã nguồn mở. Nhưng chính vì mã nguồn mở, bạn không hoàn toàn phụ thuộc vào một người: sách và hồ sơ học tập của bạn luôn ở trên máy bạn, không khoá trong một dịch vụ đóng, và bất kỳ ai cũng có thể fork, tự sửa nếu dự án dừng lại.

### Q: Sách và câu trả lời của tôi trong lúc học có bị gửi đi đâu không? Ai đọc được?

A: Sách và câu trả lời của bạn ở lại trên máy bạn — không có server riêng của Vấn Đạo, không gửi telemetry. Việc xử lý (đọc sách, hỏi-đáp) đi qua Claude Code, dùng API của Claude như bất kỳ phiên làm việc Claude Code nào khác — không phải một kênh riêng của Vấn Đạo thu thập dữ liệu.

### Q: Nếu Vấn Đạo chấm sai — bảo tôi chưa hiểu trong khi tôi hiểu rồi, hoặc ngược lại — tôi làm gì?

A: Có cơ chế cho việc này: khi AI dạy và AI chấm độc lập bất đồng, hệ ghi lại thành một "cờ bất đồng" thay vì tự động xử lý — không nhánh nào chặn bạn tiếp tục học, nhưng bất đồng cũng không bị giấu đi, nó được ghi lại để xem xét và sửa dần. Cơ chế này có ngay từ bản đầu — nó là một phần của việc kiểm tra khi hết một quyển, không phải tính năng thêm sau.

### Q: Sách của tôi không phải sách lập trình mà là sách nghiệp vụ, ví dụ BABOK (cẩm nang kiến thức ngành phân tích nghiệp vụ — business analysis) — có dùng được không?

A: Có — Vấn Đạo không giới hạn theo ngành. Trên thực tế, BABOK là một trong những nguồn tham khảo khi thiết kế chính cơ chế đánh giá của Vấn Đạo, nên đây đúng loại sách nó được nghĩ tới ngay từ đầu.

---

## Internal FAQ

### Q: Cái khó nhất về kỹ thuật — thứ chưa biết cách dựng — là gì?

A: Không phải một vấn đề kỹ thuật thông thường (viết sai thì sửa) — mà là hai giả định nền chưa kiểm chứng: (1) model chấm đúng bài vận dụng theo rubric, (2) model đọc được cảnh giới người học từ văn bản. §17 đặc tả tự nhận: nếu sai, phải dựng lại từ §1. Chưa có cách kiểm ngoài dùng thật — đây là chỗ chưa biết liệu nền tảng ý tưởng có đứng vững, không phải chỗ chưa biết cách code.

### Q: Timeline thực tế tới bước 8 (tự bế quan một quyển thật — giá trị đầu tiên) là bao lâu?

A: Không nêu số ngày/tuần — đúng luật đã tự đặt (AGENTS.md: không ước lượng thời gian, AI đã đổi tốc độ phát triển). Trả lời bằng chuỗi mốc phụ thuộc: bước 3 (`giam-dinh.py` + skill `thu-bi-kip`) → bước 4 (thu một quyển thật) → bước 5+5b (skill `thu-linh` + `kiem-thu.py` bản đầu) → bước 6 (`nghiem-cong`) → bước 7 (`nhap-mon`/`dao-tam`, song song) → bước 8 (tự bế quan). Mỗi bước xong mới biết bước sau mất gì.

### Q: Để tới bước 8, phải nói KHÔNG với cái gì trong 34 requirement / 28 component đã "đóng"?

A: Toàn bộ Bậc 2 (`ha-son`, `phuc-menh`, đạo tâm, `mach.schema.md`, `tra-tang-kinh-cac`, `ban-do.py`) — đều là cơ chế cho nhiều quyển/nhiều mạch, chưa cần khi mới có một quyển. Trong Bậc 3, giữ ngoài phạm vi: `truong-lao`/κ-calibration/`thoai-canh.py`/`canh-gioi.md` (định vị cảnh giới — cần ≥2 nguồn theo R10, không dựng được có ý nghĩa với một quyển).

**Sửa một chỗ xếp sai phát hiện khi soát PRFAQ này:** `phuc-khao` (người soát thứ hai, đúng cơ chế "cờ bất đồng" đã hứa ở Customer FAQ) từng bị gắn nhầm mác Bậc 3 trong đặc tả — thật ra cần ngay từ bước 8, và §16 (thứ tự dựng thật) vốn đã đặt nó ở Vòng 2, không phải Vòng 4. Đã sửa lại đúng bậc trong đặc tả (§13.1). R11 tự nhiên giữ trưởng lão im lặng về bậc cho tới khi đủ mẫu, nên phần cảnh giới không cần cấm thêm gì bằng lời — hệ tự trì hoãn đúng phần chưa cần.

### Q: Cái gì thật sự giết chết dự án này?

A: Mất hứng sau khi dựng xong — đúng rủi ro `trang-thai-du-an.md` tự nhận, không phải rủi ro kỹ thuật. Rủi ro kỹ thuật (giả định nền sai) có đường xử lý (dựng lại từ §1); rủi ro động lực thì không có cơ chế nào chống được ngoài kỷ luật của chính người dựng.

### Q: Một mình bạn bảo trì được bao lâu khi có người dùng khác báo lỗi hoặc đòi tính năng?

A: Không hứa SLA. README sẽ nói rõ: best-effort, không cam kết thời gian phản hồi, khuyến khích tự gửi PR — đúng chuẩn mã nguồn mở cá nhân, không giả vờ có đội ngũ đứng sau.

### Q: Người đầu tiên ngoài bạn biết tới và cài Vấn Đạo bằng cách nào?

A: Chưa có kế hoạch. Chưa nghĩ tới phân phối hay marketing gì cả — không giả vờ có chiến lược chưa tồn tại.

### Q: Vừa cài `book-to-skill` làm dependency hôm nay — nếu họ đổi API hay ngừng bảo trì thì sao?

A: Rủi ro thấp, chấp nhận được. Hai lớp cài tách biệt (pip engine cho giám định, skill riêng cho Pha 1), MIT license nên fork được nếu cần. Chưa pin version cụ thể — cần thêm vào `requirements-dev.txt` khi viết code thật ở bước 3.

### Q: Câu bạn ngại nhất, chưa ai nói thành lời: nếu tự bế quan xong quyển đầu mà thấy Vấn Đạo không hơn gì việc tự đọc rồi hỏi ChatGPT — bạn có tiếp tục dựng không?

A: Có — đó chính là lý do bước 8 tồn tại. Nếu thất bại, đó là dữ liệu quý, không phải thất bại của dự án: đúng nguyên tắc "không viết thêm design cho tới khi có executable spec" áp ngược lại cho chính ý tưởng gốc — bước 8 chính là bài kiểm executable-spec cho toàn bộ giả thuyết sản phẩm, không chỉ cho kiến trúc.

---

## The Verdict

**Đánh giá chung:** Ý tưởng đủ cứng để bắt tay dựng bước 3, không đủ cứng để coi các câu trả lời hôm nay là đã được xác nhận bởi ai ngoài chính người tạo ra nó. Phần tư duy sắc nhất nằm ở khả năng tự phát hiện và sửa lỗi ngay trong lúc làm (kiến trúc thiếu Supportive Information, quote sai gán, câu trả lời hứa quá cơ chế thật) — đó là dấu hiệu tốt hơn bất kỳ câu trả lời hoàn hảo nào. Phần mềm nhất nằm ở đúng chỗ đặc tả gốc đã tự cảnh báo: đặc tả dày, bằng chứng mỏng.

### Forged in steel

- **Khác biệt với NotebookLM/book-to-skill là thật, không phải marketing.** Đã verify trực tiếp: book-to-skill là hệ tra cứu thuần, không quiz không Socratic. NotebookLM dừng ở quiz đúng/sai. Cơ chế "không cho qua chỉ vì trả lời đúng — chấm độc lập" là khác biệt cụ thể, kiểm được, không phải tính từ ("tốt hơn", "thông minh hơn").
- **Trả lời về dữ liệu/quyền riêng tư chính xác, có cơ sở kiến trúc thật** (local storage, không telemetry) — không phải lời hứa suông.
- **Cách xử lý câu hỏi về bằng chứng Dreyfus biến điểm yếu thành kỷ luật đáng tin** — thẳng thắn "chưa có bằng chứng", nhưng nối đúng vào cơ chế đã có sẵn (R11, gate κ) thay vì né tránh hay phồng lên.
- **Epigraph Feynman xác thực, đúng chủ đề** — quá trình tìm ra và loại bỏ câu bị gán sai là một bằng chứng tốt cho kỷ luật "không bịa" đã được giữ xuyên suốt.

### Needs more heat

- **Pha Supportive Information (tóm lược trước Socratic) mới chỉ là ý tưởng đúng hướng, chưa có thiết kế.** Không có bước nào trong F-flow hiện tại, chưa biết co giãn theo cảnh giới cụ thể ra sao. Cần thiết kế thật trước khi viết vào đặc tả, không chỉ nhắc trong PRFAQ.
- **"Chưa có kế hoạch" cho người dùng đầu tiên và bảo trì là trung thực nhưng mỏng.** Chấp nhận được cho pha hiện tại (trước bước 8), nhưng nếu thật sự "cho cả người khác" như đã chốt ở Stage 1, đây là việc phải quay lại trước khi mời ai cài thử.
- **Persona xác nhận (dev chuyển BA) chỉ có một, do chính người tạo tưởng tượng ra, chưa ai khác xác nhận nó đúng.** Đủ để định hướng thiết kế, chưa đủ để khẳng định có nhu cầu thật ngoài kia.

### Cracks in the foundation

- **Mâu thuẫn "khoá Claude Code" chưa giải quyết, chỉ tạm gác.** Customer FAQ trả lời "giữ cửa mở, đang cân nhắc mở rộng" — nhưng kiến trúc thật sự phụ thuộc sâu vào cơ chế riêng của Claude Code. Nếu có người dùng thật đọc FAQ này rồi hỏi "khi nào có ChatGPT?", câu trả lời hiện tại không đứng vững lâu. Đây là quyết định kiến trúc cần chốt thật, không phải câu FAQ khéo léo.
- **Hai giả định nền chưa kiểm vẫn là rủi ro cao nhất, không đổi qua cả quá trình PRFAQ.** Toàn bộ giá trị của sản phẩm treo vào việc model chấm đúng bài vận dụng và đọc đúng cảnh giới từ văn bản — chưa có cách kiểm nào ngoài chạy thật ở bước 8.
- **"Giải pháp đi tìm vấn đề" — chưa được bác bỏ, chỉ được trả lời bằng lý lẽ, không phải bằng chứng ngoài.** Toàn bộ Customer FAQ hôm nay là founder tự đóng vai khách hàng khó tính rồi tự trả lời — chưa có một người thật, không phải người tạo, đọc thông cáo này và phản ứng. Nghiên cứu thị trường đã cảnh báo thẳng: chưa có bằng chứng nhu cầu thật cho tự-đánh-giá Dreyfus 5 bậc. PRFAQ làm tốt việc siết chặt tư duy nội bộ — nó không thay được việc đưa cho một người dev-chuyển-BA thật đọc và hỏi "vậy tôi có dùng không".

**Khuyến nghị:** Đi bước 3 (giam-dinh.py + thu-bi-kip) — đủ cứng để bắt đầu, và bước 8 tự nó là phép thử cho phần lớn "cracks" ở trên. Nhưng đừng đợi tới bước 8 mới hỏi một người thật (không phải bạn) có đọc xong thông cáo này mà muốn dùng không — càng sớm càng rẻ để biết trước khi đổ thêm công sức.

---

<!-- coaching-notes-post-verdict -->

## Coaching notes — sau Verdict (review lens `naive-reader` + sửa xếp bậc)

- Sau khi PRFAQ "hoàn tất", chạy thêm lens tự tạo `naive-reader` (subagent hoàn toàn mới, chỉ đọc đúng file PRFAQ, không đọc gì khác) — đúng cách bmad-review vẫn dùng, áp cho tài liệu chưa từng thử ở phiên trước. Ra 11 finding, verify 2 cái tải trọng cao nhất khớp 100% với file thật trước khi tin.
- 9/11 finding là sửa mechanical (đã áp dụng): giải thích "Claude Code"/"skill" lần đầu nhắc; dịch epigraph Feynman; sửa "không gửi đi đâu" chỏi với việc đi qua API Claude; sửa "tài khoản riêng" mơ hồ; gỡ jargon "subagent/hook" khỏi câu trả lời khách hàng; chú thích BABOK; làm rõ "20 mẫu" là gì.
- 2 finding còn lại là quyết định thật, không phải lỗi chính tả:
  1. **"Người" → "AI agent" xuyên suốt** — người dùng chọn trung thực tuyệt đối thay vì giọng ấm áp mơ hồ.
  2. **Dreyfus/cảnh giới xuất hiện ở FAQ mà Press Release chưa từng giới thiệu** — dẫn tới phát hiện lớn hơn dự kiến: khi soát lại xem Bậc 1/2/3 có còn hợp lý cho phạm vi bước 8, lộ ra `phuc-khao` (#20b) từng bị gắn nhầm mác Bậc 3 trong §13.1, trong khi §16 (thứ tự dựng thật) đã đặt nó ở Vòng 2 từ trước — **đúng lỗi mà lens `adversarial` từng nêu ở lần review kiến trúc trước, lúc đó ghi nhận rồi để đó vì ngoài phạm vi.** Đã sửa thật trong đặc tả (`docs/VAN-DAO-dac-ta-v1.0.md` §13.1): `phuc-khao` dời sang Bậc 1 (#11d). `truong-lao`/cảnh giới (#19) xác nhận đúng là ở ngoài phạm vi bước 8 — không phải cắt giảm tuỳ tiện, mà vì R10 đòi ≥2 nguồn, không dựng có ý nghĩa được với một quyển.
- Bài học phương pháp: dùng subagent hoàn toàn mới (không phải fork kế thừa ngữ cảnh) để review "góc nhìn người lần đầu" là đúng — người viết ra tài liệu (kể cả coach) không phải người phù hợp để tự đánh giá độ rõ ràng của chính nó.

<!-- coaching-notes-stage-4 -->

## Coaching notes — Stage 4 (Internal FAQ)

- 8 câu, tất cả chọn qua tool — toàn bộ đều chọn đúng phương án đề xuất của coach (khác Stage 3, nơi có 1 câu lệch đề xuất).
- Phát hiện đáng giữ: R11 (đặc tả sẵn có) tự động trả lời câu "nói không với gì" — không cần một quyết định roadmap mới, chỉ cần NHẬN RA cơ chế chặn công bố cảnh giới đã tự làm việc trì hoãn Bậc 2/3 "miễn phí".
- Câu "founder ngại nhất" (bước 8 không hơn ChatGPT) được xác nhận tiếp tục dựng dù thất bại — nhất quán với toàn bộ triết lý "executable spec quyết định, không phải đọc lại tài liệu" đã dùng xuyên suốt dự án.
- Timeline và người dùng đầu tiên đều trả lời kiểu "chưa biết/chưa có kế hoạch" — trung thực nhưng đáng lưu ý cho Stage 5 Verdict: đây có phải launch blocker hay chấp nhận được cho một dự án cá nhân giai đoạn này.

<!-- coaching-notes-stage-3 -->

## Coaching notes — Stage 3 (Customer FAQ)

- 8 câu hỏi, không câu nào là CTA trá hình — 4 câu quyết định qua tool chọn (NotebookLM, gimmick, khoá Claude Code, bằng chứng Dreyfus), 4 câu còn lại soạn thẳng vì mang tính sự kiện (dữ liệu, duy trì, chấm sai, sách nghiệp vụ).
- **Quyết định KHÔNG theo đề xuất của coach:** câu "khoá Claude Code" — người dùng chọn "giữ cửa mở, đang cân nhắc mở rộng" thay vì "thẳng, có chủ đích, không hứa đa nền tảng" (đề xuất ban đầu). Đã viết câu trả lời không hứa lộ trình cụ thể để tránh nợ chưa trả được — nhưng đây là tín hiệu thật: người dùng nghiêng về hướng đa nền tảng, đúng như tranh luận gác lại ở Stage 1. **Cần quay lại quyết định kiến trúc này sau PRFAQ, không phải chuyện đã xong.**
- Câu Dreyfus: chọn đúng đề xuất minh bạch toàn bộ — biến giả định chưa kiểm thành minh chứng kỷ luật (nối đúng R11 đã có sẵn trong đặc tả, không phải bịa thêm).
- Phát hiện tốt khi soạn: BABOK đã có sẵn trong nguồn tham khảo đặc tả (§19.3) — trả lời câu "sách nghiệp vụ có dùng được không" mà không cần bịa, chỉ cần trích đúng cái đã có.

<!-- coaching-notes-stage-2 -->

## Coaching notes — Stage 2 (Press Release)

- Headline chốt ở bản B sau 3 phương án — 2 bản loại vì hứa suông ("thật sự hiểu" không đo được) hoặc bỏ sót pha Supportive Information mới thêm.
- Epigraph Feynman: bản phổ biến "if you can't explain it simply..." bị verify là **gán sai cho Feynman** (không có nguồn) — tránh dùng. Dùng bản đã verify "What I cannot create, I do not understand." (bảng đen lúc mất, Caltech Archives).
- Leader quote (lời hanhnt2) — soạn nháp rồi **bỏ hẳn** theo yêu cầu người dùng: chỉ giữ epigraph Feynman, không dùng quote khác.
- Customer quote minh hoạ (fictional) — đề xuất ban đầu, **bị từ chối** vì "cấm bịa quote" — thay bằng epigraph có nguồn thật thay vì trích dẫn khách hàng giả.
- Cắt "Vấn Đạo đọc thử trước, báo nếu không rút được chữ" khỏi How It Works — theo yêu cầu người dùng: chi tiết xử lý lỗi không phải giá trị cốt lõi, có thể cải thiện dần, không đáng nhấn mạnh trong thông cáo.
- Tự sửa "cuối chương, một người chấm khác chấm bài" → "sau vài lượt, một người chấm khác kiểm tra" — vì R23 xác nhận: bỏ qua nghiệm công ở một chương vẫn tính đã qua, không chặn. Câu gốc hứa nhiều hơn cơ chế thật cho phép.
- Cân nhắc rồi bỏ "chạy hoàn toàn trên máy bạn" ở Getting Started — không chính xác (Claude Code vẫn gọi API qua mạng); chỉ dữ liệu ở lại máy, không phải toàn bộ xử lý.

<!-- coaching-notes-stage-1 -->

## Coaching notes — Stage 1 (Ignition)

**Concept type:** Open-source Claude Code skill/plugin, cài đặt cá nhân riêng lẻ (không cộng tác/multiplayer, không SaaS multi-tenant). Không có "unit economics" — khung đánh giá phải dựa trên adoption path và giá trị cho từng người dùng cá nhân.

**Giả thuyết ban đầu (do coach nêu, người dùng chưa xác nhận):**
- Vấn đề: người tự học kỹ thuật một mình, có sách nhưng không có ai hỏi ngược lại để kiểm tra hiểu thật hay chỉ nhớ mặt chữ
- Giải pháp: 8 vai AI (thế giới quan tu tiên) dạy kiểu Socratic bám đúng một cuốn sách đã có, không giảng — hỏi dẫn dắt, khảo thí, định vị năng lực theo thang Dreyfus 5 bậc
- Khách hàng: ban đầu là chính tác giả; xác nhận muốn mở rộng cho người khác dùng cá nhân riêng lẻ, nhưng **chưa mô tả được một persona cụ thể không phải bản thân** — đang chờ câu trả lời

**Artifact Analyzer — phát hiện chính** (quét `docs/VAN-DAO-dac-ta-v1.0.md`, `docs/VAN-DAO-trang-thai-du-an.md`, `AGENTS.md`):
- Phạm vi tường minh trong đặc tả: "Người dùng cần thoả mãn: chính tác giả (n=1)" — mở nguồn là chia sẻ, KHÔNG phải mục tiêu chiếm thị trường
- 2 giả định nền "Cao" rủi ro, chưa kiểm: (1) model chấm được bài vận dụng theo rubric, (2) model đọc được cảnh giới từ văn bản người học
- Rủi ro số 1 tự nhận đã ĐỔI: từ "đặc tả chưa đủ chín" sang "đặc tả quá lớn/quá chín so với bằng chứng" (2.112 dòng, 34 requirement, 28 component cho một người dùng chưa học xong chương nào)
- Cột giá trị (value) vẫn 0% — chưa ai dùng thật
- Điểm tự nhận thiếu so với 5 plugin đối chiếu: không có lịch lặp giãn cách (SM-2/FSRS)
- Ý tưởng đã cân nhắc rồi loại: Claude Code "agent teams" (còn thử nghiệm); tham số "N tháng thoái cảnh" (thay bằng "định lại không có căn cứ mới")

**Web Researcher — phát hiện chính** (bối cảnh cạnh tranh, thời điểm 2026):
- **Đối thủ gần nhất về mặt sản phẩm:** *Book2Course V2* (web app, ra mắt HN) — PDF → khoá học tương tác, quiz + AI tutor bám sách. Phản hồi launch thật: "template-like", "quiz quá hời hợt", "thiếu chiều sâu" — bằng chứng cụ thể rằng làm tốt bài toán này khó, và người dùng phát hiện sự hời hợt rất nhanh.
- **book-to-skill** (đã xác nhận qua đọc README thật): chỉ là hệ tra cứu/tham chiếu — KHÔNG có quiz, KHÔNG Socratic, KHÔNG đo năng lực → xác nhận khác biệt sư phạm Vấn Đạo tuyên bố là có thật so với công cụ này cụ thể.
- **claude-tutor**, **AI-learning-skill** (một trong hai tự nhận "Socratic dialogue") — tương đồng chức năng gần nhất trong hệ sinh thái Claude Code, nhưng tổng quát theo chủ đề, không khoá vào một cuốn sách cụ thể.
- **agent-tutor-skill** — "zero-hint quiz, theo dõi mastery cấp khái niệm" — gần nhất với "định vị năng lực" nhưng không dựa Dreyfus, không bám sách.
- **NotebookLM** (Google, miễn phí, đại chúng) đã ra mắt Quizzes/Flashcards/"Learning Guide" tutor mode (9/2025), bám nguồn tải lên — đây là **baseline** thị trường sẽ so sánh Vấn Đạo vào, không phải các skill Claude Code nhỏ lẻ.
- **Khoảng trống thời cơ:** chưa ai gộp cả 3 trụ cột cùng lúc — (a) chỉ đúng một cuốn sách, (b) từ chối tóm tắt/giảng, (c) định vị Dreyfus 5 bậc tường minh. Từng mảnh đã có ai đó làm riêng lẻ, nhưng khoảng trống **hẹp**, không rộng.
- **Rủi ro nêu thẳng:** (1) chưa có bằng chứng nhu cầu thật cho tự-đánh-giá Dreyfus 5 bậc ở lập trình viên tự học — "rủi ro là giải pháp đi tìm vấn đề"; (2) hiệu quả Socratic AI tutoring vẫn là câu hỏi học thuật chưa ngã ngũ (2025-26); (3) trần phân phối — chỉ chạy Claude Code, trong khi NotebookLM miễn phí/đại chúng đã phủ một phần chức năng cho tệp người dùng lớn hơn nhiều, chi phí chuyển đổi bằng 0.

**Persona chốt (Stage 1 hoàn tất):** dev đang chuyển hướng làm BA. Cần đọc nhiều sách chuyên môn mới trong thời gian ngắn (áp lực đổi nghề), nhưng không chỉ để "biết" — cần hiểu đủ sâu để áp dụng thật vào công việc BA sắp làm. Một người, hai nhu cầu nối tiếp (không phải hai persona khác nhau): trước tiên nắm ý cơ bản nhanh, sau đó đào sâu/áp dụng.

**Điều chỉnh khái niệm quan trọng phát sinh từ Stage 1:** ban đầu định vị "không tóm tắt, không giảng — chỉ hỏi" bị chính persona bác bỏ (rủi ro làm người học bỏ chạy, đúng như web-researcher cảnh báo). Đã sửa: Vấn Đạo cần thêm pha **Supportive Information** (giải thích/tóm lược khái niệm) trước pha Socratic — đúng thành phần thứ 2 trong 4 thành phần của 4C/ID (van Merriënboer), khung đã được chính đặc tả trích dẫn nhưng chưa triển khai đủ. Xác nhận qua tra cứu trực tiếp 4cid.org. Lượng Supportive Information nên co giãn theo cảnh giới người học (nhiều lúc mới, giảm dần khi lên cao) — khớp luật sẵn có ở §7.1 "giàn giáo dày lên giữa chừng". **Đây là mở rộng phạm vi kiến trúc thật, chưa thiết kế — việc cần làm sau khi PRFAQ xong, không phải trong 34 requirement hiện có.**

**Tranh luận chưa giải quyết, gác lại — không phải bỏ qua:** người dùng cho rằng sản phẩm nên "cắm vào đâu cũng được" (không khoá 1 hãng AI). Coach ban đầu phản bác sai (dẫn chứng sai rằng book-to-skill/BMAD khoá 1 hãng — đã tự sửa, cả hai đều đa nền tảng thật). Kiến trúc Vấn Đạo hiện tại phụ thuộc sâu vào cơ chế riêng của Claude Code (subagent tươi không fork — R9, hook SessionStart/SubagentStop, `.pham-vi.json`) — đa nền tảng đòi dựng lại tầng điều phối, không phải đổi cấu hình. Chưa chốt hướng — cần bàn riêng sau PRFAQ, không phải quyết định vội trong ignition.

**Đối thủ đáng nhớ khi viết Customer FAQ / Internal FAQ:** NotebookLM (baseline miễn phí, đại chúng) và Book2Course (bằng chứng thất bại thật khi làm quiz hời hợt).
