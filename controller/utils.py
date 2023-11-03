import re


def email_is_valid(email: str):
    return re.fullmatch(r"\w+\.?\w+@\w+\.[a-z]+", email) is not None


def drop_none_from_dict(data: dict) -> dict:
    """
    Removes entries from a dictionary where the values are ``None``

    Args:
    * ``data``: the dictionary to remove ``None`` values from.

    Returns:\n
    A copy of the given dictionary, without None values
    """
    return dict([(key, value) for key, value in data.items() if value is not None])
