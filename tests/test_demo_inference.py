"""Inference input/label isolation and threshold boundary tests."""
import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
from nids_benchmark.demo import predict_frame, load_bundle, compare_csv, model_explanation


class Preprocessor:
    def transform(self, frame):
        if set(frame.columns)!={'x','proto','service','state'}:
            raise AssertionError('Metadata leaked into model')
        return frame[['x']].to_numpy()


class Model:
    def score(self,matrix): return matrix[:,0]


class DemoInferenceTests(unittest.TestCase):
    def setUp(self):
        self.bundle=dict(run_id='CS-RF-S42',features=['x','proto','service','state'],preprocessor=Preprocessor(),fitted_model=Model(),
                         thresholds=[dict(target_fpr=.05,threshold=.5),dict(target_fpr=.01,threshold=.8)])
        self.frame=pd.DataFrame(dict(x=[.5,.7],proto=['tcp','tcp'],service=['-','-'],state=['FIN','FIN'],id=[1,2],label=[0,1],attack_cat=['Normal','DoS']))

    def test_tie_is_attack_and_metadata_never_enters_model(self):
        result=predict_frame(self.bundle,self.frame,.05)
        self.assertEqual([r['outcome'] for r in result['results']],['FP','TP'])

    def test_labels_do_not_change_scores_or_predictions(self):
        one=predict_frame(self.bundle,self.frame,.05)
        two=predict_frame(self.bundle,self.frame.drop(columns=['label','attack_cat','id']),.05)
        self.assertEqual([x['score'] for x in one['results']],[x['score'] for x in two['results']])
        self.assertNotIn('truth',two['results'][0])

    def test_rejects_invalid_numeric_missing_schema_and_unsupported_target(self):
        bad=self.frame.copy(); bad['x']=['invalid','1']
        for frame,target in ((bad,.05),(self.frame.drop(columns='proto'),.05),(self.frame,.5)):
            with self.assertRaises(ValueError): predict_frame(self.bundle,frame,target)

    def test_rejects_infinity_empty_and_excessive_input(self):
        bad=self.frame.copy();bad.loc[0,'x']=np.inf
        for frame in (bad,self.frame.iloc[:0],pd.concat([self.frame]*501)):
            with self.assertRaises(ValueError): predict_frame(self.bundle,frame,.05)

    def test_invalid_bundle_selection_rejected_before_loading(self):
        with self.assertRaises(ValueError): load_bundle('../../data','RF')

    def test_compare_uses_same_records_target_and_does_not_invent_missing_labels(self):
        with patch('nids_benchmark.demo.load_bundle',side_effect=lambda scenario,model:self.bundle) as loader:
            result=compare_csv('CS',.05,self.frame.to_csv(index=False))
        self.assertEqual(loader.call_count,4)
        self.assertEqual([x['model'] for x in result['comparisons']],['RF','XGB','IF','AE'])
        for summary in result['comparisons']:
            self.assertEqual(summary['confusion'],dict(TP=1,FP=1,TN=0,FN=0))
            self.assertEqual(summary['labeled_rows'],2)
            self.assertEqual(summary['rows'],2)
        with patch('nids_benchmark.demo.load_bundle',return_value=self.bundle):
            unlabeled=compare_csv('CS',.01,self.frame.drop(columns='label').to_csv(index=False))
        self.assertTrue(all(x['labeled_rows']==0 and x['normal_predictions']==2 for x in unlabeled['comparisons']))

    def test_score_explanation_distinguishes_if_and_ae(self):
        for model,phrase in [('isolation_forest','decision_function'),('autoencoder','tái tạo')]:
            fitted=Model();fitted.model_id=model
            explanation=model_explanation(dict(fitted_model=fitted))
            self.assertIn(phrase,explanation['description'])
            self.assertEqual(explanation['features'],[])
            self.assertIn('nhân quả',explanation['limitation'])

    def test_feature_importance_groups_one_hot_without_claiming_row_causality(self):
        from types import SimpleNamespace
        encoder=SimpleNamespace(categories_=[['tcp','udp'],['-'],['FIN','INT']])
        pre=SimpleNamespace(transformers_=[('numeric',None,['x']),('categorical',None,['proto','service','state'])],
            named_transformers_={'categorical':SimpleNamespace(named_steps={'onehot':encoder})})
        estimator=SimpleNamespace(feature_importances_=np.array([.1,.2,.3,.1,.2,.1]))
        fitted=SimpleNamespace(model_id='random_forest',estimator=estimator)
        explanation=model_explanation(dict(preprocessor=pre,fitted_model=fitted))
        values={x['feature']:x['importance'] for x in explanation['features']}
        self.assertAlmostEqual(values['proto'],.5)
        self.assertAlmostEqual(values['state'],.3)
        self.assertIn('không phải nguyên nhân',explanation['limitation'])


if __name__=='__main__': unittest.main()
