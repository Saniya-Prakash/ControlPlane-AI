import re


PII_PATTERNS = {
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

    "phone": r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",

    "credit_card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",

    "pan": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",

    "aadhaar_like": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"
}


def detect_pii(text: str) -> dict:
    """
    Detect common forms of personally identifiable information.
    """

    detected = {}

    for pii_type, pattern in PII_PATTERNS.items():

        matches = re.findall(pattern, text)

        if matches:
            detected[pii_type] = len(matches)

    if not detected:
        return {
            "detected": False,
            "risk_score": 0,
            "level": "LOW",
            "types": {}
        }

    score = min(100, 40 + len(detected) * 20)

    if score >= 80:
        level = "CRITICAL"
    elif score >= 60:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "detected": True,
        "risk_score": score,
        "level": level,
        "types": detected
    }