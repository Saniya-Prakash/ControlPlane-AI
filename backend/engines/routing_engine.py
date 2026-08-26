def estimate_complexity(prompt: str) -> str:
    """
    Estimate prompt complexity using simple deterministic rules.
    """

    words = prompt.split()
    word_count = len(words)

    complexity_keywords = [
        "analyze",
        "compare",
        "architecture",
        "design",
        "strategy",
        "optimize",
        "evaluate",
        "research",
        "algorithm",
        "financial",
        "security",
        "enterprise"
    ]

    prompt_lower = prompt.lower()

    keyword_count = sum(
        1 for keyword in complexity_keywords
        if keyword in prompt_lower
    )

    if word_count > 80 or keyword_count >= 3:
        return "HIGH"

    if word_count > 30 or keyword_count >= 1:
        return "MEDIUM"

    return "LOW"


def select_model(
    risk_score: int,
    complexity: str
) -> dict:
    """
    Select the appropriate model based on risk and complexity.
    """

    # High-risk requests need the strongest model.
    if risk_score >= 70:
        return {
            "model": "advanced-model",
            "tier": "HIGH_RELIABILITY",
            "reason": "High risk requires stronger reasoning and validation"
        }

    # Complex requests need a more capable model.
    if complexity == "HIGH":
        return {
            "model": "advanced-model",
            "tier": "HIGH_RELIABILITY",
            "reason": "High complexity request"
        }

    # Medium requests use the balanced model.
    if complexity == "MEDIUM" or risk_score >= 30:
        return {
            "model": "balanced-model",
            "tier": "BALANCED",
            "reason": "Moderate complexity or risk"
        }

    # Simple, low-risk requests use the cheaper model.
    return {
        "model": "fast-model",
        "tier": "COST_OPTIMIZED",
        "reason": "Low-risk, low-complexity request"
    }