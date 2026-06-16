from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

def create_vectorizer():
    return TfidfVectorizer(
        max_features=5000,
        stop_words="english"
    )

def save_vectorizer(vectorizer, path):
    joblib.dump(vectorizer, path)

def load_vectorizer(path):
    return joblib.load(path)