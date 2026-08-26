---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-van-dao-workspace-2026-08-24/prd.md
  - _bmad-output/planning-artifacts/architecture/architecture-van-dao-workspace-2026-08-25/ARCHITECTURE-SPINE.md
  - _bmad-output/specs/spec-van-dao-workspace/SPEC.md
  - _bmad-output/specs/spec-van-dao-workspace/stories.yaml
  - _bmad-output/specs/spec-van-dao-workspace/pham-vi-mvp.md
---

# Vấn Đạo - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Vấn Đạo, decomposing the requirements from the PRD and Architecture spine into implementable stories. No UX design contract exists (product is 100% conversational Claude Code plugin — bmad-ux was evaluated and deferred to Vòng 3 for the one visual touchpoint, FR31). `SPEC.md` + `stories.yaml` (bmad-spec output) are used as cross-reference — they already distill 17 capabilities into a proposed 19-story sequence (CAP-16 covers first-run setup, CAP-17 covers chỉ điểm — both added later while rà-ing story order); epics here group those stories, they do not re-derive them from scratch.

## Requirements Inventory

### Functional Requirements

FR1: Hệ thống phải giải nghĩa được ý và nội dung cơ bản của một cuốn sách (PDF/EPUB) — không chỉ trích xuất chữ nguyên văn — đủ để làm nguồn cho việc dạy; tự đánh dấu chỗ có độ tin cậy giải nghĩa thấp.
FR1a: Trước khi hỏi ngược từng ý trong một chương, hệ thống phải trình tóm lược/mô hình tổng quan chương đó (dựa trên lớp giải nghĩa FR1) — căn cứ theo thành phần "Supportive Information" của mô hình 4C/ID (van Merriënboer & Kirschner, *Ten Steps to Complex Learning*, 3rd ed., 2018).
FR2: Không dạy tiếp mà không hỏi ngược: mỗi ý phải chốt bằng một câu hỏi, chờ người học trả lời trước khi đi tiếp.
FR2a: Khi một câu nghiệm công đang treo, không đáp câu hỏi trùng câu đó — hỏi ngược lại, giảng lại bằng ví dụ khác nếu cần.
FR3: Quan niệm cũ phải được nêu thành lời và đối chất trước khi dạy nội dung mới trái với nó.
FR3a: Quan niệm cũ đã nêu không tự coi là đã gỡ — thừa nhận bằng lời chỉ đưa tới "đang gỡ", cần bằng chứng trong bài mới sang "đã gỡ"; tái phát là trạng thái riêng.
FR4: Mức gợi ý/giàn giáo phải co giãn theo tình trạng thật của người học — tăng lại khi vấp, không chỉ giảm một chiều.
FR5: Chỉ tính một ý/chương là "đạt" khi người học chứng minh vận dụng được vào tình huống cụ thể.
FR6: Lộ đồ phải được trình người học duyệt trước khi bắt đầu học, kèm số chương và ước lượng thời lượng.
FR7: Giáo án phải được soạn ra file trước khi dạy mỗi chương.
FR8: Vai dạy và vai chấm phải là hai tiến trình AI tách biệt; vai chấm không kế thừa hội thoại dạy (không dùng fork).
FR9: Giám khảo (sinh đề, coi thi) không được chấm.
FR10: Mọi phán quyết đạt/chưa đạt của Nghiệm Công Sứ phải trích được câu cụ thể trong bài làm.
FR11a: Ở khảo thí, phải có người soát thứ hai chấm độc lập theo mục tiêu gốc, không đọc tiêu chí chi tiết.
FR11b: Hai người soát cố ý không bàn bạc với nhau, giữ trực giao.
FR11c: Chấp nhận tần suất cờ bất đồng cao hơn để đổi lấy khả năng bắt lỗi khác loại.
FR12a: Khi hai bên chấm không khớp, hệ ghi "cờ bất đồng", không chặn người học; cân bằng thì nghiêng về người học.
FR12b: Cờ bất đồng không giấu nhưng không tự đẩy thông báo giữa lúc học.
FR13: Gợi ý học gì tiếp luôn kèm lối tự nhập, không ép một hướng duy nhất.
FR14: Mọi gợi ý phải nói rõ nguồn (dữ liệu thật hay suy đoán).
FR15: Gợi ý là suy đoán phải bắt người học xác nhận thêm trước khi coi là đã chấp nhận.
FR16: Tuyên bố "đang ở bậc X" chỉ khi có ≥2 nguồn bằng chứng độc lập.
FR17: Không công bố bậc khi κ dưới ngưỡng 0,6 — chỉ nêu dấu hiệu quan sát được.
FR18: Định bậc chạy nhiều lần độc lập, dùng độ tản mát làm thước đo độ tin — gọi "đa mẫu, đo độ tản mát", không gọi "self-consistency".
FR19: Mọi nội dung về cảnh giới/bậc phải khung là giả thuyết đang kiểm chứng.
FR20: Trước khi công bố cảnh giới, phải hiệu chuẩn — so khớp với người chấm tay trên ≥20 mẫu, tính κ.
FR21: Báo cáo hiệu chuẩn phải kèm % khớp thô song song với κ.
FR22: Sổ đạo tâm phải do chính người học tự ghi; không vai nào được ghi hộ.
FR23: Nghi thức chỉ được kích hoạt khi có việc thật đứng sau.
FR24: Nhánh hạ sơn/phục mệnh phải nhận cả báo cáo thất bại, không chỉ thành công.
FR25: Vào chương mới phụ thuộc chương trước, hệ phải nhắc lại nội dung liên quan trước khi dạy ý mới.
FR26: Hết chương cuối một quyển, trước khảo thí, hệ phải hệ thống hoá lại các ý xuyên suốt các chương.
FR27: Quay lại chương đang dở ở phiên mới, hệ phải hỏi lại một hai câu để tự quyết định đi tiếp hay ôn lại.
FR28: Bỏ giữa chừng là tạm dừng hợp lệ — giữ nguyên lộ đồ và giáo án.
FR29: Sai lầm lặp lại cùng chỗ thì bồi ghi chú vào lớp chú giải riêng — không sửa gốc, không mang chi tiết tình huống thật ra ngoài.
FR30: Gợi sách tiếp theo trả về tối đa 3 lựa chọn kèm lý do.
FR31: Tiến độ học phải xem được dưới dạng bản đồ trực quan, dựng lại được từ file trạng thái.
FR32: Ý định chưa được dựng ở bản đang chạy phải trả lời rõ "chưa hỗ trợ ở bản này".
FR33: Hệ không được khen ngợi mang tính xã giao/nịnh bợ ở bất kỳ phản hồi nào.
FR34: Khi plugin bật lần đầu, hệ phải hỏi ngôn ngữ giao tiếp qua `userConfig` — hỏi đúng một lần, phiên sau nạp lại.
FR35: Bái sư phải cho người học đặt tên riêng cho 4 vai nói-với-người-học (Trưởng môn, Tàng kinh trưởng lão, Thư linh, Giám khảo) — gợi ý sẵn kèm tự nhập, không ép chọn danh sách.
FR36: Sau khi khai vai/mạch, Trưởng môn phải chỉ điểm — gọi tên sách cụ thể cho người học tự đi tìm, đủ 5 trường, số lượng co giãn theo đã biết/chưa biết, mức chắc chắn nói trước khi đưa danh sách; phân biệt rõ "bản hỏng" (giữ quyển, tìm bản khác) khác "không thấy" (đổi quyển khác).
FR37: Pha thiết kế sư phạm (thu bí kíp) phải dừng chờ người dùng sửa và duyệt trước khi sinh cấp chương — máy chỉ đề xuất kèm lý do, không tự quyết xương sống/tiêu chí đạt/điểm hạ sơn.
FR38: Khi không rút được chữ từ file, hệ phải dừng ngay, báo tìm bản khác — không OCR, không tạo bí kíp rỗng.
FR39: Bí kíp có hai mức hợp lệ — đủ dùng (vào kho ngay) và đủ chuẩn (chia sẻ được, bồi sau khi học chương đó); dạy ở mức đủ dùng phải nói rõ đang chấm theo mục tiêu.

### NonFunctional Requirements

