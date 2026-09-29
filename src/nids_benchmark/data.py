"""Dataset loading, splitting, fingerprinting, and audit helpers."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from .contracts import FORBIDDEN_FEATURES, assert_heldout_absent, validate_required_columns


TRAIN_FILENAME = "UNSW_NB15_training-set.csv"
TEST_FILENAME = "UNSW_NB15_testing-set.csv"
CATEGORICAL_COLUMNS = ("proto", "service", "state")


@dataclass(frozen=True)
class DatasetBundle:
    train: pd.DataFrame
    test: pd.DataFrame
    train_path: Path
    test_path: Path


@dataclass(frozen=True)
class DevelopmentSplit:
    train: pd.DataFrame
    validation: pd.DataFrame


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def _normalize_frame(frame: pd.DataFrame) -> pd.DataFrame:
    validate_required_columns(frame.columns)
    normalized = frame.copy()
    normalized["label"] = pd.to_numeric(normalized["label"], errors="raise").astype("int8")
    invalid_labels = sorted(set(normalized["label"].unique()) - {0, 1})
    if invalid_labels:
        raise ValueError(f"Unsupported labels: {invalid_labels}")

    normalized["attack_cat"] = normalized["attack_cat"].fillna("").astype(str).str.strip()
    normal_mask = normalized["label"].eq(0)
    normalized.loc[normal_mask & normalized["attack_cat"].eq(""), "attack_cat"] = "Normal"
    if normalized.loc[~normal_mask, "attack_cat"].eq("").any():
        raise ValueError("Attack rows must have an attack_cat value")

    missing_categoricals = sorted(set(CATEGORICAL_COLUMNS) - set(normalized.columns))
    if missing_categoricals:
        raise ValueError(f"Missing categorical columns: {', '.join(missing_categoricals)}")
    return normalized


def load_official_splits(raw_dir: Path) -> DatasetBundle:
    train_path = raw_dir / TRAIN_FILENAME
    test_path = raw_dir / TEST_FILENAME
    missing = [str(path) for path in (train_path, test_path) if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing dataset files: {', '.join(missing)}")

    train = _normalize_frame(pd.read_csv(train_path, low_memory=False))
    test = _normalize_frame(pd.read_csv(test_path, low_memory=False))
    if list(train.columns) != list(test.columns):
        raise ValueError("Official train and test schemas differ")
    return DatasetBundle(train=train, test=test, train_path=train_path, test_path=test_path)


def feature_names(frame: pd.DataFrame) -> list[str]:
    names = [column for column in frame.columns if column not in FORBIDDEN_FEATURES]
    if not names:
        raise ValueError("No model features remain after removing metadata columns")
    return names


def _stratified_sample(frame: pd.DataFrame, size: int | None, seed: int) -> pd.DataFrame:
    if size is None or size >= len(frame):
        return frame.copy()
    if size < frame["attack_cat"].nunique() * 2:
        raise ValueError("Sample size is too small to preserve attack categories")
    sampled, _ = train_test_split(
        frame,
        train_size=size,
        random_state=seed,
        stratify=frame["attack_cat"],
    )
    return sampled.sort_index().copy()


def make_development_split(
    official_train: pd.DataFrame,
    *,
    heldout_class: str | None,
    seed: int,
    validation_size: float = 0.2,
    max_development_rows: int | None = None,
) -> DevelopmentSplit:
    development = official_train
    if heldout_class:
        heldout_mask = official_train["label"].eq(1) & official_train["attack_cat"].eq(
            heldout_class
        )
        development = official_train.loc[~heldout_mask]
    development = _stratified_sample(development, max_development_rows, seed)

    train, validation = train_test_split(
        development,
        test_size=validation_size,
        random_state=seed,
        stratify=development["attack_cat"],
    )
    if heldout_class:
        assert_heldout_absent(train.to_dict("records"), heldout_class)
        assert_heldout_absent(validation.to_dict("records"), heldout_class)
    return DevelopmentSplit(train=train.copy(), validation=validation.copy())


def sample_official_test(
    official_test: pd.DataFrame, *, size: int | None, seed: int
) -> pd.DataFrame:
    return _stratified_sample(official_test, size, seed)


def _frame_audit(frame: pd.DataFrame) -> dict[str, Any]:
    numeric = frame.select_dtypes(include=[np.number])
    infinite_by_column = {
        column: int(np.isinf(numeric[column].to_numpy(dtype=float)).sum())
        for column in numeric.columns
        if np.isinf(numeric[column].to_numpy(dtype=float)).any()
    }
    return {
        "rows": int(len(frame)),
        "columns": int(frame.shape[1]),
        "duplicate_rows": int(frame.duplicated().sum()),
        "missing_values": int(frame.isna().sum().sum()),
        "infinite_values_by_column": infinite_by_column,
        "label_counts": {
            str(key): int(value) for key, value in frame["label"].value_counts().items()
        },
        "attack_category_counts": {
            str(key): int(value)
            for key, value in frame["attack_cat"].value_counts().items()
        },
        "dtypes": {column: str(dtype) for column, dtype in frame.dtypes.items()},
    }


def build_data_manifest(bundle: DatasetBundle) -> dict[str, Any]:
    return {
        "dataset": "UNSW-NB15",
        "official_source": "https://research.unsw.edu.au/projects/unsw-nb15-dataset",
        "mirror_source": "https://huggingface.co/datasets/Mireu-Lab/UNSW-NB15",
        "files": {
            "train": {
                "filename": bundle.train_path.name,
                "bytes": bundle.train_path.stat().st_size,
                "sha256": sha256_file(bundle.train_path),
                "audit": _frame_audit(bundle.train),
            },
            "test": {
                "filename": bundle.test_path.name,
                "bytes": bundle.test_path.stat().st_size,
                "sha256": sha256_file(bundle.test_path),
                "audit": _frame_audit(bundle.test),
            },
        },
        "forbidden_features": sorted(FORBIDDEN_FEATURES),
        "categorical_features": list(CATEGORICAL_COLUMNS),
    }


def write_manifest(manifest: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
