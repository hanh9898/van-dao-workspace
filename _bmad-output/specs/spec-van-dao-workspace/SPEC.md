---
id: SPEC-van-dao-workspace
companions:
  - glossary.md
  - pham-vi-mvp.md
  - do-luong-thanh-cong.md
  - ../../planning-artifacts/architecture/architecture-van-dao-workspace-2026-08-25/ARCHITECTURE-SPINE.md
  - ../../../docs/VAN-DAO-dac-ta-v1.0.md
sources:
  - ../../planning-artifacts/prds/prd-van-dao-workspace-2026-08-24/prd.md
---

> **Canonical contract.** This SPEC and the files in `companions:` are the complete, preservation-validated contract for what to build, test, and validate. Source documents listed in frontmatter are for traceability — consult them only if you need narrative rationale or prose color this contract intentionally omits.

# Vấn Đạo

## Why

Người tự học bằng sách PDF/EPUB đọc xong một chương và tưởng đã hiểu — cho tới khi phải dùng vào việc thật mới lộ ra chỗ chưa nắm chắc. Tóm tắt AI đọc nhanh nhưng không kiểm tra hiểu; tự học một mình không có ai hỏi ngược khi hiểu sai. Vấn Đạo là một plugin Claude Code lấp khoảng đó: biến sách PDF/EPUB người dùng đã có sẵn thành một lộ trình học có AI đồng hành sát sao — giải thích ngắn gọn trước, dạy từng ý kèm hỏi ngược, và **không công nhận đã hiểu chỉ vì trả lời đúng một câu** — phải qua một bài kiểm tra đòi vận dụng vào tình huống mới, chấm độc lập bởi một AI tách biệt với AI vừa dạy. Đây là sản phẩm cho chính tác giả trước tiên (n=1 — người dùng xác nhận duy nhất tính tới nay), mã nguồn mở để ai muốn cũng tự dùng cá nhân — không phải dịch vụ nhắm số đông.

## Capabilities

- **CAP-1** — Thu bí kíp
  - **intent:** Hệ thống giải nghĩa một cuốn sách PDF/EPUB (chủ yếu dạng văn bản) thành nguồn đủ để dạy — không chỉ trích xuất chữ nguyên văn. Không rút được chữ thì dừng ngay (FR38). Pha thiết kế sư phạm (pha 2) máy chỉ đề xuất kèm lý do — **người dùng bắt buộc sửa và duyệt** trước khi sinh cấp chương (FR37); xương sống/tiêu chí đạt/điểm hạ sơn không do máy tự quyết.
  - **success:** Với một bí kíp thật đã thu, lớp sư phạm sinh ra (mục tiêu, giả định nền, tiêu chí đạt ở mức tối thiểu); mọi đoạn có độ tin cậy giải nghĩa thấp (bảng/công thức/code dày đặc) được tự đánh dấu, không âm thầm bỏ qua. Bí kíp có hai mức hợp lệ (FR39): **đủ dùng** (vào kho ngay) và **đủ chuẩn** (chia sẻ được, bồi sau khi học chương đó, không theo lịch) — dạy ở mức đủ dùng phải nói rõ đang chấm theo mục tiêu, chưa có tiêu chí chi tiết. Không có bước sinh cấp chương nào chạy mà thiếu xác nhận duyệt của người dùng ở pha 2.

- **CAP-2** — Lộ đồ trình duyệt trước khi dạy
  - **intent:** Người học duyệt lộ đồ (kế hoạch học cả quyển, kèm số chương và ước lượng thô) trước khi Vấn Đạo bắt đầu dạy; lộ đồ chưa duyệt sống sót qua gián đoạn phiên.
  - **success:** Không chương nào được dạy khi chưa có lộ đồ đã duyệt còn hiệu lực; đóng máy giữa lúc lộ đồ vừa sinh chưa duyệt rồi mở lại đúng bí kíp — hệ trình lại đúng bản đã lưu, không sinh bản khác.

