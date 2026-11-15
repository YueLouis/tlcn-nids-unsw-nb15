# Nguyễn Trọng Tín — phần phụ trách trong bộ bảo vệ

Cập nhật ngày 15/11/2026. Nhánh `trongtin`, tài khoản `YueLouis`. Phần tổng của nhóm nằm ở `main`; các số liệu thực nghiệm giữ mốc đã khóa, không đổi theo ngày biên tập tài liệu.

## Mở tài liệu hiện hành

- [Hồ sơ chung và hướng dẫn theo từng người](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/ho-so): chọn **Phần từng người** rồi chọn **Nguyễn Trọng Tín**
- [Báo cáo tổng 62 trang](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/downloads/NhomTLCN_tong_20261114.pdf): đọc trang PDF **12, 20–24 và 53–58**
- [Báo cáo đợt 4, 68 trang](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/downloads/NhomTLCN_dot4_20261114.pdf): đọc trang PDF **12, 25–29 và 59–64**
- [Trình bày và demo](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/), [gói PDF, nguồn và demo offline](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/downloads/ATTQ_NIDS_BAN_GIAO_20261114.zip)
- [Bộ phát hành hiện hành trên main](https://github.com/YueLouis/tlcn-nids-unsw-nb15/tree/main/docs/releases/final_handoff_20261114)

Các số trang trên là số trang của trình đọc PDF, tính từ bìa. PDF/nguồn ngày 14/11 là bản nội dung hiện hành. Báo cáo đợt 3 đã gửi ngày 12/11 giữ nguyên; email đợt 4 và tổng chưa gửi.

## Phần cần nắm và đối chiếu

**Protocol, RF/XGBoost, pipeline, tái lập, demo và tích hợp.** Hồ sơ chuyên môn đang lưu gồm:

- [PHAN_CHUYEN_MON.md](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/trongtin/docs/group_delivery_20261110/TrongTin/PHAN_CHUYEN_MON.md)
- [CHI_MUC_NGUON.csv](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/trongtin/docs/group_delivery_20261110/TrongTin/CHI_MUC_NGUON.csv)

Mã và phụ thuộc dùng chung:

- [scripts/demo_server.py](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/main/scripts/demo_server.py)
- [demo/presentation/](https://github.com/YueLouis/tlcn-nids-unsw-nb15/tree/main/demo/presentation/)

[Gói chuyên môn ngày 11/11](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/trongtin/docs/group_delivery_20261110/TrongTin/HO_SO_TRONGTIN_20261111.zip) giữ mã, kiểm thử và nguồn theo đường dẫn gốc. Tệp bàn giao này chỉ nối hồ sơ đó sang bộ báo cáo hiện hành; không thay nguồn, gán lại tác giả hoặc bổ sung lịch sử đợt 1–2.

## Tự giải thích trước khi trình bày

1. Ma trận 80 run được tính như thế nào?
2. Bản local và public thực hiện suy luận ở đâu?
3. CSV không có nhãn cho phép kết luận được và chưa kết luận được điều gì?
4. Khi mất mạng hoặc HDMI lỗi, nhóm trình bày bằng phương án nào?

Khi ghi nhận xét, nêu **tệp / trang / chỗ chưa rõ / đề xuất sửa** rồi gửi vào Zalo nhóm. Không ghi đã kiểm, đã hiểu hoặc đã duyệt nếu chưa thực hiện. Dữ liệu demo là tập con UNSW-NB15, chưa phải traffic độc lập do nhóm thu; demo dùng mô hình đã lưu, không huấn luyện lại hay chặn tấn công.
