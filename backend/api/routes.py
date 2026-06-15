from fastapi import APIRouter, Depends
from datetime import datetime
from backend.api.models import EmailAnalyzeRequest, UrlAnalyzeRequest, RiskScoreResponse
from backend.core.interfaces.ianalyzer import IAnalyzer
from backend.core.interfaces.irepository import IRepository
from backend.core.interfaces.ibrand_extractor import IBrandExtractor
from backend.core.interfaces.icorrelation_engine import ICorrelationEngine
from backend.core.models.threat_event import ThreatEvent
from backend.factory.analyzer_factory import AnalyzerFactory
from backend.factory.brand_extractor_factory import BrandExtractorFactory
from backend.factory.correlation_engine_factory import CorrelationEngineFactory
from backend.repository.sqlite_repository import SQLiteRepository

router = APIRouter()

# Dependency injection for the analyzer
def get_analyzer() -> IAnalyzer:
    return AnalyzerFactory.get_analyzer("mock")

# Dependency injection for the repository
def get_repository() -> IRepository:
    return SQLiteRepository()

# Dependency injection for brand extractor
def get_brand_extractor() -> IBrandExtractor:
    return BrandExtractorFactory.get_brand_extractor("keyword")

# Dependency injection for correlation engine
def get_correlation_engine() -> ICorrelationEngine:
    return CorrelationEngineFactory.get_correlation_engine("weighted")


@router.post("/analyze-email", response_model=RiskScoreResponse)
async def analyze_email(
    request: EmailAnalyzeRequest, 
    analyzer: IAnalyzer = Depends(get_analyzer),
    repository: IRepository = Depends(get_repository),
    brand_extractor: IBrandExtractor = Depends(get_brand_extractor),
    correlation_engine: ICorrelationEngine = Depends(get_correlation_engine)
):
    risk_score = analyzer.analyze_email(request.email_text)
    brand = brand_extractor.extract_brand(request.email_text)
    event_id = repository.save_email_event(request.email_text, brand, risk_score)
    
    current_event = ThreatEvent(
        event_id=event_id,
        event_type="EMAIL",
        risk_score=risk_score,
        brand=brand,
        timestamp=datetime.now()
    )
    recent_events = repository.get_recent_events(limit=100)
    correlation_result = correlation_engine.correlate(current_event, recent_events)
    
    if correlation_result:
        print("\n[MIRAGE]")
        print("Campaign Detected")
        print(f"Brand: {correlation_result.campaign_brand}")
        print(f"Event Count: {correlation_result.event_count}")
        print(f"Campaign Risk: {correlation_result.campaign_risk:.2f}")
        print("Reasons:")
        for reason in correlation_result.reasons:
            print(f"- {reason}")
        print()
        
    return RiskScoreResponse(risk_score=risk_score)

@router.post("/analyze-url", response_model=RiskScoreResponse)
async def analyze_url(
    request: UrlAnalyzeRequest, 
    analyzer: IAnalyzer = Depends(get_analyzer),
    repository: IRepository = Depends(get_repository),
    brand_extractor: IBrandExtractor = Depends(get_brand_extractor),
    correlation_engine: ICorrelationEngine = Depends(get_correlation_engine)
):
    risk_score = analyzer.analyze_url(request.url)
    brand = brand_extractor.extract_brand(request.url)
    event_id = repository.save_url_event(request.url, brand, risk_score)
    
    current_event = ThreatEvent(
        event_id=event_id,
        event_type="URL",
        risk_score=risk_score,
        brand=brand,
        timestamp=datetime.now()
    )
    recent_events = repository.get_recent_events(limit=100)
    correlation_result = correlation_engine.correlate(current_event, recent_events)
    
    if correlation_result:
        print("\n[MIRAGE]")
        print("Campaign Detected")
        print(f"Brand: {correlation_result.campaign_brand}")
        print(f"Event Count: {correlation_result.event_count}")
        print(f"Campaign Risk: {correlation_result.campaign_risk:.2f}")
        print("Reasons:")
        for reason in correlation_result.reasons:
            print(f"- {reason}")
        print()
        
    return RiskScoreResponse(risk_score=risk_score)
