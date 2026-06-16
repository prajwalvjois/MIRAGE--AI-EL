import re
import math
from urllib.parse import urlparse


def calculate_entropy(text):
    if not text:
        return 0

    entropy = 0

    for char in set(text):
        p = text.count(char) / len(text)
        entropy -= p * math.log2(p)

    return entropy


def extract_features(url):

    parsed = urlparse(url)

    domain = parsed.netloc
    path = parsed.path
    query = parsed.query

    features = {

        "url_length": len(url),

        "domain_length": len(domain),

        "tld_length":
            len(domain.split(".")[-1])
            if "." in domain else 0,

        "path_length": len(path),

        "query_length": len(query),

        "subdomain_count":
            max(len(domain.split(".")) - 2, 0),

        "slash_count":
            url.count("/"),

        "dot_count":
            url.count("."),

        "hyphen_count":
            url.count("-"),

        "underscore_count":
            url.count("_"),

        "digit_count":
            sum(c.isdigit() for c in url),

        "letter_count":
            sum(c.isalpha() for c in url),

        "special_char_count":
            len(
                re.findall(
                    r"[^a-zA-Z0-9]",
                    url
                )
            ),

        "has_https":
            int(parsed.scheme == "https"),

        "has_at_symbol":
            int("@" in url),

        "has_double_slash":
            int("//" in path),

        "is_ip_address":
            int(
                bool(
                    re.match(
                        r"^\d+\.\d+\.\d+\.\d+$",
                        domain
                    )
                )
            ),

        "percent_encoding_count":
            url.count("%"),

        "entropy":
            calculate_entropy(url)

    }

    return features


def tokenize_url(url):

    tokens = re.split(
        r"[/:.?=&_\-]+",
        url.lower()
    )

    tokens = [
        token
        for token in tokens
        if len(token) > 1
    ]

    return " ".join(tokens)