NFR1: Vai chấm phải chạy trên subagent tươi (ngữ cảnh sạch), không bao giờ fork phiên dạy — kiểm được bằng ca đối chứng (chạy có/không ngữ cảnh cấm, xác nhận khác biệt kết quả).
NFR2: Mọi thay đổi trạng thái phải là ghi thêm (append-only) — không sửa file trạng thái tại chỗ; trạng thái hiện tại luôn suy được từ artifact/log gần nhất. Nếu tiến trình bị ngắt giữa lúc ghi một dòng JSONL (mất điện, crash), dòng cuối có thể dở dang — khi đọc lại, script/skill phải phát hiện dòng cuối không parse được và bỏ qua nó khi suy trạng thái (coi như chưa từng ghi), không được crash hay coi cả file hỏng.
NFR3: Mỗi vùng dữ liệu dưới `~/.vandao/` chỉ có đúng một vai được phép ghi — vai khác chỉ đọc qua `.pham-vi.json` đã lọc theo mạch.
NFR4: Mọi skill phải có trigger eval (đúng lúc được gọi) và functional/behavioral eval (chạy ra đúng kết quả) trước khi coi là hoàn thành — quality-gate bắt buộc, không tuỳ chọn.
NFR5: Không thu telemetry — mọi dữ liệu học tập (sách, câu trả lời, đạo tâm) ở lại máy người dùng, không server riêng của Vấn Đạo thu thập.
NFR6: Nội dung nạp vào ngữ cảnh mỗi phiên phải có chặn trên cố định kích thước; việc dùng-một-lần phải chạy trong subagent tươi, không phải bước trong skill chính (chống context rot).
NFR7: `book-to-skill` (virgiliojr94) là phụ thuộc ngoài bắt buộc cho việc thu sách — phải verify chạy thật trước khi tích hợp, không chỉ đọc tài liệu. **Lớp engine đã verify chạy thật 2026-08-26** (`extract_single_file()` chạy thành công trên PDF thật + EPUB thật, `ExtractionError` xác nhận fire đúng). **Lớp skill (`npx skills add`, hội thoại Pha 1) chưa verify** — để dành lúc dev-agent thật triển khai Story 1.4.
NFR8: Cơ chế `userConfig` (`.claude-plugin/plugin.json`) phải verify chạy thật trên plugin cài cục bộ trước khi tích hợp FR34. **Verify xong 2026-08-26**: field `communication_language` thêm vào `van-dao/.claude-plugin/plugin.json`, `claude plugin validate --strict` PASS, cài thật qua `claude plugin install --config` xác nhận giá trị lưu đúng `~/.claude/settings.json`. **Sửa overclaim sau tự kiểm:** cài qua CLI KHÔNG kèm `--config` thì Claude Code KHÔNG tự chặn/hỏi — chỉ cảnh báo. `nhap-mon` phải tự kiểm field và hướng dẫn `/plugin configure` nếu chưa đặt.

### Additional Requirements

- Không có starter template — brownfield trên cấu trúc plugin đã tồn tại (`van-dao/` repo riêng); cây thư mục cố định đã chốt ở `ARCHITECTURE-SPINE.md` § Structural Seed.
- Không có hạ tầng/triển khai riêng — chạy hoàn toàn cục bộ qua Claude Code, không server, không staging/prod.
- Phụ thuộc tích hợp ngoài: `book-to-skill` (virgiliojr94) cho phân giải PDF/EPUB — engine qua pip, skill qua `npx skills add`.
- Không có di trú dữ liệu — dự án mới, chưa có dữ liệu người dùng cũ cần chuyển.
- Giám sát/logging: 3 hook hệ thống (`nap-ho-so.sh` SessionStart · `kiem-thu.sh` SubagentStop · `ghi-nhat-ky.sh` Stop) + `kiem-thu.py` gác mọi thư liên vai theo schema.
- Không có API bên ngoài/versioning — chỉ có schema nội bộ (`tham-chieu/*.schema.md`) đi cặp script kiểm tương ứng; đổi hành vi phải đổi cả hai cùng lúc trong cùng một thay đổi.
- Envelope lỗi dùng chung cho mọi script mới: ba mức `L()`/`C()`/`G()`, `--json` cho đầu ra máy đọc, mã thoát 0/1/2 — không phát minh envelope riêng mỗi script.

### UX Design Requirements

Không áp dụng — không có UX design contract (sản phẩm 100% hội thoại; điểm chạm thị giác duy nhất, FR31 bản đồ trực quan, đã hoãn sang Vòng 3 và sẽ chạy `bmad-ux` phạm vi hẹp khi tới lượt).

### FR Coverage Map

FR1: Epic 1 - Giải nghĩa sách nạp vào
FR1a: Epic 3 - Tóm lược mở đầu chương (4C/ID Supportive Information)
FR2: Epic 3 - Hỏi ngược mỗi ý
FR2a: Epic 3 - Không đáp câu trùng nghiệm công đang treo
FR3: Epic 3 - Đối chất quan niệm cũ
FR3a: Epic 3 - Tâm ma: thừa nhận ≠ gỡ, vòng đời 4 trạng thái
FR4: Epic 3 - Giàn giáo co giãn
FR5: Epic 3 - Mastery gate "đạt"
FR6: Epic 2 - Lộ đồ duyệt trước khi học
FR7: Epic 3 - Giáo án ra file trước mỗi chương
FR8: Epic 4 - Vai dạy/vai chấm tách biệt
FR9: Epic 4 - Giám khảo không chấm
FR10: Epic 4 - Phán quyết trích câu cụ thể
FR11a: Epic 4 - Soát thứ hai độc lập ở khảo thí
FR11b: Epic 4 - Hai soát không bàn bạc, trực giao
FR11c: Epic 4 - Chấp nhận cờ bất đồng cao hơn
FR12a: Epic 4 - Cờ bất đồng không chặn, nghiêng người học
FR12b: Epic 4 - Cờ bất đồng không tự đẩy thông báo
FR13: Epic 7 - Gợi ý học tiếp kèm lối tự nhập
FR14: Epic 7 - Gợi ý nói rõ nguồn thật/suy đoán
FR15: Epic 7 - Suy đoán cần xác nhận thêm
FR16: Epic 11 - Tuyên bố cảnh giới cần ≥2 nguồn
FR17: Epic 11 - Không công bố bậc khi κ<0,6
FR18: Epic 11 - Đa mẫu, đo độ tản mát
FR19: Epic 11 - Khung giả thuyết đang kiểm chứng
FR20: Epic 11 - Hiệu chuẩn ≥20 mẫu, tính κ
FR21: Epic 11 - Báo cáo hiệu chuẩn kèm % khớp thô
FR22: Epic 5 - Đạo tâm tự ghi, không vai nào ghi hộ
FR23: Epic 1 (bái sư/thu bí kíp) + Epic 11 (đột phá cảnh giới) - Nghi thức chỉ kích hoạt khi có việc thật
FR24: Epic 8 - Hạ sơn/phục mệnh nhận cả báo cáo thất bại
FR25: Epic 10 - Nhắc lại nội dung liên quan trước chương phụ thuộc
FR26: Epic 10 - Hệ thống hoá cuối quyển trước khảo thí
FR27: Epic 10 - Nối mạch cũ hỏi lại 1-2 câu
FR28: Epic 10 - Xuất quan là tạm dừng hợp lệ
FR29: Epic 12 - Chú Giải Sứ bồi sai lầm phổ biến
FR30: Epic 7 - Gợi sách tiếp theo tối đa 3 lựa chọn
FR31: Epic 9 - Bản đồ trực quan tiến độ
FR32: Epic 6 - Trả lời rõ khi chưa hỗ trợ
FR33: Epic 6 - Không khen sáo rỗng
FR34: Epic 1 - Chọn ngôn ngữ giao tiếp lúc bật plugin (userConfig)
FR35: Epic 1 - Đặt tên 4 vai nói-với-người-học trong bái sư
FR36: Epic 1 - Chỉ điểm sách cho đệ tử đi tìm, sau bái sư trước thu bí kíp
FR37: Epic 1 - Người sửa-duyệt bắt buộc ở pha 2 thu bí kíp
FR38: Epic 1 - Dừng khi không rút được chữ
FR39: Epic 1 - Hai mức hợp lệ đủ dùng/đủ chuẩn

NFR1-NFR7 và Additional Requirements không có epic riêng (không mang giá trị người dùng độc lập) — threading vào implementation notes của epic liên quan lúc viết story ở step-03 (ví dụ NFR7 verify book-to-skill → Epic 1; NFR4 eval-gate → mọi epic; 3 hook hệ thống → Epic 3/4/6).

## Epic List

