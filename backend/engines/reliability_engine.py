from detectors.response_detector import (
    detect_response_pii,
    detect_response_safety
)

from engines.grounding_engine import evaluate_grounding


def calculate_reliability_score(
    pii_score: int,
    safety_score: int,
    grounding_score: int
) -> int:
    """
    Higher score means higher response risk.
    """

    grounding_risk = 100 - grounding_score

    score = (
        pii_score * 0.35
        + safety_score * 0.35
        + grounding_risk * 0.30
    )

    return round(score)


def evaluate_response(response: str) -> dict:

    pii = detect_response_pii(response)

    safety = detect_response_safety(response)

    grounding = evaluate_grounding(response)

    risk_score = calculate_reliability_score(
        pii["risk_score"],
        safety["risk_score"],
        grounding["grounding_score"]
    )

    if risk_score >= 80:

        level = "CRITICAL"

    elif risk_score >= 60:

        level = "HIGH"

    elif risk_score >= 30:

        level = "MEDIUM"

    else:

        level = "LOW"

    return {

        "reliability_risk_score": risk_score,

        "reliability_risk_level": level,

        "checks": {

            "privacy": pii,

            "safety": safety,

            "grounding": grounding
        }
    }