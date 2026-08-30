# Sổ dấu vết review

Mọi artifact harness được version control phải **có mặt trong sổ này**. Có mặt, không phải đã review — ba trạng thái đều hợp lệ:

| Trạng thái | Nghĩa |
|---|---|
| `da-review` | Đã qua `bmad-review`; ghi ngày, lens, số finding, số đã vá |
| `no` | Trong phạm vi, chưa review, **có mốc quay lại** |
| `mien-tru` | **Không cần vòng review riêng**, kèm lý do. Ba lý do hợp lệ: (a) artifact có trước quy tắc và không phải chuẩn harness; (b) có **oracle riêng** đủ mạnh; (c) **review cùng lượt với `<đường dẫn>`** — nêu tường minh trong backtick, vì test kiểm ràng buộc đó |

> Lý do (c) không phải lời hứa suông: `test_review_log.py` kiểm rằng đường dẫn được nêu **có thật trong sổ**, và rằng khi nó chuyển sang `da-review` thì mục viện dẫn nó **cũng phải** `da-review`. Không nêu tường minh thì không có ràng buộc — và cũng không có bảo đảm nào.

**Có mặt trong sổ ≠ cần review.** Đây là hai câu hỏi khác nhau, và gộp chúng làm mọi thứ thành nợ. Sổ trả lời câu đầu cho *mọi* artifact — biết cái gì tồn tại là rẻ. Chỉ câu thứ hai mới là cổng, và nó phải hẹp: **chuẩn để người khác làm theo, hoặc code chạy trong luồng thật**. Test, config, và bản ghi không nằm trong đó.

Sổ tồn tại vì một lý do cụ thể: output trong luồng BMAD có cổng review sẵn (`bmad-build` step-04), output ngoài luồng thì không — nó phụ thuộc ai đó nhớ. Đã chứng minh thật: `work-state` được review vì người dùng bảo; `orca-help` thì không, cho tới khi có người để ý.

**Thứ được kiểm bằng máy là sự có mặt, không phải chất lượng.** `tests/test_review_log.py` kiểm mọi artifact git-tracked trong phạm vi đều có một dòng ở đây. Một dòng ghi bừa vẫn qua được test — nhưng nó nâng chi phí nói dối từ *im lặng* lên *phải chủ động viết ra một câu sai*. Đó đúng là ranh giới AD-10 đã chấp nhận cho eval.

**Phạm vi:** `.claude/skills/*/SKILL.md` · `bin/*.py` · `tests/*.py` · `docs/*.md` · `_bmad/custom/*.toml` · `_bmad/custom/lenses/*.md` · và **chính file này** — tất cả tính theo `git ls-files`, nên thứ bị gitignore (49 skill BMAD chẳng hạn) tự động nằm ngoài.

Phạm vi bản đầu bỏ sót ba nhóm, và cả ba đều là **thành phần của chính cơ chế này**: sổ, test kiểm sổ, và test nói chung. Một cơ chế tự loại mình ra khỏi tầm kiểm là chỗ nó mù nhất — lỗ đó do người dùng hỏi *"nó đã review chính nó chưa"* mới lộ ra.

---

## Skill

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `.claude/skills/work-state/SKILL.md` | `da-review` | 2026-08-31 · skill-quality, verification-gap, edge-case-hunter, adversarial · 16 finding, vá 15 · còn VG-1 (CI) chờ remote |
| `.claude/skills/orca-help/SKILL.md` | `da-review` | 2026-08-31 · skill-quality, edge-case-hunter, adversarial · 18 finding, vá 17 · còn SQ-3 (`orca open` chưa chạy thật) |

## Script

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `bin/work-state.py` | `da-review` | 2026-08-31 · cùng vòng với skill `work-state` · 19 unit test khoá lại từng lỗi |
| `bin/setup-hooks.py` | `da-review` | 2026-08-31 · adversarial, edge-case-hunter · 5 finding, **vá 1** · hook không còn gọi `python` trần: dò `python3` · `python` · `py` và kiểm bằng cách chạy thử `import sys`, vì `command -v` thấy cả stub Windows Store vốn chỉ mở cửa hàng. Không tìm được interpreter thì **chặn** chứ không cho qua kèm cảnh báo — cho qua tạo ra đúng thứ cơ chế này chống: commit trông như đã qua test. Verify thật cả hai nhánh: bình thường exit 0 test xanh; `env PATH=/nonexistent` exit 1 kèm thông báo và lối thoát `--no-verify`. Còn: `--force` ghi đè hook người khác không backup |

