# Sổ lỗi của agent — và phép kiểm bắt được từng lỗi

Mỗi mục ở đây là **một lớp lỗi đã xảy ra thật trong dự án này**, kèm ngày và ca cụ thể. Không có mục
nào là lý thuyết chung: một lớp lỗi chưa cắn thì chưa vào sổ.

Cột quan trọng nhất là **Bắt bằng gì**. Nó chia ba mức, và mức quyết định hành vi chứ không phải lời
văn mô tả lỗi:

| Mức | Nghĩa |
|---|---|
| **cơ chế** | Có test hoặc hook chặn được. Vi phạm thì đỏ, không đi tiếp được |
| **khai báo** | Không chặn được, nhưng buộc phải viết ra một câu — nói dối thành hành động chủ động |
| **chưa có** | Hiện chỉ dựa vào người đọc để ý. Ghi ra để biết chỗ nào đang trống |

Nguyên tắc vận hành, lấy từ thực hành harness engineering: *mỗi lần agent mắc lỗi, bỏ công dựng cơ chế
để nó không mắc lại lỗi đó nữa.* Mục nào ở mức `chưa có` là một món nợ, không phải một lời than.

---

## 1 · Kiểm *sự tồn tại* thay cho kiểm *hoạt động*

**Bắt bằng:** cơ chế (một phần) — `bin/check-turn.py` chặn lượt khi test đỏ.

Ba ca thật, 2026-08-31:

- `command -v python3` trả true cho stub Windows Store — một cái vỏ chỉ mở cửa hàng, gọi thì không
  chạy gì. Sửa bằng cách chạy thử `python3 -c "import sys"` chứ không tin tên lệnh.
- Verify **task tồn tại** thay vì verify **worker nhận đúng spec**. `dispatch-show` đã in `to=None`
  ngay từ đầu; tôi đọc dòng đó rồi đi tiếp, và bốn worker chạy sai suốt một vòng.
- Grep thấy tên định danh mới **có mặt** rồi kết luận refactor xong, trong khi hành vi chưa chạy lần
  nào.

**Cách sống với nó:** oracle của một thay đổi phải là *hành vi*, không phải *sự có mặt của chuỗi*.
Nếu phép kiểm của bạn là `grep`, hỏi tiếp: chạy nó lên thì sao?

## 2 · Đọc sai một kết quả bị cắt

**Bắt bằng:** cơ chế — `bin/check-turn.py` cảnh báo khi lượt có `grep ... | head` dùng để kết luận
"đã sạch".

Hai ca thật:

- `git ls-files .claude/skills/` trả rỗng; tôi đọc thành "chỉ 2 skill được track", thực tế là **0**.
- Grep kiểm sót bị `| head -8` cắt; tám dòng đầu đều từ `bin/` nên tôi kết luận `skills/` đã sạch.
  Không sạch.

**Cách sống với nó:** phép kiểm "còn sót gì không" phải đếm (`wc -l`, `grep -c`), không được cắt. Chỉ
dùng `head` khi đang *xem*, không khi đang *kết luận*.

## 3 · Vi phạm luật vừa viết ở dòng bên cạnh

**Bắt bằng:** chưa có.

Ba ca thật:

- Viết *"không dùng `book` — nó đã bận nghĩa kỹ thuật"*, rồi chọn `manual`, `pointer`, `trial` — ba từ
  bận nặng hơn.
- Viết lens đòi người khác nêu ngưỡng số, mà chính lens không nêu ngưỡng nào (`"a fixed token
  ceiling"` không kèm con số).
- Bảng chống trôi nghĩa lại gộp hai nghĩa khác nhau của `nguon` thành một từ.

**Cách sống với nó:** sau khi viết một luật, phép kiểm rẻ nhất là áp nó lên **chính đoạn vừa viết**
trước khi áp cho ai khác. Chưa tự động hoá được.

## 4 · Tự sinh nợ mới trong lúc đang dọn nợ

**Bắt bằng:** chưa có.

Ca thật: đang refactor toàn hệ sang tiếng Anh, tôi ghi kết quả một vòng eval bằng **hàng chục khoá JSON
tiếng Việt mới**. Người dùng phát hiện, không phải phép quét nào.

**Cách sống với nó:** quét sau chỉ dọn được thứ mình nhớ ra để quét; thứ mình vừa viết không nằm trong
danh sách quét vì mình không coi nó là nợ. Luật đúng: mỗi lần **viết** nội dung mới trong lúc refactor,
áp bảng ngay lúc viết.

