"""Package the final 14/11 web build for review and offline use; never submit it."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import sys
import uuid
import zipfile


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "sites/nids-presentation/dist"
OUT = ROOT / "output/review_update_20261114"
PACKAGE = OUT / "NIDS_CAP_NHAT_20261114.zip"
RELEASE = ROOT / "docs/releases/review_final_20261113"
PUBLIC_URL = "https://nids-unsw-nb15-tlcn.nttin181.chatgpt.site"
EXPECTED_RUNS = {
    f"{scenario}-{model}-S42"
    for scenario in ("CS", "LR", "LD", "LE")
    for model in ("RF", "XGB", "IF", "AE")
}
FROZEN_PDFS = {
    "NhomTLCN_dot4_BAN_NHAP_20261113.pdf": (
        "reports", "d163bfd63b78d7cd06ccacd7450d03180a22195fe2623606b15b52890497f6df"
    ),
    "NhomTLCN_tong_BAN_NHAP_20261113.pdf": (
        "reports", "4268e8506db1b87dc18a00e785af1ed198d59674a1fd4a3bdbba1cd0210e5445"
    ),
    "NhomTLCN_slide_du_phong_20261113.pdf": (
        "slides", "6eb75200459ec1fcbbb16093e2eaf919deaa7a969c77ffc3e2b29702e532aac8"
    ),
    "NhomTLCN_phan_viec_on_nhom_20261113.pdf": (
        "slides", "860cef94df5973d986df60a4ea925333b7df14242a7d8308c87b2f97fa2d86b7"
    ),
}
FROZEN_SOURCE_ZIPS = {
    "Nguon_dot4_BAN_NHAP_20261113.zip": (
        "reports", "5a8f70dbcf77f829f0dfa82e7d62b841f35ddad307b48cab422f0e5b42d0cc68"
    ),
    "Nguon_tong_BAN_NHAP_20261113.zip": (
        "reports", "f503750b9766f67a617251c37a769f3515e0ab5cb1096280e0f734277180a1ef"
    ),
}
LAUNCHER = (
    '@echo off\r\n'
    'cd /d "%~dp0"\r\n'
    'python offline_presentation.py\r\n'
    'pause\r\n'
).encode("ascii")
README = f"""# Bộ cập nhật hồ sơ NIDS — 14/11/2026

Gói này gồm toàn bộ web trình bày, hồ sơ nhóm, PDF/nguồn đọc duyệt,
16 bộ tham số model seed 42 và dữ liệu mẫu từ bản web đã được đóng gói.
Các PDF và hai ZIP nguồn báo cáo ngày 13/11 giữ nguyên byte; script kiểm
SHA-256 trước khi tạo gói. Không dùng ngày cập nhật giao diện làm ngày train.

## Mở bản offline

1. Máy cần Python 3 hiện có và Chrome/Edge hiện hành. Không cần cài pip,
   thư viện học máy hoặc tải model từ mạng để chạy gói này.
2. Giải nén ĐẦY ĐỦ ZIP vào một thư mục thường. Không chạy trong cửa sổ ZIP
   và không mở web/index.html bằng nhấp đúp.
3. Trên Windows, chạy CHAY_DEMO.cmd. Giữ cửa sổ đó mở, mở địa chỉ localhost
   thực tế được in trong cửa sổ bằng trình duyệt. Thường là
   http://127.0.0.1:4399/; nếu cổng bận, chương trình tự chọn cổng tiếp theo.
   Để xem hồ sơ, bấm Hồ sơ nhóm trên web hoặc thêm ho-so.html vào địa chỉ
   vừa được in, ví dụ http://127.0.0.1:4399/ho-so.html.

Nếu lệnh python chưa được nhận, kiểm Python 3 đã cài và có trong PATH.
Có thể mở terminal tại thư mục giải nén và chạy `py -3 offline_presentation.py`
nếu máy dùng Python Launcher. Linux/macOS dùng `python3 offline_presentation.py`.
Nhấn Ctrl+C ở cửa sổ server để dừng. Không tắt cửa sổ đó khi đang demo.

Các tệp web, model, case và PDF nằm trong gói; các liên kết ngoài như GitHub,
Drive và website public vẫn cần Internet. Gói này không có backend đồng bộ nhóm.

