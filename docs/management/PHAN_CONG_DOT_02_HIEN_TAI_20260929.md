# PHÂN CÔNG ĐỢT 2 - TRẠNG THÁI VÀ VIỆC CẦN CHỐT

> Hồ sơ lịch sử tháng 9, giữ nguyên nội dung tại thời điểm lập. Trạng thái hiện tại: `docs/management/TIEN_DO_HIEN_TAI_20261013.md` (tính từ repo). Xác nhận nhóm mới ghi riêng, không điền chữ ký vào mẫu cũ.


**Ngày kiểm tra:** 29/09/2026  
**Đề tài:** So sánh supervised learning và anomaly detection cho NIDS trên UNSW-NB15 bằng LOACO  
**Mốc nội bộ đề xuất:** chốt review và bản PDF trước 07/10/2026; mốc gửi dự kiến 12/10/2026 theo kế hoạch nội bộ hiện có, chưa phải xác nhận mới từ giảng viên.  
**Phạm vi kiểm tra:** file trên máy và đầu nhánh GitHub. Chưa kiểm kê lại Drive hoặc xác minh quyền truy cập của hai thành viên; GitHub CLI chưa đăng nhập. Việc chưa có trong repo được ghi là chưa có bằng chứng bàn giao, không suy ra thành viên chưa làm trên máy riêng.

**Cập nhật bàn giao code 29/09:** bản đồng bộ này bổ sung source, test, manifest và các bảng kết quả vào repo; README hướng dẫn clone/cài môi trường riêng và chạy thử vào thư mục riêng. Câu `64 run` trong bản Markdown và trạng thái một seed trong nguồn LaTeX đã được sửa. Các mục nói về GitHub cũ hoặc câu chữ cũ bên dưới là kết quả kiểm tra trước lần đồng bộ; các việc review khoa học và xác nhận của thành viên vẫn còn mở.

## 1. Kết luận hiện tại

Phần kỹ thuật cốt lõi của đợt 2 đã có trên máy nhóm trưởng:

- Hai official split đã được đọc và fingerprint: train `175341 x 45`, test `82332 x 45`.
- Ma trận đã khóa đúng `4 scenario x 4 model x 5 seed = 80 run`.
- Có đủ `80/80` thư mục run và `320/320` artifact bắt buộc: `run.json`, `metrics.csv`, `predictions.csv`, `model_bundle.joblib`.
- Có bảng chi tiết 80 run, bảng mean/std 16 nhóm, manifest dữ liệu, data contract, checklist Gate 1/Gate 2 và PDF 15 trang.
- Kiểm tra bằng Python hệ thống ngày 29/09: `check_dot2_final.py` PASS, gồm 9/9 unit test, validator 80 run, manifest, bảng tổng hợp và PDF.
- Đọc metadata của cả 80 run: tất cả có trạng thái `completed`, khai báo đánh giá đủ `82332` dòng test; 16 nhóm scenario/model đều đủ seed `42, 52, 62, 72, 82`. Các run được ghi ngày 26/09; không chạy train lại trong lần kiểm tra này.
- Audit lại hai CSV cho kết quả khớp manifest, kể cả checksum; fingerprint dữ liệu khớp cả 80 run. Bảng 80 run khớp metric gốc ở target FPR 5%; tính lại mean/std từ bảng này khớp đủ 16 nhóm.
- Có prototype dòng lệnh và file demo 20 dòng. Bộ artifact run hiện khoảng `2.289 GB`; cần hướng dẫn tải đúng phần trên Drive để tái lập.

Các kiểm tra trên xác nhận file hiện có và tính nhất quán của số liệu. Chưa chạy tái lập trên máy Trâm Anh/Thu, chưa tính lại toàn bộ metric từ 80 file prediction và chưa thay thế review học thuật của nhóm.

Đợt 2 **chưa được đóng** vì còn thiếu phần nghiệm thu và bàn giao:

