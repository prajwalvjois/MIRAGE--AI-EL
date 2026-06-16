from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel

class ReputationResult(BaseModel):
    reputation_score: float
    reputation_level: str
    reasons: List[str]

class IReputationAnalyzer(ABC):
    @abstractmethod
    def analyze_reputation(self, url: str) -> ReputationResult:
        pass
