import joblib

features = joblib.load(
    "models/url_features.pkl"
)

print(features)