import sqlalchemy
from typing import List

from controller.authentification import decode_token, retreive_token
from models.employees import Employee, Department
from controller import database as db


def resolve_permission(roles: List[Department], function, *args, **kwargs):
    REJECT_MESSAGE = f"Permission denied. Please login as [{' | '.join(role.name for role in roles)}]"

    token = retreive_token()
    token_payload = decode_token(token)

    if not token_payload:
        raise PermissionError(REJECT_MESSAGE)

    user_id = token_payload["user_id"]

    with db.create_session() as session:
        request = sqlalchemy.select(Employee).where(Employee.id == user_id)
        employee = session.scalar(request)

    if not employee:
        raise PermissionError(REJECT_MESSAGE)

    if employee.department not in roles:
        raise PermissionError(REJECT_MESSAGE)

    return function(*args, **kwargs)


def permission_required(roles: List[Department]):
    """
    decorator allowing to checks if the authenticated user belongs to a given department.

    Args:
    * ``roles``: A list of ``Departement`` objects which are authorized to access the function.

    Raises:
    * ``PermissionError``
    """

    def decorator(function):
        def wrapper(*args, **kwargs):
            return resolve_permission(roles, function, *args, **kwargs)

        return wrapper

    return decorator
