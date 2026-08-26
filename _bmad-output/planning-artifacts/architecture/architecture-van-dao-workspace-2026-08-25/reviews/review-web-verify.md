# Lens: Web-Verification — ARCHITECTURE-SPINE.md (Vấn Đạo)

Phạm vi: xác minh mọi quyết định công nghệ/phiên bản trong mục **Stack** (và các chỗ khác nhắc lại)
đã được web-research/reality-check thật tại **thời điểm chạy review này (2026-08-25)**, không phải
khẳng định từ training data. Không sửa `ARCHITECTURE-SPINE.md`.

Ghi chú kế thừa: `reviews/review-rubric.md` mục 4 đã tự flag rằng "đã chạy thật để xác minh" trong
spine là xác minh **tại thời điểm viết đặc tả**, chưa phải tái-xác-minh tại thời điểm chạy kiến trúc
này, và giao việc đó cho đúng lens này. Dưới đây là kết quả tái-xác-minh.

---

## 1. `book-to-skill` (virgiliojr94) — repo còn tồn tại, còn duy trì? — **PASS**

Gọi trực tiếp GitHub REST API (`api.github.com/repos/virgiliojr94/book-to-skill`) và tải thẳng
`raw.githubusercontent.com` (không qua tóm tắt gián tiếp) tại thời điểm 2026-08-25:

- Repo tồn tại thật, public, không archived, không disabled.
- `created_at: 2026-05-01`, `pushed_at: 2026-08-24` — commit gần nhất chỉ cách 1 ngày trước ngày chạy
  review này → đang được duy trì tích cực, không phải dự án chết.
- `stargazers_count: 25400`, `forks_count: 2633`, `open_issues_count: 23`, license MIT — khớp badge
  hiển thị trên README.
- Mô tả repo: *"Turn any technical book PDF into a Claude Code skill..."* — đúng phạm vi Vấn Đạo cần
  (PDF/EPUB → skill dùng trong Claude Code).

Nguồn: `https://api.github.com/repos/virgiliojr94/book-to-skill` (truy cập 2026-08-25);
`https://github.com/virgiliojr94/book-to-skill` (truy cập 2026-08-25).

## 2. Cú pháp cài đặt trong spine có khớp tài liệu hiện tại của repo? — **PASS**

Tải thẳng `docs/install.md` và `README.md` (raw, nhánh `master`) — không dựa vào cache/tóm tắt:

- `npx skills add virgiliojr94/book-to-skill` — khớp **nguyên văn** với lệnh "One command, any host"
  trong `docs/install.md` hiện tại.
- `pip install "book-to-skill[pdf,epub] @ git+https://github.com/virgiliojr94/book-to-skill.git"` —
  cú pháp git+https khớp đúng mẫu hiện tại của repo (`book-to-skill` "chưa có trên PyPI", tài liệu tự
  nói vậy). Extras: tài liệu hiện tại minh hoạ ví dụ `[pdf,epub,docx]` (3 extras); spine chỉ lấy
  `[pdf,epub]` (2 extras) — nhưng đây là lựa chọn đúng phạm vi (Vấn Đạo chỉ xử lý PDF/EPUB theo mô tả
  sản phẩm, không cần DOCX), không phải lỗi cú pháp hay bản cũ. Không flag.
- **Phân biệt "engine" (pip) vs "skill" (`npx skills add`)** mà spine dùng khớp đúng cảnh báo hiện tại
  của chính README: *"Two ways to use it, do not confuse them"* — pip chỉ cài CLI trích chữ, **không**
  đăng ký skill hội thoại; phải `npx skills add` / `git clone` mới có slash command. Đây là chi tiết
  khá đặc thù (không phải kiến thức phổ biến/training-data), việc spine nói đúng phân biệt này là bằng
  chứng khá mạnh rằng lần trước đó (đặc tả §6.2/§13.1) thật sự đã đọc tài liệu thật, không đoán.
- Đối chiếu thêm với đặc tả nguồn `docs/VAN-DAO-dac-ta-v1.0.md` dòng 974-983: đặc tả tự ghi rõ "Cả hai
  lệnh cài đặt trên đã chạy thật (`uv run --with` cho lớp engine, `npx skills add ... --host
  claude-code` cho lớp skill), không chỉ đọc tài liệu — và đã đọc trực tiếp `SKILL.md` cài về" — đúng
  tinh thần reality-check, không phải khẳng định suông.
