# Đối chiếu nguồn tài liệu - 14/10/2026

Ma trận có 13 nguồn, giữ DOI hoặc URL chính thức cùng citation key trong PDF. Mỗi dòng ghi vai trò, điều kiện/split/model/metric áp dụng, nội dung sử dụng, giới hạn và vị trí nguồn. Không coi mọi nguồn nền là nghiên cứu cùng benchmark để xếp hạng hiệu năng.

- 11 bài/tài liệu đã kiểm các đoạn nội dung liên quan từ bản PDF (9 bản đọc trực tiếp, 2 bản PDF tác giả qua web); trang dự án UNSW được đối chiếu riêng. Tổng cộng 12/13 nguồn có bằng chứng đoạn nội dung, 92,3%.
- S07: đã đối chiếu abstract/metadata, chưa lấy được toàn văn ACM. Không công bố số đo, split hay cấu hình chi tiết của bài này. Trang/bảng toàn văn vẫn còn mở.
- Đọc đoạn liên quan không đồng nghĩa đã nghiệm thu toàn bộ bài. Cột `group_review_status` giữ `pending` cho bản bổ sung; không điền nhận xét hoặc chữ ký thay thành viên.

`DOI_CHIEU_NGUON_20261014.md` là bản dễ đọc; `SOURCE_PASSAGE_EVIDENCE_20261014.json` ghi URL, phiên bản, trang và hash bản đã dùng khi có. `../evidence/dot_02/final_20261013/references_verified.json` giữ metadata lịch sử. Bản nháp và tệp tải để kiểm tra được lưu ngoài thư mục làm việc; hồ sơ này giữ chỉ dẫn truy về nguồn.

Điểm cần đọc kỹ: S03 định nghĩa FAR=(FPR+FNR)/2, khác FPR của nhóm; S04/S05 dùng bản tác giả/arXiv nên số trang khác bản xuất bản; S13 mô tả bộ đầy đủ 49 trường, còn hai CSV làm việc có 45 cột và pipeline dùng 42 feature. S09/S10 không biến AP trong mã thành diện tích hình thang PR-AUC.
