"""Denominators, missing labels and fixture integrity for application replay."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from nids_benchmark.application import summarize,load_case

class ApplicationReplayTests(unittest.TestCase):
    def test_rates_use_only_their_labeled_population(self):
        rows=[dict(outcome='FP'),dict(outcome='TN'),dict(outcome='TP'),dict(outcome='FN'),dict(prediction='Attack')]
        summary=summarize(rows)
        self.assertEqual(summary['labeled_rows'],4)
        self.assertEqual(summary['normal_support'],2)
        self.assertEqual(summary['attack_support'],2)
        self.assertEqual(summary['fpr'],.5)
        self.assertEqual(summary['recall'],.5)

    def test_unlabeled_rows_have_no_accuracy_or_error_rates(self):
        summary=summarize([dict(prediction='Attack',attack_cat='Reconnaissance')],'Reconnaissance')
        self.assertEqual(summary['labeled_rows'],0)
        for key in ['fpr','recall','precision','uadr']:self.assertIsNone(summary[key])
        self.assertEqual(summary['heldout_support'],0)

    def test_heldout_recall_is_not_recall_of_all_attacks(self):
        rows=[dict(truth='Attack',attack_cat='Reconnaissance',prediction='Normal',outcome='FN'),
              dict(truth='Attack',attack_cat='Generic',prediction='Attack',outcome='TP')]
        summary=summarize(rows,'Reconnaissance')
        self.assertEqual(summary['recall'],.5)
        self.assertEqual(summary['uadr'],0)
        self.assertEqual(summary['heldout_support'],1)

    def test_unknown_cases_and_modified_fixtures_are_rejected(self):
        with patch('nids_benchmark.application.catalog',return_value={'cases':[]}):
            with self.assertRaises(ValueError):load_case('../../unexpected')
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'one.csv').write_text('changed',encoding='utf-8')
            row=dict(id='one',filename='one.csv',sha256=hashlib.sha256(b'original').hexdigest())
            with patch('nids_benchmark.application.CASES',root),patch('nids_benchmark.application.catalog',return_value={'cases':[row]}):
                with self.assertRaises(ValueError):load_case('one')

if __name__=='__main__':unittest.main()
