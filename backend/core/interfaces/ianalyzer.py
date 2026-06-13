from abc import ABC, abstractmethod

class IAnalyzer(ABC):
    @abstractmethod
    def analyze_email(self, email_text: str) -> float:
        pass

    @abstractmethod
    def analyze_url(self, url: str) -> float:
        pass
