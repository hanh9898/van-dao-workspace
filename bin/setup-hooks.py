#!/usr/bin/env python3
"""setup-hooks.py — cài git hook chạy test trước mỗi commit.

Vì sao cần: repo này có test nhưng **không gì tự gọi chúng**. Không CI (chưa có
remote), không hook. Chúng chỉ chạy khi ai đó nhớ gõ lệnh — đúng thứ mà cơ chế
`review-log.md` được dựng ra để chống, và cơ chế đó lại mắc y hệt.

Hook `pre-commit` vá hai lỗ cùng lúc:

1. Test chạy tự động, không phụ thuộc trí nhớ.
2. `test_review_log.py` chỉ nhìn thấy artifact đã commit, nên có cửa sổ mù giữa lúc
   tạo file và lúc commit. Hook chạy đúng lúc `git commit` — khi file mới đang ở
   trong index — nên cửa sổ đó đóng lại.

Giới hạn phải biết, không giấu:

- Hook sống trong `.git/hooks/`, **không được version control**. Máy khác clone về
  là không có. Đó là lý do script này tồn tại: nó được commit, hook thì không.
- `git commit --no-verify` bỏ qua hook. Đây là guardrail, không phải cổng an ninh.
- Nó không thay CI. Khi repo có remote, CI mới là thứ không lách được.
- Hook tự dò `python3` · `python` · `py` và kiểm bằng cách chạy thử. Máy không có
  interpreter nào chạy được thì xem nhánh tương ứng trong `HOOK` bên dưới.

Dùng:
    python bin/setup-hooks.py            cài (không ghi đè hook đang có)
    python bin/setup-hooks.py --force    ghi đè hook đang có
    python bin/setup-hooks.py --check    chỉ báo trạng thái, không sửa gì

Mã thoát: 0 đã cài hoặc đã có sẵn · 1 không cài được · 2 (--check) chưa cài.
"""

import subprocess
import sys
from pathlib import Path

for _luong in (sys.stdout, sys.stderr):
    if hasattr(_luong, "reconfigure"):
        _luong.reconfigure(encoding="utf-8")

GOC = Path(__file__).resolve().parent.parent

# Dấu nhận biết hook do script này cài — để `--check` phân biệt được hook của ta
# với một hook khác người dùng tự viết, và để không ghi đè nhầm.
DAU = "# managed-by: bin/setup-hooks.py"

HOOK = f"""#!/bin/sh
{DAU}
#
# Chạy test trước khi commit. Bỏ qua bằng: git commit --no-verify
#
# Đặc biệt quan trọng: tests/test_review_log.py kiểm mọi artifact harness đều có
# mặt trong review-log.md. Chạy ở đây nghĩa là artifact mới bị bắt ngay lúc commit,
# thay vì lọt qua rồi phải có người để ý sau.

# Dò interpreter thay vì gọi `python` trần: trên phần lớn Linux chỉ có `python3`,
# và một hook gọi tên không tồn tại thì đỏ mọi lần, chặn MỌI commit. Kiểm bằng cách
# chạy thử chứ không chỉ `command -v` — Windows Store cài sẵn một `python3.exe` giả
# chỉ mở cửa hàng, `command -v` thấy nó nhưng nó không chạy được gì.
PY=""
for c in python3 python py; do
    if command -v "$c" >/dev/null 2>&1 && "$c" -c "import sys" >/dev/null 2>&1; then
        PY="$c"
        break
    fi
done

if [ -z "$PY" ]; then
    # Chặn, không cho qua. Không phải vì nghiêm khắc hơn: cho qua kèm cảnh báo tạo ra
    # đúng thứ cả cơ chế này được dựng để chống — một commit trông như đã qua test.
    # Ai không đọc dòng cảnh báo sẽ tin nhầm là xanh. Chặn thì lối thoát vẫn còn và
    # rẻ (--no-verify), chỉ khác ở chỗ nó trở thành một quyết định có ý thức.
    echo ""
    echo "pre-commit: không tìm thấy Python chạy được (đã thử python3, python, py)."
    echo "Repo này là Python — test không chạy được thì commit chưa được kiểm gì cả."
    echo ""
    echo "  Cài Python 3, hoặc:"
    echo "  git commit --no-verify   nếu bạn cố ý commit mà không chạy test"
    exit 1
fi

echo "pre-commit: chạy test bằng $PY..."
if ! "$PY" -m unittest discover tests -q; then
    echo ""
    echo "pre-commit: TEST ĐỎ — commit bị chặn."
    echo "Sửa rồi commit lại, hoặc dùng 'git commit --no-verify' nếu cố ý bỏ qua."
    exit 1
fi
echo "pre-commit: test xanh."
"""


def thu_muc_hook():
    """Hỏi git chỗ đặt hook thay vì giả định `.git/hooks` — worktree và
    `core.hooksPath` đều làm giả định đó sai."""
    r = subprocess.run(
        ["git", "rev-parse", "--git-path", "hooks"],
        cwd=GOC, capture_output=True, text=True, encoding="utf-8",
    )
    if r.returncode != 0:
        return None
    p = Path(r.stdout.strip())
    return p if p.is_absolute() else GOC / p


def main():
    chi_kiem = "--check" in sys.argv
    ghi_de = "--force" in sys.argv

    d = thu_muc_hook()
    if d is None:
        print("Không hỏi được git chỗ đặt hook — đây có phải một git repo không?")
        sys.exit(1)

    f = d / "pre-commit"

    if f.is_file():
        cua_ta = DAU in f.read_text(encoding="utf-8", errors="replace")
        if chi_kiem:
            print(f"Đã cài: {f}" if cua_ta
                  else f"Có hook pre-commit nhưng KHÔNG do script này cài: {f}")
            sys.exit(0 if cua_ta else 2)
        if not ghi_de:
            print(f"Đã có hook tại {f}"
                  + ("  (do script này cài — không cần làm gì)" if cua_ta
                     else "  (của người khác — dùng --force nếu muốn ghi đè)"))
            sys.exit(0 if cua_ta else 1)

    if chi_kiem:
        print(f"Chưa cài. Chạy: python bin/setup-hooks.py")
        sys.exit(2)

    d.mkdir(parents=True, exist_ok=True)
    # newline="\n": hook chạy qua sh, CRLF làm shebang hỏng trên Windows.
    f.write_text(HOOK, encoding="utf-8", newline="\n")
    try:
        f.chmod(0o755)
    except OSError:
        pass  # Windows không cần bit thực thi; git tự xử lý.

    print(f"Đã cài hook: {f}")
    print("Từ giờ mỗi `git commit` sẽ chạy test trước. Bỏ qua bằng --no-verify.")


if __name__ == "__main__":
    main()
