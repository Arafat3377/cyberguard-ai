from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import IsolationForest, RandomForestClassifier
import joblib
from ml_engine.pipeline import FEATURES
BASE=Path(__file__).resolve().parent.parent
csv=BASE/'datasets/security_events.csv'
if not csv.exists():
    raise SystemExit('Run: python datasets/generate_dataset.py')
df=pd.read_csv(csv)
X=df[FEATURES]; y=df['label']
# Scale for stable feature ranges; tree models do not require scaling but this keeps the pipeline reusable.
anomaly=make_pipeline(StandardScaler(), IsolationForest(n_estimators=200,contamination=.15,random_state=42))
clf=make_pipeline(StandardScaler(), RandomForestClassifier(n_estimators=200,random_state=42,class_weight='balanced'))
anomaly.fit(X); clf.fit(X,y)
out=BASE/'ml_models'; out.mkdir(exist_ok=True)
joblib.dump(anomaly,out/'anomaly_model.joblib'); joblib.dump(clf,out/'classifier_model.joblib')
print('Models trained and saved to',out)
