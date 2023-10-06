from authentification.token import decode_token, get_token


def login_required(function):
    def wrapper(*args, **kwargs):
        token = get_token()

        if not decode_token(token):
            print("You must be authentified.")
            return None

        return function(*args, **kwargs)

    return wrapper