## Khi có mạng

- Hồ sơ nhóm: {PUBLIC_URL}/ho-so.html
- Trình bày và demo: {PUBLIC_URL}/
- Drive bàn giao: https://drive.google.com/drive/folders/1d-m5b35FVvGU3AEuA8vx1c9btG5xznUl

Các URL trên chỉ là địa chỉ dịch vụ; việc đóng gói không tự chứng minh một
bản public đã triển khai. Theo biên bản triển khai/kiểm public đi cùng thông báo
bàn giao để biết phiên bản online đang hoạt động. ZIP là ảnh chụp bản web lúc gói,
không tự nhận thay đổi về sau.

## Ba bước đọc và góp ý

1. Ở Tài liệu, mở đúng PDF đợt 4/tổng và phiếu phân việc.
2. Ở Phần từng người, chọn tên mình, đọc trang được chỉ và tự trả lời câu hỏi.
3. Ở Cần chốt, chọn tên người ghi, ghi tệp/trang cùng góp ý rồi tải TXT.
   Tự gửi TXT vào Zalo nhóm; trang không tự gửi hoặc đánh dấu đã duyệt.

Góp ý ở trong trang đang mở, chưa tự đồng bộ hoặc lưu sang máy người khác.
Tải TXT không đồng nghĩa với đã nộp, đã duyệt hoặc đã được giảng viên đồng ý.
Nhóm cần tự gom góp ý, sửa nội dung và thống nhất cùng phiên bản PDF.

## Trạng thái và giới hạn

Đợt 3 đã gửi ngày 12/11. Đợt 4 và báo cáo tổng trong gói vẫn là bản chờ nhóm
đọc duyệt, CHƯA GỬI GIẢNG VIÊN. Gói cập nhật không sửa bản PDF 13/11 hoặc lịch sử đã nộp,
không tạo xác nhận đóng góp/review thay một thành viên.

Demo suy luận từ model đã lưu, không học lại hoặc chặn tấn công. CSV xử lý tại
trình duyệt. Dữ liệu mẫu là tập con UNSW-NB15, chưa phải traffic độc lập do nhóm thu.
S07 còn giới hạn abstract; T2/T9 còn thiếu log phần cứng/thời gian train lịch sử.
Nhóm cần tập nói, kiểm câu hỏi phản biện và thử HDMI trên thiết bị lớp thật.

## Kiểm tính toàn vẹn

