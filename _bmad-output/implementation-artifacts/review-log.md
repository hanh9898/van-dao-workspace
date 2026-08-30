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
| `bin/setup-hooks.py` | `da-review` | 2026-08-31 · adversarial, edge-case-hunter · 5 finding, **vá 4, rút 1, hết** · hook dò `python3`·`python`·`py` bằng cách chạy thử `import sys` (`command -v` thấy cả stub Windows Store), không tìm được thì **chặn**; phép dò tách thành một nguồn dùng chung cho hook và cho lúc cài, nên `setup-hooks.py` báo ngay interpreter nào sẽ được gọi thay vì để lộ ở commit đầu; `--force` lưu `.bak` trước khi đè hook người khác; docstring ghi `--check` thắng `--force`. **Rút 1:** "tiếng Việt trong hook gây mojibake ở locale C" — sai, `sh` không transcode, verify bằng `LC_ALL=C LANG=C` thì chữ ra đúng; mojibake chỉ phụ thuộc codepage của terminal |

## Tài liệu

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `docs/VAN-DAO-harness-viet-skill.md` | `da-review` | 2026-08-31 · ba-problem-validity, ba-requirements-quality, ba-traceability, ba-solution-evaluation · 23 finding, vá hết |
| `docs/VAN-DAO-chuan-muc-skill.md` | `da-review` | 2026-08-31 · ba-requirements-quality, ba-traceability, skill-quality · 4 finding, **vá 4, hết** · góc 1 ghi mốc 5.000 token và pool 25.000; góc 3 nêu cả tên mục bản tiếng Anh và thêm phép kiểm vùng ghi (liệt kê tệp skill đọc/ghi rồi đối chiếu vai sở hữu — lấn việc lộ ở đường ghi chứ không ở câu chữ, và đó là cách AD-3 hỏng); bảng cuối tách *câu hỏi chấm* (phổ quát) khỏi *ngưỡng số* (riêng dự án), hết mâu thuẫn với góc 1 và góc 7 |
| `docs/naming-map.md` | `no` | Bảng ánh xạ danh pháp vi→en. Danh pháp đã chốt đủ để bắt đầu: tên sản phẩm **Wayfarer**, 16 thuật ngữ hệ, 20 danh từ kỹ thuật, 9 đường dẫn dữ liệu, 5 quy tắc đặt tên. Là **chuẩn để mọi lần đổi tên sau làm theo** nên thuộc phạm vi gate — sai ở đây thì sai ở hàng trăm định danh cùng lúc, và không sửa lại được vì sau đó không ai biết hai từ khác nhau từng là một. Mốc: **trước khi đổi tên đầu tiên theo bảng này** |
| `docs/VAN-DAO-dac-ta-v1.0.md` | `mien-tru` | Đặc tả sản phẩm, có trước quy tắc này, và không phải artifact harness — nó mô tả Vấn Đạo chứ không hướng dẫn cách xây |
| `docs/VAN-DAO-setup-du-an.md` | `mien-tru` | Có trước quy tắc. Ghi lại cách dựng môi trường, không tạo hành vi mới |
| `docs/VAN-DAO-trang-thai-du-an.md` | `mien-tru` | Có trước quy tắc. Bản ghi sự kiện, không phải chuẩn |

## Lens

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `_bmad/custom/lenses/skill-quality.md` | `da-review` | 2026-08-31 · đọc thật toàn văn · 4 finding, **vá 3, đóng 1, hết** · check 8 nêu mốc 5.000/pool 25.000; check 3 và 4 phân xử theo *cách lỗi lộ ra*; check 6 định nghĩa "packaged" theo đường tiếp cận thật của từng loại skill. **Đóng bằng quyết định:** viết tiếng Anh là cố ý — quy tắc "lens cùng ngôn ngữ với thứ nó soi", ghi ở đầu `bmad-review.toml`. Người dùng chốt 2026-08-31: hệ thống chuyển tiếng Anh toàn bộ, nên file này đã đúng đích; bốn lens BA thành nợ chuyển ngữ theo `docs/` |
| `_bmad/custom/lenses/ba-problem-validity.md` | `da-review` | 2026-08-31 · 2 finding, **vá 2, hết** · tách phép 4 thành hai (bên liên quan · ai xác nhận), stance sửa "năm" → "sáu"; phép ai-xác-nhận thêm lối thoát cho dự án một tác giả — qua khi tài liệu tự nhận là chưa có người xác nhận độc lập, vẫn là finding khi tài liệu im lặng. Khoá `nếu_sai_thì` → `neu_sai_thi`, hết là khoá JSON duy nhất mang dấu. **Một finding cũ bị rút**: nghi chồng lấn với `ba-requirements-quality` là sai — phép cuối soi khẳng định hiện trạng, lens kia soi yêu cầu |
| `_bmad/custom/lenses/ba-requirements-quality.md` | `da-review` | 2026-08-31 · 1 finding, **vá 1, hết** · thêm mục soi trước chín đặc tính: yêu cầu có định danh không. `req_id` từng giả định tài liệu đã đánh ID, mà không đặc tính nào bắt được lỗi thiếu ID — thứ chặn luôn `ba-traceability` phía sau |
| `_bmad/custom/lenses/ba-traceability.md` | `da-review` | 2026-08-31 · 2 finding, **vá 2, hết** · enum `huong` thêm giá trị `kế hoạch` cho phép lần thứ 3 (trước đó ba giá trị cho bốn phép, "việc mồ côi trong kế hoạch" không ánh xạ được); và con số mắt xích đã lần giờ ghi ở dòng tổng kết markdown thay vì đòi mảng finding rỗng đựng nó — không có con số thì "chạy và sạch" trông y hệt "không chạy" |
| `_bmad/custom/lenses/ba-solution-evaluation.md` | `da-review` | 2026-08-31 · 2 finding, **vá 2, hết** · thêm đoạn nói nó KHÔNG xét gì (lens duy nhất trong năm thiếu, nên chồng lấn không phân xử được); phép 3 thêm lối thoát cho dự án một người — qua khi tài liệu thay người ký bằng oracle không phụ thuộc phán đoán tác giả (test đỏ/xanh, mã thoát, số đo có ngưỡng). Trước đó phép này fail bằng định nghĩa mỗi lượt, che mất finding thật |

