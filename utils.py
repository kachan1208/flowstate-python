from datetime import datetime, timezone


def time_rfc3339micro() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")
