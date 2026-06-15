import json
import os
from backend.core.interfaces.ibrand_whitelist_provider import IBrandWhitelistProvider

class StaticWhitelistProvider(IBrandWhitelistProvider):
    def __init__(self, config_path: str = "backend/config/brands.json"):
        self.config_path = config_path

    def get_brands(self) -> list[str]:
        if not os.path.exists(self.config_path):
            return []
            
        with open(self.config_path, "r", encoding="utf-8") as f:
            brands = json.load(f)
            
        return brands
