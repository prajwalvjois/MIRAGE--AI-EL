import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.analyzers.url_xgboost_analyzer import UrlXGBoostAnalyzer

analyzer = UrlXGBoostAnalyzer("backend/models/url/url_model.pkl", "backend/models/url/url_features.pkl")
score = analyzer.analyze_url("chrome://newtab/")
print("Score for chrome://newtab/ = ", score)

score2 = analyzer.analyze_url("https://mail.google.com/")
print("Score for https://mail.google.com/ = ", score2)