MANIFEST.json liệt kê đường dẫn, số byte và SHA-256 của mọi tệp nội dung,
gồm web, trình phục vụ, launcher và README này. Manifest không thể tự chứa
SHA-256 của chính nó; nó là tệp chỉ mục bổ sung trong ZIP. Script kiểm CRC,
toàn bộ tệp theo manifest và đủ 16 model sau khi đóng gói. Kiểm này xác nhận
nội dung gói, không xác nhận mức hiểu của nhóm hoặc chất lượng mọi dữ liệu mới.
""".encode("utf-8")


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def collect_sources() -> list[tuple[str, Path]]:
    required = (
        "index.html", "presentation.js", "presentation.css", "browser-engine.mjs",
        "browser-worker.mjs", "browser-adapter.js", "ho-so.html", "ho-so.css",
        "ho-so.js", "models/manifest.json",
        "downloads/DOI_CHIEU_YEU_CAU_20261114.md",
    )
    for name in required:
        require((DIST / name).is_file(), f"Thiếu tệp final dist: {DIST / name}")

    for name, (folder, expected_hash) in (FROZEN_PDFS | FROZEN_SOURCE_ZIPS).items():
        original = RELEASE / folder / name
        hosted = DIST / "downloads" / name
        require(original.is_file() and hosted.is_file(), f"Thiếu bản nguồn/download: {name}")
        require(sha(original) == expected_hash, f"Bản 13/11 đã khác fingerprint đã khóa: {name}")
        require(sha(hosted) == expected_hash, f"Download khác bản 13/11: {name}")

    manifest = json.loads((DIST / "models/manifest.json").read_text(encoding="utf-8"))
    models = manifest.get("models", [])
    require(len(models) == 16, "Model manifest phải có đúng 16 mục")
    require({row["run_id"] for row in models} == EXPECTED_RUNS, "Run ID model không khớp 4 × 4 seed 42")
    expected_files = set()
    for row in models:
        name = row["file"]
        require(Path(name).name == name and name.endswith(".bin.gz"), f"Tên model không hợp lệ: {name}")
        path = DIST / "models" / name
        require(path.is_file(), f"Thiếu tham số model: {path}")
        require(path.stat().st_size == row["bytes"] and sha(path) == row["sha256"], f"Model không khớp manifest: {name}")
        expected_files.add(name)
    require(len(expected_files) == 16, "Tên file model bị trùng")
    require({p.name for p in (DIST / "models").glob("*.bin.gz")} == expected_files, "Dist thừa hoặc thiếu file model")

    sources = []
    for path in sorted(DIST.rglob("*")):
        require(not path.is_symlink(), f"Không đóng gói symlink: {path}")
        if path.is_file():
            sources.append(("web/" + path.relative_to(DIST).as_posix(), path))
    server = ROOT / "scripts/offline_presentation.py"
    require(server.is_file(), f"Thiếu trình phục vụ offline: {server}")
    sources.append(("offline_presentation.py", server))
    return sources


def main() -> None:
    require(sys.version_info >= (3, 9), "Script đóng gói cần Python 3.9 trở lên")
    require(not PACKAGE.exists(), f"Gói đã tồn tại; giữ nguyên, không ghi đè: {PACKAGE}")
    sources = collect_sources()
    generated = {"CHAY_DEMO.cmd": LAUNCHER, "README.md": README}
    rows = [dict(path=name, bytes=path.stat().st_size, sha256=sha(path)) for name, path in sources]
    rows.extend(dict(path=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()) for name, data in generated.items())
    rows.sort(key=lambda row: row["path"])
    require(len({row["path"] for row in rows}) == len(rows), "Archive path bị trùng")
    manifest_bytes = (json.dumps(rows, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    OUT.mkdir(parents=True, exist_ok=True)
    temporary = OUT / f".{PACKAGE.name}.{uuid.uuid4().hex}.part"
    try:
        with zipfile.ZipFile(temporary, "x", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, path in sources:
                archive.write(path, name)
            for name, data in generated.items():
                archive.writestr(name, data)
            archive.writestr("MANIFEST.json", manifest_bytes)
        with zipfile.ZipFile(temporary) as archive:
            require(archive.testzip() is None, "ZIP có lỗi CRC")
            require(len(archive.namelist()) == len(set(archive.namelist())), "ZIP có mục trùng")
            require(set(archive.namelist()) == {row["path"] for row in rows} | {"MANIFEST.json"}, "Danh mục ZIP không khớp manifest")
            require(archive.read("MANIFEST.json") == manifest_bytes, "Manifest trong ZIP bị thay đổi")
            for row in rows:
                data = archive.read(row["path"])
                require(len(data) == row["bytes"] and hashlib.sha256(data).hexdigest() == row["sha256"], f"ZIP hash mismatch: {row['path']}")
            require(len([name for name in archive.namelist() if name.startswith("web/models/") and name.endswith(".bin.gz")]) == 16, "ZIP không có đủ 16 model")
        temporary.rename(PACKAGE)
    finally:
        if temporary.exists():
            temporary.unlink()

    # Sidecars describe this new package only. No release_20261113 files are written.
    (OUT / "MANIFEST.json").write_bytes(manifest_bytes)
    (OUT / "README.md").write_bytes(README)
    receipt = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "package": str(PACKAGE), "source_dist": str(DIST),
        "bytes": PACKAGE.stat().st_size, "sha256": sha(PACKAGE),
        "manifest_files": len(rows), "zip_entries": len(rows) + 1,
        "crc_and_manifest_hashes_match": True, "model_count": 16,
        "frozen_20261113_pdfs_and_source_zips_unchanged": True,
        "status": "PACKAGED_PENDING_GROUP_REVIEW",
        "group_approval": False, "dot4_and_total_submitted": False,
        "public_deployment_confirmed_by_packaging": False,
        "physical_hdmi_test_confirmed_by_packaging": False,
    }
    (OUT / "PACKAGE_CHECK.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
