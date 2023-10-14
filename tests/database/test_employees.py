import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from database.employees import EmployeeManager
from models.employees import Employee, Department
from tests.conftest import login_as_accounting, login_as_sales, login_as_support


def test_create_employee_from_accounting_user(session):
    """
    check that an accounting employee are allowed to create a new employee
    """
    with login_as_accounting():
        manager = EmployeeManager(session)
        manager.create(
            full_name="dummy employee",
            email="dummy.employee@epicevents.co",
            password="password",
            department=Department.ACCOUNTING,
        )

        created_employee = manager.get(Employee.full_name == "dummy employee")

        assert len(created_employee) == 1


def test_create_employee_from_unauthorized(session: Session):
    """
    check that sales or support employees are not allowed to create a new employee
    """

    manager = EmployeeManager(session)

    with login_as_sales(), pytest.raises(PermissionError) as raised_exception:
        manager.create(
            full_name="dummy employee",
            email="dummy.employee@epicevents.co",
            password="password",
            department=Department.ACCOUNTING,
        )

        assert raised_exception is not None

    with login_as_support(), pytest.raises(PermissionError) as raised_exception:
        manager.create(
            full_name="dummy employee",
            email="dummy.employee@epicevents.co",
            password="password",
            department=Department.ACCOUNTING,
        )

        assert raised_exception is not None

    request = sqlalchemy.select(Employee).where(Employee.full_name == "dummy employee")
    assert session.scalars(request).all() == []


def test_get_all_employees(session):
    """
    check thaht all employees can be accessed from all users
    """

    manager = EmployeeManager(session)

    with login_as_accounting():
        assert len(manager.all()) == 3

    with login_as_sales():
        assert len(manager.all()) == 3

    with login_as_support():
        assert len(manager.all()) == 3


def test_get_employee(session):
    """
    check that employees can be searched from all users
    """

    manager = EmployeeManager(session)

    with login_as_accounting():
        employee = manager.get(Employee.department == Department.SALES)[0]
        assert employee.email == "sales.employee@epicevents.co"

    with login_as_sales():
        employee = manager.get(Employee.department == Department.SUPPORT)[0]
        assert employee.email == "support.employee@epicevents.co"

    with login_as_support():
        employee = manager.get(Employee.department == Department.ACCOUNTING)[0]
        assert employee.email == "account.employee@epicevents.co"


def test_update_employee_from_accounting_user(session):

    manager = EmployeeManager(session)

    with login_as_accounting():

        manager.update(
            where_clause=Employee.email == "sales.employee@epicevents.co",
            full_name="updated_employee_fullname"
        )

        assert manager.get(Employee.email == "sales.employee@epicevents.co")[0].full_name == "updated_employee_fullname"


def test_delete_employee_from_accounting_user(session):

    manager = EmployeeManager(session)

    with login_as_accounting():

        employee = manager.create(
            full_name="employee to be deleted",
            email="to.be.deleted@epicevents.co",
            password="password",
            department=Department.ACCOUNTING
        )

        assert manager.get(Employee.email == employee.email)[0] is not None

        manager.delete(Employee.email == employee.email)

        assert manager.get(Employee.email == employee.email) == []
