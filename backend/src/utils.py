import datetime


def aware_utcnow() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)
