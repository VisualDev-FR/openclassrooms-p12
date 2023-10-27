import re


def email_is_valid(email: str):
    return re.fullmatch(r"\w+\.?\w+@\w+\.[a-z]+", email) is not None
