# Cửa vào hồ sơ nhóm — cập nhật ngày 14/11/2026

Trang hồ sơ nằm tại [ho-so.html](../../../demo/presentation/ho-so.html), bên cạnh giao diện trình bày. Mở public: [nids-unsw-nb15-tlcn.nttin181.chatgpt.site/ho-so.html](https://nids-unsw-nb15-tlcn.nttin181.chatgpt.site/ho-so.html); dịch vụ có thể chuyển địa chỉ sang `/ho-so`.

**Trạng thái phát hành:** bản web cập nhật **v3 đã triển khai thành công ngày 14/11/2026**, theo [biên bản triển khai](evidence/DEPLOYMENT.json). Trang hồ sơ đã mở thực tế trên public; PDF tổng mở đủ 62 trang và tệp PDF đợt 4 tải về khớp SHA của bản 13/11. Bản public đã chạy mẫu CSV bằng RF tại hai ngưỡng 1% và 5%. Chưa xác nhận tải thành công mọi liên kết public hoặc luồng tải góp ý TXT public. [Bộ bàn giao 13/11](../review_final_20261113/README.md) giữ nguyên để đối chiếu.

**Trạng thái nộp:** đợt 3 đã gửi ngày 12/11 theo [hồ sơ bản gửi](../submission_dot3_20261111/README.md). Báo cáo đợt 4 và tổng vẫn chờ ba thành viên đọc, góp ý và duyệt riêng; **chưa gửi giảng viên**. Cập nhật trang web không thay xác nhận nội dung hoặc phần đóng góp của từng người.

## Ba bước để nhóm tự xem và góp ý

1. Mở **Tài liệu**, chọn đúng PDF đợt 4, tổng, slide hoặc phiếu phân việc. Tên và mốc tài liệu vẫn là bản 13/11. Có thể mở [Drive bàn giao](https://drive.google.com/drive/folders/1d-m5b35FVvGU3AEuA8vx1c9btG5xznUl) khi cần gói đầy đủ và demo offline.
2. Mở **Phần từng người**, bấm tên của mình. Đọc đúng số trang PDF, mở nguồn mã và tự trả lời ba câu hỏi. Số trang là thứ tự trong trình xem PDF, không phải số ở chân trang. Khi tập báo cáo, dùng **Về trình bày** để trở lại bảy màn chính.
3. Mở **Cần chốt**, chọn tên người ghi, điền **tệp/trang · chỗ chưa ổn · đề xuất hoặc câu chưa hiểu**, rồi bấm **Tải góp ý · TXT**. Tự gửi tệp vừa tải vào Zalo nhóm. Nếu trình duyệt chặn tải hoặc không thấy tệp trong Downloads, sao chép nguyên góp ý vừa viết và tên người ghi để gửi vào Zalo; không dựa riêng vào dòng “Đã tạo tệp TXT”. Ghi đúng phần đã đọc; chưa hiểu thì nêu rõ để cùng giải thích.

Góp ý chỉ tồn tại ở trang đang mở cho tới khi người dùng tải TXT. Trang không có backend, không tự đồng bộ giữa các máy, không tự gửi tin và không đánh dấu đã duyệt. Nhóm cần tự gửi và tập hợp góp ý trước khi thống nhất bản nộp; tải TXT không phải bằng chứng đã nộp hoặc đã được giảng viên duyệt.

## Các tệp được nối từ trang hồ sơ

| Mở tài liệu gốc trong kho | Nội dung |
|---|---|
| [PDF đợt 4](../review_final_20261113/reports/NhomTLCN_dot4_BAN_NHAP_20261113.pdf) | 68 trang, chờ nhóm duyệt |
| [PDF tổng](../review_final_20261113/reports/NhomTLCN_tong_BAN_NHAP_20261113.pdf) | 62 trang, chờ nhóm duyệt |
| [Slide PDF dự phòng](../review_final_20261113/slides/NhomTLCN_slide_du_phong_20261113.pdf) | 9 trang, trình chiếu tĩnh |
| [Phiếu phân việc](../review_final_20261113/slides/NhomTLCN_phan_viec_on_nhom_20261113.pdf) | 2 trang, chỉ rõ phần đọc và câu hỏi |
| [Nguồn đợt 4](../review_final_20261113/reports/Nguon_dot4_BAN_NHAP_20261113.zip) / [nguồn tổng](../review_final_20261113/reports/Nguon_tong_BAN_NHAP_20261113.zip) | ZIP nguồn để chỉnh sửa và biên dịch riêng |
| [Đối chiếu yêu cầu ngày 14/11](../../management/DOI_CHIEU_YEU_CAU_20261114.md) | SP1–SP10, T1–T10, bằng chứng và phần còn mở |

Bản public của các tệp trên được phục vụ dưới `downloads/` cạnh trang hồ sơ. Các PDF/ZIP nguồn 13/11 giữ nguyên; tài liệu đối chiếu 14/11 được tách riêng. Không dùng ngày cập nhật giao diện làm ngày thực nghiệm, ngày gửi báo cáo hoặc ngày một thành viên thực hiện công việc.

## Gói offline cập nhật

[Script đóng gói ngày 14/11](../../../scripts/package_review_update_20261114.py) lấy toàn bộ web build cùng 16 model, trang hồ sơ và các PDF/ZIP nguồn 13/11; kiểm fingerprint, manifest và CRC trước khi tạo gói riêng. Gói có `README.md` hướng dẫn bằng tiếng Việt, `CHAY_DEMO.cmd` và trình phục vụ bằng thư viện chuẩn Python. Máy cần Python 3 cùng Chrome/Edge hiện hành, không cần pip; giải nén đầy đủ, chạy CMD rồi mở địa chỉ localhost thực tế in trong cửa sổ. Trang hồ sơ mở bằng cách thêm `ho-so.html` sau địa chỉ đó.

**Trạng thái Drive của gói cập nhật:** đã tải lên và tải lại [NIDS_CAP_NHAT_20261114.zip](https://drive.google.com/file/d/1SZlzTmU8x6I-h0NVQ2pZ_DvAreVQHdyK/view) trong [thư mục bàn giao của nhóm](https://drive.google.com/drive/folders/1d-m5b35FVvGU3AEuA8vx1c9btG5xznUl). Bản tải lại có **80.826.126 byte**, SHA-256 `2df248e72c62c5580ed2b677043fd9e3e632d047d0e374eb38efba63773acd81`; cả **54 tệp trong manifest** khớp hash và CRC ZIP đạt, theo [biên bản tải lại Drive](evidence/DRIVE_DOWNLOAD_CHECK.json). [Biên bản đóng gói](evidence/PACKAGE_CHECK.json) xác nhận đủ 16 model và giữ nguyên PDF/ZIP nguồn 13/11. Gói cũ được giữ nguyên; chưa tạo đường dẫn ZIP public trên website.

## Phạm vi kiểm ngày 14/11

[Tổng hợp kiểm mới ngày 14/11](evidence/VALIDATION_SUMMARY.json) ghi nhận **49 test Python đạt**, hợp đồng CSV/suy luận Node đạt và validator xác nhận **80 run duy nhất**. Ba kết quả này được tổng hợp từ đầu ra console của lượt thực hiện hiện tại; biên bản không phải bản chép đầy đủ log test. Các kiểm có tệp đối chiếu riêng nằm dưới đây.

- [Đối chiếu API local](evidence/API_AUDIT.json): 32 tổ hợp vận hành, **3.200 dự đoán**; nhãn dự đoán và ngưỡng khớp, sai số score nằm trong mức cho phép `1e-6`.
- [Đối chiếu bộ suy luận trình duyệt](evidence/BROWSER_PARITY.json): 16 model × 2 ngưỡng × 1.000 dòng = **32.000 dự đoán**, không lệch nhãn so với bản tham chiếu. Mẫu lấy từ official test, không phải traffic độc lập.
- [HTTP local và CSV](evidence/HUB_HTTP_CHECK.json): trang hồ sơ/PDF mở được, dữ liệu thiếu hợp lệ bị trả 400, ID có số 0 đầu được giữ và đường dẫn vượt thư mục bị trả 404.
- [Kiểm giao diện thực tế](evidence/LIVE_BROWSER_CHECK.json): bản local gồm bảy màn trình bày, ba tab hồ sơ và ba thành viên đã kiểm ở 1280 × 720 không tràn trang. Trên public đã mở ba tab, ba thành viên, PDF tổng 62 trang, slide 9 trang, phiếu phân việc 2 trang và PDF đợt 4 tải về khớp SHA. Mẫu RF chạy đúng tại hai ngưỡng; CSV có số hệ hex bị chặn. Không suy rộng một PDF tải thành công thành mọi tệp đều đã tải thành công.
- Gói cập nhật đã được tải lại từ Drive và đối chiếu hash; một bản cùng hash được giải nén và chạy offline AE với CSV 50 dòng; [kiểm HTTP của gói giải nén](evidence/OFFLINE_HTTP_CHECK.json) xác nhận bảy tài nguyên trả 200 và khớp hash. “Offline” ở đây là chạy từ gói local; chưa thử ngắt mạng vật lý. Tải TXT local đã mở kiểm UTF-8 đúng. **Tải TXT public chưa xác nhận toàn trình:** lượt tự động hóa trong trình duyệt Codex không nhận được tệp dù giao diện báo đã tạo; đường HTTP ngoài trình duyệt trả 403. Khi không thấy tệp, dùng cách sao chép góp ý vào Zalo ở bước 3.

Các phép kiểm kỹ thuật không thay việc từng thành viên đọc, giải thích phần mình và thử HDMI tại phòng học.

## Giới hạn và việc cần nhóm chốt

[Guide bàn giao](../../management/BAN_GIAO_BAO_VE_20261113.md) giữ phân công và hướng dẫn đọc chéo **Thu → Anh; Tín → Thu; Anh → Tín**. Cả ba cần tập một lượt trình bày, chạy demo và thử HDMI trên thiết bị thật trước buổi báo cáo.

Phần còn thiếu bằng chứng vẫn được khai báo: S07 mới đối chiếu abstract; T2 thiếu phần cứng train lịch sử; T9 thiếu thời gian train riêng và suy luận lịch sử. Không lấy phép đo sau để điền thay lịch sử. Dữ liệu demo lấy từ UNSW-NB15, chưa phải bộ traffic độc lập do nhóm thu; bản public suy luận từ model đã lưu, không huấn luyện lại hoặc chặn tấn công.

Biên bản kiểm của bản 13/11 chỉ chứng minh phạm vi đã ghi tại mốc đó; không tự xác nhận mã mới ngày 14/11. Biên bản triển khai v3 xác nhận phát hành web, không xác nhận nhóm duyệt hoặc hoàn tất toàn bộ nộp bài. Các giới hạn kiểm public còn lại được ghi riêng ở trên; bàn giao Drive đã có biên bản tải lại và đối chiếu.
