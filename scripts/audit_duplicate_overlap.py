"""Audit duplicate and cross-split overlap on UNSW-NB15 official splits.

Requires the two official CSVs in data/raw/. Writes a JSON summary so the
report can quote exact figures instead of restating them by hand.

Usage:
    python scripts/audit_duplicate_overlap.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "artifacts" / "data" / "duplicate_overlap_audit.json"

FORBIDDEN = {"id", "label", "attack_cat"}
LOACO_CLASSES = ("Reconnaissance", "DoS", "Exploits")


def load_splits() -> tuple[pd.DataFrame, pd.DataFrame]:
    train_path = RAW / "UNSW_NB15_training-set.csv"
    test_path = RAW / "UNSW_NB15_testing-set.csv"
    missing = [str(p) for p in (train_path, test_path) if not p.exists()]
    if missing:
        raise SystemExit(f"Missing dataset files: {', '.join(missing)}")
    return (
        pd.read_csv(train_path, low_memory=False),
        pd.read_csv(test_path, low_memory=False),
    )


def overlap_by_category(train: pd.DataFrame, test: pd.DataFrame, features: list[str]) -> dict:
    """Count test rows whose feature vector is also present in train, per attack_cat.

    Restricted to the 42 model features and to attacks that are not a LOACO
    held-out class, so the count is the part of the overlap that survives the
    LOACO removal step.
    """
    counts: dict[str, dict[str, int]] = {}
    for category in LOACO_CLASSES:
        # In this scenario the category is removed from development, so only
        # train rows of other categories remain available to match against.
        train_other = train.loc[train["attack_cat"].ne(category), features]
        test_heldout = test.loc[test["attack_cat"].eq(category), features]
        if train_other.empty or test_heldout.empty:
            counts[category] = {"overlap": 0, "test_rows": int(len(test_heldout))}
            continue
        merged = test_heldout.merge(train_other.drop_duplicates(), how="inner", on=features)
        counts[category] = {
            "overlap": int(len(merged)),
            "test_rows": int(len(test_heldout)),
        }
    return counts


def main() -> None:
    print("Loading UNSW-NB15 official splits...")
    train, test = load_splits()
    print(f"  Train: {len(train):,} rows x {train.shape[1]} cols")
    print(f"  Test:  {len(test):,} rows x {test.shape[1]} cols")

    features = [c for c in train.columns if c not in FORBIDDEN]
    without_id = [c for c in train.columns if c != "id"]
    print(f"  Model features (id/label/attack_cat removed): {len(features)}")

    summary = {
        "feature_columns": len(features),
        "duplicate_full_row_including_id": {
            "train": int(train.duplicated().sum()),
            "test": int(test.duplicated().sum()),
        },
        "duplicate_excluding_id_keeping_label": {
            "train": int(train[without_id].duplicated().sum()),
            "test": int(test[without_id].duplicated().sum()),
        },
        "duplicate_feature_only": {
            "train": int(train[features].duplicated().sum()),
            "test": int(test[features].duplicated().sum()),
        },
        "cross_split_overlap_all_categories": {
            "train_features_only": int(len(train[features].drop_duplicates())),
            "overlap_test_rows": int(
                len(test[features].merge(
                    train[features].drop_duplicates(), how="inner", on=features
                ))
            ),
            "test_rows": int(len(test)),
        },
        "loaco_overlap_after_heldout_removal": overlap_by_category(train, test, features),
    }

    print("\n=== Full-row duplicates (id included) ===")
    print(f"  train={summary['duplicate_full_row_including_id']['train']:,}  "
          f"test={summary['duplicate_full_row_including_id']['test']:,}")

    print("\n=== Duplicates with id removed (label + attack_cat kept) ===")
    print(f"  train={summary['duplicate_excluding_id_keeping_label']['train']:,}  "
          f"test={summary['duplicate_excluding_id_keeping_label']['test']:,}")

    print("\n=== Duplicates on the 42 model features only ===")
    print(f"  train={summary['duplicate_feature_only']['train']:,}  "
          f"test={summary['duplicate_feature_only']['test']:,}")

    cross = summary["cross_split_overlap_all_categories"]
    share = cross["overlap_test_rows"] / cross["test_rows"]
    print("\n=== Cross-split overlap (all 42 features, every category) ===")
    print(f"  {cross['overlap_test_rows']:,} / {cross['test_rows']:,} test rows ({share:.1%})")

    print("\n=== Overlap that survives LOACO held-out removal ===")
    print("  (test rows of the held-out class matching a train row of a DIFFERENT class)")
    for category, item in summary["loaco_overlap_after_heldout_removal"].items():
        pct = item["overlap"] / item["test_rows"] if item["test_rows"] else 0.0
        print(f"  {category:16s} {item['overlap']:>6,} / {item['test_rows']:>6,} ({pct:.1%})")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nWrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
