"""Test cho bin/work-state.py.

Chạy tay, không cần cài gì:

    python -m unittest discover tests -v

Dùng `unittest` của stdlib chứ không phải pytest, vì chính script cũng cố ý chỉ dùng
stdlib — nó phải chạy được ở worktree trống nơi worker Orca vừa khởi động. Test đòi
cài thêm gói sẽ phá đúng tính chất đó.

Mọi test dưới đây là hàm THUẦN: không đọc đĩa, không gọi orca, không phụ thuộc Orca
đang chạy hay không. Dữ liệu Orca truyền vào dạng tham số. Oracle vì thế tất định.

Mỗi test khoá lại một lỗi tìm ra khi chạy thật, không phải khi đọc mã. Bốn lỗi đầu
cùng một họ: script im lặng khi không kết luận được — đúng thứ nó sinh ra để bắt.
"""

import importlib.util
import unittest
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("work_state", GOC / "bin" / "work-state.py")
ws = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ws)


class TestBoDau(unittest.TestCase):
    """Hai nguồn viết slug khác nhau: story không dấu, sprint-status có dấu."""

    def test_bo_dau_tieng_viet(self):
        self.assertEqual(ws.bo_dau("chỉ-điểm-trưởng-môn"), "chi-diem-truong-mon")

    def test_bo_dau_giu_nguyen_khong_dau(self):
        self.assertEqual(ws.bo_dau("thu-bi-kip"), "thu-bi-kip")

    def test_chu_d_gach(self):
        """`đ` không phải dấu phụ nên NFD không tách được — phải xử riêng."""
        self.assertEqual(ws.bo_dau("đầu-đề"), "dau-de")


class TestKhopSprint(unittest.TestCase):
    def test_khop_qua_khac_biet_dau(self):
        sprint = {"1-3-chỉ-điểm-trưởng-môn-gọi-tên-sách": "done"}
        self.assertEqual(len(ws.khop_sprint("3-chi-diem-truong-mon-goi-ten-sach", sprint)), 1)

    def test_khop_khi_sprint_giu_ten_rut_gon(self):
        """sprint-status hay giữ tên cũ ngắn hơn sau khi story đổi phạm vi."""
        sprint = {"1-4-thu-bí-kíp": "in-progress"}
        self.assertEqual(len(ws.khop_sprint("4-thu-bi-kip-giam-dinh-va-trich-xuat", sprint)), 1)

    def test_khong_khop_ngau_nhien(self):
        """Bản đầu khớp nhầm vì vài âm tiết tình cờ giống. Khớp ngẫu nhiên nguy hơn không khớp."""
        sprint = {"1-3-chỉ-điểm-trưởng-môn-gọi-tên-sách": "done"}
        self.assertEqual(ws.khop_sprint("1-thiet-lap-ban-dau-ngon-ngu-giao-tiep", sprint), [])


class TestKhongImLang(unittest.TestCase):
    """Bốn nhánh không kết luận được. Không nhánh nào được rơi ra ngoài im lặng."""

    def test_thieu_sprint_status_phai_bao(self):
        # co_run=False để cô lập nhánh BMAD; với co_run=True script còn báo thêm
        # "story dở mà Orca không có task", đúng nhưng làm nhiễu phép kiểm này.
        lech, chua_so = ws.tim_lech(None, {"1-a": "in-progress"}, [], co_run=False)
        self.assertEqual(lech, [], "nhánh BMAD không kết luận được thì không được sinh lệch")
        self.assertTrue(any("sprint-status" in c for c in chua_so),
                        f"thiếu sprint-status phải vào chua_so, nhận: {chua_so}")

    def test_story_thieu_truong_status_phai_bao(self):
        _, chua_so = ws.tim_lech({"1-1-a": "done"}, {"1-a": "done"}, [], True,
                                 story_thieu_status=["specs/s/stories/2-b.md"])
        self.assertTrue(any("2-b.md" in c and "status" in c for c in chua_so),
                        f"file thiếu status phải vào chua_so, nhận: {chua_so}")

    def test_mot_dong_sprint_khop_nhieu_story(self):
        """EC-3: hai story khác nhau cùng nhận một dòng — chưa xác định được là cùng thứ gì."""
        sprint = {"1-1-alpha-beta": "done"}
        stories = {"1-alpha-beta-gamma": "done", "3-alpha-beta-delta": "done"}
        _, chua_so = ws.tim_lech(sprint, stories, [], True)
        self.assertTrue(any("khớp 2 story" in c for c in chua_so),
                        f"khớp nhiều-một phải vào chua_so, nhận: {chua_so}")

    def test_khong_tim_duoc_dong_tuong_ung(self):
        _, chua_so = ws.tim_lech({"9-9-hoan-toan-khac": "done"}, {"1-alpha-beta": "done"}, [], True)
        self.assertTrue(any("không tìm được" in c for c in chua_so))

    def test_chua_bind_run_phai_bao(self):
        _, chua_so = ws.tim_lech({"1-1-a-b": "done"}, {"1-a-b": "done"}, [], co_run=False)
        self.assertTrue(any("chưa bind" in c for c in chua_so))


