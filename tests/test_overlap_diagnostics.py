"""Guard against plausible but invalid post-hoc overlap conclusions."""
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from analyze_overlap_slices import exact_match_mask, model_fit_frame, slice_stats, align_predictions
from test_pr_score_diagnostics import target_copies


class OverlapDiagnosticsTests(unittest.TestCase):
    def test_feature_match_ignores_metadata_and_does_not_multiply_duplicate_keys(self):
        fit = pd.DataFrame(dict(id=[1, 2], label=[1, 1], x=[3., 3.], proto=["tcp", "tcp"]))
        test = pd.DataFrame(dict(id=[7, 8], label=[0, 1], x=[3., 4.], proto=["tcp", "tcp"]))
        self.assertEqual(exact_match_mask(fit, test, ["x", "proto"]).tolist(), [True, False])

    def test_validation_only_key_is_not_in_fit(self):
        fit = pd.DataFrame(dict(x=[1.]))
        validation_and_test = pd.DataFrame(dict(x=[2.]))
        self.assertEqual(exact_match_mask(fit, validation_and_test, ["x"]).tolist(), [False])

    def test_normal_only_fit_differs_from_supervised_match(self):
        train = pd.DataFrame(dict(label=[0, 1], x=[1., 2.]))
        test = pd.DataFrame(dict(x=[2.]))
        self.assertFalse(exact_match_mask(model_fit_frame(train, "IF"), test, ["x"])[0])
        self.assertTrue(exact_match_mask(model_fit_frame(train, "RF"), test, ["x"])[0])

    def test_metadata_key_and_missing_values_rejected(self):
        frame = pd.DataFrame(dict(label=[0], x=[np.nan]))
        for features in (["label"], ["x"]):
            with self.assertRaises(ValueError):
                exact_match_mask(frame, frame, features)

    def test_exact_match_does_not_round_close_scores(self):
        fit = pd.DataFrame(dict(x=[1.]))
        test = pd.DataFrame(dict(x=[np.nextafter(1., 2.)]))
        self.assertFalse(exact_match_mask(fit, test, ["x"])[0])

    def test_absent_denominators_are_missing_instead_of_zero(self):
        frame = target_copies().query("target_fpr == .05 and y_true == 0")
        stats = slice_stats(frame)
        self.assertEqual(stats["normal_support"], 2)
        self.assertTrue(np.isnan(stats["uadr"]))
        self.assertTrue(np.isnan(stats["recall"]))
        self.assertTrue(np.isnan(stats["ap"]))
        empty = slice_stats(frame.iloc[:0])
        self.assertTrue(np.isnan(empty["fpr"]))

    def test_raw_id_and_scenario_role_mismatch_rejected(self):
        frame = target_copies()
        test = pd.DataFrame(dict(id=[1, 2, 3, 4], label=[0, 0, 1, 1], attack_cat=["Normal", "Normal", "DoS", "Exploits"]))
        self.assertEqual(len(align_predictions(frame, test, "LD-RF-S42", "DoS")), 8)
        with self.assertRaisesRegex(ValueError, "roles"):
            align_predictions(frame, test, "LD-RF-S42", "Exploits")
        test.loc[0, "id"] = 99
        with self.assertRaisesRegex(ValueError, "coverage"):
            align_predictions(frame, test, "LD-RF-S42", "DoS")


if __name__ == "__main__":
    unittest.main()
