import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

from sklearn.model_selection import train_test_split

from url_feature_extractor import extract_features


df = pd.read_csv(
    "Data/raw/PhiUSIIL_Phishing_URL_Dataset.csv"
)

feature_rows = []

for url in df["URL"]:
    feature_rows.append(
        extract_features(str(url))
    )

X = pd.DataFrame(feature_rows)

y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = joblib.load(
    "models/url_model.pkl"
)

preds = model.predict(X_test)

print("\nAccuracy:")
print(accuracy_score(y_test, preds))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, preds))

print("\nClassification Report:")
print(classification_report(y_test, preds))