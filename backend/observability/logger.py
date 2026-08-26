import json
import os
from datetime import datetime, timezone


LOG_FILE = "audit_logs.jsonl"


def log_event(event: dict):
    """
    Store one ControlPlane request as an append-only JSON event.
    """

    event["timestamp"] = datetime.now(
        timezone.utc
    ).isoformat()

    os.makedirs(
        os.path.dirname(LOG_FILE) or ".",
        exist_ok=True
    )

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(
                event,
                ensure_ascii=False
            ) + "\n"
        )