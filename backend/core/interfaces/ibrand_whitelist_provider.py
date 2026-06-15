from abc import ABC, abstractmethod

class IBrandWhitelistProvider(ABC):
    @abstractmethod
    def get_brands(self) -> list[str]:
        pass
