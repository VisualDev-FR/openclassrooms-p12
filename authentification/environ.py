import os

DATABASE_PASSWORD = os.environ.get("EPICEVENTS_PW")
SECRET_KEY = os.environ.get("EPICEVENTS_SK")

if not DATABASE_PASSWORD:
    raise AttributeError("Environnement variable not set : EPICEVENTS_PW")


if not SECRET_KEY:
    raise AttributeError("Environnement variable not set : SECRET_KEY")


def set_token(token: str):
    os.environ["EPICEVENTS_TOKEN"] = token


def get_token() -> str:
    return os.environ.get("EPICEVENTS_TOKEN")


def clear_token():
    try:
        del os.environ["EPICEVENTS_TOKEN"]
    except KeyError:
        pass
