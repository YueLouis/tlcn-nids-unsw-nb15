# PHAO GAP THAY - 17/09/2026

## 1. Muc tieu buoi gap

Hom nay nhom khong den de bao ve mot san pham da hoan thanh. Nhom den de:

1. Nghe thay huong dan lai cach bao cao de thay theo doi duoc.
2. Trinh bay dung phan nhom da chuan bi, khong noi thanh ket qua thuc nghiem.
3. Xac nhan pham vi de tai, cach bao cao, moc nop tiep theo va san pham thay mong doi.

## 2. Cau mo dau cua Tin

> Da nhom em cam on Thay da sap xep thoi gian. Bao cao vua roi cua nhom em trinh bay chua dung cach de Thay theo doi, nen hom nay nhom em xin phep nghe Thay huong dan lai. Truoc do, nhom em xin trinh bay rat ngan gon de tai, nhung gi dang co va nhung gi chua lam, sau do nho Thay gop y de nhom sua dung tu dau a.

Neu thay muon vao thang cach bao cao thi ngung trinh bay, mo note va ghi lai dung y thay.

## 3. De tai trong 30 giay

> Nhom em dung bo du lieu network-flow UNSW-NB15 de so sanh bon mo hinh phat hien xam nhap. Random Forest va XGBoost la hai mo hinh hoc co giam sat; Isolation Forest va Autoencoder la hai mo hinh phat hien bat thuong. Ngoai closed-set, nhom du kien danh gia LOACO bang cach loai mot nhom tan cong khoi toan bo vung phat trien, sau do kiem tra kha nang phat hien nhom bi giu lai. Hien tai day moi la protocol du kien, nhom chua co ket qua mo hinh that.

## 4. Nhom da co gi tren may

Chi noi la `da co ban nhap/khung` neu chua co review cua ca ba thanh vien.

- De cuong va bao cao tien do bon tuan dau.
- Repository GitHub private: `YueLouis/tlcn-nids-unsw-nb15`.
- Cau truc thu muc `configs`, `docs`, `scripts`, `src`, `tests`, `data`.
- File cau hinh `configs/experiment_matrix.yaml`.
- Danh sach `docs/protocol/RUN_MATRIX.csv`: 4 kich ban x 4 model x 5 seed = 80 cau hinh du kien.
- Ba cau hoi nghien cuu va bang chung can thu thap trong `docs/protocol/RQ_TO_EVIDENCE.md`.
- Quy dinh output trong `docs/protocol/RESULT_SCHEMA.md`.
- Checklist review trong `docs/protocol/GATE_1_CHECKLIST.md`.
- Code contract toi thieu trong `src/nids_benchmark/contracts.py`.
- Validator `scripts/validate_protocol.py`.
- Hien tai 6/6 unit test PASS va validator bao du 80 run khong trung ID.

### Phai noi ro nhung gi CHUA CO

- Chua tai va audit day du hai CSV chinh thuc.
- Chua co data manifest/checksum/data contract hoan chinh.
- Chua co preprocessing chay tren du lieu that.
- Chua train RF, XGBoost, Isolation Forest hay Autoencoder.
- Chua co ket qua closed-set/LOACO va chua co bang bieu ket qua that.
- Chua co prototype hoan chinh.
- Gate 1 van `NOT REVIEWED`, chua co xac nhan cua ca ba thanh vien.

## 5. File mo san theo thu tu

1. `docs/reports/BAO_CAO_TIEN_DO_4_TUAN_LAN_01.pdf`
2. `docs/management/GANTT_CHART.md`
3. `docs/management/PHAN_CONG_NHOM.md`
4. `configs/experiment_matrix.yaml`
5. `docs/protocol/RUN_MATRIX.csv`
6. `docs/protocol/RQ_TO_EVIDENCE.md`
7. `docs/protocol/RESULT_SCHEMA.md`
8. `docs/protocol/GATE_1_CHECKLIST.md`
9. `src/nids_benchmark/contracts.py`
10. `tests/test_contracts.py`

