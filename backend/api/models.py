from pydantic import BaseModel

class EmailAnalyzeRequest(BaseModel):
    email_text: str

class UrlAnalyzeRequest(BaseModel):
    url: str

class RiskScoreResponse(BaseModel):
    risk_score: float
    reasons: list[str] = []
    ai_score: float = 0.0
    brand_score: float = 0.0
    context_score: float = 0.0
    correlation_score: float = 0.0
    domain_trust_score: float = 0.0
    reputation_score: float = 0.0
