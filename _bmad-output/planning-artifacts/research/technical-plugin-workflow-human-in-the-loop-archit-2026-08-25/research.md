---
title: 'technical research: Kiến trúc plugin điều phối quy trình nhiều bước có human-in-the-loop'
type: 'technical'
topic: 'Cách viết một plugin chuẩn mực cho một quy trình, có human-in-the-loop'
decision: 'Vấn Đạo nên theo mẫu hình kiến trúc nào cho một plugin Claude Code điều phối quy trình nhiều vai/nhiều bước, có nhiều điểm người dùng can thiệp/duyệt giữa chừng — feed vào architecture spine cho bước dựng tiếp theo'
source: 'run'
status: complete
preset: 'standard'
validation: 'normal'
created: '2026-08-25'
updated: '2026-08-25'
claims_verified: 17
claims_unverified: 1
---

# technical research: Kiến trúc plugin điều phối quy trình nhiều bước có human-in-the-loop

**Decision this research serves:** Vấn Đạo nên theo mẫu hình kiến trúc nào cho một plugin Claude Code điều phối quy trình nhiều vai/nhiều bước, có nhiều điểm người dùng can thiệp/duyệt giữa chừng — feed vào architecture spine cho bước dựng tiếp theo.

## 1. Tóm tắt điều hành

**Vấn Đạo đã chọn đúng hướng, và giờ có bằng chứng thật để nói vậy — không phải trực giác.** Bằng chứng hội tụ mạnh nhất trên cả 4 chiều nghiên cứu: **ít điểm duyệt, đặt đúng chỗ hệ trọng, luôn thắng gác cổng dàn trải** — chính hệ đa-agent sản xuất thật của Anthropic (Claude Research) tập trung con người vào kiểm tra edge-case chứ không giám sát từng bước [8]; một khảo cứu platform-engineering 2026 gọi "mọi hành động đều cần ký duyệt" là kiểu thất bại đầu tiên trong 3 kiểu đã đặt tên [15]; 4 chuyên gia độc lập (IT Brew) đều nói cần "điểm ma sát có chủ đích ở bước hệ trọng", không phải duyệt dàn trải [23]. Thiết kế hiện tại của Vấn Đạo (FR6 duyệt lộ đồ, FR12a-b cờ bất đồng, FR15 xác nhận suy đoán — chỉ gác ở vài mốc hệ trọng) đã khớp mẫu hình được ủng hộ mạnh nhất, không cần đổi hướng.

**Phát hiện mới quan trọng nhất, đáng hành động ngay:** một rủi ro triển khai thật, được 3 nguồn độc lập báo cáo trong vòng 2 tháng gần đây (block/buzz, OpenAI Codex, openclaw) — **một lượt duyệt có thể "thiu" nếu trạng thái nó đang duyệt thay đổi trong lúc chờ** [18][25][26]. Đây không phải rủi ro lý thuyết. FR6 (duyệt lộ đồ) và các mốc xác nhận sau này của Vấn Đạo cần một cách kiểm tra "phiên bản đã duyệt còn khớp phiên bản hiện tại không" trước khi coi lượt duyệt là hợp lệ.

**Phát hiện có thể dùng ngay, không cần tự phát minh:** Claude Code **đã có sẵn** đúng cơ chế Vấn Đạo cần — hệ thống permission mode và Hooks (`PreToolUse`, `PermissionRequest`, `PermissionDenied`, `PostToolBatch`) [27][28] — và GitHub Copilot SDK hội tụ độc lập về đúng cơ chế đó (`onPreToolUse`/`onPostToolUse`) [33], một tín hiệu chéo-hãng đáng tin cậy cho thấy đây không phải điều riêng của Claude Code mà đang thành hình dạng chuẩn cho HITL ở tầng plugin.

