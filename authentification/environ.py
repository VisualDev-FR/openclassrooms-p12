from pathlib import Path
import os

DATABASE_PASSWORD = os.environ.get("EPICEVENTS_PW")
SECRET_KEY = os.environ.get("EPICEVENTS_SK")

if not DATABASE_PASSWORD:
    raise AttributeError("Environnement variable not set : EPICEVENTS_PW")


if not SECRET_KEY:
    raise AttributeError("Environnement variable not set : SECRET_KEY")


def get_epicevents_env():

    appdata = Path(os.environ.get("appdata"))

    path = Path(appdata, "epicevents")

    if not os.path.exists(path):
        os.mkdir(path)

    return path