- Trước lần đồng bộ này, GitHub `main` ở commit `f5686f0`; phần source đợt 2 chưa được bàn giao. Sau đồng bộ, hai bạn cần xác nhận clone/cài/chạy được đúng commit mới.
- Gate 1 và Gate 2 chưa có nhận xét/chữ ký của ba thành viên.
- `docs/week_01/RELATED_WORK_MATRIX.csv` mới có header, chưa có ma trận related work thực tế.
- Chưa có artifact error analysis/RQ1-RQ3 chuyên sâu do thành viên review và ký xác nhận.
- PDF có dòng D2.9 ghi `PASS một seed`, không còn phù hợp với bằng chứng hiện tại là 5 seed; cần sửa nguồn rồi build lại.
- Bản Markdown và script tổng hợp còn câu `64 run` dù bảng thực tế là 80. PDF vẫn mô tả prediction chỉ có ở run cũ, và bảng kết quả chỉ in mean dù dẫn tới CSV có std.
- Nguồn đợt 2 chưa giữ lại đầy đủ chương đặt vấn đề/cơ sở lý thuyết của đợt 1. Bảng tiến độ chưa có tỷ lệ riêng từng việc và bảng cấu trúc artifact chưa giải thích từng cột/kiểu dữ liệu bằng dòng ví dụ như ghi chú góp ý yêu cầu.
- Test hiện tại bao phủ 9 trường hợp contract/split/threshold/role. Chưa có test trực tiếp chứng minh transformer không fit trên validation/test và adapter IF/AE có chiều score đúng; cần bổ sung đúng các hành vi còn thiếu.
- Hướng dẫn môi trường cũ phụ thuộc đường dẫn riêng và gặp lỗi thiếu `scikit-learn`. README hiện đã hướng dẫn tạo môi trường riêng với `requirements-repro.txt`; hai bạn cần kiểm chứng trên máy mình.

**Lưu ý với nhãn PASS cũ:** các checklist ngày 26/09 là bằng chứng lịch sử. Audit sâu ngày 29/09 phát hiện thiếu cách đếm duplicate và các điểm báo cáo cần sửa; không dùng nhãn PASS kỹ thuật cũ để kết luận toàn bộ hồ sơ sẵn sàng nộp.

## 2. Bảng kiểm D2

| Mã | Đầu ra | Trạng thái kiểm tra | Bằng chứng | Việc còn thiếu |
|---|---|---|---|---|
| D2.1 | Gate 1 được review | Technical PASS; người review `0/3` | `docs/protocol/GATE_1_CHECKLIST.md`, biên bản 01 | Ba người ghi nhận xét và kết luận PASS/FAIL |
| D2.2 | Manifest/fingerprint | PASS kỹ thuật | `artifacts/data/data_manifest.json` | Trâm Anh kiểm tra và ký |
| D2.3 | Audit schema/chất lượng/label/category | Có audit cơ bản; audit duplicate/overlap chưa đầy đủ | Manifest và chương dữ liệu | Bổ sung duplicate không có `id`, overlap chéo split và giới hạn diễn giải |
| D2.4 | Data contract/Gate 2 | Draft kỹ thuật PASS; người review `0/3` | `docs/evidence/dot_02/DATA_CONTRACT.md`, checklist Gate 2 | Trâm Anh và Thu review; cả nhóm chốt |
| D2.5 | Preprocessing chống leakage | Có code và test split; còn thiếu test transformer | `src/nids_benchmark/data.py`, `preprocessing.py`, tests | Tín bổ sung test fit/transform; Trâm Anh review schema |
| D2.6 | Mô tả 4 scenario | Có trong PDF và protocol | Báo cáo đợt 2, `RQ_TO_EVIDENCE.md` | Cả nhóm đọc và xác nhận diễn giải |
| D2.7 | 4 baseline và artifact | PASS: `80/80` run, `320/320` file | `results/runs/` | Không đưa file nặng lên GitHub; bàn giao Drive |
| D2.8 | Test có giải thích | PASS: `9/9` khi dùng Python hệ thống có dependencies | `tests/`, `check_dot2_final.py` | Chuẩn hóa hướng dẫn cài môi trường cho thành viên |
| D2.9 | Bảng kết quả 5 seed | PASS kỹ thuật; câu chữ trong PDF cần sửa | `DOT_02_METRICS_ALL_RUNS.csv`, `DOT_02_METRICS_MEAN_STD.csv` | Sửa `PASS một seed` thành kết quả 5 seed; Thu review metric/support |
| D2.10 | Ma trận tiến độ chi tiết | Có khung và bằng chứng | PDF, checklist D2 | Trâm Anh biên tập trạng thái cuối và cả nhóm review |

