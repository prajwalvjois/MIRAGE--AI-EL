from abc import ABC, abstractmethod

class IBrandExtractor(ABC):
    @abstractmethod
    def extract_brand(self, text: str) -> str:
        """Returns Brand Name or 'Unknown'"""
        pass
