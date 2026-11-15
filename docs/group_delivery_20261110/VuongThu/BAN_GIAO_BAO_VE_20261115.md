# Hoàng Văn Vương Thu — phần phụ trách trong bộ bảo vệ

Cập nhật ngày 15/11/2026. Nhánh `vuongthu`, tài khoản `hoangvvthu`. Phần tổng của nhóm nằm ở `main`; các số liệu thực nghiệm giữ mốc đã khóa, không đổi theo ngày biên tập tài liệu.

## Mở tài liệu hiện hành

- [Hồ sơ chung và hướng dẫn theo từng người](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/ho-so): chọn **Phần từng người** rồi chọn **Hoàng Văn Vương Thu**
- [Báo cáo tổng 62 trang](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/downloads/NhomTLCN_tong_20261114.pdf): đọc trang PDF **12–14, 19, 24–29; đọc sâu 31–48**
- [Báo cáo đợt 4, 68 trang](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/downloads/NhomTLCN_dot4_20261114.pdf): đọc trang PDF **12–14, 24, 29–34; đọc sâu 37–54**
- [Trình bày và demo](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/), [gói PDF, nguồn và demo offline](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/downloads/ATTQ_NIDS_BAN_GIAO_20261114.zip)
- [Bộ phát hành hiện hành trên main](https://github.com/YueLouis/tlcn-nids-unsw-nb15/tree/main/docs/releases/final_handoff_20261114)

Các số trang trên là số trang của trình đọc PDF, tính từ bìa. PDF/nguồn ngày 14/11 là bản nội dung hiện hành. Báo cáo đợt 3 đã gửi ngày 12/11 giữ nguyên; email đợt 4 và tổng chưa gửi.

## Phần cần nắm và đối chiếu

**Isolation Forest, Autoencoder, ngưỡng, metric và phân tích lỗi.** Hồ sơ chuyên môn đang lưu gồm:

- [PHAN_CHUYEN_MON.md](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/vuongthu/docs/group_delivery_20261110/VuongThu/PHAN_CHUYEN_MON.md)
- [CHI_MUC_NGUON.csv](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/vuongthu/docs/group_delivery_20261110/VuongThu/CHI_MUC_NGUON.csv)
- [AP_MEAN_STD.csv](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/vuongthu/docs/group_delivery_20261110/VuongThu/AP_MEAN_STD.csv)
- [DIEM_VAN_HANH.csv](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/vuongthu/docs/group_delivery_20261110/VuongThu/DIEM_VAN_HANH.csv)
- [HAI_NGUONG_FPR.csv](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/vuongthu/docs/group_delivery_20261110/VuongThu/HAI_NGUONG_FPR.csv)
- [DO_ON_DINH_LOI.csv](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/vuongthu/docs/group_delivery_20261110/VuongThu/DO_ON_DINH_LOI.csv)
- [VI_DU_GAN_NGUONG.csv](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/vuongthu/docs/group_delivery_20261110/VuongThu/VI_DU_GAN_NGUONG.csv)
- [NGUON_VI_DU_THU.csv](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/vuongthu/docs/group_delivery_20261110/VuongThu/NGUON_VI_DU_THU.csv)
- [PHAT_HIEN_THEO_LOAI.png](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/vuongthu/docs/group_delivery_20261110/VuongThu/PHAT_HIEN_THEO_LOAI.png)

Mã và phụ thuộc dùng chung:

- [src/nids_benchmark/evaluation.py](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/main/src/nids_benchmark/evaluation.py)

[Gói chuyên môn ngày 11/11](https://github.com/YueLouis/tlcn-nids-unsw-nb15/blob/vuongthu/docs/group_delivery_20261110/VuongThu/HO_SO_VUONGTHU_20261111.zip) giữ mã, kiểm thử và nguồn theo đường dẫn gốc. Tệp bàn giao này chỉ nối hồ sơ đó sang bộ báo cáo hiện hành; không thay nguồn, gán lại tác giả hoặc bổ sung lịch sử đợt 1–2.

## Tự giải thích trước khi trình bày

1. Vì sao IF và AE chỉ học Normal?
2. Hai ngưỡng target FPR 1% và 5% lấy từ đâu?
3. AP cao khác gì UADR cao trên lớp tấn công bị giấu?
4. Khi giảm ngưỡng, vì sao có thể phát hiện thêm tấn công nhưng tăng cảnh báo nhầm?

Khi ghi nhận xét, nêu **tệp / trang / chỗ chưa rõ / đề xuất sửa** rồi gửi vào Zalo nhóm. Không ghi đã kiểm, đã hiểu hoặc đã duyệt nếu chưa thực hiện. Dữ liệu demo là tập con UNSW-NB15, chưa phải traffic độc lập do nhóm thu; demo dùng mô hình đã lưu, không huấn luyện lại hay chặn tấn công.
