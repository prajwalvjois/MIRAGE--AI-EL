import json
import os
from typing import List
from backend.core.interfaces.iurl_risk_fusion_engine import IUrlRiskFusionEngine, UrlRiskAssessment

class WeightedUrlRiskFusionEngine(IUrlRiskFusionEngine):
    def __init__(self, config_path: str = "backend/config/url_risk_weights.json"):
        self.config_path = config_path

    def _get_weights(self) -> dict:
        default_weights = {
            "ai_score": 0.10,
            "brand_score": 0.40,
            "context_score": 0.20,
            "correlation_score": 0.30
        }
        if not os.path.exists(self.config_path):
            return default_weights
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default_weights

    def calculate_risk(self, ai_score: float, brand_score: float, context_score: float, correlation_score: float, reasons: List[str]) -> UrlRiskAssessment:
        weights = self._get_weights()
        
        final_risk = (
            (ai_score * weights.get("ai_score", 0.10)) +
            (brand_score * weights.get("brand_score", 0.40)) +
            (context_score * weights.get("context_score", 0.20)) +
            (correlation_score * weights.get("correlation_score", 0.30))
        )

        return UrlRiskAssessment(
            ai_score=ai_score,
            brand_score=brand_score,
            context_score=context_score,
            correlation_score=correlation_score,
            final_risk=final_risk,
            reasons=reasons
        )