**Phạm vi dựng theo Vòng** (nguồn: `pham-vi-mvp.md`, companion SPEC — quyết định phạm vi MVP chi tiết theo capability; bảng dưới nhóm lại theo epic để tra nhanh, không thay thế tài liệu gốc):

| Vòng | Epic | Capability chính (pham-vi-mvp.md) |
|---|---|---|
| **MVP (Vòng 1-2, bước 1-13)** | Epic 1, 2, 3, 4, 5, 6 | CAP-1, CAP-2/3, CAP-4, CAP-7, CAP-8 (chỉ bái sư+thu bí kíp — đột phá cảnh giới CHƯA dùng được), CAP-14, CAP-15 |
| **Vòng 3 (nhiều quyển/mạch, bước 14-19)** | Epic 7, 8, 9, 10 | CAP-5, CAP-9, CAP-10, CAP-12, CAP-13 |
| **Vòng 4 (đo và tự sửa, bước 20-25)** | Epic 11, 12 | CAP-6, CAP-11 |

Milestone MVP là "đột phá quyển đầu tiên" (đặc tả §16 bước 13, cuối Vòng 2) — khép được vòng Dạy→Soát (Epic 1-4), cộng Đạo tâm (Epic 5) và điểm đóng đối thoại đáng tin cậy (Epic 6). Epic 7-12 dựng sau, không chặn MVP.

### Epic 1: Nhập môn, chỉ điểm & nạp bí kíp
Người học thiết lập ban đầu (ngôn ngữ, tên các vai), bái sư (khai vai/mạch), được Trưởng môn chỉ điểm sách cụ thể để tự đi tìm, rồi nạp cuốn sách tìm được (PDF/EPUB) vào tàng kinh các — hệ giải nghĩa được ý sách, không chỉ trích chữ nguyên văn. Đúng thứ tự đặc tả §10: Bái sư → Chỉ điểm → (Thỉnh sách, ngoài hệ) → Thu bí kíp.
**FRs covered:** FR1, FR23 (phần bái sư/thu bí kíp), FR34, FR35, FR36, FR37, FR38, FR39
**Ghi chú:** Nghi thức chỉ kích hoạt khi việc thật đã xảy ra (khai vai/mạch xong); phụ thuộc `book-to-skill` đã verify chạy thật (NFR7). "Ghi nhập môn ký" (đặc tả dòng 197) và Epic 5 (đạo tâm) đặc tả nhóm cùng bước 7 §16 (đặc tả dòng 2005: `nhap-mon` · `dao-tam` · `bin/tang-kinh-cac.py`) — nhưng theo đúng thứ tự liệt kê 1→12, Story 1.2 (epic này) là nơi **xây** cơ chế tự-ghi/`disable-model-invocation`; Story 5.1 (Epic 5) **tái dùng** lại, không xây lại — tránh forward dependency (Epic 1 đứng trước Epic 5 trong danh sách). **Lý do dùng cơ chế này ở đây khác Epic 5:** nhập môn ký đứng trên Cialdini Commitment & Consistency (1984/2006 — cam kết tự viết tăng khả năng theo đuổi), không phải Pierce et al. 2003 của FR22 (sở hữu tâm lý với công sức đã bỏ ra) — dùng chung cơ chế, khác lý do, story không nên copy nguyên rationale của Story 5.1.

### Epic 2: Lộ đồ trình duyệt trước khi học
Người học thấy trước lộ đồ cả quyển (số chương, ước lượng thời lượng) và duyệt trước khi bắt đầu; nháp sống sót qua gián đoạn phiên (AD-9).
**FRs covered:** FR6

### Epic 3: Dạy có nền tảng — tóm lược, hỏi ngược, đối chất, giàn giáo co giãn
Mỗi chương mở đầu bằng tóm lược/mô hình tổng quan (FR1a, căn cứ 4C/ID Supportive Information — van Merriënboer & Kirschner 2018); giáo án ra file trước khi dạy; mỗi ý chốt bằng câu hỏi ngược (không đáp câu trùng nghiệm công đang treo); quan niệm cũ được đối chất trước nội dung trái ngược (thừa nhận bằng lời không tự coi là đã gỡ — cần bằng chứng trong bài); mức gợi ý co giãn theo vấp/vững; chỉ tính "đạt" khi vận dụng được vào tình huống cụ thể.
**FRs covered:** FR1a, FR2, FR2a, FR3, FR3a, FR4, FR5, FR7

### Epic 4: Soát độc lập, có căn cứ
Vai chấm tách biệt vai dạy (subagent tươi, không fork); Giám khảo không chấm; mọi phán quyết trích được câu cụ thể; khảo thí có soát thứ hai độc lập, trực giao, cờ bất đồng khi không khớp (không chặn người học).
**FRs covered:** FR8, FR9, FR10, FR11a, FR11b, FR11c, FR12a, FR12b

### Epic 5: Đạo tâm tự ghi
Người học có sổ đạo tâm ghi lại con đường học — không vai nào ghi hộ.
**FRs covered:** FR22
**Ghi chú:** Cơ chế tự-ghi/`disable-model-invocation` đã xây ở Epic 1 (Story 1.2 — "ghi nhập môn ký") được tái dùng ở đây cho sổ đạo tâm, không xây lại — đúng thứ tự liệt kê 1→12, tránh forward dependency.

### Epic 6: Đối thoại đáng tin cậy
Ý định ngoài phạm vi được trả lời rõ "chưa hỗ trợ ở bản này"; không có phản hồi khen sáo rỗng/nịnh bợ ở bất kỳ đâu — điểm đóng MVP, chạy lại toàn bộ eval suite sau epic này.
**FRs covered:** FR32, FR33

### Epic 7: Định hướng & khám phá kho
Người học được gợi ý học gì tiếp (kèm lối tự nhập, nói rõ nguồn thật/suy đoán, suy đoán cần xác nhận thêm) và gợi sách tiếp theo tối đa 3 lựa chọn kèm lý do.
**FRs covered:** FR13, FR14, FR15, FR30
**Ghi chú:** Cùng vai Trưởng môn (skill `truong-mon`) với Epic 8 và phần cache của Epic 9 — đặc tả (dòng 1756) nói rõ 4 skill của Trưởng môn là 4 thao tác của CÙNG một vai, tách file vì khác thời điểm kích hoạt, không phải khác trách nhiệm. Epic này tách khỏi Epic 8 vì độc lập giá trị (gợi ý trong hệ vs mang ra đời thực), không phải vì khác vai. Ghi trong `truong-mon/` — cùng thư mục dữ liệu vai với Epic 8/Epic 9, cần tránh xung đột ghi tại chỗ khi viết story.

### Epic 8: Hạ sơn & phục mệnh
Người học mang kiến thức ra việc thật, báo cáo lại — nhận cả báo cáo thất bại, không chỉ thành công.
**FRs covered:** FR24
**Ghi chú:** Skill `ha-son`/`phuc-menh` — cùng vai Trưởng môn với Epic 7 (không phải vai riêng). Tách epic vì khoảnh khắc trải nghiệm khác Định hướng (rời hệ ra việc thật, rồi quay lại báo cáo), độc lập giá trị. Cùng thư mục `truong-mon/` với Epic 7/Epic 9.

### Epic 9: Bản đồ trực quan tiến độ
Tiến độ nhiều quyển/mạch xem được dạng bản đồ, dựng lại được từ artifact gốc (Loại 3 — dẫn xuất/cache theo AD-5).
**FRs covered:** FR31
**Ghi chú:** Cache `ban-do.json` nằm trong `truong-mon/` (đặc tả dòng 1924) — cùng thư mục dữ liệu vai với Epic 7/Epic 8; khác cơ chế thật sự (Loại 3 dẫn xuất/chỉ đọc vs Loại 2 state machine của Epic 10 trong `thu-linh`) nên vẫn tách khỏi Epic 10, nhưng story ở step-03 cần tránh xung đột ghi tại chỗ trong `truong-mon/` với Epic 7/Epic 8.

### Epic 10: Liền mạch học tập
Vào chương phụ thuộc, hệ nhắc lại nội dung liên quan; hết quyển, hệ thống hoá lại các ý trước khảo thí; quay lại chương dở ở phiên mới, hệ hỏi lại 1-2 câu; bỏ giữa chừng là tạm dừng hợp lệ, giữ nguyên lộ đồ/giáo án.
**FRs covered:** FR25, FR26, FR27, FR28

