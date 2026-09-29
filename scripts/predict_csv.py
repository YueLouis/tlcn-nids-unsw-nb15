"""Local prototype: score UNSW-NB15-compatible CSV rows with a saved run."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("predictions_demo.csv"))
    parser.add_argument("--target-fpr", type=float, default=0.05)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bundle = joblib.load(args.bundle)
    frame = pd.read_csv(args.input, low_memory=False)
    missing = sorted(set(bundle["features"]) - set(frame.columns))
    if missing:
        raise ValueError(f"Input is missing features: {', '.join(missing)}")

    matrix = np.asarray(
        bundle["preprocessor"].transform(frame[bundle["features"]]), dtype=np.float32
    )
    scores = bundle["fitted_model"].score(matrix)
    choices = {
        float(item["target_fpr"]): float(item["threshold"])
        for item in bundle["thresholds"]
    }
    if args.target_fpr not in choices:
        raise ValueError(f"Available target FPR values: {sorted(choices)}")
    threshold = choices[args.target_fpr]

    output = pd.DataFrame(
        {
            "record_id": frame["id"] if "id" in frame else np.arange(len(frame)),
            "score": scores,
            "target_fpr": args.target_fpr,
            "threshold": threshold,
            "prediction": np.where(scores >= threshold, "Attack", "Normal"),
        }
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(args.output, index=False)
    print(f"Wrote {len(output)} predictions to {args.output}")


if __name__ == "__main__":
    main()
