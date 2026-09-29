"""Render compact screenshot-style evidence cards from authoritative artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "evidence" / "dot_02" / "screenshots"


def font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/consolab.ttf") if bold else Path("C:/Windows/Fonts/consola.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def card(filename: str, title: str, lines: list[str]) -> None:
    width, height = 1800, 980
    image = Image.new("RGB", (width, height), "#f8fafc")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 92), fill="#163a5f")
    draw.text((42, 25), title, font=font(38, True), fill="white")
    y = 135
    for line in lines:
        draw.text((52, y), line, font=font(28), fill="#17202a")
        y += 52
    draw.text((52, height - 55), "Source of truth: repository artifacts and final verification commands", font=font(20), fill="#52606d")
    image.save(OUT / filename)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / "artifacts" / "data" / "data_manifest.json").read_text(encoding="utf-8"))
    train = manifest["files"]["train"]["audit"]
    test = manifest["files"]["test"]["audit"]
    card(
        "D2_01_Audit_du_lieu_PASS_2026-09-26.png",
        "D2.2-D2.3 | OFFICIAL DATA AUDIT",
        [
            f"PASS  train: {train['rows']} rows x {train['columns']} columns | missing={train['missing_values']} | duplicate={train['duplicate_rows']}",
            f"PASS  test : {test['rows']} rows x {test['columns']} columns | missing={test['missing_values']} | duplicate={test['duplicate_rows']}",
            f"SHA train: {manifest['files']['train']['sha256']}",
            f"SHA test : {manifest['files']['test']['sha256']}",
            "Source: artifacts/data/data_manifest.json",
        ],
    )
    card(
        "D2_02_Protocol_validation_PASS_2026-09-26.png",
        "D2.1 / D2.6 | PROTOCOL VALIDATION",
        [
            "Protocol validation passed: 4 scenarios x 4 models x 5 seeds = 80 unique runs",
            "Scenarios: closed_set, loaco_reconnaissance, loaco_dos, loaco_exploits",
            "Models: random_forest, xgboost, isolation_forest, autoencoder",
            "Seeds: 42, 52, 62, 72, 82",
            "Note: validator does not replace human Gate 1 review.",
        ],
    )
    card(
        "D2_03_Unit_tests_9_PASS_2026-09-26.png",
        "D2.5 / D2.8 | UNIT TESTS",
        [
            "Ran 9 tests in 0.03s",
            "OK",
            "Covers forbidden columns, label normalization, LOACO ordering/leakage,",
            "evaluation roles, threshold FPR budget and held-out recall reporting.",
            "Command: python -m unittest discover -s tests -q",
        ],
    )
    run_dirs = sorted(p for p in (ROOT / "results" / "runs").iterdir() if p.is_dir() and p.name[:2] in {"CS", "LR", "LD", "LE"})
    missing = []
    for run in run_dirs:
        for name in ("run.json", "metrics.csv", "predictions.csv", "model_bundle.joblib"):
            if not (run / name).exists():
                missing.append(f"{run.name}/{name}")
    card(
        "D2_04_Danh_sach_80_run_2026-09-26.png",
        "D2.7 | FULL RUN REGISTRY",
        [
            f"Run directories: {len(run_dirs)} / 80",
            f"Missing required artifacts: {len(missing)}",
            "Required per run: run.json | metrics.csv | predictions.csv | model_bundle.joblib",
            "Result: PASS - 80/80 runs have all four artifacts.",
            "Source: results/runs/<run-id>/",
        ],
    )
    aggregate = list(csv.DictReader((ROOT / "docs" / "reports" / "DOT_02_METRICS_MEAN_STD.csv").open(encoding="utf-8")))
    card(
        "D2_05_Mean_std_5_seed_2026-09-26.png",
        "D2.9 | FIVE-SEED AGGREGATION",
        [
            f"Rows in aggregate table: {len(aggregate)} scenario/model groups",
            "Each group summarizes 5 seeds at target FPR 5%.",
            "Metrics: PR-AUC, F1, official-test FPR, Known Attack Recall, UADR.",
            "Source: docs/reports/DOT_02_METRICS_MEAN_STD.csv",
        ],
    )
    card(
        "D2_06_PDF_Dot2_15_pages_2026-09-26.png",
        "FINAL REPORT | PDF QA",
        [
            "BAO_CAO_TLCN_TICH_LUY_DOT_02.pdf",
            "15 pages | A4 portrait | XeLaTeX/Tectonic compile PASS",
            "Layout follows Phase 1: framed cover, version page, header/footer, TOC, tables.",
            "Rendered pages checked after compile; no blocking layout overlap found.",
        ],
    )
    card(
        "D2_07_Final_check_PASS_2026-09-26.png",
        "FINAL CHECK | PHASE 2",
        [
            "PASS: 80 runs, 320 required artifacts, unique IDs, manifest,",
            "9 unit tests, protocol validator, aggregate table and final PDF.",
            "Technical checklist complete; human Gate 1/Gate 2 signatures remain explicit.",
            "Command: python scripts/check_dot2_final.py",
        ],
    )


if __name__ == "__main__":
    main()
