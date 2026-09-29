"""Threshold selection and protocol-aligned metric generation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, f1_score, precision_score, recall_score


@dataclass(frozen=True)
class ThresholdSelection:
    target_fpr: float
    threshold: float
    validation_fpr: float
    support: int


def select_threshold(normal_scores: np.ndarray, target_fpr: float) -> ThresholdSelection:
    scores = np.asarray(normal_scores, dtype=float)
    if scores.size == 0:
        raise ValueError("Normal validation scores are empty")
    if not np.isfinite(scores).all():
        raise ValueError("Normal validation scores contain NaN or infinity")
    if not 0 <= target_fpr < 1:
        raise ValueError("target_fpr must be in [0, 1)")

    candidates = np.concatenate(
        [np.unique(scores), [np.nextafter(float(scores.max()), np.inf)]]
    )
    false_positive_rates = np.array([(scores >= value).mean() for value in candidates])
    valid = np.flatnonzero(false_positive_rates <= target_fpr)
    if valid.size == 0:
        raise RuntimeError("No threshold satisfies the requested FPR")
    index = int(valid[0])
    return ThresholdSelection(
        target_fpr=float(target_fpr),
        threshold=float(candidates[index]),
        validation_fpr=float(false_positive_rates[index]),
        support=int(scores.size),
    )


def evaluation_roles(frame: pd.DataFrame, heldout_class: str | None) -> np.ndarray:
    roles = np.full(len(frame), "known_attack", dtype=object)
    roles[frame["label"].to_numpy() == 0] = "normal"
    if heldout_class:
        heldout = frame["label"].eq(1) & frame["attack_cat"].eq(heldout_class)
        roles[heldout.to_numpy()] = "heldout_attack"
    return roles


def _safe_rate(numerator: int, denominator: int) -> float | None:
    return None if denominator == 0 else float(numerator / denominator)


def _metric_row(
    *,
    run_id: str,
    subset: str,
    metric: str,
    value: float | None,
    support: int,
    target_fpr: float | None,
    threshold: float | None,
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "split": "official_test",
        "subset": subset,
        "metric": metric,
        "value": value,
        "support": support,
        "target_fpr": target_fpr,
        "threshold": threshold,
    }


def evaluate_test_scores(
    *,
    run_id: str,
    test_frame: pd.DataFrame,
    scores: np.ndarray,
    heldout_class: str | None,
    selections: list[ThresholdSelection],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    scores = np.asarray(scores, dtype=float)
    if len(scores) != len(test_frame):
        raise ValueError("Score count does not match test rows")
    if not np.isfinite(scores).all():
        raise ValueError("Test scores contain NaN or infinity")

    labels = test_frame["label"].to_numpy(dtype=int)
    roles = evaluation_roles(test_frame, heldout_class)
    metrics: list[dict[str, object]] = []
    pr_auc = float(average_precision_score(labels, scores)) if len(np.unique(labels)) == 2 else None
    metrics.append(
        _metric_row(
            run_id=run_id,
            subset="all",
            metric="pr_auc",
            value=pr_auc,
            support=len(labels),
            target_fpr=None,
            threshold=None,
        )
    )

    prediction_frames: list[pd.DataFrame] = []
    for selection in selections:
        predictions = (scores >= selection.threshold).astype(int)
        precision = float(precision_score(labels, predictions, zero_division=0))
        recall = float(recall_score(labels, predictions, zero_division=0))
        f1 = float(f1_score(labels, predictions, zero_division=0))
        for name, value in (("precision", precision), ("recall", recall), ("f1", f1)):
            metrics.append(
                _metric_row(
                    run_id=run_id,
                    subset="all",
                    metric=name,
                    value=value,
                    support=len(labels),
                    target_fpr=selection.target_fpr,
                    threshold=selection.threshold,
                )
            )

        normal_mask = roles == "normal"
        known_mask = roles == "known_attack"
        heldout_mask = roles == "heldout_attack"
        subset_specs = (
            ("normal", "fpr", normal_mask, int(predictions[normal_mask].sum())),
            ("known_attack", "recall", known_mask, int(predictions[known_mask].sum())),
            (
                "heldout_attack",
                "uadr",
                heldout_mask,
                int(predictions[heldout_mask].sum()),
            ),
        )
        for subset, metric, mask, numerator in subset_specs:
            support = int(mask.sum())
            metrics.append(
                _metric_row(
                    run_id=run_id,
                    subset=subset,
                    metric=metric,
                    value=_safe_rate(numerator, support),
                    support=support,
                    target_fpr=selection.target_fpr,
                    threshold=selection.threshold,
                )
            )

        prediction_frames.append(
            pd.DataFrame(
                {
                    "record_id": test_frame["id"].to_numpy(),
                    "run_id": run_id,
                    "split": "official_test",
                    "attack_cat": test_frame["attack_cat"].to_numpy(),
                    "evaluation_role": roles,
                    "y_true": labels,
                    "score": scores,
                    "target_fpr": selection.target_fpr,
                    "threshold": selection.threshold,
                    "y_pred": predictions,
                }
            )
        )
    return pd.DataFrame(metrics), pd.concat(prediction_frames, ignore_index=True)
