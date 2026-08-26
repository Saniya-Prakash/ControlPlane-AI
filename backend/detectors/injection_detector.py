import re


INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?prior\s+instructions",
    r"disregard\s+(all\s+)?previous\s+instructions",
    r"forget\s+(all\s+)?previous\s+instructions",
    r"reveal\s+(the\s+)?system\s+prompt",
    r"show\s+(me\s+)?(the\s+)?system\s+prompt",
    r"reveal\s+(your\s+)?system\s+instructions",
    r"show\s+(me\s+)?your\s+instructions",
    r"bypass\s+(the\s+)?safety",
    r"bypass\s+(all\s+)?restrictions",
    r"you\s+are\s+now\s+unrestricted",
    r"jailbreak",
]


def detect_prompt_injection(prompt: str) -> dict:
    """
    Detect common prompt injection patterns.

    Returns:
        risk_score: 0-100
        level: LOW/MEDIUM/HIGH/CRITICAL
        detected: boolean
        matches: detected patterns
    """

    prompt_lower = prompt.lower()

    matches = []

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, prompt_lower):
            matches.append(pattern)

    if not matches:
        return {
            "detected": False,
            "risk_score": 0,
            "level": "LOW",
            "matches": []
        }

    score = min(100, 50 + len(matches) * 20)

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
        "matches": matches
    }