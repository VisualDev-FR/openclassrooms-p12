import re


def email_is_valid(email: str):
    return re.fullmatch(r"\w+\.?\w+@\w+\.[a-z]+", email) is not None


def drop_none_from_dict(data: dict) -> dict:
    return dict([(key, value) for key, value in data.items() if value is not None])