Khong tu mo tat ca mot luc. Thay hoi den dau moi mo file lien quan den do.

## 6. Phan cong de tung ban tu tra loi

### Nguyen Trong Tin

> Em la nhom truong, phu trach repository, protocol, preprocessing, Random Forest, XGBoost, quan ly cac lan chay va tich hop. Hien em da co khung config, run matrix, result schema, contract code va validator. Em chua chay model that vi du lieu va protocol chua duoc nhom review xong.

### Trinh Tram Anh

> Em phu trach phan du lieu va tai lieu nen: UNSW-NB15, nguon du lieu, checksum, schema, missing, duplicate, phan bo nhan, related work va bien tap. Hien trong repo co cac mau glossary, data-audit checklist va related-work matrix; buoc tiep theo la kiem ke du lieu chinh thuc va ban giao data contract.

### Hoang Van Vuong Thu

> Em phu trach Isolation Forest, Autoencoder, cach quy doi score, chon threshold, metric va phan tich FP/FN. Hien trong repo co ban nhap metric/threshold spec va synthetic-test list; chua train hai mo hinh bat thuong tren du lieu that.

Neu artifact nao khong phai chinh ban do tu viet/review, phai noi that: `File nay la ban nhap chung cua nhom, em chua review xong phan cua minh.`

## 7. Thay hoi gi - dap ngan gon nhu the nao

### De tai cuoi cung lam ra cai gi?

> San pham chinh la mot benchmark co the chay lai de so sanh bon mo hinh tren closed-set va ba kich ban LOACO, kem bang bieu, phan tich loi, bao cao, slide va mot prototype chay local. Nhom em khong dat muc tieu lam SOC hoan chinh hay website thuong mai.

### Co can VMware khong?

> Hien protocol dung bo du lieu flow co san nen chua can VMware. Neu Thay yeu cau demo traffic song hoac moi truong tan cong thi nhom moi bo sung may ao theo pham vi Thay chot.

### Tai sao chon UNSW-NB15?

> Vi bo du lieu co official train/test, co nhan Normal/Attack va attack category, phu hop de so sanh closed-set voi held-out attack. Nhom van phai neu gioi han vi day la benchmark cu va khong dai dien day du cho mang thuc te hien nay.

### LOACO la gi?

> Leave-One-Attack-Class-Out la loai hoan toan mot attack class khoi vung phat trien truoc khi split, fit preprocessing, train va tuning; sau do moi danh gia class do tren official test.

### LOACO co phai phat hien zero-day khong?

> Khong a. No chi mo phong mot attack class chua thay trong benchmark. Nhom em khong dung ket qua nay de khang dinh phat hien moi zero-day ngoai thuc te.

### Tai sao co 80 run?

> Co 4 kich ban gom closed-set va 3 LOACO, nhan 4 model, nhan 5 seed, nen co 80 cau hinh du kien. Day la 80 dong ke hoach, chua phai 80 ket qua da chay.

### Tai sao phai chay 5 seed?

> De thay ket qua co on dinh theo ngau nhien hay khong va bao cao mean/std, tranh chon mot lan chay dep.

### Tai sao khong chi dung Accuracy?

> Du lieu an ninh mang mat can bang nen Accuracy co the cao du model bo sot attack. Nhom uu tien recall cua attack bi giu lai, recall cua known attack va FPR tren Normal; kem Precision, F1 va PR-AUC.

### Threshold lay o dau?

> Du kien lay tren Normal validation tai FPR muc tieu 1% va 5%, khong nhin official test de chon threshold. Day van la diem nhom muon xin Thay xac nhan.

### Tai sao cam `id`, `label`, `attack_cat` lam feature?

> `label` va `attack_cat` la thong tin dap an, con `id` la dinh danh. Dua vao feature se gay leakage va lam ket qua ao.

### Bay gio code duoc den dau?

> Code hien tai moi la scaffold va contract: loai cot cam, chuan hoa label, gan vai tro normal/known/held-out, loai held-out class khoi development, kiem tra run matrix. Sau unit test, 6 test PASS. Chua co training pipeline va model result.

