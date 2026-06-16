import os
import joblib
from backend.core.interfaces.ianalyzer import IAnalyzer

class EmailXGBoostAnalyzer(IAnalyzer):
    def __init__(self, model_path: str = "backend/models/email/email_model.pkl", vectorizer_path: str = "backend/models/email/email_features.pkl"):
        # We need absolute or relative paths handled properly, but the working directory is the app root
        print("[MIRAGE] Email Model Loaded")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(vectorizer_path):
            raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")
            
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    def analyze_email(self, email_text: str) -> float:
        if not email_text:
            return 0.0
            
        X = self.vectorizer.transform([email_text])
        risk_score = self.model.predict_proba(X)[0][1]
        
        print(f"[MIRAGE] Email Risk Score: {risk_score}")
        return float(risk_score)

    def analyze_url(self, url: str) -> float:
        # Fallback to MockAnalyzer logic for URLs as per instructions
        return 0.30
