from fastapi import APIRouter, Depends
from backend.api.models import EmailAnalyzeRequest, UrlAnalyzeRequest, RiskScoreResponse
from backend.core.interfaces.ianalyzer import IAnalyzer
from backend.core.interfaces.irepository import IRepository
from backend.factory.analyzer_factory import AnalyzerFactory
from backend.repository.sqlite_repository import SQLiteRepository

router = APIRouter()

# Dependency injection for the analyzer
def get_analyzer() -> IAnalyzer:
    return AnalyzerFactory.get_analyzer("mock")

# Dependency injection for the repository
def get_repository() -> IRepository:
    return SQLiteRepository()

@router.post("/analyze-email", response_model=RiskScoreResponse)
async def analyze_email(
    request: EmailAnalyzeRequest, 
    analyzer: IAnalyzer = Depends(get_analyzer),
    repository: IRepository = Depends(get_repository)
):
    risk_score = analyzer.analyze_email(request.email_text)
    repository.save_email_event(request.email_text, risk_score)
    return RiskScoreResponse(risk_score=risk_score)

@router.post("/analyze-url", response_model=RiskScoreResponse)
async def analyze_url(
    request: UrlAnalyzeRequest, 
    analyzer: IAnalyzer = Depends(get_analyzer),
    repository: IRepository = Depends(get_repository)
):
    risk_score = analyzer.analyze_url(request.url)
    repository.save_url_event(request.url, risk_score)
    return RiskScoreResponse(risk_score=risk_score)
