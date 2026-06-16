import re
import math
from urllib.parse import urlparse
import tldextract


def entropy(text):
    if not text:
        return 0

    prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(text)]

    return -sum(p * math.log2(p) for p in prob)


def extract_features(url):

    parsed = urlparse(url)

    domain = parsed.netloc

    ext = tldextract.extract(url)

    tld = ext.suffix

    features = {}

    # Length features

    features["url_length"] = len(url)

    features["domain_length"] = len(domain)

    features["tld_length"] = len(tld)

    features["path_length"] = len(parsed.path)

    features["query_length"] = len(parsed.query)

    # Structure features

    features["subdomain_count"] = len(ext.subdomain.split(".")) if ext.subdomain else 0

    features["slash_count"] = url.count("/")

    features["dot_count"] = url.count(".")

    features["hyphen_count"] = url.count("-")

    features["underscore_count"] = url.count("_")

    # Character features

    features["digit_count"] = sum(c.isdigit() for c in url)

    features["letter_count"] = sum(c.isalpha() for c in url)

    features["special_char_count"] = len(re.findall(r"[^a-zA-Z0-9]", url))

    # Security indicators

    features["has_https"] = int(url.startswith("https"))

    features["has_at_symbol"] = int("@" in url)

    features["has_double_slash"] = int("//" in url[8:])

    # IP address detection

    ip_pattern = r"(\d{1,3}\.){3}\d{1,3}"

    features["is_ip_address"] = int(bool(re.search(ip_pattern, domain)))

    # Obfuscation indicators

    features["percent_encoding_count"] = url.count("%")

    features["entropy"] = entropy(url)

    return features