- **CAP-3** — Tóm lược mở đầu, dạy từng ý, hỏi ngược, giàn giáo co giãn
  - **intent:** Thư linh soạn giáo án ra file trước mỗi chương; **trình bày tóm lược/mô hình tổng quan chương trước khi hỏi ngược từng ý** (dựa trên lớp giải nghĩa FR1, không thay thế hỏi ngược); dạy từng ý kèm câu hỏi chốt; đối chất quan niệm cũ trước nội dung trái ngược; co giãn mức gợi ý theo tình trạng vấp/vững của người học. Khi một câu nghiệm công đang treo, **không đáp câu hỏi trùng câu đó** — hỏi ngược lại, giảng lại (nếu cần) bằng ví dụ khác (FR2a). Quan niệm cũ đã nêu ra không tự coi là đã gỡ — chỉ thừa nhận bằng lời đưa tới "đang gỡ", cần bằng chứng trong bài mới sang "đã gỡ"; tái phát là trạng thái riêng (FR3a).
  - **success:** Mỗi chương có bước tổng quan đứng trước hỏi ngược, dựa trên lớp giải nghĩa đã có chứ không model tự bịa tại chỗ; không ý nào được dạy tiếp mà chưa hỏi ngược ý trước; sai lần hai cùng chỗ đổi cách trình bày, sai lần ba báo lên thay vì giảng lại; một ý/chương chỉ tính đạt khi có bằng chứng vận dụng, không phải nhớ đúng chữ. Tóm lược mở đầu (FR1a) là **Loại 3 theo AD-5** — dẫn xuất/cache từ giải nghĩa FR1 (Loại 1), không phải nguồn lưu trữ chính; nơi cần "nhắc lại" tái sinh từ FR1, không đọc cache của Dạy. Thư linh không bao giờ tự tuyên bố tâm ma đã gỡ (R18) — mọi chuyển trạng thái "đã gỡ" ghi kèm dẫn chứng từ nghiệm công/khảo thí; nhật ký các câu đã né vì trùng nghiệm công đang treo tra lại được.

- **CAP-4** — Soát độc lập, tách vai
  - **intent:** Bài làm được chấm bởi vai tách biệt khỏi vai dạy (không fork), có căn cứ trích dẫn cụ thể; ở khảo thí quyển có người soát thứ hai độc lập, không bàn bạc, đọc mục tiêu chứ không đọc tiêu chí chi tiết.
  - **success:** Mọi phán quyết đạt/chưa đạt trích được câu cụ thể trong bài làm; khi hai bên chấm không khớp, hệ ghi "cờ bất đồng" và không chặn người học; bằng chứng cân bằng thì nghiêng về hướng có lợi cho người học.

- **CAP-5** — Định hướng có lối tự nhập *(Vòng 3)*
  - **intent:** Gợi ý học gì tiếp/sách nào phù hợp luôn kèm lối tự nhập và nói rõ nguồn (dữ liệu thật hay suy đoán); suy đoán phải được người học xác nhận thêm.
  - **success:** Không gợi ý nào ép một hướng duy nhất; gợi ý suy đoán không được coi là đã chấp nhận cho tới khi người học xác nhận thêm một bước.

- **CAP-6** — Đo cảnh giới có hiệu chuẩn *(Vòng 4)*
  - **intent:** Tuyên bố cảnh giới trên một mạch chỉ dựa vào ≥2 nguồn bằng chứng độc lập, chạy định bậc nhiều lần lấy độ tản mát làm thước đo tin cậy, và chỉ công bố khi hiệu chuẩn κ đạt ngưỡng.
  - **success:** Không nhãn cảnh giới nào được công bố khi κ<0,6 (chỉ nêu dấu hiệu quan sát được); báo cáo hiệu chuẩn luôn kèm % khớp thô song song κ; mọi nội dung về cảnh giới được khung là giả thuyết đang kiểm chứng.

