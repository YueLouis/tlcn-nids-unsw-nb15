"""Small, dependency-free helpers for the dataset and evaluation contract."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any


FORBIDDEN_FEATURES = frozenset({"id", "label", "attack_cat"})
REQUIRED_COLUMNS = frozenset({"id", "label", "attack_cat"})


class ContractError(ValueError):
    """Raised when an input violates a locked protocol rule."""


def validate_required_columns(columns: Iterable[str]) -> None:
    """Require the metadata columns needed to build targets and audit data."""
    available = set(columns)
    missing = sorted(REQUIRED_COLUMNS - available)
    if missing:
        raise ContractError(f"Missing required columns: {', '.join(missing)}")


def feature_columns(columns: Sequence[str]) -> list[str]:
    """Return model features while keeping labels and record IDs out."""
    validate_required_columns(columns)
    features = [column for column in columns if column not in FORBIDDEN_FEATURES]
    if not features:
        raise ContractError("No feature columns remain after removing forbidden columns")
    return features


def validate_feature_columns(columns: Iterable[str]) -> None:
    """Reject a feature list that contains protocol-forbidden metadata."""
    forbidden = sorted(set(columns) & FORBIDDEN_FEATURES)
    if forbidden:
        raise ContractError(f"Forbidden feature columns: {', '.join(forbidden)}")


def binary_label(value: Any) -> int:
    """Normalize the official binary label to 0 (Normal) or 1 (Attack)."""
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)) and value in (0, 1):
        return int(value)
    normalized = str(value).strip().lower()
    if normalized in {"0", "normal", "benign"}:
        return 0
    if normalized in {"1", "attack", "anomaly", "abnormal"}:
        return 1
    raise ContractError(f"Unsupported binary label: {value!r}")


def evaluation_role(row: Mapping[str, Any], heldout_class: str | None = None) -> str:
    """Assign the protocol role used by metrics for one record."""
    if binary_label(row["label"]) == 0:
        return "normal"
    if heldout_class and str(row["attack_cat"]).strip() == heldout_class:
        return "heldout_attack"
    return "known_attack"


def development_rows(
    rows: Iterable[Mapping[str, Any]], heldout_class: str | None = None
) -> list[Mapping[str, Any]]:
    """Remove a held-out attack class before any split or fitting step."""
    if not heldout_class:
        return list(rows)
    return [
        row
        for row in rows
        if not (
            binary_label(row["label"]) == 1
            and str(row["attack_cat"]).strip() == heldout_class
        )
    ]


def assert_heldout_absent(rows: Iterable[Mapping[str, Any]], heldout_class: str) -> None:
    """Fail fast if an LOACO development set still contains the held-out class."""
    leaked = sum(
        1
        for row in rows
        if binary_label(row["label"]) == 1
        and str(row["attack_cat"]).strip() == heldout_class
    )
    if leaked:
        raise ContractError(
            f"Held-out class {heldout_class!r} appears in development data: {leaked} rows"
        )
