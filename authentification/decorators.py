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
            raise PermissionError("Please login and retry.")

        return function(*args, **kwargs)

    return wrapper


def permission_required(roles: typing.List[Department]):
    """
    checks if the authenticated user belongs to a given department.

    Several departments can be specified, in order to give permission to multiple roles.

    returns ``None`` if the user is not authenticated or if he does not belong to the required departement.
    """

    def decorator(function):
        def wrapper(*args, **kwargs):
            REJECT_MESSAGE = "Permission denied."

            token = retreive_token()
            token_payload = decode_token(token)

            if not token_payload:
                raise PermissionError(REJECT_MESSAGE)

            user_id = token_payload["user_id"]

            session = Session(engine)
            request = sqlalchemy.select(Employee).where(Employee.id == user_id)
            employee = session.scalar(request)

            if not employee:
                raise PermissionError(REJECT_MESSAGE)

            if employee.department not in roles:
                print(employee.id, employee.department, roles)
                raise PermissionError(REJECT_MESSAGE)

            return function(*args, **kwargs)

        return wrapper

    return decorator
