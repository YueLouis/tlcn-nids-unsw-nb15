"""Regression cases where a plausible diagnostic could silently mislead."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import auc, average_precision_score, precision_recall_curve


spec = importlib.util.spec_from_file_location("pr_scores", Path(__file__).resolve().parents[1] / "scripts/analyze_pr_scores.py")
diagnostics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagnostics)


def target_copies() -> pd.DataFrame:
    parts = []
    for target, threshold in ((0.01, 0.8), (0.05, 0.5)):
        parts.append(pd.DataFrame(dict(record_id=[1, 2, 3, 4], run_id=["LD-RF-S42"] * 4,
            split=["official_test"] * 4, attack_cat=["Normal", "Normal", "DoS", "Exploits"],
            evaluation_role=["normal", "normal", "heldout_attack", "known_attack"],
            y_true=[0, 0, 1, 1], score=[0.2, 0.5, 0.5, 0.9],
            target_fpr=target, threshold=threshold,
            y_pred=(np.array([0.2, 0.5, 0.5, 0.9]) >= threshold).astype(int))))
    return pd.concat(parts, ignore_index=True)


def saved_fixture():
    rows = [("all", "pr_auc", 5 / 6, 4, np.nan, np.nan)]
    for target, threshold, values in ((0.01, 0.8, [1, 0.5, 2 / 3, 0, 1, 0]),
                                       (0.05, 0.5, [2 / 3, 1, 0.8, 0.5, 1, 1])):
        for (subset, metric, support), value in zip(
            [("all", "precision", 4), ("all", "recall", 4), ("all", "f1", 4),
             ("normal", "fpr", 2), ("known_attack", "recall", 1), ("heldout_attack", "uadr", 1)], values):
            rows.append((subset, metric, value, support, target, threshold))
    saved = pd.DataFrame(rows, columns=["subset", "metric", "value", "support", "target_fpr", "threshold"])
    meta = {"threshold_policy": {"selections": [dict(target_fpr=0.01, threshold=0.8),
                                                   dict(target_fpr=0.05, threshold=0.5)]}}
    return meta, saved


class PRScoreDiagnosticTests(unittest.TestCase):
    def test_duplicate_target_does_not_double_support_and_equality_is_attack(self):
        part = diagnostics.unique_scores(target_copies())
        self.assertEqual(len(part), 4)
        data = target_copies().query("target_fpr == 0.05")
        self.assertEqual(data.y_pred.tolist(), [0, 1, 1, 1])
        self.assertEqual(diagnostics.confusion(data.y_true.to_numpy(), data.y_pred.to_numpy())["fpr"], 0.5)

    def test_rejects_different_score_between_target_copies(self):
        frame = target_copies()
        frame.loc[4, "score"] = 0.3
        with self.assertRaisesRegex(ValueError, "copies disagree"):
            diagnostics.unique_scores(frame)

    def test_rejects_duplicate_record_in_one_target(self):
        frame = target_copies()
        frame.loc[1, "record_id"] = 1
        with self.assertRaisesRegex(ValueError, "Duplicate record"):
            diagnostics.unique_scores(frame)

    def test_rejects_strict_threshold_comparison_at_a_tie(self):
        frame = target_copies()
        frame.loc[5, "y_pred"] = 0
        with self.assertRaisesRegex(ValueError, "score >= threshold"):
            diagnostics.unique_scores(frame)

    def test_heldout_scope_excludes_known_attacks_and_changes_prevalence(self):
        scopes = diagnostics.scope_frames(diagnostics.unique_scores(target_copies()))
        self.assertEqual(len(scopes["all"]), 4)
        self.assertEqual(scopes["normal_vs_heldout"].record_id.tolist(), [1, 2, 3])
        self.assertAlmostEqual(scopes["normal_vs_heldout"].y_true.mean(), 1 / 3)

    def test_average_precision_is_not_trapezoidal_area(self):
        labels, scores = np.array([0, 1, 1]), np.array([0.9, 0.8, 0.7])
        precision, recall, _ = precision_recall_curve(labels, scores)
        self.assertAlmostEqual(average_precision_score(labels, scores), 7 / 12)
        self.assertNotAlmostEqual(average_precision_score(labels, scores), auc(recall, precision))

    def test_saved_metrics_count_ap_support_once_and_check_both_thresholds(self):
        meta, saved = saved_fixture()
        points, checks = diagnostics.verify_saved_metrics(meta, target_copies(), saved, 5 / 6)
        self.assertEqual(checks, 13)
        self.assertEqual([point["uadr"] for point in points], [0, 1])

    def test_rejects_saved_metric_with_doubled_ap_support(self):
        meta, saved = saved_fixture()
        saved.loc[0, "support"] = 8
        with self.assertRaisesRegex(ValueError, "Saved metric mismatch"):
            diagnostics.verify_saved_metrics(meta, target_copies(), saved, 5 / 6)

    def test_rejects_value_from_a_different_threshold(self):
        meta, saved = saved_fixture()
        saved.loc[1, "threshold"] = 0.5
        with self.assertRaisesRegex(ValueError, "threshold mismatch"):
            diagnostics.verify_saved_metrics(meta, target_copies(), saved, 5 / 6)


if __name__ == "__main__":
    unittest.main()
