from pydantic import BaseModel

class EmailAnalyzeRequest(BaseModel):
    email_text: str

class UrlAnalyzeRequest(BaseModel):
    url: str

class RiskScoreResponse(BaseModel):
    risk_score: float
    reasons: list[str] = []
