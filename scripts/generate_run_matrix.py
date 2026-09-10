"""Generate the protocol-locked 80-run experiment matrix."""

from __future__ import annotations

import csv
from itertools import product
from pathlib import Path


SCENARIOS = (
    ("CS", "closed_set", ""),
    ("LR", "loaco_reconnaissance", "Reconnaissance"),
    ("LD", "loaco_dos", "DoS"),
    ("LE", "loaco_exploits", "Exploits"),
)
MODELS = (
    ("RF", "random_forest", "supervised"),
    ("XGB", "xgboost", "supervised"),
    ("IF", "isolation_forest", "anomaly"),
    ("AE", "autoencoder", "anomaly"),
)
SEEDS = (42, 52, 62, 72, 82)


def build_rows() -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for scenario, model, seed in product(SCENARIOS, MODELS, SEEDS):
        scenario_code, scenario_id, heldout_class = scenario
        model_code, model_id, model_family = model
        rows.append(
            {
                "run_id": f"{scenario_code}-{model_code}-S{seed}",
                "scenario": scenario_id,
                "heldout_class": heldout_class,
                "model": model_id,
                "model_family": model_family,
                "seed": seed,
                "status": "planned",
            }
        )
    return rows


def validate(rows: list[dict[str, str | int]]) -> None:
    run_ids = [str(row["run_id"]) for row in rows]
    if len(rows) != 80:
        raise ValueError(f"Expected 80 runs, found {len(rows)}")
    if len(run_ids) != len(set(run_ids)):
        raise ValueError("Run IDs must be unique")


def main() -> None:
    rows = build_rows()
    validate(rows)
    output = Path(__file__).resolve().parents[1] / "docs" / "protocol" / "RUN_MATRIX.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    # Keep the status message ASCII-safe on Windows terminals with legacy code pages.
    print(f"Generated {len(rows)} unique runs at docs/protocol/RUN_MATRIX.csv")


if __name__ == "__main__":
    main()