### Validator PASS co nghia la de tai da chay dung chua?

> Chua a. Validator chi kiem tra cau hinh co du 4 kich ban, 4 model, 5 seed, run ID khong trung va tai lieu protocol ton tai. Gate 1 van can con nguoi review, con model van chua train.

### Tai sao chon Reconnaissance, DoS va Exploits?

> Day la ba lop nhom de xuat so bo de tao ba bai kiem tra held-out khac nhau. Nhom chua xem day la quyet dinh cuoi; nhom se kiem tra support cua tung lop va xin Thay xac nhan truoc khi khoa protocol.

### Ai viet nhung file nay? Co dung AI khong?

> Nhom co dung AI de ho tro tao khung, giai thich va kiem tra logic. Nhom em khong xem output AI la ket qua tu dong: cac thanh vien phai doc, review, chay test, hieu va chiu trach nhiem phan duoc giao. Hien nhom con thieu review cheo va se sua theo cach Thay huong dan.

### Tai sao bao cao vua roi Thay khong theo doi duoc?

> Da nhom em nhan thieu sot vi bao cao dua qua nhieu thuat ngu va chua trinh bay theo dung luong thong tin Thay can. Hom nay nhom xin Thay chi ro mau/trinh tu; nhom se viet lai gon, co viec, nguoi, artifact va trang thai ro rang.

### Nhom bi tre gi?

> Nhom gui bao cao bon tuan dau cham so voi moc can gui. Phan thuc nghiem cung chua bat dau vi nhom dang khoa protocol va chua audit du lieu. Nhom xin nhan thieu sot va chot lai lich theo huong dan cua Thay.

## 8. Cau hoi nhom phai hoi thay

Neu thay chua noi ro, Tin hoi lan luot, khong hoi don dap:

1. `Thay cho nhom em xin cau truc mot lan bao cao ma Thay de theo doi nhat gom nhung muc nao a?`
2. `Moi bon tuan nhom gui mot ban tong hop, con trong bon tuan co can cap nhat hang tuan trong cung chuoi mail khong a?`
3. `Moi cong viec co can ghi nguoi phu trach, file minh chung, trang thai va viec tiep theo khong a?`
4. `Thay muon nhom gui PDF, Word, link Drive hay link repository; quy tac dat ten file nhu the nao a?`
5. `Lan bao cao tiep theo tinh tu ngay nao va han cu the la ngay nao a?`
6. `Pham vi bon model va ba lop LOACO hien tai co phu hop khong, hay Thay muon nhom thu hep/mo rong?`
7. `San pham cuoi Thay mong doi la benchmark + prototype local, hay can them web/VMware/demo traffic song a?`
8. `Thay co mau bao cao hoac mot bao cao cu de nhom tham khao khong a?`

## 9. Khi thay giao viec hoac sua yeu cau

Tin ghi theo mau nay ngay tai cho:

| Yeu cau cua Thay | Ai lam | File/san pham | Han | Can hoi lai |
|---|---|---|---|---|
| | | | | |

Cuoi buoi, doc lai:

> Da de nhom em xac nhan lai: nhom can lam ...; trinh bay theo ...; nop/bao cao vao ...; san pham gom ... Dung nhu vay khong a?

## 10. Ba dieu tuyet doi khong noi qua

1. Khong noi `da co 80 ket qua`; moi chi co 80 cau hinh du kien.
2. Khong noi `Gate 1 da PASS`; trang thai van la `NOT REVIEWED`.
3. Khong noi `da co mo hinh/IDS/prototype`; chua train tren du lieu that.

## 11. Cau cuu nguy khi bi hoi ma chua chac

> Da phan nay nhom em chua co du bang chung de ket luan. Em xin ghi lai dung cau hoi cua Thay, sau buoi nay nhom se kiem tra artifact/du lieu va phan hoi trong cung chuoi mail a.

Khong doan, khong bia so lieu, khong tranh tra loi vong vo.
