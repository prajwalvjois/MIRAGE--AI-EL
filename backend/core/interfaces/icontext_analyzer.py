from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel

class ContextAnalysisResult(BaseModel):
    keyword_count: int
    keywords_found: List[str]
    context_score: float

class IContextAnalyzer(ABC):
    @abstractmethod
    def analyze_context(self, url: str) -> ContextAnalysisResult:
        pass