## 3. Phân công đề xuất áp dụng từ ngày 29/09

### Nguyễn Trọng Tín - tích hợp, GitHub và bản giao cuối

**Phải bàn giao:**

1. Tạo commit/PR chứa code, `requirements.txt`, tests, protocol, evidence và nguồn báo cáo; không commit dataset raw, `results/runs/`, model bundle, predictions hàng loạt hoặc thư mục build.
2. Xác minh quyền repo của hai bạn; chuẩn hóa môi trường và cập nhật README để thành viên mới có thể clone, tạo branch, cài dependencies, chạy test và một smoke test. Môi trường đã kiểm tra là Python 3.14.4, NumPy 2.4.6, pandas 3.0.3, scikit-learn 1.9.0, SciPy 1.17.1, XGBoost 3.4.1, joblib 1.5.3, PyYAML 6.0.3. Cung cấp phiên bản tái lập thay cho đường dẫn riêng của máy Tín.
3. Sửa câu `64 run` trong script sinh báo cáo; Trâm Anh biên tập nội dung nguồn PDF rồi Tín build và kiểm tra. Khi có test mới, cập nhật số test trong báo cáo/checker theo log thực tế, không giữ cứng `9/9`.
4. Điền phần tích hợp trong Gate 1/Gate 2; đối chiếu mọi con số trong PDF với CSV/JSON cụ thể.
5. Gửi cho hai bạn commit/branch nền để họ clone và làm việc trên branch riêng.
6. Bổ sung test kiểm tra preprocessor không fit trên validation/test và anomaly preprocessor chỉ fit Normal. Nâng kiểm tra registry để đối chiếu đúng 80 tổ hợp và không chấp nhận run `completed_smoke` làm full run.
7. Bàn giao link Drive trỏ đúng dataset/checksum, bảng metric nhẹ và model cần chạy demo; hai bạn xác nhận tải được. Bảo toàn 80 run gốc khi chạy lại: CLI hiện dùng cùng `run_id` cho smoke/full nên luôn đặt `--output-dir results/member_checks/<ten>` cho thử nghiệm của từng người.

**File/đầu ra:** `README.md`, `requirements*.txt`, test preprocessing, `scripts/check_dot2_final.py`, `scripts/build_dot2_report.py`, commit nền và PDF được build từ nguồn nhóm đã review.  
**Bằng chứng PASS:** URL commit/PR; hai bạn cài/chạy được; toàn bộ test PASS; validator `80/80`; final check PASS; PDF không còn mâu thuẫn số run/seed.

**Reviewer:** Trâm Anh review schema/data section; Thu review metric/evaluator; cả nhóm duyệt PDF.  
**Hạn đề xuất:** 30/09 cho PR nền; 05/10 cho PDF sửa; 07/10 cho bản khóa.

### Trịnh Trâm Anh - dữ liệu, related work và diễn giải học thuật

**Phải bàn giao:**

