import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.model_selection import train_test_split

from email_preprocessor import load_vectorizer

df = pd.read_csv(
    "data/raw/phishing_email.csv"
)

X_text = df["text_combined"]
y = df["label"]

vectorizer = load_vectorizer(
    "models/email_features.pkl"
)

X = vectorizer.transform(X_text)

_, X_test, _, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = joblib.load(
    "models/email_model.pkl"
)

preds = model.predict(X_test)

print("\nAccuracy:")
print(accuracy_score(y_test, preds))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, preds))

print("\nClassification Report:")
print(classification_report(y_test, preds))