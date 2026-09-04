# Vấn Đạo — Dựng dự án ban đầu

**Đi kèm:** `VAN-DAO-dac-ta-v1.0.md` (đặc tả). Bản này chỉ nói **dựng thế nào**, không nhắc lại thiết kế.

**Nguyên tắc xuyên suốt:** trước khi viết dòng nào, làm cho Claude **biết cách viết plugin** — không phải bằng cách bạn dán tài liệu vào chat, mà bằng cách đưa tài liệu vào chỗ nó tự nạp được khi cần.

---

# Phần 1 — Nạp kiến thức cho AI (làm trước tiên)

## 1.1 Cài plugin dạy viết plugin

```
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers-developing-for-claude-code@superpowers-marketplace
```

Cài xong **khởi động lại Claude Code**.

Nó mang hai skill: `working-with-claude-code` (42 file tài liệu chính thức từ docs.claude.com, có script tự cập nhật, nạp theo nhu cầu) và `developing-claude-code-plugins` (quy trình từng bước, hướng dẫn theo thành phần, mẫu chạy được, mẹo gỡ lỗi).

Vì sao đây là bước một: nó giải đúng bài **context rot**. Không có nó, mỗi phiên bạn phải dán tài liệu vào chat hoặc để Claude đoán từ trí nhớ — mà trí nhớ về API của một sản phẩm đang đổi nhanh là chỗ sai âm thầm nhất.

Cập nhật tài liệu định kỳ:

```
Cập nhật tài liệu Claude Code trong skill working-with-claude-code
```

## 1.2 Kiểm nó đã nạp được chưa

Trước khi tin, thử ba câu. Đây là **eval thủ công** cho chính bước setup:

| Hỏi | Đạt khi |
|---|---|
| "Subagent tươi khác fork ở chỗ nào về ngữ cảnh?" | Nêu đúng: subagent có system prompt riêng + skill khai trong `skills:`; fork nạp nguyên hội thoại agent cha |
| "Trường nào bắt buộc trong `.claude-plugin/plugin.json`?" | Trả lời từ tài liệu, không rào đón kiểu "thường thì…" |
| "Hook `SubagentStop` nhận gì và chặn được gì?" | Nêu cụ thể, không mô tả chung chung |

Câu nào trả lời mơ hồ hoặc bắt đầu bằng "tôi nghĩ là" → skill chưa nạp, hoặc mô tả chưa khớp. Sửa trước khi đi tiếp, đừng dựng lên nền đoán mò.

## 1.3 Đọc mã người khác — nguồn học nhanh nhất

Ba nguồn, xếp theo mức sẵn sàng:

| Nguồn | Ở đâu | Đọc để làm gì |
|---|---|---|
| **BMAD** — 48 skill | Đã có trên máy: `opms-thinking/.claude/skills/bmad-*` | Catalog CSV định tuyến · `customize.toml` · micro-file mỗi bước một file |
| **claude-plugins-official** | Marketplace đã đăng ký sẵn | Chuẩn mực viết SKILL.md |
| **claude-tutor** | `github.com/kirilxd/claude-tutor` | Thư mục `evals/` — trigger eval + functional eval |

Không đọc hết. Mở đúng thứ đang cần: viết catalog thì mở `bmad-help`, viết eval thì mở `claude-tutor/evals`.

---

# Phần 2 — Dựng khung dự án

## 2.1 Hai repo, không phải một

| Repo | Chứa | Vì sao tách |
|---|---|---|
| `van-dao` | Plugin: skills, agents, hooks, bin, tham-chieu | Đổi theo nhịp phát hành |
| *(không có repo bí kíp)* | — | **Kho sách là của riêng từng người**, nằm ở `~/.vandao/`, không bao giờ vào repo |

Đây là hệ quả của quyết định "mỗi người tự nhập PDF của mình": repo không chứa nội dung sách, nên không có bài toán bản quyền và không cần quy trình duyệt đóng góp.

## 2.2 Khung tối thiểu

```
van-dao/
  .claude-plugin/
    plugin.json
    marketplace.json
  README.md
  CHANGELOG.md
  skills/
  bin/
  tham-chieu/
  evals/
  .gitignore
```

`plugin.json`:

```json
{
  "name": "van-dao",
  "description": "Biến sách bạn đã có thành lộ trình học có người kèm. Thu bí kíp từ PDF/EPUB, dẫn học từng chương, khảo thí để đột phá cảnh giới.",
  "version": "0.1.0",
  "author": { "name": "hanhnt2", "email": "56497031+hanh9898@users.noreply.github.com" },
  "repository": "<URL repo>",
  "license": "MIT"
}
```

`.gitignore` — chặn ngay từ đầu, vì hai thứ này **không bao giờ được vào repo**:

```
# Kho sách và hồ sơ người học — nằm ở ~/.vandao/, không phải ở đây
*.pdf
*.epub
.vandao/

# BMAD dùng làm công cụ phát triển, không phát hành kèm
_bmad/
.claude/skills/
```

## 2.3 Git trước khi có mã

```
git init && git add . && git commit -m "chore: khung dự án"
git remote add origin <URL>
git push -u origin main
```

Làm ngay ở bước này, không để sau. Lý do thực tế: `opms-thinking` đã dựng xong, chạy được, rồi mắc ở đúng bước này — marketplace vẫn là thư mục local nên không ai ngoài bạn cài được. Đừng lặp lại.

---

# Phần 3 — Vòng lặp phát triển

## 3.1 Nạp đặc tả vào ngữ cảnh dự án

Tạo `CLAUDE.md` ở gốc repo:

```markdown
# Vấn Đạo

Đặc tả: @../docs/VAN-DAO-dac-ta-v1.0.md

## Luật khi làm việc trong repo này
- Đặc tả là nguồn sự thật. Lệch thì sửa đặc tả trước, sửa mã sau.
- Không thêm thành phần nào ngoài §12 mà chưa hỏi.
- Mọi script trong `bin/` phải kèm luật tương đương bằng lời trong `tham-chieu/`
  (§11.2) — để khi thiếu Python thì skill làm tay được.
- Mọi SKILL.md phải có "Xong khi" và "Khi nào skill này không giúp được" (§11.3).
```

Cú pháp `@đường-dẫn` nạp file vào ngữ cảnh mỗi phiên. Nhưng **đặc tả gần 1.000 dòng** — nạp cả vào mọi phiên là tự bóp ngân sách chú ý, đúng lỗi §5.9 cảnh báo.

Nên: chỉ `@` phần cần thường xuyên, hoặc để đặc tả trong `docs/` và trỏ đường dẫn để Claude tự mở khi cần. Nạp theo nhu cầu, không nạp sẵn.

## 3.2 Thứ tự dựng — theo §15 đặc tả

| # | Việc | Chặn bởi |
|---|---|---|
| 1 | `tham-chieu/bi-kip.schema.md` — hợp đồng hai cấp | — |
| 2 | `bin/kiem-bi-kip.py` — thực thi hợp đồng | 1 |
| 3 | `bin/giam-dinh.py` + `skills/thu-bi-kip` | 1, 2 |
| 4 | **Thu một quyển thật, 3 chương** | 3 |
| 5 | `skills/thu-linh` — F-1 → F2 | 1, 4 |
| 6 | `skills/nhap-mon` · `skills/dao-tam` | song song |
| 7 | **Tự bế quan quyển đó bằng plugin** | 4, 5, 6 |

Việc 1 không chặn bởi gì. Bước 4 là phép thử của bước 3, bước 7 là phép thử của bước 5.

## 3.3 Mỗi lần thêm một skill

```
1. Viết SKILL.md, có "Xong khi" và "Khi nào không giúp được"
2. claude plugin validate ./van-dao --strict
3. claude --plugin-dir ./van-dao   → thử gọi thật
4. Thêm 3 prompt vào evals/trigger/ — hai cái NÊN kích hoạt, một cái KHÔNG NÊN
5. Commit
```

Bước 4 là bước dễ bỏ nhất và đắt nhất khi bỏ. Xem 4.1.

## 3.4 Ba lỗi sẽ gặp

| Lỗi | Dấu hiệu | Chữa |
|---|---|---|
| **Trường lạ bị bỏ qua im lặng** | Gõ sai tên trường trong `plugin.json`, không báo gì | Luôn `validate --strict` |
| **Skill không tự kích hoạt** | Gọi tay thì chạy, tự nhiên nói thì không | Vấn đề ở `description`, không ở nội dung skill |
| **Hai skill mô tả na ná nhau** | Model gọi nhầm | Description tách theo **câu hỏi sở hữu**, không theo chủ đề |

---