### Epic 11: Đo cảnh giới có hiệu chuẩn
Tuyên bố cảnh giới cần ≥2 nguồn độc lập, đa mẫu đo độ tản mát, chỉ công bố khi κ đạt ngưỡng hiệu chuẩn (≥20 mẫu, báo cáo cả % khớp thô); mọi nội dung bậc/cảnh giới khung là giả thuyết đang kiểm chứng; nghi thức đột phá cảnh giới kích hoạt ở đây.
**FRs covered:** FR16, FR17, FR18, FR19, FR20, FR21, FR23 (phần đột phá cảnh giới)

### Epic 12: Chú Giải Sứ bồi sai lầm phổ biến
Sai lầm lặp lại cùng chỗ được bồi ghi chú vào lớp chú giải riêng — không sửa gốc, không mang chi tiết tình huống thật ra ngoài.
**FRs covered:** FR29

## Epic Details

### Epic 1: Nhập môn, chỉ điểm & nạp bí kíp

**Mục tiêu:** Người học thiết lập ban đầu, bái sư, được Trưởng môn chỉ điểm sách để tự đi tìm, rồi nạp cuốn sách tìm được vào tàng kinh các. Đúng luồng đặc tả §10: Bái sư → Chỉ điểm → *(Thỉnh sách, ngoài hệ)* → Thu bí kíp.
**FRs covered:** FR1, FR23 (bái sư/thu bí kíp), FR34, FR35, FR36, FR37, FR38, FR39 · **NFR:** NFR7, NFR8

#### Story 1.1: Thiết lập ban đầu — ngôn ngữ giao tiếp

As a người mới cài plugin Vấn Đạo,
I want được giúp chọn ngôn ngữ giao tiếp ngay khi bật plugin lần đầu,
So that mọi phiên sau đó các vai nói đúng ngôn ngữ tôi chọn mà không phải chọn lại.

**Acceptance Criteria:**

**Given** plugin `van-dao` được bật lần đầu trên máy
**When** Claude Code xử lý `.claude-plugin/plugin.json`
**Then** người dùng có thể chọn ngôn ngữ giao tiếp qua `userConfig` (field `communication_language`)
**And** given người dùng đã chọn ngôn ngữ, một phiên mới bắt đầu, hệ nạp lại đúng lựa chọn đã lưu — không hỏi lại
**And** cơ chế `userConfig` đã verify chạy thật 2026-08-26 (NFR8) — `van-dao/.claude-plugin/plugin.json` có field `communication_language` (type=string, title bắt buộc, default=Vietnamese), `claude plugin validate --strict` PASS, `claude plugin install --config communication_language=<value>` lưu đúng vào `~/.claude/settings.json` → `pluginConfigs["van-dao@van-dao"].options`
**And** given plugin cài KHÔNG kèm `--config` (đường CLI thật đã verify), Claude Code KHÔNG tự chặn/hỏi — chỉ in cảnh báo "1 userConfig option not yet set — run `/plugin configure` hoặc `--config KEY=VALUE`" và cài xong với field trống; **story này không được giả định Claude Code tự động hỏi khi bật plugin** — `nhap-mon` phải tự kiểm tra `communication_language` đã set chưa, và nếu chưa thì chủ động hướng dẫn người dùng chạy `/plugin configure van-dao@van-dao`. Đường cài tương tác thật (người dùng có TTY, không qua CLI headless) vẫn chưa verify được — có thể khác hành vi, cần kiểm khi có điều kiện
**And** `plugin.json` hiện tại đã có field `userConfig.communication_language` — chỉ thêm field vào file đã tồn tại, không tạo file/cơ chế cấu hình mới song song

#### Story 1.2: Bái sư — đặt tên môn phái, khai vai/mạch, đặt tên 4 vai

As a người học mới,
I want bái sư nhập môn — đặt tên môn phái, khai vai và mạch muốn luyện (hoặc được hỏi "làm nghề gì" nếu chưa biết), và đặt tên riêng cho 4 vai sẽ đồng hành cùng mình,
So that tôi chính thức bắt đầu hành trình với một bản sắc rõ ràng, không phải điền form vô cảm.

**Acceptance Criteria:**

**Given** người học gõ `/vd:nhap-mon` lần đầu
**When** bái sư bắt đầu
**Then** hệ hỏi tên môn phái và ghi nhập môn ký qua cơ chế tự-ghi — story này XÂY cơ chế `disable-model-invocation` ở tầng skill/tool (không chỉ quy ước lời nói trong prompt): một vai AI thử ghi hộ hoặc soạn sẵn nội dung để người học duyệt phải bị chặn ở tầng cơ chế, một ca thử "AI cố ghi hộ" phải thất bại rõ ràng, không âm thầm thành công. Story 5.1 (đạo tâm) tái dùng nguyên cơ chế này, không xây lại
**And** given người học đã biết muốn luyện gì, khi được hỏi, họ khai thẳng vai + mạch
**And** given người học chưa biết muốn luyện gì, khi được hỏi, hệ hỏi VAI trước ("ngươi làm nghề gì") — không hỏi mạch trước — rồi gợi ý mạch kèm cờ nguồn gợi ý, cho chọn từ gợi ý hoặc tự nhập
**And** given đang trong bái sư, tới bước đặt tên vai, hệ gợi ý tên cho 4 vai nói-với-người-học và cho tự nhập tên khác; 4 vai âm thầm không được hỏi
**And** given người học vừa khai xong vai/mạch, nghi thức bái sư kích hoạt
**And** given người học hỏi về đột phá cảnh giới ở MVP, hệ trả lời "chưa hỗ trợ ở bản này"
**And** given người học đã có hồ sơ (đã từng bái sư), khi gõ `/vd:nhap-mon` lần nữa, hệ KHÔNG tạo hồ sơ mới đè lên hồ sơ cũ và KHÔNG kích hoạt lại nghi thức bái sư vô cớ — chỉ nghi thức thật khi có việc thật mới đứng sau (FR23)

#### Story 1.3: Chỉ điểm — Trưởng môn gọi tên sách

As a người học vừa khai xong vai/mạch,
I want Trưởng môn chỉ cho tôi tên sách cụ thể để tự đi tìm — không phải tự tôi mò kiếm không định hướng,
So that tôi có việc rõ ràng để làm tiếp, dù tàng kinh các đang trống trơn.

**Acceptance Criteria:**

**Given** người học vừa khai vai/mạch xong
**When** Trưởng môn chỉ điểm
**Then** mỗi chỉ điểm nêu đủ 5 trường (tên, tác giả, năm/ấn bản, công pháp hay tâm pháp, vì sao) — không đưa tên trần
**And** given người học đã biết muốn luyện gì, chỉ điểm nhận 3 công pháp + 2 tâm pháp; given chưa biết, nhận 1+1 kèm câu "thỉnh được rồi quay lại, ta chỉ tiếp"
**And** given kho chưa có dữ liệu thật lẫn khai báo từ bí kíp (ca mặc định ở n=1), câu rào "đây là suy đoán" xuất hiện trước danh sách, không phải sau
**And** given một chỉ điểm sách công pháp, luôn kèm gợi ý tâm pháp đỡ trần tương ứng
**And** given người học xin chỉ điểm lần nữa, mọi mục `dang_treo` cũ chuyển `het_hieu_luc` (không cộng dồn) nhưng vẫn tra lại được nếu người học hỏi tên cũ
**And** given người học quay lại hệ qua bất kỳ lối vào nào (không riêng xin chỉ điểm lần nữa) mà còn chỉ điểm `dang_treo` chưa thu bí kíp, hệ nhắc nhẹ một câu ("còn quyển X đang chờ") — pull khi họ tự quay lại, không tự đẩy thông báo giữa chừng (giữ đúng tinh thần FR12b)
**And** given người học báo "không tìm được quyển này" (`khong_thay`), hệ ghi `chi-diem-hong.jsonl` và chỉ điểm quyển khác
**And** given người học báo `khong_thay` từ 2 lần liên tiếp trở lên trong cùng một vòng chỉ điểm, lần chỉ điểm kế tiếp đổi chiến lược — ưu tiên sách phổ biến/dễ tìm hơn, hoặc hỏi thêm ràng buộc từ người học — không lặp lại y hệt cách chọn cũ
**And** given người học tìm thấy sách nhưng bản này không rút được chữ (`ban_hong`), hệ GIỮ NGUYÊN quyển trong chỉ điểm và khuyên tìm bản khác — khác hẳn xử lý `khong_thay`, không gạch khỏi chỉ điểm
**And** given kho đã có đủ dữ liệu thật (≥5 người cùng vai) hoặc có khai từ bí kíp, chỉ điểm chuyển từ mức suy đoán sang kèm số liệu/kèm nguồn (bảng quyết định §10.3) — không giữ mãi ở mức suy đoán một khi đã có bằng chứng thật để dùng
**And** given kho (kể cả nguồn suy đoán của model) có ít hơn số lượng chỉ điểm đã hứa (3+2 hoặc 1+1), hệ trả đúng số lượng có, không bịa thêm cho đủ — đúng nguyên tắc đã áp cho Story 7.2

