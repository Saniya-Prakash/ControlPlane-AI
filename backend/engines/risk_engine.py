from detectors.injection_detector import detect_prompt_injection
from detectors.pii_detector import detect_pii
from detectors.safety_detector import detect_safety_risk


def calculate_overall_risk(
    injection_score: int,
    pii_score: int,
    safety_score: int
) -> int:

    score = (
        injection_score * 0.35
        + pii_score * 0.35
        + safety_score * 0.30
    )

    return round(score)


def get_risk_level(score: int) -> str:

    if score >= 80:
        return "CRITICAL"

    if score >= 60:
        return "HIGH"

    if score >= 30:
        return "MEDIUM"

    return "LOW"


def determine_decision(
    overall_score: int,
    injection_detected: bool,
    pii_detected: bool,
    safety_detected: bool
) -> str:

    # Critical security violation
    if injection_detected:
        return "BLOCK"

    # Sensitive information exposure
    if pii_detected:
        return "BLOCK"

    # High-risk safety content
    if safety_detected and overall_score >= 30:
        return "REVIEW"

    if overall_score >= 80:
        return "BLOCK"

    if overall_score >= 60:
        return "REVIEW"

    if overall_score >= 30:
        return "MONITOR"

    return "ALLOW"


def analyze_prompt(prompt: str) -> dict:

    injection = detect_prompt_injection(prompt)

    pii = detect_pii(prompt)

    safety = detect_safety_risk(prompt)

    overall_score = calculate_overall_risk(
        injection["risk_score"],
        pii["risk_score"],
        safety["risk_score"]
    )

    risk_level = get_risk_level(overall_score)

    decision = determine_decision(
        overall_score,
        injection["detected"],
        pii["detected"],
        safety["detected"]
    )

    return {
        "risk_score": overall_score,
        "risk_level": risk_level,

        "decision": decision,

        "risks": {
            "prompt_injection": injection,
            "privacy": pii,
            "safety": safety
        }
    }