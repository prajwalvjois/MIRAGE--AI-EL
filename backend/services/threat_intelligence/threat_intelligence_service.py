from urllib.parse import urlparse
from typing import List
from backend.core.interfaces.ithreat_intelligence_provider import IThreatIntelligenceProvider
from backend.core.interfaces.ithreat_intelligence_service import IThreatIntelligenceService, ThreatIntelligenceResult

class ThreatIntelligenceService(IThreatIntelligenceService):
    def __init__(self, providers: List[IThreatIntelligenceProvider]):
        self.providers = providers

    def check_url(self, url: str) -> ThreatIntelligenceResult:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if not domain:
            if "/" in url:
                domain = url.split("/")[0].lower()
            else:
                domain = url.lower()
                
        if ":" in domain:
            domain = domain.split(":")[0]

        for provider in self.providers:
            if provider.check_domain(domain):
                return ThreatIntelligenceResult(
                    is_known_malicious=True,
                    source=provider.name,
                    matched_domain=domain
                )
        
        return ThreatIntelligenceResult(is_known_malicious=False)
