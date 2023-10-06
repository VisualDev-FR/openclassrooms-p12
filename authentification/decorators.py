from authentification.token import decode_token, get_token
from database.manager import engine
from sqlalchemy.orm import Session


def login_required(function):
    def wrapper(*args, **kwargs):
        token = get_token()

        if not decode_token(token):
            print("You must be authentified.")
            return None

        return function(*args, **kwargs)

    return wrapper


def sales_user_required(function):
    reject_message = "You must be authentified as a sales employee."

    def wrapper(*args, **kwargs):
        token = get_token()

        decoded_token = decode_token(token)

        if not decoded_token:
            print(reject_message)
            return None
