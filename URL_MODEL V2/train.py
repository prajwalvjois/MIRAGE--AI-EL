import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier

from url_feature_extractor import extract_features


print("Loading dataset...")

df = pd.read_csv(
    "Data/raw/PhiUSIIL_Phishing_URL_Dataset.csv"
)

print("Dataset shape:", df.shape)


print("Generating lexical features...")

feature_rows = []

for url in df["URL"]:
    feature_rows.append(
        extract_features(str(url))
    )

X = pd.DataFrame(feature_rows)

y = df["label"]


print("Feature matrix shape:", X.shape)


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print("Training XGBoost...")

model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    random_state=42
)

model.fit(X_train, y_train)


preds = model.predict(X_test)

acc = accuracy_score(y_test, preds)

print(f"Accuracy: {acc:.4f}")


joblib.dump(
    model,
    "models/url_model.pkl"
)

joblib.dump(
    X.columns.tolist(),
    "models/url_features.pkl"
)

print("Saved url_model.pkl")
print("Saved url_features.pkl")