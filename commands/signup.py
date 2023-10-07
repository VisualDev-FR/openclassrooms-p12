from pwinput import pwinput
from authentification.login import sign_up
from authentification.environ import DATABASE_PASSWORD


if __name__ == "__main__":
    """
    Entry point for registration functionality.

    Asks the user for the database password to access this method, then collects
    all the information required to create a new user in the database and log him in.
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

    sign_up(
        full_name=full_name,
        email=email,
        password=password,
    )
