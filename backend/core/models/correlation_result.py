from pydantic import BaseModel
from typing import List

class CorrelationResult(BaseModel):
    campaign_risk: float
    campaign_brand: str
    event_count: int
    reasons: List[str]
