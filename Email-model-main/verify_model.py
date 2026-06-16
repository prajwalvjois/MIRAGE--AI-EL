import joblib

model = joblib.load(
    "models/email_model.pkl"
)

vectorizer = joblib.load(
    "models/email_features.pkl"
)

print(type(model))
print(type(vectorizer))