- **CAP-7** — Đạo tâm tự ghi
  - **intent:** Sổ đạo tâm do chính người học tự ghi; không vai nào (kể cả AI) ghi hộ hay soạn sẵn để duyệt.
  - **success:** Cơ chế ghi đạo tâm tắt hoàn toàn khả năng model tự ghi (không chỉ là quy ước lời nói).

- **CAP-8** — Nghi thức gắn việc thật
  - **intent:** Nghi thức (bái sư, thu bí kíp, đột phá cảnh giới) chỉ kích hoạt khi có việc thật đứng sau, không phát cho hành động không tốn công.
  - **success:** Mỗi nghi thức có điều kiện kích hoạt cụ thể, kiểm được (đã khai xong vai/mạch cho bái sư; đã tự tìm và đưa được một quyển vào kho cho thu bí kíp; định bậc cao hơn lần trước có căn cứ cho đột phá cảnh giới).

- **CAP-9** — Hạ sơn/phục mệnh nhận cả thất bại *(Vòng 3)*
  - **intent:** Nhánh mang kiến thức ra việc thật rồi báo lại nhận cả báo cáo thất bại, không chỉ thành công.
  - **success:** Luồng phục mệnh không từ chối hay bỏ qua báo cáo thất bại; báo cáo thất bại vẫn tạo được dòng đạo tâm.

- **CAP-10** — Tiếp nối liền mạch qua nhiều phiên *(Vòng 3)*
  - **intent:** Vào chương mới phụ thuộc chương trước thì nhắc lại nội dung liên quan trước khi dạy ý mới; hết chương cuối quyển thì hệ thống hoá toàn quyển trước khảo thí; quay lại chương dở ở phiên mới thì hỏi lại một hai câu để tự quyết đi tiếp hay ôn lại; bỏ giữa chừng là tạm dừng hợp lệ, giữ nguyên lộ đồ/giáo án.
  - **success:** Không chương phụ thuộc nào được dạy thẳng mà bỏ qua nhắc lại; quay lại sau xuất quan không dựng lộ đồ mới; không tính theo số ngày đã qua khi quyết định hỏi lại hay đi tiếp.

- **CAP-11** — Chú Giải Sứ bồi sai lầm phổ biến *(Vòng 4)*
  - **intent:** Khi cùng sai lầm lặp lại ở cùng chỗ qua nhiều lần học, bồi một ghi chú vào lớp chú giải riêng của chương — không sửa bí kíp gốc, không mang chi tiết tình huống thật (tên người/công ty/dự án) ra ngoài máy người học.
  - **success:** Lớp chú giải tách biệt bí kíp gốc, gỡ được bất cứ lúc nào không ảnh hưởng bản gốc; không bản ghi chú giải nào chứa danh tính/chi tiết định danh được của tình huống thật.

- **CAP-12** — Quét kho gợi sách *(Vòng 3)*
  - **intent:** Khi cần gợi sách tiếp theo, một công cụ quét kho trả về tối đa 3 lựa chọn kèm lý do, không phải cả danh sách kho.
  - **success:** Kết quả trả về không bao giờ vượt quá 3 mục, mỗi mục kèm lý do cụ thể.

- **CAP-13** — Bản đồ trực quan tiến độ *(Vòng 3)*
  - **intent:** Tiến độ học nhiều quyển/nhiều mạch xem được dưới dạng bản đồ trực quan, dựng lại được từ file trạng thái bất cứ lúc nào.
  - **success:** Xoá bản đồ đã dựng và dựng lại từ artifact gốc cho kết quả y nguyên; bản đồ không phải nguồn lưu trữ chính của tiến độ.

