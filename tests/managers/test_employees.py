import pytest
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError

from controller.managers import EmployeeManager
from models.employees import Employee, Department
from models.clients import Client
from models.contracts import Contract
from models.events import Event


def test_create_employee_from_accounting_user(database_mock, session, login_as_accounting):
    """
    check that an accounting employee are allowed to create a new employee
    """
    with database_mock, login_as_accounting:
        manager = EmployeeManager(session)
        manager.create(
            full_name="dummy employee",
            email="dummy.employee@epicevents.co",
            password="password",
            department=Department.ACCOUNTING,
        )

        created_employee = manager.get(Employee.full_name == "dummy employee")

        assert len(created_employee) == 1


def test_create_employee_from_unauthorized(database_mock, session: Session, login_as_sales, login_as_support):
    """
    check that sales or support employees are not allowed to create a new employee
    """

    manager = EmployeeManager(session)

    with database_mock, login_as_sales, pytest.raises(PermissionError) as raised_exception:
        manager.create(
            full_name="dummy employee",
            email="dummy.employee@epicevents.co",
            password="password",
            department=Department.ACCOUNTING,
        )

        assert raised_exception is not None

    with database_mock, login_as_support, pytest.raises(PermissionError) as raised_exception:
        manager.create(
            full_name="dummy employee",
            email="dummy.employee@epicevents.co",
            password="password",
            department=Department.ACCOUNTING,
        )

        assert raised_exception is not None

    request = sqlalchemy.select(Employee).where(
        Employee.full_name == "dummy employee")
    assert session.scalars(request).all() == []


def test_create_employee_with_invalid_datas(database_mock, session, login_as_accounting):
    manager = EmployeeManager(session)

    with database_mock, login_as_accounting:

        # invalid email
        with pytest.raises(ValueError):
            manager.create(
                full_name="Valid fullname",
                email="invalid_email",
                password="Valid password",
                department=Department.ACCOUNTING,
            )

        # invalid departement
        with pytest.raises(DataError):
            manager.create(
                full_name="Valid fullname",
                email="valid.email@example.co",
                password="Valid password",
                department="Invalid departement",
            )


def test_get_all_employees(database_mock, session, login_as_accounting, login_as_sales, login_as_support):
    """
    check thaht all employees can be accessed from all users
    """

    manager = EmployeeManager(session)

    with database_mock, login_as_accounting:
        assert len(manager.all()) == 10

    with database_mock, login_as_sales:
        assert len(manager.all()) == 10

    with database_mock, login_as_support:
        assert len(manager.all()) == 10


def test_get_employee(database_mock, session, login_as_accounting, login_as_sales, login_as_support):
    """
    check that employees can be searched from all users
    """

    manager = EmployeeManager(session)

    with database_mock, login_as_accounting:
        employee = manager.get(Employee.department == Department.SALES)[0]
        assert employee.email == "sales.employee@epicevents.co"

    with database_mock, login_as_sales:
        employee = manager.get(Employee.department == Department.SUPPORT)[0]
        assert employee.email == "support.employee@epicevents.co"

    with database_mock, login_as_support:
        employee = manager.get(Employee.department == Department.ACCOUNTING)[0]
        assert employee.email == "account.employee@epicevents.co"


def test_update_employee_from_accounting_user(database_mock, session, login_as_accounting):
    manager = EmployeeManager(session)

    with database_mock, login_as_accounting:
        manager.update(
            where_clause=Employee.email == "sales.employee@epicevents.co",
            full_name="updated_employee_fullname",
        )

        assert (
            manager.get(Employee.email ==
                        "sales.employee@epicevents.co")[0].full_name
            == "updated_employee_fullname"
        )


def test_update_employee_from_unauthorized(database_mock, session, login_as_sales, login_as_support):
    manager = EmployeeManager(session)

    def update_employee():
        manager.update(
            where_clause=Employee.email == "sales.employee@epicevents.co",
            full_name="updated_employee_fullname",
        )

    with database_mock, login_as_sales, pytest.raises(PermissionError):
        update_employee()

    with database_mock, login_as_support, pytest.raises(PermissionError):
        update_employee()


def test_update_employee_with_invalid_datas(database_mock, session, login_as_accounting):

    manager = EmployeeManager(session)

    with database_mock, login_as_accounting, pytest.raises(ValueError):
        manager.update(
            where_clause=Employee.id == 1,
            email="null",
        )


def test_delete_employee_from_unauthorized(database_mock, session, login_as_sales, login_as_support):

    manager = EmployeeManager(session)

    with database_mock, login_as_sales, pytest.raises(PermissionError):
        manager.delete(Employee.id == 1)

    with database_mock, login_as_support, pytest.raises(PermissionError):
        manager.delete(Employee.id == 1)


def test_delete_employee_from_accounting_user(database_mock, session: Session, login_as_accounting):

    manager = EmployeeManager(session)

    def count_objects(object: type) -> int:
        return len(session.scalars(sqlalchemy.select(object)).all())

    with database_mock, login_as_accounting:

        assert count_objects(Employee) == 10
        assert count_objects(Client) == 10
        assert count_objects(Contract) == 10
        assert count_objects(Event) == 10

        manager.delete(Employee.id == 1)

        assert count_objects(Employee) == 9
        assert count_objects(Client) == 7
        assert count_objects(Contract) == 7
        assert count_objects(Event) == 7
