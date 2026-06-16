from abc import ABC, abstractmethod
from typing import Dict, List

class IBrandDomainProvider(ABC):
    @abstractmethod
    def get_brand_domains(self) -> Dict[str, List[str]]:
        pass