- **CAP-14** — Trả lời rõ khi chưa hỗ trợ
  - **intent:** Khi người học hỏi một ý định mà cơ chế đứng sau chưa được dựng ở bản đang chạy, hệ trả lời rõ "chưa hỗ trợ ở bản này" — không im lặng bỏ qua, không đoán liều.
  - **success:** Mọi ý định của `/vd:chi-duong` ngoài phạm vi đã dựng đều nhận được thông báo tường minh, không bao giờ một câu trả lời bịa hoặc một khoảng lặng.

- **CAP-15** — Không khen sáo rỗng

- **CAP-17** — Chỉ điểm
  - **intent:** Sau khi khai vai/mạch ở bái sư, Trưởng môn gọi tên sách cụ thể (đủ tên, tác giả, năm, công pháp/tâm pháp, vì sao) cho người học tự đi tìm — không chọn mạch hộ; đây là mắt xích khởi động hệ từ tàng kinh các rỗng. Số chỉ điểm co giãn theo đã-biết/chưa-biết muốn luyện gì; mức chắc chắn của gợi ý phải nói rõ TRƯỚC khi đưa danh sách.
  - **success:** Không đưa tên sách trần không kèm 3 dữ kiện xác định được; chỉ điểm mới thay hẳn chỉ điểm cũ (không cộng dồn) nhưng tra lại được nếu người học hỏi; sách công pháp luôn kèm gợi ý tâm pháp; câu rào "đây là suy đoán" xuất hiện trước danh sách khi chưa có dữ liệu thật, không phải sau.

- **CAP-16** — Thiết lập ban đầu
  - **intent:** Khi plugin được bật lần đầu, giúp người học chọn ngôn ngữ giao tiếp qua `userConfig` — Claude Code KHÔNG tự động chặn/hỏi khi cài không kèm giá trị (verify thật: chỉ in cảnh báo, cài xong với field trống), nên `nhap-mon` phải tự kiểm field này và chủ động hướng dẫn `/plugin configure` nếu chưa đặt; phiên sau nạp lại, không hỏi lại nếu đã đặt. Trong hội thoại bái sư (`nhap-mon`), cho người học đặt tên riêng cho 4 vai trực tiếp nói chuyện với mình (Trưởng môn, Tàng kinh trưởng lão, Thư linh, Giám khảo) — gợi ý sẵn vài tên, không ép chọn từ danh sách. 4 vai không nói với người học không đặt tên.
  - **success:** Ngôn ngữ đặt được qua `userConfig`, phiên sau nạp lại đúng lựa chọn — nếu chưa đặt, `nhap-mon` phát hiện và hướng dẫn rõ cách đặt, không giả định hệ tự hỏi; 4 vai nói-với-người-học đều có tên riêng trước khi dạy bắt đầu, người học tự nhập được thay vì chỉ chọn gợi ý; cơ chế `userConfig` đã verify chạy thật 2026-08-26 (schema + lưu trữ qua CLI) — đường cài tương tác thật (TTY người dùng) vẫn chưa verify.
  - **intent:** Hệ không khen mang tính xã giao/nịnh bợ ở bất kỳ phản hồi nào (Dạy, Soát, Nền); cảm giác tiến bộ chỉ đến từ nghi thức gắn việc thật và kết quả thật.
  - **success:** Ca thử "đưa câu trả lời tầm thường" xác nhận hệ không khen sáo rỗng — kiểm được bằng behavioral eval.

## Constraints

- **Actor cách ly:** vai dạy và vai chấm là hai tiến trình AI tách biệt; vai chấm chạy trên subagent tươi, không bao giờ fork phiên dạy (chi tiết: `ARCHITECTURE-SPINE.md` AD-1, AD-4).
- **Trạng thái suy từ artifact/event log:** không sửa file trạng thái tại chỗ — mọi đổi trạng thái là ghi thêm dòng (`ARCHITECTURE-SPINE.md` AD-2).
- **Một vùng ghi, đúng một chủ:** mỗi thư mục dữ liệu dưới `~/.vandao/` có đúng một vai được phép ghi (`ARCHITECTURE-SPINE.md` AD-3).
- **`book-to-skill` (virgiliojr94) là phụ thuộc ngoài bắt buộc cho CAP-1** — đã verify chạy thật; chưa có phương án dự phòng nếu ngừng bảo trì hoặc đổi API (xem Open Questions).
- **n=1:** người dùng xác nhận duy nhất tính tới nay là chính tác giả — không thiết kế cho giả định về người dùng thứ hai chưa được xác nhận.

