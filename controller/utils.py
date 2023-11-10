import re


def validate_email(email: str):
    """
    Validates an email address format.

    Args:
    * ``email``: the email to validate

    Returns:
    * A string containing the given email

    Raises:
    * ``ValueError`` if the email is not valid
    """
    if not re.fullmatch(r"\w+\.?\w+@\w+\.[a-z]+", email):
        raise ValueError(f"Invalid email: {email}")

    return email


def drop_dict_none_values(data: dict) -> dict:
    """
    Removes entries from a dictionary where the values are ``None``

    Args:
    * ``data``: the dictionary to remove ``None`` values from.

    Returns:\n
    A copy of the given dictionary, without None values
    """
    return dict([(key, value) for key, value in data.items() if value is not None])
