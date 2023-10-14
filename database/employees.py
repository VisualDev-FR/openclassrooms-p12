import typing
from sqlalchemy.orm import Session

from authentification.decorators import login_required, permission_required
from models.employees import Employee, Department
from database.manager import Manager, engine


class EmployeeManager(Manager):
    """
    Manage the access to ``Employee`` table.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Employee)

    @login_required
    def get(self, *args, **kwargs) -> typing.List[Employee]:
        return super().get(*args, **kwargs)

    @login_required
    def all(self) -> typing.List[Employee]:
        return super().all()

    @permission_required(roles=[Department.ACCOUNTING])
    def create(self, full_name: str, email: str, password: str, department: Department):
        new_employee = Employee(
            full_name=full_name,
            email=email,
            department=department,
        )

        new_employee.set_password(password)

        return super().create(new_employee)

    @permission_required(roles=[Department.ACCOUNTING])
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    @permission_required(roles=[Department.ACCOUNTING])
    def delete(*args, **kwargs):
        return super().delete(**kwargs)
