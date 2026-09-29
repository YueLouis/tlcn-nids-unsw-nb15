from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from nids_benchmark.evaluation import evaluate_test_scores, select_threshold


class EvaluationTests(unittest.TestCase):
    def test_threshold_respects_ties_and_fpr_budget(self) -> None:
        selection = select_threshold(np.array([0.1, 0.2, 0.2, 0.9]), 0.25)
        self.assertEqual(selection.threshold, 0.9)
        self.assertEqual(selection.validation_fpr, 0.25)

    def test_heldout_recall_is_reported_separately(self) -> None:
        frame = pd.DataFrame(
            {
                "id": [1, 2, 3, 4],
                "label": [0, 0, 1, 1],
                "attack_cat": ["Normal", "Normal", "DoS", "Exploits"],
            }
        )
        selection = select_threshold(np.array([0.1, 0.2]), 0.5)
        metrics, predictions = evaluate_test_scores(
            run_id="LD-RF-S42",
            test_frame=frame,
            scores=np.array([0.1, 0.2, 0.8, 0.7]),
            heldout_class="DoS",
            selections=[selection],
        )
        uadr = metrics.loc[
            (metrics["subset"] == "heldout_attack") & (metrics["metric"] == "uadr"),
            "value",
        ].iloc[0]
        self.assertEqual(uadr, 1.0)
        self.assertIn("heldout_attack", set(predictions["evaluation_role"]))

    def test_empty_heldout_subset_returns_none(self) -> None:
        frame = pd.DataFrame(
            {
                "id": [1, 2, 3],
                "label": [0, 0, 1],
                "attack_cat": ["Normal", "Normal", "Exploits"],
            }
        )
        selection = select_threshold(np.array([0.1, 0.2]), 0.5)
        metrics, _ = evaluate_test_scores(
            run_id="LD-RF-S42",
            test_frame=frame,
            scores=np.array([0.1, 0.2, 0.8]),
            heldout_class="DoS",
            selections=[selection],
        )
        heldout_row = metrics.loc[
            (metrics["subset"] == "heldout_attack") & (metrics["metric"] == "uadr"),
        ]
        self.assertEqual(len(heldout_row), 1)
        self.assertTrue(pd.isna(heldout_row.iloc[0]["value"]))
        self.assertEqual(heldout_row.iloc[0]["support"], 0)

    def test_support_matches_subset_size(self) -> None:
        frame = pd.DataFrame(
            {
                "id": [1, 2, 3, 4, 5],
                "label": [0, 0, 1, 1, 1],
                "attack_cat": ["Normal", "Normal", "DoS", "DoS", "Exploits"],
            }
        )
        selection = select_threshold(np.array([0.1, 0.2]), 0.5)
        metrics, _ = evaluate_test_scores(
            run_id="LD-RF-S42",
            test_frame=frame,
            scores=np.array([0.1, 0.2, 0.8, 0.7, 0.6]),
            heldout_class="DoS",
            selections=[selection],
        )
        # Normal: 2 rows (label=0)
        normal_fpr = metrics.loc[
            (metrics["subset"] == "normal") & (metrics["metric"] == "fpr"),
        ]
        self.assertEqual(normal_fpr.iloc[0]["support"], 2)
        # Known attack: 1 row (Exploits, label=1)
        known_recall = metrics.loc[
            (metrics["subset"] == "known_attack") & (metrics["metric"] == "recall"),
        ]
        self.assertEqual(known_recall.iloc[0]["support"], 1)
        # Held-out attack: 2 rows (DoS)
        heldout_uadr = metrics.loc[
            (metrics["subset"] == "heldout_attack") & (metrics["metric"] == "uadr"),
        ]
        self.assertEqual(heldout_uadr.iloc[0]["support"], 2)


if __name__ == "__main__":
    unittest.main()
