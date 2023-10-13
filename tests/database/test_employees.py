from database.employees import EmployeeManager
from models.employees import Employee, Department


def test_create_employee(session):

    manager = EmployeeManager(session)
    manager.create(
        full_name="dummy employee",
        email="dummy.employee@epicevents.co",
        password="password",
        department=Department.ACCOUNTING,
    )

    created_employee = manager.all()

    assert len(created_employee) == 4
