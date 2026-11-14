# Đối chiếu yêu cầu với bộ bàn giao ngày 13/11

Ngày lập bảng: **14/11/2026**. Bảng này nối mã SP/T trong [bản đối chiếu ngày 25/10](../evidence/dot_03/session_20261025/DOI_CHIEU_YEU_CAU.json) sang tài liệu đang dùng. Đây là bảng theo dõi đầu ra của nhóm, không phải rubric mới hoặc xác nhận nghiệm thu của giảng viên. Không sửa bảng đối chiếu cũ, kết quả thực nghiệm hoặc lịch sử đã nộp.

**Trạng thái nộp:** đợt 3 đã gửi ngày 12/11 theo [hồ sơ bản gửi](../releases/submission_dot3_20261111/README.md). Đợt 4 và tổng trong [bộ bàn giao 13/11](../releases/review_final_20261113/README.md) là bản chờ nhóm đọc duyệt, chưa gửi giảng viên. Chưa có xác nhận mới của ba thành viên trong bảng này.

## Cách đọc trạng thái

- **Có đầu ra và biên bản kỹ thuật:** đã có tệp/nguồn cùng phép kiểm được ghi trong biên bản. Mốc kiểm đi theo biên bản; không tự xác nhận mã đã đổi sau đó.
- **Một phần, thiếu bằng chứng:** phần có nguồn được nêu riêng với phần chưa có. Không dùng số đo mới để điền giả log lịch sử.
- **Chờ nhóm đọc duyệt:** cần người được phân công thực sự mở, kiểm, giải thích và ghi góp ý. Trạng thái này áp dụng cho mọi SP/T bên dưới, kể cả khi kiểm kỹ thuật đạt.

Đợt 4 có **68 trang**, tổng có **62 trang**, slide PDF có **9 trang**, phiếu phân việc có **2 trang**. Xem [biên bản biên dịch nguồn từ ZIP](../releases/review_final_20261113/evidence/CLEAN_COMPILE_CHECK.json), [kiểm bảng đợt 4](../releases/review_final_20261113/reports/dot4_REPORT_TABLE_CHECK.json), [kiểm bảng tổng](../releases/review_final_20261113/reports/tong_REPORT_TABLE_CHECK.json) và [kiểm slide/phiếu](../releases/review_final_20261113/slides/SLIDES_CHECK.json). Đây là kết quả kiểm của bản 13/11, không phải một lượt chạy kiểm mã mới ngày 14/11.

## Sản phẩm SP1–SP10

