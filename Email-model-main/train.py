import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

from email_preprocessor import (
    create_vectorizer,
    save_vectorizer
)

print("Loading dataset...")

df = pd.read_csv(
    "data/raw/phishing_email.csv"
)

print("Dataset shape:", df.shape)

X_text = df["text_combined"]
y = df["label"]

print("Creating TF-IDF features...")

vectorizer = create_vectorizer()

X = vectorizer.fit_transform(X_text)

print("Feature matrix:", X.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training XGBoost...")

model = XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    eval_metric="logloss"
)

model.fit(X_train, y_train)

preds = model.predict(X_test)

acc = accuracy_score(y_test, preds)

print(f"Accuracy: {acc:.4f}")

joblib.dump(
    model,
    "models/email_model.pkl"
)

save_vectorizer(
    vectorizer,
    "models/email_features.pkl"
)

print("Saved email_model.pkl")
print("Saved email_features.pkl")