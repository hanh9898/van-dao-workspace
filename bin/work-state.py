#!/usr/bin/env python3
"""work-state.py — hợp nhất trạng thái BMAD và Orca thành một JSON duy nhất.

Vì sao script này tồn tại: công việc trong repo này có hai nguồn trạng thái sống
song song mà không tham chiếu nhau. BMAD giữ trạng thái trên đĩa (`sprint-status.yaml`,
frontmatter mỗi story). Orca giữ trạng thái trong runtime (Run, Task, Dispatch,
worktree). Không có gì nối chúng, nên không ai — người hay agent — trả lời được
câu "đang ở đâu" mà không mở hai chỗ rồi tự đối chiếu trong đầu.

Script chỉ trả **dữ kiện**, không khuyến nghị. Việc "nên làm gì tiếp" phụ thuộc ý
định của người dùng lúc đó, nên nó thuộc phần phán đoán của model, không thuộc đây.

Giá trị lớn nhất nằm ở khoá `lech`: nó phát hiện hai nguồn đang nói khác nhau —
thứ không thấy được bằng mắt vì phải mở hai nơi mới so được.

Dùng:
    work-state.py            JSON đầy đủ
    work-state.py --brief    bản rút gọn cho người đọc nhanh
    work-state.py --version  in phiên bản script

Mã thoát:
    0  đọc được ít nhất một nguồn
    1  không đọc được nguồn nào (sai thư mục?)

Không phụ thuộc gói ngoài — chỉ stdlib, để chạy được ở bất kỳ worktree nào kể cả
khi worker Orca khởi động trong môi trường chưa cài gì.
"""

import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

for _luong in (sys.stdout, sys.stderr):
    if hasattr(_luong, "reconfigure"):
        _luong.reconfigure(encoding="utf-8")

PHIEN_BAN = "1.1.0"

GOC = Path(__file__).resolve().parent.parent
SPRINT = GOC / "_bmad-output" / "implementation-artifacts" / "sprint-status.yaml"
STORIES = GOC / "_bmad-output" / "specs"


def chay_orca(*args):
    """Gọi orca, trả (ok, payload). Orca không chạy hay chưa bind Run đều KHÔNG phải lỗi."""
    try:
        r = subprocess.run(
            ["orca", *args, "--json"],
            capture_output=True, text=True, encoding="utf-8", timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return False, {"ly_do": type(e).__name__}
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return False, {"ly_do": "khong_parse_duoc", "stderr": r.stderr[:200]}
    if not d.get("ok"):
        return False, {"ly_do": (d.get("error") or {}).get("code", "khong_ro")}
    return True, d.get("result", {})


def doc_sprint():
    """Đọc development_status từ sprint-status.yaml. Parse thủ công — file có hình dạng cố định.

    Trả (trạng thái theo khoá, danh sách dòng không khớp hình dạng). Danh sách thứ hai
    tồn tại vì regex này mỏng: đổi cấu trúc file (thêm khoá lồng chẳng hạn) sẽ làm dòng
    rơi ra ngoài, và rơi im lặng thì không ai biết trạng thái đang đọc thiếu.
    """
    if not SPRINT.is_file():
        return None, []
    trong_block = False
    muc, dong_la = {}, []
    for dong in SPRINT.read_text(encoding="utf-8").splitlines():
        if dong.startswith("development_status:"):
            trong_block = True
            continue
        if trong_block:
            if dong and not dong.startswith(("  ", "\t")):
                break
            # Chỉ nhận dòng đúng hình dạng "  <key>: <giá-trị-đơn>". Khoá lồng
            # (giá trị rỗng rồi thụt sâu hơn) sẽ KHÔNG khớp và bị bỏ — nên đếm
            # riêng để hình dạng file đổi thì có dấu hiệu, không im lặng.
            if not dong.strip() or dong.strip().startswith("#"):
                continue
            m = re.match(r"^  ([^:#]+):[ 	]*([a-z][a-z-]*)[ 	]*(#.*)?$", dong)
            if m:
                muc[m.group(1).strip()] = m.group(2).strip()
            else:
                dong_la.append(dong.strip()[:60])
    return muc, dong_la


def doc_stories():
    """Đọc `status:` từ frontmatter mỗi story.

    Trả (status theo tên, file thiếu status, tên bị trùng). Hai danh sách sau không
    phải chi tiết thừa: một file story bị bỏ qua âm thầm là đúng loại lỗi script này
    sinh ra để bắt.
    """
    ra, thieu, trung = {}, [], []
    if not STORIES.is_dir():
        return ra, thieu, trung
    for f in sorted(STORIES.rglob("stories/*.md")):
        if f.name.endswith(".deferred.md"):
            continue
        dau = f.read_text(encoding="utf-8")[:800]
        m = re.search(r"^status:\s*'?([a-z-]+)'?", dau, re.M)
        if not m:
            thieu.append(str(f.relative_to(GOC)))
            continue
        if f.stem in ra:
            trung.append(str(f.relative_to(GOC)))
            continue
        ra[f.stem] = m.group(1)
    return ra, thieu, trung


def bo_dau(s):
    """Bỏ dấu **tiếng Việt**. Hai nguồn viết slug khác nhau — story không dấu,
    sprint-status có dấu — nên không chuẩn hoá thì phép khớp chỉ trúng ngẫu nhiên
    ở vài âm tiết tình cờ giống, và trúng ngẫu nhiên còn tệ hơn không trúng.

    Giới hạn có chủ ý: NFD tách được dấu phụ của phần lớn ngôn ngữ Latin, nhưng các
    ký tự gạch ngang thân như `đ` (Việt), `ø` (Bắc Âu), `ł` (Ba Lan) thì không —
    chúng là ký tự riêng, không phải chữ cái cộng dấu. Ở đây chỉ xử `đ`, vì repo này
    đặt tên bằng tiếng Việt. Dùng script cho repo ngôn ngữ khác thì bổ sung ở đây,
    đừng giả định nó đã tổng quát."""
    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if not unicodedata.combining(c))


