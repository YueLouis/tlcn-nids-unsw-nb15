"""Summarize saved official-test predictions without fitting models or thresholds."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


SUPPORT = {"Normal": 37000, "Analysis": 677, "Backdoor": 583, "DoS": 4089,
           "Exploits": 11132, "Fuzzers": 6062, "Generic": 18871,
           "Reconnaissance": 3496, "Shellcode": 378, "Worms": 44}


def sha256(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def analyze(runs: Path, output: Path) -> dict:
    folders = sorted(p for p in runs.iterdir() if p.is_dir())
    expected = {f"{s}-{m}-S{seed}" for s in ("CS", "LR", "LD", "LE")
                for m in ("RF", "XGB", "IF", "AE") for seed in (42, 52, 62, 72, 82)}
    if {p.name for p in folders} != expected:
        raise ValueError("Run matrix is incomplete or contains unexpected folders")
    rows, examples, provenance = [], [], []
    checked_rows = metric_checks = 0
    for folder in folders:
        path = folder / "predictions.csv"
        before = sha256(path)
        meta = json.loads((folder / "run.json").read_text(encoding="utf-8"))
        df = pd.read_csv(path)
        if set(df.run_id) != {folder.name} or set(df.split) != {"official_test"}:
            raise ValueError(f"Invalid provenance: {folder.name}")
        if len(df) != 164664 or df.duplicated(["record_id", "target_fpr"]).any():
            raise ValueError(f"Invalid prediction row coverage: {folder.name}")
        if not np.isfinite(df[["score", "threshold"]].to_numpy()).all():
            raise ValueError(f"Nonfinite score: {folder.name}")
        if not ((df.score >= df.threshold).astype(int) == df.y_pred).all():
            raise ValueError(f"Prediction/threshold mismatch: {folder.name}")
        if not ((df.attack_cat != "Normal").astype(int) == df.y_true).all():
            raise ValueError(f"Label/category mismatch: {folder.name}")
        metrics = pd.read_csv(folder / "metrics.csv")
        scenario, model, _ = folder.name.split("-")
        for target, part in df.groupby("target_fpr"):
            if target not in (0.01, 0.05) or part.attack_cat.value_counts().to_dict() != SUPPORT:
                raise ValueError(f"Category coverage mismatch: {folder.name}/{target}")
            heldout = meta["heldout_class"]
            role = np.where(part.attack_cat == "Normal", "normal",
                            np.where(part.attack_cat == heldout, "heldout_attack", "known_attack"))
            if not (part.evaluation_role == role).all():
                raise ValueError(f"Role mismatch: {folder.name}")
            fp = int(((part.y_true == 0) & (part.y_pred == 1)).sum())
            tn = int(((part.y_true == 0) & (part.y_pred == 0)).sum())
            tp = int(((part.y_true == 1) & (part.y_pred == 1)).sum())
            fn = int(((part.y_true == 1) & (part.y_pred == 0)).sum())
            check = {("normal", "fpr"): fp / (fp + tn),
                     ("all", "precision"): tp / (tp + fp) if tp + fp else 0.0,
                     ("all", "recall"): tp / (tp + fn)}
            for role_name, metric_name in (("known_attack", "recall"), ("heldout_attack", "uadr")):
                subset = part[part.evaluation_role == role_name]
                if len(subset):
                    check[(role_name, metric_name)] = float(subset.y_pred.mean())
            for (subset, metric), value in check.items():
                saved = metrics[(metrics.target_fpr == target) & (metrics.subset == subset) & (metrics.metric == metric)]
                if len(saved) != 1 or not np.isclose(float(saved.iloc[0].value), value, atol=1e-12, rtol=0):
                    raise ValueError(f"Metric mismatch: {folder.name}/{target}/{metric}")
                metric_checks += 1
            for category, group in part.groupby("attack_cat"):
                normal = category == "Normal"
                error_count = int((group.y_pred != group.y_true).sum())
                rows.append(dict(run_id=folder.name, scenario=scenario, model=model, seed=meta["seed"],
                                 target_fpr=target, attack_cat=category, evaluation_role=group.evaluation_role.iloc[0],
                                 support=len(group), error_type="FP" if normal else "FN",
                                 error_count=error_count, correct_count=len(group)-error_count,
                                 error_rate=error_count/len(group)))
            # Deterministic examples for traceability, not a statistical sample or causal explanation.
            if meta["seed"] == 42 and scenario == "CS" and target == 0.05:
                for error_type, mask in (("FP", (part.y_true == 0) & (part.y_pred == 1)),
                                         ("FN", (part.y_true == 1) & (part.y_pred == 0))):
                    for row in part[mask].sort_values("record_id").head(2).to_dict("records"):
                        row.update(error_type=error_type, selection="lowest_record_id_in_error_subset",
                                   score_minus_threshold=row["score"]-row["threshold"])
                        examples.append(row)
        after = sha256(path)
        if after != before:
            raise ValueError(f"Input changed during analysis: {folder.name}")
        checked_rows += len(df)
        provenance.append(dict(run_id=folder.name, predictions_sha256=before))
    all_rows = pd.DataFrame(rows)
    group_keys = ["scenario", "model", "target_fpr", "attack_cat", "evaluation_role", "support", "error_type"]
    summary = all_rows.groupby(group_keys, as_index=False).agg(
        seed_count=("seed", "count"), error_count_mean=("error_count", "mean"),
        error_rate_mean=("error_rate", "mean"), error_rate_std=("error_rate", "std"))
    if not (summary.seed_count == 5).all() or len(summary) != 320:
        raise ValueError("Seed aggregation is incomplete")
    output.mkdir(parents=True, exist_ok=True)
    all_rows.to_csv(output / "CATEGORY_ERRORS_ALL_RUNS.csv", index=False)
    summary.to_csv(output / "CATEGORY_ERRORS_MEAN_STD.csv", index=False)
    pd.DataFrame(examples).to_csv(output / "ERROR_EXAMPLES_CS_S42.csv", index=False)
    audit = dict(run_count=len(folders), category_rows=len(all_rows), summary_rows=len(summary),
                 prediction_rows_checked=checked_rows, metric_checks=metric_checks,
                 original_predictions_unchanged=True, training_performed=False,
                 denominator="Normal support for FP; each attack category support for FN",
                 std="sample standard deviation across five seeds (ddof=1)",
                 examples_policy="first two by record_id per model/error_type; CS seed42 target5%; not representative",
                 failure_count=0, inputs=provenance)
    (output / "category_error_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    return audit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, default=Path("results/runs"))
    parser.add_argument("--output", type=Path, default=Path("docs/evidence/dot_02/category_errors_20261014"))
    args = parser.parse_args()
    result = analyze(args.runs, args.output)
    print(json.dumps({k: v for k, v in result.items() if k != "inputs"}, indent=2))