#### Story 1.4: Thu bí kíp

As a người học đã tìm được sách từ chỉ điểm,
I want đưa PDF/EPUB vào tàng kinh các, tự sửa-duyệt phần thiết kế sư phạm máy đề xuất, và biết rõ bí kíp đang ở mức hợp lệ nào,
So that tôi có nguồn nội dung sư phạm đáng tin cậy do chính tôi xác nhận, không phải máy tự quyết một mình.

**Acceptance Criteria:**

**Given** một file PDF/EPUB không rút được chữ (scan ảnh, lỗi font)
**When** giám định chạy
**Then** hệ dừng ngay, báo "tìm bản khác" — không OCR, không tạo bí kíp rỗng
**And** given rút được chữ nhưng nội dung không thành câu có nghĩa (tỉ lệ ký tự lạ cao bất thường, hoặc mất cấu trúc câu — ví dụ sách chủ yếu hình/bảng mà giám định chỉ vét được vài từ rời rạc), hệ xử lý giống hệt trường hợp không rút được chữ — dừng, báo tìm bản khác, không âm thầm sinh bí kíp từ nội dung rác
**And** given giám định qua, tới pha 2 (thiết kế sư phạm), máy chỉ đề xuất kèm lý do cho từng đề xuất (xương sống, tiêu chí đạt, điểm hạ sơn) — không tự quyết
**And** given đề xuất pha 2 đã có mà người dùng chưa sửa-và-duyệt, pha 3 (sinh cấp chương) không được chạy
**And** given người dùng duyệt xong, pha 3 chạy, bí kíp được gắn đúng một trong hai mức: đủ dùng (mục tiêu/giả định nền/tiêu chí đạt thô/≥1 câu vận dụng) hoặc đủ chuẩn (thêm tiêu chí chi tiết/sai lầm phổ biến/worked example)
**And** given một chương ở mức đủ dùng được dạy, Thư linh nói rõ "chưa có tiêu chí chi tiết, chấm theo mục tiêu" — không để người học tưởng đang bị chấm chặt hơn thực tế
**And** given người học thu cùng một cuốn sách đã có sẵn trong kho (trùng), hệ KHÔNG tạo bản sao và KHÔNG ghi đè bí kíp cũ (bí kíp gốc BẤT BIẾN) — báo rõ sách đã có trong kho, hỏi người học muốn làm gì tiếp (ví dụ tiếp tục học bản đã có) thay vì âm thầm xử lý
**And** given bí kíp vào kho thành công, nghi thức thu bí kíp kích hoạt, chỉ điểm chuyển `da_thu`
**And** lớp engine của `book-to-skill` (`extract_single_file()`, cài qua `pip`/`uv run --with`) đã verify chạy thật 2026-08-26 — PDF thật (arXiv, 15 trang, pdftotext, has_toc=False đúng) và EPUB thật (Gutenberg, có TOC, has_toc=True đúng) đều trích xuất thành công; `ExtractionError` xác nhận fire đúng khi input không parse được
**And** lớp skill (`npx skills add virgiliojr94/book-to-skill`, hội thoại Pha 1 theo SKILL.md Bước 0-3) CHƯA verify riêng — story này chưa được coi là hoàn thành cho tới khi lớp skill cũng verify chạy thật lúc triển khai (NFR7)
**And** độ phủ verify engine hiện tại còn hẹp (đúng 2 mẫu: 1 PDF arXiv 15 trang, 1 EPUB Gutenberg) — trước khi coi Epic 1 sẵn sàng ra mắt thật, khuyến nghị thử thêm 1-2 mẫu đa dạng cấu trúc hơn (sách nhiều công thức/bảng, sách đối thoại) để biết điểm mù còn lại, không bắt buộc nhưng phải là quyết định có ý thức

### Epic 2: Lộ đồ trình duyệt trước khi học

**Mục tiêu:** Người học thấy trước lộ đồ cả quyển và duyệt trước khi bắt đầu; nháp sống sót qua gián đoạn phiên.
**FRs covered:** FR6

#### Story 2.1: Lộ đồ trình duyệt trước khi dạy

As a người học vừa thu được bí kíp,
I want thấy trước lộ đồ cả quyển (số chương, ước lượng thời lượng) và duyệt trước khi Thư linh bắt đầu dạy,
So that tôi biết trước hành trình dài bao lâu, không bị dạy ngay mà chưa đồng ý lộ trình.

**Acceptance Criteria:**

**Given** một bí kíp vừa vào kho (Story 1.4 xong)
**When** Thư linh sinh lộ đồ
**Then** lộ đồ hiện đủ số chương và ước lượng thời lượng, đánh dấu rõ đây là ước lượng thô, không phải cam kết
**And** given lộ đồ vừa sinh xong, hệ ghi nháp NGAY (append, đúng AD-2) — không chờ đóng máy mới ghi
**And** given người học đóng máy giữa lúc lộ đồ chưa duyệt rồi mở lại đúng bí kíp, hệ trình lại đúng bản nháp đã lưu — không sinh bản khác (AD-9)
**And** given lộ đồ chưa được duyệt, không chương nào được dạy
**And** given lộ đồ đã duyệt nhưng người học muốn sửa sau đó, sửa lộ đồ bắt buộc duyệt lại — mỗi lần duyệt là một bản ghi mới, không sửa tại chỗ (AD-6)

### Epic 3: Dạy có nền tảng — tóm lược, hỏi ngược, đối chất, giàn giáo co giãn

**Mục tiêu:** Mỗi chương mở đầu bằng tóm lược; mỗi ý chốt bằng câu hỏi ngược; quan niệm cũ được đối chất; mức gợi ý co giãn theo vấp/vững; chỉ tính "đạt" khi vận dụng được.
**FRs covered:** FR1a, FR2, FR2a, FR3, FR3a, FR4, FR5, FR7

#### Story 3.1: Tóm lược mở đầu, giáo án, hỏi ngược, đối chất quan niệm cũ

As a người học đã duyệt lộ đồ,
I want mỗi chương mở đầu bằng một bản tóm lược, được hỏi ngược từng ý thay vì nghe giảng suông, và được đối chất khi cách làm cũ của tôi mâu thuẫn với nội dung mới,
So that tôi hiểu khung tổng quan trước, nhớ lâu hơn nhờ tự trả lời, và không bị nhồi đè lên thói quen cũ mà không biết.

**Acceptance Criteria:**

**Given** một chương sắp được dạy
**When** Thư linh bắt đầu
**Then** giáo án được soạn ra file trước, và một bản tóm lược/mô hình tổng quan chương được trình bày trước khi hỏi ngược ý đầu tiên — tóm lược dựa trên lớp giải nghĩa FR1 đã có, không tự bịa tại chỗ
**And** given một ý đang được dạy, mỗi ý phải chốt bằng một câu hỏi, chờ người học trả lời trước khi đi ý tiếp
**And** given quan niệm cũ của người học mâu thuẫn với nội dung mới, quan niệm cũ được nêu thành lời và đối chất TRƯỚC khi dạy nội dung trái ngược — không lặng lẽ nhồi đè
**And** given người học chỉ thừa nhận bằng lời quan niệm cũ vướng, trạng thái tâm ma chuyển "đang gỡ" — KHÔNG tự coi là "đã gỡ"; chuyển "đã gỡ" đòi bằng chứng trong bài (nghiệm công/khảo thí, làm khác đi thật)
**And** given trạng thái đã "đã gỡ" nhưng dấu hiệu cũ xuất hiện lại, hệ chuyển "tái phát" — trạng thái riêng, Thư linh nói khác với người mới ("chỗ này ngươi từng vượt qua ở chương X")
**And** given người học bảo cách cũ vẫn đúng trong hoàn cảnh của họ, hệ đóng nhánh đối chất, không ép
**And** given một câu nghiệm công đang treo (chưa chấm xong), người học hỏi trùng câu đó, Thư linh KHÔNG đáp — hỏi ngược lại; nếu cần giảng lại thì dùng ví dụ KHÁC, không dùng đúng ca đang nghiệm công

