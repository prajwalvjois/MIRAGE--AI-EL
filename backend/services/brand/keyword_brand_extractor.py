import re
from backend.core.interfaces.ibrand_extractor import IBrandExtractor
from backend.core.interfaces.ibrand_whitelist_provider import IBrandWhitelistProvider

class KeywordBrandExtractor(IBrandExtractor):
    def __init__(self, whitelist_provider: IBrandWhitelistProvider):
        self.whitelist_provider = whitelist_provider

    def extract_brand(self, text: str) -> str:
        if not text:
            return "Unknown"
        
        brands = self.whitelist_provider.get_brands()
        text_lower = text.lower()
        counts = {}
        
        for brand in brands:
            brand_lower = brand.lower()
            # Find all non-overlapping occurrences of the brand in the text
            count = len(re.findall(re.escape(brand_lower), text_lower))
            if count > 0:
                counts[brand] = count
                
        if not counts:
            return "Unknown"
            
        # Select the brand with the highest count. In case of ties, max() returns the first one encountered.
        winning_brand = max(counts, key=counts.get)
        return winning_brand