| Mã | Đầu ra cần có | Tệp hoặc bằng chứng đang dùng | Trạng thái kỹ thuật và phần cần làm tiếp |
|---|---|---|---|
| SP1 | Báo cáo đợt 3, đợt 4 và tổng | [Đợt 3 đã gửi](../releases/submission_dot3_20261111/README.md); [PDF đợt 4](../releases/review_final_20261113/reports/NhomTLCN_dot4_BAN_NHAP_20261113.pdf); [PDF tổng](../releases/review_final_20261113/reports/NhomTLCN_tong_BAN_NHAP_20261113.pdf) | Nguồn hai bản mới đã biên dịch độc lập và đối chiếu PDF. Cả ba đọc chéo đợt 4/tổng rồi chọn đúng phiên bản nộp; không thay PDF đợt 3 đã gửi |
| SP2 | Mã có cấu trúc và hướng dẫn chạy | [README](../../README.md); [mã thư viện](../../src/nids_benchmark/); [script](../../scripts/); [kiểm thử](../../tests/); [môi trường tái lập](../../requirements-repro.txt) | Có mã và hướng dẫn. Kiểm mã phải theo phiên bản thực sự đang dùng; không lấy số test cũ làm kết quả cho thay đổi mới |
| SP3 | Inventory, fingerprint và audit dữ liệu | [Manifest](../../artifacts/data/data_manifest.json); [data contract](../evidence/dot_02/DATA_CONTRACT.md); Chương dữ liệu trong PDF mới | Có số dòng/cột, nhãn, checksum và giới hạn overlap. Anh tự mở nguồn, kiểm ý nghĩa 42 feature và phép chia tập |
| SP4 | Preprocessor đã lưu cùng model | [Manifest 16 model cho trình duyệt](../releases/review_final_20261113/evidence/BROWSER_MODEL_MANIFEST.json); [hướng dẫn nhận dữ liệu/model gốc](../../README.md#chạy-thí-nghiệm) | Tham số phục vụ demo đã xuất; bundle Python gốc và dữ liệu nặng lấy từ Drive, không nằm trong bản clone này. Bản public seed 42 không thay toàn bộ 80 bundle nghiên cứu |
| SP5 | Bốn model/cấu hình, đủ 80 run | [Cấu hình](../../configs/experiment_matrix.yaml); [ma trận 80 run](../protocol/RUN_MATRIX.csv); [audit chẩn đoán](../evidence/dot_03/final_diagnostics_20261025/FINAL_DIAGNOSTICS_AUDIT.json) | Có ma trận và bằng chứng kiểm artifact của lần chạy đã khóa. Không chạy lại hoặc sửa ngày 80 run để khớp ngày biên tập; file nặng nhận từ Drive |
| SP6 | Closed-set và ba LOACO, năm seed | [Điểm vận hành từng run](../evidence/dot_03/pr_scores_20261022/OPERATING_POINTS_ALL_RUNS.csv); [AP mean/std](../evidence/dot_03/pr_scores_20261022/AP_MEAN_STD.csv); [ba RQ](../protocol/RQ_TO_EVIDENCE.md) | Có bảng theo scenario/model/seed và hai target. Nhóm giải thích năm seed dùng cùng official test, không phải năm dataset độc lập |
| SP7 | Bảng/hình sinh từ artifact đã khóa | [Audit chẩn đoán](../evidence/dot_03/final_diagnostics_20261025/FINAL_DIAGNOSTICS_AUDIT.json); [script tạo chương](../../scripts/prepare_final_diagnostic_chapter.py); hai biên bản kiểm bảng ở đầu trang | Có truy vết bảng/hình. Đọc từng kết luận với support, scope, target và nguồn; không coi render hoặc checksum là duyệt nội dung |
| SP8 | Prototype có so sánh và giải thích | [Prototype local](../../demo/index.html); [mã suy luận Python](../../src/nids_benchmark/demo.py); [giao diện trình bày](../../demo/presentation/); [hướng dẫn demo](BAN_GIAO_BAO_VE_20261113.md#kịch-bản-demo-dễ-giải-thích) | Có prototype local so bốn model và màn trình bày chọn một model mỗi lần. Biên bản public/API của bản 13/11 ở bộ bàn giao; nhóm cần tự chạy, đọc score/ngưỡng và nêu giới hạn |
| SP9 | Slide và câu hỏi phản biện | [Slide PDF](../releases/review_final_20261113/slides/NhomTLCN_slide_du_phong_20261113.pdf); [phiếu phân việc](../releases/review_final_20261113/slides/NhomTLCN_phan_viec_on_nhom_20261113.pdf); [câu hỏi tự trả lời](BAN_GIAO_BAO_VE_20261113.md#câu-hỏi-phải-tự-trả-lời-trước-buổi-báo-cáo) | Tệp đã chuẩn bị, chưa thay buổi tập nói và hỏi đáp thật. PDF là phương án tĩnh, không chạy suy luận CSV |
| SP10 | Kịch bản demo, nguồn dữ liệu, bản đồ mã và tự nhận xét | [Lab local](../../demo/lab.html); [danh mục case](../../demo/cases/catalog.json); [mã ứng dụng](../../src/nids_benchmark/application.py); [báo cáo ứng dụng](../application_20261026/report.html); [mẫu góp ý](BAN_GIAO_BAO_VE_20261113.md#cách-ghi-góp-ý-và-chốt) | Có phần minh họa và mẫu để nhóm nhận xét. Case lấy từ UNSW-NB15; chưa có traffic độc lập, live capture, online learning hay cơ chế chặn tấn công |

## Bảng T1–T10

Các bảng dưới đây được đọc trong PDF tổng/đợt 4 cùng CSV nguồn. Tên tệp dữ liệu năm 2026 phản ánh ngày tạo phân tích, không biến ngày đó thành lần train mới.

| Mã | Nội dung | Nguồn đối chiếu | Trạng thái kỹ thuật / giới hạn |
|---|---|---|---|
| T1 | Support Normal và 9 category | [Manifest dữ liệu](../../artifacts/data/data_manifest.json) | Có support train/test; phân biệt số dòng và số vector feature duy nhất |
| T2 | Phần cứng, thư viện, seed, phiên bản feature | [Môi trường tái lập](../../requirements-repro.txt); [cấu hình](../../configs/experiment_matrix.yaml); [phần cứng phép đo sau](../evidence/dot_03/final_diagnostics_20261025/HARDWARE_CURRENT.json) | **Một phần:** có cấu hình, seed và phiên bản thư viện; thiếu bằng chứng phần cứng khi train 80 run lịch sử. Máy đo suy luận sau không thay phần cứng train |
| T3 | Cấu hình bốn model | [Cấu hình thí nghiệm](../../configs/experiment_matrix.yaml); [model adapters](../../src/nids_benchmark/models.py) | Có cấu hình; giải thích thư viện được dùng và phần tích hợp của pipeline |
| T4 | Closed-set P/R/F1/FPR/AP | [Điểm vận hành mean/std](../evidence/dot_03/pr_scores_20261022/OPERATING_POINTS_MEAN_STD.csv); [AP mean/std](../evidence/dot_03/pr_scores_20261022/AP_MEAN_STD.csv) | Có bảng hai target; AP không phải metric tại một threshold; nêu FPR test thực tế |
| T5 | LOACO Reconnaissance, hai target | [Điểm vận hành mean/std](../evidence/dot_03/pr_scores_20261022/OPERATING_POINTS_MEAN_STD.csv) | Có Known Recall/UADR/FPR và sample std qua năm seed; held-out chỉ thuộc phạm vi benchmark |
| T6 | LOACO DoS, hai target | [Điểm vận hành mean/std](../evidence/dot_03/pr_scores_20261022/OPERATING_POINTS_MEAN_STD.csv) | Có bảng cùng định nghĩa/scope; không suy ra phát hiện mọi DoS thực tế |
| T7 | LOACO Exploits, hai target | [Điểm vận hành mean/std](../evidence/dot_03/pr_scores_20261022/OPERATING_POINTS_MEAN_STD.csv) | Có bảng cùng định nghĩa/scope; kiểm support held-out và known riêng |
| T8 | Detection theo attack category | [Category mean/std](../evidence/dot_02/category_errors_20261014/CATEGORY_ERRORS_MEAN_STD.csv); [heatmap](../evidence/dot_03/final_diagnostics_20261025/CATEGORY_DETECTION_HEATMAP.png) | Có detection = 1 − FN/support Attack; không gọi binary prediction là tên attack category |
| T9 | Thời gian train/suy luận và kích thước | [Từng run](../evidence/dot_03/final_diagnostics_20261025/RUNTIME_SIZE_ALL_RUNS.csv); [mean/std](../evidence/dot_03/final_diagnostics_20261025/RUNTIME_SIZE_MEAN_STD.csv) | **Một phần:** có tổng thời gian run, kích thước bundle và phép đo transform+score sau trên 80 bundle. Thiếu train-only và thời gian suy luận lịch sử; không gọi tổng run là train time hoặc phép đo sau là latency vận hành |
| T10 | Lỗi theo role/category/proto/service/state | [Category từng run](../evidence/dot_02/category_errors_20261014/CATEGORY_ERRORS_ALL_RUNS.csv); [lỗi theo nhóm](../evidence/dot_03/final_diagnostics_20261025/GROUP_ERRORS_ALL_RUNS.csv); [ví dụ gần ngưỡng](../evidence/dot_03/final_diagnostics_20261025/NEAR_THRESHOLD_EXAMPLES_S42.csv) | Có mẫu số theo role/nhóm và quy tắc chọn ví dụ. Tương quan và importance không chứng minh nguyên nhân lỗi |

Các hình H1–H8 và chi tiết prototype P1–P5 vẫn truy vết theo bảng gốc 25/10; bản PDF mới giữ phân tích kế thừa và bổ sung trình bày. Phạm vi ba RQ vẫn theo [RQ_TO_EVIDENCE](../protocol/RQ_TO_EVIDENCE.md), chưa mở thêm RQ mới.

## Những phần chưa được tự đánh dấu hoàn thành

| Phần còn mở | Căn cứ và hành động tiếp theo |
|---|---|
| Đọc chéo, hiểu bài và đóng góp của từng người | [Guide phân việc](BAN_GIAO_BAO_VE_20261113.md#mỗi-người-phụ-trách-phần-nào) cùng mẫu góp ý; chỉ ghi người/ngày/nội dung thật sau khi thực hiện. Không ký hoặc viết nhận xét thay thành viên |
| Duyệt nộp đợt 4/tổng | Chốt đúng phiên bản PDF sau khi cả ba đọc và góp ý. Chưa có duyệt mới hoặc email nộp trong bảng này; duyệt đợt 3 không tự áp dụng cho hai bản tiếp theo |
| S07 toàn văn | [Tài liệu nền](../references/README.md) ghi chỉ đối chiếu abstract. Có thể tiếp tục tìm bản hợp pháp và kiểm đúng đoạn; chưa có thì giữ giới hạn, không tự thêm số đo/split/cấu hình từ toàn văn chưa đọc |
| T2/T9 lịch sử | Giữ các ô thiếu bằng chứng. Nếu cần phép đo mới, lập mục thí nghiệm riêng và ghi đúng ngày/môi trường; không gán lại cho 80 run gốc |
| Dữ liệu ngoài và đánh giá vận hành | Demo CSV không tự trở thành dataset độc lập. Thu traffic, trích feature tương thích, gán nhãn và đánh giá ngoài benchmark là hướng tiếp nối cần kế hoạch riêng |
| Tập nói, HDMI và demo dự phòng | Dùng [HDMI và màn hình lớp](BAN_GIAO_BAO_VE_20261113.md#hdmi-và-màn-hình-lớp) và kịch bản tập trong guide; kiểm UI ở máy không thay thử thiết bị lớp |
| Thông báo lịch chính thức | [Gantt](GANTT_CHART.md) là baseline gốc; các ghi nhận ngày truyền miệng cũ không thay thông báo của khoa/giảng viên. Lưu thông báo được nhóm cung cấp để chốt lịch nộp/báo cáo |

## Bản nào đã được kiểm trên Drive

[Biên bản tải lại Drive ngày 13/11](../releases/review_final_20261113/evidence/DRIVE_DOWNLOAD_CHECK.json) ghi gói `NIDS_BAN_GIAO_20261113.zip` phiên bản 2 khớp bản ở máy, 30 tệp trong manifest khớp kích thước/SHA-256, ZIP chính và ZIP offline không lỗi CRC. Đây là phép kiểm nội dung đã tải, không phải xác nhận nhóm hoặc giảng viên duyệt. Tài liệu đối chiếu ngày 14/11 này chưa được dùng để thay hoặc đóng gói lại bản 13/11.
