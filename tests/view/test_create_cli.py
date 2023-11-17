import sqlalchemy
from sqlalchemy.orm import Session
from click.testing import CliRunner

from models.employees import Employee, Department
from models.clients import Client
from models.contracts import Contract
from models.events import Event
from view.create import generic_create
from view import cli


def test_create_employee(database_mock, session: Session, login_as_accounting):

    with database_mock, login_as_accounting:

        runner = CliRunner()
        result = runner.invoke(cli, args=[
            "create", "employees",
            "--email", "valid.email@example.co",
            "--password", "password",
            "--fullname", "valid, Fullname",
            "--department", "sales",
        ])

        created_object = session.scalar(
            sqlalchemy.select(Employee)
            .where(Employee.email == "valid.email@example.co")
        )

        assert created_object.department == Department.SALES
        assert "valid.email@example.co" in result.output

        runner = CliRunner()
        result = runner.invoke(cli, args=[
            "create", "employees",
            "--email", "invalid_email",
            "--password", "password",
            "--fullname", "valid, Fullname",
            "--department", "sales",
        ])

        assert "Invalid email" in str(result.exception)


def test_create_clients(database_mock, session: Session, login_as_sales):

    with database_mock, login_as_sales:
        # email, fullname, phone, enterprise
        runner = CliRunner()
        result = runner.invoke(cli, args=[
            "create", "clients",
            "--email", "valid.email@example.co",
            "--fullname", "valid, Fullname",
            "--phone", "0607080910",
            "--enterprise", "dummy enterprise"
        ])

        created_object = session.scalar(
            sqlalchemy.select(Client)
            .where(Client.email == "valid.email@example.co")
        )

        assert created_object.phone == "0607080910"
        assert "valid.email@example.co" in result.output


def test_create_contract(database_mock, session: Session, login_as_accounting):

    with database_mock, login_as_accounting:
        runner = CliRunner()
        result = runner.invoke(cli, args=[
            "create", "contracts",
            "--client_id", "1",
            "--total", "99",
            "--to_be_paid", "99",
            "--signed", "0",
        ])

        created_object = session.scalar(
            sqlalchemy.select(Contract)
            .where(Contract.id == 11)
        )

        assert created_object.client_id == 1
        assert created_object.account_contact_id == 2
        assert "total_amount" in result.output


def test_create_event(database_mock, session: Session, login_as_sales):

    with database_mock, login_as_sales:
        runner = CliRunner()
        result = runner.invoke(cli, args=[
            "create", "events",
            "--start", "2023-11-17",
            "--end", "2023-11-18",
            "--location", "dummy location",
            "--attendees", "50",
            "--contract_id", "2",
            "--support_id", "3",
            "--notes", "dummy notes",
        ])

        created_object = session.scalar(
            sqlalchemy.select(Event)
            .where(Event.id == 11)
        )

        print("\n", result.output)

        assert created_object.location == "dummy location"
        assert "dummy location" in result.output