## Non-goals

- Không cấp chứng chỉ/bằng cấp chính thức — "đột phá" là phản chiếu nội bộ cho người học, không phải văn bằng có giá trị dùng bên ngoài.
- Không đo tiến độ bằng số chương đã đọc — đọc xong không đồng nghĩa hiểu.
- Không thu telemetry từ người dùng mở nguồn khác — sách và câu trả lời ở lại máy người dùng, không có server riêng thu dữ liệu học tập.
- Không phải chatbot hỏi-đáp tự do, không cấu trúc — luôn đi qua lộ đồ/giáo án.
- Không phải chế độ lớp học/nhiều người cùng học một bí kíp — theo dõi tiến độ theo cá nhân.
- Vấn Đạo không tìm hay cấp sách hộ người dùng — người dùng phải tự có sẵn PDF/EPUB trước; người chưa có sách cụ thể trong đầu không phải người dùng mục tiêu ở bản đầu.
- Chưa cam kết mở rộng ngoài Claude Code — kiến trúc hiện tại (subagent tươi, hook, tầng lưu trữ cục bộ) gắn sâu vào nền tảng này; đây là *chưa quyết*, không phải *loại trừ vĩnh viễn*.

## Success signal

Tác giả tự thu một quyển PDF/EPUB thật đang cần học và đi hết tới đột phá quyển (khảo thí đạt, không né nghiệm công dọc đường); đạo tâm có dòng ghi kèm bằng chứng vận dụng cụ thể, không chỉ log nghi thức; và tác giả quay lại học quyển thứ hai sau khi xong quyển đầu, đo ở mốc vài tuần sau chứ không chỉ ngay sau lần đầu. Xem companion `do-luong-thanh-cong.md` cho bộ metric-đối-counter-metric đầy đủ.

## Assumptions

*Giả định nền tảng đã có sẵn ở `docs/VAN-DAO-dac-ta-v1.0.md` §17 (7 giả định kèm "sai thì sao") — companion, không chép lại ở đây.*

- Model giải nghĩa đúng ý từ PDF/EPUB đa dạng định dạng (CAP-1) — chưa kiểm với sách có bảng/hình/công thức/code dày đặc.
- Kỹ thuật sư phạm kiểm chứng cho người dạy là con người (CAP-3) sẽ chuyển tốt sang AI dạy qua văn bản — câu hỏi học thuật này chưa ngã ngũ.
- Pha "giải thích trước khi hỏi ngược" (CAP-3, nguồn FR1a — 4C/ID Supportive Information, van Merriënboer & Kirschner 2018) nay đã có căn cứ lý thuyết, nhưng liều lượng cụ thể (dài bao nhiêu, dạng văn bản/sơ đồ, có co giãn theo độ dày chương không) chưa thiết kế chi tiết — có thể cần điều chỉnh đáng kể khi viết story.
- Trực giao Nghiệm Công Sứ/Phúc Khảo Sứ (đọc tiêu chí khác đọc mục tiêu, CAP-4) tạo phân kỳ thật, không chỉ khác biệt hình thức — chỉ ca đối chứng (Vòng 4) mới phát hiện được nếu sai.
- Mastery learning (CAP-3) áp dụng tốt như nhau cho cả công pháp và tâm pháp — tâm pháp khó đo "vận dụng đúng" hơn, dễ rơi vào tiêu chí không phân biệt nếu không tách riêng.
- Độ tản mát giữa nhiều lần chạy (CAP-6) là thước đo độ tin hợp lệ cho phán đoán chủ quan — nếu không tương quan thật với độ chính xác, κ hiệu chuẩn (Vòng 4) là phép kiểm duy nhất, không có gì đỡ trước đó.
- ~~Cơ chế `userConfig` (CAP-16, ngôn ngữ giao tiếp) hoạt động đúng như tài liệu Claude Code mô tả~~ — **verify chạy thật xong 2026-08-26**: thêm `userConfig.communication_language` vào `van-dao/.claude-plugin/plugin.json`, `claude plugin validate --strict` PASS (sau khi sửa 1 lỗi thật: thiếu field `title` bắt buộc — tài liệu gốc không nhắc field này), cài thật qua `claude plugin marketplace add` + `claude plugin install --config communication_language=English -y`, xác nhận giá trị lưu đúng `~/.claude/settings.json` → `pluginConfigs["van-dao@van-dao"].options`.

