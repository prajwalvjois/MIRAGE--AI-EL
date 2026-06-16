import os
import joblib
import pandas as pd
from backend.core.interfaces.ianalyzer import IAnalyzer
from backend.utils.url_feature_extractor import extract_features

class UrlXGBoostAnalyzer(IAnalyzer):
    def __init__(self, model_path: str = "backend/models/url/url_model.pkl", features_path: str = "backend/models/url/url_features.pkl"):
        print("[MIRAGE] URL Model Loaded")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(features_path):
            raise FileNotFoundError(f"Features file not found: {features_path}")
            
        self.model = joblib.load(model_path)
        self.feature_columns = joblib.load(features_path)

    def analyze_email(self, email_text: str) -> float:
        # Fallback to MockAnalyzer logic for emails if called
        return 0.30

    def analyze_url(self, url: str) -> float:
        if not url:
            return 0.0
            
        features = extract_features(url)
        X = pd.DataFrame([features])
        X = X.reindex(columns=self.feature_columns, fill_value=0)
        
        risk_score = self.model.predict_proba(X)[0][1]
        
        print(f"[MIRAGE] URL Risk Score: {risk_score}")
        return float(risk_score)
