# Làm rõ mốc kiểm thử 42, 46 và phiên bản hiện tại

Ngày đối chiếu: 15/11/2026. Đây là ghi nhận bổ sung; không thay đổi log, ZIP, PDF hoặc thời gian của hồ sơ trước đây.

## Kết quả đối chiếu

- Trong 65 commit truy cập được từ bốn nhánh đã kiểm, số hàm kiểm thử được khai báo lần lượt thuộc các mức 0, 9, 17, 46, 49, 51 và 52. Không tìm thấy phiên bản đã commit có đúng 42 hàm. Đếm hàm trong mã nguồn không đồng nghĩa với số bài được thực thi thành công.
- Trên máy vẫn giữ `docs/evidence/dot_03/session_20261025/tests_completion.log` và `snapshot_tests.log`, có dòng `Ran 42 tests` và `OK`. Vì vậy không kết luận rằng chưa từng có lượt chạy 42 bài.
- `clean_handoff_verification.log` được giữ trên máy ghi ngày kiểm 25/10/2026, Python 3.14.4, scikit-learn 1.9.0, 42 bài và SHA-256 của hai ZIP tại thời điểm ấy. Các tệp `.log` này chưa có trong cây Git được đối chiếu.
- Hồ sơ `CLEAN_ENV_HANDOFF_AUDIT.json` ghi ngày 26/10/2026 tham chiếu SHA-256 của hai ZIP khác. `clean_snapshot_tests.log` ghi 46 bài đạt. Cùng tên gói ngày 25/10 không bảo đảm cùng nội dung qua các lượt đóng gói.
- Chưa đối chiếu được nguyên gói nguồn có đúng SHA-256 của lượt 42 bài với một commit cụ thể. Vì vậy mốc 42 là thông tin trong log lưu cục bộ; chưa phải kết quả có thể tái lập từ một phiên bản Git đã xác định.

## Cách ghi trong báo cáo tiếp theo

> Log lưu cục bộ của lượt kiểm ngày 25/10 ghi 42 bài đạt. Lịch sử Git hiện truy cập được chưa xác định đúng phiên bản nguồn tương ứng với lượt này. Hồ sơ kiểm môi trường ngày 26/10 ghi 46 bài cho gói có SHA-256 khác. Kết quả kiểm phiên bản hiện tại được trình bày riêng với commit, lệnh chạy và log của chính lượt đó.

Không đổi con số 42 thành 46 trong bản lịch sử, không dùng lượt kiểm hiện tại làm bằng chứng chạy ngày 25/10. Nếu không còn gói nguồn cũ, giữ giới hạn này trong bản giải trình thay vì dựng lại một nguồn mang ngày cũ.

## Dấu vết hai lượt đóng gói

| Lượt | Gói báo cáo | Gói demo |
|---|---|---|
| Log 25/10, 42 bài | `d8efcc0cab0ad1bb61bf911df692b2c2cd294c855b086ae96aec57ed4aa38c5a` | `95eb27f2af47a541bf8d678bce566f99bc3e96e5b8e923f32df8126f2010304b` |
| Audit 26/10, 46 bài | `20ddf5b59c01751ee6ae02c5826db2187c38e7443f7017c2e58fddab0022a5dd` | `a2bc06eef304ec32ffa73118c881cc7c5cc64eeead237739a67506516b7d703f` |

Các hash trên là SHA-256 của byte tệp ZIP, không phải Git commit hay Git blob ID.
