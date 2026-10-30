# Việc của Trâm Anh — dữ liệu và nguồn

**Cách làm mới 25/10:** đã có [bộ báo cáo và ảnh hướng dẫn](../../../../02_Bao_cao/BO_HO_SO_NHOM_20261025/MO_DAU.html). Anh đọc Chương 3, phần overlap Chương 7 và tài liệu tham khảo của báo cáo tổng; ghi trang, nguồn đã mở, điều hiểu và chỗ muốn sửa. Chưa cần viết lại từ đầu. Các yêu cầu tự viết/hạn bên dưới là phương án lịch sử 22/10, không áp làm hạn chậm nộp.

## Phương án ban đầu 22/10 (lịch sử)

Bạn chịu trách nhiệm phần “dữ liệu này là gì và kết luận bị giới hạn ở đâu”, rồi viết thành phần dùng được trong báo cáo. Hạn bản đầu **25/10**, bản chính **29/10**, sửa sau review **05/11**; đây là hạn nội bộ đề xuất.

## Bắt đầu từ đây

Tính từ gốc repo `tlcn-nids-unsw-nb15/`:

1. `artifacts/data/data_manifest.json`: số dòng/cột, nhãn, category, hash.
2. `docs/evidence/dot_02/DATA_CONTRACT.md`: 42 feature, metadata và các cột categorical.
3. `docs/references/RELATED_WORK_MATRIX_DOT_02.csv`: S03 về UNSW-NB15, S13 nguồn chính thức, S12 về giới hạn NIDS thực tế; S07 đang thiếu toàn văn.
4. `docs/report_cumulative/BAO_CAO_TLCN_TICH_LUY_DOT_02.tex`, mục duplicate/overlap; bản PDF 37 trang trong hồ sơ nhóm.
5. `artifacts/data/duplicate_overlap_audit.json` trên máy nhóm trưởng/Drive. Nếu bản clone thiếu, nhờ Tín cấp đúng bản; không tự kết luận artifact không tồn tại.

## Sản phẩm bạn tự tạo

**`ANH_DU_LIEU_VA_GIOI_HAN.md`**: bảng train/test, tổng dòng, Normal/Attack, support Reconnaissance/DoS/Exploits, feature đầu vào và metadata bị loại. Mỗi hàng có đường dẫn nguồn; tự giải thích official train khác tập fit mỗi seed thế nào. Viết đoạn giải thích duplicate/overlap; phân biệt overlap với official train và overlap với tập fit thực tế. Đếm overlap sẵn có chưa phải bằng chứng định lượng tác động đến UADR.

**`ANH_PHIEU_DOC_NGUON.md`**: tự đọc ít nhất S03, S12 và S13. Mỗi nguồn ghi URL/DOI, đúng trang/mục đã đọc, diễn giải bằng lời của mình, phần báo cáo được hỗ trợ và điều nguồn không chứng minh. Kiểm lại S07: nếu chưa lấy được toàn văn, ghi đúng trạng thái; không cần gán hoàn thành chỉ để đủ nguồn.

**`ANH_NOI_DUNG_BAO_CAO.md`**: khoảng 1–2 trang nội dung dữ liệu và giới hạn, đủ nguồn trích, có thể ghép vào báo cáo tích lũy. Không viết “không có leakage” tuyệt đối, “phát hiện mọi zero-day” hoặc suy ra hiệu quả vận hành thực tế từ benchmark.

## Đạt khi nào

- Tự mở được nguồn từng số trong bảng; phân biệt 45 cột, 42 feature gốc và số chiều sau encoding.
- Nói được một ví dụ held-out và vì sao phải loại trước khi split/fit.
- Mỗi nhận định có nguồn/bằng chứng và giới hạn; ghi rõ đọc abstract/đoạn/toàn văn.
- Thu review support/diễn giải; Tín đối chiếu bảng với manifest. Bạn tự sửa và ghi lại nhận xét đã xử lý.

**Chưa có sản phẩm do bạn bàn giao trong hồ sơ mới.** Nội dung trên là giao việc, không phải xác nhận bạn đã làm. Ghi phần công cụ hỗ trợ riêng khi bàn giao.
