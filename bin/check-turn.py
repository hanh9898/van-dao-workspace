#!/usr/bin/env python3
"""check-turn.py — hook `Stop`: chặn lượt kết thúc khi còn việc đo được là chưa xong.

Vì sao cần: `docs/agent-pitfalls.md` liệt kê 10 lớp lỗi đã xảy ra thật. Ba lớp nặng
nhất — dừng ở phần dễ, tự đổi sang cách dễ hơn, báo cáo xong khi chưa verify — đều
xảy ra ở khoảng trống giữa **việc được giao** và **việc agent tự định nghĩa lại trong
đầu**. Khoảng đó không đóng được bằng lời nhắc; nó chỉ đóng được khi có một bản khai
báo viết ra từ đầu để đối chiếu.

Ba phép kiểm, xếp theo mức cưỡng chế:

1. `.done-criteria.md` còn mục `- [ ]`  ->  CHẶN (exit 2)
   Bản khai báo đầu việc. Mục cố ý bỏ ghi `- [~]` kèm lý do, không tính là chưa xong.

2. File `.py` thay đổi mà test đỏ      ->  CHẶN (exit 2)
   Cùng luật với git pre-commit, nhưng bắn sớm hơn: lúc agent định dừng, chưa tới
   lúc commit.

3. Lượt dùng `grep ... | head` để kết luận "đã sạch"  ->  CẢNH BÁO (exit 0)
   Lỗi số 2 trong sổ, đã cắn hai lần. Không chặn vì dễ báo nhầm — `head` khi đang
   *xem* là hợp lệ, chỉ sai khi đang *kết luận*.

Chống lặp vô hạn: cùng một lý do chặn quá `TOI_DA` lần liên tiếp thì thôi chặn và nói
rõ. Một hook chặn mãi sẽ bị tắt, và lúc đó nó không bảo vệ được gì nữa.

Mã thoát: 0 cho đi tiếp (có thể kèm cảnh báo ở stderr) · 2 chặn, agent phải làm tiếp.
"""

import json
import subprocess
import sys
from pathlib import Path

for _l in (sys.stdout, sys.stderr):
    if hasattr(_l, "reconfigure"):
        _l.reconfigure(encoding="utf-8")

GOC = Path(__file__).resolve().parent.parent
TIEU_CHI = GOC / ".done-criteria.md"
TRANG_THAI = GOC / ".git" / "agent-turn-state.json"
TOI_DA = 2


def doc_trang_thai():
    try:
        return json.loads(TRANG_THAI.read_text(encoding="utf-8"))
    except Exception:
        return {}


def ghi_trang_thai(d):
    try:
        TRANG_THAI.write_text(json.dumps(d), encoding="utf-8")
    except OSError:
        pass


def chan(ly_do, thong_diep):
    """Chặn lượt — trừ khi đã chặn cùng lý do quá nhiều lần."""
    st = doc_trang_thai()
    n = st.get(ly_do, 0) + 1
    if n > TOI_DA:
        ghi_trang_thai({})
        print(f"[check-turn] đã chặn {TOI_DA} lần vì `{ly_do}` mà chưa xong — thôi chặn.\n"
              f"{thong_diep}\n"
              f"Nói thẳng với người dùng là việc này còn dở và vì sao.", file=sys.stderr)
        sys.exit(0)
    ghi_trang_thai({ly_do: n})
    print(thong_diep, file=sys.stderr)
    sys.exit(2)


def git(*a, cwd=GOC):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def kiem_tieu_chi():
    """Phép kiểm 1: bản khai báo đầu việc còn mục chưa xong."""
    if not TIEU_CHI.is_file():
        return
    dong = TIEU_CHI.read_text(encoding="utf-8", errors="replace").splitlines()
    chua = [d.strip() for d in dong if d.strip().startswith("- [ ]")]
    if not chua:
        return
    chan("tieu-chi-chua-xong",
         "[check-turn] `.done-criteria.md` còn mục chưa xong:\n  "
         + "\n  ".join(chua[:8])
         + "\n\nLàm nốt, hoặc nếu cố ý bỏ thì đổi `- [ ]` thành `- [~]` kèm lý do "
           "— bỏ có ghi lý do là quyết định, bỏ im lặng là quên.")


def kiem_test():
    """Phép kiểm 2: có sửa .py mà test đỏ."""
    r = git("status", "--porcelain")
    if r.returncode != 0:
        return
    py = [d for d in r.stdout.splitlines() if d.strip().endswith(".py")]
    if not py:
        return
    t = subprocess.run([sys.executable, "-m", "unittest", "discover", "tests", "-q"],
                       cwd=GOC, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if t.returncode == 0:
        return
    chan("test-do",
         "[check-turn] có thay đổi trong file .py và test ĐANG ĐỎ:\n"
         + (t.stderr or t.stdout)[-1200:]
         + "\n\nSửa cho xanh trước khi kết thúc lượt.")


def kiem_grep_bi_cat(transcript):
    """Phép kiểm 3: dùng `grep | head` để kết luận đã sạch. Chỉ cảnh báo."""
    if not transcript:
        return
    p = Path(transcript)
    if not p.is_file():
        return
    try:
        dong = p.read_text(encoding="utf-8", errors="replace").splitlines()[-400:]
    except OSError:
        return
    nghi = 0
    for d in dong:
        if "grep" in d and "| head" in d and "wc -l" not in d and "grep -c" not in d:
            nghi += 1
    if nghi:
        print(f"[check-turn] lượt này có {nghi} lệnh dạng `grep ... | head`. "
              "Nếu bất kỳ lệnh nào trong số đó được dùng để KẾT LUẬN 'đã sạch / không "
              "còn sót', kết luận đó không đứng được — `head` cắt mất phần sau. "
              "Đếm bằng `grep -c` hoặc `wc -l` rồi kết luận lại. "
              "(Lỗi số 2 trong docs/agent-pitfalls.md, đã cắn hai lần.)", file=sys.stderr)


def main():
    try:
        vao = json.load(sys.stdin)
    except Exception:
        vao = {}

    # Hook Stop có thể bắn lại sau khi chính nó chặn; không chặn chồng.
    if vao.get("stop_hook_active"):
        sys.exit(0)

    kiem_tieu_chi()
    kiem_test()
    kiem_grep_bi_cat(vao.get("transcript_path"))

    ghi_trang_thai({})   # lượt kết thúc sạch — xoá bộ đếm
    sys.exit(0)


if __name__ == "__main__":
    main()
