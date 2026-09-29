"""Verify score direction: higher score = more anomaly-like for all 4 models."""

from __future__ import annotations

import unittest

import numpy as np

from nids_benchmark.models import FittedModel, fit_model


def _make_dataset(seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    """30 Normal + 10 Attack rows, 8 numeric features."""
    rng = np.random.RandomState(seed)
    normal = rng.randn(30, 8) * 0.5 + 0.5  # centered ~0.5
    rng2 = np.random.RandomState(seed + 1)
    attack = rng2.randn(10, 8) * 2.0 + 5.0  # shifted
    X = np.vstack([normal, attack])
    y = np.array([0] * 30 + [1] * 10)
    return X, y


class ScoreDirectionTests(unittest.TestCase):
    def test_rf_score_direction(self) -> None:
        X, y = _make_dataset()
        model = fit_model("random_forest", X, y, seed=42, smoke=True)
        self.assertEqual(model.family, "supervised")
        scores = model.score(X)
        attack_scores = scores[y == 1]
        normal_scores = scores[y == 0]
        self.assertGreater(
            float(attack_scores.mean()), float(normal_scores.mean()),
            "RF attack scores should be higher than normal scores",
        )

    def test_xgb_score_direction(self) -> None:
        X, y = _make_dataset()
        model = fit_model("xgboost", X, y, seed=42, smoke=True)
        self.assertEqual(model.family, "supervised")
        scores = model.score(X)
        attack_scores = scores[y == 1]
        normal_scores = scores[y == 0]
        self.assertGreater(
            float(attack_scores.mean()), float(normal_scores.mean()),
            "XGB attack scores should be higher than normal scores",
        )

    def test_if_higher_score_more_anomaly(self) -> None:
        X, y = _make_dataset()
        model = fit_model("isolation_forest", X, y, seed=42, smoke=True)
        self.assertEqual(model.family, "anomaly")
        scores = model.score(X)
        attack_scores = scores[y == 1]
        normal_scores = scores[y == 0]
        self.assertGreater(
            float(attack_scores.mean()), float(normal_scores.mean()),
            "IF attack scores should be higher than normal scores",
        )

    def test_ae_higher_score_more_anomaly(self) -> None:
        X, y = _make_dataset()
        # Build autoencoder directly with specific architecture
        from sklearn.neural_network import MLPRegressor
        normal_X = X[y == 0]
        ae = MLPRegressor(
            hidden_layer_sizes=(8, 2, 8),
            max_iter=100,
            random_state=42,
        )
        ae.fit(normal_X, normal_X)
        fitted = FittedModel(model_id="autoencoder", family="anomaly", estimator=ae)
        scores = fitted.score(X)
        attack_scores = scores[y == 1]
        normal_scores = scores[y == 0]
        self.assertGreater(
            float(attack_scores.mean()), float(normal_scores.mean()),
            "AE attack scores (MSE) should be higher than normal scores",
        )


if __name__ == "__main__":
    unittest.main()
