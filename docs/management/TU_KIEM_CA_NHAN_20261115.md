# Phần tự kiểm của từng thành viên

Hướng dẫn ngày 15/11/2026. Ba tệp đầu ra dưới đây vẫn cần người được phân công trực tiếp thực hiện; hướng dẫn không xác nhận đã hoàn thành. Mỗi bạn bắt đầu từ một việc nhỏ, ghi phần mình hiểu và điều còn cần hỏi.

Mở [hồ sơ online](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/ho-so), chọn **Phần từng người → tên mình → Việc tự kiểm**. [Bộ Drive hiện hành](https://drive.google.com/drive/folders/1s5d-14RMFRqoWnEDMVtRtUSsrUeguP_z) giữ tài liệu chung; các thư mục cá nhân vẫn dùng theo phân công tại [chỉ mục bốn phần](../group_delivery_20261110/README.md).

## Trâm Anh — dữ liệu

1. Mở [DU_LIEU_MANIFEST.json](../group_delivery_20261110/TramAnh/DU_LIEU_MANIFEST.json). Tìm số dòng và danh sách cột của hai tập, ghi key và số thực tế nhìn thấy.
2. Đối chiếu `id`, `label`, `attack_cat` với `FORBIDDEN_FEATURES` trong [contracts.py](../../src/nids_benchmark/contracts.py) và cách chia tập ở [data.py](../../src/nids_benchmark/data.py). Giải thích vì sao giữ nhãn để chấm nhưng bỏ khỏi feature.
3. Mở [DUPLICATE_OVERLAP.json](../group_delivery_20261110/TramAnh/DUPLICATE_OVERLAP.json), chọn một phép đếm và đối chiếu [audit_duplicate_overlap.py](../../scripts/audit_duplicate_overlap.py). Xác định đang so cả hàng hay chỉ vector đặc trưng; nêu một giới hạn.

Tự viết `docs/evidence/dot_03/member_work/tram_anh/ANH_DU_LIEU_VA_GIOI_HAN.md`. Đính kèm tên tệp, key/dòng đã kiểm và cách hiểu của mình. Thu đọc chéo phần này; Anh đọc phần Tín.

## Vương Thu — kết quả

1. Mở [HAI_NGUONG_FPR.csv](../group_delivery_20261110/VuongThu/HAI_NGUONG_FPR.csv), tìm hai dòng CS–RF ở target 1% và 5%. Ghi đúng `recall_mean`, `fpr_mean`, tiêu đề cột và đơn vị; đây là trung bình 5 seed.
2. Mở [NGUON_VI_DU_THU.csv](../group_delivery_20261110/VuongThu/NGUON_VI_DU_THU.csv), chọn ID 68699 hoặc 975 thuộc LR–RF–S42, target 5%. Ghi kịch bản, model, seed, target, nhãn thật, score, threshold và dự đoán. Hai ID này dùng trong CSV nguồn, không có trong preset web; phạm vi LR khác bảng CS nhiều seed phía trên.
3. Đối chiếu [evaluation.py](../../src/nids_benchmark/evaluation.py), giải thích đánh đổi báo nhầm/bỏ sót bằng số vừa kiểm và vì sao target validation không bảo đảm FPR test giống hệt.

Tự viết `docs/evidence/dot_03/member_work/vuong_thu/THU_PHAN_TICH_KET_QUA.md`. Giữ dòng nguồn đã dùng và điều chưa hiểu. Tín đọc chéo phần này; Thu đọc phần Anh.

## Trọng Tín — demo

1. Mở [web trình bày](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/), bấm **Demo → 1 · Chọn dữ liệu**: **Chỉ Normal · xem báo động nhầm**, **CS**, **RF**, target **5%**. Bấm **Chạy suy luận**, xem bản ghi **#1** ở bước 2. Ô vị trí là thứ tự hàng, không phải ô nhập ID.
2. Tải CSV, giữ ảnh lượt vừa chạy và ghi giờ thực hiện. Giữ nguyên dữ liệu, CS và RF; đổi target **1%**, chạy lại rồi tải CSV thứ hai. Đặt tên hai tệp theo target để tránh nhầm.
3. Ghi score, threshold và dự đoán ở hai lượt, đối chiếu [VI_DU_HAI_NGUONG.csv](../group_delivery_20261110/TrongTin/VI_DU_HAI_NGUONG.csv). Giải thích thành phần nào đổi; vì sao đây là suy luận từ model đã lưu, chưa phải huấn luyện mới hoặc dữ liệu mạng độc lập.

Tự viết `docs/evidence/dot_03/member_work/trong_tin/TIN_NHAT_KY_TAI_LAP.md`, kèm hai CSV và ảnh mới. Anh đọc chéo phần này; Tín đọc phần Thu.

## Lưu việc đã làm

- Ghi ngày thực hiện thật, đầu vào/nguồn, kết quả đối chiếu, giải thích của mình, mức hỗ trợ đã nhận và câu còn vướng. Không dùng ảnh cũ hoặc ghi đã đọc thay người khác.
- Mỗi người dùng tài khoản của mình lưu phần tự thực hiện lên nhánh `tramanh`, `vuongthu` hoặc `trongtin` và thư mục Drive cá nhân; gửi liên kết vào Zalo nhóm. `main` giữ bản tổng hợp.
- Đọc chéo phải chỉ được ít nhất một câu hoặc số liệu đã đối chiếu, ghi nhận xét cụ thể. Bấm sao chép/tải TXT góp ý trên web không tự tạo tệp tự kiểm hoặc hoàn tất phần cá nhân.

Tài liệu này do trợ lý chuẩn bị theo yêu cầu của nhóm trưởng. Báo cáo đợt 4 và tổng đã có nội dung để sử dụng; email chưa gửi. Công việc và nhận xét thật được bổ sung đúng ngày người thực hiện làm xong.

## Đưa phần tự làm lên GitHub và Drive

1. Mở GitHub, bấm ảnh đại diện kiểm đúng tài khoản: Anh là `tta2405`, Thu là `hoangvvthu`, Tín là `YueLouis`. Nếu khác, đổi tài khoản trước khi lưu. Không sửa tên/email commit để nhận phần của người khác.
2. Mở [repository nhóm](https://github.com/YueLouis/tlcn-nids-unsw-nb15), chọn nhánh của mình ở nút đang ghi `main`: Anh chọn `tramanh`, Thu chọn `vuongthu`, Tín chọn `trongtin`.
3. Ở trang gốc repository, chọn **Add file → Create new file**. Dán nguyên đường dẫn tệp đầu ra của mình được ghi ở trên vào ô tên tệp. Nếu tệp đã có, mở tệp rồi bấm biểu tượng bút để sửa thay vì tạo trùng.
4. Viết điều chính mình vừa kiểm. Bấm **Commit changes**, ghi ngắn việc đã làm, chọn lưu vào đúng nhánh cá nhân đang mở. Kiểm lại trang tệp và tên tài khoản trong commit sau khi lưu. Nếu báo không có quyền, gửi ảnh lỗi vào nhóm, đừng lưu sang nhánh người khác.
5. Với CSV/ảnh của lượt kiểm, ở đúng thư mục cá nhân chọn **Add file → Upload files**, tải các tệp nhỏ liên quan và ghi chú nguồn. Không tải dataset, model nặng hoặc thông tin đăng nhập lên GitHub.
6. Lưu cùng bản `.md` và tệp kèm vào Drive cá nhân đã dẫn tại [chỉ mục bốn phần](../group_delivery_20261110/README.md): kiểm tài khoản góc trên, mở đúng thư mục, chọn **Mới → Tải tệp lên**. Mở lại tệp vừa tải để chắc đúng bản.
7. Gửi liên kết GitHub của tệp/commit và liên kết Drive vào Zalo nhóm, nhờ người đọc chéo góp ý một chỗ cụ thể. Nhóm tổng hợp qua pull request vào `main` sau khi đọc; việc tạo commit không tự xác nhận đã được đọc hoặc duyệt.
