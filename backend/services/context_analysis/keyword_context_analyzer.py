import json
import os
import re
from typing import List
from backend.core.interfaces.icontext_analyzer import IContextAnalyzer, ContextAnalysisResult

class KeywordContextAnalyzer(IContextAnalyzer):
    def __init__(self, config_path: str = "backend/config/keywords.json"):
        self.config_path = config_path

    def _get_keywords(self) -> List[str]:
        if not os.path.exists(self.config_path):
            return []
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def analyze_context(self, url: str) -> ContextAnalysisResult:
        keywords = self._get_keywords()
        url_lower = url.lower()
        
        # Split URL into tokens separating by non-alphanumeric chars
        tokens = re.split(r"[^a-zA-Z0-9]", url_lower)
        
        found = []
        for kw in keywords:
            kw_lower = kw.lower()
            # check if keyword appears as a substring or exact piece in tokens
            if kw_lower in url_lower:
                found.append(kw)
                
        count = len(found)
        if count == 0:
            score = 0.0
        elif count == 1:
            score = 0.25
        elif count == 2:
            score = 0.50
        elif count == 3:
            score = 0.75
        else:
            score = 1.0
            
        return ContextAnalysisResult(
            keyword_count=count,
            keywords_found=found,
            context_score=score
        )
