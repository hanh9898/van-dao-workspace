# Rubric Walker — ARCHITECTURE-SPINE.md (Vấn Đạo)

Checklist nguồn: `references/reviewer-gate.md` (skill bmad-architecture), đối chiếu với PRD
(`prd-van-dao-workspace-2026-08-24/prd.md`) và đặc tả (`docs/VAN-DAO-dac-ta-v1.0.md`).

## 1. Cố định đúng điểm phân kỳ, không bỏ sót? — **CONCERN**

7 AD hiện có phủ tốt: cách ly actor (AD-1), event-sourcing (AD-2), single-writer (AD-3), luật chọn
loại thành phần (AD-4), phân loại dữ liệu (AD-5), lộ đồ-là-hợp-đồng-sống (AD-6), hook-chỉ-gác-ranh-giới-thật
(AD-7). Nhưng **một chiều load-bearing bị bỏ sót hoàn toàn**: đặc tả §5.9 (dòng ~699-701) đặt ra
**"Ba luật chống context rot"** — (1) cái gì nạp mỗi phiên phải cố định cỡ (SessionStart chỉ nạp hồ sơ +
bản đồ + lộ đồ đang dở, cả ba cố định cỡ, không dài ra theo lịch sử), (2) cái gì lớn theo thời gian phải
nằm sau một truy vấn có lọc (`lo-trinh.jsonl`, `can-cu/*.jsonl` không bao giờ nạp toàn bộ), (3) chi phí
tỉ lệ với **thứ cần**, không với **thứ có**. Đây đúng là điểm hai epic độc lập có thể chọn lệch nhau thật
sự — một epic viết logic nạp phiên có thể "nạp cho chắc" toàn bộ `lo-trinh.jsonl`, epic khác đúng luật lọc
— và event-sourcing (AD-2) chỉ nói *cách ghi*, không nói *cách đọc có giới hạn*. Không có AD, không có
dòng Deferred, không có câu hỏi mở nào nhắc tới luật này — im lặng hoàn toàn. **Nên thêm AD-8** ràng buộc
đúng ba luật này, Binds ít nhất `SessionStart` (`nap-ho-so.sh`) + mọi vai đọc log tăng trưởng
(`truong-lao`, `truong-mon`).

## 2. Mỗi AD's Rule enforceable, ngăn đúng divergence? — **CONCERN (nhẹ)**

AD-1, AD-3, AD-6, AD-7 có đường thực thi cụ thể (kiem-thu.py/hook, `.pham-vi.json`, script dấu vân tay).
AD-2, AD-4, AD-5 hiện là **quy ước không có script/test nào xác nhận** — chấp nhận được cho một spine
(review có thể enforce), nhưng đáng ghi rõ trong spine rằng đây là "enforced by code review" chứ không
phải "enforced by tooling", để tầng epic không tưởng nhầm có script kiểm sẵn. Không phải lỗi chặn, chỉ là
thiếu một dòng làm rõ mức thực thi của từng AD.

## 3. Deferred có an toàn để hoãn không? — **PASS**

FR31 (UX hẹp, đã có lý do hoãn cụ thể), cơ chế dấu vân tay AD-6 (chi tiết implementation, đúng tầng dưới
quyết), môi trường vận hành (nêu rõ "không có" thay vì im lặng — đúng cách checklist muốn), Vòng 3/4 (đã
chốt thứ tự ở đặc tả §16, không lặp lại). Không mục nào trong Deferred có nguy cơ hai đơn vị chọn lệch.

## 4. Tech nêu tên còn đúng/phù hợp? — **CONCERN**

Spine dẫn "đã chạy thật để xác minh" từ đặc tả, nhưng đó là xác minh **tại thời điểm viết đặc tả**, không
phải tại thời điểm chạy run kiến trúc này (2026-08-25) — spine chưa tự tái-xác-minh
`book-to-skill` (virgiliojr94) trên web (còn tồn tại, còn cùng API `[pdf,epub]` extras không). Đây đúng là
việc lens "web-verification" trong `finalize_reviewers` phải làm — nếu lens đó cũng bỏ qua thì đây là lỗ
hổng thật của cả gate, không chỉ của rubric walker.

## 5. Ratify hay mâu thuẫn đặc tả? — **PASS** (theo phạm vi đọc được)

Không thấy đoạn đặc tả nào giả định lộ đồ bất biến sau duyệt hay có cơ chế duyệt-lại khác — AD-6/AD-7 là
bổ sung hợp lệ, không mâu thuẫn. (Một fork riêng đang đối chiếu sâu hơn toàn bộ đặc tả cho việc này — xem
`reconcile-dac-ta.md` khi có.)

## 6. Phủ đủ capability PRD? — **PASS**

Bảng Capability→Architecture Map phủ cả 7 nhóm FR (4.1-4.7). Không kiểm chi tiết từng FR lẻ (việc của
`reconcile-prd.md` riêng).

## 7. Chiều nào bị im lặng hoàn toàn? — **Xem mục 1** (context rot). Môi trường vận hành đã được nói rõ
(mục 3), không bị bỏ sót.

---

**Verdict:** CONCERNS — không có FAIL chặn, nhưng thiếu một AD load-bearing thật (context-rot budget,
§5.9) và một khoảng thiếu tái-xác-minh tech hiện tại. Khuyến nghị thêm AD-8 trước khi đóng spine.
