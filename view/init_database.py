import json
import datetime
from sqlalchemy.orm import Session
from pathlib import Path
from pwinput import pwinput

from view import cli
from database import manager
from models.employees import Employee
from models.clients import Client
from models.contracts import Contract
from models.events import Event
from authentification.environ import DATABASE_PASSWORD


def create_employees():
    """
    create employees in database, from ``data/employees.json``.
    """

    print("create employees...")

    data_path = Path("data", "employees.json")

    with open(data_path, "rb") as reader:
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


def create_clients():
    """
    create clients in database, from ``data/clients.json``.
    """

    print("create clients...")

    data_path = Path("data", "clients.json")

    with open(data_path, "rb") as reader:
        clients_data = json.loads(reader.read())

    session = Session(manager.engine)

    clients = [
        Client(
            full_name=data["full_name"],
            email=data["email"],
            phone=data["phone"],
            enterprise=data["enterprise"],
            sales_contact_id=data["sales_contact_id"],
        )
        for data in clients_data
    ]

    session.add_all(clients)
    session.commit()


def create_contracts():
    """
    create contracts in database, from ``data/contracts.json``.
    """

    print("create contracts...")

    data_path = Path("data", "contracts.json")

    with open(data_path, "rb") as reader:
        contracts_data = json.loads(reader.read())

    session = Session(manager.engine)

    contracts = [
        Contract(
            total_amount=data["total_amount"],
            to_be_paid=data["to_be_paid"],
            is_signed=data["is_signed"],
            client_id=data["client_id"],
            account_contact_id=data["account_contact_id"],
        )
        for data in contracts_data
    ]

    session.add_all(contracts)
    session.commit()


def create_events():
    """
    create events in database, from ``data/events.json``.
    """

    print("create events...")

    data_path = Path("data", "events.json")

    with open(data_path, "rb") as reader:
        events_data = json.loads(reader.read())

    session = Session(manager.engine)

    events = [
        Event(
            start_date=datetime.datetime.fromisoformat(data["start_date"]),
            end_date=datetime.datetime.fromisoformat(data["end_date"]),
            location=data["location"],
            attendees_count=data["attendees_count"],
            notes=data["notes"],
            support_contact_id=data["support_contact_id"],
            contract_id=data["contract_id"],
        )
        for data in events_data
    ]

    session.add_all(events)
    session.commit()


@cli.command
def init():
    """
    reset the database tables and insert demos datas
    """

    if pwinput("password: ") != DATABASE_PASSWORD:
        print("Invalid password")
        return

    manager.drop_tables()
    manager.create_tables()

    create_employees()
    create_clients()
    create_contracts()
    create_events()
