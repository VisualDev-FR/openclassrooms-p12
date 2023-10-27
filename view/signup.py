from pwinput import pwinput

from authentification.login import perform_sign_up
from authentification.environ import DATABASE_PASSWORD
from view import cli


@cli.command
def signup():
    """
    Create an employee account. (You need the database password to perform this action)
    """

    password = pwinput(
        "You need the database password to access this method.\npassword : "
    )

    if password != DATABASE_PASSWORD:
        print("Invalid password.")
        exit()

    full_name = input("full name : ")
    email = input("email : ")
    password = pwinput("password : ")

    perform_sign_up(
        full_name=full_name,
        email=email,
        password=password,
    )