#### Story 3.2: Giàn giáo co giãn, chẩn đoán và giảng lại

As a người học đang học một ý,
I want mức gợi ý co giãn theo tình trạng thật của tôi — giảm khi tôi vững, tăng lại khi tôi vấp,
So that tôi không bị bỏ mặc khi khó, và không bị giảng dài dòng khi đã hiểu.

**Acceptance Criteria:**

**Given** người học mới bắt đầu một ý
**When** Thư linh giảng
**Then** mức gợi ý đủ chi tiết ban đầu, giảm dần khi người học vững
**And** given người học sai lần hai ở cùng một chỗ, Thư linh đổi cách trình bày — không lặp lại y hệt lần một
**And** given người học sai lần ba ở cùng một chỗ, Thư linh báo lên (không tự giảng lại lần nữa)
**And** given báo cáo "có thể thiếu nền" vừa gửi lên, Thư linh nói rõ với người học đang đóng nhánh dạy ý này lại, không phải đã giải quyết xong — người học tự quyết đi tiếp, quay lại sau, hay hỏi hướng khác qua `chi-duong`; không để im lặng treo không câu trả lời nào
**And** given một ý/chương được nghiệm công, chỉ tính "đạt" khi có bằng chứng vận dụng vào tình huống cụ thể — không phải nhớ đúng chữ
**And** given chưa đạt, người học được hỗ trợ thêm rồi thử lại
**And** given người học vấp lặp lại cùng một chỗ (sai lần hai/ba), khi Thư linh gom "vấp lặp" để gửi Chú Giải Sứ (đặc tả — cạnh giao tiếp `TL → CG`), Thư linh PHẢI tự lọc bỏ chi tiết tình huống thật (tên người, công ty, dự án cụ thể) TRƯỚC khi gửi — không trông chờ một mình Chú Giải Sứ lọc ở đầu ra cuối (Story 12.1); đây là lớp phòng thủ thứ nhất, không phải lớp duy nhất, vì Thư linh (khác Chú Giải Sứ) có toàn quyền đọc `tinh-huong/` nên là nơi rò rỉ có thể xảy ra dù Chú Giải Sứ chưa từng chạm dữ liệu thô

### Epic 4: Soát độc lập, tách vai

**Mục tiêu:** Bài làm được chấm bởi vai tách biệt vai dạy, có căn cứ trích dẫn; khảo thí có soát thứ hai độc lập, cờ bất đồng khi không khớp.
**FRs covered:** FR8, FR9, FR10, FR11a, FR11b, FR11c, FR12a, FR12b
**Phạm vi:** Epic này chỉ ghi cờ bất đồng (`bat-dong.jsonl`), không bồi/sửa `tieu_chi_dat` từ dữ liệu đó — đặc tả gọi đây là "mẫu miễn phí" cho tàng kinh trưởng lão dùng để bồi tiêu chí sau (§9.5), nhưng việc tiêu thụ cờ bất đồng để cải thiện tiêu chí không thuộc 12 epic này, để dành Vòng sau.

#### Story 4.1: Soát độc lập, tách vai

As a người học vừa nộp bài,
I want được chấm bởi một vai AI hoàn toàn tách biệt khỏi vai vừa dạy tôi, với căn cứ trích dẫn cụ thể — không phải một lời khen/chê suông,
So that tôi tin kết quả chấm là thật, không phải chính người vừa dạy tự khen bài mình dạy.

**Acceptance Criteria:**

**Given** một bài làm vừa nộp
**When** Nghiệm Công Sứ chấm
**Then** Nghiệm Công Sứ chạy trên subagent tươi (ngữ cảnh sạch), không kế thừa hội thoại dạy (không dùng fork)
**And** given Thư linh gửi bài chấm, thư gửi CHỈ gồm bài chương + tiêu chí đạt — KHÔNG mang giáo án, KHÔNG mang ghi chép buổi dạy
**And** given Nghiệm Công Sứ kết luận đạt/chưa đạt, phán quyết phải trích được câu cụ thể trong bài làm làm căn cứ — không kết luận suông
**And** given Giám khảo đã sinh đề và coi thi, Giám khảo KHÔNG được chấm — tách biệt khỏi Nghiệm Công Sứ/Phúc Khảo Sứ
**And** given một khảo thí quyển, có Phúc Khảo Sứ soát thứ hai độc lập — đọc mục tiêu gốc, KHÔNG đọc tiêu chí chi tiết mà Nghiệm Công Sứ dùng, và hai bên cố ý không bàn bạc với nhau
**And** given kết quả Nghiệm Công Sứ và Phúc Khảo Sứ đưa về, **Trưởng môn** (không phải Nghiệm Công Sứ/Phúc Khảo Sứ tự xử) nhận và định tuyến — Trưởng môn không dạy, không chấm, chỉ ghi nhận và định tuyến (R21)
**And** given Nghiệm Công Sứ và Phúc Khảo Sứ đã cân nhắc xong nhưng không khớp hoặc lưỡng lự không kết luận được (đúng nghĩa FR12a), Trưởng môn ghi "cờ bất đồng" và KHÔNG chặn người học ở bất kỳ nhánh bất thường nào
**And** given Nghiệm Công Sứ hoặc Phúc Khảo Sứ (subagent) lỗi/timeout — chưa từng trả lời được, không phải đã cân nhắc rồi lưỡng lự — hệ KHÔNG ghi nhầm thành "cờ bất đồng"; đây là sự cố kỹ thuật, xử lý bằng retry/báo lỗi riêng, không lẫn vào bản ghi bất đồng thật (tránh làm loãng dữ liệu bất đồng dùng để hiệu chuẩn sau này)
**And** given bằng chứng cân bằng giữa hai bên, kết quả nghiêng về hướng có lợi cho người học
**And** given cả Nghiệm Công Sứ và Phúc Khảo Sứ đều xác nhận qua khảo thí quyển, hệ tuyên bố **ĐỘT PHÁ QUYỂN** — đây là tiêu chí đạt của cả hệ (đặc tả §1.3), và là milestone MVP tự nó được định nghĩa xoay quanh ("đột phá quyển đầu tiên", `pham-vi-mvp.md`)
**And** given cờ bất đồng đã ghi, người học xem được nếu chủ động mở đạo tâm — nhưng hệ KHÔNG tự đẩy thông báo giữa lúc đang học
**And** given file `.pham-vi.json` (gác phạm vi đọc chéo vai) tồn tại nhưng không parse được (JSON hỏng, hoặc thiếu key `doc`/`ghi` bắt buộc — ví dụ do crash giữa lúc ghi), hệ xử lý GIỐNG HỆT trường hợp file thiếu (R26) — KHÔNG vai nào đọc được, fail an toàn; không được coi file hỏng là "không giới hạn" rồi cho đọc tự do

### Epic 5: Đạo tâm tự ghi

**Mục tiêu:** Người học có sổ đạo tâm ghi lại con đường học — không vai nào ghi hộ.
**FRs covered:** FR22
**Phụ thuộc:** Story 5.1 **tái dùng** nguyên cơ chế `disable-model-invocation` đã xây ở Story 1.2 (Bái sư — ghi nhập môn ký), áp dụng cho sổ đạo tâm — không xây lại từ đầu. Đúng thứ tự liệt kê 1→12 (Story 1.2 dispatch trước). Về thời điểm dựng thật, đặc tả §16 bước 7 nhóm `nhap-mon` · `dao-tam` · `bin/tang-kinh-cac.py` cùng một bước — hai story vẫn có thể triển khai gần nhau về thời gian, nhưng về mặt phụ thuộc kỹ thuật, Story 5.1 đứng sau Story 1.2, không phải ngược lại.

#### Story 5.1: Đạo tâm tự ghi

As a người học,
I want tự viết dòng đạo tâm bằng chính lời mình — không có vai AI nào soạn sẵn để tôi duyệt,
So that những gì tôi ghi lại là thật của tôi, không phải bản "tốt hơn về hình thức" do AI viết hộ.

**Acceptance Criteria:**

