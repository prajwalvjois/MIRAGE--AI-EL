from pydantic import BaseModel
from typing import Optional

class EmailAnalyzeRequest(BaseModel):
    email_text: str

class UrlAnalyzeRequest(BaseModel):
    url: str

class CampaignResponse(BaseModel):
    brand: str
    related_events: int
    campaign_risk: float

class RiskScoreResponse(BaseModel):
    risk_score: float
    reasons: list[str] = []
    ai_score: float = 0.0
    brand_score: float = 0.0
    context_score: float = 0.0
    correlation_score: float = 0.0
    domain_trust_score: float = 0.0
    reputation_score: float = 0.0
    campaign: Optional[CampaignResponse] = None
