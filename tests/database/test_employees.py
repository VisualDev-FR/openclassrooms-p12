from database.employees import EmployeeManager
from models.employees import Employee, Department
from tests.conftest import login_as_accounting, login_as_sales, login_as_support


def test_create_employee_from_accounting_user(session):
    """
    check that an accounting employee is allowed to create a new employee
    """
    with login_as_accounting(session):
        manager = EmployeeManager(session)
        manager.create(
            full_name="dummy employee",
            email="dummy.employee@epicevents.co",
            password="password",
            department=Department.ACCOUNTING,
        )

        created_employee = manager.get(Employee.full_name == "dummy employee")

        assert len(created_employee) == 1


def test_create_employee_from_unothorized(session):
    """
    check that sales or support employees are not allowed to create a new employee
    """
    with login_as_sales(session):
        manager = EmployeeManager(session)
        manager.create(
            full_name="dummy employee",
            email="dummy.employee@epicevents.co",
            password="password",
            department=Department.ACCOUNTING,
        )

        created_employee = manager.get(Employee.full_name == "dummy employee")

        assert len(created_employee) == 0

    with login_as_support(session):
        manager = EmployeeManager(session)
        manager.create(
            full_name="dummy employee",
            email="dummy.employee@epicevents.co",
            password="password",
            department=Department.ACCOUNTING,
        )

        created_employee = manager.get(Employee.full_name == "dummy employee")

        assert len(created_employee) == 0
