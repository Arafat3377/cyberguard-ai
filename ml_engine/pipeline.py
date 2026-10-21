"""Small, reproducible ML demonstration for the academic prototype.
Features: failed_logins, bytes, connections, requests, unusual_hour.
Anomaly detection uses IsolationForest; classification uses RandomForest.
"""
from pathlib import Path
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

BASE = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE / 'ml_models'
FEATURES = ['failed_logins','bytes','connections','requests','unusual_hour']

def train_models(X, y):
    anomaly = IsolationForest(n_estimators=150, contamination=0.15, random_state=42)
    anomaly.fit(X)
    clf = RandomForestClassifier(n_estimators=150, random_state=42, class_weight='balanced')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25, random_state=42, stratify=y)
    clf.fit(X_train, y_train)
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(anomaly, MODEL_DIR/'anomaly_model.joblib')
    joblib.dump(clf, MODEL_DIR/'classifier_model.joblib')
    return classification_report(y_test, clf.predict(X_test), zero_division=0)

def predict(features):
    anomaly = joblib.load(MODEL_DIR/'anomaly_model.joblib')
    clf = joblib.load(MODEL_DIR/'classifier_model.joblib')
    arr = np.array([[features[f] for f in FEATURES]])
    score = float(-anomaly.score_samples(arr)[0])
    is_anomaly = anomaly.predict(arr)[0] == -1
    label = str(clf.predict(arr)[0])
    return {'anomaly': is_anomaly, 'anomaly_score': round(score, 4), 'label': label}
