from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel

class CorrelationAnalysisResult(BaseModel):
    correlation_score: float
    reasons: List[str]

class IUrlCorrelationEngine(ABC):
    @abstractmethod
    def analyze_correlation(self, brand_mismatch: bool, keywords_found: List[str], extracted_brand: str) -> CorrelationAnalysisResult:
        pass
