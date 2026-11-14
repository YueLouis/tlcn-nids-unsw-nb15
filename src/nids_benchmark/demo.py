"""Validated local inference using an allowlisted frozen seed-42 bundle."""
from functools import lru_cache
from io import StringIO
from pathlib import Path
import csv
import re

import joblib
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
SCENARIOS=('CS','LR','LD','LE')
MODELS=('RF','XGB','IF','AE')
DECIMAL_NUMBER=re.compile(r'^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$', re.ASCII)


def read_demo_csv(text: str) -> pd.DataFrame:
    """Read strict CSV without silently renaming duplicate columns or inferring labels."""
    if not isinstance(text, str):
        raise ValueError('Nội dung CSV phải là văn bản.')
    text=text.removeprefix('\ufeff')
    # csv.reader(strict=True) still accepts a quote in the middle of an unquoted field.
    quoted=False
    closed_quote=False
    field_start=True
    index=0
    while index < len(text):
        character=text[index]
        if closed_quote and character not in ',\r\n':
            raise ValueError('CSV có ký tự sau dấu nháy đóng.')
        if character == '"':
            if quoted and index+1 < len(text) and text[index+1] == '"':
                index+=1
            elif quoted:
                quoted=False
                closed_quote=True
            elif field_start:
                quoted=True
                field_start=False
            else:
                raise ValueError('Dấu nháy CSV không hợp lệ.')
        elif not quoted and character in ',\r\n':
            field_start=True
            closed_quote=False
        else:
            field_start=False
        index+=1
    if quoted:
        raise ValueError('CSV có dấu nháy chưa đóng.')
    try:
        rows=[row for row in csv.reader(StringIO(text, newline=''), strict=True)
              if any(cell != '' for cell in row)]
    except csv.Error as exc:
        raise ValueError('Không đọc được CSV: dấu nháy không hợp lệ.') from exc
    if not rows:
        raise ValueError('CSV trống hoặc thiếu tên cột.')
    header=rows[0]
    if any(not key.strip() for key in header) or len(set(header)) != len(header):
        raise ValueError('CSV thiếu hoặc trùng tên cột.')
    if not 1 <= len(rows)-1 <= 1000:
        raise ValueError('Chọn từ 1 đến 1.000 dòng CSV mỗi lượt.')
    for number, row in enumerate(rows[1:], 2):
        if len(row) != len(header):
            raise ValueError(f'CSV sai số cột ở dòng {number}.')
    return pd.DataFrame(rows[1:], columns=header)


def model_explanation(bundle: dict) -> dict:
    """Describe the stored model, without claiming a causal row explanation."""
    fitted=bundle['fitted_model']
    model_id=getattr(fitted,'model_id','')
    if model_id in ('random_forest','xgboost'):
        pre=bundle['preprocessor']
        estimator=fitted.estimator
        importance=np.asarray(estimator.feature_importances_,dtype=float)
        numeric=list(pre.transformers_[0][2])
        categorical=list(pre.transformers_[1][2])
        encoder=pre.named_transformers_['categorical'].named_steps['onehot']
        names=numeric+[col for col,values in zip(categorical,encoder.categories_) for _ in values]
        if len(names)!=len(importance) or not np.isfinite(importance).all() or (importance<0).any():
            raise ValueError('Feature importance không khớp schema trong bundle.')
        grouped=pd.Series(importance,index=names).groupby(level=0).sum().sort_values(ascending=False)
        return dict(method='RF impurity' if model_id=='random_forest' else 'XGB gain',
            description='Feature có trọng số cao trong mô hình đã học; gộp one-hot về feature gốc.',
            limitation='Importance toàn mô hình, không phải nguyên nhân dự đoán của từng dòng. Không so trực tiếp trọng số RF với XGB.',
            features=[dict(feature=str(name),importance=float(value)) for name,value in grouped.head(5).items()])
    if model_id=='isolation_forest':
        description='Score = âm decision_function của Isolation Forest. Điểm cao hơn là bất thường hơn so với Normal đã học.'
    elif model_id=='autoencoder':
        description='Score = lỗi tái tạo bình phương trung bình của Autoencoder trên feature đã biến đổi. Lỗi cao hơn là bất thường hơn.'
    else:
        description='Score cao hơn là giống Attack/anomaly hơn; score ≥ ngưỡng thì báo Attack.'
    return dict(method='Cách đọc score',description=description,
        limitation='Thông tin cách tính score, chưa giải thích nhân quả từng dòng; score khác thang giữa các model.',features=[])


