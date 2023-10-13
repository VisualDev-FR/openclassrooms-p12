import sqlalchemy
import typing
from sqlalchemy.orm import Session

from database.manager import Manager, engine
from models.employees import Employee, Department
from authentification.decorators import login_required, accounting_user_required


class EmployeeManager(Manager):
    """
    Manage the access to ``Employee`` table.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Employee)

    @login_required
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    @login_required
    def all(self) -> typing.List[Employee]:
        return super().all()

    @accounting_user_required
    def create(self, full_name: str, email: str, password: str, department: Department):
        new_employee = Employee(
            full_name=full_name,
            email=email,
            department=department,
        )

        new_employee.set_password(password)

        self._session.add(new_employee)
        self._session.commit()

    @accounting_user_required
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    @accounting_user_required
    def delete(*args, **kwargs):
        return super().delete(**kwargs)
