from authentification.login import login
from authentification.token import get_token, clear_token


def execute(*args):

    email = args[0] if len(args) else input("email : ")
    password = input("password : ")

    login(email, password)


if __name__ == "__main__":
    execute()

    print(get_token())
