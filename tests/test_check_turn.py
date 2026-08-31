"""Kiểm `bin/check-turn.py` — hook Stop chặn lượt khi còn việc đo được là chưa xong.

    python -m unittest discover tests -v

Vì sao test này quan trọng hơn vẻ ngoài của nó: đây là một hook CHẶN. Hook chặn sai
thì hoặc nó khoá agent trong vòng lặp, hoặc người dùng tắt nó đi — và một hook bị tắt
không bảo vệ được gì. Hai ca nguy hiểm nhất được khoá ở đây là **chống lặp vô hạn** và
**`- [~]` không bị tính là chưa xong**.
"""

import importlib.util
import io
import json
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from tempfile import TemporaryDirectory

GOC = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("check_turn", GOC / "bin" / "check-turn.py")
ct = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ct)


class Nen(unittest.TestCase):
    """Mỗi ca chạy trên thư mục tạm — không đụng file thật của repo."""

    def setUp(self):
        self._tmp = TemporaryDirectory()
        d = Path(self._tmp.name)
        (d / ".git").mkdir()
        self._goc, self._tc, self._tt = ct.GOC, ct.TIEU_CHI, ct.TRANG_THAI
        ct.GOC = d
        ct.TIEU_CHI = d / ".done-criteria.md"
        ct.TRANG_THAI = d / ".git" / "agent-turn-state.json"

    def tearDown(self):
        ct.GOC, ct.TIEU_CHI, ct.TRANG_THAI = self._goc, self._tc, self._tt
        self._tmp.cleanup()

    def viet(self, noi):
        ct.TIEU_CHI.write_text(noi, encoding="utf-8")

    def chay_kiem_tieu_chi(self):
        """Trả mã thoát; None nghĩa là không chặn."""
        try:
            with redirect_stderr(io.StringIO()):
                ct.kiem_tieu_chi()
        except SystemExit as e:
            return e.code
        return None


class TestTieuChi(Nen):
    def test_khong_co_file_thi_khong_chan(self):
        """Việc nhỏ không cần khai báo — hook phải im lặng, nếu không nó thành thuế."""
        self.assertIsNone(self.chay_kiem_tieu_chi())

    def test_con_muc_chua_xong_thi_chan(self):
        self.viet("- [x] xong rồi\n- [ ] chưa làm\n")
        self.assertEqual(self.chay_kiem_tieu_chi(), 2)

    def test_tat_ca_da_xong_thi_khong_chan(self):
        self.viet("- [x] a\n- [x] b\n")
        self.assertIsNone(self.chay_kiem_tieu_chi())

    def test_muc_co_y_bo_khong_tinh_la_chua_xong(self):
        """`- [~]` là bỏ CÓ LÝ DO. Không có lối thoát này thì hook chặn mãi một việc
        đã quyết định không làm, và người dùng sẽ tắt hook."""
        self.viet("- [x] a\n- [~] bỏ vì cần remote, xem mục hoãn 17\n")
        self.assertIsNone(self.chay_kiem_tieu_chi())

    def test_dem_thut_dong_van_tinh(self):
        """Mục lồng trong danh sách vẫn là mục chưa xong."""
        self.viet("- [x] a\n  - [ ] con chưa làm\n")
        self.assertEqual(self.chay_kiem_tieu_chi(), 2)


class TestChongLapVoHan(Nen):
    """Ca nguy hiểm nhất: hook chặn mãi thì agent kẹt và người dùng tắt hook."""

    def test_chan_toi_da_roi_thoi(self):
        self.viet("- [ ] việc không làm nổi\n")
        ma = [self.chay_kiem_tieu_chi() for _ in range(ct.TOI_DA + 1)]
        self.assertEqual(ma[:ct.TOI_DA], [2] * ct.TOI_DA,
                         "phải chặn đủ số lần trước khi bỏ cuộc")
        self.assertEqual(ma[ct.TOI_DA], 0,
                         "quá ngưỡng thì cho đi tiếp, không khoá agent lại")

    def test_bo_dem_xoa_sau_khi_thoi_chan(self):
        self.viet("- [ ] x\n")
        for _ in range(ct.TOI_DA + 1):
            self.chay_kiem_tieu_chi()
        self.assertEqual(json.loads(ct.TRANG_THAI.read_text(encoding="utf-8")), {},
                         "bộ đếm phải sạch, nếu không lần chặn sau bị tính dồn")

    def test_bo_dem_rieng_theo_ly_do(self):
        """Hai lý do khác nhau không được cộng dồn vào nhau."""
        ct.TRANG_THAI.write_text(json.dumps({"test-do": ct.TOI_DA}), encoding="utf-8")
        self.viet("- [ ] x\n")
        self.assertEqual(self.chay_kiem_tieu_chi(), 2,
                         "bộ đếm của `test-do` không được làm câm `tieu-chi-chua-xong`")


class TestCanhBaoGrepBiCat(Nen):
    """Cảnh báo, KHÔNG chặn — `head` khi đang xem là hợp lệ, chỉ sai khi kết luận."""

    def _chay(self, noi):
        p = Path(self._tmp.name) / "t.jsonl"
        p.write_text(noi, encoding="utf-8")
        buf = io.StringIO()
        with redirect_stderr(buf):
            ct.kiem_grep_bi_cat(str(p))
        return buf.getvalue()

    def test_bao_khi_co_grep_head(self):
        self.assertIn("agent-pitfalls", self._chay('{"c":"grep -rn abc . | head -8"}\n'))

    def test_khong_bao_khi_da_dem(self):
        self.assertEqual(self._chay('{"c":"grep -rc abc . | wc -l"}\n'), "")

    def test_khong_bao_khi_dung_grep_c(self):
        self.assertEqual(self._chay('{"c":"grep -c abc x | head -1"}\n'), "")

    def test_transcript_khong_ton_tai_thi_im(self):
        self.assertEqual(ct.kiem_grep_bi_cat(str(Path(self._tmp.name) / "khong-co")), None)


if __name__ == "__main__":
    unittest.main()
