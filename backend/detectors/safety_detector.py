import re


SAFETY_PATTERNS = {
    "violence": [
        r"\bhow to attack\b",
        r"\bhow to hurt\b",
        r"\bhow to kill\b",
    ],

    "illegal_activity": [
        r"\bhow to hack\b",
        r"\bsteal someone's password\b",
        r"\bmake a bomb\b",
    ],

    "self_harm": [
        r"\bhow to hurt myself\b",
        r"\bhow to kill myself\b",
    ]
}


def detect_safety_risk(text: str) -> dict:
    """
    Detect potentially unsafe categories in the prompt.
    """

    text_lower = text.lower()

    detected_categories = []

    for category, patterns in SAFETY_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, text_lower):
                detected_categories.append(category)
                break

    if not detected_categories:
        return {
            "detected": False,
            "risk_score": 0,
            "level": "LOW",
            "categories": []
        }

    score = min(100, 60 + len(detected_categories) * 20)

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
        "categories": detected_categories
    }