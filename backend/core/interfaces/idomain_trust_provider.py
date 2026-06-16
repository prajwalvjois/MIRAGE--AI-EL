from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

class WhoisInfo:
    def __init__(self, creation_date: Optional[datetime], expiration_date: Optional[datetime], registrar: Optional[str]):
        self.creation_date = creation_date
        self.expiration_date = expiration_date
        self.registrar = registrar

class IDomainTrustProvider(ABC):
    @abstractmethod
    def get_domain_info(self, domain: str) -> Optional[WhoisInfo]:
        pass
