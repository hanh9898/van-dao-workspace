# Lens — Chất lượng từng yêu cầu (BABOK: Verify Requirements)

**Mục tiêu:** kiểm từng yêu cầu theo chín đặc tính chất lượng mà BABOK đặt ra cho requirements và designs. Đây là **verification** — "yêu cầu có đủ tốt để làm theo không" — không phải validation ("nó có giải đúng vấn đề không", việc của `ba-solution-evaluation`).

## Stance

Đọc như người sắp phải **thi hành** từng dòng và sẽ bị bắt lỗi nếu làm sai. Mỗi yêu cầu mơ hồ là một chỗ người thi hành phải đoán — và đoán khác nhau thì kết quả khác nhau.

Một yêu cầu không kiểm được pass/fail thì không phải yêu cầu, chỉ là mong muốn; mà mong muốn thì không ai fail được nó, nên nó luôn "đạt". Đó là finding, không phải chuyện nhỏ.

## Chín đặc tính — soi từng yêu cầu

| Đặc tính | Hỏng khi |
|---|---|
| **Atomic** | Một ID gộp nhiều yêu cầu rời — thi hành được nửa này mà không nửa kia |
| **Complete** | Thiếu một trong năm chỗ: **ai** (actor) · **được/không được làm gì** · **điều kiện & dữ liệu vào** · **cách kiểm pass/fail** · **cái gì ngoài phạm vi** |
| **Consistent** | Mâu thuẫn với một yêu cầu khác, hoặc dùng hai con số/hai thuật ngữ cho cùng một thứ |
| **Concise** | Lẫn lý lẽ, bối cảnh, hoặc cách làm vào chỗ đáng lẽ chỉ nêu điều phải đạt |
| **Feasible** | Đòi thứ chưa có đường thực hiện, hoặc phụ thuộc một tiền đề chưa được xác nhận |
| **Unambiguous** | Còn tính từ chưa ghim: nhanh · dễ · ổn định · đầy đủ · linh hoạt · phù hợp · tối ưu |
| **Testable** | Không nêu được cách quan sát từ **ngoài** để nói đạt hay không đạt |
| **Prioritized** | Không biết cái nào phải có, cái nào bỏ được khi hết thời gian |
| **Understandable** | Người thi hành phải tra thêm tài liệu khác mới hiểu được |

## Ba phép kiểm bổ sung, riêng cho tài liệu có ngưỡng số

1. **Ngưỡng có đơn vị và có công cụ đo.** "≤ N" mà không nói đo bằng gì thì hai người đo ra hai kết quả.
2. **Ngưỡng nhất quán khắp tài liệu.** Cùng một ràng buộc xuất hiện ở phần yêu cầu, phần kế hoạch, phần rủi ro — ba chỗ phải cùng một con số.
3. **Ngưỡng phân biệt được con số *của nền tảng* với con số *do dự án tự đặt*.** Lẫn hai loại này khiến người sau không biết được phép đổi cái nào.

## Kiểm ngược — tìm cách nó sai

Với mỗi yêu cầu, hỏi: *"tôi có thể thi hành đúng từng chữ mà vẫn không đạt được điều tài liệu muốn không?"* Nếu có, yêu cầu đó chưa ghim đủ.

## Đầu ra

Canonical fields, thêm:

- `req_id` — ID của yêu cầu (hoặc `N/A` nếu finding thuộc về cả nhóm)
- `dac_tinh` — đặc tính bị vi phạm, dùng đúng tên trong bảng trên

Báo cả những yêu cầu **thiếu hẳn** mà tài liệu ngầm giả định là có.
