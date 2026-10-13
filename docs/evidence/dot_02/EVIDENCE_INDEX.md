# Evidence đợt 2 - cập nhật 13/10/2026

| Đầu ra | Nguồn kiểm chứng | Kết quả |
|---|---|---|
| Raw train/test | artifacts/data/data_manifest.json | SHA-256 khớp; 175341/82332 dòng x 45 cột |
| Duplicate/overlap | artifacts/data/duplicate_overlap_audit.json | Có giới hạn overlap; xem DATA_CONTRACT.md |
| Protocol | docs/protocol/RUN_MATRIX.csv; final_20261013/protocol.log | 80 ID đúng ma trận |
| Test | tests/; final_20261013/unit_tests.log | 17/17 PASS |
| Artifact | results/runs/ | 80 run completed; 320 file bắt buộc |
| Audit prediction | final_20261013/audit_current.py; numerical_audit.json | 13.173.120 dòng; không sai lệch |
| Cách chia dữ liệu đã lưu | scripts/audit_saved_partitions.py; final_20261013/saved_split_audit.json | Scaler của 80/80 model khớp phân tầng theo attack_cat; không huấn luyện lại |
| PDF | output/pdf/NhomTLCN_TramAnh_VuongThu_TrongTin_dot2.pdf | 30 trang, tích lũy từ đợt 1 |
| Tài liệu nền | docs/references/; final_20261013/references_verified.json | 12 DOI metadata + trang UNSW; full-text review còn mở |
| Xác nhận nhóm | final_20261013/XAC_NHAN_NHOM_20261013.md | Nhóm trưởng cung cấp xác nhận cả ba; không thay chữ ký/duyệt của thầy |

Log là đầu ra thật; không dùng ảnh thẻ PASS dựng lại làm chứng cứ. Bản nháp và hình minh họa tháng 9 đã bảo toàn ngoài workspace, có nhật ký di chuyển SHA-256.