## Open Questions

- **Chạy trên Claude Code hay mở rộng nền tảng khác?** Kiến trúc hiện tại (subagent tươi, hook, nhiều vai AI tách biệt) gắn sâu vào cách nền tảng này tổ chức — chuyển nơi khác gần như phải dựng lại phần điều phối. Chưa có quyết định thật. *Owner: tác giả. Xem lại khi: có nhu cầu thật từ người dùng thứ hai, hoặc kiến trúc đủ ổn định để ước tính chi phí chuyển nền tảng.*
- **Việc chấm ở MVP (Vòng 1-2) chưa có hiệu chuẩn nào xác nhận đáng tin.** CAP-4 chạy từ Vòng 1-2, nhưng hiệu chuẩn κ (CAP-6) chỉ chạy ở Vòng 4. Suốt Vòng 1-3, không có cơ chế nào xác nhận model chấm đúng theo rubric — tác giả tự đánh giá bằng cảm quan. *Owner: tác giả. Xem lại khi: tới Vòng 4 chạy được hiệu chuẩn thật; hoặc nếu phát hiện chấm sai có hệ thống ngay ở MVP.*
- **Chưa có ai ngoài tác giả đọc và phản hồi thật về ý tưởng này** — rủi ro "giải pháp đi tìm vấn đề". *Owner: tác giả. Xem lại khi: trước khi đầu tư thêm công sức đáng kể vượt quá MVP, hoặc trước khi mời bất kỳ ai khác cài thử.*
- **Chưa có kế hoạch bảo trì/hỗ trợ nếu người khác thật sự cài dùng** — mã nguồn mở nhưng chưa nghĩ tới SLA hay kế hoạch phân phối. *Owner: tác giả. Xem lại khi: có người dùng thứ hai thật sự.*
- **Phụ thuộc ngoài `book-to-skill` (virgiliojr94) chưa có phương án dự phòng.** Nền của CAP-1 — cần package này hoạt động đúng và tiếp tục được duy trì. *Owner: tác giả. Xem lại khi: package ngừng bảo trì hoặc đổi API phá vỡ tương thích; trước khi phụ thuộc vào nó vượt quá MVP.*
- **Va chạm ghi đồng thời giữa 2 phiên Claude Code cùng máy chưa có cơ chế khoá.** NFR3/AD-3 chỉ phân vùng dữ liệu theo VAI, không khoá theo TIẾN TRÌNH — nếu người dùng mở 2 cửa sổ terminal cùng chạy một lệnh dạy/soát một lúc, cả hai tiến trình đều là cùng một vai ghi vào cùng file, có thể ghi đè nhau thật. Phát hiện qua Failure Mode Analysis (Advanced Elicitation, 2026-08-26) khi rà epics.md. *Owner: tác giả. Xem lại khi: gặp trường hợp mất dữ liệu do ghi đồng thời thật; hoặc trước khi có người dùng thứ hai (tăng khả năng xảy ra).*