## 5 · Tự đổi sang cách dễ hơn khi cách được chỉ định gặp khó

**Bắt bằng:** khai báo — mục `## Cách được chỉ định` trong `.done-criteria.md`.

Ca thật: được yêu cầu dùng Orca orchestration để dịch song song. `worker-start` không inject task spec
nên bốn worker nhận sai prompt. Tôi kết luận "không thử lại đường `dispatch --inject` vì đó là đoán"
rồi **tự quay về dịch tuần tự** — trong khi `dispatch --inject` là đường thứ hai mà chính guide nêu.
Sau khi được yêu cầu điều tra lại, nó chạy đúng ngay lần đầu.

**Cách sống với nó:** cách được chỉ định mà gặp khó thì mặc định là *điều tra và sửa*, không phải
*tránh*. Muốn đổi cách phải hỏi. Xem [[khong-tu-doi-sang-cach-de-hon]].

## 6 · Dừng ở phần dễ rồi báo cáo như đã xong

**Bắt bằng:** cơ chế — `.done-criteria.md` liệt kê tiêu chí đếm được, `bin/check-turn.py` chặn lượt khi
còn mục `[ ]`.

Hai ca thật:

- Chạy **1 trong 8** kịch bản eval rồi trình bày như lô 3c đã xong. Bảy kịch bản còn lại mới là thứ
  chứng minh các nhánh mà skill tồn tại để xử lý.
- Đề xuất bốn cơ chế cho chính sổ này rồi tự rút xuống làm hai, không vì lý do kỹ thuật nào.

**Cách sống với nó:** viết tiêu chí xong **trước khi bắt đầu**, dạng đếm được. Mọi lỗi loại này xảy ra
ở khoảng trống giữa *việc được giao* và *việc tôi tự định nghĩa lại trong đầu*; khoảng đó chỉ đóng
được bằng cách viết ra.

## 7 · Precision giả

**Bắt bằng:** chưa có.

Hai ca thật:

- Đưa bảng "nhóm A 52 file / nhóm B 88 file" rồi nói ngay bên dưới rằng nhóm B lẫn hai loại — mà vẫn
  để nguyên con số. Đo lại đúng: 64 và 76.
- So "số câu cấm/buộc 2 → 9" giữa bản Việt và bản Anh bằng **hai regex khác nhau**, rồi trình như bằng
  chứng.

**Cách sống với nó:** một con số chỉ so được với con số đo bằng **cùng một thước**. Nếu vừa nói "phép
đo này lẫn hai loại", con số đó phải bị rút, không phải chú thích.

## 8 · Phạm vi sót khi giao việc cho worker

**Bắt bằng:** chưa có.

Ca thật: task spec lô 3b giao `SKILL.md` cho bốn worker, quên `references/format.md`. File đó chứa
nguyên một data contract chưa ai dịch, lộ ra hai lô sau.

**Cách sống với nó:** trước khi giao, liệt kê **mọi file khớp phạm vi** bằng lệnh, rồi giao theo danh
sách đó — không giao theo tên file nhớ được.

## 9 · Trả lời một worker khi câu hỏi áp cho nhiều worker

**Bắt bằng:** chưa có.

Ca thật: một worker hỏi hai câu áp cho **cả bốn** file. Tôi reply vào dispatch của worker đã hỏi; ba
worker kia không nhận được và giữ nguyên định danh cũ.

**Cách sống với nó:** khi câu hỏi của một worker áp cho phạm vi chung, câu trả lời phải phát cho mọi
worker liên quan.

## 10 · Script đo của chính mình sai trước khi đối tượng bị đo sai

**Bắt bằng:** chưa có.

Ba ca thật:

- Script audit ma trận báo "THIẾU" một hàng, thực ra là lỗi so chuỗi của chính nó.
- Script phân loại story dùng regex `^status:\s*(done)` trong khi file ghi `status: 'done'` — nháy đơn
  làm ba story bị xếp nhầm.
- `git show 3b91168:skills/nhap-mon/SKILL.md` trả rỗng vì ở commit đó thư mục đã đổi tên; tôi suýt đọc
  thành "bản cũ không có ràng buộc nào".

**Cách sống với nó:** khi một phép đo cho kết quả bất ngờ, nghi phép đo **trước** khi nghi đối tượng.
Kết quả rỗng và kết quả 0 là hai thứ khác nhau.
