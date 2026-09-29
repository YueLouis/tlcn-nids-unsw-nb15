"""Run one protocol-aligned NIDS experiment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from nids_benchmark.models import SUPPORTED_MODELS
from nids_benchmark.runner import SCENARIOS, RunRequest, run_experiment


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), required=True)
    parser.add_argument("--model", choices=sorted(SUPPORTED_MODELS), required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-dir", type=Path, default=Path("results/runs"))
    parser.add_argument("--validation-size", type=float, default=0.2)
    parser.add_argument("--max-development-rows", type=int)
    parser.add_argument("--max-test-rows", type=int)
    parser.add_argument("--no-save-predictions", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    request = RunRequest(
        scenario=args.scenario,
        model=args.model,
        seed=args.seed,
        raw_dir=args.raw_dir,
        output_dir=args.output_dir,
        validation_size=args.validation_size,
        max_development_rows=args.max_development_rows,
        max_test_rows=args.max_test_rows,
        save_predictions=not args.no_save_predictions,
    )
    metadata = run_experiment(request)
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
