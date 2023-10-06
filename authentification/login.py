from sqlalchemy.orm import Session
import sqlalchemy

from models.employees import Employee
from database.manager import create_engine
from authentification.token import create_token, set_token, clear_token


def login(email: str, password: str) -> bool:
    engine = create_engine()

    session = Session(engine)
    request = sqlalchemy.select(Employee)

    employee = session.scalar(request)

    if not employee:
        return False

    password_is_valid = employee.check_password(password)

    if password_is_valid:
        token = create_token(user_id=employee.id)
        set_token(token)
        return True

    else:
        clear_token()
        return False


def logout():
    clear_token()
