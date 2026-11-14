# Trịnh Trâm Anh — phần phụ trách trong bộ bảo vệ

Cập nhật ngày 15/11/2026. Nhánh `tramanh`, tài khoản `tta2405`. Phần tổng của nhóm nằm ở `main`; các số liệu thực nghiệm giữ mốc đã khóa, không đổi theo ngày biên tập tài liệu.

## Mở tài liệu hiện hành

- [Hồ sơ chung và hướng dẫn theo từng người](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/ho-so): chọn **Phần từng người** rồi chọn **Trịnh Trâm Anh**
- [Báo cáo tổng 62 trang](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/downloads/NhomTLCN_tong_20261114.pdf): đọc trang PDF **16–19 và 33–36**
- [Báo cáo đợt 4, 68 trang](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/downloads/NhomTLCN_dot4_20261114.pdf): đọc trang PDF **21–24 và 39–42**
- [Trình bày và demo](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/), [gói PDF, nguồn và demo offline](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/downloads/ATTQ_NIDS_BAN_GIAO_20261114.zip)
- [Bộ phát hành hiện hành trên main](https://github.com/YueLouis/tlcn-nids-unsw-nb15/tree/main/docs/releases/final_handoff_20261114)

Các số trang trên là số trang của trình đọc PDF, tính từ bìa. PDF/nguồn ngày 14/11 là bản nội dung hiện hành. Báo cáo đợt 3 đã gửi ngày 12/11 giữ nguyên; email đợt 4 và tổng chưa gửi.

## Phần cần nắm và đối chiếu

**Dữ liệu, nguồn học thuật, cách chia tập và giới hạn benchmark.** Hồ sơ chuyên môn đang lưu gồm:

- [PHAN_CHUYEN_MON.md](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/tramanh/docs/group_delivery_20261110/TramAnh/PHAN_CHUYEN_MON.md)
- [CHI_MUC_NGUON.csv](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/tramanh/docs/group_delivery_20261110/TramAnh/CHI_MUC_NGUON.csv)
- [DU_LIEU_MANIFEST.json](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/tramanh/docs/group_delivery_20261110/TramAnh/DU_LIEU_MANIFEST.json)
- [DUPLICATE_OVERLAP.json](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/tramanh/docs/group_delivery_20261110/TramAnh/DUPLICATE_OVERLAP.json)
- [KIEM_TRA_TAP_FIT.csv](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/tramanh/docs/group_delivery_20261110/TramAnh/KIEM_TRA_TAP_FIT.csv)
- [OVERLAP_MEAN_STD.csv](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/tramanh/docs/group_delivery_20261110/TramAnh/OVERLAP_MEAN_STD.csv)
- [MA_TRAN_TAI_LIEU.csv](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/tramanh/docs/group_delivery_20261110/TramAnh/MA_TRAN_TAI_LIEU.csv)

Mã và phụ thuộc dùng chung:

- [src/nids_benchmark/data.py](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/main/src/nids_benchmark/data.py)
- [src/nids_benchmark/preprocessing.py](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/main/src/nids_benchmark/preprocessing.py)

[Gói chuyên môn ngày 11/11](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/tramanh/docs/group_delivery_20261110/TramAnh/HO_SO_TRAMANH_20261111.zip) giữ mã, kiểm thử và nguồn theo đường dẫn gốc. Tệp bàn giao này chỉ nối hồ sơ đó sang bộ báo cáo hiện hành; không thay nguồn, gán lại tác giả hoặc bổ sung lịch sử đợt 1–2.

## Tự giải thích trước khi trình bày

1. Vì sao loại id, label và attack_cat khỏi đầu vào?
2. LOACO loại lớp tấn công bị giấu ra khỏi tập nào?
3. Preprocessing được fit trên tập nào, vì sao không fit lên official test?
4. Trùng flow giữa train và test ảnh hưởng cách diễn giải kết quả thế nào?

Khi ghi nhận xét, nêu **tệp / trang / chỗ chưa rõ / đề xuất sửa** rồi gửi vào Zalo nhóm. Không ghi đã kiểm, đã hiểu hoặc đã duyệt nếu chưa thực hiện. Dữ liệu demo là tập con UNSW-NB15, chưa phải traffic độc lập do nhóm thu; demo dùng mô hình đã lưu, không huấn luyện lại hay chặn tấn công.