def tu_khoa(ten):
    """Rút các từ có nghĩa từ một slug, đã bỏ dấu, để khớp giữa hai cách đặt tên."""
    return {t for t in re.split(r"[-_]", bo_dau(ten).lower())
            if len(t) > 2 and not t.isdigit()}


# Ngưỡng khớp slug. Đặt tên thay vì để số trần trong biểu thức, và giải thích ở đây
# vì hai con số này quyết định khi nào script dám kết luận:
#   TU_TRUNG_TOI_THIEU  — dưới mức này thì trùng có thể do ngẫu nhiên
#   TI_LE_TRUNG         — tính theo bên NGẮN hơn, vì sprint-status hay giữ tên rút gọn
TU_TRUNG_TOI_THIEU = 2
TI_LE_TRUNG = 0.6


def khop_sprint(ten_story, sprint):
    """Tìm dòng sprint-status ứng với một story. Trả danh sách ứng viên.

    0 ứng viên = không tìm được. >1 = mơ hồ. Cả hai đều KHÔNG được coi là 'không lệch'.
    """
    tk = tu_khoa(ten_story)
    ra = []
    for k, v in sprint.items():
        tk_k = tu_khoa(k)
        if not tk_k:
            continue
        trung = len(tk_k & tk)
        nho = min(len(tk), len(tk_k))
        if nho and trung >= TU_TRUNG_TOI_THIEU and trung / nho >= TI_LE_TRUNG:
            ra.append((k, v))
    return ra


def tim_lech(sprint, stories, orca_tasks, co_run, story_thieu_status=()):
    """Đối chiếu các nguồn. Hàm thuần — mọi đầu vào là tham số, không đọc đĩa, không gọi orca.

    Trả (lech, khong_doi_chieu_duoc). Tách hai thứ này là toàn bộ lý do script tồn tại:
    một phép so KHÔNG CHẠY ĐƯỢC khác hẳn một phép so chạy rồi thấy khớp. Mọi nhánh
    không kết luận được PHẢI đi vào danh sách thứ hai — không nhánh nào được im lặng.
    """
    lech, chua_so = [], []

    if not sprint:
        chua_so.append(
            "không đọc được `sprint-status.yaml` nên KHÔNG so được frontmatter story "
            "với sprint — đây không phải 'không có lệch'"
        )
    elif not stories:
        chua_so.append("không đọc được story nào nên không có gì để so với sprint-status")
    else:
        # Chiều một-nhiều: mỗi story khớp mấy dòng sprint
        da_khop = {}
        for ten, tt in sorted(stories.items()):
            ung_vien = khop_sprint(ten, sprint)
            if len(ung_vien) == 1:
                k, v = ung_vien[0]
                da_khop.setdefault(k, []).append(ten)
                if v != tt:
                    lech.append(
                        f"story `{ten}` frontmatter ghi '{tt}' nhưng sprint-status `{k}` ghi '{v}'"
                    )
            elif not ung_vien:
                chua_so.append(f"story `{ten}`: không tìm được dòng tương ứng trong sprint-status")
            else:
                ten_kh = ", ".join(k for k, _ in ung_vien)
                chua_so.append(
                    f"story `{ten}`: khớp mơ hồ với {len(ung_vien)} dòng sprint-status "
                    f"({ten_kh}) — không dám kết luận"
                )
        # Chiều nhiều-một: một dòng sprint bị nhiều story cùng nhận
        for k, ds in sorted(da_khop.items()):
            if len(ds) > 1:
                chua_so.append(
                    f"dòng sprint-status `{k}` khớp {len(ds)} story cùng lúc "
                    f"({', '.join(ds)}) — định danh mơ hồ, không kết luận được cái nào"
                )

    for f in sorted(story_thieu_status):
        chua_so.append(f"file story `{f}` không có trường `status:` trong frontmatter — bị bỏ qua")

    dang_lam = [k for k, v in (stories or {}).items() if v == "in-progress"]

    if not co_run:
        chua_so.append(
            "chưa bind Orca Run nên KHÔNG so được BMAD với Orca — "
            "chạy `orca orchestration run-create` hoặc `run-use` trước nếu cần phép so đó"
        )
    else:
        if dang_lam and not orca_tasks:
            lech.append(
                f"có {len(dang_lam)} story đang dở ({', '.join(dang_lam)}) "
                "nhưng Orca không có task nào — công việc đang chạy ngoài điều phối"
            )
        cho_xong = [t for t in (orca_tasks or []) if t.get("status") not in ("completed", "failed")]
        if cho_xong and not dang_lam:
            lech.append(
                f"Orca có {len(cho_xong)} task chưa đóng nhưng không story nào ở trạng thái in-progress"
            )
    return lech, chua_so


