from abc import ABC, abstractmethod
from typing import List, Optional
from backend.core.models.threat_event import ThreatEvent
from backend.core.models.correlation_result import CorrelationResult

class ICorrelationEngine(ABC):
    @abstractmethod
    def correlate(self, event: ThreatEvent, recent_events: List[ThreatEvent]) -> Optional[CorrelationResult]:
        pass
