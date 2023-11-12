from controller import database as db
from models.employees import Employee, Department
import sqlalchemy
from sqlalchemy.orm import Session
from pathlib import Path
import datetime
import os
import jwt

from controller.environ import get_epicevents_path, SECRET_KEY

__JWT_ALGORITHM = "HS256"
__JWT_EXPIRATION_TIME = datetime.timedelta(hours=1)


def __get_token_path() -> Path:
    """
    retreive the file where the token is stored
    """
    return Path(get_epicevents_path(), "token.txt")


def store_token(token: str):
    """
    store a given token on the user's disk
    """
    path = __get_token_path()

    with open(path, "w") as writer:
        writer.write(token)


def retreive_token() -> str:
    """
    retreive the authentification json-web-token stored on the user's disk.

    Return None if no token exists.
    """
    path = __get_token_path()

    if not path.exists():
        return None

    with open(path, "r") as reader:
        return reader.read()


def clear_token() -> bool:
    """
    remove the token stored on the user's disk

    Returns:
    * `True` if the token was sucessfully deleted
    * `False` if no token exists
    """
    path = __get_token_path()

    if path.exists():
        os.remove(path)
        return True

    return False


def create_token(user_id: int) -> str:
    """
    Return a Json-web-token for a given user, encrypted with
    a secret key defined in `authentification.environ.SECRET_KEY`
    """

    expiration_time = datetime.datetime.utcnow() + __JWT_EXPIRATION_TIME

    return jwt.encode(
        payload={
            "exp": expiration_time,
            "user_id": user_id,
        },
        key=SECRET_KEY,
        algorithm=__JWT_ALGORITHM,
    )


def decode_token(token: str) -> dict:
    """
    decode a json-web-token and returns the contained payload.\n
    return ``None`` if the token has expirated or doesn't exist on the user's disk.
    """
    try:
        return jwt.decode(jwt=token, key=SECRET_KEY, algorithms=__JWT_ALGORITHM)

    except Exception:
        # token is expired or is not valid
        clear_token()
        return None


def get_authenticated_user_id() -> int:
    stored_token = retreive_token()

    if not stored_token:
        return None

    token_payload = decode_token(stored_token)

    if token_payload is None:
        return None

    return token_payload["user_id"]


def retreive_authenticated_user(session: Session) -> Employee:
    user_id = get_authenticated_user_id()

    return session.scalar(
        sqlalchemy.select(Employee)
        .where(Employee.id == user_id)
    )


def perform_login(email: str, password: str) -> Employee:
    """
    Create a json-web-token containing the user id, and stores it on the user's disk.

    Later, the application will check this stored token to determine whether the user is authenticated or not.

    returns the retreived ``Employee`` objet if the login was sucessfull, else returns ``None``.
    """

    with db.create_session() as session:
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
    with db.create_session() as session:
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
