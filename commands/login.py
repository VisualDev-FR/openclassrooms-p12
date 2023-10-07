import sys
from authentification.login import login


if __name__ == "__main__":
    args = sys.argv
    email = args[0] if len(args) else input("email : ")
    password = input("password : ")

    logged_in_employee = login(email, password)

    if not logged_in_employee:
        print("Invalid credentials")

    print(f"Welcome {logged_in_employee.full_name} !")