**Cảnh báo lớn nhất:** phần lớn phát hiện ở tầng "workflow engine backend" (LangGraph, Temporal, AWS Step Functions) — dù đúng và hữu ích — **không phải hình dạng gần nhất với Vấn Đạo**, vốn là một plugin CLI, không phải dịch vụ backend. Vòng 2 đã lấp phần lớn khoảng trống này bằng khảo sát trực tiếp các công cụ dev cùng loại (Claude Code, Cline, Cursor, Copilot, Aider, VS Code) — nhưng vẫn còn khoảng trống nhỏ (JetBrains, nhánh bình luận cline#12959) — xem §6.

## 2. Theo từng chiều

### 2.1 Toàn cảnh & độ trưởng thành (Landscape & maturity)

Tầng giao thức/khả năng tương tác của hệ sinh thái AI-agent đang hội tụ về chuẩn trung lập nhà cung cấp: MCP (truy cập tool/context) và A2A (agent-tới-agent) đều đã được Agentic AI Foundation của Linux Foundation quản trị từ tháng 12/2025 [1][2][3]; A2A báo cáo hơn 150 tổ chức hỗ trợ, đã triển khai sản xuất thật ở nhiều ngành, tính tới mốc 1 năm [4][5]. Ngược lại, tầng framework ứng dụng vẫn đang cạnh tranh gay gắt — LangGraph, CrewAI, Microsoft Agent Framework (hợp nhất từ AutoGen + Semantic Kernel), Google ADK chưa có người thắng rõ ràng [9] (độ tin trung bình, chỉ 1 nguồn tổng hợp).

Cho riêng human-in-the-loop, hai cơ chế lặp lại xuyên suốt hệ sinh thái: `interrupt()`/checkpointer của LangGraph [6] và cơ chế Signal dựa trên durable execution của Temporal [7][11] — cả hai coi "dừng chờ người" là nguyên thuỷ hạng nhất, không phải chắp vá thêm sau. Hệ đa-agent sản xuất thật của chính Anthropic (Claude Research) là điểm tham chiếu đáng chú ý nhất: dùng cấu trúc orchestrator-worker với ngữ cảnh subagent cô lập, và — quan trọng — **tập trung con người vào kiểm tra edge-case/đánh giá, không giám sát liên tục từng bước** [8]. Đây là bằng chứng trực tiếp liên quan tới thiết kế nhiều vai, nhiều mốc duyệt của Vấn Đạo: ngay cả hệ nội bộ chủ lực của Anthropic cũng chọn ít điểm chạm người dùng hơn, đặt đúng chỗ, thay vì gác cổng khắp nơi.

### 2.2 Mẫu hình kiến trúc trong thực tế (Architecture patterns in practice)

Ba cơ chế cụ thể thống trị cho "dừng chờ người": `interrupt()` + checkpointer của LangGraph [6], mẫu callback (`waitForTaskToken`) của AWS Step Functions [12], và tổ hợp Signal + Timer bền của Temporal [7][11]. Cả ba chia sẻ một chi tiết triển khai không hiển nhiên nhưng quan trọng: **khi resume, đơn vị công việc bị ngắt chạy lại TỪ ĐẦU, không phải từ điểm ngắt** — LangGraph ghi rõ điều này cho node của nó [6], nghĩa là bất kỳ bước nào có side-effect ngoài (gọi API, ghi file, ghi DB) đặt trước một điểm duyệt người phải được viết để chịu được chạy lại — một người thực hành độc lập xác nhận đúng gánh nặng này trong thực tế, và nói thêm một lỗi liền kề: gộp lẫn trạng thái ngắn hạn của checkpointer với tầng bộ nhớ dài hạn là nguyên nhân phổ biến gây "quên" ngữ cảnh ngay qua điểm dừng HITL [20].

Mẫu Saga (với giao dịch bù trừ) là câu trả lời chuẩn cho ngữ nghĩa rollback trong workflow nhiều bước [13], và các engine durable-execution nói chung (Temporal, Restate, Conductor-OSS, Azure Durable Functions) chia sẻ một trừu tượng checkpoint/resume chung [14].

Phát hiện đáng hành động nhất ở chiều này là 3 kiểu thất bại đã đặt tên tại chính điểm duyệt người, từ một khảo cứu platform-engineering 2026 [15]:

1. **Thiết kế vì sợ hãi** — mọi hành động đều cần ký duyệt, thông lượng sụp đổ, và trong vòng một quý ai đó sẽ âm thầm tắt cổng khi giám sát trở nên bất tiện.
2. **Duyệt hình thức (rubber-stamp)** — khi ~98% lượt duyệt đều ổn, người duyệt ngừng đọc, và cổng trở thành độ trễ không có giám sát thật.
3. **Thiết kế chỉ-đồng-bộ** — duyệt bị chặn theo thời gian phản hồi của người (có thể qua đêm/cuối tuần) sẽ mất trạng thái ngay lần đầu không ai theo dõi, trừ khi trạng thái bên dưới là bền (durable).

Điều này được củng cố cùng chiều (dù không có dữ liệu cứng độc lập) bởi lập luận của một hãng an ninh mạng ủng hộ "human-on-the-loop" (kiểm tra ngẫu nhiên/audit) thay vì "human-in-the-loop" cho triage khối lượng lớn [16], và có nền tảng học thuật trong "thiên kiến tự động hoá" (Goddard, Roudsari & Wyatt 2012) và "Ironies of Automation" của Bainbridge (1983) [17] — người được giao "giám sát" một hệ tự động thường ngừng tự kiểm chứng nó.

### 2.3 Thực tế triển khai (Implementation reality)

Một trích dẫn thứ cấp từ báo cáo "State of Agent Engineering 2026" của LangChain khẳng định hơn 60% sự cố agent AI sản xuất thật bắt nguồn từ lỗi quản lý trạng thái — bao gồm cả trạng thái dừng/resume của HITL — nhưng nguồn gốc chưa được đọc trực tiếp trong lượt chạy này, cần coi là **chưa xác minh** [19].

Các bài viết từ người thực hành hội tụ về một đường cong thoái hoá cụ thể, lặp lại được cho "mệt mỏi vì duyệt": kiểm tra kỹ lưỡng → duyệt bằng phím tắt hình thức → cuối cùng ra lệnh cho agent bỏ qua hoàn toàn quyền hạn, tạo ra "vẻ ngoài có giám sát mà không có giám sát thật" [21][22] (độ tin trung bình/thấp, bài viết cá nhân, nhưng khớp độc lập với khảo cứu platform-engineering ở chiều 2.2).

Phát hiện tin cậy cao nhất ở chiều này đến từ 4 chuyên gia có tên được IT Brew phỏng vấn [23]: thiết kế human-in-the-loop hiệu quả dùng ma sát có chủ đích ở đúng bước hệ trọng (không gác cổng dàn trải); cần công cụ review theo đúng lĩnh vực chứ không phải nút approve/reject chung chung; đòi người duyệt phải thấy được toàn bộ quá trình làm việc của agent — nếu không cổng duyệt trở thành hình thức; và nên coi công việc của người duyệt giống kiểm soát không lưu: phán đoán hệ trọng dưới áp lực thời gian, có quyền hỏi lại thay vì chỉ bấm nhị phân.

### 2.4 Mẫu hình riêng cho plugin/công cụ CLI (vòng 2, lấp khoảng trống)

Đây là chiều áp dụng trực tiếp nhất cho Vấn Đạo, vì khảo sát đúng loại sản phẩm — plugin công cụ dev thật — thay vì workflow engine backend.

**Claude Code đã ghi tài liệu chính chủ cho đúng nguyên thuỷ Vấn Đạo cần dùng**: hệ thống permission mode (Manual chờ hỏi trước hầu hết hành động; auto có model thứ hai — classifier — tự review) [27] và hệ thống Hooks với `PreToolUse` (chặn được một lượt gọi tool, trả allow/deny/ask, hoặc chặn cứng qua exit code 2), `PermissionRequest`, `PermissionDenied` (có retry), và `PostToolBatch` (đánh giá hiệu ứng tích luỹ của một loạt hành động trước lượt model tiếp theo) [28]. GitHub Copilot SDK hội tụ độc lập về đúng cơ chế đó — hook `onPreToolUse`/`onPostToolUse` — dưới một hãng khác [33], một tín hiệu chéo-hãng có ý nghĩa rằng đây đang thành hình dạng chuẩn cho HITL ở tầng plugin, không phải đặc thù riêng của Claude Code.

Bốn kiểu điểm duyệt khác nhau thật sự tồn tại trong các công cụ đang chạy thật, đáng gọi tên rõ vì đánh đổi khác nhau:

- **Gác từng hành động** — chặn trước mỗi hành động rủi ro (Claude Code chế độ Manual, hộp thoại xác nhận `prepareInvocation` của VS Code [32], permission prompt của GitHub Copilot CLI [33]).
- **Review diff theo lô/sau khi xong** — để agent làm xong rồi mới xem lại tổng thể (Cursor xem diff màu sau khi sinh [30], Aider tự commit rồi tuỳ chọn review [34]).
- **Khả năng đảo ngược rẻ** — checkpoint tự động vào một shadow git repo (tách khỏi lịch sử thật của người dùng) thay vì gác trước khi chạy, làm cho auto-approve khả thi bằng cách đưa cái giá của một sai lầm về gần bằng 0 (Cline [29]).
- **Định tuyến theo điểm rủi ro** — kết hợp chính sách duyệt, phát hiện của AI review agent, và cấu hình để quyết định có cần người xem hay không; tự nhận rõ **không thay thế** review đầy đủ của người khi phát hiện cần xem (Cursor "PR Routing & Approval" [31]).

Phát hiện mới quan trọng nhất của vòng này là một kiểu thất bại cụ thể, được quan sát lặp lại: **một lượt duyệt có thể "thiu" nếu trạng thái nó đang duyệt thay đổi trong lúc chờ.** Ba người bình luận độc lập trên một issue GitHub của công cụ đang chạy thật (block/buzz#3871) đều nêu cùng một dạng vấn đề này trong khoảng vài ngày, tháng 7-8/2026 [18]: không có lease-expiry cho lượt duyệt đang chờ, không có đối tượng trạng thái có thẩm quyền (trạng thái sống trong "văn xuôi và sự chú ý của người vận hành" thay vì một trường có cấu trúc), và lượt duyệt không fail-closed khi digest của artifact thay đổi mà không có chuyển trạng thái rõ ràng. Codex của OpenAI có một lỗi liên quan đã được người dùng báo cáo, đã shipped: chính agent tự hết giờ và tự huỷ hộp thoại duyệt đang chờ của nó sau ~70-110 giây, rồi báo "chưa được duyệt" dù người dùng chưa hề chạm vào [25]. `openclaw/openclaw` đã vá một vấn đề liền kề — kết quả của một lượt duyệt cũ gắn nhầm vào lượt duyệt mới hơn — bằng cách gán mỗi quyết định duyệt cho một chủ sở hữu thao tác rõ ràng [26]. **Đây là rủi ro triển khai thật, lặp lại, không phải trường hợp biên lý thuyết** — 3 nguồn độc lập (công cụ khác nhau, hãng khác nhau, trong cửa sổ 2 tháng) là bằng chứng củng cố mạnh.

Ghi chú: thảo luận cline/cline#12959 [24], đề xuất một vòng review Plan↔Act tự động gắn liền vào công cụ, đáng tham khảo như một **đề xuất thiết kế** (review đa-model trước khi áp dụng, có lập luận rõ là logic chuyển chế độ cần gắn liền vào công cụ chứ không mô phỏng qua hook/MCP) nhưng chỉ đọc được phần mở đầu trong lượt chạy này (nhánh bình luận không lấy được) — chưa nên coi là mẫu hình đã ổn định, đã triển khai.

## 3. Phát hiện xuyên chiều

1. **Câu trả lời cơ chế của cả ngành (checkpoint/interrupt bền) và kiểu thất bại triển khai của nó (thiu khi resume) là CÙNG MỘT phát hiện nhìn từ hai độ cao khác nhau.** Quan sát trừu tượng ở §2.2 — "resume chạy lại từ đầu, không phải từ điểm ngắt" [6] — và lỗi cụ thể được 3 nguồn độc lập báo cáo ở §2.4 — một lượt duyệt có thể "thiu" nếu trạng thái nó đang duyệt thay đổi trong lúc chờ [18][25][26] — mô tả đúng một khoảng trống kiến trúc. Bất kỳ điểm duyệt HITL nào Vấn Đạo dựng đều cần câu trả lời rõ ràng cho "nếu thứ đang chờ duyệt thay đổi trong lúc chờ thì sao" — không chỉ cơ chế "dừng và chờ".

2. **Ít điểm duyệt, đặt đúng chỗ hệ trọng, luôn thắng gác cổng dàn trải — xuất hiện độc lập ở mọi độ cao đã khảo sát**: hệ sản xuất thật của chính Anthropic tập trung người vào kiểm tra edge-case thay vì giám sát liên tục [8]; khảo cứu platform-engineering gọi tên gác cổng dàn trải là kiểu thất bại #1 trong 3 [15]; 4 chuyên gia độc lập hội tụ về "ma sát có chủ đích ở bước hệ trọng, không phải gác dàn trải" [23]; và cả triết lý thiết kế của Cline (đảo ngược rẻ thay vì gác trước khi chạy) là một câu trả lời cấu trúc cho đúng vấn đề này [29]. Đây không phải ý kiến của một nguồn — đây là phát hiện được củng cố nhiều nhất trên cả 4 chiều nghiên cứu này.

3. **Hai kiến trúc điểm duyệt thật sự khác nhau đang chạy trong các công cụ dev, và không cái nào "chuẩn hơn" — chúng là hai cách đặt cược khác nhau.** Gác từng hành động (Claude Code, VS Code, GitHub Copilot CLI) [27][32][33] hỏi trước mỗi bước rủi ro; review diff theo lô/sau khi xong (Cursor, Aider) [30][34] để agent làm xong rồi mới xem lại tổng thể. Thiết kế nhiều vai của Vấn Đạo (Thư linh dạy, Nghiệm Công Sứ/Phúc Khảo Sứ chấm riêng biệt, cờ bất đồng) gần họ review-theo-lô hơn — chấm diễn ra sau khi người học nộp bài, không phải một cổng sống — trong khi duyệt lộ đồ/giáo án gần gác từng hành động hơn. Đây là một tổ hợp lai hợp lệ, nhưng đáng gọi tên rõ thay vì giả định một kiểu áp dụng đồng nhất khắp nơi.

## 4. Bằng chứng ngược

Không chạy red-team pass ở lượt nghiên cứu này (`red_team: off`) — không có mục nào ở phần này.

## 5. Khuyến nghị

1. **Xây điểm duyệt của Vấn Đạo (FR6 duyệt lộ đồ, FR12a-b cờ bất đồng, FR15 xác nhận suy đoán) trực tiếp trên hệ thống Hooks/permission-mode có sẵn của Claude Code, thay vì tự phát minh một cơ chế song song** — đây đúng là mẫu hình Claude Code tự tài liệu hoá, và GitHub Copilot hội tụ độc lập về cùng cơ chế [27][28][33]. Độ tin: cao (tài liệu chính chủ, hội tụ chéo-hãng). *Feed vào: architecture spine.*

2. **Cho mỗi lượt duyệt đang chờ một cách kiểm tra "thiu" rõ ràng trước khi coi là hợp lệ** — gắn FR6 (duyệt lộ đồ) và các mốc xác nhận khác với một dấu vân tay trạng thái (ví dụ: bản lộ đồ/giáo án nào đã được trình xem), và fail-closed (hỏi lại) thay vì âm thầm áp dụng lượt duyệt cũ lên nội dung đã đổi. Đây là rủi ro mới, đáng hành động nhất tìm được ở lượt chạy này [18][25][26]. Độ tin: cao cho việc rủi ro là thật (3 nguồn độc lập, gần đây, chéo-hãng); trung bình cho hình dạng cách sửa cụ thể (gắn dấu vân tay + fail-closed là một đề xuất trong vài đề xuất, chưa phải chuẩn ngành đã ổn định). *Feed vào: architecture spine, roadmap risk.*

3. **Giữ nguyên trực giác "ít điểm duyệt, đặt đúng chỗ" hiện tại của Vấn Đạo — không cần thêm cổng duyệt mới.** FR6/FR12a-b/FR15 đã chỉ gác ở mốc hệ trọng (bắt đầu lộ đồ, bất đồng, gợi ý chưa chắc) chứ không phải mọi lượt model. Đây là phát hiện được củng cố nhiều nhất của cả nghiên cứu (xem §1, §3 mục 2) — không phải sở thích thiết kế, nên đừng đổi mà không cân nhắc lại bằng chứng đó trước. *Feed vào: architecture spine.*

4. **Khi Vấn Đạo chạy thật, định kỳ rà soát "tỷ lệ duyệt trôi qua" của từng điểm duyệt** — nếu một cổng (ví dụ duyệt lộ đồ) gần như luôn được duyệt không sửa gì, đó là tín hiệu đã ghi nhận rằng cổng đã ngừng bắt được gì, không phải dấu hiệu thiết kế đang hoàn hảo. Độ tin: trung bình (một nguồn độ tin thấp, nhưng khớp kiểu thất bại "rubber-stamp" tìm thấy độc lập ở §2.2). *Feed vào: roadmap risk, kiểm thử vận hành sau MVP.*

5. **Thiết kế FR12b hiện tại (cờ bất đồng chỉ thấy được nếu người học chủ động mở đạo tâm, không tự đẩy thông báo) đã đúng hướng — gần họ review-theo-lô hơn là gác trực tiếp**, tránh được kiểu thất bại "chỉ-đồng-bộ" vì không chặn chờ phản hồi sống của người dùng [15]. Không cần đổi; ghi nhận đã khớp bằng chứng.

## 6. Câu hỏi còn mở

1. Liệu hook `PostToolBatch` của Claude Code (đánh giá hiệu ứng tích luỹ của một loạt hành động trước lượt model tiếp theo) có thể thay thế hoặc bổ sung cho một số điểm duyệt hiện đang gác riêng lẻ của Vấn Đạo — chưa khảo sát trong lượt này; cần đọc kỹ ngữ nghĩa kích hoạt chính xác của hook đó.
2. Báo cáo "State of Agent Engineering 2026" của LangChain (>60% sự cố là lỗi quản lý trạng thái) có đứng vững ở nguồn gốc không — mới chỉ thấy qua trích dẫn thứ cấp trong lượt này [18].
3. Kiến trúc duyệt của JetBrains AI Assistant/Junie — chưa khảo sát, một khoảng trống trong khảo sát mẫu hình plugin.
4. Nhánh bình luận của cline/cline#12959 (không lấy được, render bằng JS) có thể chứa nội dung liên quan trực tiếp tới thiết kế vòng review nhiều vai của Vấn Đạo (Nghiệm Công Sứ → Phúc Khảo Sứ) — chỉ đọc được phần mở đầu trong lượt này.

## 7. Phụ lục nguồn

| # | Nguồn | Nhà xuất bản | Ngày | Truy cập | Độ tin |
|---|---|---|---|---|---|
| [1] | [MCP joins Agentic AI Foundation](https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/) | Model Context Protocol (Anthropic) | 2025-12 | 2026-08-25 | Cao |
| [2] | [OpenAI, Anthropic, Block join Linux Foundation](https://techcrunch.com/2025/12/09/openai-anthropic-and-block-join-new-linux-foundation-effort-to-standardize-the-ai-agent-era/) | TechCrunch | 2025-12 | 2026-08-25 | Cao |
| [3] | [MCP joins the Linux Foundation](https://github.blog/open-source/maintainers/mcp-joins-the-linux-foundation-what-this-means-for-developers-building-the-next-era-of-ai-tools-and-agents/) | GitHub Blog | 2025-12 | 2026-08-25 | Cao |
| [4] | [A2A Protocol surpasses 150 organizations](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year) | Linux Foundation | 2026-04 | 2026-08-25 | Cao |
| [5] | [A year of open collaboration: A2A anniversary](https://opensource.googleblog.com/2026/04/a-year-of-open-collaboration-celebrating-the-anniversary-of-a2a.html) | Google Open Source Blog | 2026-04 | 2026-08-25 | Cao |
| [6] | [LangGraph `interrupt()` reference](https://reference.langchain.com/python/langgraph/types/interrupt) | LangChain (official docs) | 2026 (undated) | 2026-08-25 | Cao |
| [7] | [Temporal: human-in-the-loop AI cookbook](https://docs.temporal.io/ai-cookbook/human-in-the-loop-python) | Temporal (official docs) | 2026 (undated) | 2026-08-25 | Cao |
| [8] | [Anthropic: how we built our multi-agent research system](https://www.anthropic.com/engineering/built-multi-agent-research-system) | Anthropic (engineering blog) | 2025 (ước lượng) | 2026-08-25 | Cao |
| [9] | [AI agent orchestration frameworks 2026](https://zylos.ai/research/2026-01-12-ai-agent-orchestration-frameworks/) | Zylos Research (tổng hợp) | 2026-01 | 2026-08-25 | Trung bình |
| [11] | [Reliable document approvals with human-in-the-loop workflows](https://temporal.io/blog/human-in-the-loop-approvals) | Temporal (engineering blog) | 2026 | 2026-08-25 | Cao |
| [12] | [AWS Step Functions: connect to a resource (callback pattern)](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html) | AWS (tài liệu chính chủ) | 2026 (hiện tại) | 2026-08-25 | Trung bình |
| [13] | [Mastering saga patterns](https://temporal.io/blog/mastering-saga-patterns-for-distributed-transactions-in-microservices) · [Saga pattern glossary](https://www.conduktor.io/glossary/saga-pattern-for-distributed-transactions) | Temporal / Conduktor | 2026 | 2026-08-25 | Trung bình |
| [14] | [Conductor-OSS FAQ](https://conductor-oss.github.io/conductor/devguide/faq.html) · [What is durable execution](https://restate.dev/what-is-durable-execution) | Conductor-OSS / Restate | 2026 | 2026-08-25 | Trung bình |
| [15] | [The platform engineer's guide to human-in-the-loop agentic workflows](https://platformengineering.com/features/the-platform-engineers-guide-to-human-in-the-loop-agentic-workflows/) | Platform Engineering (Aditya Shrivastava) | 2026-07 | 2026-08-25 | Trung bình |
| [16] | [Human-in-the-loop vs. human-on-the-loop](https://reliaquest.com/blog/human-in-the-loop-vs-human-on-the-loop/) | ReliaQuest | 2026-07 | 2026-08-25 | Thấp |
| [17] | [Approval fatigue (Encyclopedia of Agentic Coding Patterns)](https://aipatternbook.com/approval-fatigue) | aipatternbook.com | 2026 (trích 1983, 2012, 2025) | 2026-08-25 | Trung bình |
| [18] | [block/buzz issue #3871](https://github.com/block/buzz/issues/3871) (+ bình luận HashMac, loganrenz, samiriasbeck) | GitHub (block/buzz) | 2026-07/08 | 2026-08-25 | Cao |
| [19] | [LangGraph agent architecture](https://eastondev.com/blog/en/posts/ai/20260424-langgraph-agent-architecture/) (trích LangChain 2026 report) | eastondev.com | 2026-04 | 2026-08-25 | Trung bình |
| [20] | [Architecting human-in-the-loop agents](https://medium.com/data-science-collective/architecting-human-in-the-loop-agents-interrupts-persistence-and-state-management-in-langgraph-fa36c9663d6f) | Medium — Burak Degirmencioglu | 2025-12 | 2026-08-25 | Trung bình |
| [21] | [Trust engineering](https://mhsu2112.substack.com/p/trust-engineering) | Substack — Mike Hsu | 2026-03 | 2026-08-25 | Trung bình |
| [22] | [Approval fatigue is breaking AI agents](https://medium.com/@shreya_edulakanti/approval-fatigue-is-breaking-ai-agents-execution-boundaries-fix-it-6c46c6d512dd) | Medium — Shreya Edulakanti | 2026 | 2026-08-25 | Thấp |
| [23] | [What makes a good human-in-the-loop](https://www.itbrew.com/stories/2026/03/16/what-makes-a-good-human-in-the-loop) | IT Brew | 2026-03 | 2026-08-25 | Cao |
| [24] | [cline/cline discussion #12959](https://github.com/cline/cline/discussions/12959) | GitHub (cline/cline) | 2026 (chỉ đọc OP) | 2026-08-25 | Trung bình |
| [25] | [OpenAI Codex issue #29627](https://github.com/openai/codex/issues/29627) | GitHub (openai/codex) | 2026-06-23 | 2026-08-25 | Cao |
| [26] | [openclaw/openclaw PR #98394](https://github.com/openclaw/openclaw/pull/98394) | GitHub (openclaw/openclaw) | 2026-07 | 2026-08-25 | Cao |
| [27] | [Claude Code: permission modes](https://code.claude.com/docs/en/permission-modes) | Anthropic (Claude Code Docs) | Hiện tại | 2026-08-25 | Cao |
| [28] | [Claude Code: hooks](https://code.claude.com/docs/en/hooks) | Anthropic (Claude Code Docs) | Hiện tại | 2026-08-25 | Cao |
| [29] | [Cline: checkpoints](https://docs.cline.bot/core-workflows/checkpoints) | Cline (tài liệu chính chủ) | Hiện tại | 2026-08-25 | Cao |
| [30] | [Cursor: agent review](https://docs.cursor.com/agent/review) | Cursor (tài liệu chính chủ) | Hiện tại | 2026-08-25 | Trung bình |
| [31] | [Cursor: PR routing & approval](https://cursor.com/docs/approval-agents) | Cursor (tài liệu chính chủ) | Hiện tại | 2026-08-25 | Trung bình |
| [32] | [VS Code: Language Model Tool API](https://code.visualstudio.com/api/extension-guides/ai/tools) | Microsoft (VS Code API Docs) | Hiện tại | 2026-08-25 | Cao |
| [33] | [GitHub Copilot: responsible use of agents](https://docs.github.com/en/copilot/responsible-use/agents) | GitHub (tài liệu chính chủ) | Hiện tại | 2026-08-25 | Trung bình *(rà soát ngữ nghĩa cuối phát hiện: đúng nhà xuất bản nhưng đây là trang chính sách/responsible-use, không phải trang tham chiếu kỹ thuật của hook — GitHub Docs có trang riêng cho hooks reference chưa được xác minh trực tiếp trong lượt này; hạ độ tin thay vì bỏ claim)* |
| [34] | [Aider: git integration](https://aider.chat/docs/git.html) | Aider (tài liệu chính chủ) | Hiện tại | 2026-08-25 | Trung bình |

*Số thứ tự 10 bỏ trống có chủ đích — nguồn gốc là Pickaxe "controlled autonomy", 1 nguồn vendor độ tin thấp, không dùng làm căn cứ cho phát hiện/khuyến nghị nào trong báo cáo này nên đã loại khỏi bảng; giữ số trống thay vì đánh số lại để không phá các trích dẫn từ mục 11 trở đi.*

## 8. Bản đồ độ mới

Tính bằng `recon_kit.py staleness`, không tự đếm tay. Ngưỡng freshness theo gói Technical (landscape/mechanism/plugin-pattern coi là AI-adjacent ≤ 3 tháng; version ≤ 1 tháng; pattern/failure-claim/implementation-reality/pain-point/success-factor ≤ 6 tháng vì gắn với hệ sinh thái đang đổi nhanh).

- **10/18 claim đã qua hạn re-check** tính tới 2026-08-25 — phần lớn là các claim tầng "cơ chế nền tảng" (LangGraph, Temporal, MCP/A2A) ghi nhận đầu 2026, ít khả năng đổi bản chất nhưng nên xác nhận lại phiên bản trước khi khoá cứng vào kiến trúc.
- **Re-check sớm nhất: 2025-09-01** (2 claim về hệ đa-agent Anthropic — ngày xuất bản gốc chỉ ước lượng, không có timestamp rõ trên trang).
- Các claim mới nhất, ít gấp nhất để re-check: Claude Code hooks/permission-mode, GitHub Copilot SDK, Cline checkpoints, block/buzz#3871 (đều re-check từ 2026-11 trở đi) — đây cũng là 4 claim quan trọng nhất cho khuyến nghị #1 và #2.

*Đây là công việc cho một lượt Refresh sau này, không phải việc cần làm ngay.*