## Test

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `tests/test_work_state.py` | `mien-tru` | Test có **oracle riêng**: nó chạy và xanh/đỏ, nên kỳ vọng sai lộ ra khi code đúng mà test đỏ — đã xảy ra thật, hai test fail vì kỳ vọng sai chứ không phải script sai. Không viện dẫn vòng review của `bin/work-state.py`: vòng đó diễn ra **trước khi test tồn tại** |
| `tests/test_review_log.py` | `mien-tru` | Test có **oracle riêng** — fail ngay lần chạy đầu vì bug của chính nó (đọc nhầm bảng giải thích thành bảng artifact), và đó chính là oracle làm việc |

## Cấu hình

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `_bmad/custom/bmad-review.toml` | `da-review` | 2026-08-31 · đến hạn đúng lúc: miễn trừ của nó hứa "review cùng lượt với lens nó đăng ký" · 3 finding, **vá 1, hết hiệu lực 1, đóng 1, hết** · `when` của `ba-traceability` nới ra vì phép lần thứ 4 chỉ cần một mục ranh giới. Finding về `when` của `ba-solution-evaluation` hết hiệu lực sau khi lens có lối thoát. **Đóng bằng quyết định:** không có lens `applies_to = "code"` là cố ý — lens custom chỉ đáng viết khi có kiểu hỏng lens shipped không bắt, mà adversarial và edge-case-hunter đã tìm ra finding thật trên cả hai script; lý do ghi ở đầu file |
| `_bmad/custom/bmad-prd.toml` | `mien-tru` | Config cho `bmad-prd`, review cùng lượt khi dùng skill đó |
| `_bmad/custom/config.toml` | `mien-tru` | Config chung, review cùng lượt với thứ nó cấu hình |

## Chính cơ chế

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `_bmad-output/implementation-artifacts/review-log.md` | `mien-tru` | Chủ yếu là **bản ghi**. Phần quy tắc của nó (khi nào bắt buộc review, ba trạng thái nghĩa gì) sống ở `docs/VAN-DAO-chuan-muc-skill.md` §A.7 — review ở đó, không review hai lần cùng một luật |

---

## Vì sao có `no` mà không đỏ

Một quy tắc mới áp lên artifact có sẵn sẽ đỏ hàng loạt, và một phép kiểm đỏ kéo dài thì bị tắt — rủi ro này đã ghi trong `VAN-DAO-harness-viet-skill.md` §9. Nên test kiểm **sự có mặt**, không kiểm trạng thái. Nợ hiện ra trong sổ, không biến mất, nhưng cũng không chặn việc khác.

Tính đến 2026-08-31 sổ không còn mục `no` nào. Đừng đọc điều đó thành "`no` là trạng thái xấu phải tránh": artifact tiếp theo được thêm vào rất có thể vào sổ dưới dạng `no`, và đó là đúng cách dùng. Một cuốn sổ toàn `da-review` mãi mãi nghĩa là không ai thêm gì mới — hoặc có người đang ghi bừa.

## Cơ chế này đang ở tầng nào

Không phải tầng 2 hoàn toàn. `bin/setup-hooks.py` cài một hook `pre-commit` chạy test tự động, nên nó **không còn phụ thuộc ai nhớ gõ lệnh** — nhưng ba giới hạn phải nói thẳng:

- Hook sống trong `.git/hooks/`, **không được version control**. Máy khác clone về là không có, cho tới khi ai đó chạy `python bin/setup-hooks.py`.
- `git commit --no-verify` bỏ qua được. Đây là guardrail, không phải cổng an ninh.
- Chỉ chạy lúc commit. Thay đổi chưa commit vẫn nằm ngoài.
- Cần một interpreter Python chạy được. Hook tự dò `python3` · `python` · `py` và kiểm bằng cách chạy thử; không tìm được thì nó **chặn** chứ không im lặng cho qua — commit trông như đã qua test là đúng thứ cơ chế này chống.

Nên gọi đúng: **tầng 2.5**. Mạnh hơn "ai đó nhớ chạy", yếu hơn CI. Nó lên tầng 2 thật khi repo có remote — mục hoãn số 17.

Điều test **thật sự** bắt: một artifact mới được thêm mà không ai ghi vào sổ. Đó là ca đã xảy ra thật với `orca-help`.

Điều nó **không** bắt, và đã bỏ lọt thật: `_bmad/custom/bmad-review.toml` viện dẫn "review cùng lượt với lens nó đăng ký" mà không nêu đường dẫn trong backtick, nên phép kiểm ở lý do (c) không khớp được, và mục đó tụt lại phía sau năm lens đã `da-review` cho tới khi có người đọc bảng bằng mắt. §9 ở đầu sổ đã cảnh báo trước đúng chuyện này — cảnh báo không phải phép kiểm. Ai viết lý do (c) mà không đặt đường dẫn trong backtick thì đang tự bỏ ràng buộc của chính mình.
