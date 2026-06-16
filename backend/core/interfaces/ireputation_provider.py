from abc import ABC, abstractmethod
from typing import Optional

class IReputationProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_reputation_score(self, domain: str) -> Optional[float]:
        pass
