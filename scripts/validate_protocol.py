"""Validate the protocol contract before any dataset or model work starts."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "configs" / "experiment_matrix.yaml"
MATRIX_PATH = ROOT / "docs" / "protocol" / "RUN_MATRIX.csv"

EXPECTED_SCENARIOS = {
    "closed_set": "",
    "loaco_reconnaissance": "Reconnaissance",
    "loaco_dos": "DoS",
    "loaco_exploits": "Exploits",
}
EXPECTED_MODELS = {
    "random_forest": "supervised",
    "xgboost": "supervised",
    "isolation_forest": "anomaly",
    "autoencoder": "anomaly",
}
EXPECTED_SEEDS = [42, 52, 62, 72, 82]


def fail(message: str) -> None:
    raise ValueError(message)


def parse_simple_yaml(path: Path) -> dict:
    """Parse the small, flat contract used by experiment_matrix.yaml."""
    text = path.read_text(encoding="utf-8")
    config: dict = {}

    scalar_patterns = {
        "dataset": r'^dataset:\s*"([^"]+)"',
        "score_direction": r'^score_direction:\s*"([^"]+)"',
    }
    for key, pattern in scalar_patterns.items():
        match = re.search(pattern, text, flags=re.MULTILINE)
        if match:
            config[key] = match.group(1)

    for key, pattern, converter in (
        ("seeds", r"^seeds:\s*\[([^\]]+)\]", int),
        ("threshold_fpr_targets", r"^threshold_fpr_targets:\s*\[([^\]]+)\]", float),
    ):
        match = re.search(pattern, text, flags=re.MULTILINE)
        if match:
            config[key] = [converter(value.strip()) for value in match.group(1).split(",")]

    forbidden = re.search(r'^forbidden_features:\s*\[([^\]]+)\]', text, flags=re.MULTILINE)
    if forbidden:
        config["forbidden_features"] = [
            value.strip().strip('"') for value in forbidden.group(1).split(",")
        ]

    sections: dict[str, list[dict[str, str]]] = {"scenarios": [], "models": []}
    section = None
    item = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.rstrip(":") in sections:
            section = line.rstrip(":")
            item = None
            continue
        if section and line.startswith("- id:"):
            item = {"id": line.split(":", 1)[1].strip().strip('"')}
            sections[section].append(item)
            continue
        if section and item and ":" in line:
            key, value = line.split(":", 1)
            parsed = value.strip().strip('"')
            item[key.strip()] = "" if parsed == "null" else parsed

    config.update(sections)
    return config


def validate_config(config: dict) -> None:
    if config.get("dataset") != "UNSW-NB15":
        fail("Dataset must remain UNSW-NB15")

    scenarios = {item["id"]: item.get("heldout_class") or "" for item in config["scenarios"]}
    if scenarios != EXPECTED_SCENARIOS:
        fail(f"Scenario contract mismatch: {scenarios}")

    models = {item["id"]: item["family"] for item in config["models"]}
    if models != EXPECTED_MODELS:
        fail(f"Model contract mismatch: {models}")

    if config.get("seeds") != EXPECTED_SEEDS:
        fail(f"Seed contract mismatch: {config.get('seeds')}")
    if config.get("threshold_fpr_targets") != [0.01, 0.05]:
        fail("Threshold targets must be 1% and 5% FPR")
    if config.get("score_direction") != "higher_means_more_attack_like":
        fail("All adapters must use the common score direction")
    if set(config.get("forbidden_features", [])) != {"id", "label", "attack_cat"}:
        fail("Forbidden feature contract must contain id, label and attack_cat")


def validate_matrix() -> None:
    with MATRIX_PATH.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))

    if len(rows) != 80:
        fail(f"Expected 80 runs, found {len(rows)}")

    run_ids = [row["run_id"] for row in rows]
    if len(run_ids) != len(set(run_ids)):
        fail("RUN_MATRIX.csv contains duplicate run_id values")

    expected = {
        (scenario, model, seed)
        for scenario in EXPECTED_SCENARIOS
        for model in EXPECTED_MODELS
        for seed in EXPECTED_SEEDS
    }
    actual = {(row["scenario"], row["model"], int(row["seed"])) for row in rows}
    if actual != expected:
        fail("RUN_MATRIX.csv does not match the locked scenario/model/seed product")

    for row in rows:
        expected_heldout = EXPECTED_SCENARIOS[row["scenario"]]
        if row["heldout_class"] != expected_heldout:
            fail(f"Held-out class mismatch for {row['run_id']}")
        if row["model_family"] != EXPECTED_MODELS[row["model"]]:
            fail(f"Model family mismatch for {row['run_id']}")
        if row["status"] != "planned":
            fail(f"Unexpected initial status for {row['run_id']}: {row['status']}")


def validate_required_docs() -> None:
    required = (
        "docs/protocol/GATE_1_CHECKLIST.md",
        "docs/protocol/RESULT_SCHEMA.md",
        "docs/protocol/RQ_TO_EVIDENCE.md",
        "docs/week_01/METRIC_THRESHOLD_SPEC.md",
        "docs/week_01/SYNTHETIC_TESTS.md",
    )
    missing = [path for path in required if not (ROOT / path).exists()]
    if missing:
        fail(f"Missing protocol artifacts: {', '.join(missing)}")


def main() -> int:
    config = parse_simple_yaml(CONFIG_PATH)
    validate_config(config)
    validate_matrix()
    validate_required_docs()
    print("Protocol validation passed: 4 scenarios x 4 models x 5 seeds = 80 unique runs")
    print("Gate 1 remains a human review step; this script does not mark PASS automatically")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, TypeError, ValueError) as exc:
        print(f"Protocol validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
