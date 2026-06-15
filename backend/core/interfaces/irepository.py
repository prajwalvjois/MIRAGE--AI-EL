from abc import ABC, abstractmethod
from typing import List
from backend.core.models.threat_event import ThreatEvent

class IRepository(ABC):
    @abstractmethod
    def save_email_event(self, email_text: str, brand: str, risk_score: float) -> str:
        """Saves an email analysis event and returns the record ID."""
        pass

    @abstractmethod
    def save_url_event(self, url: str, brand: str, risk_score: float) -> str:
        """Saves a URL analysis event and returns the record ID."""
        pass

    @abstractmethod
    def get_recent_events(self, limit: int = 100) -> List[ThreatEvent]:
        """Retrieves recent threat events for correlation purposes."""
        pass
