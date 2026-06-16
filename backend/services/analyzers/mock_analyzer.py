from backend.core.interfaces.ianalyzer import IAnalyzer

class MockAnalyzer(IAnalyzer):
    def analyze_email(self, email_text: str) -> float:
        # Mock logic as requested
        return 0.85

    def analyze_url(self, url: str) -> float:
        # Mock logic as requested
        return 0.30
