"""Kiểm mọi artifact harness đều có mặt trong sổ dấu vết review.

    python -m unittest discover tests -v

Test này kiểm **sự có mặt**, không kiểm chất lượng review. Lý do có chủ ý: một quy
tắc mới áp lên artifact có sẵn sẽ đỏ hàng loạt, và phép kiểm đỏ kéo dài thì bị tắt.
Nợ được phép tồn tại trong sổ; thứ không được phép là một artifact mới xuất hiện mà
không ai ghi nhận — ca đã xảy ra thật với `orca-help`.

Phạm vi tính theo `git ls-files`, nên artifact bị gitignore (49 skill BMAD chẳng hạn)
tự động nằm ngoài mà không cần danh sách loại trừ tự bịa.
"""

import re
import subprocess
import unittest
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
SO = GOC / "_bmad-output" / "implementation-artifacts" / "review-log.md"

# Mẫu đường dẫn thuộc phạm vi. Thêm nhóm mới thì thêm một dòng ở đây — và nhớ rằng
# thêm nhóm nghĩa là mọi file cũ trong nhóm đó phải được ghi vào sổ cùng lượt.
PHAM_VI = (
    ".claude/skills/*/SKILL.md",
    "bin/*.py",
    "docs/*.md",
    "_bmad/custom/lenses/*.md",
    # Test là code sẽ chạy, và một test sai cho cảm giác an toàn giả — loại nguy hiểm
    # nhất. Chính file này fail ở lần chạy đầu vì bug của nó, nên nó thuộc phạm vi.
    "tests/*.py",
    # Override quyết định lens nào chạy và skill hành xử ra sao; sai thì hành vi đổi
    # mà không file nào khác lộ ra.
    "_bmad/custom/*.toml",
    # Chính cuốn sổ. Nó không chỉ ghi lại — nó định nghĩa phạm vi và ba trạng thái,
    # tức là một chuẩn. Cơ chế tự loại mình ra khỏi tầm kiểm là chỗ nó mù nhất.
    "_bmad-output/implementation-artifacts/review-log.md",
)

TRANG_THAI_HOP_LE = {"da-review", "no", "mien-tru"}


def la_dong_artifact(dong):
    """Dòng bảng có cột đầu là một ĐƯỜNG DẪN.

    Cần thiết vì sổ còn có bảng giải thích ba trạng thái, cùng hình dạng `| \`x\` | ... |`.
    Không lọc thì test đọc dòng giải thích thành artifact — lỗi này đã xảy ra thật ở
    lần chạy đầu, và nó fail theo kiểu khó hiểu (`'no'` bị báo là thiếu mốc).
    """
    if not dong.startswith("| `"):
        return None
    o = [x.strip() for x in dong.split("|")]
    if len(o) < 4:
        return None
    ten = o[1].strip("`")
    return o if "/" in ten else None


def artifact_trong_pham_vi():
    """Mọi file git-tracked khớp một mẫu trong PHAM_VI."""
    ra = []
    for mau in PHAM_VI:
        r = subprocess.run(
            ["git", "ls-files", mau],
            cwd=GOC, capture_output=True, text=True, encoding="utf-8",
        )
        ra.extend(d.strip() for d in r.stdout.splitlines() if d.strip())
    return sorted(set(ra))


class TestSoDauVetReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not SO.is_file():
            raise unittest.SkipTest(f"chưa có sổ: {SO}")
        cls.noi_dung = SO.read_text(encoding="utf-8")

    def test_moi_artifact_co_mat_trong_so(self):
        """Ca test này tồn tại để bắt: thêm artifact mới mà quên ghi nhận."""
        thieu = [a for a in artifact_trong_pham_vi() if a not in self.noi_dung]
        self.assertEqual(
            thieu, [],
            "artifact sau chưa có dòng nào trong review-log.md — thêm vào sổ với một "
            f"trong ba trạng thái {sorted(TRANG_THAI_HOP_LE)}:\n  " + "\n  ".join(thieu),
        )

    def test_moi_dong_dung_trang_thai_hop_le(self):
        """Trạng thái viết sai chính tả sẽ lọt qua phép kiểm trên nếu không có test này."""
        dong_bang = [o for o in map(la_dong_artifact, self.noi_dung.splitlines()) if o]
        self.assertGreater(len(dong_bang), 0, "sổ không có dòng artifact nào")
        sai = []
        for o in dong_bang:
            tt = o[2].strip("`")
            if tt not in TRANG_THAI_HOP_LE:
                sai.append(f"{o[1]} → trạng thái {tt!r}")
        self.assertEqual(sai, [], "trạng thái không hợp lệ:\n  " + "\n  ".join(sai))

    def test_moi_muc_no_deu_co_moc_quay_lai(self):
        """Nợ không mốc thì không phải hoãn, là quên — cùng luật với deferred-work.md."""
        thieu_moc = []
        for d in self.noi_dung.splitlines():
            o = la_dong_artifact(d)
            if not o or o[2].strip("`") != "no":
                continue
            if not re.search(r"[Mm]ốc:", o[3]):
                thieu_moc.append(o[1])
        self.assertEqual(
            thieu_moc, [],
            "mục `no` phải ghi 'Mốc:' — nợ không mốc thì không phải hoãn:\n  "
            + "\n  ".join(thieu_moc),
        )

    def test_khong_ghi_artifact_da_bien_mat(self):
        """Sổ liệt kê file không còn tồn tại nghĩa là nó lạc hậu theo chiều ngược lại."""
        trong_pham_vi = set(artifact_trong_pham_vi())
        da_mat = []
        for d in self.noi_dung.splitlines():
            if not d.startswith("| `"):
                continue
            m = re.match(r"\| `([^`]+)`", d)
            if not m:
                continue
            duong_dan = m.group(1)
            if "/" not in duong_dan:
                continue
            if duong_dan not in trong_pham_vi and not (GOC / duong_dan).exists():
                da_mat.append(duong_dan)
        self.assertEqual(da_mat, [],
                         "sổ ghi artifact không còn tồn tại:\n  " + "\n  ".join(da_mat))


if __name__ == "__main__":
    unittest.main()
