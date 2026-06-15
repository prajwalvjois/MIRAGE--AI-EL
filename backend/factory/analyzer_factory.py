from backend.core.interfaces.ianalyzer import IAnalyzer
from backend.services.mock_analyzer import MockAnalyzer

class AnalyzerFactory:
    @staticmethod
    def get_analyzer(model_type: str = "mock") -> IAnalyzer:
        if model_type == "mock":
            return MockAnalyzer()
        raise ValueError(f"Unknown analyzer type: '{model_type}'")
