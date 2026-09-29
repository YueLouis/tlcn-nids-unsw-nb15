"""Leakage-safe preprocessing for the official UNSW-NB15 split."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .contracts import validate_feature_columns
from .data import CATEGORICAL_COLUMNS, feature_names


def build_preprocessor(frame: pd.DataFrame) -> tuple[ColumnTransformer, list[str]]:
    features = feature_names(frame)
    validate_feature_columns(features)
    categorical = [column for column in CATEGORICAL_COLUMNS if column in features]
    numeric = [column for column in features if column not in categorical]

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                    dtype=np.float32,
                ),
            ),
        ]
    )
    transformer = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric),
            ("categorical", categorical_pipeline, categorical),
        ],
        verbose_feature_names_out=False,
    )
    return transformer, features


def transform_frame(
    preprocessor: ColumnTransformer, frame: pd.DataFrame, features: list[str]
) -> np.ndarray:
    transformed = preprocessor.transform(frame[features])
    array = np.asarray(transformed, dtype=np.float32)
    if not np.isfinite(array).all():
        raise ValueError("Preprocessed feature matrix contains NaN or infinity")
    return array
