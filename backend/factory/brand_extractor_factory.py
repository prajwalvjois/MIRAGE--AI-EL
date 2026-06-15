from backend.core.interfaces.ibrand_extractor import IBrandExtractor
from backend.services.brand.keyword_brand_extractor import KeywordBrandExtractor
from backend.providers.whitelist.static_whitelist_provider import StaticWhitelistProvider

class BrandExtractorFactory:
    @staticmethod
    def get_brand_extractor(extractor_type: str = "keyword") -> IBrandExtractor:
        if extractor_type == "keyword":
            whitelist_provider = StaticWhitelistProvider()
            return KeywordBrandExtractor(whitelist_provider)
        raise ValueError(f"Unknown brand extractor type: '{extractor_type}'")
