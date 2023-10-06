import datetime
import jwt
from authentification.environ import clear_token
from authentification.environ import (
    SECRET_KEY,
)

__JWT_ALGORITHM = "HS256"
__JWT_EXPIRATION_TIME = datetime.timedelta(hours=1)


def create_token(user_id: int):
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
