# Sổ dấu vết review

Mọi artifact harness được version control phải **có mặt trong sổ này**. Có mặt, không phải đã review — ba trạng thái đều hợp lệ:

| Trạng thái | Nghĩa |
|---|---|
| `da-review` | Đã qua `bmad-review`; ghi ngày, lens, số finding, số đã vá |
| `no` | Trong phạm vi, chưa review, **có mốc quay lại** |
| `mien-tru` | Ngoài phạm vi, kèm lý do |

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
| `bin/setup-hooks.py` | `no` | Cài git hook `pre-commit` chạy test. Chính nó là artifact đầu tiên cơ chế này bắt được trên ca thật: viết xong, `git add`, test đỏ vì chưa có dòng nào ở đây. Mốc: cùng lượt với lần sửa hook tiếp theo |

## Tài liệu

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `docs/VAN-DAO-harness-viet-skill.md` | `da-review` | 2026-08-31 · ba-problem-validity, ba-requirements-quality, ba-traceability, ba-solution-evaluation · 23 finding, vá hết |
| `docs/VAN-DAO-chuan-muc-skill.md` | `no` | **Chưa review lần nào.** Nó là tài liệu định nghĩa chuẩn cho mọi skill sau, nên đáng review hơn phần lớn thứ khác. Mốc: **trước khi ai đó viết skill thứ tư dựa vào nó** |
| `docs/VAN-DAO-dac-ta-v1.0.md` | `mien-tru` | Đặc tả sản phẩm, có trước quy tắc này, và không phải artifact harness — nó mô tả Vấn Đạo chứ không hướng dẫn cách xây |
| `docs/VAN-DAO-setup-du-an.md` | `mien-tru` | Có trước quy tắc. Ghi lại cách dựng môi trường, không tạo hành vi mới |
| `docs/VAN-DAO-trang-thai-du-an.md` | `mien-tru` | Có trước quy tắc. Bản ghi sự kiện, không phải chuẩn |

## Lens

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `_bmad/custom/lenses/skill-quality.md` | `no` | Chưa review, nhưng **đã chứng minh giá trị qua 4 lần chạy thật** (story 1.3, 1.4, work-state, orca-help) — bằng chứng dùng được thay cho review lý thuyết. Mốc: khi sửa nó lần tới |
| `_bmad/custom/lenses/ba-problem-validity.md` | `no` | Mới, dùng đúng một lần. Mốc: sau lần dùng thứ hai — một lần chưa đủ biết nó bắt đúng hay bắt bừa |
| `_bmad/custom/lenses/ba-requirements-quality.md` | `no` | Mới, dùng đúng một lần. Mốc: sau lần dùng thứ hai — một lần chưa đủ biết nó bắt đúng hay bắt bừa |
| `_bmad/custom/lenses/ba-traceability.md` | `no` | Lens duy nhất bắt được lỗi mà tự chấm bỏ sót hoàn toàn (yêu cầu mồ côi), nên đáng review sớm hơn ba lens BA kia. Mốc: ngay sau lần dùng thứ hai |
| `_bmad/custom/lenses/ba-solution-evaluation.md` | `no` | Mới, dùng đúng một lần. Mốc: sau lần dùng thứ hai, cùng lượt với ba lens BA kia |

## Test

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `tests/test_work_state.py` | `no` | Viết SAU vòng review của `work-state`, nên chưa nằm trong vòng nào. Hai test của nó từng fail vì kỳ vọng sai chứ không phải script sai. Mốc: cùng lượt với lần sửa `work-state.py` tiếp theo |
| `tests/test_review_log.py` | `no` | Fail ngay lần chạy đầu vì bug của chính nó (đọc nhầm bảng giải thích thành bảng artifact). Mốc: **ngay sau khi cơ chế này chạy đủ một chu kỳ thật** — tức khi nó bắt được một artifact mới bị quên |

## Cấu hình

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `_bmad/custom/bmad-review.toml` | `no` | Đăng ký 6 lens; sai một dòng thì lens không chạy mà không gì báo. Mốc: khi thêm lens tiếp theo |
| `_bmad/custom/bmad-prd.toml` | `no` | Override `persistent_facts` cho `bmad-prd`, đã dùng thật một lần. Mốc: lần sửa tiếp theo |
| `_bmad/custom/config.toml` | `no` | Cấu hình chung. Mốc: lần sửa tiếp theo |

## Chính cơ chế

| Artifact | Trạng thái | Chi tiết |
|---|---|---|
| `_bmad-output/implementation-artifacts/review-log.md` | `no` | Sổ này định nghĩa phạm vi và ba trạng thái — nó là chuẩn, không chỉ là bản ghi. Mốc: **cùng lượt với `docs/VAN-DAO-chuan-muc-skill.md`**, vì §A.7 của tài liệu đó và sổ này là hai nửa của cùng một quy tắc; review một cái mà bỏ cái kia là bỏ nửa vấn đề |

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