def main():
    if "--version" in sys.argv:
        print(f"work-state.py {PHIEN_BAN}")
        return

    brief = "--brief" in sys.argv

    sprint, dong_la = doc_sprint()
    stories, thieu_status, trung_ten = doc_stories()

    orca_ok, orca_status = chay_orca("status")
    tasks_ok, tasks = chay_orca("orchestration", "task-list")
    wt_ok, wt = chay_orca("worktree", "ps")

    danh_sach_task = tasks.get("tasks", []) if tasks_ok else []
    lech, chua_so = tim_lech(sprint, stories, danh_sach_task, tasks_ok, thieu_status)
    for f in trung_ten:
        chua_so.append(f"file story `{f}` trùng tên với một story khác — bị bỏ qua")
    if dong_la:
        chua_so.append(
            f"{len(dong_la)} dòng trong `development_status` không đúng hình dạng "
            f"`  <khoá>: <giá-trị>` nên bị bỏ qua (ví dụ: {dong_la[0]!r}) — "
            "hình dạng file có thể đã đổi"
        )

    ket_qua = {
        "goc_repo": str(GOC),
        "bmad": {
            "doc_duoc": sprint is not None,
            "sprint_status_dang_hoat_dong": (
                {k: v for k, v in sprint.items() if v not in ("backlog", "optional")}
                if sprint else None
            ),
            "so_dong_sprint_bo_qua": (
                sum(1 for v in sprint.values() if v in ("backlog", "optional")) if sprint else 0
            ),
            "story_status_khong_done": {k: v for k, v in stories.items() if v != "done"},
            "so_story_done": sum(1 for v in stories.values() if v == "done"),
            "dang_lam": [k for k, v in stories.items() if v == "in-progress"],
        },
        "orca": {
            "app_chay": orca_ok,
            "phien_ban": (orca_status.get("runtime") or {}).get("appVersion") if orca_ok else None,
            "co_run_binding": tasks_ok,
            "ly_do_khong_co_task": None if tasks_ok else tasks.get("ly_do"),
            "task": [
                {"id": t.get("id"), "status": t.get("status"),
                 "spec": (t.get("spec") or "")[:120]}
                for t in danh_sach_task
            ],
            "worktree_doc_duoc": wt_ok,
            "worktree": [
                {"ten": w.get("displayName"), "branch": w.get("branch"),
                 "trang_thai": w.get("workspaceStatus")}
                for w in (wt.get("worktrees", []) if wt_ok else [])
            ] if wt_ok else None,
        },
        "lech": lech,
        "khong_doi_chieu_duoc": chua_so,
    }

    if sprint is None and not stories:
        print(json.dumps(
            {"loi": "khong_doc_duoc_nguon_nao",
             "goi_y": f"Chạy từ trong repo có _bmad-output/. Đang tìm ở: {GOC}"},
            ensure_ascii=False, indent=2))
        sys.exit(1)

    if brief:
        b = ket_qua["bmad"]
        o = ket_qua["orca"]
        print(f"Repo  : {ket_qua['goc_repo']}")
        so_story = len(b["story_status_khong_done"]) + b["so_story_done"]
        print(f"BMAD  : {so_story} story, đang dở: {b['dang_lam'] or '(không có)'}")
        wt = "?" if o["worktree"] is None else len(o["worktree"])
        print(f"Orca  : {'chạy' if o['app_chay'] else 'không chạy'}"
              f" · {len(o['task'])} task · {wt} worktree")
        if ket_qua["lech"]:
            print("LỆCH  :")
            for l in ket_qua["lech"]:
                print(f"  - {l}")
        else:
            print("LỆCH  : không thấy (trong phạm vi đã so được)")
        if ket_qua["khong_doi_chieu_duoc"]:
            print("CHƯA SO ĐƯỢC:")
            for c in ket_qua["khong_doi_chieu_duoc"]:
                print(f"  - {c}")
    else:
        print(json.dumps(ket_qua, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
