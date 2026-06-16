from urllib.parse import urlparse
from typing import List
from backend.core.interfaces.ireputation_analyzer import IReputationAnalyzer, ReputationResult
from backend.core.interfaces.ireputation_provider import IReputationProvider

class ReputationAnalyzer(IReputationAnalyzer):
    def __init__(self, providers: List[IReputationProvider]):
        self.providers = providers

    def _get_tld(self, domain: str) -> str:
        parts = domain.split('.')
        if len(parts) > 1:
            return parts[-1]
        return ""

    def analyze_reputation(self, url: str) -> ReputationResult:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().split(':')[0]
        if not domain:
            if "/" in url:
                domain = url.split("/")[0].lower()
            else:
                domain = url.lower()
                
        # Query providers
        score = None
        for provider in self.providers:
            prov_score = provider.get_reputation_score(domain)
            if prov_score is not None:
                score = prov_score
                break
                
        reasons = []
        
        if score is not None:
            if score < 0.3:
                level = "HIGH"
                reasons.append("Domain has strong reputation")
            elif score > 0.7:
                level = "LOW"
                reasons.append("Low reputation domain")
            else:
                level = "MODERATE"
                reasons.append("Moderate reputation domain")
        else:
            # Fallback heuristics
            tld = self._get_tld(domain)
            trusted_tlds = {"com", "org", "edu", "net", "gov", "mil"}
            rare_tlds = {"xyz", "top", "click", "zip", "biz", "info", "loan", "win", "online", "site"}
            
            if tld in trusted_tlds:
                score = 0.2
                level = "HIGH"
                reasons.append("Trusted TLD detected")
            elif tld in rare_tlds:
                score = 0.8
                level = "LOW"
                reasons.append("Rare TLD detected")
            else:
                score = 0.5
                level = "MODERATE"
                reasons.append("Unknown reputation domain")
                
        return ReputationResult(
            reputation_score=score,
            reputation_level=level,
            reasons=reasons
        )
