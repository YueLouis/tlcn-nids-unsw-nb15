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


if __name__ == "__main__":
    unittest.main()
