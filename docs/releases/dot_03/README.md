# Báo cáo đợt 3 — chốt kỹ thuật ngày 30/10/2026

[Đọc PDF 60 trang](NhomTLCN_TramAnh_VuongThu_TrongTin_dot3.pdf) · [Thư mục Drive đầy đủ](https://drive.google.com/drive/folders/1AyxVWgeJj9mZ0L_d0AVosxKS6IUpghbe) · [ZIP nguồn](https://drive.google.com/file/d/1TGvWrlX7XEU1vKEIkcmN7pH2L2P9OCH3/view) · [Nguồn TeX](../../report_dot3_final_20261030/main.tex)

Mốc báo cáo 09/11/2026 theo nhóm trưởng xác nhận đã thống nhất với thầy. Phạm vi kết quả chốt đến 30/10; phần 31/10–08/11 là kế hoạch tiếp theo. Đây là bản đã kiểm kỹ thuật, chưa có xác nhận cả ba duyệt nội dung; chưa gửi email/nộp và chưa được giảng viên phê duyệt. Tín tự gửi; lời nhắc tối 08/11 và sáng 09/11 giữ nguyên.

## Bằng chứng kiểm

- 46 unit test đạt; protocol đủ 4 kịch bản × 4 model × 5 seed = 80 run.
- Tính lại PR/score và overlap từ kết quả đã lưu; tám CSV khớp. Kiểm feature importance 40 bundle và 174 dòng bảng in theo CSV.
- Demo: 16 bundle × hai target, 3.200 dự đoán/nhãn/ngưỡng khớp; sai khác score tuyệt đối tối đa 2,197×10⁻⁷, trong dung sai 10⁻⁶.
- Dựng lại ZIP nguồn: văn bản và ảnh cả 60 trang khớp PDF; không có tham chiếu thiếu, ký tự thiếu hoặc dòng tràn trong log LaTeX.
- 333 hash đầu vào lịch sử được bảo toàn. Không huấn luyện lại hoặc chọn lại ngưỡng.
- Bản Drive tải lại: đủ 14 tệp (gồm MANIFEST), SHA-256 khớp toàn bộ local.

[Audit mới](../../evidence/dot_03/final_20261030/) · [Đối chiếu Drive](../../evidence/dot_03/sync_20261030/DRIVE_RELEASE_READBACK.json) · [Manifest phát hành](RELEASE_MANIFEST.json).

## Dùng mã và demo

Code, cấu hình, test, CSV phân tích nhẹ và nguồn báo cáo ở GitHub. Dữ liệu gốc, predictions và model nặng ở [Drive nhóm](https://drive.google.com/drive/folders/13KGqMT4NUr8JfvTpF0IEKfUDT0Dlvq5S). ZIP nguồn trong thư mục đợt 3 có metadata/metric 80 run, không chứa toàn bộ model/predictions.

Cài `requirements-repro.txt` và `requirements-analysis.txt`, đặt `PYTHONPATH=src`. Chạy `python -m unittest discover -s tests -v` và `python scripts/validate_protocol.py`. Gói demo đủ 16 bundle seed 42 được đồng bộ tại [05_Ket_qua_Thi_nghiem trên Drive](https://drive.google.com/drive/folders/1OTUR12qsUInUWIW6hxHzHO5bHtq-H8NL), tên `DEMO_NIDS_NHOM_20261025.zip` (bổ sung giao diện 26/10). Muốn dùng demo phải nhận đúng bundle; xem [hướng dẫn chung](../../START_HERE_NHOM.md).

S07 vẫn mới kiểm abstract; phần cứng và thời gian train-only lịch sử chưa có bằng chứng. Thành viên cần tự đọc, chạy, ghi góp ý và đóng góp thật. Các giới hạn này đã nêu trong PDF.

## SHA-256

- PDF: `b241f781a4a8c88b3ab63ae34f69d2fbdeedd82f802ffb0c7c3e61358e5f8ce7`
- ZIP nguồn: `3d6cd9985aa42f7b06e87e9da3af3309ff1ea0c9650ee0b22b2959b6129fe98b`

Các log ngày 13/10, 22–26/10 giữ đúng mốc lịch sử; audit mới nằm trong `final_20261030`. PDF đợt 1–2 giữ nguyên bản đã gửi. Việc đồng bộ không xác nhận thầy đã đọc hoặc nhóm đã nghiệm thu.
