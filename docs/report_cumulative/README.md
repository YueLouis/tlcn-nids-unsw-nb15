# Nguồn báo cáo tích lũy

Đợt 1 giữ bản lịch sử. Đợt 2 hiện 37 trang, 419,315 byte; SHA-256 `edafd81b6d4373fdae40c3086569254130a3148840fd37e026acba93c8a7c0dd`; PDF bàn giao ở `../../output/pdf/NhomTLCN_TramAnh_VuongThu_TrongTin_dot2.pdf`.

Biên dịch bằng XeLaTeX/MiKTeX. Sao chép **toàn bộ thư mục này**, gồm các module `.tex`, `figures/` và `assets/`, sang thư mục build ngoài workspace. Từ thư mục sao chép, chạy bốn lượt:

```text
xelatex -interaction=nonstopmode -halt-on-error -no-shell-escape BAO_CAO_TLCN_TICH_LUY_DOT_02.tex
```

Đọc log để xử lý lỗi/tham chiếu; render từng trang trước khi thay PDF chính. Không chỉ sao chép tệp TeX chính: báo cáo dùng `model_mechanisms.tex`, `related_work_comparison.tex`, `rq3_two_targets.tex` và ba hình TikZ trong `figures/`. Các hình kết quả ở `assets/final_20261013/` sinh từ metric thật.

Log/test/audit gốc tại `../evidence/dot_02/final_20261013/`; bảng hai target tại `../reports/DOT_02_TWO_TARGETS.csv`; ghi chú thay đổi tại `../reports/DOT_02_CAP_NHAT_20261017.md`. Manifest `../evidence/dot_02/revision_20261017/RELEASE_MANIFEST.json` mô tả snapshot hiện tại, không chứng nhận commit mã lịch sử của các run.
