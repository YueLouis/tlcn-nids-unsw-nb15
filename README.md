# TLCN NIDS - UNSW-NB15

**Kho GitHub hiện tại:** `https://github.com/YueLouis/tlcn-nids-unsw-nb15`  
**Nhánh làm việc chuẩn:** `main`  
**Thư mục Drive của nhóm:** `https://drive.google.com/drive/folders/13KGqMT4NUr8JfvTpF0IEKfUDT0Dlvq5S?hl=vi`  
**Lưu ý lưu trữ:** GitHub giữ code, config và tài liệu nguồn; dataset, model, prediction và artifact nặng được giữ ở Drive dùng chung.

So sánh mô hình học có giám sát và phát hiện bất thường cho hệ thống phát hiện
xâm nhập mạng trên UNSW-NB15 bằng đánh giá leave-one-attack-class-out (LOACO).

## Phạm vi nghiên cứu

- Mô hình học có giám sát: Random Forest và XGBoost.
- Mô hình phát hiện bất thường: Isolation Forest và Autoencoder.
- Kịch bản: closed-set và ba vòng LOACO giữ lại lần lượt Reconnaissance, DoS,
  Exploits.
- Seed cố định: 42, 52, 62, 72, 82.
- Tổng ma trận chính: 4 kịch bản x 4 mô hình x 5 seed = 80 run.

Ba câu hỏi nghiên cứu chính và bằng chứng cần thu thập được mô tả tại
[`docs/protocol/RQ_TO_EVIDENCE.md`](docs/protocol/RQ_TO_EVIDENCE.md).

## Trạng thái

- Đã có hai tập train/test UNSW-NB15 thật, data manifest, checksum SHA-256 và
  báo cáo audit schema/nhãn.
- Pipeline end-to-end đã chạy được Random Forest, XGBoost, Isolation Forest và
  Autoencoder trên closed-set và cả ba kịch bản LOACO.
- Mỗi run sinh `run.json`, `metrics.csv`, `predictions.csv` và
  `model_bundle.joblib`; prototype local đã đọc CSV và trả về Normal/Attack kèm score.
- Đã có đủ 80 full run theo ma trận 4 scenario x 4 model x 5 seed, mỗi run có
  `run.json`, `metrics.csv`, `predictions.csv` và `model_bundle.joblib`. Bản tổng hợp
  mean/std đợt 2 nằm tại
  `docs/reports/BAO_CAO_TIEN_DO_DOT_02.md`.
- Cập nhật 17/10/2026: nhóm trưởng cho biết chưa chắc mức hiểu từng thành viên; cả nhóm dự kiến tự rà soát hai đợt ngày 18/10. Lời báo đồng ý trước đó được giữ làm lịch sử tại `docs/evidence/dot_02/final_20261013/XAC_NHAN_NHOM_20261013.md`, không chứng minh đã nghiệm thu nội dung. Xem [hướng dẫn rà soát](docs/management/HUONG_DAN_RA_SOAT_HAI_DOT_20261018.md).
- Bản hiện tại: `output/pdf/NhomTLCN_TramAnh_VuongThu_TrongTin_dot2.pdf` (37 trang, hiệu chỉnh toàn văn 17/10). Đã xem đủ trang và đối chiếu 384 số in; dữ liệu/80 run/320 artifact không đổi. Log 17 test đạt giữ mốc 13/10; không huấn luyện lại. [Nội dung thay đổi](docs/reports/DOT_02_CAP_NHAT_20261017.md) và [bảng hai target](docs/reports/DOT_02_TWO_TARGETS.csv).
- Kiểm trước gửi ngày 17/10: [phiếu kiểm cuối](docs/evidence/dot_02/final_20261013/KIEM_TRA_CUOI_DOT_2_20261017.md), [email nháp](docs/reports/EMAIL_GUI_THAY_DOT_2_20261017.md). Chưa gửi email nộp giảng viên.
- Đã đối chiếu đoạn nội dung của 12/13 nguồn (92,3%); S07 mới kiểm abstract, toàn văn và nghiệm thu toàn bài còn mở. Phân tích lỗi category ban đầu đã có cho 80 run; PR/score distribution, giải thích feature, độ nhạy overlap, demo và bộ cuối đề tài thuộc bước tiếp nối. Nhóm còn phải tự đọc, giải thích phương pháp/kết quả và kiểm lại mô tả đóng góp trước khi chốt nộp. Kiểm kỹ thuật không xác nhận mức hiểu của thành viên. Xem `docs/management/TIEN_DO_HIEN_TAI_20261013.md`.
- Kiểm bàn giao 14/10: Drive đủ 80 thư mục run duy nhất/320 artifact, SHA-256 khớp local; hai CSV raw, hai PDF và hồ sơ học tập đã đối chiếu. Các bản trùng đã chuyển vào thùng rác có thể khôi phục. Xem [trạng thái bàn giao](docs/evidence/dot_02/final_20261013/REMOTE_DELIVERY.md).

## Cấu trúc repository

