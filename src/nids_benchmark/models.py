"""Common adapters for the four benchmark models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.neural_network import MLPRegressor


SUPPORTED_MODELS = frozenset(
    {"random_forest", "xgboost", "isolation_forest", "autoencoder"}
)


@dataclass
class FittedModel:
    model_id: str
    family: str
    estimator: Any

    def score(self, matrix: np.ndarray) -> np.ndarray:
        if self.model_id in {"random_forest", "xgboost"}:
            return np.asarray(self.estimator.predict_proba(matrix)[:, 1], dtype=float)
        if self.model_id == "isolation_forest":
            return -np.asarray(self.estimator.decision_function(matrix), dtype=float)
        if self.model_id == "autoencoder":
            reconstructed = np.asarray(self.estimator.predict(matrix), dtype=np.float32)
            return np.mean(np.square(matrix - reconstructed), axis=1, dtype=np.float64)
        raise ValueError(f"Unsupported model: {self.model_id}")


def _build_estimator(model_id: str, seed: int, smoke: bool) -> Any:
    if model_id == "random_forest":
        return RandomForestClassifier(
            n_estimators=80 if smoke else 300,
            min_samples_leaf=2,
            class_weight="balanced_subsample",
            random_state=seed,
            n_jobs=-1,
        )
    if model_id == "xgboost":
        from xgboost import XGBClassifier

        return XGBClassifier(
            n_estimators=100 if smoke else 350,
            max_depth=6,
            learning_rate=0.08,
            subsample=0.85,
            colsample_bytree=0.85,
            eval_metric="logloss",
            tree_method="hist",
            random_state=seed,
            n_jobs=-1,
        )
    if model_id == "isolation_forest":
        return IsolationForest(
            n_estimators=100 if smoke else 300,
            max_samples="auto",
            contamination="auto",
            random_state=seed,
            n_jobs=-1,
        )
    if model_id == "autoencoder":
        return MLPRegressor(
            hidden_layer_sizes=(64, 16, 64),
            activation="relu",
            solver="adam",
            batch_size=256,
            learning_rate_init=0.001,
            max_iter=20 if smoke else 80,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=6,
            random_state=seed,
        )
    raise ValueError(f"Unsupported model: {model_id}")


def fit_model(
    model_id: str,
    matrix: np.ndarray,
    labels: np.ndarray,
    *,
    seed: int,
    smoke: bool,
) -> FittedModel:
    if model_id not in SUPPORTED_MODELS:
        raise ValueError(f"Unsupported model: {model_id}")
    estimator = _build_estimator(model_id, seed, smoke)
    if model_id in {"isolation_forest", "autoencoder"}:
        normal_matrix = matrix[labels == 0]
        if len(normal_matrix) == 0:
            raise ValueError("Anomaly models require Normal training rows")
        if model_id == "autoencoder":
            estimator.fit(normal_matrix, normal_matrix)
        else:
            estimator.fit(normal_matrix)
        return FittedModel(model_id=model_id, family="anomaly", estimator=estimator)

    estimator.fit(matrix, labels)
    return FittedModel(model_id=model_id, family="supervised", estimator=estimator)
