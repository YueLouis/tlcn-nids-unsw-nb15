from __future__ import annotations

import unittest

import pandas as pd

from nids_benchmark.data import make_development_split


class DataPipelineTests(unittest.TestCase):
    def test_heldout_is_removed_before_split(self) -> None:
        rows = []
        for index in range(20):
            rows.append(
                {
                    "id": index,
                    "label": 0,
                    "attack_cat": "Normal",
                    "proto": "tcp",
                    "service": "-",
                    "state": "FIN",
                    "dur": float(index),
                }
            )
        for index in range(20, 40):
            rows.append(
                {
                    "id": index,
                    "label": 1,
                    "attack_cat": "DoS" if index < 30 else "Exploits",
                    "proto": "udp",
                    "service": "dns",
                    "state": "INT",
                    "dur": float(index),
                }
            )
        split = make_development_split(
            pd.DataFrame(rows), heldout_class="DoS", seed=42, validation_size=0.25
        )
        self.assertNotIn("DoS", set(split.train["attack_cat"]))
        self.assertNotIn("DoS", set(split.validation["attack_cat"]))


if __name__ == "__main__":
    unittest.main()
