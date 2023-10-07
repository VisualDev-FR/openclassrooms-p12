from authentification.login import sign_up
from authentification.token import retreive_token, clear_token
from authentification.environ import DATABASE_PASSWORD


def execute(*args):
    """
    Entry point for registration functionality.\n
    Asks the user for the database password to access this method, then collects
    all the information required to create a new user in the database and log him in.
    """

    password = input("You need the database password to access this method.\npassword : ")

    if password != DATABASE_PASSWORD:
        print("Invalid password.")
        return

    full_name = input("full name : ")
    email = input("email : ")
    password = input("password : ")

    sign_up(
        full_name=full_name,
        email=email,
        password=password,
    )


if __name__ == "__main__":
    execute()
