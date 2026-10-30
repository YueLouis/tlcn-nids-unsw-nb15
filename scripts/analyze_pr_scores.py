"""Round-3 PR/score diagnostics from frozen predictions; no training or tuning."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import tempfile
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import average_precision_score, precision_recall_curve


ROOT = Path(__file__).resolve().parents[1]
MODELS = ("RF", "XGB", "IF", "AE")
SCENARIOS = {"CS": "Closed-set", "LR": "LOACO Reconnaissance",
             "LD": "LOACO DoS", "LE": "LOACO Exploits"}
ROLES = {"normal": "Normal", "known_attack": "Known attack", "heldout_attack": "Held-out attack"}


def sha256(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def unique_scores(frame: pd.DataFrame) -> pd.DataFrame:
    """Reject mismatched/duplicate target copies before computing ranking metrics."""
    if set(frame.target_fpr) != {0.01, 0.05}:
        raise ValueError("Expected both validation FPR targets")
    if frame.duplicated(["record_id", "target_fpr"]).any():
        raise ValueError("Duplicate record within a target")
    if not np.isfinite(frame[["score", "threshold"]].to_numpy()).all():
        raise ValueError("Nonfinite score or threshold")
    if not frame.y_true.isin([0, 1]).all() or not frame.y_pred.isin([0, 1]).all():
        raise ValueError("Nonbinary labels or predictions")
    if not np.array_equal((frame.score >= frame.threshold).astype(int), frame.y_pred):
        raise ValueError("Stored prediction disagrees with score >= threshold")
    parts = [frame[frame.target_fpr == target].sort_values("record_id").reset_index(drop=True)
             for target in (0.01, 0.05)]
    columns = ["record_id", "run_id", "split", "attack_cat", "evaluation_role", "y_true", "score"]
    if not parts[0][columns].equals(parts[1][columns]):
        raise ValueError("The two target copies disagree on record identity, labels, roles or score")
    return parts[0]


def confusion(labels: np.ndarray, predicted: np.ndarray) -> dict:
    tp = int(((labels == 1) & (predicted == 1)).sum())
    fp = int(((labels == 0) & (predicted == 1)).sum())
    fn = int(((labels == 1) & (predicted == 0)).sum())
    tn = int(((labels == 0) & (predicted == 0)).sum())
    return dict(tp=tp, fp=fp, fn=fn, tn=tn,
                precision=tp / (tp + fp) if tp + fp else 0.0,
                recall=tp / (tp + fn) if tp + fn else np.nan,
                f1=2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0,
                fpr=fp / (fp + tn) if fp + tn else np.nan)


def verify_saved_metrics(meta: dict, frame: pd.DataFrame, saved: pd.DataFrame, ap: float) -> tuple[list, int]:
    expected = [("all", "pr_auc", None, ap, len(frame) // 2)]
    points = []
    for selection in meta["threshold_policy"]["selections"]:
        target, threshold = selection["target_fpr"], selection["threshold"]
        part = frame[frame.target_fpr == target]
        if len(part) * 2 != len(frame) or not np.allclose(part.threshold, threshold, atol=1e-12, rtol=0):
            raise ValueError("Threshold metadata/row coverage mismatch")
        stats = confusion(part.y_true.to_numpy(), part.y_pred.to_numpy())
        for metric in ("precision", "recall", "f1"):
            expected.append(("all", metric, target, stats[metric], len(part)))
        for role, metric in (("normal", "fpr"), ("known_attack", "recall"), ("heldout_attack", "uadr")):
            subset = part[part.evaluation_role == role]
            expected.append((role, metric, target, float(subset.y_pred.mean()) if len(subset) else np.nan, len(subset)))
        points.append(dict(target_fpr=target, threshold=threshold,
                           known_recall=float(part.loc[part.evaluation_role == "known_attack", "y_pred"].mean()),
                           uadr=float(part.loc[part.evaluation_role == "heldout_attack", "y_pred"].mean()),
                           **stats))
    if len(expected) != 13 or len(saved) != 13:
        raise ValueError("Expected exactly 13 saved metrics")
    for subset, metric, target, value, support in expected:
        match = saved[(saved.subset == subset) & (saved.metric == metric)
                      & (saved.target_fpr.isna() if target is None else saved.target_fpr == target)]
        if len(match) != 1:
            raise ValueError(f"Missing or duplicate metric: {subset}/{metric}/{target}")
        row = match.iloc[0]
        if int(row.support) != support or not np.isclose(row.value, value, atol=1e-12, rtol=0, equal_nan=True):
            raise ValueError(f"Saved metric mismatch: {subset}/{metric}/{target}")
        threshold = np.nan if target is None else next(
            selection["threshold"] for selection in meta["threshold_policy"]["selections"]
            if selection["target_fpr"] == target)
        if not np.isclose(row.threshold, threshold, atol=1e-12, rtol=0, equal_nan=True):
            raise ValueError(f"Saved metric threshold mismatch: {subset}/{metric}/{target}")
    return points, len(expected)


def scope_frames(part: pd.DataFrame) -> dict[str, pd.DataFrame]:
    scopes = {"all": part}
    if part.evaluation_role.eq("heldout_attack").any():
        scopes["normal_vs_heldout"] = part[part.evaluation_role.isin(["normal", "heldout_attack"])]
    return scopes


def draw_figures(examples: dict, output: Path) -> int:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    count = 0
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    for scenario, title in SCENARIOS.items():
        for scope in (("all",) if scenario == "CS" else ("all", "normal_vs_heldout")):
            fig, ax = plt.subplots(figsize=(8.8, 6.2), layout="constrained")
            for model in MODELS:
                part, meta = examples[(scenario, model)]
                data = scope_frames(part)[scope]
                precision, recall, _ = precision_recall_curve(data.y_true, data.score)
                ap = average_precision_score(data.y_true, data.score)
                line, = ax.plot(recall, precision, label=f"{model}: AP={ap:.4f}", lw=1.8)
                for selection, marker in zip(meta["threshold_policy"]["selections"], ("o", "s")):
                    stats = confusion(data.y_true.to_numpy(), (data.score >= selection["threshold"]).to_numpy())
                    ax.scatter(stats["recall"], stats["precision"], color=line.get_color(), marker=marker, s=40, zorder=4)
            prevalence = float(data.y_true.mean())
            ax.axhline(prevalence, ls="--", color="gray", label=f"Positive prevalence={prevalence:.4f}")
            ax.set(xlim=(0, 1.01), ylim=(0, 1.02), xlabel="Recall", ylabel="Precision",
                   title=f"{title} | {scope} | seed 42\nCircles: validation target 1%; squares: 5%")
            ax.grid(alpha=0.2)
            legend_corner = "upper right" if (scenario, scope) == ("LR", "normal_vs_heldout") else "lower left"
            ax.legend(loc=legend_corner, fontsize=9)
            fig.savefig(output / f"PR_{scenario}_{scope}_S42.png", dpi=170)
            plt.close(fig)
            count += 1
        fig, axes = plt.subplots(2, 2, figsize=(12, 8), layout="constrained")
        for ax, model in zip(axes.flat, MODELS):
            part, meta = examples[(scenario, model)]
            linthresh = max(float(np.quantile(np.abs(part.score), 0.95)) * 0.01, 1e-10)
            for role, label in ROLES.items():
                values = np.sort(part.loc[part.evaluation_role == role, "score"].to_numpy())
                if len(values):
                    ax.step(values, np.arange(1, len(values) + 1) / len(values), where="post",
                            label=f"{label} (n={len(values):,})", lw=1.5)
            for selection, style in zip(meta["threshold_policy"]["selections"], (":", "--")):
                ax.axvline(selection["threshold"], color="black", ls=style, lw=1,
                           label=f"Val target {selection['target_fpr']:.0%}")
            ax.set_xscale("symlog", linthresh=linthresh)
            ax.set(title=model, xlabel="Raw score (symlog scale)", ylabel="Empirical cumulative fraction", ylim=(0, 1.02))
            ax.grid(alpha=0.2)
            ax.legend(fontsize=8, loc="upper left")
        fig.suptitle(f"{title} | score distributions | seed 42\nEach role normalized separately; thresholds fixed on validation")
        fig.savefig(output / f"SCORE_ECDF_{scenario}_S42.png", dpi=150)
        plt.close(fig)
        count += 1
    return count


def analyze(runs: Path, output: Path, raw_test: Path, matrix: Path) -> dict:
    runs, output = runs.resolve(), output.resolve()
    protected = [runs, ROOT / "data", ROOT / "docs/report_cumulative", ROOT / "docs/evidence/dot_02", ROOT / "output/pdf"]
    if any(output == path.resolve() or output.is_relative_to(path.resolve()) or path.resolve().is_relative_to(output)
           for path in protected):
        raise ValueError("Output overlaps a protected input/report directory")
    if output.exists():
        raise FileExistsError("Use a new output directory to preserve previous diagnostics")
    matrix_frame = pd.read_csv(matrix).fillna({"heldout_class": ""})
    folders = {folder.name: folder for folder in runs.iterdir() if folder.is_dir()}
    if len(matrix_frame) != 80 or set(folders) != set(matrix_frame.run_id) or matrix_frame.run_id.duplicated().any():
        raise ValueError("Expected exactly the 80 protocol run IDs")
    paths = [raw_test.resolve(), matrix.resolve(), Path(__file__).resolve()]
    paths += [folder / name for folder in folders.values() for name in ("run.json", "metrics.csv", "predictions.csv")]
    before = {path: sha256(path) for path in paths}
    reference = pd.read_csv(raw_test, usecols=["id", "label", "attack_cat"]).sort_values("id").reset_index(drop=True)
    if len(reference) != 82332 or reference.id.duplicated().any():
        raise ValueError("Official-test record count/identity mismatch")
    ap_rows, point_rows, quantiles, examples = [], [], [], {}
    prediction_rows = metric_checks = 0
    for index, record in enumerate(matrix_frame.to_dict("records"), 1):
        run_id = record["run_id"]
        folder = folders[run_id]
        meta = json.loads((folder / "run.json").read_text(encoding="utf-8"))
        if any(meta[key] != record[key] for key in ("run_id", "scenario", "model", "seed")):
            raise ValueError(f"Run metadata disagrees with matrix: {run_id}")
        if (meta["heldout_class"] or "") != record["heldout_class"] or meta["status"] != "completed":
            raise ValueError(f"Incomplete or wrong held-out run: {run_id}")
        if meta["threshold_policy"]["source_split"] != "normal_validation":
            raise ValueError(f"Invalid threshold source: {run_id}")
        if [s["target_fpr"] for s in meta["threshold_policy"]["selections"]] != [0.01, 0.05]:
            raise ValueError(f"Unexpected threshold policy: {run_id}")
        # Preserve adjacent float64 scores and ties across CSV serialization.
        frame = pd.read_csv(folder / "predictions.csv", float_precision="round_trip")
        part = unique_scores(frame)
        if set(frame.run_id) != {run_id} or set(frame.split) != {"official_test"}:
            raise ValueError(f"Prediction provenance mismatch: {run_id}")
        if len(part) != len(reference) or not np.array_equal(part.record_id, reference.id):
            raise ValueError(f"Official-test identity mismatch: {run_id}")
        if not np.array_equal(part.y_true, reference.label) or not np.array_equal(part.attack_cat, reference.attack_cat):
            raise ValueError(f"Official-test labels mismatch: {run_id}")
        roles = np.where(reference.label == 0, "normal",
                         np.where(reference.attack_cat == meta["heldout_class"], "heldout_attack", "known_attack"))
        if not np.array_equal(part.evaluation_role, roles):
            raise ValueError(f"Incorrect evaluation roles: {run_id}")
        scenario, model, _ = run_id.split("-")
        identity = dict(run_id=run_id, scenario=scenario, model=model, seed=meta["seed"])
        scopes = scope_frames(part)
        for scope, data in scopes.items():
            ap = float(average_precision_score(data.y_true, data.score))
            ap_rows.append(dict(**identity, scope=scope, support=len(data), positives=int(data.y_true.sum()),
                                prevalence=float(data.y_true.mean()), ap=ap))
        ap_all = ap_rows[-len(scopes)]["ap"]
        saved = pd.read_csv(folder / "metrics.csv", float_precision="round_trip")
        if set(saved.run_id) != {run_id} or set(saved.split) != {"official_test"}:
            raise ValueError(f"Saved metric provenance mismatch: {run_id}")
        points, checks = verify_saved_metrics(meta, frame, saved, ap_all)
        point_rows += [dict(**identity, **point) for point in points]
        for role, data in part.groupby("evaluation_role"):
            values = np.quantile(data.score, [0, 0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1])
            quantiles.append(dict(**identity, role=role, support=len(data),
                                  **dict(zip(("min", "q01", "q05", "q25", "q50", "q75", "q95", "q99", "max"), values))))
        if meta["seed"] == 42:
            examples[(scenario, model)] = (part, meta)
        prediction_rows += len(frame)
        metric_checks += checks
        if index % 20 == 0:
            print(f"Validated {index}/80 runs", flush=True)
    aps, points = pd.DataFrame(ap_rows), pd.DataFrame(point_rows)
    summary = aps.groupby(["scenario", "model", "scope"], as_index=False).agg(
        seed_count=("seed", "nunique"), support=("support", "first"), positives=("positives", "first"),
        prevalence=("prevalence", "first"), ap_mean=("ap", "mean"), ap_std=("ap", "std"))
    point_summary = points.groupby(["scenario", "model", "target_fpr"], as_index=False).agg(
        seed_count=("seed", "nunique"), fpr_mean=("fpr", "mean"), fpr_std=("fpr", "std"),
        recall_mean=("recall", "mean"), recall_std=("recall", "std"),
        known_recall_mean=("known_recall", "mean"), known_recall_std=("known_recall", "std"),
        uadr_mean=("uadr", "mean"), uadr_std=("uadr", "std"))
    if len(summary) != 28 or len(point_summary) != 32 or not (summary.seed_count == 5).all() or not (point_summary.seed_count == 5).all():
        raise ValueError("Incomplete five-seed aggregation")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".pr_scores_", dir=output.parent) as temporary:
        staging = Path(temporary) / "bundle"
        staging.mkdir()
        for name, data in (("AP_ALL_RUNS", aps), ("AP_MEAN_STD", summary),
                           ("OPERATING_POINTS_ALL_RUNS", points), ("OPERATING_POINTS_MEAN_STD", point_summary),
                           ("SCORE_QUANTILES_ALL_RUNS", pd.DataFrame(quantiles))):
            data.to_csv(staging / f"{name}.csv", index=False)
        figure_count = draw_figures(examples, staging)
        if any(sha256(path) != fingerprint for path, fingerprint in before.items()):
            raise ValueError("Protected input changed during diagnostics")
        audit = dict(created_at_utc=datetime.now(timezone.utc).isoformat(),
                     base_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                     run_count=80, prediction_rows_checked=prediction_rows, unique_record_run_pairs=80 * len(reference),
                     saved_metric_checks=metric_checks, ap_rows=len(aps), ap_groups=len(summary),
                     operating_point_groups=len(point_summary), figure_count=figure_count,
                     inputs_unchanged=True, training_performed=False, threshold_tuning_performed=False,
                     plot_seed=42, plot_policy="seed42 declared before analysis; other seeds summarized numerically",
                     ap_definition="average_precision_score; not trapezoidal PR-AUC; one copy per record/run",
                     std_definition="sample std across five seeds on the same official test; not a confidence interval",
                     normal_vs_heldout_scope="Excludes known attacks; prevalence differs by scenario; AP not directly comparable across scopes",
                     versions=dict(python=platform.python_version(), numpy=np.__version__, pandas=pd.__version__,
                                   sklearn=sklearn.__version__, matplotlib=version("matplotlib")),
                     inputs=[dict(path=str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path), sha256=value)
                             for path, value in before.items()])
        (staging / "PR_SCORE_AUDIT.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
        staging.rename(output)
    return audit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, default=ROOT / "results/runs")
    parser.add_argument("--output", type=Path, default=ROOT / "docs/evidence/dot_03/pr_scores_20261022")
    parser.add_argument("--raw-test", type=Path, default=ROOT / "data/raw/UNSW_NB15_testing-set.csv")
    parser.add_argument("--matrix", type=Path, default=ROOT / "docs/protocol/RUN_MATRIX.csv")
    args = parser.parse_args()
    result = analyze(args.runs, args.output, args.raw_test, args.matrix)
    print(json.dumps({key: value for key, value in result.items() if key != "inputs"}, indent=2))
