from abc import ABC, abstractmethod

class IRepository(ABC):
    @abstractmethod
    def save_email_event(self, email_text: str, risk_score: float) -> str:
        """Saves an email analysis event and returns the record ID."""
        pass

    @abstractmethod
    def save_url_event(self, url: str, risk_score: float) -> str:
        """Saves a URL analysis event and returns the record ID."""
        pass
