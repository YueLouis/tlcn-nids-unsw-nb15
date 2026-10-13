# Nguồn báo cáo tích lũy

Đợt 1 giữ bản lịch sử; đợt 2 cập nhật từ nền đợt 1. PDF nộp: `../../output/pdf/NhomTLCN_TramAnh_VuongThu_TrongTin_dot2.pdf` (30 trang).

Biên dịch với XeLaTeX/MiKTeX. Để tránh aux/toc cũ và không làm bẩn workspace, chép file `.tex` cùng `assets/` vào một thư mục build ngoài workspace, chạy XeLaTeX 4 lượt ở thư mục đó: `xelatex -interaction=nonstopmode -halt-on-error -no-shell-escape BAO_CAO_TLCN_TICH_LUY_DOT_02.tex`. Kiểm tra log, render PDF và đối chiếu trước khi cập nhật bản chính.

Hình kết quả ở `assets/final_20261013/` lấy từ metric thật. Log, metadata và audit prediction ở `../evidence/dot_02/final_20261013/`. Không dùng các script dựng thẻ PASS cũ làm bằng chứng terminal.
