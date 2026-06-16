from typing import List
from backend.core.interfaces.ibrand_extractor import IBrandExtractor
from backend.core.interfaces.ianalyzer import IAnalyzer
from backend.core.interfaces.ibrand_impersonation_analyzer import IBrandImpersonationAnalyzer
from backend.core.interfaces.icontext_analyzer import IContextAnalyzer
from backend.core.interfaces.iurl_correlation_engine import IUrlCorrelationEngine
from backend.core.interfaces.iurl_risk_fusion_engine import IUrlRiskFusionEngine, UrlRiskAssessment
from backend.core.interfaces.ithreat_intelligence_service import IThreatIntelligenceService

class UrlIntelligenceService:
    def __init__(self,
                 ai_model: IAnalyzer,
                 brand_extractor: IBrandExtractor,
                 brand_analyzer: IBrandImpersonationAnalyzer,
                 context_analyzer: IContextAnalyzer,
                 correlation_engine: IUrlCorrelationEngine,
                 fusion_engine: IUrlRiskFusionEngine,
                 threat_service: IThreatIntelligenceService):
        self.ai_model = ai_model
        self.brand_extractor = brand_extractor
        self.brand_analyzer = brand_analyzer
        self.context_analyzer = context_analyzer
        self.correlation_engine = correlation_engine
        self.fusion_engine = fusion_engine
        self.threat_service = threat_service

    def analyze(self, url: str) -> UrlRiskAssessment:
        # 0. Threat Intelligence
        threat_result = self.threat_service.check_url(url)
        if threat_result.is_known_malicious:
            print("[MIRAGE] Threat Intelligence Match:")
            print(threat_result.matched_domain)
            print("Source:")
            print(threat_result.source)
            print("Risk Forced:")
            print("1.0")

            return UrlRiskAssessment(
                ai_score=0.0,
                brand_score=0.0,
                context_score=0.0,
                correlation_score=0.0,
                final_risk=1.0,
                reasons=["Known malicious domain"]
            )

        reasons: List[str] = []

        # 1. AI Score
        ai_score = self.ai_model.analyze_url(url)
        
        # 2. Extract Brand
        brand = self.brand_extractor.extract_brand(url)
        
        # 3. Brand Impersonation
        brand_result = self.brand_analyzer.analyze_brand(url, brand)
        if brand_result.has_brand:
            reasons.append(f"Brand detected: {brand_result.brand}")
            if brand_result.brand_mismatch:
                reasons.append("Brand mismatch detected")

        # 4. Context Analysis
        context_result = self.context_analyzer.analyze_context(url)
        if context_result.keyword_count > 0:
            reasons.append(f"Keywords found: {', '.join(context_result.keywords_found)}")

        # 5. Correlation Analysis
        correlation_result = self.correlation_engine.analyze_correlation(
            brand_mismatch=brand_result.brand_mismatch,
            keywords_found=context_result.keywords_found,
            extracted_brand=brand_result.brand
        )
        for reason in correlation_result.reasons:
            reasons.append(reason)

        # 6. Fusion
        fusion_result = self.fusion_engine.calculate_risk(
            ai_score=ai_score,
            brand_score=brand_result.brand_score,
            context_score=context_result.context_score,
            correlation_score=correlation_result.correlation_score,
            reasons=reasons
        )

        print(f"[MIRAGE] URL AI Score: {ai_score}")
        print(f"[MIRAGE] URL Final Risk: {fusion_result.final_risk}")

        return fusion_result
