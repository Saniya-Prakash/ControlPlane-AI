import re


def detect_response_pii(response: str) -> dict:
    """
    Detect sensitive information accidentally present
    in an AI-generated response.
    """

    patterns = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

        "phone": r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",

        "credit_card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",

        "pan": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
    }

    detected = {}

    for pii_type, pattern in patterns.items():

        matches = re.findall(pattern, response)

        if matches:
            detected[pii_type] = len(matches)

    if not detected:
        return {
            "detected": False,
            "risk_score": 0,
            "level": "LOW",
            "types": {}
        }

    score = min(100, 50 + len(detected) * 15)

    if score >= 80:
        level = "CRITICAL"
    elif score >= 60:
        level = "HIGH"
    else:
        level = "MEDIUM"

    return {
        "detected": True,
        "risk_score": score,
        "level": level,
        "types": detected
    }


def detect_response_safety(response: str) -> dict:
    """
    Detect potentially unsafe instructions in generated responses.
    """

    unsafe_patterns = [
        r"step[- ]by[- ]step.*hack",
        r"how to hack",
        r"how to make a bomb",
        r"how to kill",
        r"steal.*password",
        r"bypass.*security",
        r"bypass.*authentication"
    ]

    matches = []

    response_lower = response.lower()

    for pattern in unsafe_patterns:

        if re.search(pattern, response_lower):
            matches.append(pattern)

    if not matches:

        return {
            "detected": False,
            "risk_score": 0,
            "level": "LOW",
            "matches": []
        }

    score = min(100, 70 + len(matches) * 15)

    return {
        "detected": True,
        "risk_score": score,
        "level": "CRITICAL",
        "matches": matches
    }