"""Post-hoc exact feature matching against each frozen run's actual fit set."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import average_precision_score

from nids_benchmark.data import feature_names, load_official_splits, make_development_split
from nids_benchmark.runner import RunRequest, _fingerprint_request
from analyze_pr_scores import sha256, unique_scores, verify_saved_metrics

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = {"CS": ("closed_set", None), "LR": ("loaco_reconnaissance", "Reconnaissance"),
             "LD": ("loaco_dos", "DoS"), "LE": ("loaco_exploits", "Exploits")}
MODELS = {"RF": "random_forest", "XGB": "xgboost", "IF": "isolation_forest", "AE": "autoencoder"}
SEEDS = (42, 52, 62, 72, 82)
METRICS = ("precision", "recall", "fpr", "known_recall", "uadr", "ap")


def model_fit_frame(development_train: pd.DataFrame, model: str) -> pd.DataFrame:
    return development_train.loc[development_train.label.eq(0)] if model in ("IF", "AE") else development_train


def exact_match_mask(fit: pd.DataFrame, test: pd.DataFrame, features: list[str]) -> np.ndarray:
    if not features or set(features) & {"id", "label", "attack_cat"}:
        raise ValueError("Match keys must contain features only")
    if fit[features].isna().any().any() or test[features].isna().any().any():
        raise ValueError("Missing feature values need an explicit matching policy")
    keys = pd.MultiIndex.from_frame(fit[features].drop_duplicates())
    return pd.MultiIndex.from_frame(test[features]).isin(keys)


def slice_stats(frame: pd.DataFrame) -> dict:
    y, pred = frame.y_true.to_numpy(), frame.y_pred.to_numpy()
    tp, fp = int(((y == 1) & (pred == 1)).sum()), int(((y == 0) & (pred == 1)).sum())
    fn, tn = int(((y == 1) & (pred == 0)).sum()), int(((y == 0) & (pred == 0)).sum())
    counts = {role: int(frame.evaluation_role.eq(role).sum())
              for role in ("normal", "known_attack", "heldout_attack")}
    ratio = lambda numerator, denominator: numerator / denominator if denominator else np.nan
    return dict(support=len(frame), normal_support=counts["normal"], known_support=counts["known_attack"],
                heldout_support=counts["heldout_attack"], tp=tp, fp=fp, fn=fn, tn=tn,
                precision=ratio(tp, tp + fp), recall=ratio(tp, tp + fn), fpr=ratio(fp, fp + tn),
                known_recall=float(frame.loc[frame.evaluation_role.eq("known_attack"), "y_pred"].mean()),
                uadr=float(frame.loc[frame.evaluation_role.eq("heldout_attack"), "y_pred"].mean()),
                ap=float(average_precision_score(y, frame.score)) if len(np.unique(y)) == 2 else np.nan)


def align_predictions(frame: pd.DataFrame, test: pd.DataFrame, run_id: str, heldout: str | None) -> pd.DataFrame:
    unique_scores(frame)
    reference = test.set_index("id").sort_index()
    if not reference.index.is_unique:
        raise ValueError("Raw test IDs are not unique")
    ordered = frame.sort_values(["target_fpr", "record_id"]).reset_index(drop=True)
    if not ordered.run_id.eq(run_id).all() or not ordered.split.eq("official_test").all():
        raise ValueError("Prediction run/split mismatch")
    roles = np.where(reference.label.eq(0), "normal",
                     np.where(reference.attack_cat.eq(heldout), "heldout_attack", "known_attack"))
    for _, part in ordered.groupby("target_fpr"):
        if not np.array_equal(part.record_id.to_numpy(), reference.index.to_numpy()):
            raise ValueError("Prediction ID coverage mismatch")
        if not np.array_equal(part.y_true.to_numpy(), reference.label.to_numpy()) or not np.array_equal(
                part.attack_cat.to_numpy(), reference.attack_cat.to_numpy()):
            raise ValueError("Prediction labels disagree with raw test")
        if not np.array_equal(part.evaluation_role.to_numpy(), roles):
            raise ValueError("Prediction evaluation roles disagree with scenario")
    return ordered


def validate_fit_bundle(path: Path, fit: pd.DataFrame, features: list[str], meta: dict) -> None:
    bundle = joblib.load(path)
    numeric = [c for c in features if c not in ("proto", "service", "state")]
    scaler = bundle["preprocessor"].named_transformers_["numeric"].named_steps["scaler"]
    if bundle["run_id"] != meta["run_id"] or bundle["features"] != features:
        raise ValueError("Saved model identity/features mismatch")
    if len(fit) != meta["row_counts"]["model_fit_rows"] or len(fit) != meta["row_counts"]["preprocessor_fit_rows"]:
        raise ValueError("Reconstructed fit row count mismatch")
    if scaler.n_samples_seen_ != len(fit) or not np.allclose(scaler.mean_, fit[numeric].mean(), rtol=1e-10, atol=1e-10):
        raise ValueError("Reconstructed fit mean mismatch")
    if not np.allclose(scaler.var_, fit[numeric].var(ddof=0), rtol=1e-10, atol=1e-10):
        raise ValueError("Reconstructed fit variance mismatch")


def summarize(rows: pd.DataFrame) -> pd.DataFrame:
    keys = ["scenario", "model", "cohort", "target_fpr"]
    groups = rows.groupby(keys, dropna=False)
    result = groups.agg(seed_count=("seed", "nunique"), support_min=("support", "min"), support_max=("support", "max"),
                        normal_min=("normal_support", "min"), normal_max=("normal_support", "max"),
                        known_min=("known_support", "min"), known_max=("known_support", "max"),
                        heldout_min=("heldout_support", "min"), heldout_max=("heldout_support", "max"))
    for metric in METRICS:
        result[f"{metric}_mean"] = groups[metric].mean()
        result[f"{metric}_std"] = groups[metric].std()
        result[f"{metric}_valid_seeds"] = groups[metric].count()
    if len(result) != 96 or not result.seed_count.eq(5).all():
        raise ValueError("Incomplete cohort/scenario/model/target/seed coverage")
    return result.reset_index()


def draw_figure(summary: pd.DataFrame, output: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.5), layout="constrained")
    for ax, (scenario, metric, title) in zip(axes, (("CS", "fpr", "Closed-set: Normal FPR"),
            ("CS", "recall", "Closed-set: Attack recall"), ("LR", "uadr", "LOACO Reconnaissance: UADR"))):
        for i, (cohort, color) in enumerate((("matched", "#386A52"), ("unmatched", "#9A523D"))):
            part = summary.query("scenario == @scenario and target_fpr == 0.05 and cohort == @cohort").set_index("model").reindex(MODELS)
            ax.bar(np.arange(4) + (i - .5) * .36, part[f"{metric}_mean"] * 100, width=.36,
                   yerr=part[f"{metric}_std"] * 100, color=color, label=cohort, capsize=3)
        ax.set_xticks(np.arange(4), list(MODELS)); ax.set_ylim(0, 105)
        ax.set_title(title, fontsize=11); ax.set_ylabel("Percent (%)")
        ax.grid(axis="y", alpha=.18); ax.set_axisbelow(True)
    axes[0].legend(loc="upper left")
    fig.suptitle("Exact match against actual model fit set; target validation FPR 5%\nMean/sample std, five seeds; cohorts differ by model and seed", fontsize=12)
    fig.savefig(output / "OVERLAP_SLICES.png", dpi=180); plt.close(fig)


def run_analysis(output: Path) -> dict:
    if output.exists() or output.resolve().is_relative_to((ROOT / "results/runs").resolve()):
        raise ValueError("Use a new output folder outside frozen runs")
    run_dirs = sorted((ROOT / "results/runs").iterdir())
    expected = {f"{s}-{m}-S{seed}" for s in SCENARIOS for m in MODELS for seed in SEEDS}
    if {p.name for p in run_dirs if p.is_dir()} != expected:
        raise ValueError("Expected exact locked 80-run matrix")
    protected = [ROOT / "data/raw" / f"UNSW_NB15_{s}-set.csv" for s in ("training", "testing")]
    protected += [p / name for p in run_dirs for name in ("run.json", "metrics.csv", "predictions.csv", "model_bundle.joblib")]
    protected += [ROOT / "artifacts/data/data_manifest.json", ROOT / "docs/evidence/dot_02/final_20261013/saved_split_audit.json",
                  ROOT / "docs/management/DAC_TA_OVERLAP_DOT_03_20261025.md", Path(__file__), ROOT / "scripts/analyze_pr_scores.py"]
    protected += [ROOT / "src/nids_benchmark" / f"{n}.py" for n in ("data", "runner", "models", "preprocessing", "evaluation", "contracts")]
    before = {p: sha256(p) for p in protected}
    raw = load_official_splits(ROOT / "data/raw")
    features = feature_names(raw.train)
    if len(features) != 42:
        raise ValueError("Expected 42 raw model features")
    manifest = json.loads((ROOT / "artifacts/data/data_manifest.json").read_text(encoding="utf-8"))
    for role, path in (("train", raw.train_path), ("test", raw.test_path)):
        if before[path] != manifest["files"][role]["sha256"]:
            raise ValueError("Raw data differs from baseline manifest")
    fingerprint = hashlib.sha256(f"{before[raw.train_path]}:{before[raw.test_path]}".encode("ascii")).hexdigest()
    split_audit = json.loads((ROOT / "docs/evidence/dot_02/final_20261013/saved_split_audit.json").read_text(encoding="utf-8"))
    audited = {row["run_id"]: row for row in split_audit["entries"]}
    test = raw.test.sort_values("id")
    records, fit_records, metric_checks, checked_rows = [], [], 0, 0
    for scenario, (scenario_name, heldout) in SCENARIOS.items():
        for seed in SEEDS:
            split = make_development_split(raw.train, heldout_class=heldout, seed=seed)
            partition_hash = hashlib.sha256(np.sort(split.train.id.to_numpy(dtype=np.int64)).tobytes()).hexdigest()
            match_cache = {}
            for model, model_name in MODELS.items():
                run_id = f"{scenario}-{model}-S{seed}"
                folder = ROOT / "results/runs" / run_id
                meta = json.loads((folder / "run.json").read_text(encoding="utf-8"))
                request = RunRequest(scenario_name, model_name, seed, ROOT / "data/raw", ROOT / "results/runs")
                if meta["status"] != "completed" or meta["data_fingerprint"] != fingerprint or meta["config_fingerprint"] != _fingerprint_request(request):
                    raise ValueError(f"Frozen run contract mismatch: {run_id}")
                if meta["software_versions"]["scikit_learn"] != sklearn.__version__:
                    raise ValueError("Use the baseline scikit-learn version to reconstruct partitions")
                if partition_hash != audited[run_id]["development_train_id_sha256"]:
                    raise ValueError("Reconstructed development IDs differ from audited partition")
                if len(split.train) != meta["row_counts"]["development_train"] or len(split.validation) != meta["row_counts"]["development_validation"]:
                    raise ValueError("Reconstructed development row count mismatch")
                fit = model_fit_frame(split.train, model)
                validate_fit_bundle(folder / "model_bundle.joblib", fit, features, meta)
                family = "normal_only" if model in ("IF", "AE") else "all_development_train"
                if family not in match_cache:
                    match_cache[family] = exact_match_mask(fit, test, features)
                matched = match_cache[family]
                frame = pd.read_csv(folder / "predictions.csv", float_precision="round_trip")
                checked_rows += len(frame)
                frame = align_predictions(frame, test, run_id, heldout)
                saved = pd.read_csv(folder / "metrics.csv", float_precision="round_trip")
                _, checks = verify_saved_metrics(meta, frame, saved, average_precision_score(
                    frame.loc[frame.target_fpr.eq(.01), "y_true"], frame.loc[frame.target_fpr.eq(.01), "score"]))
                metric_checks += checks
                fit_records.append(dict(run_id=run_id, fit_scope=family, fit_rows=len(fit),
                    development_train_id_sha256=partition_hash,
                    model_fit_id_sha256=hashlib.sha256(np.sort(fit.id.to_numpy(dtype=np.int64)).tobytes()).hexdigest(),
                    matched_test_rows=int(matched.sum()), fit_bundle_checked=True))
                for target, part in frame.groupby("target_fpr", sort=True):
                    stats = {}
                    for cohort, mask in (("all", np.ones(len(test), dtype=bool)), ("matched", matched), ("unmatched", ~matched)):
                        stats[cohort] = slice_stats(part.loc[mask])
                        records.append(dict(run_id=run_id, scenario=scenario, model=model, seed=seed, fit_scope=family,
                            cohort=cohort, target_fpr=target, threshold=float(part.threshold.iloc[0]), **stats[cohort]))
                    for key in ("support", "normal_support", "known_support", "heldout_support", "tp", "fp", "fn", "tn"):
                        if stats["all"][key] != stats["matched"][key] + stats["unmatched"][key]:
                            raise ValueError(f"Cohort reconciliation failed: {run_id}/{key}")
            print(f"Validated {scenario}/seed {seed}: {len(fit_records)}/80", flush=True)
    rows = pd.DataFrame(records)
    summary = summarize(rows)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".overlap_", dir=output.parent) as temporary:
        staging = Path(temporary) / "bundle"; staging.mkdir()
        rows.to_csv(staging / "OVERLAP_ALL_RUNS.csv", index=False)
        summary.to_csv(staging / "OVERLAP_MEAN_STD.csv", index=False)
        pd.DataFrame(fit_records).to_csv(staging / "FIT_SET_CHECKS.csv", index=False)
        draw_figure(summary, staging)
        if any(sha256(p) != value for p, value in before.items()):
            raise ValueError("Protected input changed during analysis")
        audit = dict(created_at_utc=datetime.now(timezone.utc).isoformat(),
            base_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            run_count=len(fit_records), prediction_rows_checked=checked_rows, saved_metric_checks=metric_checks,
            cohort_rows=len(rows), cohort_groups=len(summary), feature_count=len(features),
            inputs_unchanged=True, training_performed=False, threshold_tuning_performed=False,
            method="Exact raw 42-feature match against reconstructed model fit set; verified stored scaler, counts and prior partition ID hash",
            limitations="Post-hoc slice association, not causal overlap removal; cohorts differ by model/seed; same test over seeds, no independent confidence interval",
            missing_metric_policy="NaN for absent denominator; AP requires both labels; valid seed count recorded",
            versions=dict(python=platform.python_version(), numpy=np.__version__, pandas=pd.__version__, sklearn=sklearn.__version__),
            inputs=[dict(path=str(p.relative_to(ROOT)), sha256=value) for p,value in before.items()])
        (staging / "OVERLAP_AUDIT.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        staging.rename(output)
    return audit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "docs/evidence/dot_03/overlap_20261025")
    args = parser.parse_args()
    result = run_analysis(args.output.resolve())
    print(json.dumps({k:v for k,v in result.items() if k != "inputs"}, ensure_ascii=False, indent=2))
