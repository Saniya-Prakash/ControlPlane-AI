import json
import os


LOG_FILE = "audit_logs.jsonl"


def load_events():

    if not os.path.exists(LOG_FILE):
        return []

    events = []

    with open(
        LOG_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            try:

                events.append(
                    json.loads(line)
                )

            except json.JSONDecodeError:

                continue

    return events


def get_metrics():

    events = load_events()

    if not events:

        return {
            "total_requests": 0,
            "allowed": 0,
            "rewritten": 0,
            "blocked": 0,
            "average_risk_score": 0,
            "average_reliability_risk": 0,
            "model_usage": {},
            "risk_categories": {}
        }

    allowed = 0
    rewritten = 0
    blocked = 0

    total_risk = 0
    total_reliability = 0

    model_usage = {}
    risk_categories = {}

    for event in events:

        decision = event.get(
            "final_decision"
        )

        if decision == "ALLOW":

            allowed += 1

        elif decision == "REWRITE":

            rewritten += 1

        elif decision == "BLOCK":

            blocked += 1

        total_risk += event.get(
            "risk_score",
            0
        )

        total_reliability += event.get(
            "reliability_risk_score",
            0
        )

        model = event.get("model")

        if model:

            model_usage[model] = (
                model_usage.get(model, 0) + 1
            )

        categories = event.get(
            "risk_categories",
            []
        )

        for category in categories:

            risk_categories[category] = (
                risk_categories.get(category, 0) + 1
            )

    total_requests = len(events)

    return {

        "total_requests": total_requests,

        "allowed": allowed,

        "rewritten": rewritten,

        "blocked": blocked,

        "average_risk_score": round(
            total_risk / total_requests,
            2
        ),

        "average_reliability_risk": round(
            total_reliability / total_requests,
            2
        ),

        "model_usage": model_usage,

        "risk_categories": risk_categories
    }