from pathlib import Path
from authentification.environ import get_epicevents_path
import datetime
import os

import jwt

from authentification.environ import (
    SECRET_KEY,
)

__JWT_ALGORITHM = "HS256"
__JWT_EXPIRATION_TIME = datetime.timedelta(hours=1)


def __get_token_path() -> Path:
    """
    retreive the file where the token is stored
    """
    return Path(get_epicevents_path(), "token.txt")


def store_token(token: str):
    """
    store a given token on the user's disk
    """
    path = __get_token_path()

    with open(path, "w") as writer:
        writer.write(token)


def retreive_token() -> str:
    """
    retreive the token stored on the user's disk
    """
    path = __get_token_path()

    if not path.exists():
        return None

    with open(path, "r") as reader:
        return reader.read()


def clear_token():
    """
    remove the token stored on the user's disk
    """
    path = __get_token_path()

    if path.exists():
        os.remove(path)


def create_token(user_id: int) -> str:
    """
    Return a Json-web-token for a given user, encrypted with
    a secret key defined in `authentification.environ.SECRET_KEY`
    """

    expiration_time = datetime.datetime.utcnow() + __JWT_EXPIRATION_TIME

    return jwt.encode(
        payload={
            "exp": expiration_time,
            "user_id": user_id,
        },
        key=SECRET_KEY,
        algorithm=__JWT_ALGORITHM,
    )


def decode_token(token: str) -> dict:
    """
    decode a json-web-token and returns the contained payload.\n
    return ``None`` if the token has expirated.
    """
    try:
        return jwt.decode(jwt=token, key=SECRET_KEY, algorithms=__JWT_ALGORITHM)

    except Exception:
        # token is expired or is not valid
        clear_token()
        return None
