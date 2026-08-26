import re


def rewrite_response(
    original_response: str,
    reliability_result: dict
) -> str:

    checks = reliability_result["checks"]

    privacy_issue = checks["privacy"]["detected"]

    safety_issue = checks["safety"]["detected"]

    grounding = checks["grounding"]

    grounding_issue = not grounding["grounded"]

    rewritten = original_response

    # ==========================================
    # PRIVACY REWRITE
    # ==========================================

    if privacy_issue:

        rewritten = re.sub(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            "[REDACTED EMAIL]",
            rewritten
        )

        rewritten = re.sub(
            r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",
            "[REDACTED PHONE]",
            rewritten
        )

        rewritten = re.sub(
            r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
            "[REDACTED CARD]",
            rewritten
        )

        rewritten = re.sub(
            r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
            "[REDACTED ID]",
            rewritten
        )

    # ==========================================
    # SAFETY REWRITE
    # ==========================================

    if safety_issue:

        rewritten = (
            "I can't provide instructions that could enable "
            "harmful or unauthorized activity. I can instead "
            "help with safe, defensive, or educational "
            "information about the topic."
        )

    # ==========================================
    # GROUNDING REWRITE
    # ==========================================

    if grounding_issue and not safety_issue:

        supported_facts = grounding.get(
            "supported_facts",
            []
        )

        if supported_facts:

            rewritten = (
                "The response could not be fully verified "
                "against the trusted knowledge base. "
                "Here is the information that can be "
                "supported with available evidence:\n\n"
            )

            rewritten += "\n".join(
                f"• {fact}"
                for fact in supported_facts
            )

        else:

            rewritten = (
                "I could not verify the generated response "
                "against the available trusted knowledge "
                "base. The information should be verified "
                "before relying on it."
            )

    return rewritten