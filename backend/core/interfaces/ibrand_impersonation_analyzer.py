from abc import ABC, abstractmethod
from pydantic import BaseModel

class BrandAnalysisResult(BaseModel):
    brand: str
    has_brand: bool
    brand_mismatch: bool
    brand_score: float

class IBrandImpersonationAnalyzer(ABC):
    @abstractmethod
    def analyze_brand(self, domain: str, extracted_brand: str) -> BrandAnalysisResult:
        pass