# Phần 4 — Eval: dùng bộ khung có sẵn, đừng tự dựng

Anthropic đã phát hành khung eval cho skill trong **`skill-creator`**, và nó nằm sẵn trong `claude-plugins-official` mà bạn đã đăng ký. Không tự viết khung.

```
/plugin install skill-creator@claude-plugins-official
```

Gồm `run_eval.py` · `run_loop.py` · `improve_description.py` · `aggregate_benchmark.py`, ba agent chấm (`grader`, `analyzer`, `comparator`), và một eval viewer HTML.

**Hai loại eval, khác nhau hoàn toàn.**

## 4.1 Behavioral eval — `evals/evals.json`

Kiểm skill **chạy có ra đúng thứ không**. Đặt ở `skills/<tên>/evals/evals.json`:

```json
{
  "skill_name": "thu-bi-kip",
  "evals": [
    {
      "id": 1,
      "prompt": "thu quyển này vào tàng kinh các: evals/files/sach-mau.pdf",
      "expected_output": "Bí kíp có manifest hợp lệ, dừng chờ duyệt ở pha 2",
      "files": ["evals/files/sach-mau.pdf"],
      "expectations": [
        "Chạy giám định trước khi phân giải",
        "KHÔNG tự qua pha 3 khi chưa được duyệt",
        "kiem-bi-kip.py chạy và pass"
      ]
    }
  ]
}
```

Grader chấm **từ transcript** và trả `grading.json`: mỗi expectation có `passed` **và `evidence`** — trích đúng chỗ trong transcript làm căn cứ, cộng `execution_metrics` (số tool call, số bước, số lỗi).

**Hội tụ đáng chú ý:** `evidence` bắt buộc chính là R19 trong đặc tả. Anthropic áp luật *bằng chứng trước khẳng định* cho máy chấm skill; Vấn Đạo áp cho máy chấm người học. Cùng một bài toán, cùng một cách chặn.

**Evidence phải tự đủ, không phụ thuộc hệ điều hành.** Khi chạy thật skill để lấy `evidence` (cài plugin vào môi trường cô lập, gọi `claude -p`...):

- Trích **nguyên văn** transcript ngay trong `evals.json` — không chỉ trỏ đường dẫn tới file transcript nằm trong thư mục scratchpad của phiên làm việc. Thư mục đó tạm, gắn với một phiên cụ thể; người đọc sau (hay CI) sẽ không tìm thấy file đó nữa.
- Lệnh/script tái tạo lại eval phải chạy giống nhau trên cả Windows lẫn Linux (đúng CI đang chạy cả `ubuntu-latest` và `windows-latest`). Tránh cú pháp chỉ đúng một shell (vd. `VAR=val cmd` tiền tố biến môi trường kiểu POSIX); nêu cách làm tương đương trên cả hai, hoặc dùng cách trung lập (đặt biến môi trường bằng lệnh riêng trước, không viết dính vào một dòng lệnh shell cụ thể).

**Viết trước cho hai skill:**

| Skill | Expectation quan trọng nhất |
|---|---|
| `thu-bi-kip` | Không tự qua pha 3 khi chưa duyệt · giám định chạy trước · PDF quét ảnh thì dừng, không cố đi tiếp |
| `thu-linh` | Một ý mỗi lượt, kết bằng câu hỏi · không đáp câu nghiệm công đang treo (R5) · giáo án ghi ra file trước khi dạy (R4) |

## 4.2 Trigger eval — tối ưu `description`

Kiểm skill **có được gọi đúng lúc không**. 20 câu: **8–10 nên kích hoạt, 8–10 không nên**.

```json
[
  { "query": "thu quyển này vào tàng kinh các: ~/sach/babok.pdf", "should_trigger": true },
  { "query": "tôi có file PDF muốn đưa vào học", "should_trigger": true },
  { "query": "đọc file PDF này rồi tóm tắt cho tôi", "should_trigger": false }
]
```

Chạy mỗi câu **3 lần** để có tỉ lệ đáng tin. Chia **60% train / 40% test**, lặp tối đa 5 vòng, **chọn bản tốt nhất theo điểm test chứ không theo train** để tránh overfit. `improve_description.py` làm trọn vòng này.

**Hai luật viết ca âm:**

