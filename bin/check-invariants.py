#!/usr/bin/env python3
"""check-invariants.py — đếm bất biến cấu trúc của một tài liệu markdown.

Vì sao cần: dịch một tài liệu đặc tả không có oracle cho "đúng nghĩa không". Nhưng
phần lớn thiệt hại thật của một bản dịch không nằm ở nghĩa — nó nằm ở chỗ **mất mát
âm thầm**: rơi một hàng bảng, mất một mã ràng buộc, gộp hai mục thành một. Những thứ
đó đếm được.

Cách dùng:

    python bin/check-invariants.py docs/spec.md                 in số đo
    python bin/check-invariants.py docs/spec.md --json          máy đọc
    python bin/check-invariants.py docs/spec.md --so <file>     so với bản đã lưu
    python bin/check-invariants.py docs/spec.md --luu <file>    lưu làm mốc

Quy trình dịch:

    1. --luu mốc.json           (trước khi đổi bất cứ chữ nào)
    2. ...dịch một lô...
    3. --so mốc.json            (mọi số phải khớp)

Mã thoát: 0 khớp hoặc chỉ in số · 1 lệch · 2 không đọc được file.

Giới hạn phải biết: nó **không** kiểm nghĩa. Một bản dịch sai hoàn toàn mà giữ nguyên
cấu trúc vẫn qua. Nó chỉ bắt mất mát — đó là thứ nó được dựng cho, và là thứ người
đọc lại bản dịch dễ bỏ sót nhất.
"""

import json
import re
import sys
from pathlib import Path

for _luong in (sys.stdout, sys.stderr):
    if hasattr(_luong, "reconfigure"):
        _luong.reconfigure(encoding="utf-8")


def do(noi_dung):
    """Trả về dict số đo. Khối mã bị loại khỏi phần đếm heading và bảng — bên trong
    khối mã, `# gì đó` là comment chứ không phải tiêu đề."""
    dong = noi_dung.splitlines()

    trong_ma = False
    ngoai_ma = []
    so_khoi_ma = 0
    for d in dong:
        if d.lstrip().startswith("```"):
            so_khoi_ma += 1
            trong_ma = not trong_ma
            continue
        if not trong_ma:
            ngoai_ma.append(d)

    sach = "\n".join(ngoai_ma)

    # Bảng: đếm dòng phân cách `|---|`, mỗi bảng có đúng một. Kèm số cột để bắt
    # trường hợp bảng còn đó nhưng mất một cột.
    cot_bang = [len([c for c in d.split("|") if c.strip()])
                for d in ngoai_ma if re.match(r"^\s*\|[\s:|-]*-[\s:|-]*\|\s*$", d)]

    return {
        "h1": sum(1 for d in ngoai_ma if d.startswith("# ")),
        "h2": sum(1 for d in ngoai_ma if d.startswith("## ")),
        "h3": sum(1 for d in ngoai_ma if d.startswith("### ")),
        "bang": len(cot_bang),
        "cot_bang": cot_bang,
        # Hàng bảng: bắt "bảng còn đó nhưng thiếu hàng" — kiểu mất mát êm nhất.
        "hang_bang": sum(1 for d in ngoai_ma
                         if d.lstrip().startswith("|") and not re.match(r"^\s*\|[\s:|-]*-[\s:|-]*\|\s*$", d)),
        "khoi_ma": so_khoi_ma // 2,
        # Mã định danh phải sống sót nguyên vẹn qua bản dịch.
        "ma_r": sorted(set(re.findall(r"\bR\d+\b", sach))),
        "ma_ad": sorted(set(re.findall(r"\bAD-\d+\b", sach))),
        "ma_fr_nfr": sorted(set(re.findall(r"\b(?:FR|NFR)\d+\b", sach))),
        "tham_chieu_muc": sorted(set(re.findall(r"§\d+(?:\.\d+)*", sach))),
    }


def so_sanh(a, b):
    """Trả danh sách khác biệt. a = mốc, b = hiện tại."""
    lech = []
    for k in a:
        if a[k] == b.get(k):
            continue
        if isinstance(a[k], list) and a[k] and isinstance(a[k][0], str):
            mat = [x for x in a[k] if x not in b.get(k, [])]
            them = [x for x in b.get(k, []) if x not in a[k]]
            if mat:
                lech.append(f"{k}: MẤT {', '.join(mat)}")
            if them:
                lech.append(f"{k}: THÊM {', '.join(them)}")
        elif isinstance(a[k], list):
            lech.append(f"{k}: mốc {a[k]} → nay {b.get(k)}")
        else:
            lech.append(f"{k}: mốc {a[k]} → nay {b.get(k)}")
    return lech


def main():
    dsach = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not dsach:
        print(__doc__.split("Cách dùng:")[1].split("Quy trình")[0].strip())
        sys.exit(2)

    f = Path(dsach[0])
    try:
        noi = f.read_text(encoding="utf-8")
    except OSError as e:
        print(f"không đọc được {f}: {e}")
        sys.exit(2)

    d = do(noi)

    def cho(co):
        i = sys.argv.index(co)
        return Path(sys.argv[i + 1]) if i + 1 < len(sys.argv) else None

    if "--luu" in sys.argv:
        p = cho("--luu")
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Đã lưu mốc: {p}")
        sys.exit(0)

    if "--so" in sys.argv:
        p = cho("--so")
        moc = json.loads(p.read_text(encoding="utf-8"))
        lech = so_sanh(moc, d)
        if not lech:
            print(f"KHỚP — {f} giữ nguyên mọi bất biến so với {p}")
            sys.exit(0)
        print(f"LỆCH {len(lech)} chỗ, {f} so với {p}:")
        for x in lech:
            print("  " + x)
        print("\nMỗi dòng trên là một thứ bản dịch làm mất hoặc thêm. Không cái nào là"
              " lỗi về nghĩa — script này không kiểm nghĩa.")
        sys.exit(1)

    if "--json" in sys.argv:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        sys.exit(0)

    print(f"{f}")
    print(f"  heading      H1 {d['h1']} · H2 {d['h2']} · H3 {d['h3']}")
    print(f"  bảng         {d['bang']} bảng, {d['hang_bang']} hàng")
    print(f"  khối mã      {d['khoi_ma']}")
    for k, ten in (("ma_r", "mã R"), ("ma_ad", "mã AD"), ("ma_fr_nfr", "FR/NFR"),
                   ("tham_chieu_muc", "tham chiếu §")):
        if d[k]:
            print(f"  {ten:<12} {len(d[k])}")


if __name__ == "__main__":
    main()
