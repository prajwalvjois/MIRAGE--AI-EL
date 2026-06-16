import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from backend.factory.url_intelligence_factory import UrlIntelligenceFactory

service = UrlIntelligenceFactory.get_service()
service.analyze('https://google.com')
service.analyze('https://very-new-phishing-domain-xyz.com')
