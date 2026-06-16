from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel

class DomainTrustResult(BaseModel):
    domain_age_days: Optional[int]
    is_new_domain: bool
    is_very_new_domain: bool
    registration_length_days: Optional[int]
    trust_score: float
    reasons: List[str]

class IDomainTrustAnalyzer(ABC):
    @abstractmethod
    def analyze_trust(self, url: str) -> DomainTrustResult:
        pass
