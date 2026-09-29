from __future__ import annotations

import unittest

from nids_benchmark.contracts import (
    ContractError,
    assert_heldout_absent,
    binary_label,
    development_rows,
    evaluation_role,
    feature_columns,
    validate_feature_columns,
)


ROWS = [
    {"id": 1, "label": 0, "attack_cat": "Normal", "proto": "tcp"},
    {"id": 2, "label": 1, "attack_cat": "DoS", "proto": "tcp"},
    {"id": 3, "label": 1, "attack_cat": "Reconnaissance", "proto": "udp"},
]


class ContractTests(unittest.TestCase):
    def test_feature_columns_remove_metadata(self) -> None:
        self.assertEqual(feature_columns(["id", "label", "attack_cat", "proto"]), ["proto"])

    def test_forbidden_feature_is_rejected(self) -> None:
        with self.assertRaises(ContractError):
            validate_feature_columns(["proto", "label"])

    def test_binary_label_normalization(self) -> None:
        self.assertEqual(binary_label("Normal"), 0)
        self.assertEqual(binary_label("Attack"), 1)
        with self.assertRaises(ContractError):
            binary_label("unknown")

    def test_loaco_removes_heldout_before_development(self) -> None:
        development = development_rows(ROWS, heldout_class="Reconnaissance")
        self.assertEqual([row["id"] for row in development], [1, 2])
        assert_heldout_absent(development, "Reconnaissance")

    def test_loaco_validator_catches_leakage(self) -> None:
        with self.assertRaises(ContractError):
            assert_heldout_absent(ROWS, "Reconnaissance")

    def test_evaluation_roles(self) -> None:
        self.assertEqual(evaluation_role(ROWS[0], "Reconnaissance"), "normal")
        self.assertEqual(evaluation_role(ROWS[1], "Reconnaissance"), "known_attack")
        self.assertEqual(evaluation_role(ROWS[2], "Reconnaissance"), "heldout_attack")


if __name__ == "__main__":
    unittest.main()