## Tài liệu

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `docs/VAN-DAO-harness-viet-skill.md` | `da-review` | 2026-08-31 · ba-problem-validity, ba-requirements-quality, ba-traceability, ba-solution-evaluation · 23 finding, vá hết |
| `docs/VAN-DAO-chuan-muc-skill.md` | `da-review` | 2026-08-31 · ba-requirements-quality, ba-traceability, skill-quality · 4 finding, **vá 1** · đã vá: góc 1 (Sống sót) giờ ghi mốc 5.000 token và mốc chung 25.000, bảng tóm sửa theo — trước đó bảo "xem mục nào rơi sau mốc" mà không nói mốc nào. Còn: bảng cuối xếp Phần B vào cột phổ quát trong khi góc 7 trỏ vào bảng A.0 và ngưỡng token, hai thứ chính tài liệu xếp vào cột riêng Vấn Đạo; góc 3 gọi tên hai mục bằng tiếng Việt nên không soi được skill đã chuyển tiếng Anh; không góc nào soi quyền ghi vùng dữ liệu |
| `docs/VAN-DAO-dac-ta-v1.0.md` | `mien-tru` | Đặc tả sản phẩm, có trước quy tắc này, và không phải artifact harness — nó mô tả Vấn Đạo chứ không hướng dẫn cách xây |
| `docs/VAN-DAO-setup-du-an.md` | `mien-tru` | Có trước quy tắc. Ghi lại cách dựng môi trường, không tạo hành vi mới |
| `docs/VAN-DAO-trang-thai-du-an.md` | `mien-tru` | Có trước quy tắc. Bản ghi sự kiện, không phải chuẩn |

## Lens

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `_bmad/custom/lenses/skill-quality.md` | `da-review` | 2026-08-31 · đọc thật toàn văn, không dựa hiệu quả đã đo · 4 finding, **vá 1** · đã vá: check 8 giờ nêu thẳng mốc 5.000 token / pool 25.000 và bắt người soi báo mốc rơi vào đâu — trước đó chỉ nói "a fixed token ceiling" nên không kiểm được. Còn: check 3 và 4 chồng lấn; check 6 đòi "actual packaged skill" — không xác định cho skill workspace không phải plugin; viết tiếng Anh trong bộ lens tiếng Việt |
| `_bmad/custom/lenses/ba-problem-validity.md` | `da-review` | 2026-08-31 · 2 finding riêng: stance nói "năm phép kiểm" nhưng phép 4 chứa hai câu hỏi độc lập (liệt kê bên liên quan · ai xác nhận vấn đề) — thực chất sáu; và `nếu_sai_thì` là khoá đầu ra duy nhất trong cả bộ có dấu tiếng Việt, cạnh `babok_area` tiếng Anh trong chính file này — bốn lens BA emit bốn kiểu đặt tên khoá khác nhau, khớp lẫn nhau không được. **Rút lại một finding cũ**: nghi chồng lấn với `ba-requirements-quality` là sai, đọc thật thì phép 5 soi khẳng định hiện trạng còn lens kia soi yêu cầu |
| `_bmad/custom/lenses/ba-requirements-quality.md` | `da-review` | 2026-08-31 · 1 finding riêng: `req_id` giả định tài liệu đã đánh ID, mà không đặc tính nào trong chín đặc tính bắt được lỗi "yêu cầu không có ID" — đúng thứ lens này nên bắt nhất |
| `_bmad/custom/lenses/ba-traceability.md` | `da-review` | 2026-08-31 · 2 finding riêng: đòi "nói rõ đã lần bao nhiêu mắt xích" khi kết quả rỗng, nhưng đầu ra là mảng finding — mảng rỗng không có chỗ đựng con số; và enum `huong` chỉ ba giá trị trong khi có bốn phép lần, "việc mồ côi trong kế hoạch" không ánh xạ rõ vào giá trị nào |
| `_bmad/custom/lenses/ba-solution-evaluation.md` | `da-review` | 2026-08-31 · 2 finding riêng: phép 3 (người xác nhận khác người làm) luôn fail trong workspace một người — sinh noise nền mỗi lần chạy, không có lối thoát; và là lens duy nhất trong năm không nói nó KHÔNG xét gì, nên chồng lấn không được phân xử |

