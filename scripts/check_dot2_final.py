"""Final audit for the Phase 2 deliverables."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("run.json", "metrics.csv", "predictions.csv", "model_bundle.joblib")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> None:
    runs = sorted(p for p in (ROOT / "results" / "runs").iterdir() if p.is_dir() and p.name[:2] in {"CS", "LR", "LD", "LE"})
    if len(runs) != 80:
        fail(f"expected 80 run directories, found {len(runs)}")
    missing = [f"{run.name}/{name}" for run in runs for name in REQUIRED if not (run / name).exists()]
    if missing:
        fail(f"missing artifacts: {missing[:3]}")
    run_ids = [json.loads((run / "run.json").read_text(encoding="utf-8"))["run_id"] for run in runs]
    statuses = [json.loads((run / "run.json").read_text(encoding="utf-8"))["status"] for run in runs]
    bad_status = [run.name for run, st in zip(runs, statuses) if st != "completed"]
    if bad_status:
        fail(f"runs with non-completed status: {bad_status[:3]}")
    SCENARIOS = ["CS", "LR", "LD", "LE"]
    MODELS = ["RF", "XGB", "IF", "AE"]
    SEEDS = [42, 52, 62, 72, 82]
    expected_ids = {f"{s}-{m}-S{seed}" for s in SCENARIOS for m in MODELS for seed in SEEDS}
    actual_ids = set(run_ids)
    if actual_ids != expected_ids:
        missing = expected_ids - actual_ids
        extra = actual_ids - expected_ids
        fail(f"run_id mismatch: missing={missing}, extra={extra}")
    if len(set(run_ids)) != 80:
        fail("run IDs are not unique")
    aggregate = ROOT / "docs" / "reports" / "DOT_02_METRICS_MEAN_STD.csv"
    if not aggregate.exists() or sum(1 for _ in aggregate.open(encoding="utf-8")) != 17:
        fail("mean/std table does not contain 16 groups plus header")
    manifest = json.loads((ROOT / "artifacts" / "data" / "data_manifest.json").read_text(encoding="utf-8"))
    if manifest["files"]["train"]["audit"]["rows"] != 175341 or manifest["files"]["test"]["audit"]["rows"] != 82332:
        fail("manifest row counts changed")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q"], cwd=ROOT, env=env, capture_output=True, text=True)
    if result.returncode:
        print(result.stdout)
        print(result.stderr)
        fail("unit tests failed")
    test_match = re.search(r"Ran (\d+) tests?", result.stderr + result.stdout)
    test_count = test_match.group(1) if test_match else "?"
    result = subprocess.run([sys.executable, "scripts/validate_protocol.py"], cwd=ROOT, env=env, capture_output=True, text=True)
    if result.returncode:
        print(result.stdout)
        print(result.stderr)
        fail("protocol validator failed")
    pdf = ROOT / "output" / "pdf" / "NhomTLCN_TramAnh_VuongThu_TrongTin_dot2.pdf"
    if not pdf.exists() or pdf.stat().st_size < 100000:
        fail("final PDF missing or unexpectedly small")
    tex = ROOT / "docs" / "report_cumulative" / "BAO_CAO_TLCN_TICH_LUY_DOT_02.tex"
    if tex.exists() and pdf.stat().st_mtime < tex.stat().st_mtime:
        fail("PDF is older than LaTeX source — rebuild needed")
    print(f"PASS: 80 runs, 320 required artifacts, unique IDs, manifest, {test_count} tests, validator, aggregate table and PDF")


if __name__ == "__main__":
    main()
