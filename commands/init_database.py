import json
from sqlalchemy.orm import Session
from pathlib import Path

from database import manager
from models.employees import Employee


def create_employees():
    """
    create employees in database, from ``employees.json`` datas.
    """

    employees_data = Path("data", "employees.json")

    with open(employees_data, "r") as reader:
        employees_data = json.loads(reader.read())

    session = Session(manager.engine)

    employees = []

    for data in employees_data:
        new_employee = Employee(
            full_name=data["full_name"],
            email=data["email"],
            department=data["departement"],
        )

        new_employee.set_password(password="password")

        employees.append(new_employee)

    session.add_all(employees)
    session.commit()


if __name__ == "__main__":
    """
    reset the database tables and insert some datas
    """
    manager.drop_tables()
    manager.create_tables()

    create_employees()
