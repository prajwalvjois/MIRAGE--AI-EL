from backend.core.interfaces.ianalyzer import IAnalyzer
from backend.services.analyzers.mock_analyzer import MockAnalyzer
from backend.services.analyzers.email_distilbert_analyzer import EmailDistilBERTAnalyzer
from backend.services.analyzers.url_xgboost_analyzer import UrlXGBoostAnalyzer

class AnalyzerFactory:
    # Need to keep the initialized components so we only load it once,
    # as per instructions: "Do NOT load on every request" ->
    # But EmailDistilBERTAnalyzer load files ONLY in its __init__. 
    # If get_analyzer is called per request in FastAPI Depend, it will instantiate a new one!
    # So we should cache it here or in the analyzer.
    _email_distilbert_instance = None
    _url_xgboost_instance = None
    _mock_instance = None

    @classmethod
    def get_analyzer(cls, model_type: str = "mock") -> IAnalyzer:
        if model_type == "mock":
            if cls._mock_instance is None:
                cls._mock_instance = MockAnalyzer()
            return cls._mock_instance
        elif model_type == "email_distilbert":
            if cls._email_distilbert_instance is None:
                cls._email_distilbert_instance = EmailDistilBERTAnalyzer()
            return cls._email_distilbert_instance
        elif model_type == "url_xgboost":
            if cls._url_xgboost_instance is None:
                cls._url_xgboost_instance = UrlXGBoostAnalyzer()
            return cls._url_xgboost_instance
        raise ValueError(f"Unknown analyzer type: '{model_type}'")
