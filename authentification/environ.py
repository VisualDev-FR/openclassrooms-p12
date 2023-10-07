"""
This module is an helper to retreive all necessaries environnement variables.\n

it performs a check during the import, to crash the application if needed variable environnement are not set.
"""

from pathlib import Path
import os

DATABASE_USERNAME = os.environ.get("EPICEVENTS_USER")
DATABASE_PASSWORD = os.environ.get("EPICEVENTS_PW")
SECRET_KEY = os.environ.get("EPICEVENTS_SK")

__ENV_NOT_SET_MESSAGE = "Environnement variable not set : {name}"


if not DATABASE_USERNAME:
    raise AttributeError(__ENV_NOT_SET_MESSAGE.format(name="EPICEVENTS_USER"))

if not DATABASE_PASSWORD:
    raise AttributeError(__ENV_NOT_SET_MESSAGE.format(name="EPICEVENTS_PW"))

if not SECRET_KEY:
    raise AttributeError(__ENV_NOT_SET_MESSAGE.format(name="SECRET_KEY"))


def get_epicevents_path() -> Path:
    """
    return the path of the epicevents directory on the user's disk.\n
    if not exists, creates it.
    """
    appdata_path = Path(os.environ.get("appdata"))
    epicevent_path = Path(appdata_path, "epicevents")

    if not epicevent_path.exists():
        os.mkdir(epicevent_path)

    return epicevent_path
