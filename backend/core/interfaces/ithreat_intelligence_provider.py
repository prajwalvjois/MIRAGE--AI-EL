from abc import ABC, abstractmethod

class IThreatIntelligenceProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def check_domain(self, domain: str) -> bool:
        pass
