"""End-to-end execution of one closed-set or LOACO experiment."""

from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any

import joblib
import numpy as np
import pandas as pd
import sklearn

from .data import (
    DatasetBundle,
    feature_names,
    load_official_splits,
    make_development_split,
    sample_official_test,
    sha256_file,
)
from .evaluation import evaluate_test_scores, select_threshold
from .models import fit_model
from .preprocessing import build_preprocessor, transform_frame


SCENARIOS: dict[str, tuple[str, str | None]] = {
    "closed_set": ("CS", None),
    "loaco_reconnaissance": ("LR", "Reconnaissance"),
    "loaco_dos": ("LD", "DoS"),
    "loaco_exploits": ("LE", "Exploits"),
}
MODEL_CODES = {
    "random_forest": "RF",
    "xgboost": "XGB",
    "isolation_forest": "IF",
    "autoencoder": "AE",
}


@dataclass(frozen=True)
class RunRequest:
    scenario: str
    model: str
    seed: int
    raw_dir: Path
    output_dir: Path
    validation_size: float = 0.2
    target_fprs: tuple[float, ...] = (0.01, 0.05)
    max_development_rows: int | None = None
    max_test_rows: int | None = None
    save_predictions: bool = True

    @property
    def run_id(self) -> str:
        scenario_code = SCENARIOS[self.scenario][0]
        return f"{scenario_code}-{MODEL_CODES[self.model]}-S{self.seed}"

    @property
    def heldout_class(self) -> str | None:
        return SCENARIOS[self.scenario][1]

    @property
    def smoke(self) -> bool:
        return self.max_development_rows is not None or self.max_test_rows is not None


def _validate_request(request: RunRequest) -> None:
    if request.scenario not in SCENARIOS:
        raise ValueError(f"Unsupported scenario: {request.scenario}")
    if request.model not in MODEL_CODES:
        raise ValueError(f"Unsupported model: {request.model}")
    if not 0 < request.validation_size < 1:
        raise ValueError("validation_size must be between 0 and 1")


def _fingerprint_request(request: RunRequest) -> str:
    payload = {
        "scenario": request.scenario,
        "model": request.model,
        "seed": request.seed,
        "validation_size": request.validation_size,
        "target_fprs": request.target_fprs,
        "max_development_rows": request.max_development_rows,
        "max_test_rows": request.max_test_rows,
    }
    encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _dataset_fingerprint(bundle: DatasetBundle) -> str:
    joined = f"{sha256_file(bundle.train_path)}:{sha256_file(bundle.test_path)}"
    return hashlib.sha256(joined.encode("ascii")).hexdigest()


def _versions() -> dict[str, str]:
    versions = {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "scikit_learn": sklearn.__version__,
        "joblib": joblib.__version__,
    }
    try:
        import xgboost

        versions["xgboost"] = xgboost.__version__
    except ImportError:
        pass
    return versions


def run_experiment(request: RunRequest) -> dict[str, Any]:
    _validate_request(request)
    started_at = datetime.now(timezone.utc)
    started_clock = perf_counter()
    run_dir = request.output_dir / request.run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    bundle = load_official_splits(request.raw_dir)
    split = make_development_split(
        bundle.train,
        heldout_class=request.heldout_class,
        seed=request.seed,
        validation_size=request.validation_size,
        max_development_rows=request.max_development_rows,
    )
    test = sample_official_test(bundle.test, size=request.max_test_rows, seed=request.seed)

    anomaly_model = request.model in {"isolation_forest", "autoencoder"}
    preprocessor_fit_frame = (
        split.train.loc[split.train["label"].eq(0)] if anomaly_model else split.train
    )
    preprocessor, features = build_preprocessor(preprocessor_fit_frame)
    train_matrix = np.asarray(
        preprocessor.fit(preprocessor_fit_frame[features]).transform(split.train[features]),
        dtype=np.float32,
    )
    validation_matrix = transform_frame(preprocessor, split.validation, features)
    test_matrix = transform_frame(preprocessor, test, features)
    labels = split.train["label"].to_numpy(dtype=int)

    fitted = fit_model(
        request.model,
        train_matrix,
        labels,
        seed=request.seed,
        smoke=request.smoke,
    )
    validation_scores = fitted.score(validation_matrix)
    normal_validation_scores = validation_scores[
        split.validation["label"].to_numpy(dtype=int) == 0
    ]
    selections = [
        select_threshold(normal_validation_scores, target_fpr)
        for target_fpr in request.target_fprs
    ]
    test_scores = fitted.score(test_matrix)
    metrics, predictions = evaluate_test_scores(
        run_id=request.run_id,
        test_frame=test,
        scores=test_scores,
        heldout_class=request.heldout_class,
        selections=selections,
    )

    metrics_path = run_dir / "metrics.csv"
    metrics.to_csv(metrics_path, index=False)
    prediction_path = run_dir / "predictions.csv"
    if request.save_predictions:
        predictions.to_csv(prediction_path, index=False)

    model_path = run_dir / "model_bundle.joblib"
    joblib.dump(
        {
            "run_id": request.run_id,
            "model_id": request.model,
            "scenario": request.scenario,
            "heldout_class": request.heldout_class,
            "features": features,
            "preprocessor": preprocessor,
            "fitted_model": fitted,
            "thresholds": [asdict(selection) for selection in selections],
        },
        model_path,
        compress=3,
    )

    completed_at = datetime.now(timezone.utc)
    metadata: dict[str, Any] = {
        "run_id": request.run_id,
        "protocol_version": "1.0-draft",
        "scenario": request.scenario,
        "heldout_class": request.heldout_class,
        "model": request.model,
        "model_family": fitted.family,
        "seed": request.seed,
        "status": "completed_smoke" if request.smoke else "completed",
        "data_fingerprint": _dataset_fingerprint(bundle),
        "config_fingerprint": _fingerprint_request(request),
        "threshold_policy": {
            "source_split": "normal_validation",
            "target_fpr": list(request.target_fprs),
            "score_direction": "higher_means_more_attack_like",
            "selections": [asdict(selection) for selection in selections],
        },
        "row_counts": {
            "development_train": len(split.train),
            "development_validation": len(split.validation),
            "official_test_evaluated": len(test),
            "preprocessor_fit_rows": len(preprocessor_fit_frame),
            "model_fit_rows": int((labels == 0).sum())
            if fitted.family == "anomaly"
            else len(labels),
        },
        "feature_count_after_encoding": int(train_matrix.shape[1]),
        "started_at": started_at.isoformat(),
        "completed_at": completed_at.isoformat(),
        "duration_seconds": round(perf_counter() - started_clock, 3),
        "software_versions": _versions(),
        "artifact_paths": {
            "metrics": str(metrics_path),
            "predictions": str(prediction_path) if request.save_predictions else None,
            "model_bundle": str(model_path),
        },
    }
    (run_dir / "run.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return metadata
