from backend.services.brand_impersonation.static_brand_domain_provider import StaticBrandDomainProvider
from backend.services.brand_impersonation.brand_impersonation_analyzer import BrandImpersonationAnalyzer
from backend.services.context_analysis.keyword_context_analyzer import KeywordContextAnalyzer
from backend.services.url_fusion.url_correlation_engine import UrlCorrelationEngine
from backend.services.url_fusion.weighted_url_risk_fusion_engine import WeightedUrlRiskFusionEngine
from backend.services.url_orchestrator.url_intelligence_service import UrlIntelligenceService
from backend.factory.analyzer_factory import AnalyzerFactory
from backend.factory.brand_extractor_factory import BrandExtractorFactory

class UrlIntelligenceFactory:
    _instance = None

    @classmethod
    def get_service(cls) -> UrlIntelligenceService:
        if cls._instance is None:
            # Inject dependencies
            domain_provider = StaticBrandDomainProvider()
            brand_analyzer = BrandImpersonationAnalyzer(domain_provider)
            context_analyzer = KeywordContextAnalyzer()
            correlation_engine = UrlCorrelationEngine()
            fusion_engine = WeightedUrlRiskFusionEngine()
            
            ai_model = AnalyzerFactory.get_analyzer("url_xgboost")
            brand_extractor = BrandExtractorFactory.get_brand_extractor("keyword")
            
            cls._instance = UrlIntelligenceService(
                ai_model=ai_model,
                brand_extractor=brand_extractor,
                brand_analyzer=brand_analyzer,
                context_analyzer=context_analyzer,
                correlation_engine=correlation_engine,
                fusion_engine=fusion_engine
            )
        return cls._instance