1. Review `data_manifest.json` và `DATA_CONTRACT.md`; lập bảng audit dễ đọc gồm nguồn, checksum, kích thước, dòng/cột, dtype, missing, infinity, label và attack category.
2. Kiểm tra và ghi rõ quy ước duplicate: full-row duplicate hiện là `0`, nhưng khi bỏ `id` có `67601` dòng train và `26387` dòng test trùng; feature-only duplicate lần lượt là `74301` và `28386`. Đây chưa tự động là leakage, nhưng phải được giải thích hoặc đưa vào limitation.
3. Kiểm tra hiện tượng `8541` dòng test có đúng 42 feature trùng một dòng train; số này đã được xác nhận bằng join đủ 42 cột, không chỉ hash. Phân tích thêm overlap với development train/validation thực tế của từng scenario. Giữ official split theo protocol; mọi phân tích loại trùng bổ sung phải được ghi rõ, không âm thầm đổi dữ liệu của 80 run.
4. Điền `docs/week_01/RELATED_WORK_MATRIX.csv` bằng 10-15 nguồn theo phân công nền; mỗi dòng ghi dataset, split, model, metric, kết quả, hạn chế và mức liên quan. Chỗ chưa xác minh ghi rõ, không điền số liệu suy đoán.
5. Review các đoạn diễn giải kết quả để không tuyên bố zero-day thực tế hoặc model tốt nhất từ một metric/seed.
6. Ghi nhận xét và ký Gate 1/Gate 2 sau khi đọc PDF, manifest và data contract.
7. Biên tập `docs/report_cumulative/BAO_CAO_TLCN_TICH_LUY_DOT_02.tex`: khôi phục nền tảng đợt 1 để đúng bản tích lũy; bổ sung tỷ lệ từng đầu việc theo tiêu chí đã kiểm tra, bảng cột/kiểu/ví dụ artifact; sửa `PASS một seed` và mô tả prediction cũ; đưa std và support cần thiết vào bảng. Nhận phần kỹ thuật từ Thu/Tín, sau đó giao nguồn cho Tín build để tránh hai người cùng sửa file.

**File/đầu ra đề xuất:** `docs/evidence/dot_02/REVIEW_DU_LIEU_TRAM_ANH.md`, báo cáo duplicate/overlap có script tái tạo, related-work matrix 10-15 nguồn, nguồn báo cáo tích lũy đã biên tập. Đây là file cần bàn giao, chưa được tạo trong lần kiểm tra này.  
**Bằng chứng PASS:** số liệu truy về hai CSV, quy ước duplicate rõ, nguồn trích dẫn kiểm chứng được, nhận xét trong checklist và xác nhận thực tế.  
**Reviewer:** Tín review schema/checksum; Thu review support lớp và cách diễn giải.  
**Hạn đề xuất:** 02/10 cho audit và các nguồn lõi; 04/10 cho related work + review chéo; 05/10 cho nguồn báo cáo tích lũy.

### Hoàng Văn Vương Thu - anomaly model, threshold, metric và error analysis

**Phải bàn giao:**

1. Review `IsolationForest` và `Autoencoder`: score direction, fit trên Normal development, threshold lấy từ Normal validation, không dùng official test để tuning.
2. Kiểm tra bảng `metrics.csv` và `DOT_02_METRICS_MEAN_STD.csv`: metric nào có threshold, support thực sự mang nghĩa gì, trường hợp `heldout_attack` ở closed-set vì sao là null/0. Hiện precision/recall/F1 ghi support=82332 là số mẫu đánh giá, không phải mẫu số riêng của precision/recall; thống nhất schema và bổ sung TP/FP/FN/TN hoặc mẫu số đúng để tránh diễn giải sai. `pr_auc` trong code dùng average precision; ghi rõ cách tính.
3. Từ kết quả có sẵn, tạo bảng mean/std ở cả target FPR 1% và 5%, kèm FPR thực tế trên test và support. Bảng tổng hợp hiện chỉ có target 5%; ở closed-set, FPR mean của RF khoảng 18.57%, XGBoost 18.71%, IF 6.15%, AE 9.16%. Target validation 5% không bảo đảm test FPR 5%; cần kiểm tra nguyên nhân, chưa đủ bằng chứng để kết luận chắc chắn do distribution shift.
4. Viết phân tích ban đầu phục vụ đợt 2: các lỗi FP/FN theo attack category và một số trường hợp điển hình, nhận xét kết quả closed-set/LOACO có giới hạn. Bảng phân tích sâu, toàn bộ PR curve/score distribution/feature importance cho RQ1-RQ3 là đầu việc tiếp nối, không biến thành yêu cầu phải hoàn tất toàn đề tài trước đợt 2.
5. Ghi nhận xét và ký Gate 1/Gate 2 sau khi đọc PDF, threshold spec và kết quả.
6. Bổ sung test cho score direction IF/AE, trường hợp subset rỗng và ý nghĩa support. Tái chạy đại diện một closed-set IF và AE trên máy Thu trong thư mục `results/member_checks/vuong-thu`, lưu môi trường và so với run gốc; chưa cần chạy lại toàn bộ 80 run.