```text
configs/                Cấu hình nghiên cứu đã version hóa
docs/management/        Phân công và tiến độ
docs/meetings/          Biên bản họp nhóm
docs/protocol/          Giao thức, schema và checklist các gate
docs/week_01/           Kế hoạch và đầu ra tuần 1
scripts/                Công cụ tạo/kiểm tra artifact
src/nids_benchmark/     Data, preprocessing, model adapters, evaluator và runner
tests/                  Kiểm thử chống sai protocol và data leakage
```

## Bắt đầu cho thành viên mới

Đọc [`docs/START_HERE_NHOM.md`](docs/START_HERE_NHOM.md) để lấy code, nhận dữ liệu và chọn nhánh riêng. Phân công chi tiết nằm ở [`docs/management/PHAN_CONG_DOT_02_HIEN_TAI_20260929.md`](docs/management/PHAN_CONG_DOT_02_HIEN_TAI_20260929.md).

## Quy tắc dữ liệu và bảo mật

- Không đưa dataset UNSW-NB15, model nặng, prediction theo từng record hoặc file
  chứa thông tin nhạy cảm lên GitHub.
- Không commit mật khẩu, token, API key, file `.env` hoặc thông tin đăng nhập.
- `label`, `attack_cat` và `id` không được dùng làm feature của mô hình.
- Official test chỉ dùng để đánh giá cuối; không dùng để fit preprocessing,
  chọn hyperparameter hoặc chọn threshold.

## Cài đặt và kiểm tra code

Môi trường thực nghiệm đã kiểm chứng: Python 3.14.4. Các phiên bản thư viện
được ghi trong `requirements-repro.txt`; `requirements.txt` giữ khoảng phiên bản
cho phát triển. Lệnh dưới đây dùng PowerShell trên Windows, không cần kích hoạt
môi trường bằng `Activate.ps1`.

```powershell
git clone https://github.com/YueLouis/tlcn-nids-unsw-nb15.git
cd tlcn-nids-unsw-nb15
git switch -c work/ten-cua-ban
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-repro.txt
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/validate_protocol.py
```

Unit test và validator chạy được ngay sau cài đặt, không cần dataset. Trên
Linux/macOS, dùng `.venv/bin/python` và `export PYTHONPATH=src` tương ứng.

## Chạy thí nghiệm

Nhận hai file từ Drive dùng chung, đối chiếu SHA-256 trong
[`artifacts/data/data_manifest.json`](artifacts/data/data_manifest.json), rồi đặt vào:

```text
data/raw/UNSW_NB15_training-set.csv
data/raw/UNSW_NB15_testing-set.csv
```

Chạy trong PowerShell tại thư mục repo:

```powershell
$env:PYTHONPATH = "src"

# Audit dữ liệu thật và ghi manifest/checksum.
.\.venv\Scripts\python.exe scripts/audit_data.py

# Chạy thử trong thư mục riêng, bảo toàn kết quả gốc.
.\.venv\Scripts\python.exe scripts/run_experiment.py `
  --scenario closed_set --model random_forest --seed 42 `
  --max-development-rows 20000 --max-test-rows 10000 `
  --output-dir results/member_checks/local

# Run đầy đủ: không dùng hai tham số --max-... .
.\.venv\Scripts\python.exe scripts/run_experiment.py `
  --scenario loaco_reconnaissance --model xgboost --seed 42 `
  --output-dir results/member_checks/local

# Prototype dự đoán CSV bằng model vừa chạy hoặc nhận từ Drive.
.\.venv\Scripts\python.exe scripts/predict_csv.py `
  --bundle results/member_checks/local/CS-RF-S42/model_bundle.joblib `
  --input duong_dan_flow.csv --output predictions_demo.csv
```

Các lần chạy cùng scenario/model/seed dùng chung mã run và sẽ ghi cùng thư mục.
Mỗi thành viên thay `local` bằng tên mình; dùng thư mục mới khi muốn giữ nhiều lần
thử. Không chạy smoke vào `results/runs/` chứa 80 run chuẩn.

## Đối chiếu toàn bộ hồ sơ đợt 2

Chỉ chạy bước này sau khi đã nhận đủ `results/runs/` và bản PDF từ Drive,
hoặc tự tái tạo chúng. Bản PDF đặt tại
`output/pdf/NhomTLCN_TramAnh_VuongThu_TrongTin_dot2.pdf`.

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe scripts/check_dot2_final.py
```

Các test kiểm tra cột cấm, chuẩn hóa nhãn, LOACO leakage, threshold theo
FPR, UADR và vai trò đánh giá. Validator protocol kiểm tra ma trận 80 run.
Gate 1 vẫn là bước review của cả nhóm, không được tự động đánh dấu PASS.

## Thành viên

- Nguyễn Trọng Tín - nhóm trưởng, repository, preprocessing, RF/XGBoost và tích hợp.
- Trịnh Trâm Anh - dữ liệu, tổng quan NIDS, related work và biên tập báo cáo.
- Hoàng Văn Vương Thu - Isolation Forest, Autoencoder, threshold, metric và error analysis.
