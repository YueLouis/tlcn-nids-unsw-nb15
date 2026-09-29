# Báo cáo tiến độ tiểu luận chuyên ngành - Đợt 2

**Trạng thái:** Bản tích lũy kỹ thuật ngày 26/09/2026; đã chạy đủ 80 run theo protocol.

## 1. Kết luận ngắn

Pipeline đã đọc đúng hai official split UNSW-NB15 (175,341 dòng train, 82,332 dòng test), vượt qua 9/9 unit test và tạo đủ 80 artifact run cho 4 scenario x 4 model x 5 seed. Mỗi run có run.json, metrics.csv, predictions.csv và model_bundle.joblib; mean/std đã được tổng hợp riêng. Gate 1/Gate 2 vẫn cần review người.

## 2. Audit dữ liệu

| Split | Dòng | Cột | Duplicate | Missing | Label 0 | Label 1 | SHA-256 |
|---|---:|---:|---:|---:|---:|---:|---|
| train | 175,341 | 45 | 0 | 0 | 56,000 | 119,341 | `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa` |
| test | 82,332 | 45 | 0 | 0 | 37,000 | 45,332 | `734fe6642edf758f7c94d7d9149426b49d202fe8e7bf0bef47392489c3c0a559` |

Artifact đầy đủ: `artifacts/data/data_manifest.json`.

## 3. Protocol và kiểm thử

- Cột metadata bị loại khỏi feature: `id`, `label`, `attack_cat`.
- Preprocessing fit trên development; LOACO loại held-out class trước split/fit.
- Threshold lấy từ Normal validation tại FPR mục tiêu 1% và 5%; official test chỉ dùng đánh giá.
- `python -m unittest discover -s tests -v`: **9/9 PASS**.
- `python scripts/validate_protocol.py`: **80 run_id hợp lệ** trong ma trận protocol.

## 4. Bảng kết quả chi tiết theo run

Bảng dưới đây dùng threshold mục tiêu FPR 5%. `pr_auc` không phụ thuộc threshold; `normal:fpr`, `known_attack:recall` và `heldout_attack:uadr` có support trong `metrics.csv`. Bảng mean/std qua 5 seed nằm ở phần tiếp theo.

