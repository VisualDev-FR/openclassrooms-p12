import sys
from pwinput import pwinput
from authentification.login import login


if __name__ == "__main__":
    """
    Entry point for login feature.
    """

    args = sys.argv
    email = args[1] if len(args) > 1 else input("email : ")
    password = pwinput("password : ")

    logged_in_employee = login(email, password)

    if not logged_in_employee:
        print("Invalid credentials")

    print(f"Welcome {logged_in_employee.full_name} !")
