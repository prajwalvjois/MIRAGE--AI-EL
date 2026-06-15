from pydantic import BaseModel
from datetime import datetime

class ThreatEvent(BaseModel):
    event_id: str
    event_type: str
    risk_score: float
    brand: str
    timestamp: datetime