| run_id | scenario | model | seed | status | official_test_rows | artifact_dir | all:f1 | all:precision | all:recall | heldout_attack:uadr | known_attack:recall | normal:fpr | pr_auc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CS-AE-S42 | closed_set | autoencoder | 42 | completed | 82332 | results\runs\CS-AE-S42 | 0.8472 | 0.9131 | 0.7901 |  | 0.7901 | 0.0921 | 0.9170 |
| CS-AE-S52 | closed_set | autoencoder | 52 | completed | 82332 | results\runs\CS-AE-S52 | 0.8409 | 0.9163 | 0.7769 |  | 0.7769 | 0.0870 | 0.9161 |
| CS-AE-S62 | closed_set | autoencoder | 62 | completed | 82332 | results\runs\CS-AE-S62 | 0.8561 | 0.9112 | 0.8073 |  | 0.8073 | 0.0964 | 0.9284 |
| CS-AE-S72 | closed_set | autoencoder | 72 | completed | 82332 | results\runs\CS-AE-S72 | 0.8444 | 0.9110 | 0.7870 |  | 0.7870 | 0.0942 | 0.9353 |
| CS-AE-S82 | closed_set | autoencoder | 82 | completed | 82332 | results\runs\CS-AE-S82 | 0.8598 | 0.9181 | 0.8085 |  | 0.8085 | 0.0884 | 0.9301 |
| CS-IF-S42 | closed_set | isolation_forest | 42 | completed | 82332 | results\runs\CS-IF-S42 | 0.4296 | 0.8546 | 0.2869 |  | 0.2869 | 0.0598 | 0.8082 |
| CS-IF-S52 | closed_set | isolation_forest | 52 | completed | 82332 | results\runs\CS-IF-S52 | 0.5107 | 0.8848 | 0.3589 |  | 0.3589 | 0.0572 | 0.8378 |
| CS-IF-S62 | closed_set | isolation_forest | 62 | completed | 82332 | results\runs\CS-IF-S62 | 0.4348 | 0.8489 | 0.2922 |  | 0.2922 | 0.0637 | 0.8090 |
| CS-IF-S72 | closed_set | isolation_forest | 72 | completed | 82332 | results\runs\CS-IF-S72 | 0.4720 | 0.8558 | 0.3259 |  | 0.3259 | 0.0673 | 0.8176 |
| CS-IF-S82 | closed_set | isolation_forest | 82 | completed | 82332 | results\runs\CS-IF-S82 | 0.4543 | 0.8641 | 0.3081 |  | 0.3081 | 0.0594 | 0.8195 |
| CS-RF-S42 | closed_set | random_forest | 42 | completed | 82332 | results\runs\CS-RF-S42 | 0.9159 | 0.8662 | 0.9717 |  | 0.9717 | 0.1838 | 0.9879 |
| CS-RF-S52 | closed_set | random_forest | 52 | completed | 82332 | results\runs\CS-RF-S52 | 0.9156 | 0.8665 | 0.9706 |  | 0.9706 | 0.1832 | 0.9880 |
| CS-RF-S62 | closed_set | random_forest | 62 | completed | 82332 | results\runs\CS-RF-S62 | 0.9138 | 0.8624 | 0.9718 |  | 0.9718 | 0.1900 | 0.9878 |
| CS-RF-S72 | closed_set | random_forest | 72 | completed | 82332 | results\runs\CS-RF-S72 | 0.9159 | 0.8668 | 0.9708 |  | 0.9708 | 0.1828 | 0.9880 |
| CS-RF-S82 | closed_set | random_forest | 82 | completed | 82332 | results\runs\CS-RF-S82 | 0.9145 | 0.8633 | 0.9721 |  | 0.9721 | 0.1886 | 0.9879 |
| CS-XGB-S42 | closed_set | xgboost | 42 | completed | 82332 | results\runs\CS-XGB-S42 | 0.9148 | 0.8653 | 0.9704 |  | 0.9704 | 0.1851 | 0.9887 |
| CS-XGB-S52 | closed_set | xgboost | 52 | completed | 82332 | results\runs\CS-XGB-S52 | 0.9149 | 0.8652 | 0.9706 |  | 0.9706 | 0.1852 | 0.9885 |
| CS-XGB-S62 | closed_set | xgboost | 62 | completed | 82332 | results\runs\CS-XGB-S62 | 0.9105 | 0.8590 | 0.9685 |  | 0.9685 | 0.1948 | 0.9879 |
| CS-XGB-S72 | closed_set | xgboost | 72 | completed | 82332 | results\runs\CS-XGB-S72 | 0.9139 | 0.8654 | 0.9683 |  | 0.9683 | 0.1846 | 0.9882 |
| CS-XGB-S82 | closed_set | xgboost | 82 | completed | 82332 | results\runs\CS-XGB-S82 | 0.9133 | 0.8645 | 0.9679 |  | 0.9679 | 0.1858 | 0.9881 |
| LD-AE-S42 | loaco_dos | autoencoder | 42 | completed | 82332 | results\runs\LD-AE-S42 | 0.8603 | 0.9193 | 0.8085 | 0.8953 | 0.7999 | 0.0870 | 0.9347 |
| LD-AE-S52 | loaco_dos | autoencoder | 52 | completed | 82332 | results\runs\LD-AE-S52 | 0.8457 | 0.9100 | 0.7898 | 0.8731 | 0.7815 | 0.0956 | 0.9286 |
| LD-AE-S62 | loaco_dos | autoencoder | 62 | completed | 82332 | results\runs\LD-AE-S62 | 0.8501 | 0.9164 | 0.7927 | 0.8726 | 0.7848 | 0.0886 | 0.9291 |
| LD-AE-S72 | loaco_dos | autoencoder | 72 | completed | 82332 | results\runs\LD-AE-S72 | 0.8518 | 0.9118 | 0.7992 | 0.8829 | 0.7909 | 0.0948 | 0.9244 |
| LD-AE-S82 | loaco_dos | autoencoder | 82 | completed | 82332 | results\runs\LD-AE-S82 | 0.8531 | 0.9163 | 0.7980 | 0.8951 | 0.7884 | 0.0893 | 0.9297 |
| LD-IF-S42 | loaco_dos | isolation_forest | 42 | completed | 82332 | results\runs\LD-IF-S42 | 0.4631 | 0.8640 | 0.3163 | 0.0445 | 0.3433 | 0.0610 | 0.8204 |
| LD-IF-S52 | loaco_dos | isolation_forest | 52 | completed | 82332 | results\runs\LD-IF-S52 | 0.4551 | 0.8673 | 0.3085 | 0.0364 | 0.3354 | 0.0578 | 0.8215 |
| LD-IF-S62 | loaco_dos | isolation_forest | 62 | completed | 82332 | results\runs\LD-IF-S62 | 0.4037 | 0.8433 | 0.2654 | 0.0298 | 0.2887 | 0.0604 | 0.8081 |
| LD-IF-S72 | loaco_dos | isolation_forest | 72 | completed | 82332 | results\runs\LD-IF-S72 | 0.4505 | 0.8568 | 0.3055 | 0.0433 | 0.3315 | 0.0626 | 0.8229 |
| LD-IF-S82 | loaco_dos | isolation_forest | 82 | completed | 82332 | results\runs\LD-IF-S82 | 0.4737 | 0.8623 | 0.3266 | 0.0562 | 0.3534 | 0.0639 | 0.8188 |
| LD-RF-S42 | loaco_dos | random_forest | 42 | completed | 82332 | results\runs\LD-RF-S42 | 0.9141 | 0.8653 | 0.9687 | 0.9978 | 0.9658 | 0.1848 | 0.9874 |
| LD-RF-S52 | loaco_dos | random_forest | 52 | completed | 82332 | results\runs\LD-RF-S52 | 0.9137 | 0.8620 | 0.9719 | 0.9985 | 0.9693 | 0.1907 | 0.9876 |
| LD-RF-S62 | loaco_dos | random_forest | 62 | completed | 82332 | results\runs\LD-RF-S62 | 0.9138 | 0.8616 | 0.9728 | 0.9983 | 0.9702 | 0.1914 | 0.9876 |
| LD-RF-S72 | loaco_dos | random_forest | 72 | completed | 82332 | results\runs\LD-RF-S72 | 0.9148 | 0.8644 | 0.9715 | 0.9980 | 0.9689 | 0.1868 | 0.9877 |
| LD-RF-S82 | loaco_dos | random_forest | 82 | completed | 82332 | results\runs\LD-RF-S82 | 0.9150 | 0.8661 | 0.9697 | 0.9980 | 0.9669 | 0.1837 | 0.9877 |
| LD-XGB-S42 | loaco_dos | xgboost | 42 | completed | 82332 | results\runs\LD-XGB-S42 | 0.9144 | 0.8686 | 0.9654 | 0.9919 | 0.9627 | 0.1789 | 0.9879 |
| LD-XGB-S52 | loaco_dos | xgboost | 52 | completed | 82332 | results\runs\LD-XGB-S52 | 0.9162 | 0.8696 | 0.9682 | 0.9954 | 0.9655 | 0.1779 | 0.9884 |
| LD-XGB-S62 | loaco_dos | xgboost | 62 | completed | 82332 | results\runs\LD-XGB-S62 | 0.9132 | 0.8639 | 0.9685 | 0.9924 | 0.9661 | 0.1870 | 0.9881 |
| LD-XGB-S72 | loaco_dos | xgboost | 72 | completed | 82332 | results\runs\LD-XGB-S72 | 0.9125 | 0.8616 | 0.9697 | 0.9917 | 0.9675 | 0.1908 | 0.9883 |
| LD-XGB-S82 | loaco_dos | xgboost | 82 | completed | 82332 | results\runs\LD-XGB-S82 | 0.9137 | 0.8646 | 0.9687 | 0.9951 | 0.9660 | 0.1858 | 0.9879 |
| LE-AE-S42 | loaco_exploits | autoencoder | 42 | completed | 82332 | results\runs\LE-AE-S42 | 0.8490 | 0.9151 | 0.7918 | 0.8148 | 0.7843 | 0.0900 | 0.9236 |
| LE-AE-S52 | loaco_exploits | autoencoder | 52 | completed | 82332 | results\runs\LE-AE-S52 | 0.8461 | 0.9144 | 0.7873 | 0.7831 | 0.7887 | 0.0903 | 0.9334 |
| LE-AE-S62 | loaco_exploits | autoencoder | 62 | completed | 82332 | results\runs\LE-AE-S62 | 0.8615 | 0.9164 | 0.8128 | 0.8522 | 0.7999 | 0.0909 | 0.9307 |
| LE-AE-S72 | loaco_exploits | autoencoder | 72 | completed | 82332 | results\runs\LE-AE-S72 | 0.8465 | 0.9108 | 0.7906 | 0.8034 | 0.7865 | 0.0949 | 0.9258 |
| LE-AE-S82 | loaco_exploits | autoencoder | 82 | completed | 82332 | results\runs\LE-AE-S82 | 0.8448 | 0.9192 | 0.7816 | 0.7809 | 0.7818 | 0.0842 | 0.9334 |
| LE-IF-S42 | loaco_exploits | isolation_forest | 42 | completed | 82332 | results\runs\LE-IF-S42 | 0.4549 | 0.8521 | 0.3102 | 0.0605 | 0.3915 | 0.0660 | 0.8183 |
| LE-IF-S52 | loaco_exploits | isolation_forest | 52 | completed | 82332 | results\runs\LE-IF-S52 | 0.4448 | 0.8549 | 0.3006 | 0.0594 | 0.3791 | 0.0625 | 0.8160 |
| LE-IF-S62 | loaco_exploits | isolation_forest | 62 | completed | 82332 | results\runs\LE-IF-S62 | 0.4395 | 0.8608 | 0.2951 | 0.0480 | 0.3755 | 0.0585 | 0.8216 |
| LE-IF-S72 | loaco_exploits | isolation_forest | 72 | completed | 82332 | results\runs\LE-IF-S72 | 0.4372 | 0.8485 | 0.2944 | 0.0586 | 0.3712 | 0.0644 | 0.8116 |
| LE-IF-S82 | loaco_exploits | isolation_forest | 82 | completed | 82332 | results\runs\LE-IF-S82 | 0.4453 | 0.8568 | 0.3008 | 0.0384 | 0.3862 | 0.0616 | 0.8185 |
| LE-RF-S42 | loaco_exploits | random_forest | 42 | completed | 82332 | results\runs\LE-RF-S42 | 0.9137 | 0.8684 | 0.9640 | 0.9792 | 0.9590 | 0.1790 | 0.9838 |
| LE-RF-S52 | loaco_exploits | random_forest | 52 | completed | 82332 | results\runs\LE-RF-S52 | 0.9106 | 0.8639 | 0.9626 | 0.9670 | 0.9611 | 0.1858 | 0.9830 |
| LE-RF-S62 | loaco_exploits | random_forest | 62 | completed | 82332 | results\runs\LE-RF-S62 | 0.9104 | 0.8604 | 0.9665 | 0.9737 | 0.9642 | 0.1921 | 0.9831 |
| LE-RF-S72 | loaco_exploits | random_forest | 72 | completed | 82332 | results\runs\LE-RF-S72 | 0.9105 | 0.8628 | 0.9638 | 0.9673 | 0.9627 | 0.1877 | 0.9828 |
| LE-RF-S82 | loaco_exploits | random_forest | 82 | completed | 82332 | results\runs\LE-RF-S82 | 0.9129 | 0.8726 | 0.9570 | 0.9658 | 0.9542 | 0.1711 | 0.9826 |
| LE-XGB-S42 | loaco_exploits | xgboost | 42 | completed | 82332 | results\runs\LE-XGB-S42 | 0.9107 | 0.8670 | 0.9590 | 0.9754 | 0.9537 | 0.1803 | 0.9848 |
| LE-XGB-S52 | loaco_exploits | xgboost | 52 | completed | 82332 | results\runs\LE-XGB-S52 | 0.9071 | 0.8586 | 0.9613 | 0.9686 | 0.9589 | 0.1939 | 0.9837 |
| LE-XGB-S62 | loaco_exploits | xgboost | 62 | completed | 82332 | results\runs\LE-XGB-S62 | 0.9088 | 0.8610 | 0.9622 | 0.9707 | 0.9594 | 0.1904 | 0.9840 |
| LE-XGB-S72 | loaco_exploits | xgboost | 72 | completed | 82332 | results\runs\LE-XGB-S72 | 0.9103 | 0.8628 | 0.9634 | 0.9700 | 0.9613 | 0.1878 | 0.9842 |
| LE-XGB-S82 | loaco_exploits | xgboost | 82 | completed | 82332 | results\runs\LE-XGB-S82 | 0.9092 | 0.8652 | 0.9579 | 0.9690 | 0.9543 | 0.1829 | 0.9833 |
| LR-AE-S42 | loaco_reconnaissance | autoencoder | 42 | completed | 82332 | results\runs\LR-AE-S42 | 0.8568 | 0.9170 | 0.8040 | 0.2629 | 0.8492 | 0.0891 | 0.9159 |
| LR-AE-S52 | loaco_reconnaissance | autoencoder | 52 | completed | 82332 | results\runs\LR-AE-S52 | 0.8396 | 0.9177 | 0.7738 | 0.1831 | 0.8232 | 0.0851 | 0.9124 |
| LR-AE-S62 | loaco_reconnaissance | autoencoder | 62 | completed | 82332 | results\runs\LR-AE-S62 | 0.8492 | 0.9137 | 0.7932 | 0.2151 | 0.8415 | 0.0918 | 0.9333 |
| LR-AE-S72 | loaco_reconnaissance | autoencoder | 72 | completed | 82332 | results\runs\LR-AE-S72 | 0.8528 | 0.9154 | 0.7983 | 0.2623 | 0.8431 | 0.0904 | 0.9239 |
| LR-AE-S82 | loaco_reconnaissance | autoencoder | 82 | completed | 82332 | results\runs\LR-AE-S82 | 0.8583 | 0.9110 | 0.8113 | 0.2677 | 0.8567 | 0.0971 | 0.9329 |
| LR-IF-S42 | loaco_reconnaissance | isolation_forest | 42 | completed | 82332 | results\runs\LR-IF-S42 | 0.4423 | 0.8633 | 0.2973 | 0.0037 | 0.3218 | 0.0577 | 0.8146 |
| LR-IF-S52 | loaco_reconnaissance | isolation_forest | 52 | completed | 82332 | results\runs\LR-IF-S52 | 0.5055 | 0.8817 | 0.3543 | 0.0100 | 0.3831 | 0.0582 | 0.8329 |
| LR-IF-S62 | loaco_reconnaissance | isolation_forest | 62 | completed | 82332 | results\runs\LR-IF-S62 | 0.4262 | 0.8434 | 0.2852 | 0.0043 | 0.3086 | 0.0649 | 0.8102 |
| LR-IF-S72 | loaco_reconnaissance | isolation_forest | 72 | completed | 82332 | results\runs\LR-IF-S72 | 0.4569 | 0.8496 | 0.3125 | 0.0074 | 0.3380 | 0.0678 | 0.8178 |
| LR-IF-S82 | loaco_reconnaissance | isolation_forest | 82 | completed | 82332 | results\runs\LR-IF-S82 | 0.4967 | 0.8739 | 0.3469 | 0.0077 | 0.3753 | 0.0614 | 0.8315 |
| LR-RF-S42 | loaco_reconnaissance | random_forest | 42 | completed | 82332 | results\runs\LR-RF-S42 | 0.9152 | 0.8659 | 0.9704 | 0.9811 | 0.9695 | 0.1842 | 0.9855 |
| LR-RF-S52 | loaco_reconnaissance | random_forest | 52 | completed | 82332 | results\runs\LR-RF-S52 | 0.9145 | 0.8645 | 0.9707 | 0.9774 | 0.9701 | 0.1864 | 0.9852 |
| LR-RF-S62 | loaco_reconnaissance | random_forest | 62 | completed | 82332 | results\runs\LR-RF-S62 | 0.9131 | 0.8630 | 0.9694 | 0.9728 | 0.9691 | 0.1885 | 0.9847 |
| LR-RF-S72 | loaco_reconnaissance | random_forest | 72 | completed | 82332 | results\runs\LR-RF-S72 | 0.9146 | 0.8666 | 0.9682 | 0.9785 | 0.9673 | 0.1826 | 0.9852 |
| LR-RF-S82 | loaco_reconnaissance | random_forest | 82 | completed | 82332 | results\runs\LR-RF-S82 | 0.9145 | 0.8641 | 0.9712 | 0.9765 | 0.9708 | 0.1871 | 0.9852 |
| LR-XGB-S42 | loaco_reconnaissance | xgboost | 42 | completed | 82332 | results\runs\LR-XGB-S42 | 0.9117 | 0.8628 | 0.9664 | 0.9863 | 0.9648 | 0.1882 | 0.9853 |
| LR-XGB-S52 | loaco_reconnaissance | xgboost | 52 | completed | 82332 | results\runs\LR-XGB-S52 | 0.9123 | 0.8642 | 0.9661 | 0.9823 | 0.9647 | 0.1860 | 0.9858 |
| LR-XGB-S62 | loaco_reconnaissance | xgboost | 62 | completed | 82332 | results\runs\LR-XGB-S62 | 0.9107 | 0.8589 | 0.9691 | 0.9891 | 0.9675 | 0.1951 | 0.9850 |
| LR-XGB-S72 | loaco_reconnaissance | xgboost | 72 | completed | 82332 | results\runs\LR-XGB-S72 | 0.9136 | 0.8666 | 0.9660 | 0.9780 | 0.9650 | 0.1821 | 0.9853 |
| LR-XGB-S82 | loaco_reconnaissance | xgboost | 82 | completed | 82332 | results\runs\LR-XGB-S82 | 0.9113 | 0.8636 | 0.9646 | 0.9674 | 0.9644 | 0.1866 | 0.9846 |

