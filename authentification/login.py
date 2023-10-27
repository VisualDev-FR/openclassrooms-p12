from sqlalchemy.orm import Session
import sqlalchemy

from models.employees import Employee, Department
from database.manager import engine
from authentification.token import create_token, store_token, clear_token


def perform_login(email: str, password: str) -> Employee:
    """
    Create a json-web-token containing the user id, and stores it on the user's disk.

    Later, the application will check this stored token to determine whether the user is authenticated or not.

    returns the retreived ``Employee`` objet if the login was sucessfull, else returns ``None``.
    """
    session = Session(engine)
    request = sqlalchemy.select(Employee).where(Employee.email == email)

    employee = session.scalar(request)

    if not employee:
        return None

    password_is_valid = employee.check_password(password)

    if password_is_valid:
        token = create_token(user_id=employee.id)
        store_token(token)
        return employee

    else:
        clear_token()
        return None


def perform_sign_up(full_name: str, email: str, password: str):
    """
    Create a new user in the database without be logged in, then loggin the created user.\n
    As only accounting employees are allowed to create users, the created user will be assigned to accounting department.
    """
    with Session(engine) as session:
        new_employee = Employee(
            full_name=full_name,
            email=email,
            department=Department.ACCOUNTING,
        )

        new_employee.set_password(password)

        session.add(new_employee)
        session.commit()

    perform_login(email, password)


def perform_logout() -> bool:
    return clear_token()
