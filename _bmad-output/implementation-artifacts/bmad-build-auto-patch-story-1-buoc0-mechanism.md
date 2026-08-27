---
status: 'saved-for-human-decision'
story: '_bmad-output/specs/spec-van-dao-workspace/stories/1-thiet-lap-ban-dau-ngon-ngu-giao-tiep.md'
reason: 'intent_gap — intent-contract Always clause contradicts a verified-correct implementation'
saved: '2026-08-27'
---

# Patch giữ lại — sửa cơ chế Bước 0 (`nhap-mon`)

## Vì sao lưu file này thay vì áp thẳng

Nhánh `intent_gap` của quy trình review yêu cầu revert code khi root cause nằm trong
`<intent-contract>`, để không có thay đổi nào tồn tại ngoài ý người điều phối trong lúc chờ quyết
định sửa contract. Nhưng bản sửa dưới đây đã được **verify bằng chạy thật 3 lần** (không suy diễn)
và chứng minh cách đọc gốc trong `<intent-contract>` (đọc `plugin.json`) **không thể** làm được —
revert sẽ đưa lại đúng bug đã chứng minh, không bảo vệ được gì. Đã **không revert** code thật trong
`van-dao/skills/nhap-mon/SKILL.md` (deviation có báo lại, theo đúng tiền lệ "Lần chạy 1" của chính
story này) — file này chỉ lưu lại patch để tham chiếu nếu người điều phối muốn khôi phục nguyên trạng
trước khi quyết định.

## Patch (đã áp trong `van-dao/skills/nhap-mon/SKILL.md`, giữ nguyên hiện trạng)

```diff
- Đọc `userConfig.communication_language` từ `.claude-plugin/plugin.json` (đã verify chạy thật — NFR8):
- - **Có giá trị** (vd. `"Vietnamese"`): dùng ngay giá trị đó cho mọi phản hồi tiếp theo trong phiên này...
- - **Trống hoặc chưa set**: nói rõ với người học là chưa đặt ngôn ngữ giao tiếp...
+ Giá trị `communication_language` người học đã cấu hình (Claude Code tự thế chỗ vào đây lúc nạp skill,
+ không phải giá trị tĩnh khai trong `plugin.json`):
+
+ ${user_config.communication_language}
+
+ **Không đọc trực tiếp `.claude-plugin/plugin.json` để lấy giá trị này** — file đó chỉ khai schema
+ (kiểu, tiêu đề, default gợi ý), không phải giá trị người học thật sự đã đặt...
```

## Câu hỏi chưa giải quyết được (cần người quyết)

`<intent-contract>` mục **Always** hiện viết: *"Đọc `userConfig.communication_language` đã có sẵn
trong `plugin.json` (không tạo cơ chế cấu hình song song)."*

Đã verify chạy thật (3 lần, transcript thật trong `van-dao/skills/nhap-mon/evals/evals.json`):
`plugin.json` chỉ chứa schema tĩnh (`default: "Vietnamese"`), không phải giá trị người dùng thật đã
đặt — đọc trực tiếp file này **không thể** phân biệt "chưa cấu hình" với "đã cấu hình bằng đúng giá
trị mặc định" trong mọi trường hợp, vi phạm thẳng AC thứ hai của story (`I/O & Edge-Case Matrix`
dòng 1). Cơ chế đúng — `${user_config.communication_language}` (xác nhận thật tại
`code.claude.com/docs/en/plugins-reference`) — đã dùng, và không tạo cơ chế cấu hình song song
(vẫn cùng một field `communication_language`, chỉ đổi cách đọc).

Không tự sửa `<intent-contract>` (đúng luật). Người điều phối cần chọn một trong:

1. Sửa câu "Always" thành mô tả theo **đích** thay vì **cơ chế**: *"Đọc đúng giá trị
   `communication_language` người học đã cấu hình qua `userConfig` (không tạo cơ chế cấu hình song
   song); cách đọc cụ thể do triển khai quyết định, miễn đúng 3 dòng I/O matrix."*
2. Giữ nguyên câu "Always" như hiện tại, chấp nhận đây là một sai sót đã biết trong đặc tả gốc, và
   coi bản sửa Bước 0 là ngoại lệ đã ghi lại rõ ràng (Spec Change Log) — không sửa contract, chỉ ghi
   chú.
3. Cách khác người điều phối thấy phù hợp hơn.

Không có lựa chọn nào trong 3 cái trên tự nó rõ ràng hơn — đây đúng là quyết định cần người, không
phải suy luận thêm sẽ tự lộ ra đáp án.