- `pyproject.toml` hiện tại của `book-to-skill`: `requires-python = ">=3.9"` — không ép Python 3.11,
  nên lựa chọn Python 3.11 của Vấn Đạo (mục 3 dưới) không đến từ ràng buộc của dependency này.

Nguồn: `https://raw.githubusercontent.com/virgiliojr94/book-to-skill/master/docs/install.md`,
`.../README.md`, `.../pyproject.toml`, `.../SKILL.md` (tất cả truy cập 2026-08-25, nhánh `master`);
đối chiếu nội bộ `docs/VAN-DAO-dac-ta-v1.0.md` dòng 974-983, 1796.

## 3. Python 3.11 — còn là lựa chọn hợp lý cho dự án greenfield viết năm 2026? — **CONCERN**

- Tính tới 2026-08-25: Python 3.11 đang ở pha **security-fix-only** (đã hết bugfix), EOL
  **2027-10-31**; Python 3.10 EOL còn sớm hơn (**2026-10-31**, tức chỉ 2 tháng nữa). Python 3.12 vẫn
  còn security support tới 2028; Python 3.13 (phát hành 10/2024) và Python 3.14 (bản mới nhất) là các
  lựa chọn được khuyến nghị phổ biến hiện nay cho dự án mới.
- Dependency chính (`book-to-skill`) chỉ yêu cầu `>=3.9` — không có ràng buộc nào ép về 3.11.
- Đã grep toàn bộ `docs/VAN-DAO-dac-ta-v1.0.md` (nguồn duy nhất được spine dẫn cho Stack) tìm "3.11",
  "Python 3", "ubuntu-latest": **không có kết quả nào**. Đặc tả không hề nhắc tới phiên bản Python hay
  ma trận CI. Nghĩa là con số "Python 3.11" trong bảng Stack của spine **không truy được về một quyết
  định đã ghi ở đặc tả, cũng không thấy nguồn web nào được dẫn** — khác hẳn dòng `book-to-skill` ngay
  cạnh nó, vốn có nguồn "đã chạy thật để xác minh" rõ ràng.
