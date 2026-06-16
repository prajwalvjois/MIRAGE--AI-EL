from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel

class UrlRiskAssessment(BaseModel):
    ai_score: float
    brand_score: float
    context_score: float
    correlation_score: float
    final_risk: float
    reasons: List[str]

class IUrlRiskFusionEngine(ABC):
    @abstractmethod
    def calculate_risk(self, ai_score: float, brand_score: float, context_score: float, correlation_score: float, reasons: List[str]) -> UrlRiskAssessment:
        pass
