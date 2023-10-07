from sqlalchemy.orm import Session
import sqlalchemy
import typing

from authentification.token import decode_token, retreive_token
from models.employees import Employee, Department
from database.manager import engine


def login_required(function):
    """
    Decorator allowing to check if the current user is authenticated.\n

    Retreive the token stored on the user's disk, and try to decode it.
    If one of those two steps fails, the authentification check is rejected.
    """

    def wrapper(*args, **kwargs):
        token = retreive_token()

        if not decode_token(token):
            print("You must be authentified.")
            return None

        return function(*args, **kwargs)

    return wrapper


def __check_department(
    department: Department, function: typing.Callable, *args, **kwargs
) -> typing.Any:
    """
    Generic decorator wrapper, allowing to check if the authenticated user belongs to a given department.
    """
    REJECT_MESSAGE = f"You must be authentified as a {department.value} employee to access this function."

    token = retreive_token()
    decoded_token = decode_token(token)

    if not decoded_token:
        print(REJECT_MESSAGE)
        return None

    user_id = decoded_token["user_id"]

    session = Session(engine)
    request = sqlalchemy.select(Employee).where(Employee.id == user_id)
    employee = session.scalar(request)

    if not employee:
        print(REJECT_MESSAGE)
        return None

    if employee.department is not department:
        print(REJECT_MESSAGE)
        return None

    return function(*args, **kwargs)


def sales_user_required(function):
    """
    Decorator allowing to check if the authenticated user belongs to ``sales`` department.
    """

    def wrapper(*args, **kwargs):
        return __check_department(Department.SALES, function, *args, **kwargs)

    return wrapper


def accounting_user_required(function):
    """
    Decorator allowing to check if the authenticated user belongs to ``accounts`` department.
    """

    def wrapper(*args, **kwargs):
        return __check_department(Department.ACCOUNTING, function, *args, **kwargs)

    return wrapper


def support_user_required(function):
    """
    Decorator allowing to check if the authenticated user belongs to ``support`` department.
    """

    def wrapper(*args, **kwargs):
        return __check_department(Department.SUPPORT, function, *args, **kwargs)

    return wrapper
