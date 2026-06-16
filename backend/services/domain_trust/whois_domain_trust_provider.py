import time
try:
    import whois
except ImportError:
    whois = None

from urllib.parse import urlparse
from datetime import datetime
from typing import Optional
from backend.core.interfaces.idomain_trust_provider import IDomainTrustProvider, WhoisInfo

class WhoisDomainTrustProvider(IDomainTrustProvider):
    def __init__(self):
        # Cache format: { "domain": (WhoisInfo or None, expiry_timestamp) }
        self._cache = {}
        self._cache_ttl = 24 * 3600  # 24 hours

    def get_domain_info(self, domain: str) -> Optional[WhoisInfo]:
        now = time.time()
        
        # Clean domain
        parsed = urlparse(domain)
        netloc = parsed.netloc if parsed.netloc else domain
        netloc = netloc.lower().split(':')[0]
        if '/' in netloc:
            netloc = netloc.split('/')[0]

        # Return from cache if valid
        if netloc in self._cache:
            entry, expiry = self._cache[netloc]
            if now < expiry:
                return entry

        # Fetch WHOIS
        try:
            if whois is None:
                raise ImportError("python-whois is not installed")
                
            w = whois.whois(netloc)
            creation_date = w.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
                
            expiration_date = w.expiration_date
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]
                
            registrar = w.registrar
            if isinstance(registrar, list):
                registrar = registrar[0]

            info = WhoisInfo(
                creation_date=creation_date,
                expiration_date=expiration_date,
                registrar=registrar
            )
            
            # Cache the result
            self._cache[netloc] = (info, now + self._cache_ttl)
            return info
            
        except Exception as e:
            print(f"[MIRAGE] WHOIS lookup failed for {netloc}: {e}")
            self._cache[netloc] = (None, now + self._cache_ttl)
            return None
