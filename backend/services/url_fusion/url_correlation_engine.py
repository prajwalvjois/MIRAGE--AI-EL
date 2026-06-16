from typing import List
from backend.core.interfaces.iurl_correlation_engine import IUrlCorrelationEngine, CorrelationAnalysisResult

class UrlCorrelationEngine(IUrlCorrelationEngine):
    def analyze_correlation(self, brand_mismatch: bool, keywords_found: List[str], extracted_brand: str) -> CorrelationAnalysisResult:
        correlation_score = 0.0
        reasons = []

        if brand_mismatch and len(keywords_found) > 0:
            correlation_score = 1.0
            reasons.append("Brand/keyword correlation detected")
            
        return CorrelationAnalysisResult(
            correlation_score=correlation_score,
            reasons=reasons
        )
