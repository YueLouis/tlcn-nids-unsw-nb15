"""Prove that the preprocessor does not leak validation/test into training statistics."""

from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from nids_benchmark.preprocessing import build_preprocessor


def _make_synthetic_frame(
    n_train: int = 15,
    n_val: int = 5,
    *,
    attack_cat: str = "Normal",
    label: int = 0,
    val_outlier: float | None = None,
    service: str = "-",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build a synthetic frame with 'dur' column and categorical columns."""
    cols = {
        "id": [],
        "label": [],
        "attack_cat": [],
        "proto": [],
        "service": [],
        "state": [],
        "dur": [],
    }
    rows = n_train + n_val
    for i in range(rows):
        cols["id"].append(i)
        cols["label"].append(label)
        cols["attack_cat"].append(attack_cat)
        cols["proto"].append("tcp")
        cols["service"].append(service)
        cols["state"].append("FIN")
        # Training rows: uniform in [0, 1]; validation rows get outlier
        if i < n_train:
            cols["dur"].append(float(i) / max(n_train - 1, 1))
        else:
            cols["dur"].append(999.0 if val_outlier is None else val_outlier)
    frame = pd.DataFrame(cols)
    return frame.iloc[:n_train], frame.iloc[n_train:]


class PreprocessorLeakageTests(unittest.TestCase):
    def test_preprocessor_fit_does_not_see_validation_data(self) -> None:
        train, val = _make_synthetic_frame(n_train=15, n_val=5)
        transformer, features = build_preprocessor(train)
        transformer.fit(train[features])

        # Check that StandardScaler statistics reflect only training data
        scaler = transformer.named_transformers_["numeric"].named_steps["scaler"]
        # The 'dur' column is index 0 in numeric features
        dur_mean = scaler.mean_[0]
        # Training dur values are in [0, 1], so mean should be close to 0.5
        self.assertAlmostEqual(dur_mean, 0.5, delta=0.15,
                               msg=f"mean {dur_mean:.4f} pulled toward validation outlier 999")
        # Validation outlier (999) must not pull the mean
        self.assertLess(dur_mean, 1.0,
                        msg="StandardScaler mean leaked validation outlier 999")

        # Transform should succeed for both splits
        train_t = transformer.transform(train[features])
        val_t = transformer.transform(val[features])
        self.assertEqual(train_t.shape[0], len(train))
        self.assertEqual(val_t.shape[0], len(val))

    def test_anomaly_preprocessor_fit_normal_only(self) -> None:
        """Fit on Normal-only; verify OneHot categories don't include attack-only."""
        # Build Normal-only frame (label=0)
        normal_rows = []
        for i in range(15):
            normal_rows.append({
                "id": i, "label": 0, "attack_cat": "Normal",
                "proto": "tcp", "service": "-", "state": "FIN", "dur": float(i) * 0.1,
            })
        normal_frame = pd.DataFrame(normal_rows)

        # Build mixed frame with an attack-only service category
        mixed_rows = list(normal_rows)
        for i in range(15, 25):
            mixed_rows.append({
                "id": i, "label": 1, "attack_cat": "DoS",
                "proto": "tcp", "service": "http", "state": "INT", "dur": float(i) * 0.1,
            })
        mixed_frame = pd.DataFrame(mixed_rows)

        # Fit on normal-only
        transformer_normal, features = build_preprocessor(normal_frame)
        transformer_normal.fit(normal_frame[features])

        # Fit on mixed
        transformer_mixed, features2 = build_preprocessor(mixed_frame)
        transformer_mixed.fit(mixed_frame[features])

        # Both should succeed
        self.assertIsNotNone(transformer_normal)
        self.assertIsNotNone(transformer_mixed)

        # Check OneHotEncoder categories from normal-only fit
        # transformers_ is list of (name, transformer, columns)
        cat_transformer_normal = transformer_normal.transformers_[1][1]
        onehot_categories = cat_transformer_normal.named_steps["onehot"].categories_
        # 'http' service should NOT appear in normal-only categories
        service_categories = onehot_categories[1]  # service is index 1 (proto, service, state)
        self.assertNotIn("http", service_categories,
                         msg="OneHot categories leaked attack-only category from non-training data")


if __name__ == "__main__":
    unittest.main()