**Given** người học mở đạo tâm để ghi
**When** hệ hỗ trợ
**Then** hệ tái dùng cơ chế `disable-model-invocation` đã có từ Story 1.2 (không xây lại) — áp dụng cho skill/tool ghi đạo tâm
**And** given một vai AI (bất kỳ) thử ghi hộ hoặc soạn sẵn nội dung đạo tâm để người học duyệt, hành động đó bị chặn ở tầng cơ chế, không chỉ bị khuyên tránh
**And** given sổ đạo tâm đã có nhiều dòng, mọi dòng đều tra được tác giả là chính người học — không có bản ghi nào tác giả là AI
**And** given cơ chế này được kiểm tra, một ca thử "AI cố ghi hộ" phải thất bại rõ ràng, không âm thầm thành công

### Epic 6: Đối thoại đáng tin cậy

**Mục tiêu:** Ý định ngoài phạm vi được trả lời rõ "chưa hỗ trợ ở bản này"; không có phản hồi khen sáo rỗng/nịnh bợ ở bất kỳ đâu — điểm đóng MVP.
**FRs covered:** FR32, FR33

#### Story 6.1: Trả lời rõ khi chưa hỗ trợ

As a người học,
I want khi tôi hỏi về một tính năng chưa được dựng ở bản hiện tại, hệ nói thẳng "chưa hỗ trợ" thay vì im lặng hoặc đoán liều,
So that tôi không mất thời gian chờ một thứ sẽ không bao giờ xảy ra ở bản này.

**Acceptance Criteria:**

**Given** người học hỏi một ý định thuộc Vòng 3/4 (chưa dựng ở MVP) qua `/vd:chi-duong`
**When** hệ xử lý
**Then** hệ trả lời rõ "chưa hỗ trợ ở bản này" — không im lặng, không đoán liều một câu trả lời nghe hợp lý
**And** given ý định đó thuộc bất kỳ vai nào (không riêng Trưởng môn), quy tắc trả lời rõ áp dụng như nhau — cross-cutting
**And** given người học hỏi lại cùng ý định, câu trả lời "chưa hỗ trợ" nhất quán, không đổi giữa các lần hỏi

#### Story 6.2: Không khen sáo rỗng

As a người học,
I want hệ không bao giờ khen tôi kiểu xã giao/nịnh bợ,
So that mọi phản hồi tích cực tôi nhận được là thật, có căn cứ — không phải lời khen rỗng để tôi thấy dễ chịu.

**Acceptance Criteria:**

**Given** người học đưa một câu trả lời tầm thường (không đặc sắc)
**When** bất kỳ vai nào phản hồi (Dạy, Soát, Nền)
**Then** phản hồi không chứa lời khen mang tính xã giao/nịnh bợ tách khỏi tiến bộ thật
**And** given ca thử behavioral eval "đưa câu trả lời tầm thường", kết quả xác nhận không có sáo rỗng ở bất kỳ vai nào được thử
**And** given đây là story cuối MVP, toàn bộ eval suite (trigger + functional/behavioral) của các story trước được chạy lại trước khi coi MVP hoàn thành
**And** given bất kỳ hành động nào của hệ (dạy, chấm, ghi log), không request nào rời khỏi máy người dùng mang theo nội dung sách/câu trả lời/đạo tâm — NFR5 xác minh được bằng cách rà mọi lời gọi mạng ra ngoài trong story trước đó, không chỉ đọc tài liệu khẳng định suông

### Epic 7: Định hướng & khám phá kho

**Mục tiêu:** Người học được gợi ý học gì tiếp (kèm lối tự nhập, nói rõ nguồn thật/suy đoán) và gợi sách tiếp theo tối đa 3 lựa chọn kèm lý do.
**FRs covered:** FR13, FR14, FR15, FR30
**Ghi chú:** Cùng vai Trưởng môn, cùng thư mục `truong-mon/` với Epic 8/9 — tránh xung đột ghi tại chỗ khi viết story.

#### Story 7.1: Định hướng có lối tự nhập

As a người học đã xong ít nhất một mạch,
I want được gợi ý học gì tiếp kèm lối tự nhập lựa chọn khác — không bị ép theo một hướng duy nhất,
So that tôi luôn có tiếng nói cuối cùng về hành trình của mình.

**Acceptance Criteria:**

**Given** người học vừa hoàn thành một mạch/quyển
**When** Trưởng môn gợi ý học gì tiếp
**Then** gợi ý luôn kèm lối tự nhập — không ép người học theo một hướng duy nhất
**And** given mỗi gợi ý, hệ nói rõ nguồn: dựa trên dữ liệu thật (lịch sử học, hồ sơ) hay chỉ là suy đoán của model
**And** given một gợi ý là suy đoán (không có dữ liệu xác nhận), hệ bắt người học xác nhận thêm trước khi coi gợi ý đó là đã chấp nhận — không dừng ở một nhãn thụ động dễ bị lướt qua
**And** given người học tự nhập một hướng khác gợi ý, hệ tôn trọng lựa chọn đó, không lặp lại thuyết phục theo hướng cũ

#### Story 7.2: Quét kho gợi sách

As a người học muốn biết trong kho có gì phù hợp để học tiếp,
I want một công cụ quét kho trả về tối đa 3 lựa chọn kèm lý do — không phải cả danh sách dài,
So that tôi không bị choáng ngợp bởi quá nhiều lựa chọn.

**Acceptance Criteria:**

**Given** người học yêu cầu gợi sách tiếp theo
**When** `tra-tang-kinh-cac` quét kho
**Then** kết quả trả về tối đa 3 lựa chọn, mỗi lựa chọn kèm lý do — không phải toàn bộ danh sách kho
**And** given công cụ này là công cụ, không phải vai, nó không tự quyết định hộ người học — chỉ đưa danh sách rút gọn kèm lý do để người học tự chọn
**And** given kho có ít hơn 3 lựa chọn phù hợp, hệ trả đúng số lượng có, không bịa thêm cho đủ 3
**And** given kho không có lựa chọn nào phù hợp (0 kết quả), hệ nói rõ lý do (kho trống, hoặc không quyển nào khớp mạch/cảnh giới hiện tại) — không trả danh sách rỗng im lặng như thể lỗi

### Epic 8: Hạ sơn & phục mệnh

**Mục tiêu:** Người học mang kiến thức ra việc thật, báo cáo lại — nhận cả báo cáo thất bại, không chỉ thành công.
**FRs covered:** FR24
**Ghi chú:** Skill `ha-son`/`phuc-menh` — cùng vai Trưởng môn với Epic 7/9, cùng thư mục `truong-mon/`.

#### Story 8.1: Hạ sơn và phục mệnh

As a người học muốn thử áp dụng điều đã học vào việc thật,
I want nhận nhiệm vụ hạ sơn lịch luyện rồi báo cáo lại kết quả — kể cả khi thất bại,
So that thất bại thật cũng là bằng chứng học tập có giá trị, không phải thứ phải giấu đi.

**Acceptance Criteria:**

**Given** người học đã đột phá quyển và muốn thử việc thật (nhánh tuỳ chọn, không bắt buộc)
**When** hạ sơn được kích hoạt
**Then** Trưởng môn giao nhiệm vụ lịch luyện — đường bằng chứng mạnh hơn, không phải cửa bắt buộc
**And** given người học quay lại báo cáo (phục mệnh), hệ nhận cả báo cáo thất bại lẫn thành công — không chỉ đón nhận tin tốt
**And** given phục mệnh đã báo cáo, Trưởng môn dẫn người học qua đạo tâm để TỰ ghi dòng đạo tâm — Trưởng môn không ghi hộ, cùng ràng buộc với Story 5.1

### Epic 9: Bản đồ trực quan tiến độ

**Mục tiêu:** Tiến độ nhiều quyển/mạch xem được dạng bản đồ, dựng lại được từ artifact gốc.
**FRs covered:** FR31
**Ghi chú:** Cache `ban-do.json` nằm trong `truong-mon/` — cùng thư mục với Epic 7/8; Loại 3 (dẫn xuất, AD-5), không phải nguồn lưu trữ chính.

#### Story 9.1: Bản đồ trực quan tiến độ

As a người học có nhiều quyển/mạch đang học,
I want xem tiến độ dưới dạng bản đồ trực quan,
So that tôi thấy được toàn cảnh hành trình của mình, không chỉ từng mảnh rời rạc.

**Acceptance Criteria:**

