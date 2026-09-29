# Data Contract - Phase 2 Draft

## Dataset identity

- Dataset: UNSW-NB15.
- Official train split: 175,341 rows and 45 columns.
- Official test split: 82,332 rows and 45 columns.
- Both splits have zero missing values, zero infinite values, and zero exact duplicate rows in the recorded audit.
- Fingerprints, byte sizes, source URLs, label counts, attack-category counts, and dtypes are recorded in `artifacts/data/data_manifest.json`.

## Feature contract

The raw schema contains 45 columns. `id`, `label`, and `attack_cat` are metadata/targets and are forbidden as model features. The model input therefore contains 42 columns. The categorical feature columns are `proto`, `service`, and `state`; remaining model inputs are numeric according to the manifest.

| Field group | Columns | Use |
|---|---|---|
| Identifier | `id` | Metadata only; never a feature |
| Binary target | `label` | Target only; never a feature |
| Attack category | `attack_cat` | Scenario/analysis target; never a feature |
| Categorical features | `proto`, `service`, `state` | Encoded by the fitted preprocessing pipeline |
| Numeric features | Remaining 39 non-forbidden columns | Scaled/processed according to model pipeline |

## Split and leakage rules

1. Preprocessing is fitted only on the permitted development/training partition.
2. Validation is used for model selection and threshold selection.
3. The official test split is used only for final evaluation.
4. Thresholds are selected from Normal validation records at target FPR 1% and 5%.
5. In LOACO scenarios, the held-out attack category is removed before splitting and before fitting preprocessing.

## Acceptance criteria

- No forbidden feature reaches a model matrix.
- Manifest values match the two official CSV files.
- Every run records its scenario, model, seed, threshold target, threshold, metric, and support.
- Any missing or unavailable metric is represented explicitly rather than silently imputed.

## Review state

This is a Phase 2 working draft. It becomes PASS only after Trinh Tram Anh and Hoang Van Vuong Thu review the schema and all three members record their decision in the Gate 2 checklist.
