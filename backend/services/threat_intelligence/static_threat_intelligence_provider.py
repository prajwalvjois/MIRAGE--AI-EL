import json
import os
from backend.core.interfaces.ithreat_intelligence_provider import IThreatIntelligenceProvider

class StaticThreatIntelligenceProvider(IThreatIntelligenceProvider):
    def __init__(self, config_path: str = "backend/config/known_malicious_domains.json"):
        self.config_path = config_path

    @property
    def name(self) -> str:
        return "StaticThreatIntelligenceProvider"

    def _get_domains(self) -> list[str]:
        if not os.path.exists(self.config_path):
            return []
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def check_domain(self, domain: str) -> bool:
        domains = self._get_domains()
        return domain.lower() in [d.lower() for d in domains]