class TestPhatHienLech(unittest.TestCase):
    def test_hai_nguon_khac_trang_thai(self):
        sprint = {"1-4-thu-bí-kíp": "done"}
        stories = {"4-thu-bi-kip-giam-dinh-va-trich-xuat": "in-progress"}
        lech, _ = ws.tim_lech(sprint, stories, [], co_run=False)
        self.assertEqual(len(lech), 1, f"chỉ được đúng một lệch, nhận: {lech}")
        self.assertIn("in-progress", lech[0])
        self.assertIn("done", lech[0])

    def test_story_do_dang_ma_orca_khong_co_task(self):
        lech, _ = ws.tim_lech({"1-1-a-b": "in-progress"}, {"1-a-b": "in-progress"}, [], True)
        self.assertTrue(any("ngoài điều phối" in l for l in lech))

    def test_orca_co_task_ma_khong_story_nao_do_dang(self):
        lech, _ = ws.tim_lech({"1-1-a-b": "done"}, {"1-a-b": "done"},
                              [{"id": "t1", "status": "ready"}], True)
        self.assertTrue(any("chưa đóng" in l for l in lech))

    def test_task_da_xong_khong_tinh_la_lech(self):
        lech, _ = ws.tim_lech({"1-1-a-b": "done"}, {"1-a-b": "done"},
                              [{"id": "t1", "status": "completed"}], True)
        self.assertEqual(lech, [])

    def test_trang_thai_khop_thi_khong_bao_lech(self):
        lech, chua_so = ws.tim_lech({"1-1-alpha-beta": "done"}, {"1-alpha-beta": "done"}, [], True)
        self.assertEqual(lech, [])
        self.assertEqual(chua_so, [])


class TestDocSprint(unittest.TestCase):
    """Parse YAML thủ công — khoá đúng hình dạng file để đổi cấu trúc là test đỏ."""

    def test_doc_duoc_file_that_cua_repo(self):
        muc, dong_la = ws.doc_sprint()
        if muc is None:
            self.skipTest("repo này không có sprint-status.yaml")
        self.assertGreater(len(muc), 0)
        self.assertTrue(all(isinstance(v, str) for v in muc.values()))

    def test_file_that_khong_co_dong_la(self):
        """Nếu test này đỏ, hình dạng `sprint-status.yaml` đã đổi và regex không theo kịp.

        Đây là lưới an toàn cho phép parse thủ công: regex mỏng thì phải có thứ báo
        khi file đổi, nếu không nó bỏ qua dòng trong im lặng và trạng thái đọc ra thiếu.
        """
        muc, dong_la = ws.doc_sprint()
        if muc is None:
            self.skipTest("repo này không có sprint-status.yaml")
        self.assertEqual(dong_la, [],
                         f"có dòng không parse được trong development_status: {dong_la}")

    def test_dong_la_duoc_bao_chu_khong_lan_vao_trang_thai(self):
        """Dòng không khớp hình dạng phải ra danh sách riêng, không nhét vào dict trạng thái."""
        muc, dong_la = ws.doc_sprint()
        if muc is None:
            self.skipTest("repo này không có sprint-status.yaml")
        self.assertFalse(any(k.startswith("__") for k in muc),
                         "không được dùng khoá đặc biệt trong dict trạng thái")


class TestLocWorktreeTheoRepo(unittest.TestCase):
    """`orca worktree ps` trả worktree của MỌI repo trên máy, không chỉ repo này.

    Ca đã xảy ra thật: báo 7 worktree trong khi chỉ 1 thuộc repo này, 6 cái kia là
    dự án khác — người đọc tưởng chúng liên quan tới story đang làm.
    """

    def _wt(self, path, repo_id, ten="x"):
        return {"path": path, "repoId": repo_id, "displayName": ten,
                "branch": "refs/heads/main", "workspaceStatus": "in-progress"}

    def test_chi_giu_worktree_cung_repo(self):
        goc = str(ws.GOC).replace("\\", "/")
        ds = {"worktrees": [
            self._wt(goc, "R1", "main"),
            self._wt(goc + "/con", "R1", "con"),
            self._wt("D:/khac/opms", "R2", "opms"),
            self._wt("D:/khac/test", "R3", "test"),
        ]}
        giu, loai, ly_do = ws.loc_worktree_repo_nay(ds)
        self.assertEqual(len(giu), 2, "worktree con cùng repoId phải được giữ")
        self.assertEqual(loai, 2)
        self.assertIsNone(ly_do)

    def test_khong_nhan_ra_repo_thi_bao_chu_khong_im_lang(self):
        """Không lọc bừa, và cũng không im lặng — phải trả lý do để vào
        `khong_doi_chieu_duoc`. Đây đúng ranh giới skill tự đặt: một phép so không
        chạy được khác hẳn một phép so chạy mà không thấy gì."""
        ds = {"worktrees": [self._wt("D:/khac/opms", "R2")]}
        giu, loai, ly_do = ws.loc_worktree_repo_nay(ds)
        self.assertEqual(len(giu), 1, "không nhận ra repo thì giữ nguyên, không vứt")
        self.assertEqual(loai, 0)
        self.assertIsNotNone(ly_do)

    def test_khong_co_worktree_nao(self):
        self.assertEqual(ws.loc_worktree_repo_nay({}), ([], 0, None))

    def test_so_sanh_path_khong_phan_biet_dau_gach_va_hoa_thuong(self):
        """Orca trả `C:/...`, Path trên Windows cho `C:\...` — so thô là trượt."""
        goc = str(ws.GOC).replace("/", "\\").upper()
        ds = {"worktrees": [self._wt(goc, "R1"), self._wt("D:/khac", "R2")]}
        giu, loai, ly_do = ws.loc_worktree_repo_nay(ds)
        self.assertEqual((len(giu), loai, ly_do), (1, 1, None))


if __name__ == "__main__":
    unittest.main()