**Given** người học có dữ liệu tiến độ ở nhiều quyển/mạch
**When** yêu cầu xem bản đồ
**Then** `ban-do.py` dựng bản đồ trực quan (Artifact) từ artifact gốc — không đọc/ghi vào đây như nguồn lưu trữ chính
**And** given file cache bản đồ bị xoá hoặc hỏng, hệ dựng lại được đúng từ artifact gốc — không mất dữ liệu tiến độ thật
**And** given tiến độ vừa cập nhật (đột phá chương/quyển/mạch mới), lần xem bản đồ tiếp theo phản ánh đúng, không hiển thị dữ liệu cũ đã lỗi thời

### Epic 10: Liền mạch học tập

**Mục tiêu:** Vào chương phụ thuộc, hệ nhắc lại nội dung liên quan; hết quyển, hệ thống hoá lại các ý trước khảo thí; quay lại chương dở ở phiên mới, hệ hỏi lại 1-2 câu; bỏ giữa chừng là tạm dừng hợp lệ.
**FRs covered:** FR25, FR26, FR27, FR28

#### Story 10.1: Nhắc lại và hệ thống hoá cuối quyển

As a người học đang học một quyển nhiều chương,
I want được nhắc lại nội dung liên quan trước chương phụ thuộc, và được hệ thống hoá lại toàn quyển trước khảo thí,
So that tôi không phải tự nhớ lại từ đầu, và có một cái nhìn tổng thể trước khi thi.

**Acceptance Criteria:**

**Given** một chương mới phụ thuộc chương trước
**When** Thư linh chuẩn bị dạy
**Then** hệ nhắc lại (không dạy lại từ đầu) nội dung liên quan đã học, trước khi dạy ý mới — tự tái sinh từ lớp giải nghĩa FR1, không đọc cache tóm lược của Epic 3
**And** given hết chương cuối một quyển, trước khi vào khảo thí, hệ hệ thống hoá lại các ý xuyên suốt các chương thành một cái nhìn toàn quyển — xây liên kết ý xuyên chương (4C/ID), không phải tóm tắt lại chữ

#### Story 10.2: Nối lại mạch cũ và xuất quan

As a người học quay lại một chương đang học dở sau một khoảng nghỉ,
I want được hỏi lại một hai câu để tự quyết định đi tiếp hay ôn lại — không bị coi như chưa từng nghỉ,
So that việc quay lại luôn mượt, dù tôi nghỉ một ngày hay một tháng.

**Acceptance Criteria:**

**Given** người học quay lại một chương đang dở ở phiên mới
**When** hệ nạp lại trạng thái
**Then** hệ hỏi lại một hai câu của chương trước để tự quyết định đi tiếp hay lùi lại ôn — không tự động coi như không có gì thay đổi, và không tính theo số ngày đã qua
**And** given người học bỏ giữa chừng, hệ giữ nguyên lộ đồ và giáo án khi dừng — đây là tạm dừng hợp lệ, không phải kết thúc
**And** given người học quay lại sau khi bỏ giữa chừng, hệ vào thẳng luồng nối lại mạch cũ — không dựng lộ đồ mới

### Epic 11: Đo cảnh giới có hiệu chuẩn

**Mục tiêu:** Tuyên bố cảnh giới cần ≥2 nguồn độc lập, đa mẫu đo độ tản mát, chỉ công bố khi κ đạt ngưỡng hiệu chuẩn; mọi nội dung bậc/cảnh giới khung là giả thuyết đang kiểm chứng; nghi thức đột phá cảnh giới kích hoạt ở đây.
**FRs covered:** FR16, FR17, FR18, FR19, FR20, FR21, FR23 (phần đột phá cảnh giới)
**Ghi chú vận hành:** Nếu hiệu chuẩn lại nhiều lần vẫn không đạt κ≥0,6, quy trình chẩn đoán "sai ở đâu" (đặc tả §11.2 — 5 nguồn: Model yếu/Harness yếu/Task mơ hồ/Grader sai/Nhiễu môi trường) là bước vận hành lúc hiệu chuẩn thật, không phải FR/story riêng — dev-agent triển khai story này cần đọc §11.2/§11.3 đặc tả, không chỉ mã hoá logic κ rồi coi xong.

#### Story 11.1: Đo cảnh giới có hiệu chuẩn

As a người học đã đột phá nhiều quyển trên cùng một mạch,
I want cảnh giới của tôi chỉ được công bố khi có đủ bằng chứng độc lập và đã hiệu chuẩn đáng tin,
So that tôi không bị gắn một nhãn cảnh giới sai lệch dựa trên phán đoán chủ quan chưa kiểm chứng.

**Acceptance Criteria:**

**Given** một mạch đã có bài nộp từ nhiều bí kíp khác nhau
**When** hệ định vị cảnh giới
**Then** tuyên bố "đang ở bậc X" chỉ đưa ra khi có ≥2 nguồn bằng chứng độc lập
**And** given định bậc chạy nhiều lần độc lập trên cùng bằng chứng, độ tản mát giữa các lần chạy dùng làm thước đo độ tin — gọi đúng tên "đa mẫu, đo độ tản mát", không gọi "self-consistency"
**And** given độ khớp hiệu chuẩn κ dưới ngưỡng 0,6, hệ KHÔNG công bố bậc — chỉ nêu dấu hiệu quan sát được, không gắn tên bậc
**And** given κ đúng bằng 0,6 (biên chính xác), hệ VẪN công bố bậc — chỉ κ THẤP HƠN 0,6 mới không công bố (so sánh `<`, không phải `<=`, đúng nguyên văn FR17 "dưới ngưỡng")
**And** given bất kỳ nội dung nào nói với người dùng về cảnh giới/bậc, nội dung đó được khung là một giả thuyết đang được kiểm chứng — không phải một phép đo đã được khoa học xác nhận
**And** given trước khi dùng để công bố cảnh giới, hệ đã hiệu chuẩn: so khớp với người chấm tay trên ≥20 mẫu (phủ nhiều mạch, nhiều mức), tính κ; κ<0,6 thì không công bố, phải hiệu chuẩn lại
**And** given báo cáo hiệu chuẩn được trình bày, báo cáo kèm % khớp thô song song với κ — không báo κ một mình
**And** given cảnh giới định vị cao hơn lần trước và có căn cứ, nghi thức đột phá cảnh giới kích hoạt — nghi thức thứ ba của FR23, chỉ dùng được từ đây trở đi
**And** **cần 20 mẫu chấm tay thật trước khi coi story này verify xong** — đây là việc người thật ngồi chấm, không phải code; chưa có, để dành lúc dev-agent triển khai thật (cùng kỷ luật với NFR7/NFR8 — không chỉ đọc tài liệu/viết logic κ là đủ)

### Epic 12: Chú Giải Sứ bồi sai lầm phổ biến

**Mục tiêu:** Sai lầm lặp lại cùng chỗ được bồi ghi chú vào lớp chú giải riêng — không sửa gốc, không mang chi tiết tình huống thật ra ngoài.
**FRs covered:** FR29

#### Story 12.1: Chú Giải Sứ bồi sai lầm phổ biến

As a người học lặp lại cùng một sai lầm ở cùng một chỗ qua nhiều lần học,
I want lỗi đó được bồi thành ghi chú cho người học sau — mà không ai nhìn thấy chi tiết tình huống riêng tư của tôi,
So that kinh nghiệm thật của tôi giúp ích cho người khác mà không lộ thông tin cá nhân.

**Acceptance Criteria:**

**Given** cùng một sai lầm lặp lại ở cùng một chỗ qua nhiều lần học
**When** Chú Giải Sứ phát hiện
**Then** hệ bồi một ghi chú vào lớp chú giải riêng của chương đó — không sửa bí kíp gốc
**And** given ghi chú được bồi, nội dung KHÔNG mang chi tiết tình huống thật của người học ra ngoài — không tên người, công ty, dự án cụ thể
**And** given Chú Giải Sứ là vai duy nhất có đầu ra rời khỏi máy người học, nó bị cấm đọc `ban-giao/`/`tinh-huong/` (AD-1) — tuyệt đối không được thấy dữ liệu riêng tư để không có gì rò rỉ dù vô tình
**And** given bí kíp đạt mức chia sẻ được, lớp chú giải bồi thêm đi kèm khi chia sẻ — bí kíp gốc (bất biến) tách biệt khỏi lớp chú giải (bồi dần theo thời gian)

---

**Trạng thái:** Epic 1-12 đã có story chi tiết (Given/When/Then). step-04 final validation đã chạy xong (FR Coverage, Architecture, Story Quality, Epic Structure, Dependency Validation — đều pass). `stepsCompleted: [1, 2, 3, 4]`. Sẵn sàng cho phát triển.
