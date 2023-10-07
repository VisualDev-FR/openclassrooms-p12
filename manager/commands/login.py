from authentification.login import login
from authentification.token import retreive_token, clear_token


def execute(*args):
    email = args[0] if len(args) else input("email : ")
    password = input("password : ")

    logged_in_employee = login(email, password)

    if not logged_in_employee:
        print("Invalid credentials")

    print(f"Welcome {logged_in_employee.full_name} !")


if __name__ == "__main__":
    execute()
