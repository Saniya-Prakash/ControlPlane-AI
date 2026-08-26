import re

from knowledge.knowledge_base import KNOWLEDGE_BASE


def normalize_text(text: str) -> str:
    """
    Normalize text for simple semantic-style comparison.
    """

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def calculate_word_overlap(
    claim: str,
    fact: str
) -> float:

    claim_words = set(
        normalize_text(claim).split()
    )

    fact_words = set(
        normalize_text(fact).split()
    )

    if not claim_words:
        return 0.0

    common_words = claim_words.intersection(
        fact_words
    )

    return len(common_words) / len(claim_words)


def find_relevant_facts(
    response: str
) -> list:

    response_normalized = normalize_text(response)

    relevant_facts = []

    for category in KNOWLEDGE_BASE.values():

        for fact in category["facts"]:

            fact_words = set(
                normalize_text(fact).split()
            )

            response_words = set(
                response_normalized.split()
            )

            overlap = len(
                fact_words.intersection(response_words)
            )

            if overlap >= 3:

                relevant_facts.append({
                    "fact": fact,
                    "overlap": overlap
                })

    return relevant_facts


def evaluate_grounding(response: str) -> dict:

    relevant_facts = find_relevant_facts(response)

    if not relevant_facts:

        return {
            "grounded": False,
            "grounding_score": 0,
            "level": "HIGH",
            "supported_facts": [],
            "message": "No supporting evidence found in trusted knowledge base."
        }

    best_score = 0
    supported_facts = []

    for item in relevant_facts:

        score = calculate_word_overlap(
            response,
            item["fact"]
        )

        if score > best_score:
            best_score = score

        if score >= 0.25:

            supported_facts.append(
                item["fact"]
            )

    grounding_score = round(
        best_score * 100
    )

    if grounding_score >= 60:

        level = "LOW"
        grounded = True

    elif grounding_score >= 30:

        level = "MEDIUM"
        grounded = False

    else:

        level = "HIGH"
        grounded = False

    return {
        "grounded": grounded,
        "grounding_score": grounding_score,
        "level": level,
        "supported_facts": supported_facts,
        "message": (
            "Response contains information supported "
            "by the trusted knowledge base."
            if grounded
            else
            "Response has insufficient supporting evidence."
        )
    }