from abc import ABC, abstractmethod
from pydantic import BaseModel

class ThreatIntelligenceResult(BaseModel):
    is_known_malicious: bool
    source: str = ""
    matched_domain: str = ""

class IThreatIntelligenceService(ABC):
    @abstractmethod
    def check_url(self, url: str) -> ThreatIntelligenceResult:
        pass
