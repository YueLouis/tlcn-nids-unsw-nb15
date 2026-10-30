import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from analyze_final_diagnostics import grouped_errors


class FinalDiagnosticTests(unittest.TestCase):
    def test_error_rates_keep_role_denominators_separate(self):
        frame=pd.DataFrame(dict(evaluation_role=['normal']*3+['heldout_attack']*2,
            proto=['udp']*5,y_true=[0,0,0,1,1],y_pred=[1,1,0,0,1]))
        rows={r['evaluation_role']:r for r in grouped_errors(frame,'proto')}
        self.assertEqual(sum(r['support'] for r in rows.values()),5)
        normal,held=rows['normal'],rows['heldout_attack']
        self.assertEqual((normal['fp'],normal['tn'],normal['fn'],normal['tp']),(2,1,0,0))
        self.assertAlmostEqual(normal['error_rate'],2/3)
        self.assertEqual((held['fp'],held['tn'],held['fn'],held['tp']),(0,0,1,1))
        self.assertAlmostEqual(held['error_rate'],1/2)


if __name__=='__main__':unittest.main()
