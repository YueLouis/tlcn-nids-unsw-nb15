# Evidence Index - Phase 2 (final technical pass)

This folder records reproducible evidence for the cumulative Phase 2 report.

The checks below describe the snapshot of 26 September 2026. See the
[29 September review and work allocation](../../management/PHAN_CONG_DOT_02_HIEN_TAI_20260929.md)
for the open duplicate/overlap audit, test coverage, and report revisions.
The repository includes the lightweight source evidence; screenshots, model
bundles, record-level predictions, and compiled reports are distributed separately.

## Technical evidence captured

| ID | Evidence | Source of truth | Status |
|---|---|---|---|
| D2.1 | Official train/test audit | `artifacts/data/data_manifest.json` | PASS |
| D2.2 | Run-matrix validation | `docs/protocol/RUN_MATRIX.csv` | PASS; human Gate 1 review pending |
| D2.3 | Unit tests | `tests/` and unittest log | PASS: 9/9 |
| D2.4 | Experiment registry | `results/runs/` | PASS: 80 runs, five seeds, four scenarios, four models |
| D2.5 | Full-run artifact contract | `results/runs/<run-id>/` | PASS: every run has four required artifacts |
| D2.6 | Five-seed aggregate | `docs/reports/DOT_02_METRICS_MEAN_STD.csv` | PASS |
| D2.7 | Final checklist | `docs/evidence/dot_02/FINAL_CHECKLIST.md` | Technical PASS; human Gate review pending |
| D2.8 | Gate 2 checklist | `docs/protocol/GATE_2_CHECKLIST.md` | Technical PASS; three signatures pending |

## Screenshot evidence

- `screenshots/D2_01_Audit_du_lieu_PASS_2026-09-26.png`
- `screenshots/D2_02_Protocol_validation_PASS_2026-09-26.png`
- `screenshots/D2_03_Unit_tests_9_PASS_2026-09-26.png`
- `screenshots/D2_04_Danh_sach_80_run_2026-09-26.png`
- `screenshots/D2_05_Mean_std_5_seed_2026-09-26.png`
- `screenshots/D2_06_PDF_Dot2_15_pages_2026-09-26.png`
- `screenshots/D2_07_Final_check_PASS_2026-09-26.png`

Screenshots are illustrative evidence. Numeric claims must be taken from the source files above, not transcribed from screenshots.

## Important limitations

- The technical matrix is complete: 80 official runs, five seeds, and four artifacts per run.
- Model interpretation remains bounded by the declared protocol and metrics; no zero-day claim is made.
- Gate 1 and Gate 2 still require review and confirmation by all three team members.
