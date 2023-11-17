import re
import tabulate as tabulator
from typing import List, Any


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


def validate_phone(phone):
    """
    Validates an phone number format.

    Args:
    * ``phone``: the phone number to validate

    Returns:
    * The phone number given in parameters

    Raises:
    * ``ValueError`` if the phone number is not valid
    """
    cleaned_phone = re.sub(r'\D', '', phone)

    pattern = re.compile(r'^\+?\d{1,3}?\d{9,15}$')

    if pattern.match(cleaned_phone):
        return phone
    else:
        raise ValueError(f"Invalid phone : {phone}")


def drop_dict_none_values(data: dict) -> dict:
    """
    Removes entries from a dictionary where the values are ``None``

    Args:
    * ``data``: the dictionary to remove ``None`` values from.

    Returns:\n
    A copy of the given dictionary, without None values
    """
    return dict([(key, value) for key, value in data.items() if value is not None])


def tabulate(objects: List[Any], headers: List[str]) -> str:
    """
    Prettify a list of objects to a tabulated view.

    Args:
    * ``objects``: a list of objects to display, the objects must implement the method ``to_list()``
    * ``headers``: a list of strings containing the headers of the tabulated view

    Returns:
    A string representing the table of the given datas

    """
    return tabulator.tabulate(
        tabular_data=[obj.to_list() for obj in objects],
        headers=headers
    )
