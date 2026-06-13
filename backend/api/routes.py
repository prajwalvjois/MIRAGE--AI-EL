from fastapi import APIRouter, Depends
from backend.api.models import EmailAnalyzeRequest, UrlAnalyzeRequest, RiskScoreResponse
from backend.core.interfaces.ianalyzer import IAnalyzer
from backend.services.mock_analyzer import MockAnalyzer

router = APIRouter()

# Dependency injection for the analyzer
def get_analyzer() -> IAnalyzer:
    return MockAnalyzer()

@router.post("/analyze-email", response_model=RiskScoreResponse)
async def analyze_email(request: EmailAnalyzeRequest, analyzer: IAnalyzer = Depends(get_analyzer)):
    risk_score = analyzer.analyze_email(request.email_text)
    return RiskScoreResponse(risk_score=risk_score)

@router.post("/analyze-url", response_model=RiskScoreResponse)
async def analyze_url(request: UrlAnalyzeRequest, analyzer: IAnalyzer = Depends(get_analyzer)):
    risk_score = analyzer.analyze_url(request.url)
    return RiskScoreResponse(risk_score=risk_score)
