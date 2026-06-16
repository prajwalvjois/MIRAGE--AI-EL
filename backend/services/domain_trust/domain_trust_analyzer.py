from datetime import datetime, timezone
from urllib.parse import urlparse
from typing import Optional
from backend.core.interfaces.idomain_trust_analyzer import IDomainTrustAnalyzer, DomainTrustResult
from backend.core.interfaces.idomain_trust_provider import IDomainTrustProvider

class DomainTrustAnalyzer(IDomainTrustAnalyzer):
    def __init__(self, provider: IDomainTrustProvider):
        self.provider = provider

    def analyze_trust(self, url: str) -> DomainTrustResult:
        parsed = urlparse(url)
        domain = parsed.netloc if parsed.netloc else url
        domain = domain.lower().split(':')[0]
        if '/' in domain:
            domain = domain.split('/')[0]

        info = self.provider.get_domain_info(domain)

        if not info or not info.creation_date:
            return DomainTrustResult(
                domain_age_days=0,
                is_new_domain=False,
                is_very_new_domain=False,
                registration_length_days=0,
                trust_score=0.0,
                reasons=["Domain trust unavailable"]
            )

        now = datetime.now()
        
        # Ensure we can subtract
        try:
            creation = info.creation_date
            if creation.tzinfo is not None:
                # If timezone aware, convert now to aware
                now = datetime.now(timezone.utc)
                
            age_timedelta = now - creation
            domain_age_days = age_timedelta.days

            # Also calc registration length if expiration exists
            reg_length_days = 0
            if info.expiration_date:
                expiration = info.expiration_date
                if expiration.tzinfo is not None and creation.tzinfo is None:
                    # handle timezone mismatch if any? We assume simple enough for now
                    pass
                try:
                    reg_length_timedelta = expiration - creation
                    reg_length_days = reg_length_timedelta.days
                except Exception:
                    pass

        except Exception as e:
            print(f"[MIRAGE] Domain Trust Analysis error dates: {e}")
            return DomainTrustResult(
                domain_age_days=0,
                is_new_domain=False,
                is_very_new_domain=False,
                registration_length_days=0,
                trust_score=0.0,
                reasons=["Domain trust unavailable"]
            )

        if domain_age_days < 0:
            domain_age_days = 0

        is_new_domain = domain_age_days < 30
        is_very_new_domain = domain_age_days < 7

        score = 0.0
        reasons = []

        if is_very_new_domain:
            score = 1.0
            reasons.append("Domain registered less than 7 days ago")
        elif is_new_domain:
            score = 0.9
            reasons.append("Domain age less than 30 days")
        elif domain_age_days < 180:
            score = 0.5
            reasons.append("Domain age less than 6 months")
        else:
            score = 0.0 # Old domain, low risk
            if domain_age_days > 5 * 365:
                reasons.append("Domain age > 5 years")
            
        # Optional: Registration length signal if very short
        if reg_length_days > 0 and reg_length_days <= 365:
            # Registration length of exactly 1 year is common, but < 1 year could be risk factor.
            # We don't overwrite high scores but add reasons
            if score < 0.3:
                score += 0.2
            reasons.append("Short registration period detected")
                
        if not reasons:
            reasons.append("Old domain")

        return DomainTrustResult(
            domain_age_days=domain_age_days,
            is_new_domain=is_new_domain,
            is_very_new_domain=is_very_new_domain,
            registration_length_days=reg_length_days,
            trust_score=score,
            reasons=reasons
        )