@lru_cache(maxsize=16)
def load_bundle(scenario: str, model: str):
    if scenario not in SCENARIOS or model not in MODELS:
        raise ValueError('Chọn kịch bản và mô hình trong danh sách.')
    return joblib.load(ROOT/'results/runs'/f'{scenario}-{model}-S42'/'model_bundle.joblib')


def predict_frame(bundle: dict, frame: pd.DataFrame, target: float) -> dict:
    if len(frame)<1 or len(frame)>1000:
        raise ValueError('Chọn từ 1 đến 1.000 dòng CSV mỗi lượt.')
    missing=sorted(set(bundle['features'])-set(frame.columns))
    if missing:
        raise ValueError('CSV thiếu cột: '+', '.join(missing))
    features=frame[bundle['features']].copy()
    numeric=[c for c in bundle['features'] if c not in ('proto','service','state')]
    if any(not DECIMAL_NUMBER.fullmatch(str(value).strip())
           for value in features[numeric].to_numpy().flat):
        raise ValueError('Cột số có ô trống hoặc dữ liệu không hợp lệ.')
    try:
        features[numeric]=features[numeric].apply(pd.to_numeric,errors='raise')
    except (TypeError,ValueError) as exc:
        raise ValueError('Cột số có dữ liệu không đọc được.') from exc
    if not np.isfinite(features[numeric].to_numpy(dtype=float)).all():
        raise ValueError('Cột số có ô trống, NaN hoặc vô cực.')
    if features[['proto','service','state']].isna().any().any() or any(
        not str(value).strip() for value in features[['proto','service','state']].to_numpy().flat
    ):
        raise ValueError('Cột proto/service/state có ô trống.')
    choices={float(x['target_fpr']):float(x['threshold']) for x in bundle['thresholds']}
    if target not in choices: raise ValueError('Chỉ hỗ trợ target validation 1% hoặc 5%.')
    matrix=np.asarray(bundle['preprocessor'].transform(features),dtype=np.float32)
    if not np.isfinite(matrix).all(): raise ValueError('Dữ liệu sau biến đổi có NaN hoặc vô cực.')
    scores=bundle['fitted_model'].score(matrix)
    threshold=choices[target]
    if not np.isfinite(scores).all(): raise ValueError('Mô hình trả về điểm không hữu hạn.')
    predicted=(scores>=threshold).astype(int)
    results=[]
    for i,(_,row) in enumerate(frame.iterrows()):
        result=dict(record_id=str(row['id']) if 'id' in frame else str(i+1),score=float(scores[i]),
                    threshold=threshold,prediction='Attack' if predicted[i] else 'Normal')
        raw_label=str(row.get('label','')).strip()
        if DECIMAL_NUMBER.fullmatch(raw_label) and float(raw_label) in (0.,1.):
            label=int(float(raw_label)); result['truth']='Attack' if label else 'Normal'
            result['outcome']=('TP' if predicted[i] else 'FN') if label else ('FP' if predicted[i] else 'TN')
        if 'attack_cat' in frame and pd.notna(row['attack_cat']): result['attack_cat']=str(row['attack_cat'])
        results.append(result)
    confusion={name:sum(row.get('outcome')==name for row in results) for name in ('TP','FP','TN','FN')}
    return dict(run_id=bundle['run_id'],seed=42,target_fpr=target,threshold=threshold,
        rows=len(frame),attack_predictions=int(predicted.sum()),normal_predictions=int((predicted==0).sum()),
        labeled_rows=sum(confusion.values()),confusion=confusion,explanation=model_explanation(bundle),
        note='Ngưỡng lấy từ Normal validation; kết quả minh họa CSV UNSW-NB15, chưa phải cảm biến mạng trực tiếp.',results=results)


def predict_csv(scenario: str, model: str, target: float, text: str) -> dict:
    frame=read_demo_csv(text)
    return predict_frame(load_bundle(scenario,model),frame,target)


def compare_csv(scenario: str, target: float, text: str) -> dict:
    """Evaluate all four frozen bundles on the same input and threshold policy."""
    frame=read_demo_csv(text)
    comparisons=[]
    for model in MODELS:
        result=predict_frame(load_bundle(scenario,model),frame,target)
        result.pop('results')
        result['model']=model
        comparisons.append(result)
    return dict(scenario=scenario,seed=42,target_fpr=target,rows=len(frame),comparisons=comparisons,
        note='Cùng CSV và target validation; các model có ngưỡng/score khác nhau. FP/FN chỉ tính dòng có nhãn hợp lệ. Mẫu minh họa không thay kết quả toàn test.')
