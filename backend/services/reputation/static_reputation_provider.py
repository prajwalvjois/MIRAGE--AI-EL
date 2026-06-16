import json
import os
from typing import Optional
from backend.core.interfaces.ireputation_provider import IReputationProvider

class StaticReputationProvider(IReputationProvider):
    def __init__(self, config_path: str = "backend/config/reputation_domains.json"):
        self.config_path = config_path
        self._reputation_data = {}
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self._reputation_data = json.load(f)
            except Exception:
                pass

    @property
    def name(self) -> str:
        return "StaticReputationProvider"

    def get_reputation_score(self, domain: str) -> Optional[float]:
        return self._reputation_data.get(domain.lower())