- Đây khớp đúng dấu hiệu lens này cần bắt: một con số phiên bản trông hợp lý (3.11 từng là bản "mới
  nhất ổn định" phổ biến trong dữ liệu huấn luyện) nhưng **chưa có bằng chứng đã được đối chiếu với
  thực tế 2026** — không sai chức năng ngay lập tức (3.11 vẫn chạy được, vẫn nhận security patch tới
  10/2027), nhưng chọn một bản sắp hết vòng đời cho một plugin mới bắt đầu là rủi ro không cần thiết,
  và không có lý do tương thích nào biện minh cho nó ở đây.
- Khuyến nghị: architect nêu rõ lý do chọn 3.11 (nếu có, ví dụ ràng buộc CI runner nào đó chưa nói ra),
  hoặc nâng lên 3.12/3.13 cho phù hợp mặt bằng hiện tại — không chặn gate nhưng nên sửa trước khi đóng
  spine, vì Stack là bảng "quyết định công nghệ" — đúng đối tượng lens này rà.

Nguồn: tổng hợp từ tìm kiếm web ("Python end-of-life dates 2026", các bảng EOL từ endoflife.ai/
isitpatched.com/dev.to, truy cập 2026-08-25) đối chiếu lịch phát hành chính thức PSF; grep nội bộ
`docs/VAN-DAO-dac-ta-v1.0.md` (không có kết quả cho "3.11"/"Python 3"/CI matrix).

## 4. Claude Code — "subagent tươi" (fresh, không fork) còn là khái niệm hiện hành? — **PASS**

- Tài liệu hiện tại (`code.claude.com/docs/en/agent-sdk/subagents`, các nguồn tổng hợp 2026) xác nhận
  đúng phân biệt spine dùng: subagent (không phải fork) khởi tạo **ngữ cảnh mới hoàn toàn** — chỉ có
  system prompt của riêng nó, CLAUDE.md, và các skill preload; **không** thấy lịch sử hội thoại chính,
  không thấy các file phiên chính đã đọc. Ngược lại, fork kế thừa toàn bộ lịch sử. Đây khớp chính xác
  câu spine dùng: "subagent tươi — ngữ cảnh mới mỗi lần gọi, không bao giờ fork phiên đang chạy."
- Bằng chứng trực tiếp mạnh hơn cả tài liệu web: chính công cụ `Agent` đang sẵn có trong phiên chạy
  lens này (Claude Code, 2026-08-25) mô tả nguyên văn: *"`\"fork\"` forks yourself... any other type —
  or omitting it — starts a fresh agent"* — tức phân biệt fresh-subagent-vs-fork là tính năng đang
  chạy thật ngay lúc review này, không phải suy diễn từ training data.

Nguồn: `https://code.claude.com/docs/en/agent-sdk/subagents` (qua tìm kiếm, truy cập 2026-08-25); quan
sát trực tiếp schema công cụ `Agent` trong phiên Claude Code hiện tại.

## 5. Claude Code Hook — `SessionStart`/`SubagentStop`/`Stop` còn là event hiện hành? — **PASS**

Tải trực tiếp `https://code.claude.com/docs/en/hooks` (truy cập 2026-08-25): tài liệu liệt kê đầy đủ
danh sách hook event hiện hành (32 event, gồm cả nhóm mới hơn như `SubagentStart`, `PostToolBatch`,
`TeammateIdle`...). Cả ba event spine dùng đều có mặt, đúng vai trò:

- `SessionStart` — "Khi phiên bắt đầu hoặc resume" — khớp cách spine dùng cho `nap-ho-so.sh`.
- `SubagentStop` — "Khi một subagent kết thúc" — khớp cách spine dùng cho `kiem-thu.sh`.
- `Stop` — "Khi Claude kết thúc trả lời" — khớp cách spine dùng cho `ghi-nhat-ky.sh`.

Không có dấu hiệu đổi tên/khai tử với 3 event này. Không cần sửa gì ở AD-7 hay bảng cây thư mục
`hooks/`.

Nguồn: `https://code.claude.com/docs/en/hooks` (truy cập 2026-08-25).

## 6. Claude Code Artifact — còn là tính năng hiện hành? — **PASS**

Tìm kiếm xác nhận trang tài liệu chính thức `code.claude.com/docs/en/artifacts` đang tồn tại
(2026-08-25): Artifact trong Claude Code là trang web tương tác, publish từ phiên CLI/desktop lên URL
riêng tư trên claude.ai, mặc định private, có thể chia sẻ trong tổ chức, giới hạn 16 MiB, chạy dưới
CSP nghiêm ngặt (đúng những gì mô tả công cụ `Artifact` sẵn có trong chính phiên đang chạy lens này
cũng nói). Việc spine để FR31 (bản đồ trực quan qua Artifact) ở mục Deferred, không phải Stack, là hợp
lý — không cần xác minh sâu hơn cho MVP hiện tại vì chưa dùng tới ở vòng này, nhưng khái niệm nền tảng
là có thật và đang hoạt động, không phải khái niệm đã lỗi thời hay bị nhầm với claude.ai thường.

Nguồn: `https://code.claude.com/docs/en/artifacts` (qua tìm kiếm + xác nhận tồn tại, truy cập
2026-08-25); quan sát trực tiếp công cụ `Artifact` sẵn có trong phiên Claude Code hiện tại.

---

## Verdict tổng

**CONCERNS** — không có FAIL chặn gate. 5/6 mục PASS với bằng chứng web trực tiếp (API call, raw file
fetch, tài liệu chính thức, cộng thêm quan sát trực tiếp tool đang chạy — không dựa vào training data).
1 mục CONCERN thật: **Python 3.11** trong bảng Stack không có nguồn (không có trong đặc tả, không có
citation web nào trong spine) và là một lựa chọn phiên bản đã bắt đầu lỗi thời cho một dự án greenfield
2026 (security-only, EOL 2027-10-31; mặt bằng khuyến nghị hiện nay là 3.12/3.13). Khuyến nghị: architect
bổ sung lý do chọn 3.11 (nếu có ràng buộc thật) hoặc nâng version trước khi đóng spine — không chặn các
lens khác tiếp tục chạy song song.
