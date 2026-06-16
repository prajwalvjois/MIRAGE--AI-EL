from backend.factory.url_intelligence_factory import UrlIntelligenceFactory

service = UrlIntelligenceFactory.get_service()
res = service.analyze("https://paypal-login-security.com")
print(res)

res2 = service.analyze("https://github-login-security.com")
print(res2)

res3 = service.analyze("https://google.com")
print(res3)