## 5. Tổng hợp mean/std qua 5 seed

Bảng này dùng 80 run có official test đầy đủ; mỗi scenario/model có 5 seed. Các cột là mean và độ lệch chuẩn sample của metric tại target FPR 5%.

| scenario | model | pr_auc_mean | pr_auc_std | all:f1_mean | all:f1_std | normal:fpr_mean | normal:fpr_std | known_attack:recall_mean | known_attack:recall_std | heldout_attack:uadr_mean | heldout_attack:uadr_std |
|---|---|---|---|---|---|---|---|---|---|---|---|
| closed_set | autoencoder | 0.9254 | 0.0085 | 0.8497 | 0.0080 | 0.0916 | 0.0039 | 0.7940 | 0.0136 |  |  |
| closed_set | isolation_forest | 0.8184 | 0.0120 | 0.4603 | 0.0328 | 0.0615 | 0.0040 | 0.3144 | 0.0292 |  |  |
| closed_set | random_forest | 0.9879 | 0.0001 | 0.9151 | 0.0009 | 0.1857 | 0.0034 | 0.9714 | 0.0007 |  |  |
| closed_set | xgboost | 0.9883 | 0.0003 | 0.9135 | 0.0018 | 0.1871 | 0.0043 | 0.9691 | 0.0012 |  |  |
| loaco_dos | autoencoder | 0.9293 | 0.0037 | 0.8522 | 0.0054 | 0.0911 | 0.0039 | 0.7891 | 0.0070 | 0.8838 | 0.0112 |
| loaco_dos | isolation_forest | 0.8183 | 0.0059 | 0.4492 | 0.0269 | 0.0611 | 0.0023 | 0.3305 | 0.0248 | 0.0421 | 0.0099 |
| loaco_dos | random_forest | 0.9876 | 0.0001 | 0.9143 | 0.0006 | 0.1875 | 0.0035 | 0.9682 | 0.0018 | 0.9981 | 0.0003 |
| loaco_dos | xgboost | 0.9881 | 0.0003 | 0.9140 | 0.0014 | 0.1841 | 0.0055 | 0.9656 | 0.0017 | 0.9933 | 0.0018 |
| loaco_exploits | autoencoder | 0.9294 | 0.0044 | 0.8496 | 0.0068 | 0.0901 | 0.0038 | 0.7883 | 0.0070 | 0.8069 | 0.0290 |
| loaco_exploits | isolation_forest | 0.8172 | 0.0037 | 0.4443 | 0.0068 | 0.0626 | 0.0029 | 0.3807 | 0.0082 | 0.0529 | 0.0096 |
| loaco_exploits | random_forest | 0.9831 | 0.0004 | 0.9116 | 0.0016 | 0.1832 | 0.0082 | 0.9602 | 0.0039 | 0.9706 | 0.0057 |
| loaco_exploits | xgboost | 0.9840 | 0.0005 | 0.9092 | 0.0014 | 0.1870 | 0.0055 | 0.9575 | 0.0033 | 0.9707 | 0.0027 |
| loaco_reconnaissance | autoencoder | 0.9237 | 0.0096 | 0.8513 | 0.0074 | 0.0907 | 0.0044 | 0.8427 | 0.0125 | 0.2382 | 0.0375 |
| loaco_reconnaissance | isolation_forest | 0.8214 | 0.0102 | 0.4655 | 0.0344 | 0.0620 | 0.0043 | 0.3454 | 0.0327 | 0.0066 | 0.0026 |
| loaco_reconnaissance | random_forest | 0.9852 | 0.0003 | 0.9144 | 0.0008 | 0.1858 | 0.0024 | 0.9694 | 0.0013 | 0.9773 | 0.0030 |
| loaco_reconnaissance | xgboost | 0.9852 | 0.0004 | 0.9119 | 0.0011 | 0.1876 | 0.0047 | 0.9653 | 0.0012 | 0.9806 | 0.0085 |

## 6. Giới hạn bằng chứng

- Đã chạy đủ 80 run seed theo protocol. Tuy nhiên, Gate 1/Gate 2 vẫn cần review người và nhóm chưa được dùng một bảng số liệu để khẳng định model tốt nhất ngoài protocol đã định.
- Mọi run hiện đã có run.json, metrics.csv, predictions.csv và model_bundle.joblib; prediction files được giữ ngoài GitHub do kích thước.
- Gate 1/Gate 2 vẫn cần ba thành viên review và ký xác nhận riêng; validator không tự thay thế review người.

## 7. Artifact truy vết

- Bảng chi tiết: `docs/reports/DOT_02_METRICS_ALL_RUNS.csv`.
- Bảng mean/std: `docs/reports/DOT_02_METRICS_MEAN_STD.csv`.
- Mỗi run: `results/runs/<run_id>/run.json`, `metrics.csv`, `model_bundle.joblib`.
- Manifest: `artifacts/data/data_manifest.json`.
