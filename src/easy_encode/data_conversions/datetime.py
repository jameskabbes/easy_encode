import datetime


def datetime_to_float(x: datetime.datetime):
    return x.timestamp()


def datetime_to_str(x: datetime.datetime):
    return x.isoformat()


def datetime_from_number(x: float | int):
    return datetime.datetime.fromtimestamp(x)


def datetime_from_str(x: str):
    return datetime.datetime.fromisoformat(x)
