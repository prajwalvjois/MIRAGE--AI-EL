from urllib.parse import urlparse
from backend.core.interfaces.ibrand_impersonation_analyzer import IBrandImpersonationAnalyzer, BrandAnalysisResult
from backend.core.interfaces.ibrand_domain_provider import IBrandDomainProvider

class BrandImpersonationAnalyzer(IBrandImpersonationAnalyzer):
    def __init__(self, domain_provider: IBrandDomainProvider):
        self.domain_provider = domain_provider

    def analyze_brand(self, url: str, extracted_brand: str) -> BrandAnalysisResult:
        if extracted_brand == "Unknown" or not extracted_brand:
            return BrandAnalysisResult(
                brand="Unknown",
                has_brand=False,
                brand_mismatch=False,
                brand_score=0.0
            )

        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        if not domain:
            # try to parse domain directly from string if no scheme provided
            if "/" in url:
                domain = url.split("/")[0].lower()
            else:
                domain = url.lower()
        
        # Remove port if present
        if ":" in domain:
            domain = domain.split(":")[0]
            
        # extract root domain to match against config
        domain_parts = domain.split(".")
        
        official_domains = self.domain_provider.get_brand_domains().get(extracted_brand, [])
        official_domains_lower = [d.lower() for d in official_domains]
        
        # check if it ends with one of the official domains
        mismatch = True
        for off_dom in official_domains_lower:
            if domain == off_dom or domain.endswith("." + off_dom):
                mismatch = False
                break
                
        has_brand = True
        brand_score = 1.0 if mismatch else 0.0

        return BrandAnalysisResult(
            brand=extracted_brand,
            has_brand=has_brand,
            brand_mismatch=mismatch,
            brand_score=brand_score
        )
