import json
import os
from typing import Dict, List
from backend.core.interfaces.ibrand_domain_provider import IBrandDomainProvider

class StaticBrandDomainProvider(IBrandDomainProvider):
    def __init__(self, config_path: str = "backend/config/brand_domains.json"):
        self.config_path = config_path

    def get_brand_domains(self) -> Dict[str, List[str]]:
        if not os.path.exists(self.config_path):
            return {}
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