**File/đầu ra đề xuất:** `docs/evidence/dot_02/REVIEW_MO_HINH_METRIC_THU.md`, script/bảng so sánh 1% và 5%, test evaluator/adapter, phần viết kỹ thuật giao Trâm Anh. Đây là file cần bàn giao, chưa được tạo trong lần kiểm tra này.  
**Bằng chứng PASS:** bảng sinh từ artifact, định nghĩa support đúng, test PASS, log chạy lại trên máy Thu, nhận xét có giới hạn và xác nhận checklist.  
**Reviewer:** Tín review interface và artifact; Trâm Anh review cách diễn giải và support.  
**Hạn đề xuất:** 03/10 cho review metric + anomaly; 05/10 cho error analysis.

## 4. Việc bắt buộc của cả nhóm

1. Tín gửi commit nền; Trâm Anh và Thu clone repo, cài `requirements.txt`, chạy test và báo lại commit/hash đã kiểm tra.
2. Cả ba đọc PDF đã sửa cùng các file nguồn; mỗi người ghi nhận xét hoặc ghi rõ `không có vấn đề`. Bản hiện tại 15 trang, số trang bản sửa có thể thay đổi.
3. Cả ba điền tên, ngày và kết luận vào `GATE_1_CHECKLIST.md` và `GATE_2_CHECKLIST.md`; không đánh dấu PASS chỉ dựa trên validator.
4. Sau review, Tín build PDF lần cuối; Trâm Anh kiểm tra dữ liệu/diễn giải; Thu kiểm tra metric/error analysis; cả nhóm chốt bản gửi.

## 5. Quy tắc GitHub sau khi đồng bộ

```text
main                  <- chỉ nhận PR đã review
work/tin-integration  <- Tín: code, pipeline, report build
work/tram-anh-data    <- Trâm Anh: audit, related work, data contract review
work/vuong-thu-eval   <- Thu: metric, threshold, anomaly, error analysis
```

Mỗi PR phải ghi file đã đổi, lệnh kiểm tra đã chạy, kết quả PASS/FAIL và người review. Dataset raw, model bundle, predictions theo record và artifact nặng tiếp tục lưu ở Drive; GitHub chỉ giữ code, config, protocol, tài liệu nguồn và bằng chứng nhẹ.

## 6. Tiêu chí đóng đợt 2

- [ ] PR nền đã được merge hoặc ít nhất cả hai thành viên clone được đúng commit.
- [ ] Audit dữ liệu, related work và data contract có người review.
- [ ] Phân tích kết quả ban đầu, bảng hai target FPR và giới hạn dữ liệu có bằng chứng CSV/JSON; các phần RQ1-RQ3 chuyên sâu còn lại được ghi vào kế hoạch nội bộ.
- [ ] D2.9 trong PDF ghi đúng kết quả 5 seed.
- [ ] Gate 1 có đủ 3 xác nhận; Gate 2 có đủ 3 xác nhận.
- [ ] Final check PASS trong môi trường có đủ dependencies.
- [ ] PDF cuối đã được cả ba đọc và thống nhất trước mốc gửi 12/10/2026.

## 7. Cách đọc tiến độ để không giao lại việc đã có

- Code bốn model và 80 bộ artifact đã có: Thu/Tín tiếp nhận, chạy kiểm chứng có chọn lọc, sửa lỗi nếu có và phân tích kết quả; không giao nhiệm vụ viết lại bốn model từ đầu.
- Audit cơ bản đã có: Trâm Anh tiếp nhận rồi bổ sung kiểm tra duplicate/overlap và nền học thuật, không bắt đầu lại việc tìm một bộ dữ liệu khác.
- Gate 1 là xác nhận protocol của nhóm; Gate 2 là xác nhận chất lượng dữ liệu/data contract. Trong repo hiện chưa có xác nhận nào được điền cho ba thành viên.
- Mỗi người tự commit phần thực sự đã làm/review trên tài khoản của mình. Việc code đang ở máy Tín không chứng minh ai đã viết từng phần; không gán lịch sử đóng góp khi chưa có bằng chứng.
