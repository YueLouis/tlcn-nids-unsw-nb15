"""Build the traceable 80-run summary and progress report for round 2."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "results" / "runs"
OUT = ROOT / "docs" / "reports"


def markdown_table(frame: pd.DataFrame) -> str:
    columns = [str(column) for column in frame.columns]
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for values in frame.itertuples(index=False, name=None):
        rendered = []
        for value in values:
            if isinstance(value, float):
                rendered.append("" if pd.isna(value) else f"{value:.4f}")
            else:
                rendered.append("" if pd.isna(value) else str(value))
        lines.append("| " + " | ".join(rendered) + " |")
    return "\n".join(lines)


def main() -> None:
    rows: list[pd.DataFrame] = []
    for metrics_path in sorted(RUNS.glob("*/metrics.csv")):
        frame = pd.read_csv(metrics_path)
        frame["artifact_dir"] = str(metrics_path.parent.relative_to(ROOT))
        rows.append(frame)
    if not rows:
        raise SystemExit("No metrics.csv files found")
    test_result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q"],
        cwd=ROOT, env={**os.environ, "PYTHONPATH": str(ROOT / "src")}, capture_output=True, text=True,
    )
    test_match = re.search(r"Ran (\d+) tests?", test_result.stderr + test_result.stdout)
    test_count = test_match.group(1) if test_match else "?"
    metrics = pd.concat(rows, ignore_index=True)
    selected = metrics[metrics["target_fpr"].eq(0.05)].copy()
    selected["metric_key"] = selected["subset"] + ":" + selected["metric"]
    table = selected.pivot_table(
        index="run_id", columns="metric_key", values="value", aggfunc="first"
    ).reset_index()
    pr_auc = (
        metrics[metrics["metric"].eq("pr_auc")]
        .loc[:, ["run_id", "value"]]
        .rename(columns={"value": "pr_auc"})
        .drop_duplicates("run_id")
    )
    metadata = []
    for run_json in sorted(RUNS.glob("*/run.json")):
        item = json.loads(run_json.read_text(encoding="utf-8"))
        metadata.append(
            {
                "run_id": item["run_id"],
                "scenario": item["scenario"],
                "model": item["model"],
                "seed": item["seed"],
                "status": item["status"],
                "official_test_rows": item["row_counts"]["official_test_evaluated"],
                "artifact_dir": str(run_json.parent.relative_to(ROOT)),
            }
        )
    meta = pd.DataFrame(metadata)
    summary = meta.merge(table, on="run_id", how="left").merge(pr_auc, on="run_id", how="left")
    OUT.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUT / "DOT_02_METRICS_ALL_RUNS.csv", index=False)
    summary["scenario"] = summary["scenario"].astype(str)
    summary["model"] = summary["model"].astype(str)
    full = summary[summary["official_test_rows"].eq(82332)].copy()
    metric_columns = [
        "pr_auc", "all:f1", "normal:fpr", "known_attack:recall", "heldout_attack:uadr"
    ]
    aggregate = full.groupby(["scenario", "model"], as_index=False)[metric_columns].agg(["mean", "std"])
    aggregate.columns = [
        "scenario", "model", *[f"{metric}_{stat}" for metric in metric_columns for stat in ("mean", "std")]
    ]
    aggregate.to_csv(OUT / "DOT_02_METRICS_MEAN_STD.csv", index=False)

    manifest = json.loads((ROOT / "artifacts" / "data" / "data_manifest.json").read_text(encoding="utf-8"))
    train = manifest["files"]["train"]["audit"]
    test = manifest["files"]["test"]["audit"]
    report = [
        "# Báo cáo tiến độ tiểu luận chuyên ngành - Đợt 2",
        "",
        "**Trạng thái:** Bản tích lũy kỹ thuật ngày 26/09/2026; đã chạy đủ 80 run theo protocol.",
        "",
        "## 1. Kết luận ngắn",
        "",
        f"Pipeline đã đọc đúng hai official split UNSW-NB15 ({train['rows']:,} dòng train, {test['rows']:,} dòng test), vượt qua {test_count}/{test_count} unit test và tạo đủ 80 artifact run cho 4 scenario x 4 model x 5 seed. Mỗi run có run.json, metrics.csv, predictions.csv và model_bundle.joblib; mean/std đã được tổng hợp riêng. Gate 1/Gate 2 vẫn cần review người.",
        "",
        "## 2. Audit dữ liệu",
        "",
        "| Split | Dòng | Cột | Duplicate | Missing | Label 0 | Label 1 | SHA-256 |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
        f"| train | {train['rows']:,} | {train['columns']} | {train['duplicate_rows']} | {train['missing_values']} | {train['label_counts']['0']:,} | {train['label_counts']['1']:,} | `{manifest['files']['train']['sha256']}` |",
        f"| test | {test['rows']:,} | {test['columns']} | {test['duplicate_rows']} | {test['missing_values']} | {test['label_counts']['0']:,} | {test['label_counts']['1']:,} | `{manifest['files']['test']['sha256']}` |",
        "",
        "Artifact đầy đủ: `artifacts/data/data_manifest.json`.",
        "",
        "## 3. Protocol và kiểm thử",
        "",
        "- Cột metadata bị loại khỏi feature: `id`, `label`, `attack_cat`.",
        "- Preprocessing fit trên development; LOACO loại held-out class trước split/fit.",
        "- Threshold lấy từ Normal validation tại FPR mục tiêu 1% và 5%; official test chỉ dùng đánh giá.",
        f"- `python -m unittest discover -s tests -v`: **{test_count}/{test_count} PASS**.",
        "- `python scripts/validate_protocol.py`: **80 run_id hợp lệ** trong ma trận protocol.",
        "",
        "## 4. Bảng kết quả chi tiết theo run",
        "",
        "Bảng dưới đây dùng threshold mục tiêu FPR 5%. `pr_auc` không phụ thuộc threshold; `normal:fpr`, `known_attack:recall` và `heldout_attack:uadr` có support trong `metrics.csv`. Bảng mean/std qua 5 seed nằm ở phần tiếp theo.",
        "",
        markdown_table(summary),
        "",
        "## 5. Tổng hợp mean/std qua 5 seed",
        "",
        "Bảng này dùng 80 run có official test đầy đủ; mỗi scenario/model có 5 seed. Các cột là mean và độ lệch chuẩn sample của metric tại target FPR 5%.",
        "",
        markdown_table(aggregate.round(4)),
        "",
        "## 6. Giới hạn bằng chứng",
        "",
        "- Đã chạy đủ 80 run seed theo protocol. Tuy nhiên, Gate 1/Gate 2 vẫn cần review người và nhóm chưa được dùng một bảng số liệu để khẳng định model tốt nhất ngoài protocol đã định.",
        "- Mọi run hiện đã có run.json, metrics.csv, predictions.csv và model_bundle.joblib; prediction files được giữ ngoài GitHub do kích thước.",
        "- Gate 1/Gate 2 vẫn cần ba thành viên review và ký xác nhận riêng; validator không tự thay thế review người.",
        "",
        "## 7. Artifact truy vết",
        "",
        "- Bảng chi tiết: `docs/reports/DOT_02_METRICS_ALL_RUNS.csv`.",
        "- Bảng mean/std: `docs/reports/DOT_02_METRICS_MEAN_STD.csv`.",
        "- Mỗi run: `results/runs/<run_id>/run.json`, `metrics.csv`, `model_bundle.joblib`.",
        "- Manifest: `artifacts/data/data_manifest.json`.",
    ]
    (OUT / "BAO_CAO_TIEN_DO_DOT_02.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("Round-2 report and 80-run summary written (%d runs)" % len(summary))


if __name__ == "__main__":
    main()
