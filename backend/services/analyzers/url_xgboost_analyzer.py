import os
import joblib
import scipy.sparse
import numpy as np
from backend.core.interfaces.ianalyzer import IAnalyzer
from backend.services.analyzers.url_feature_extractor import extract_features, tokenize_url

class UrlXGBoostAnalyzer(IAnalyzer):
    def __init__(self, 
                 model_path: str = "backend/models/url/url_model.pkl", 
                 vectorizer_path: str = "backend/models/url/url_vectorizer.pkl",
                 features_path: str = "backend/models/url/url_features.pkl"):
        print("[MIRAGE] URL Model V3 Loaded")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(vectorizer_path):
            raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")
        if not os.path.exists(features_path):
            raise FileNotFoundError(f"Features file not found: {features_path}")
            
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        self.features_list = joblib.load(features_path)

    def analyze_url(self, url: str) -> float:
        if not url:
            return 0.0
            
        try:
            # 1. Extract lexical features
            features_dict = extract_features(url)
            
            # Ensure lexical features are aligned in the exact training order
            lexical_features = [features_dict.get(col, 0) for col in self.features_list]
            lexical_array = np.array(lexical_features).reshape(1, -1)
            
            # 2. Generate URL tokens
            tokenized_url = tokenize_url(url)
            
            # 3. Transform TF-IDF
            tfidf_features = self.vectorizer.transform([tokenized_url])
            
            # 4. Combine lexical and TF-IDF
            # scipy.sparse.hstack expects a sequence of matrices/arrays
            X = scipy.sparse.hstack([lexical_array, tfidf_features])
            
            # 5. Generate risk score
            risk_score = self.model.predict_proba(X)[0][1]
            
            return float(risk_score)
        except Exception as e:
            print(f"Error analyzing URL: {e}")
            return 0.50

    def analyze_email(self, email_text: str) -> float:
        # URL Analyzer doesn't analyze emails
        return 0.0