## Test

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `tests/test_work_state.py` | `mien-tru` | Test có **oracle riêng**: nó chạy và xanh/đỏ, nên kỳ vọng sai lộ ra khi code đúng mà test đỏ — đã xảy ra thật, hai test fail vì kỳ vọng sai chứ không phải script sai. Không viện dẫn vòng review của `bin/work-state.py`: vòng đó diễn ra **trước khi test tồn tại** |
| `tests/test_review_log.py` | `mien-tru` | Test có **oracle riêng** — fail ngay lần chạy đầu vì bug của chính nó (đọc nhầm bảng giải thích thành bảng artifact), và đó chính là oracle làm việc |

## Cấu hình

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `_bmad/custom/bmad-review.toml` | `da-review` | 2026-08-31 · đến hạn đúng lúc: miễn trừ của nó hứa "review cùng lượt với lens nó đăng ký", và cả năm lens vừa chuyển `da-review` · 3 finding, vá 0 · `when` của `ba-traceability` đòi "ít nhất hai tầng" trong khi phép 4 của lens (đối chiếu ranh giới) chỉ cần một tầng — `when` chặt hơn chính lens nên chặn nhầm; `when` của `ba-solution-evaluation` không loại được tài liệu một tác giả, nơi phép "ai ký" luôn fail; không lens custom nào `applies_to = "code"` nên `bin/*.py` chỉ soi được bằng lens shipped |
| `_bmad/custom/bmad-prd.toml` | `mien-tru` | Config cho `bmad-prd`, review cùng lượt khi dùng skill đó |
| `_bmad/custom/config.toml` | `mien-tru` | Config chung, review cùng lượt với thứ nó cấu hình |

## Chính cơ chế

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `_bmad-output/implementation-artifacts/review-log.md` | `mien-tru` | Chủ yếu là **bản ghi**. Phần quy tắc của nó (khi nào bắt buộc review, ba trạng thái nghĩa gì) sống ở `docs/VAN-DAO-chuan-muc-skill.md` §A.7 — review ở đó, không review hai lần cùng một luật |

---

## Vì sao có `no` mà không đỏ

Một quy tắc mới áp lên artifact có sẵn sẽ đỏ hàng loạt, và một phép kiểm đỏ kéo dài thì bị tắt — rủi ro này đã ghi trong `VAN-DAO-harness-viet-skill.md` §9. Nên test kiểm **sự có mặt**, không kiểm trạng thái. Nợ hiện ra trong sổ, không biến mất, nhưng cũng không chặn việc khác.

## Cơ chế này đang ở tầng nào

Không phải tầng 2 hoàn toàn. `bin/setup-hooks.py` cài một hook `pre-commit` chạy test tự động, nên nó **không còn phụ thuộc ai nhớ gõ lệnh** — nhưng ba giới hạn phải nói thẳng:

- Hook sống trong `.git/hooks/`, **không được version control**. Máy khác clone về là không có, cho tới khi ai đó chạy `python bin/setup-hooks.py`.
- `git commit --no-verify` bỏ qua được. Đây là guardrail, không phải cổng an ninh.
- Chỉ chạy lúc commit. Thay đổi chưa commit vẫn nằm ngoài.

Nên gọi đúng: **tầng 2.5**. Mạnh hơn "ai đó nhớ chạy", yếu hơn CI. Nó lên tầng 2 thật khi repo có remote — mục hoãn số 17.

Điều test **thật sự** bắt: một artifact mới được thêm mà không ai ghi vào sổ. Đó là ca đã xảy ra thật với `orca-help`.
