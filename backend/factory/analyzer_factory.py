from backend.core.interfaces.ianalyzer import IAnalyzer
from backend.services.analyzers.mock_analyzer import MockAnalyzer
from backend.services.analyzers.email_xgboost_analyzer import EmailXGBoostAnalyzer

class AnalyzerFactory:
    # Need to keep the initialized components so we only load it once,
    # as per instructions: "Do NOT load on every request" ->
    # But EmailXGBoostAnalyzer load files ONLY in its __init__. 
    # If get_analyzer is called per request in FastAPI Depend, it will instantiate a new one!
    # So we should cache it here or in the analyzer.
    _email_xgboost_instance = None
    _mock_instance = None

    @classmethod
    def get_analyzer(cls, model_type: str = "mock") -> IAnalyzer:
        if model_type == "mock":
            if cls._mock_instance is None:
                cls._mock_instance = MockAnalyzer()
            return cls._mock_instance
        elif model_type == "email_xgboost":
            if cls._email_xgboost_instance is None:
                cls._email_xgboost_instance = EmailXGBoostAnalyzer()
            return cls._email_xgboost_instance
        raise ValueError(f"Unknown analyzer type: '{model_type}'")