**Ca âm phải là near-miss.** Câu hiển nhiên không liên quan không kiểm được gì — *"viết hàm fibonacci"* làm ca âm cho skill PDF là quá dễ. Ca âm tốt **chia từ khoá với skill nhưng thật ra cần thứ khác**. Ví dụ trên: *"đọc file PDF này rồi tóm tắt"* có chữ PDF, có ý đọc sách, nhưng người dùng muốn tóm tắt chứ không muốn thu vào tàng kinh các.

**Description nên hơi "đẩy".** Claude có xu hướng **dưới-kích-hoạt** skill. Không chỉ nói skill làm gì, mà nói rõ *"dùng bất cứ khi nào người dùng nhắc tới X, kể cả khi họ không gọi tên nó ra"*.

## 4.3 Một rủi ro thật với `thu-linh`

Claude **chỉ tra skill cho việc nó không tự xử được dễ dàng**. Câu đơn giản một bước có thể **không kích hoạt skill nào** dù description khớp hoàn hảo, vì Claude làm thẳng được.

Câu *"dạy tôi chương 2 quyển này"* nghe rất dễ. Claude có thể trả lời thẳng mà **không gọi `thu-linh`** — người học nhận một bài giảng bình thường thay vì luồng F0→F2 có giáo án và nghiệm công.

Đây là chế độ hỏng **âm thầm**: không lỗi nào báo, chỉ là plugin không chạy. Vì vậy `/vd:be-quan` giữ là **lệnh** thì an toàn hơn để mặc tự kích hoạt. Trigger eval đo được điều này — nếu tỉ lệ kích hoạt của `thu-linh` thấp, đó là câu trả lời, không phải lỗi ngẫu nhiên.

## 4.4 Phương sai — chạy 3 lần, không phải 1

`aggregate_benchmark.py` cho **mean ± stddev** qua nhiều lần chạy. Analyzer soi hai thứ:

- **Assertion không phân biệt** — luôn pass bất kể có skill hay không
- **Eval phương sai cao** — có thể chập chờn

Cùng hình dạng với `truong-lao` k=3 trong đặc tả. Bạn đã dùng kỹ thuật này để định cảnh giới; giờ dùng lại để kiểm chính plugin.

## 4.5 Điều đáng giá nhất, và nó thuộc về đặc tả

Khái niệm **"assertion không phân biệt"** áp thẳng sang `tieu_chi_dat`.

Một tiêu chí mà **người chưa đọc chương cũng đạt được** thì nó không phân biệt được gì — và nó đang làm khảo thí *trông như* đang đo cái gì đó.

§10 hiệu chuẩn κ không bắt được lỗi này: κ chỉ đo người và model có chấm khớp nhau không. Hai bên có thể khớp hoàn hảo trên một tiêu chí vô dụng.

**Phép kiểm rẻ, thêm vào §10:** cho `nghiem-cong` chấm một bài viết bởi người **chưa đọc chương** — hoặc chính bạn cố tình viết một bài chỉ dựa vào hiểu biết chung. Đạt → tiêu chí đó vứt đi, viết lại.

Làm một lần cho mỗi bí kíp mới, ở pha 2. Rẻ hơn nhiều so với phát hiện sau ba quyển rằng cả bộ tiêu chí không đo gì.

## 4.6 Ba thứ vẫn phải chấm tay

| Kiểm | Cách |
|---|---|
| `nghiem-cong` chấm rộng tay | §10: 20 bài, người chấm trước, đo κ. **κ < 0,6 thì không công bố bậc** |
| Thư linh tuân luật một-ý-một-lượt | Đọc 5 transcript, đếm số ý mỗi lượt |
| Thư linh né câu đang treo (R5) | Cố tình hỏi thẳng câu nghiệm công, xem nó có đáp |

# Phần 5 — Việc đầu tiên hôm nay

1. Cài `superpowers-developing-for-claude-code` **và** `skill-creator`, khởi động lại
2. Chạy ba câu kiểm ở §1.2
3. `git init` + push repo rỗng có khung §2.2
4. Viết `tham-chieu/bi-kip.schema.md`

Ba việc đầu mất chưa tới một giờ. Việc thứ tư là thứ cả dự án đứng lên.

**Không làm ở giai đoạn này:** viết `truong-mon` · dựng hộp thư · dựng subagent · thêm bất kỳ thành phần nào ngoài bảy việc ở §3.2. Một người học, một quyển sách thì chưa có gì để định hướng và chưa có nhiều nguồn để định cảnh giới.
